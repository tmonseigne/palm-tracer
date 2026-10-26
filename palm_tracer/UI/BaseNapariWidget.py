"""Définit les références et les utilitaires de calques communs aux widgets Napari de PALM Tracer."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import napari

from palm_tracer.PALMTracer import PALMTracer
from palm_tracer.UI.BaseWidget import BaseWidget

if TYPE_CHECKING:
	from napari.layers import Layer


# --------------------------------------------------
class BaseNapariWidget(BaseWidget):
	"""
	Partage les références et l'interception des dépôts dans une fenêtre Napari.

	Les classes filles définissent leurs noms de calques et le traitement des fichiers déposés.

	:param viewer: Visionneuse Napari utilisée sans copie.
	:param palmtracer: Instance PALMTracer partagée, ou :obj:`None` pour en créer une.
	"""

	LAYERS_NAME: list[str] = []
	"""Noms des calques, à redéfinir dans chaque classe fille."""
	LAYER_ARGS: dict[str, dict[str, Any]] = {
			"Present":  {"border": 0.4, "edge": 0.5, "color": "lime", "face": "lime", "size": 1.0},
			"Filtered": {"border": 0.2, "edge": 0.5, "color": "red", "face": "red", "size": 1.0},
			"Past":     {"border": 0.2, "edge": 0.5, "color": "cyan", "face": "transparent", "size": 1.0},
			"Future":   {"border": 0.2, "edge": 0.5, "color": "orange", "face": "transparent", "size": 1.0}}
	"""Styles communs des points et des contours de ROI ; les classes filles peuvent les redéfinir."""

	# ==================================================
	# region Initialisation
	# ==================================================
	def __init__(self, viewer: napari.Viewer, palmtracer: PALMTracer | None = None):
		"""
		Conserve les références partagées et initialise la base Qt.

		:param viewer: Visionneuse Napari recevant les calques du widget.
		:param palmtracer: Instance partagée, ou :obj:`None` pour en créer une.
		"""
		super().__init__()
		self.viewer = viewer  # .										Conservation du lien vers le Viewer Napari
		self.pt = PALMTracer() if palmtracer is None else palmtracer  # Récupération ou création d' l'objet PALMTracer

	# ==================================================
	# endregion Initialisation
	# ==================================================

	# ==================================================
	# region Calques
	# ==================================================
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
