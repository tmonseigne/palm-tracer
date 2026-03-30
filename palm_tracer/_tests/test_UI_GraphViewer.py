"""Fichier des tests pour le widget."""

import pytest
from qtpy.QtCore import Qt

from palm_tracer._tests.Utils import *
from palm_tracer.Settings.Types import FileList
from palm_tracer.UI import BasePlotlyWidget, GraphViewerWidget

OUTPUT_DIR = INPUT_DIR / "stack_PALM_Tracer"
SIZE_X, SIZE_Y, INTENSITY, RATIO = 100, 50, 1000, 10
SIZE = int(SIZE_X * np.sqrt(SIZE_Y))
POINTS = np.stack([rng.uniform(1, SIZE_Y - 1, size=SIZE), rng.uniform(1, SIZE_X - 1, size=SIZE)], axis=1)


##################################################
def get_pt():
	"""Instance basique de PALMTracer pour chaque test."""
	pt = PALMTracer()
	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.update_box([f"{INPUT_DIR / 'stack.tif'}"])
	pt.df["loc"] = pd.read_csv(INPUT_DIR / "localizations.csv")
	pt.df["f_loc"] = pt.df["loc"].copy()
	pt.df["trc"] = pd.read_csv(INPUT_DIR / "tracking.csv")
	pt.df["f_trc"] = pt.df["trc"].copy()
	pt.df["blk"] = pt.df["trc"].copy()
	pt.df["f_blk"] = pt.df["trc"].copy()
	pt.df["MSD"] = pd.read_csv(INPUT_DIR / "tracking_MSD.csv")
	pt.df["InD"] = pd.read_csv(INPUT_DIR / "tracking_InstantD.csv")
	pt.df["Fit"] = pd.read_csv(INPUT_DIR / "tracking_Fit.csv")
	return pt


##################################################
@pytest.fixture
def w() -> GraphViewerWidget:
	"""Instance fraîche de GraphViewerWidget pour chaque test."""
	pt = get_pt()
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
	"""Test basique du widget."""
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	fake_qfiledialog(BasePlotlyWidget, f"{INPUT_DIR / 'stack.tif'}")
	qtbot.mouseClick(w._btn_add_stack, Qt.MouseButton.LeftButton)

	w.close()


##################################################
def test_actualize(w: GraphViewerWidget, qtbot):
	"""Test basique de création du widget."""
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	w._actualize()  # Actualize

	ref = w._filters["Plane"].value
	new_f = [2, 50]
	w._filters["Plane"].value = new_f
	assert w._filters["Plane"].value == new_f, "Filtre incorrect."
	w._actualize()
	assert w._filters["Plane"].value == ref, "Filtre incorrect."

	w.close()


##################################################
def test_reset_filtered(w: GraphViewerWidget, qtbot, capsys):
	"""Test basique de création du widget."""
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	for key, value in w._status.items(): print(f"{key}:{value.text()}")
	assert w._status["Localization"].text() == "Yes (Filtered)", "Status Incorrect."
	w._reset_filtered()
	for key, value in w._status.items(): print(f"{key}:{value.text()}")
	assert w._status["Localization"].text() == "Yes", "Status Incorrect."

	w.close()


##################################################
def test_update_filtered(w: GraphViewerWidget, qtbot, capsys):
	"""Test basique de création du widget."""
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	ref = w._filters["Plane"].value
	new_f = [2, 50]
	w._filters["Plane"].value = new_f
	assert w._filters["Plane"].value == new_f, "Filtre incorrect."
	assert w._pt.settings.filtering["Plane"].value == ref, "Filtre incorrect."
	w._update_filtered()
	assert w._pt.settings.filtering["Plane"].value == new_f, "Filtre incorrect."

	w.close()


