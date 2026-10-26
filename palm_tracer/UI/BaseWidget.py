"""Définit l'identité, le style et le glisser-déposer communs aux widgets Qt."""

from __future__ import annotations

from pathlib import Path
from typing import cast

from qtpy.compat import isalive
from qtpy.QtCore import QEvent, QObject, Qt
from qtpy.QtGui import QContextMenuEvent, QDropEvent, QHideEvent, QShowEvent
from qtpy.QtWidgets import QApplication, QDockWidget, QMenu, QWidget

from palm_tracer.Tools import Ui


# --------------------------------------------------
class BaseWidget(QWidget):
	"""
	Intercepte les fichiers déposés dans toute la fenêtre Qt contenant le widget.

	Le titre et le style Qt commun sont initialisés pour les fenêtres autonomes comme pour les panneaux intégrés.
	La cible comprend les widgets enfants et la fenêtre Napari éventuelle, même lorsque le dock est flottant.
	Les classes filles doivent définir l'action du dépôt dans :meth:`_drop_files`.
	La base reste instanciable ; appeler l'action sans la redéfinir lève :class:`NotImplementedError`.

	:param parent: Widget Qt parent, ou :obj:`None` pour une fenêtre autonome.
	"""

	UI_NAME: str = ""
	"""Nom de l'interface, à redéfinir dans chaque classe fille."""
	DROP_MULTIPLE: bool = True
	"""Autorise plusieurs URL par dépôt ; les outils limités à un fichier redéfinissent cette constante."""
	DROP_EXTENSIONS: tuple[str, ...] = ()
	"""Extensions de fichiers autorisées en minuscules ; un tuple vide ne limite pas les extensions."""
	DROP_DIRECTORIES: bool = False
	"""Accepte les dossiers en plus des fichiers autorisés."""

	# ==================================================
	# region Initialisation
	# ==================================================
	def __init__(self, parent: QWidget | None = None):
		"""
		Initialise l'identité, le style Qt et l'état du filtre de dépôt.

		:param parent: Widget Qt parent, ou :obj:`None` pour une fenêtre autonome.
		"""
		super().__init__(parent)
		self.setWindowTitle(self.UI_NAME)
		self.setStyleSheet(Ui.STYLESHEET_COMMON)
		self._drop_window: QWidget | None = None  # .		 Fenêtre Qt dont les dépôts sont interceptés.
		self._drop_accepts: bool = False  # .				 État initial à restaurer lors du masquage.
		self._context_menu_exclusions: list[QWidget] = []  # Vues conservant exclusivement leur propre menu contextuel.

	# ==================================================
	# endregion Initialisation
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
		if (not self.DROP_MULTIPLE and len(urls) != 1) or not valid_paths:
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
