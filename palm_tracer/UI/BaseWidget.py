"""Définit l'identité, le style et le glisser-déposer communs aux widgets Qt."""

from __future__ import annotations

from pathlib import Path
from typing import cast

from qtpy.compat import isalive
from qtpy.QtCore import QEvent, QObject, Qt
from qtpy.QtGui import QDropEvent, QHideEvent, QShowEvent
from qtpy.QtWidgets import QApplication, QWidget

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
		self._drop_window: QWidget | None = None  # Fenêtre Qt dont les dépôts sont interceptés.
		self._drop_accepts: bool = False  # .		État initial à restaurer lors du masquage.

	# ==================================================
	# endregion Initialisation
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
