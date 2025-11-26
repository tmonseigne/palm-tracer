""" Fichier des tests pour le widget. """
from pathlib import Path
from typing import cast

import numpy as np
import pandas as pd
import pytest
from qtpy.QtCore import Qt

from palm_tracer import PALMTracer
from palm_tracer._tests.Utils import is_headless_macos
from palm_tracer.Settings.Types import FileList
from palm_tracer.UI import GraphViewerWidget
from palm_tracer.UI.GraphViewerWidget import FILE_STATUS

INPUT_DIR = Path(__file__).parent / "input"
OUTPUT_DIR = INPUT_DIR / "stack_PALM_Tracer"
rng = np.random.default_rng(42)  # Initialisation du générateur avec une seed
SIZE_X, SIZE_Y, INTENSITY, RATIO = 100, 50, 1000, 10
SIZE = int(SIZE_X * np.sqrt(SIZE_Y))
POINTS = np.stack([rng.uniform(1, SIZE_Y - 1, size=SIZE), rng.uniform(1, SIZE_X - 1, size=SIZE)], axis=1)


##################################################
def get_pt():
	pt = PALMTracer()
	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR / "stack.tif"}"]
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
@pytest.mark.skipif(is_headless_macos(), reason="Napari/VisPy causes segfault in headless macOS")
def test_widget_creation(w: GraphViewerWidget, qtbot):
	"""Test basique de création du widget."""
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)
	w.close()
	assert True


##################################################
@pytest.mark.skipif(is_headless_macos(), reason="Napari/VisPy causes segfault in headless macOS")
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
	assert True


##################################################
@pytest.mark.skipif(is_headless_macos(), reason="Napari/VisPy causes segfault in headless macOS")
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
	assert True


##################################################
@pytest.mark.skipif(is_headless_macos(), reason="Napari/VisPy causes segfault in headless macOS")
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
	assert True


##################################################
@pytest.mark.skipif(is_headless_macos(), reason="Napari/VisPy causes segfault in headless macOS")
def test_update_plot(w: GraphViewerWidget, qtbot, capsys):
	"""Test basique de création du widget."""
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	# Plot pour La pile
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

	# En cas de colonne inexistante.
	w._df["loc"].drop(columns=[w._cmb_src.currentText()], inplace=True)
	w._update_plot()

	w._actualize()  # Restaurer le csv
	qtbot.mouseClick(w._btn_loc, Qt.MouseButton.LeftButton)  # Retour sur la localisation

	# En cas de Dataframe vide.
	w._df["loc"] = w._df["loc"].iloc[0:0]
	w._update_plot()

	# Plot pour les trajectoires
	w._actualize()  # Restaurer le csv
	qtbot.mouseClick(w._btn_trc, Qt.MouseButton.LeftButton)
	assert w._btg_src.checkedId() == 2, "Index de la source incorrecte."

	w._update_plot()

	w.close()
	assert True


##################################################
@pytest.mark.skipif(is_headless_macos(), reason="Napari/VisPy causes segfault in headless macOS")
def test_status(w: GraphViewerWidget, qtbot, capsys):
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	# Clés vides (il vérifie juste que les dataframe ne sont pas vide dans ce cas il indique que c'est bon)
	ref = {"loc": FILE_STATUS[1], "trc": FILE_STATUS[1], "MSD": FILE_STATUS[1], "InD": FILE_STATUS[1], "Fit": FILE_STATUS[1]}
	res = w._get_status("", "", ["", "", ""])
	for key in res: assert res[key] == ref[key], "Status incorrect."

	# Clés pour dataframes simples
	res = w._get_status("loc", "trc", ["MSD", "InD", "Fit"])
	for key in res: assert res[key] == ref[key], "Status incorrect."

	# Clés pour dataframes filtrés
	ref = {"loc": FILE_STATUS[2], "trc": FILE_STATUS[2], "MSD": FILE_STATUS[2], "InD": FILE_STATUS[2], "Fit": FILE_STATUS[2]}
	res = w._get_status("f_loc", "f_trc", ["f_MSD", "f_InD", "f_Fit"])
	for key in res: assert res[key] == ref[key], "Status incorrect."

	# Clés pour dataframes simples mais trajectoires reconnecté
	ref = {"loc": FILE_STATUS[1], "trc": FILE_STATUS[3], "MSD": FILE_STATUS[1], "InD": FILE_STATUS[1], "Fit": FILE_STATUS[1]}
	res = w._get_status("loc", "blk", ["MSD", "InD", "Fit"])
	for key in res: assert res[key] == ref[key], "Status incorrect."

	# Clés pour dataframes filtrés mais trajectoires reconnecté
	ref = {"loc": FILE_STATUS[2], "trc": FILE_STATUS[4], "MSD": FILE_STATUS[2], "InD": FILE_STATUS[2], "Fit": FILE_STATUS[2]}
	res = w._get_status("f_loc", "f_blk", ["f_MSD", "f_InD", "f_Fit"])
	for key in res: assert res[key] == ref[key], "Status incorrect."

	# Vider les dataframes
	ref = {"loc": FILE_STATUS[0], "trc": FILE_STATUS[0], "MSD": FILE_STATUS[0], "InD": FILE_STATUS[0], "Fit": FILE_STATUS[0]}
	for key in w._df: w._df[key] = pd.DataFrame()
	res = w._get_status("f_loc", "f_blk", ["f_MSD", "f_InD", "f_Fit"])
	for key in res: assert res[key] == ref[key], "Status incorrect."

	w.close()
	assert True
