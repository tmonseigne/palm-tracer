"""Définit les comportements et notifications communs aux widgets Qt."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import cast

from qtpy.compat import isalive
from qtpy.QtCore import QEvent, QObject, Qt, Signal, Slot
from qtpy.QtGui import QContextMenuEvent, QCursor, QDropEvent, QHideEvent, QResizeEvent, QShowEvent
from qtpy.QtWidgets import QApplication, QDockWidget, QMenu, QWidget
from superqt.utils import FunctionWorker

from palm_tracer.PALMTracer import PALMTracer
from palm_tracer.Tools import Ui
from palm_tracer.UI.NotificationWidget import NotificationLevel, NotificationWidget


# --------------------------------------------------
class BaseWidget(QWidget):
	"""
	Intercepte les fichiers déposés dans toute la fenêtre Qt contenant le widget.

	Le titre et le style Qt commun sont initialisés pour les fenêtres autonomes comme pour les panneaux intégrés.
	La cible comprend les widgets enfants et la fenêtre Napari éventuelle, même lorsque le dock est flottant.
	Les classes filles doivent définir l'action du dépôt dans :meth:`_drop_files`.
	La base reste instanciable ; appeler l'action sans la redéfinir lève :class:`NotImplementedError`.

	:param parent: Widget Qt parent, ou :obj:`None` pour une fenêtre autonome.
	:param palmtracer: Instance partagée conservée sans copie, ou :obj:`None` pour en créer une.
	"""

	UI_NAME: str = ""
	"""Nom de l'interface, à redéfinir dans chaque classe fille."""
	DROP_MULTIPLE: bool = True
	"""Autorise plusieurs URL par dépôt ; les outils limités à un fichier redéfinissent cette constante."""
	DROP_EXTENSIONS: tuple[str, ...] = ()
	"""Extensions de fichiers autorisées en minuscules ; un tuple vide ne limite pas les extensions."""
	DROP_DIRECTORIES: bool = False
	"""Accepte les dossiers en plus des fichiers autorisés."""
	_standalone_windows: dict[int, BaseWidget] = {}
	"""Références des fenêtres autonomes conservées jusqu'à leur destruction par Qt."""
	_notification_requested = Signal(str, str, int)
	"""Transmet les demandes de notification au thread graphique, y compris depuis un worker."""

	# ==================================================
	# region Initialisation
	# ==================================================
	def __init__(self, parent: QWidget | None = None, palmtracer: PALMTracer | None = None):
		"""
		Conserve ou crée l'instance métier et initialise l'identité, le style Qt et l'état du filtre de dépôt.

		:param parent: Widget Qt parent, ou :obj:`None` pour une fenêtre autonome.
		:param palmtracer: Instance partagée, ou :obj:`None` pour en créer une.
		"""
		super().__init__(parent)
		self.pt: PALMTracer = PALMTracer() if palmtracer is None else palmtracer  # Instance fournie sans copie ou créée pour ce widget.
		self._notification: NotificationWidget | None = None  # Notification unique, créée seulement au premier message.
		self.setWindowTitle(self.UI_NAME)
		self.setStyleSheet(Ui.STYLESHEET_COMMON)
		self._drop_window: QWidget | None = None  # .		 	Fenêtre Qt dont les dépôts sont interceptés.
		self._drop_accepts: bool = False  # .				 	État initial à restaurer lors du masquage.
		self._context_menu_exclusions: list[QWidget] = []  # .	Vues conservant exclusivement leur propre menu contextuel.
		self._notification_requested.connect(self._show_notification)
		self._processing: bool = False  # .						Traitement et éventuelle finalisation encore actifs.
		self._worker: FunctionWorker | None = None  # .			Conserve le worker jusqu'à son signal de fin.
		self._post_process: Callable[[], None] | None = None  # Mise à jour exécutée uniquement après réussite, sur le thread Qt.
		self._processing_was_enabled: bool = True  # .			État à restaurer après le traitement.

	# ==================================================
	# endregion Initialisation
	# ==================================================

	# ==================================================
	# region Fenêtres autonomes
	# ==================================================
	def show_standalone(self, width: int = 1280, height: int = 720):
		"""
		Dimensionne et affiche une fenêtre autonome en conservant sa référence jusqu'à sa destruction.

		La fermeture détruit la fenêtre et libère sa référence commune. Les appels répétés n'ajoutent
		ni référence ni connexion supplémentaire. Les panneaux intégrés restent gérés par leur conteneur.

		:param width: Largeur initiale en pixels logiques.
		:param height: Hauteur initiale en pixels logiques.
		"""
		identity = id(self)
		if identity not in BaseWidget._standalone_windows:
			BaseWidget._standalone_windows[identity] = self
			# Capture uniquement l'identifiant pour ne pas retenir la fenêtre dans son propre callback.
			self.destroyed.connect(lambda: BaseWidget._standalone_windows.pop(identity, None))
		self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
		self.resize(width, height)
		self.show()

	# ==================================================
	# endregion Fenêtres autonomes
	# ==================================================

	# ==================================================
	# region Threads
	# ==================================================
	@property
	def processing(self) -> bool:
		"""Indique si un calcul ou sa finalisation est encore en cours pour ce widget."""
		return self._processing

	# --------------------------------------------------
	def _thread_process(self, compute_func: Callable[[], None], post_func: Callable[[], None] | None = None):
		"""
		Lance un calcul dans un worker et désactive temporairement les interactions du widget.

		Une demande reçue pendant un traitement est ignorée, sans annulation ni mise en attente.
		Le calcul ne doit accéder à aucun widget ou calque ; la finalisation est exécutée dans le thread graphique.
		Les préconditions métier sont vérifiées par le calcul ou par son appelant, indépendamment de cette base Qt.

		:param compute_func: Calcul sans argument à exécuter en arrière-plan.
		:param post_func: Mise à jour sans argument à exécuter après réussite, avant la réactivation du widget.
		"""
		if self._processing: return
		self._processing = True
		self._post_process = post_func
		self._freeze_ui(True)
		try:
			worker = FunctionWorker(compute_func)
			self._worker = worker
			worker.returned.connect(self._process_returned)
			worker.errored.connect(self._process_failed)
			worker.finished.connect(self._process_done)
			worker.start()
		except Exception as error:
			self._process_done()
			self._process_failed(error)

	# --------------------------------------------------
	@Slot(object)
	def _process_returned(self, _result: object):
		"""
		Exécute la finalisation du calcul réussi depuis le thread graphique.

		:param _result: Valeur transmise par le worker et ignorée par cette interface de calcul sans retour.
		"""
		try:
			if self._post_process is not None: self._post_process()
		except Exception as error:
			self._process_failed(error)
			return

	# --------------------------------------------------
	@Slot(object)
	def _process_failed(self, error: Exception):
		"""
		Signale une erreur de calcul, de démarrage ou de finalisation dans le panneau concerné.

		:param error: Exception remontée par le worker ou par sa finalisation.
		"""
		self.notify_error(f"Error in thread: {error}")

	# --------------------------------------------------
	@Slot()
	def _process_done(self):
		"""Libère le traitement terminé et restaure les interactions et le curseur du widget."""
		if not self._processing: return
		self._worker = None
		self._post_process = None
		self._freeze_ui(False)
		self._processing = False

	# --------------------------------------------------
	def _freeze_ui(self, on: bool):
		"""
		Grise le widget sans bloquer les rafraîchissements et impose le curseur d'attente dans l'application.

		Le curseur global reste visible sur les panneaux désactivés et les enfants ayant leur propre curseur.
		Chaque traitement empile un curseur d'attente et le dépile à sa fin ; les autres panneaux restent utilisables.

		:param on: Active le curseur d'attente et désactive le panneau, ou restaure son état initial.
		"""
		if on:
			self._processing_was_enabled = not self.testAttribute(Qt.WidgetAttribute.WA_ForceDisabled)
			QApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
			self.setEnabled(False)
		else:
			self.setEnabled(self._processing_was_enabled)
			QApplication.restoreOverrideCursor()

	# ==================================================
	# endregion Threads
	# ==================================================

	# ==================================================
	# region Notifications
	# ==================================================
	def notify(self, message: str, level: NotificationLevel = "info", duration_ms: int = 3000):
		"""
		Conserve le message dans la console et demande une notification locale sans accéder aux widgets depuis un worker.

		Le message suivant remplace le précédent. L'affichage Qt est délégué au thread graphique par un signal.
		Les messages provenant du moteur de calcul ne sont pas interceptés globalement.

		:param message: Texte brut du message.
		:param level: Niveau d'information, de succès, d'avertissement ou d'erreur.
		:param duration_ms: Délai avant fondu en millisecondes ; zéro demande une fermeture manuelle.
		:raises ValueError: Si le niveau est inconnu ou le délai négatif.
		"""
		if level not in ("info", "success", "warning", "error") or duration_ms < 0:
			raise ValueError("Niveau de notification inconnu ou délai négatif.")
		if level == "warning": Ui.print_warning(message)
		elif level == "error": Ui.print_error(message)
		elif level == "success": Ui.print_success(message)
		else: print(message)
		self._notification_requested.emit(message, level, duration_ms)

	# --------------------------------------------------
	def notify_info(self, message: str, duration_ms: int = 3000):
		"""
		Affiche une information locale avec disparition automatique.

		:param message: Texte brut du message.
		:param duration_ms: Délai avant fondu ; zéro conserve le message jusqu'à sa fermeture manuelle.
		"""
		self.notify(message, "info", duration_ms)

	# --------------------------------------------------
	def notify_success(self, message: str, duration_ms: int = 3000):
		"""
		Affiche la réussite d'une opération dans le panneau courant.

		:param message: Texte brut du message.
		:param duration_ms: Délai avant fondu ; zéro conserve le message jusqu'à sa fermeture manuelle.
		"""
		self.notify(message, "success", duration_ms)

	# --------------------------------------------------
	def notify_warning(self, message: str, duration_ms: int = 3000):
		"""
		Affiche un avertissement local sans ouvrir de dialogue bloquant.

		:param message: Texte brut du message.
		:param duration_ms: Délai avant fondu ; zéro conserve le message jusqu'à sa fermeture manuelle.
		"""
		self.notify(message, "warning", duration_ms)

	# --------------------------------------------------
	def notify_error(self, message: str, duration_ms: int = 3000):
		"""
		Affiche une erreur locale sans ouvrir de dialogue bloquant.

		:param message: Texte brut du message.
		:param duration_ms: Délai avant fondu ; zéro conserve le message jusqu'à sa fermeture manuelle.
		"""
		self.notify(message, "error", duration_ms)

	# --------------------------------------------------
	@Slot(str, str, int)
	def _show_notification(self, message: str, level: str, duration_ms: int):
		"""
		Crée ou remplace la notification depuis le thread graphique.

		Les messages reçus lorsque le panneau est masqué restent dans la console sans créer de notification invisible.

		:param message: Texte brut du message.
		:param level: Niveau préalablement validé par :meth:`notify`.
		:param duration_ms: Délai avant fondu, en millisecondes.
		"""
		if not self.isVisible(): return
		if self._notification is None: self._notification = NotificationWidget(self)
		self._notification.show_message(message, cast(NotificationLevel, level), duration_ms)

	# --------------------------------------------------
	def resizeEvent(self, event: QResizeEvent):
		"""
		Maintient la notification dans le coin du panneau lorsque sa taille change.

		:param event: Événement de redimensionnement Qt.
		"""
		super().resizeEvent(event)
		if self._notification is not None: self._notification.reposition()

	# ==================================================
	# endregion Notifications
	# ==================================================

	# ==================================================
	# region Menu contextuel
	# ==================================================
	def _get_always_on_top_target(self) -> QWidget | None:
		"""
		Retourne la fenêtre autonome ou le dock flottant contenant le widget.

		Un panneau docké ne doit pas modifier les propriétés de la fenêtre Napari qui l'héberge.

		:return: Fenêtre pouvant rester au premier plan, ou :obj:`None` pour un panneau intégré.
		"""
		if self.isWindow(): return self
		parent = self.parentWidget()
		while parent is not None:
			if isinstance(parent, QDockWidget): return parent if parent.isFloating() else None
			parent = parent.parentWidget()
		return None

	# --------------------------------------------------
	def _set_always_on_top(self, enabled: bool):
		"""
		Change le maintien au premier plan sans déplacer ni réafficher une fenêtre initialement masquée.

		:param enabled: Active le maintien au premier plan de la fenêtre autonome ou du dock flottant.
		"""
		window = self._get_always_on_top_target()
		if window is None: return
		if bool(window.windowFlags() & Qt.WindowType.WindowStaysOnTopHint) == enabled: return
		geometry, visible = window.geometry(), window.isVisible()
		# Qt masque la fenêtre lorsque ses attributs de fenêtre sont modifiés.
		window.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, enabled)
		window.setGeometry(geometry)
		if visible: window.show()

	# --------------------------------------------------
	def contextMenuEvent(self, event: QContextMenuEvent):
		"""
		Propose une case de maintien au premier plan depuis le panneau du widget uniquement.

		Les vues exclues conservent leur menu contextuel. Un panneau docké affiche l'option désactivée,
		car son maintien individuel au premier plan nécessite un détachement préalable.

		:param event: Demande de menu contextuel par la souris ou le clavier.
		"""
		child = QApplication.focusWidget() if event.reason() == QContextMenuEvent.Reason.Keyboard else self.childAt(event.pos())
		if child is not None and any(isalive(view) and (view is child or view.isAncestorOf(child)) for view in self._context_menu_exclusions):
			event.ignore()
			return
		window = self._get_always_on_top_target()
		menu = QMenu(self)
		action = menu.addAction("Always on top")
		action.setCheckable(True)
		action.setChecked(window is not None and bool(window.windowFlags() & Qt.WindowType.WindowStaysOnTopHint))
		action.setEnabled(window is not None)
		action.toggled.connect(self._set_always_on_top)
		try: menu.exec(event.globalPos())
		finally: menu.deleteLater()
		event.accept()

	# ==================================================
	# endregion Menu contextuel
	# ==================================================

	# ==================================================
	# region Glisser-déposer
	# ==================================================
	def _get_drop_target(self) -> QWidget:
		"""
		Retourne la racine Qt, y compris lorsque le widget appartient à un dock flottant.

		:return: Fenêtre délimitant toute la zone de dépôt.
		"""
		window: QWidget = self
		while window.parentWidget() is not None: window = window.parentWidget()
		return window

	# --------------------------------------------------
	def showEvent(self, event: QShowEvent):
		"""
		Active l'interception après l'insertion du widget dans sa fenêtre Qt.

		:param event: Événement d'affichage Qt.
		"""
		super().showEvent(event)
		if self._drop_window is not None and isalive(self._drop_window): return
		window = self._get_drop_target()
		self._drop_window = window
		self._drop_accepts = window.acceptDrops()
		window.setAcceptDrops(True)
		QApplication.instance().installEventFilter(self)

	# --------------------------------------------------
	def hideEvent(self, event: QHideEvent):
		"""
		Retire le filtre et restaure les dépôts si la fenêtre Qt existe encore.

		:param event: Événement de masquage Qt.
		"""
		QApplication.instance().removeEventFilter(self)
		if self._notification is not None and isalive(self._notification): self._notification.dismiss()
		window = self._drop_window
		self._drop_window = None
		# Qt peut détruire la fenêtre avant de masquer ses widgets enfants.
		if window is not None and isalive(window): window.setAcceptDrops(self._drop_accepts)
		super().hideEvent(event)

	# --------------------------------------------------
	def eventFilter(self, watched: QObject, event: QEvent) -> bool:
		"""
		Intercepte les fichiers locaux dans toute la fenêtre et délègue leur traitement.

		Les autres fenêtres et les glissements sans fichier local restent inchangés.
		Un dépôt local invalide est consommé, mais refusé avant son traitement habituel.

		:param watched: Objet Qt destinataire de l'événement.
		:param event: Événement à filtrer.
		:return: ``True`` si l'événement est consommé.
		"""
		if event.type() not in (QEvent.Type.DragEnter, QEvent.Type.DragMove, QEvent.Type.Drop): return False
		window = self._drop_window
		if window is None or not isalive(window) or not isinstance(watched, QWidget): return False
		if watched is not window and not window.isAncestorOf(watched): return False
		drop = cast(QDropEvent, event)
		urls = drop.mimeData().urls()
		paths = [url.toLocalFile() for url in urls if url.isLocalFile()]
		if not paths: return False
		valid_paths = all((Path(path).is_file() and (not self.DROP_EXTENSIONS or Path(path).suffix.lower() in self.DROP_EXTENSIONS))
						  or (self.DROP_DIRECTORIES and Path(path).is_dir()) for path in paths)
		if self._processing or (not self.DROP_MULTIPLE and len(urls) != 1) or not valid_paths:
			drop.ignore()
			return True
		# Copy décrit l'ajout des chemins ; aucun fichier source n'est déplacé.
		drop.setDropAction(Qt.DropAction.CopyAction)
		drop.accept()
		if event.type() == QEvent.Type.Drop: self._drop_files(paths)
		return True

	# --------------------------------------------------
	def _drop_files(self, paths: list[str]):
		"""
		Traite les fichiers acceptés ; à redéfinir dans chaque classe fille recevant des dépôts.

		:param paths: Chemins locaux du dépôt validé.
		:raises NotImplementedError: Si la classe fille ne définit pas le traitement du dépôt.
		"""
		raise NotImplementedError("Le widget doit définir le traitement des fichiers déposés.")

# ==================================================
# endregion Glisser-déposer
# ==================================================
