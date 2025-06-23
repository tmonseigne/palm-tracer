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
	if os.path.exists(SETTINGS_FILE): os.remove(SETTINGS_FILE)  # On supprime le fichier setting
	viewer = make_napari_viewer()								# Créer un viewer à l'aide de la fixture.
	my_widget = PALMTracerWidget(viewer)						# Créer notre widget, en passant par le viewer.
	viewer.close()
	assert True


##################################################
@pytest.mark.skipif(is_headless_macos(), reason="Napari/VisPy causes segfault in headless macOS")
def test_widget_reset_layer(make_napari_viewer, capsys, qtbot):
	"""Test remise à zéro des calques."""
	if os.path.exists(SETTINGS_FILE): os.remove(SETTINGS_FILE)  # On supprime le fichier setting
	viewer = make_napari_viewer()								# Créer un viewer à l'aide de la fixture.
	my_widget = PALMTracerWidget(viewer)						# Créer notre widget, en passant par le viewer.

	my_widget._reset_layer()									# remise à 0 des calques sans fichier dans le batch.
	# Ajout d'une entrée
	file_list = cast(FileList, my_widget.pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	qtbot.waitUntil(lambda: "Raw" in my_widget.viewer.layers, timeout=5000)  # Attente : qu'il ait mis une image
	my_widget._reset_layer()												 # remise à 0 des calques sans changement.
	viewer.close()
	assert True


##################################################
@pytest.mark.skipif(is_headless_macos(), reason="Napari/VisPy causes segfault in headless macOS")
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_widget_get_actual_image(make_napari_viewer, capsys, qtbot):
	""" Test de récupération d'image. """
	if os.path.exists(SETTINGS_FILE): os.remove(SETTINGS_FILE)  # On supprime le fichier setting
	viewer = make_napari_viewer()								# Créer un viewer à l'aide de la fixture.
	my_widget = PALMTracerWidget(viewer)						# Créer notre widget, en passant par le viewer.

	file_list = cast(FileList, my_widget.pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	qtbot.waitUntil(lambda: "Raw" in my_widget.viewer.layers, timeout=5000)					   # Attente : qu'il ai mis une image
	assert my_widget._get_actual_image() is not None, "Aucune image récupéré."				   # Récupéraiton de l'image
	assert my_widget._get_actual_image(-100) is None, "Une image hors limite a été récupéré."  # Récupération d'une image hors limite
	assert my_widget._get_actual_image(100) is None, "Une image hors limite a été récupéré."   # Récupération d'une image hors limite
	viewer.close()


##################################################
@pytest.mark.skipif(is_headless_macos(), reason="Napari/VisPy causes segfault in headless macOS")
def test_widget_add_detection_layers(make_napari_viewer, capsys, qtbot):
	"""Test Ajout des calques de détection."""
	if os.path.exists(SETTINGS_FILE): os.remove(SETTINGS_FILE)  # On supprime le fichier setting
	viewer = make_napari_viewer()								# Créer un viewer à l'aide de la fixture.
	my_widget = PALMTracerWidget(viewer)						# Créer notre widget, en passant par le viewer.
	my_widget.pt.settings.localization["Preview"].set_value(True)
	qtbot.waitUntil(lambda: my_widget.pt.settings.localization["Preview"].get_value(), timeout=5000)
	qtbot.waitUntil(lambda: not my_widget._processing, timeout=5000)
	my_widget.pt.settings.localization["ROI Shape"].set_value(0)
	qtbot.waitUntil(lambda: my_widget.pt.settings.localization["ROI Shape"].get_value() == 0, timeout=5000)
	qtbot.waitUntil(lambda: not my_widget._processing, timeout=5000)

	# Ajout avec des tableaux normaux.
	my_widget._preview_locs = {"Past": POINTS, "Present": POINTS, "Future": POINTS}
	my_widget._add_detection_layers()
	qtbot.waitUntil(lambda: f"Points Present" in my_widget.viewer.layers, timeout=5000)

	# Ajout avec des calques existants et un future vide.
	my_widget._preview_locs = {"Past": POINTS, "Present": POINTS, "Future": None}
	my_widget._add_detection_layers()
	qtbot.waitUntil(lambda: not f"Points Future" in my_widget.viewer.layers, timeout=5000)

	# Ajout avec un tableau vide et rien en passé et future.
	my_widget._preview_locs = {"Past": np.zeros((2, 0)), "Present": POINTS, "Future": None}
	my_widget._add_detection_layers()
	qtbot.waitUntil(lambda: not f"Points Past" in my_widget.viewer.layers, timeout=5000)

	my_widget.pt.settings.localization["ROI Shape"].set_value(1)
	qtbot.waitUntil(lambda: my_widget.pt.settings.localization["ROI Shape"].get_value() == 1, timeout=5000)
	qtbot.waitUntil(lambda: not my_widget._processing, timeout=5000)
	my_widget._preview_locs = {"Past": POINTS, "Present": POINTS, "Future": POINTS}
	my_widget._add_detection_layers()
	qtbot.waitUntil(lambda: f"Points Future" in my_widget.viewer.layers, timeout=5000)

	viewer.close()
	assert True


##################################################
@pytest.mark.skipif(is_headless_macos(), reason="Napari/VisPy causes segfault in headless macOS")
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_widget_preview(make_napari_viewer, capsys, qtbot):
	"""Test click sur le bouton preview."""
	if os.path.exists(SETTINGS_FILE): os.remove(SETTINGS_FILE)  # On supprime le fichier setting
	viewer = make_napari_viewer()								# Créer un viewer à l'aide de la fixture.
	my_widget = PALMTracerWidget(viewer)						# Créer notre widget, en passant par le viewer.

	my_widget._preview()  # Appel de la méthode preview alors que c'est décoché (typiquement le cas par défaut à chaque changement de valeur)
	my_widget.pt.settings.localization["Preview"].set_value(True)
	qtbot.waitUntil(lambda: my_widget.pt.settings.localization["Preview"].get_value(), timeout=5000)
	qtbot.waitUntil(lambda: not my_widget._processing, timeout=5000)
	my_widget._preview()  # Appel de la méthode preview alors que c'est coché mais sans fichier

	# Ajout d'une entrée
	file_list = cast(FileList, my_widget.pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	qtbot.waitUntil(lambda: "Raw" in my_widget.viewer.layers, timeout=5000)  # Attente : qu'il ai mis une image
	qtbot.waitUntil(lambda: not my_widget._processing, timeout=5000)		 # Attente : le flag doit passer à False
	my_widget._preview()													 # Appel de la méthode preview.
	viewer.close()
	assert True


##################################################
@pytest.mark.skipif(is_headless_macos(), reason="Napari/VisPy causes segfault in headless macOS")
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_widget_auto_threshold(make_napari_viewer, capsys, qtbot):
	"""Test click sur le bouton auto_threshold."""
	if os.path.exists(SETTINGS_FILE): os.remove(SETTINGS_FILE)  # On supprime le fichier setting
	viewer = make_napari_viewer()								# Créer un viewer à l'aide de la fixture.
	my_widget = PALMTracerWidget(viewer)						# Créer notre widget, en passant par le viewer.

	my_widget._auto_threshold()									# Appel de la méthode auto_threshold sans fichier dans le batch.

	# Ajout d'une entrée
	file_list = cast(FileList, my_widget.pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	qtbot.waitUntil(lambda: "Raw" in my_widget.viewer.layers, timeout=5000)  # Attente : qu'il ai mis une image
	my_widget._auto_threshold()												 # Appel de la méthode auto_threshold.
	viewer.close()
	assert True


##################################################
@pytest.mark.skipif(is_headless_macos(), reason="Napari/VisPy causes segfault in headless macOS")
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_widget_thread_process(make_napari_viewer, capsys, qtbot):
	"""Test click sur le bouton process."""
	if os.path.exists(SETTINGS_FILE): os.remove(SETTINGS_FILE)  # On supprime le fichier setting
	viewer = make_napari_viewer()								# Créer un viewer à l'aide de la fixture.
	my_widget = PALMTracerWidget(viewer)						# Créer notre widget, en passant par le viewer.

	my_widget._thread_process(my_widget._auto_threshold)
	qtbot.waitUntil(lambda: not my_widget._processing, timeout=5000)  # Attente : que le thread soit terminé

	# appel avec un process en cours
	my_widget._processing = True
	my_widget._thread_process(my_widget._auto_threshold)
	my_widget._processing = False

	# Ajout d'une entrée
	file_list = cast(FileList, my_widget.pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	my_widget._thread_process(my_widget.pt.process)					  # Appel de la méthode process
	qtbot.waitUntil(lambda: not my_widget._processing, timeout=5000)  # Attente : que le thread soit terminé
	my_widget._thread_process(my_widget._auto_threshold)			  # Appel de la méthode auto threshold mais impossible de l'executer dans ce contexte.
	qtbot.waitUntil(lambda: not my_widget._processing, timeout=5000)  # Attente : que le thread soit terminé
	viewer.close()
	assert True
