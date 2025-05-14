""" Fichier des tests pour le widget. """
import os
from pathlib import Path
from typing import cast

import numpy as np
import pytest

from palm_tracer import PALMTracerWidget
from palm_tracer._tests.Utils import is_headless_macos, is_not_dll_friendly
from palm_tracer.Settings.Types import FileList
from palm_tracer.UI.PALMTracerWidget import SETTINGS_FILE

INPUT_DIR = Path(__file__).parent / "input"

rng = np.random.default_rng(42)  # Initialisation du générateur avec une seed
SIZE_X, SIZE_Y, INTENSITY, RATIO = 100, 50, 1000, 10
SIZE = int(SIZE_X * np.sqrt(SIZE_Y))
POINTS = np.stack([rng.uniform(1, SIZE_Y - 1, size=SIZE), rng.uniform(1, SIZE_X - 1, size=SIZE)], axis=1)

##################################################
@pytest.mark.skipif(is_headless_macos(), reason="Napari/VisPy causes segfault in headless macOS")
def test_widget_creation(make_napari_viewer, capsys):
	"""Test basique de création du widget."""
	viewer = make_napari_viewer()		  # Créer un viewer à l'aide de la fixture.
	my_widget = PALMTracerWidget(viewer)  # Créer notre widget, en passant par le viewer.
	viewer.close()
	assert True


##################################################
@pytest.mark.skipif(is_headless_macos(), reason="Napari/VisPy causes segfault in headless macOS")
def test_widget_reset_layer(make_napari_viewer, capsys):
	"""Test remise à zéro des calques."""
	viewer = make_napari_viewer()		  # Créer un viewer à l'aide de la fixture.
	my_widget = PALMTracerWidget(viewer)  # Créer notre widget, en passant par le viewer.

	my_widget._reset_layer()			  # remise à 0 des calques sans fichier dans le batch.
	# Ajout d'une entrée
	file_list = cast(FileList, my_widget.pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	my_widget._reset_layer()			  # remise à 0 des calques sans changement.
	viewer.close()
	assert True


##################################################
@pytest.mark.skipif(is_headless_macos(), reason="Napari/VisPy causes segfault in headless macOS")
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_widget_get_actual_image(make_napari_viewer, capsys):
	""" Test de récupération d'image. """
	viewer = make_napari_viewer()		  # Créer un viewer à l'aide de la fixture.
	my_widget = PALMTracerWidget(viewer)  # Créer notre widget, en passant par le viewer.

	file_list = cast(FileList, my_widget.pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	assert my_widget._get_actual_image() is not None, "Aucune image récupéré."				   # Récupéraiton de l'image
	assert my_widget._get_actual_image(-100) is None, "Une image hors limite a été récupéré."  # Récupéraiton d'une image hors limite
	assert my_widget._get_actual_image(100) is None, "Une image hors limite a été récupéré."   # Récupéraiton d'une image hors limite
	viewer.close()

##################################################
@pytest.mark.skipif(is_headless_macos(), reason="Napari/VisPy causes segfault in headless macOS")
def test_widget_add_detection_layers(make_napari_viewer, capsys):
	"""Test Ajout des calques de détection."""
	if os.path.exists(SETTINGS_FILE): os.remove(SETTINGS_FILE)  #Dans ce cas, il faut supprimer le fichier setting
	viewer = make_napari_viewer()		  # Créer un viewer à l'aide de la fixture.
	my_widget = PALMTracerWidget(viewer)  # Créer notre widget, en passant par le viewer.

	# Ajout avec un tableau vide et rien en passé et future.
	my_widget._preview_locs = {"Past": None, "Present": np.zeros((2, 0)), "Future": None}
	my_widget._add_detection_layers()

	# Ajout avec des tableaux normaux.
	my_widget._preview_locs =  {"Past": POINTS, "Present": POINTS, "Future": POINTS}
	my_widget._add_detection_layers()

	# Ajout avec des calques existants et un future vide.
	my_widget._preview_locs = {"Past": POINTS, "Present": POINTS, "Future": None}
	my_widget._add_detection_layers()
	my_widget.pt.settings.localization["ROI Shape"].set_value(1)
	my_widget._add_detection_layers()

	viewer.close()
	assert True


##################################################
@pytest.mark.skipif(is_headless_macos(), reason="Napari/VisPy causes segfault in headless macOS")
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_widget_preview(make_napari_viewer, capsys):
	"""Test click sur le bouton preview."""
	viewer = make_napari_viewer()		  # Créer un viewer à l'aide de la fixture.
	my_widget = PALMTracerWidget(viewer)  # Créer notre widget, en passant par le viewer.

	my_widget._preview()				  # Appel de la méthode preview sans fichier dans le batch.

	# Ajout d'une entrée
	file_list = cast(FileList, my_widget.pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	my_widget._preview()				  # Appel de la méthode preview.
	viewer.close()
	assert True


##################################################
@pytest.mark.skipif(is_headless_macos(), reason="Napari/VisPy causes segfault in headless macOS")
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_widget_auto_threshold(make_napari_viewer, capsys):
	"""Test click sur le bouton auto_threshold."""
	viewer = make_napari_viewer()		  # Créer un viewer à l'aide de la fixture.
	my_widget = PALMTracerWidget(viewer)  # Créer notre widget, en passant par le viewer.

	my_widget._auto_threshold()			  # Appel de la méthode auto_threshold sans fichier dans le batch.

	# Ajout d'une entrée
	file_list = cast(FileList, my_widget.pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	my_widget._auto_threshold()			  # Appel de la méthode auto_threshold.
	viewer.close()
	assert True


##################################################
@pytest.mark.skipif(is_headless_macos(), reason="Napari/VisPy causes segfault in headless macOS")
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_widget_thread_process(make_napari_viewer, capsys):
	"""Test click sur le bouton process."""
	viewer = make_napari_viewer()		  # Créer un viewer à l'aide de la fixture.
	my_widget = PALMTracerWidget(viewer)  # Créer notre widget, en passant par le viewer.

	my_widget._thread_process(my_widget._auto_threshold)

	# appel avec un process en cours
	my_widget._processing = True
	my_widget._thread_process(my_widget._auto_threshold)
	my_widget._processing = False

	# Ajout d'une entrée
	file_list = cast(FileList, my_widget.pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	my_widget._thread_process(my_widget.pt.process)		 # Appel de la méthode process
	my_widget._thread_process(my_widget._auto_threshold) # Appel de la méthode auto threshold mais impossible de l'executer dnas ce contexte (donc erreur prévu)
	viewer.close()
	assert True
