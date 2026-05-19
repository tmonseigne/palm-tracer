"""Fichier des tests pour le widget."""
import pytest
from qtpy.QtCore import Qt

from palm_tracer._tests.Utils import *
from palm_tracer.Settings.Types import ButtonGroup, Combo
from palm_tracer.Settings.Types.BaseUI import BaseUI
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


###################################################
def test_get_data(w: GraphViewerWidget, qtbot, capsys):
	"""Test de différentes récupérations de données."""
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	ref_title: str
	ref_shape: tuple
	ref_data: list[int] | list[list[int]] | list[float] | list[list[float]]

	s = w._pt.settings.graph
	s["Type"].value = 0
	# Changement de source
	s["Source"].value = len(cast(Combo, s["Source"]).items) - 1  # Localisation Count est un affichage Scatter Plot

	# Classique
	data, title = w._get_data()
	ref_title, ref_shape, ref_data = "Localizations Count", (2, 2), [[1, 4], [2, 2]]
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# Double vue
	s["Dual"].value = True
	s["Source"].value = 1
	s["Source B"].value = 2
	data, title = w._get_data()
	ref_title, ref_shape, ref_data = "Localizations Sigma X / Sigma Y", (6, 2), [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1]]
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"

	# Colonne inexistante
	w._pt.localizations.drop("Sigma X", inplace=True, axis=1)
	data, title = w._get_data()
	ref_title, ref_shape, ref_data = "Localizations Sigma X / Sigma Y", (0,), []
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	w.close()


###################################################
def test_get_data_from_src(w: GraphViewerWidget, qtbot, capsys):
	"""Test de différentes récupérations de données."""
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	ref_title: str
	ref_shape: tuple
	ref_data: list[int] | list[list[int]] | list[float] | list[list[float]]

	# Localizations
	# Colonne inexistante
	data, title = w._get_data_from_src(0, "no column")
	ref_title, ref_shape, ref_data = "Localizations no column", (0,), []
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# Classique
	data, title = w._get_data_from_src(0, "X")
	ref_title, ref_shape, ref_data = "Localizations X", (6,), [1, 2, 3, 4, 1, 2]
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# Count
	data, title = w._get_data_from_src(0, "Localizations Count")
	ref_title, ref_shape, ref_data = "Localizations Count", (2, 2), [[1, 4], [2, 2]]
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# Empty
	for _ in range(4): w._pt.localizations.drop(w._pt.localizations.index, inplace=True)
	data, title = w._get_data_from_src(0, "X")
	ref_title, ref_shape, ref_data = "Localizations X", (0,), []
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"

	# Tracks
	# Colonne inexistante
	data, title = w._get_data_from_src(1, "no column")
	ref_title, ref_shape, ref_data = "Tracks no column", (0,), []
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# Length
	data, title = w._get_data_from_src(1, "Length")
	ref_title, ref_shape, ref_data = "Tracks Length", (9, 2), [[1, 98], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1], [9, 1]]
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# MSD
	w._graph_settings["MSD Step"].value = 5
	data, title = w._get_data_from_src(1, "MSD")
	ref_title, ref_shape, ref_data = "Tracks MSD Step 5", (1, 2), [[81, 0.14]]
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	w._graph_settings["MSD Step"].value = 9
	data, title = w._get_data_from_src(1, "MSD")
	ref_title, ref_shape, ref_data = "Tracks MSD Step 9", (0,), []
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# Instant D
	data, title = w._get_data_from_src(1, "Instant D")
	ref_title, ref_shape, ref_data = "Tracks Instant D", (27,), [4.51, 1.37, 3.04, 1.13, 1e-06, 1.99, 1e-06, 2.34, 0.81, 4.02, 4.26, 1.31, 6.37, 0.60,
																 2.22, 4.83, 0.27, 0.96, 5.41, 9.19, 0.60, 1.24, 0.54, 2.43, 2.23, 1.61, 3.05, ]
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# Fit
	data, title = w._get_data_from_src(1, "MSE(0)")
	ref_title, ref_shape, ref_data = "Tracks MSE(0)", (14, 2), [[35, 1], [37, 1], [66, 1], [75, 1], [81, 1], [83, 1], [102, 1], [114, 1],
																[131, 1], [152, 1], [158, 1], [165, 1], [176, 1], [220, 1]]
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# --- Empty ---
	for _ in range(4): w._pt.tracks.drop(w._pt.tracks.index, inplace=True)
	for _ in range(2):
		df = w._pt.tracks_compute
		for d in df.values(): d.drop(d.index, inplace=True)

	data, title = w._get_data_from_src(1, "Length")
	ref_title, ref_shape, ref_data = "Tracks Length", (0,), []
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	data, title = w._get_data_from_src(1, "MSD")
	ref_title, ref_shape, ref_data = "Tracks MSD", (0,), []
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	data, title = w._get_data_from_src(1, "Instant D")
	ref_title, ref_shape, ref_data = "Tracks Instant D", (0,), []
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	data, title = w._get_data_from_src(1, "MSE(0)")
	ref_title, ref_shape, ref_data = "Tracks MSE(0)", (0,), []
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# print(f"TEST \n{title} : {data.shape}\n{data}")
	w.close()