##################################################
def test_update_plot(w: GraphViewerWidget, qtbot, capsys):
	"""Test basique de création du widget."""
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	# Plot pour la pile
	qtbot.mouseClick(w._btn_src["Stack"], Qt.MouseButton.LeftButton)
	assert w._btg_src.checkedId() == 0, "Index de la source incorrecte."
	w._update_plot()

	# Plot pour les localisations
	qtbot.mouseClick(w._btn_src["Localization"], Qt.MouseButton.LeftButton)
	assert w._btg_src.checkedId() == 1, "Index de la source incorrecte."
	assert w._cmb_src_a.value == 0, "Index de la donnée incorrecte."
	w._update_plot()

	w._cmb_src_a.value = 1
	assert w._cmb_src_a.value == 1, "Index de la donnée incorrecte."
	w._update_plot()

	# Plot pour les trajectoires
	qtbot.mouseClick(w._btn_src["Tracks"], Qt.MouseButton.LeftButton)
	assert w._btg_src.checkedId() == 2, "Index de la source incorrecte."
	w._update_plot()

	# Affichage de Instant D
	w._cmb_src_a.value = 2
	assert w._cmb_src_a.value == 2, "Index de la donnée incorrecte."
	w._update_plot()

	w.close()


##################################################
def test_dual_source(w: GraphViewerWidget, qtbot, capsys):
	"""Test basique du widget."""
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)
	ref_title: str
	ref_shape: tuple
	ref_data: list[int] | list[list[int]]

	qtbot.mouseClick(w._btn_src["Localization"], Qt.MouseButton.LeftButton)
	w._dual_source.value = True

	# Colonnes incompatibles pour le dual source
	qtbot.mouseClick(w._btn_src["Tracks"], Qt.MouseButton.LeftButton)  # Passage au tracking
	assert w._btg_src.checkedId() == 2, "Index de la source incorrecte."
	w._cmb_src_a.value = 0
	w._cmb_src_b.value = 1
	data, title = w._get_plot_data()
	ref_title, ref_shape, ref_data = "Tracks Instant D / Total Intensity", (0,), []
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	w.close()


