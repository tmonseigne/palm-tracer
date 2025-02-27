""" Fichier des tests pour l'utilisation des DLL """

import os
import shutil
from pathlib import Path
from typing import cast

from matplotlib import pyplot as plt

from palm_tracer import PALMTracer
from palm_tracer.Settings.Types import FileList
from palm_tracer.Tools import print_warning

INPUT_DIR = Path(__file__).parent / "input"
OUTPUT_DIR = Path(__file__).parent / "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)


##################################################
def test_process_no_input(make_napari_viewer):
	"""Test pour le process sans fichiers en entrée."""
	pt = PALMTracer()

	if not pt.is_dll_valid():
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		pt.process()
		print_warning("\n====================\nAucune comparaison avec Metamorph dans ce test.\n====================\n")
	assert True


##################################################
def test_process_nothing(make_napari_viewer):
	""" Test pour le process avec tout les élément à False et aucun fichier chargeable. """
	pt = PALMTracer()

	if not pt.is_dll_valid():
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		file_list = cast(FileList, pt.settings.batch["Files"])
		file_list.items = [f"{INPUT_DIR}/stack.tif"]
		file_list.update_box()
		paths = pt.settings.batch.get_paths()
		for path in paths:
			shutil.rmtree(path, ignore_errors=True)  # Supprime récursivement le dossier et tout son contenu pour n'avoir rien à charger.
		pt.process()
		# Test d'une visualisation sans données.
		pt.settings.visualization_hr.active = True
		pt.process()


##################################################
def test_process_multiple_stack(make_napari_viewer):
	""" Test pour le process avec plusieurs piles. """
	pt = PALMTracer()

	if not pt.is_dll_valid():
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		file_list = cast(FileList, pt.settings.batch["Files"])
		file_list.items = [f"{INPUT_DIR}/stack.tif", f"{INPUT_DIR}/stack_quadrant.tif"]
		file_list.update_box()
		pt.settings.batch["Mode"].set_value(1)
		pt.process()


##################################################
def test_process_only_localization(make_napari_viewer):
	"""
	Test pour le process de localisation.

	.. todo::
		Comparer avec une sortie de PALM Tracer.
		Actuellement différence de résultat, nécessite une investigation
	"""
	pt = PALMTracer()

	if not pt.is_dll_valid():
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		file_list = cast(FileList, pt.settings.batch["Files"])
		file_list.items = [f"{INPUT_DIR}/stack.tif"]
		file_list.update_box()
		pt.settings.localization.active = True
		pt.process()
		print_warning("\n====================\nAucune comparaison avec Metamorph dans ce test.\n====================\n")
	assert True


##################################################
def test_process_only_tracking(make_napari_viewer):
	"""
	Test pour le process de tracking.

	.. todo::
		Comparer avec une sortie de PALM Tracer.
		Actuellement différence de résultat, nécessite une investigation
	"""
	pt = PALMTracer()

	if not pt.is_dll_valid():
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		pt.settings.tracking.active = True
		file_list = cast(FileList, pt.settings.batch["Files"])
		file_list.items = [f"{INPUT_DIR}/stack.tif"]
		file_list.update_box()
		pt.process()
		print_warning("\n====================\nAucune comparaison avec Metamorph dans ce test.\n====================\n")
	assert True


##################################################
def test_process_only_visualization():
	"""
	Test pour le process de localisation.

	.. todo::
		Comparer avec une sortie de PALM Tracer.
		Actuellement différence de résultat, nécessite une investigation
	"""
	app = initialize_qt_app_for_testing()
	pt = PALMTracer()

	if not pt.is_dll_valid():
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		pt.settings.visualization_hr.active = True
		file_list = cast(FileList, pt.settings.batch["Files"])
		file_list.items = [f"{INPUT_DIR}/stack.tif"]
		file_list.update_box()
		pt.process()
		print_warning("\n====================\nAucune comparaison avec Metamorph dans ce test.\n====================\n")
	assert True


##################################################
def test_process_all():
	"""
	Test Basique pour le process.

	.. todo::
		Comparer avec une sortie de PALM Tracer.
		Actuellement différence de résultat, nécessite une investigation
	"""
	app = initialize_qt_app_for_testing()
	pt = PALMTracer()

	if not pt.is_dll_valid():
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		pt.settings.localization.active = True
		pt.settings.tracking.active = True
		pt.settings.visualization_hr.active = True
		file_list = cast(FileList, pt.settings.batch["Files"])
		file_list.items = [f"{INPUT_DIR}/stack.tif"]
		file_list.update_box()
		pt.process()
		print_warning("\n====================\nAucune comparaison avec Metamorph dans ce test.\n====================\n")
	assert True
