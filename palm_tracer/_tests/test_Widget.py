""" Fichier des tests pour le widget """

from pathlib import Path
from typing import cast

import numpy as np

from palm_tracer import PALMTracerWidget
from palm_tracer.Settings.Types import FileList

INPUT_DIR = Path(__file__).parent / "input"


##################################################
def test_widget_creation(make_napari_viewer, capsys):
	"""Test basique de création du widget."""
	viewer = make_napari_viewer()  # Créer un viewer à l'aide de la fixture.
	my_widget = PALMTracerWidget(viewer)  # Créer notre widget, en passant par le viewer.
	assert True


##################################################
def test_widget_reset_layer(make_napari_viewer, capsys):
	"""Test click sur le bouton."""
	viewer = make_napari_viewer()  # Créer un viewer à l'aide de la fixture.
	my_widget = PALMTracerWidget(viewer)  # Créer notre widget, en passant par le viewer.

	# Ajout d'une entrée
	file_list = cast(FileList, my_widget.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	assert True

##################################################
def test_widget_auto_threshold(make_napari_viewer, capsys):
	"""Test click sur le bouton."""
	viewer = make_napari_viewer()  # Créer un viewer à l'aide de la fixture.
	my_widget = PALMTracerWidget(viewer)  # Créer notre widget, en passant par le viewer.

	# Ajout d'une entrée
	file_list = cast(FileList, my_widget.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	my_widget.auto_threshold()  # Appel de la méthode auto_threshold
	assert True

##################################################
def test_widget_process(make_napari_viewer, capsys):
	"""Test click sur le bouton."""
	viewer = make_napari_viewer()  # Créer un viewer à l'aide de la fixture.
	my_widget = PALMTracerWidget(viewer)  # Créer notre widget, en passant par le viewer.

	# Ajout d'une entrée
	file_list = cast(FileList, my_widget.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	my_widget.process()  # Appel de la méthode process
	assert True
