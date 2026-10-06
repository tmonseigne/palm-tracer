"""Définit les références et le glisser-déposer communs aux widgets Napari de PALM Tracer."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

import napari
from qtpy.compat import isalive
from qtpy.QtCore import QEvent, QObject, Qt
from qtpy.QtGui import QDropEvent, QHideEvent, QShowEvent
from qtpy.QtWidgets import QApplication, QWidget

from palm_tracer.PALMTracer import PALMTracer

if TYPE_CHECKING:
	from napari.layers import Layer


##################################################
class BaseNapariWidget(QWidget):
	"""
	Partage les références et l'interception des dépôts dans une fenêtre Napari.

	Les classes filles définissent leurs noms de calques et le traitement des fichiers déposés.

	:param viewer: Visionneuse Napari utilisée sans copie.
	:param palmtracer: Instance PALMTracer partagée, ou :obj:`None` pour en créer une.
	"""

	UI_NAME: str = ""
	"""Nom de l'interface, à redéfinir dans chaque classe fille."""
	LAYERS_NAME: list[str] = []
	"""Noms des calques, à redéfinir dans chaque classe fille."""
	LAYER_ARGS: dict[str, dict[str, Any]] = {
			"Present":  {"border": 0.4, "edge": 0.5, "color": "lime", "face": "lime", "size": 1.0},
			"Filtered": {"border": 0.2, "edge": 0.5, "color": "red", "face": "red", "size": 1.0},
			"Past":     {"border": 0.2, "edge": 0.5, "color": "cyan", "face": "transparent", "size": 1.0},
			"Future":   {"border": 0.2, "edge": 0.5, "color": "orange", "face": "transparent", "size": 1.0}}
	"""Styles communs des points et des contours de ROI ; les classes filles peuvent les redéfinir."""
	DROP_MULTIPLE: bool = True
	"""Autorise plusieurs URL par dépôt ; les visualiseurs d'une seule pile redéfinissent cette constante."""

	# ==================================================
	# region Initialisation
	# ==================================================
	##################################################
	def __init__(self, viewer: napari.Viewer, palmtracer: PALMTracer | None = None):
		"""
		Conserve les références partagées et initialise l'état du filtre de dépôt.

		:param viewer: Visionneuse Napari recevant les calques du widget.
		:param palmtracer: Instance partagée, ou :obj:`None` pour en créer une.
		"""
		super().__init__()
		self.viewer = viewer  # .										Conservation du lien vers le Viewer Napari
		self.pt = PALMTracer() if palmtracer is None else palmtracer  # Récupération ou création d' l'objet PALMTracer
		self._drop_window: QWidget | None = None  # .					Fenêtre Qt dont les dépôts sont interceptés.
		self._drop_accepts: bool = False  # .							État initial à restaurer lors du masquage.

	# ==================================================
	# endregion Initialisation
	# ==================================================

	# ==================================================
	# region Glisser-déposer
	# ==================================================
	##################################################
	def _get_drop_target(self) -> QWidget:
		"""
		Retourne la racine Qt du plugin, y compris lorsque son dock est flottant.

		:return: Widget délimitant la zone de dépôt ; retourner ``self`` la limiterait au plugin.
		"""
		window: QWidget = self
		while window.parentWidget() is not None: window = window.parentWidget()
		return window

	##################################################
	def showEvent(self, event: QShowEvent):
		"""
		Active l'interception après l'insertion du plugin dans sa fenêtre Qt.

		:param event: Événement d'affichage Qt.
		"""
		super().showEvent(event)
		if self._drop_window is not None and isalive(self._drop_window): return
		window = self._get_drop_target()
		self._drop_window = window
		self._drop_accepts = window.acceptDrops()
		window.setAcceptDrops(True)
		QApplication.instance().installEventFilter(self)

	##################################################
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

	##################################################
	def eventFilter(self, watched: QObject, event: QEvent) -> bool:
		"""
		Intercepte les fichiers locaux dans la fenêtre cible et délègue leur traitement.

		Les autres fenêtres et les glissements sans fichier local restent inchangés.
		Un dépôt local invalide est consommé, mais refusé avant son traitement par Napari.

		:param watched: Objet Qt destinataire de l'événement.
		:param event: Événement à filtrer.
		:return: ``True`` si l'événement est consommé.
		"""
		if event.type() not in (QEvent.Type.DragEnter, QEvent.Type.DragMove, QEvent.Type.Drop): return False  # Sélection des évènement Drag and Drop.
		window = self._drop_window
		if window is None or not isalive(window) or not isinstance(watched, QWidget): return False
		if watched is not window and not window.isAncestorOf(watched): return False
		drop = cast(QDropEvent, event)
		urls = drop.mimeData().urls()
		paths = [url.toLocalFile() for url in urls if url.isLocalFile()]
		if not paths: return False
		if (not self.DROP_MULTIPLE and len(urls) != 1) or not any(Path(path).is_file() for path in paths) or not self._can_drop_files(paths):
			drop.ignore()
			return True
		# Copy décrit l'ajout des chemins ; aucun fichier source n'est déplacé.
		drop.setDropAction(Qt.DropAction.CopyAction)
		drop.accept()
		if event.type() == QEvent.Type.Drop: self._drop_files(paths)
		return True

	##################################################
	def _can_drop_files(self, paths: list[str]) -> bool:
		"""
		Indique si l'état du widget permet le dépôt ; les classes filles peuvent ajouter leurs contraintes.

		:param paths: Chemins locaux du dépôt contenant au moins un fichier existant.
		:return: ``True`` si le widget autorise le dépôt.
		"""
		return True

	##################################################
	def _drop_files(self, paths: list[str]):
		"""
		Traite les fichiers acceptés ; cette méthode doit être redéfinie dans chaque classe fille.

		:param paths: Chemins locaux du dépôt validé.
		:raises NotImplementedError: Si la classe fille ne définit pas le traitement du dépôt.
		"""
		raise NotImplementedError("Le widget doit définir le traitement des fichiers déposés.")

	# ==================================================
	# endregion Glisser-déposer
	# ==================================================

	# ==================================================
	# region Calques
	# ==================================================
	##################################################
	@staticmethod
	def update_layer(layer: Layer, data: Any, visible: bool | None = None, **properties: Any) -> None:
		"""
		Met à jour un calque Napari en le rendant temporairement visible.

		Ce contournement évite les erreurs de rendu pouvant survenir lors de la modification d'un calque masqué.
		Les données sont affectées avant les propriétés supplémentaires.
		À la fin de la mise à jour, la visibilité initiale est restaurée si le paramètre de visibilité vaut :obj:`None`, sinon l'état demandé est appliqué.

		:param layer: Calque Napari à mettre à jour.
		:param data: Nouvelles données du calque.
		:param visible: Visibilité finale, ou :obj:`None` pour conserver l'état initial.
		:param properties: Propriétés supplémentaires à affecter après les données.
		"""
		initial_visibility = layer.visible
		layer.visible = True
		try:
			layer.data = data
			for name, value in properties.items(): setattr(layer, name, value)
		finally: layer.visible = initial_visibility if visible is None else visible
