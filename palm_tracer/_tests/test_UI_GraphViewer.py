""" Fichier des tests pour le widget. """
import os
import shutil
from pathlib import Path
from typing import cast

import numpy as np
import pytest
from qtpy import QtCore

from palm_tracer import PALMTracer
from palm_tracer._tests.Utils import is_headless_macos, is_not_dll_friendly
from palm_tracer.Settings.Types import FileList
from palm_tracer.UI import GraphViewerWidget

INPUT_DIR = Path(__file__).parent / "input"
INPUT_FILE = INPUT_DIR / "stack.tif"
OUTPUT_DIR = INPUT_DIR / "stack_PALM_Tracer"
rng = np.random.default_rng(42)  # Initialisation du générateur avec une seed
SIZE_X, SIZE_Y, INTENSITY, RATIO = 100, 50, 1000, 10
SIZE = int(SIZE_X * np.sqrt(SIZE_Y))
POINTS = np.stack([rng.uniform(1, SIZE_Y - 1, size=SIZE), rng.uniform(1, SIZE_X - 1, size=SIZE)], axis=1)


##################################################
def get_pt():
	pt = PALMTracer()
	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_FILE}"]
	file_list.update_box()
	return pt


##################################################
@pytest.mark.skipif(is_headless_macos(), reason="Napari/VisPy causes segfault in headless macOS")
def test_widget_creation(qtbot):
	"""Test basique de création du widget."""
	pt = PALMTracer()
	w = GraphViewerWidget(pt)
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)
	w.close()
	assert True


##################################################
@pytest.mark.skipif(is_headless_macos(), reason="Napari/VisPy causes segfault in headless macOS")
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_actualize(qtbot):
	"""Test basique de création du widget."""
	if os.path.exists(OUTPUT_DIR): shutil.rmtree(OUTPUT_DIR, ignore_errors=False)  # On supprime le dossier de sortie
	# Make a process good before
	pt = get_pt()
	w = GraphViewerWidget(pt)
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	# Make a good process
	pt.settings.localization.active = True
	pt.settings.localization["Fit"].set_value(1)
	pt.settings.localization["Gaussian Fit"]["Mode"].set_value(3)
	pt.settings.tracking.active = True
	pt.process()

	w._actualize()  # Actualize
	w.close()
	assert True


##################################################
@pytest.mark.skipif(is_headless_macos(), reason="Napari/VisPy causes segfault in headless macOS")
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_on_source_change(qtbot):
	"""Test basique de création du widget."""
	pt = get_pt()
	w = GraphViewerWidget(pt)
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	qtbot.mouseClick(w._btn_loc, QtCore.Qt.LeftButton)
	qtbot.waitUntil(lambda: w._btg_src.checkedId() == 1, timeout=2000)
	qtbot.mouseClick(w._btn_trc, QtCore.Qt.LeftButton)
	qtbot.waitUntil(lambda: w._btg_src.checkedId() == 2, timeout=2000)
	w.close()
	assert True


##################################################
@pytest.mark.skipif(is_headless_macos(), reason="Napari/VisPy causes segfault in headless macOS")
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_on_type_change(qtbot):
	"""Test basique de création du widget."""
	pt = get_pt()
	w = GraphViewerWidget(pt)
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	w._loc.drop(index=w._loc.index, inplace=True)  # vider le csv
	w._update_plot()
	w._actualize()  # reload csv
	qtbot.mouseClick(w._btn_loc, QtCore.Qt.LeftButton)
	qtbot.waitUntil(lambda: w._btg_src.checkedId() == 1, timeout=2000)

	w._loc.drop(index=w._loc.index, inplace=True)  # vider le csv
	w._update_plot()
	w._actualize()  # reload csv
	w._update_plot()

	qtbot.mouseClick(w._btn_loc, QtCore.Qt.LeftButton)
	qtbot.waitUntil(lambda: w._btg_src.checkedId() == 1, timeout=2000)
	w._cmb_src.setCurrentIndex(1)
	qtbot.waitUntil(lambda: w._cmb_src.currentIndex() == 1, timeout=2000)
	w._export_png_via_qt(f"{OUTPUT_DIR}/test.png", 2)  # sans interface, il exporte un carré blanc

	w._loc.drop(columns=["Integrated Intensity"], inplace=True, errors="ignore")
	w._update_plot()  # column name doesn't match

	w.close()
	assert True
