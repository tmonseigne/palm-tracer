""" Fichier des tests pour le widget. """
from typing import cast

import pytest
from qtpy.QtCore import Qt

from palm_tracer import PALMTracer
from palm_tracer._tests.Utils import *
from palm_tracer.Settings.Types import FileList
from palm_tracer.UI import GraphViewerWidget

OUTPUT_DIR = INPUT_DIR / "stack_PALM_Tracer"
SIZE_X, SIZE_Y, INTENSITY, RATIO = 100, 50, 1000, 10
SIZE = int(SIZE_X * np.sqrt(SIZE_Y))
POINTS = np.stack([rng.uniform(1, SIZE_Y - 1, size=SIZE), rng.uniform(1, SIZE_X - 1, size=SIZE)], axis=1)


##################################################
def get_pt():
	pt = PALMTracer()
	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR / 'stack.tif'}"]
	file_list.update_box()
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
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_widget_creation(w: GraphViewerWidget, qtbot):
	"""Test basique de création du widget."""
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)
	w.close()


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_actualize(w: GraphViewerWidget, qtbot):
	"""Test basique de création du widget."""
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	w._actualize()  # Actualize

	ref = w._filters["Plane"].get_value()
	new_f = [2, 50]
	w._filters["Plane"].set_value(new_f)
	assert w._filters["Plane"].get_value() == new_f, "Filtre incorrect."
	w._actualize()
	assert w._filters["Plane"].get_value() == ref, "Filtre incorrect."

	w.close()


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_reset_filtered(w: GraphViewerWidget, qtbot, capsys):
	"""Test basique de création du widget."""
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	assert w._status["loc"].text() == "Yes (Filtered)", "Status Incorrect."
	w._reset_filtered()
	assert w._status["loc"].text() == "Yes", "Status Incorrect."

	w.close()


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_update_filtered(w: GraphViewerWidget, qtbot, capsys):
	"""Test basique de création du widget."""
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	ref = w._filters["Plane"].get_value()
	new_f = [2, 50]
	w._filters["Plane"].set_value(new_f)
	assert w._filters["Plane"].get_value() == new_f, "Filtre incorrect."
	assert w._pt.settings.filtering["Plane"].get_value() == ref, "Filtre incorrect."
	w._update_filtered()
	assert w._pt.settings.filtering["Plane"].get_value() == new_f, "Filtre incorrect."

	w.close()


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_update_plot(w: GraphViewerWidget, qtbot, capsys):
	"""Test basique de création du widget."""
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	# Plot pour la pile
	qtbot.mouseClick(w._btn_stack, Qt.MouseButton.LeftButton)
	assert w._btg_src.checkedId() == 0, "Index de la source incorrecte."
	w._update_plot()

	# Plot pour les localisations
	qtbot.mouseClick(w._btn_loc, Qt.MouseButton.LeftButton)
	assert w._btg_src.checkedId() == 1, "Index de la source incorrecte."
	assert w._cmb_src.currentIndex() == 0, "Index de la donnée incorrecte."
	w._update_plot()

	w._cmb_src.setCurrentIndex(1)
	assert w._cmb_src.currentIndex() == 1, "Index de la donnée incorrecte."
	w._update_plot()

	# Plot pour les trajectoires
	qtbot.mouseClick(w._btn_trc, Qt.MouseButton.LeftButton)
	assert w._btg_src.checkedId() == 2, "Index de la source incorrecte."
	w._update_plot()

	# Affichage de Instant D
	w._cmb_src.setCurrentIndex(2)
	assert w._cmb_src.currentIndex() == 2, "Index de la donnée incorrecte."
	w._update_plot()

	w.close()


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_get_plot_data(w: GraphViewerWidget, qtbot, capsys):
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	ref_title: str
	ref_shape: tuple
	ref_data: list[int] | list[list[int]]

	# Plot pour la pile
	qtbot.mouseClick(w._btn_stack, Qt.MouseButton.LeftButton)
	assert w._btg_src.checkedId() == 0, "Index de la source incorrecte."

	data, title = w.get_plot_data()
	ref_title, ref_shape = "Stack Intensity", (10, 128, 256)
	assert data.shape == ref_shape, f"Dimensions incorrectes.\nAttendu: {ref_shape}\nObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\nAttendu: {ref_title}\nObtenu : {title}"

	# Plot pour la pile filtrée
	w._filters["Plane"].active = True
	w._filters["Plane"].set_value([2, 50])

	data, title = w.get_plot_data()
	ref_title, ref_shape = "Stack Intensity", (9, 128, 256)
	assert data.shape == ref_shape, f"Dimensions incorrectes.\nAttendu: {ref_shape}\nObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\nAttendu: {ref_title}\nObtenu : {title}"

	# Plot pour les localisations
	qtbot.mouseClick(w._btn_loc, Qt.MouseButton.LeftButton)
	assert w._btg_src.checkedId() == 1, "Index de la source incorrecte."
	assert w._cmb_src.currentIndex() == 0, "Index de la donnée incorrecte."

	data, title = w.get_plot_data()
	ref_title, ref_shape, ref_data = "Localizations Count", (2, 2), [[1, 4], [2, 2]]
	assert data.shape == ref_shape, f"Dimensions incorrectes.\nAttendu: {ref_shape}\nObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\nAttendu: {ref_title}\nObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	w._cmb_src.setCurrentIndex(1)
	assert w._cmb_src.currentIndex() == 1, "Index de la donnée incorrecte."
	data, title = w.get_plot_data()
	ref_title, ref_shape, ref_data = "Localizations Intensity", (6,), [1, 1, 0, 1, 1, 1]
	assert data.shape == ref_shape, f"Dimensions incorrectes.\nAttendu: {ref_shape}\nObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\nAttendu: {ref_title}\nObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# En cas de colonne inexistante.
	w._df["loc"].drop(columns=[w._cmb_src.currentText()], inplace=True)
	data, title = w.get_plot_data()
	ref_title, ref_shape, ref_data = "Localizations Intensity", (0,), []
	assert data.shape == ref_shape, f"Dimensions incorrectes.\nAttendu: {ref_shape}\nObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\nAttendu: {ref_title}\nObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	w._actualize()  # Restaurer le csv
	qtbot.mouseClick(w._btn_loc, Qt.MouseButton.LeftButton)  # Retour sur la localisation

	# En cas de Dataframe vide.
	w._df["loc"] = w._df["loc"].iloc[0:0]
	data, title = w.get_plot_data()
	ref_title, ref_shape, ref_data = "Localizations Count", (0,), []
	assert data.shape == ref_shape, f"Dimensions incorrectes.\nAttendu: {ref_shape}\nObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\nAttendu: {ref_title}\nObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# Plot pour les trajectoires
	w._actualize()  # Restaurer le csv
	qtbot.mouseClick(w._btn_trc, Qt.MouseButton.LeftButton)
	assert w._btg_src.checkedId() == 2, "Index de la source incorrecte."

	# Affichage de Longeur
	data, title = w.get_plot_data()
	ref_title, ref_shape, ref_data = "Tracks Length", (9, 2), [[1, 98], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1], [9, 1]]
	assert data.shape == ref_shape, f"Dimensions incorrectes.\nAttendu: {ref_shape}\nObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\nAttendu: {ref_title}\nObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# Affichage de MSD
	w._cmb_src.setCurrentIndex(1)
	assert w._cmb_src.currentIndex() == 1, "Index de la donnée incorrecte."
	data, title = w.get_plot_data()
	ref_title, ref_shape = "Tracks MSD Step 1", (14, 2)
	assert data.shape == ref_shape, f"Dimensions incorrectes.\nAttendu: {ref_shape}\nObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\nAttendu: {ref_title}\nObtenu : {title}"

	# Changement de Step.
	w._display_settings["MSD"].set_value(3)
	data, title = w.get_plot_data()
	ref_title, ref_shape, ref_data = "Tracks MSD Step 3", (6, 2), []
	assert data.shape == ref_shape, f"Dimensions incorrectes.\nAttendu: {ref_shape}\nObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\nAttendu: {ref_title}\nObtenu : {title}"
	# np.testing.assert_array_equal(data, ref_data)

	# En cas de colonne inexistante.
	w._display_settings["MSD"].set_value(8)
	data, title = w.get_plot_data()
	ref_title, ref_shape, ref_data = "Tracks MSD Step 8", (0,), []
	assert data.shape == ref_shape, f"Dimensions incorrectes.\nAttendu: {ref_shape}\nObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\nAttendu: {ref_title}\nObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# Affichage de Instant D
	w._cmb_src.setCurrentIndex(2)
	assert w._cmb_src.currentIndex() == 2, "Index de la donnée incorrecte."
	data, title = w.get_plot_data()
	ref_title, ref_shape, ref_data = "Tracks Instant Diffusion", (27,), []
	assert data.shape == ref_shape, f"Dimensions incorrectes.\nAttendu: {ref_shape}\nObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\nAttendu: {ref_title}\nObtenu : {title}"
	# np.testing.assert_array_equal(data, ref_data)

	# Une colonne de Fit
	w._cmb_src.setCurrentIndex(3)
	assert w._cmb_src.currentIndex() == 3, "Index de la donnée incorrecte."
	data, title = w.get_plot_data()
	ref_title, ref_shape, ref_data = "Tracks Total Intensity", (14, 2), []
	assert data.shape == ref_shape, f"Dimensions incorrectes.\nAttendu: {ref_shape}\nObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\nAttendu: {ref_title}\nObtenu : {title}"
	# np.testing.assert_array_equal(data, ref_data)

	# En cas de colonne inexistante.
	w._df["Fit"].drop(columns=[w._cmb_src.currentText()], inplace=True)
	data, title = w.get_plot_data()
	ref_title, ref_shape, ref_data = "Tracks Total Intensity", (0,), []
	assert data.shape == ref_shape, f"Dimensions incorrectes.\nAttendu: {ref_shape}\nObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\nAttendu: {ref_title}\nObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	w.close()


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_status(w: GraphViewerWidget, qtbot, capsys):
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	# Clés vides (il vérifie juste que les dataframe ne sont pas vide dans ce cas il indique que c'est bon)
	ref = {"loc": w.FILE_STATUS[1], "trc": w.FILE_STATUS[1], "MSD": w.FILE_STATUS[1], "InD": w.FILE_STATUS[1], "Fit": w.FILE_STATUS[1]}
	res = w._get_status("", "", ["", "", ""])
	for key in res: assert res[key] == ref[key], f"Status incorrect.\nAttendu: {ref}\nObtenu : {res}"

	# Clés pour dataframes simples
	res = w._get_status("loc", "trc", ["MSD", "InD", "Fit"])
	for key in res: assert res[key] == ref[key], f"Status incorrect.\nAttendu: {ref}\nObtenu : {res}"

	# Clés pour dataframes filtrés
	ref = {"loc": w.FILE_STATUS[2], "trc": w.FILE_STATUS[2], "MSD": w.FILE_STATUS[2], "InD": w.FILE_STATUS[2], "Fit": w.FILE_STATUS[2]}
	res = w._get_status("f_loc", "f_trc", ["f_MSD", "f_InD", "f_Fit"])
	for key in res: assert res[key] == ref[key], f"Status incorrect.\nAttendu: {ref}\nObtenu : {res}"

	# Clés pour dataframes simples mais trajectoires reconnecté
	ref = {"loc": w.FILE_STATUS[1], "trc": w.FILE_STATUS[3], "MSD": w.FILE_STATUS[1], "InD": w.FILE_STATUS[1], "Fit": w.FILE_STATUS[1]}
	res = w._get_status("loc", "blk", ["MSD", "InD", "Fit"])
	for key in res: assert res[key] == ref[key], f"Status incorrect.\nAttendu: {ref}\nObtenu : {res}"

	# Clés pour dataframes filtrés mais trajectoires reconnecté
	ref = {"loc": w.FILE_STATUS[2], "trc": w.FILE_STATUS[4], "MSD": w.FILE_STATUS[2], "InD": w.FILE_STATUS[2], "Fit": w.FILE_STATUS[2]}
	res = w._get_status("f_loc", "f_blk", ["f_MSD", "f_InD", "f_Fit"])
	for key in res: assert res[key] == ref[key], f"Status incorrect.\nAttendu: {ref}\nObtenu : {res}"

	# Vider les dataframes
	ref = {"loc": w.FILE_STATUS[0], "trc": w.FILE_STATUS[0], "MSD": w.FILE_STATUS[0], "InD": w.FILE_STATUS[0], "Fit": w.FILE_STATUS[0]}
	for key in w._df: w._df[key] = pd.DataFrame()
	res = w._get_status("f_loc", "f_blk", ["f_MSD", "f_InD", "f_Fit"])
	for key in res: assert res[key] == ref[key], f"Status incorrect.\nAttendu: {ref}\nObtenu : {res}"

	w.close()


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_tracks_source(w: GraphViewerWidget, qtbot, capsys):
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	# Récupération des sources classique
	ref = ["Length", "MSD", "Instant Diffusion", "Total Intensity", "D(0) (μm²/s)", "MSD(0) (μm²)", "MSE(0)", "A (μm²/s)", "B (μm²)", "MSE"]
	res = w._get_tracks_src()
	assert ref == res, f"Liste des sources incorrecte.\nAttendu: {ref}\nObtenu : {res}"

	# Avec des Dataframes Vide
	ref = ["Length"]
	for key in w._df: w._df[key] = pd.DataFrame()
	res = w._get_tracks_src()
	assert ref == res, f"Liste des sources incorrecte.\nAttendu: {ref}\nObtenu : {res}"

	w.close()
