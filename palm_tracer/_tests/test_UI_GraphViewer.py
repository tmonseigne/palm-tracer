"""Teste le widget de visualisation interactive des données PALM."""

import pytest
from qtpy.QtCore import QCoreApplication, QEvent, Qt

from palm_tracer._tests.Utils import *
from palm_tracer.Settings.Types import BaseUIType, ButtonGroup, Combo
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
def flush_qt_delete_events():
	"""Traite les événements Qt de suppression différée."""
	QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
	QCoreApplication.processEvents()


##################################################
def test_widget_creation(w: GraphViewerWidget, qtbot):
	"""Vérifie la création du widget."""
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)
	w.close()

##################################################
def test_results_status_automatic_update(w: GraphViewerWidget, qtbot):
	"""Vérifie que les statuts sont actualisés directement par Results."""
	qtbot.addWidget(w)
	results_ui = w._pt.results.get_ui(w.UI_NAME)

	w._pt.results.reset()
	assert results_ui._labels["Localizations"].text() == "No"

	w._pt.results["loc"] = pd.DataFrame(np.zeros((2, 1)))
	assert results_ui._labels["Localizations"].text() == "Yes (2 localizations)"




##################################################
def test_widget_double_creation(qtbot):
	"""Vérifie Permettant de gérer la création en doublon de la même UI."""

	"""Reproduit le cas où une UI Qt cachée dans un dict survit à la destruction C++."""
	pt = get_fake_pt()

	w = GraphViewerWidget(pt)
	w.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	w.close()
	flush_qt_delete_events()

	# Ici les BaseUI sont encore dans les settings, mais leurs objets Qt internes peuvent être supprimés côté C++.
	w2 = GraphViewerWidget(pt)
	w2.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
	w2.resize(1000, 600)
	w2.show()
	qtbot.waitExposed(w2)
	w2.close()
	flush_qt_delete_events()


##################################################
def test_add_stack(w: GraphViewerWidget, qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Vérifie l'ajout d'une pile."""
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	fake_qfiledialog(BasePlotlyWidget, f"{INPUT_DIR / 'stack.tif'}")
	qtbot.mouseClick(w._btn_add_stack, Qt.MouseButton.LeftButton)

	w.close()


##################################################
def test_change_type(w: GraphViewerWidget, qtbot):
	"""Vérifie la création du widget."""
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	ui: BaseUIType = cast(ButtonGroup, w._pt.settings.graph["Type"]).get_ui(w.UI_NAME)
	qtbot.mouseClick(ui.boxes[0], Qt.MouseButton.LeftButton)  # Appuie sur localization
	assert w._pt.settings.graph["Type"].value == 0
	qtbot.mouseClick(ui.boxes[1], Qt.MouseButton.LeftButton)  # Appuie sur Tracks
	assert w._pt.settings.graph["Type"].value == 1

	w.close()


###################################################
def test_update_plot_localization(w: GraphViewerWidget, qtbot, capsys):
	"""Vérifie différentes visualizations."""
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	s = w._pt.settings.graph
	ui: BaseUIType = cast(ButtonGroup, s["Type"]).get_ui(w.UI_NAME)
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
