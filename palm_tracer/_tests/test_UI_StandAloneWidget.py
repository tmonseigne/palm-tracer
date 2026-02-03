"""Fichier des tests pour le widget."""

import pytest

from palm_tracer._tests.Utils import *
from palm_tracer.UI.BaseStandAloneWidget import BaseStandAloneWidget  # classe


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_widget_creation(qtbot):
	"""Test basique de création du widget."""
	w = BaseStandAloneWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)
	# Fonction qui devra toujours être redefini chez les classes filles, donc petit test rapide ici.
	assert "image" in str(w._download_initial_path())
	w.close()