##################################################
def test_get_plot_data(w: GraphViewerWidget, qtbot, capsys):
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	ref_title: str
	ref_shape: tuple
	ref_data: list[int] | list[list[int]] | list[float] | list[list[float]]

	# Plot pour la pile
	qtbot.mouseClick(w._btn_src["Stack"], Qt.MouseButton.LeftButton)
	assert w._btg_src.checkedId() == 0, "Index de la source incorrecte."

	data, title = w._get_plot_data()
	ref_title, ref_shape = "Stack Intensity", (10, 128, 256)
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"

	# Plot pour la pile filtrée
	w._filters["Plane"].active = True
	w._filters["Plane"].value = [2, 50]

	data, title = w._get_plot_data()
	ref_title, ref_shape = "Stack Intensity", (9, 128, 256)
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"

	# Plot pour les localisations
	qtbot.mouseClick(w._btn_src["Localization"], Qt.MouseButton.LeftButton)
	assert w._btg_src.checkedId() == 1, "Index de la source incorrecte."
	assert w._cmb_src_a.value == 0, "Index de la donnée incorrecte."

	data, title = w._get_plot_data()
	ref_title, ref_shape, ref_data = "Localizations Count", (2, 2), [[1, 4], [2, 2]]
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	w._cmb_src_a.value = 1
	assert w._cmb_src_a.value == 1, "Index de la donnée incorrecte."
	data, title = w._get_plot_data()
	ref_title, ref_shape, ref_data = "Localizations X", (6,), [1, 2, 3, 4, 1, 2]
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# En cas de colonne inexistante.
	w._df["Localization"].drop(columns=[w._cmb_src_a.current_text], inplace=True)
	data, title = w._get_plot_data()
	ref_title, ref_shape, ref_data = "Localizations X", (0,), []
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	w._actualize()  # Restaurer le csv
	qtbot.mouseClick(w._btn_src["Localization"], Qt.MouseButton.LeftButton)  # Retour sur la localisation

	# En cas de Dataframe vide.
	w._df["Localization"] = w._df["Localization"].iloc[0:0]
	data, title = w._get_plot_data()
	ref_title, ref_shape, ref_data = "Localizations Count", (0,), []
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# Plot pour les trajectoires
	w._actualize()  # Restaurer le csv
	qtbot.mouseClick(w._btn_src["Tracks"], Qt.MouseButton.LeftButton)
	assert w._btg_src.checkedId() == 2, "Index de la source incorrecte."

	# Affichage de Longeur
	data, title = w._get_plot_data()
	ref_title, ref_shape, ref_data = "Tracks Length", (9, 2), [[1, 98], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1], [9, 1]]
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# Affichage de MSD
	w._cmb_src_a.value = 1
	assert w._cmb_src_a.value == 1, "Index de la donnée incorrecte."
	data, title = w._get_plot_data()
	ref_title, ref_shape = "Tracks MSD Step 1", (14, 2)
	ref_data = [[35, 0.39], [37, 0.26], [66, 0.37], [75, 0.47], [81, 0.49], [83, 0.24], [102, 0.14],
				[114, 0.43], [131, 0.35], [152, 0.37], [158, 0.42], [165, 0.50], [176, 0.34], [220, 0.46]]
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# Changement de Step.
	w._msd_step.value = 3
	data, title = w._get_plot_data()
	ref_title, ref_shape, ref_data = "Tracks MSD Step 3", (6, 2), [[81, 0.40], [83, 1.60], [114, 1.07], [152, 0.73], [158, 1.12], [165, 0.30]]
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# En cas de colonne inexistante.
	w._msd_step.value = 8
	data, title = w._get_plot_data()
	ref_title, ref_shape, ref_data = "Tracks MSD Step 8", (0,), []
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# Affichage de Instant D
	w._cmb_src_a.value = 2
	assert w._cmb_src_a.value == 2, "Index de la donnée incorrecte."
	data, title = w._get_plot_data()
	ref_title, ref_shape = "Tracks Instant D", (27,)
	ref_data = [4.51, 1.37, 3.04, 1.13, 1e-06, 1.99, 1e-06, 2.34, 0.81, 4.02, 4.26, 1.31, 6.37,
				0.60, 2.22, 4.83, 0.27, 0.96, 5.41, 9.19, 0.60, 1.24, 0.54, 2.43, 2.23, 1.61, 3.05]
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# Une colonne de Fit
	w._cmb_src_a.value = 3
	assert w._cmb_src_a.value == 3, "Index de la donnée incorrecte."
	data, title = w._get_plot_data()
	ref_title, ref_shape = "Tracks Total Intensity", (14, 2)
	ref_data = [[35, 6300.36], [37, 9467.97], [66, 5307.80], [75, 5218.86], [81, 14337.08], [83, 13517.40], [102, 4276.15],
				[114, 9437.99], [131, 4724.48], [152, 11162.22], [158, 9454.11], [165, 9683.89], [176, 5313.26], [220, 6232.91]]
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\nAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# En cas de colonne inexistante.
	w._df["Fit"].drop(columns=[w._cmb_src_a.current_text], inplace=True)
	data, title = w._get_plot_data()
	ref_title, ref_shape, ref_data = "Tracks Total Intensity", (0,), []
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	w.close()


##################################################
def test_tracks_source(w: GraphViewerWidget, qtbot, capsys):
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	# Récupération des sources classiques.
	ref = ["Length", "MSD", "Instant D", "Total Intensity", "D(0) (μm²/s)", "MSD(0) (μm²)", "MSE(0)", "A (μm²/s)", "B (μm²)", "MSE"]
	res = w._get_tracks_src()
	assert ref == res, f"Liste des sources incorrecte.\nAttendu : {ref}\nObtenu : {res}"

	# Avec des Dataframes Vide
	ref = ["Length"]
	for key in w._df: w._df[key] = pd.DataFrame()
	res = w._get_tracks_src()
	assert ref == res, f"Liste des sources incorrecte.\nAttendu : {ref}\nObtenu : {res}"

	w.close()
