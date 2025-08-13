""" Fichier des tests pour le widget. """
import sys
from pathlib import Path
from typing import cast

import numpy as np
import pytest
from qtpy.QtWidgets import QApplication

from palm_tracer import PALMTracer
from palm_tracer._tests.Utils import is_headless_macos
from palm_tracer.Settings.Types import FileList
from palm_tracer.UI import GraphViewerWidget

INPUT_DIR = Path(__file__).parent / "input"

rng = np.random.default_rng(42)  # Initialisation du générateur avec une seed
SIZE_X, SIZE_Y, INTENSITY, RATIO = 100, 50, 1000, 10
SIZE = int(SIZE_X * np.sqrt(SIZE_Y))
POINTS = np.stack([rng.uniform(1, SIZE_Y - 1, size=SIZE), rng.uniform(1, SIZE_X - 1, size=SIZE)], axis=1)


##################################################
@pytest.mark.skipif(is_headless_macos(), reason="Napari/VisPy causes segfault in headless macOS")
def test_widget_creation(make_napari_viewer, capsys, qtbot):
	"""Test basique de création du widget."""
	pt = PALMTracer()
	w = GraphViewerWidget(pt)
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)
	w.close()
	assert True

@pytest.mark.skipif(is_headless_macos(), reason="Napari/VisPy causes segfault in headless macOS")
def test_change_source(make_napari_viewer, capsys):
	"""Test basique de création du widget."""
	assert True
