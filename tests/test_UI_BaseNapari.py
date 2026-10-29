"""Teste les références partagées et les gardes Qt de la base des widgets Napari."""

from importlib import import_module

import pytest
from napari.components import ViewerModel
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QDockWidget, QMainWindow

from palm_tracer.PALMTracer import PALMTracer
from palm_tracer.UI import BaseNapariWidget


# --------------------------------------------------
class _DummyLayer:
	"""Simule un calque et mémorise sa visibilité lors des affectations."""

	visible: bool  #: Visibilité courante du calque.
	data: str  #: Données représentées par le calque simulé.
	invalid_property: str  #: Propriété dont l'affectation doit échouer.
	updates_visibility: list[bool]  #: Visibilité observée lors de chaque mise à jour.
	face_color: str  #: Couleur affectée par la mise à jour du calque.
	blending: str  #: Mode de mélange affecté par la mise à jour du calque.

	# --------------------------------------------------
	def __init__(self, visible: bool, invalid_property: str = ""):
		"""
		Initialise le calque avec l'état demandé.

		:param visible: Visibilité initiale du calque.
		:param invalid_property: Nom de la propriété dont l'affectation doit échouer.
		"""
		object.__setattr__(self, "visible", visible)
		object.__setattr__(self, "data", "old-data")
		object.__setattr__(self, "invalid_property", invalid_property)
		object.__setattr__(self, "updates_visibility", [])

	# --------------------------------------------------
	def __setattr__(self, name, value):
		"""Mémorise la visibilité courante ou refuse la propriété utilisée pour simuler une erreur."""
		if name == self.invalid_property:
			raise ValueError("Invalid property")
		if name != "visible": self.updates_visibility.append(self.visible)
		object.__setattr__(self, name, value)


# ==================================================
# region Initialisation
# ==================================================
@pytest.mark.parametrize("shared", [False, True], ids=["new-instance", "shared-instance"])
def test_initialization_preserves_references(qtbot, monkeypatch, shared):
	"""Vérifie l'identité des références et l'absence de création supplémentaire en mode partagé."""
	viewer, pt = ViewerModel(), PALMTracer()
	created = []

	# --------------------------------------------------
	def create_palmtracer():
		"""Observe la création de l'instance par défaut."""
		created.append(pt)
		return pt

	monkeypatch.setattr(import_module("palm_tracer.UI.BaseWidget"), "PALMTracer", create_palmtracer)
	widget = BaseNapariWidget(viewer, pt if shared else None)
	qtbot.addWidget(widget)

	assert widget.viewer is viewer
	assert widget.pt is pt
	assert len(created) == (0 if shared else 1)


# ==================================================
# endregion Initialisation
# ==================================================

# ==================================================
# region Glisser-déposer
# ==================================================
@pytest.mark.parametrize("floating", [False, True], ids=["docked", "floating"])
def test_drop_target_preserves_root_window(qtbot, floating):
	"""Vérifie que la fenêtre Napari reste la cible lorsque le dock est détaché."""
	window = QMainWindow()
	qtbot.addWidget(window)
	dock = QDockWidget(window)
	widget = BaseNapariWidget(ViewerModel())
	dock.setWidget(widget)
	window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
	window.show()
	dock.setFloating(floating)

	assert widget._get_drop_target() is window
	assert widget._drop_window is window


# ==================================================
# endregion Glisser-déposer
# ==================================================

# ==================================================
# region Calques
# ==================================================
@pytest.mark.parametrize("initial_visibility, visible, expected_visibility", [
		pytest.param(False, None, False, id="preserve-hidden"),
		pytest.param(True, None, True, id="preserve-visible"),
		pytest.param(False, True, True, id="force-visible"),
		pytest.param(True, False, False, id="force-hidden")])
def test_update_layer(initial_visibility, visible, expected_visibility):
	"""Vérifie la mise à jour du calque et les différentes politiques de visibilité."""
	layer = _DummyLayer(initial_visibility)
	BaseNapariWidget.update_layer(layer, "new-data", visible, face_color="lime", blending="translucent")

	assert layer.data == "new-data"
	assert layer.face_color == "lime"
	assert layer.blending == "translucent"
	assert layer.updates_visibility == [True, True, True]
	assert layer.visible is expected_visibility


# --------------------------------------------------
def test_update_layer_restores_visibility_on_error():
	"""Vérifie la restauration de la visibilité lorsqu'une propriété ne peut pas être affectée."""
	layer = _DummyLayer(False, "invalid")
	with pytest.raises(ValueError, match="Invalid property"): BaseNapariWidget.update_layer(layer, "new-data", invalid=True)
	assert layer.visible is False

# ==================================================
# endregion Calques
# ==================================================
