"""Fichier des tests pour le widget."""
import pytest
from qtpy.QtCore import Qt

from palm_tracer._tests.Utils import *
from palm_tracer.Settings.Types import BaseUI, ButtonGroup, Combo
from palm_tracer.UI import BasePlotlyWidget, GraphViewerWidget

OUTPUT_DIR = INPUT_DIR / "stack_PALM_Tracer"
SIZE_X, SIZE_Y, INTENSITY, RATIO = 100, 50, 1000, 10
SIZE = int(SIZE_X * np.sqrt(SIZE_Y))
POINTS = np.stack([rng.uniform(1, SIZE_Y - 1, size=SIZE), rng.uniform(1, SIZE_X - 1, size=SIZE)], axis=1)


##################################################
@pytest.fixture
def w() -> GraphViewerWidget:
	"""Instance fraîche de GraphViewerWidget pour chaque test."""
	pt = get_fake_pt()
	w = GraphViewerWidget(pt)
	return w


##################################################
def test_widget_creation(w: GraphViewerWidget, qtbot):
	"""Test basique de création du widget."""
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)
	w.close()


##################################################
def test_add_stack(w: GraphViewerWidget, qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Test d'ajout du'ne pile."""
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	fake_qfiledialog(BasePlotlyWidget, f"{INPUT_DIR / 'stack.tif'}")
	qtbot.mouseClick(w._btn_add_stack, Qt.MouseButton.LeftButton)

	w.close()


##################################################
def test_change_type(w: GraphViewerWidget, qtbot):
	"""Test basique de création du widget."""
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	ui: BaseUI = cast(ButtonGroup, w._pt.settings.graph["Type"]).get_ui(w.UI_NAME)
	qtbot.mouseClick(ui.boxes[0], Qt.MouseButton.LeftButton)  # Appuie sur localization
	assert w._pt.settings.graph["Type"].value == 0
	qtbot.mouseClick(ui.boxes[1], Qt.MouseButton.LeftButton)  # Appuie sur Tracks
	assert w._pt.settings.graph["Type"].value == 1

	w.close()


###################################################
def test_update_plot_localization(w: GraphViewerWidget, qtbot, capsys):
	"""Test de différentes visualizations."""
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	s = w._pt.settings.graph
	ui: BaseUI = cast(ButtonGroup, s["Type"]).get_ui(w.UI_NAME)
	qtbot.mouseClick(ui.boxes[0], Qt.MouseButton.LeftButton)  # Appuie sur localization
	assert w._pt.settings.graph["Type"].value == 0

	# Changement de source
	s["Source"].value = 1  # Changement de graph
	s["Source"].value = len(cast(Combo, s["Source"]).items) - 1  # Localisation Count est un affichage Scatter Plot

	# Dual View
	s["Dual"].value = True
	s["Source"].value = 1
	s["Source B"].value = 2

	w.close()
