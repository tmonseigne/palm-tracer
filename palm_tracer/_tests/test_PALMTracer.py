""" Fichier des tests pour la classe PALMTracer """

import os
import shutil
from pathlib import Path
from typing import cast

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
		pt.settings.gallery.active = True
		pt.settings.visualization_hr.active = True
		pt.settings.visualization_graph.active = True
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
	""" Test pour le process de localisation. """
	pt = PALMTracer()

	if not pt.is_dll_valid():
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		file_list = cast(FileList, pt.settings.batch["Files"])
		file_list.items = [f"{INPUT_DIR}/stack.tif"]
		file_list.update_box()
		pt.settings.localization.active = True
		pt.process()
	assert True


##################################################
def test_process_only_tracking(make_napari_viewer):
	""" Test pour le process de tracking. """
	pt = PALMTracer()

	if not pt.is_dll_valid():
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		pt.settings.tracking.active = True
		file_list = cast(FileList, pt.settings.batch["Files"])
		file_list.items = [f"{INPUT_DIR}/stack.tif"]
		file_list.update_box()
		pt.process()
	assert True


##################################################
def test_process_only_visualization_hr(make_napari_viewer):
	""" Test pour le process de visualization HR. """
	pt = PALMTracer()

	if not pt.is_dll_valid():
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		pt.settings.visualization_hr.active = True
		file_list = cast(FileList, pt.settings.batch["Files"])
		file_list.items = [f"{INPUT_DIR}/stack.tif"]
		file_list.update_box()
		pt.process()
	assert True


##################################################
def test_process_only_visualization_graph(make_napari_viewer):
	""" Test pour le process de visualization HR. """
	pt = PALMTracer()

	if not pt.is_dll_valid():
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		pt.settings.visualization_graph.active = True
		file_list = cast(FileList, pt.settings.batch["Files"])
		file_list.items = [f"{INPUT_DIR}/stack.tif"]
		file_list.update_box()
		pt.process()
	assert True


##################################################
def test_process_only_gallery(make_napari_viewer):
	""" Test pour le process de visualization HR. """
	pt = PALMTracer()

	if not pt.is_dll_valid():
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		pt.settings.gallery.active = True
		file_list = cast(FileList, pt.settings.batch["Files"])
		file_list.items = [f"{INPUT_DIR}/stack.tif"]
		file_list.update_box()
		pt.process()
	assert True


##################################################
def test_process_all(make_napari_viewer):
	""" Test Basique pour le process complet. """
	pt = PALMTracer()

	if not pt.is_dll_valid():
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		pt.settings.localization.active = True
		pt.settings.localization["Gaussian Fit"]["Mode"].set_value(4)
		pt.settings.tracking.active = True
		pt.settings.gallery.active = True
		pt.settings.visualization_hr.active = True
		pt.settings.visualization_graph.active = True
		file_list = cast(FileList, pt.settings.batch["Files"])
		file_list.items = [f"{INPUT_DIR}/stack.tif"]
		file_list.update_box()
		pt.process()
	assert True


##################################################
def test_process_filter_plan(make_napari_viewer):
	""" Test pour le filtrage des plans lors de l'exécution. """
	pt = PALMTracer()

	if not pt.is_dll_valid():
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		pt.settings.localization.active = True
		file_list = cast(FileList, pt.settings.batch["Files"])
		file_list.items = [f"{INPUT_DIR}/stack.tif"]
		file_list.update_box()
		pt.settings.filtering["Plane"].active = True
		pt.settings.filtering["Plane"].set_value([2, 3])
		pt.process()
		assert pt.localizations["Plane"].isin([2, 3]).all(), "Le DataFrame contient des valeurs hors [2, 3] dans la colonne Plane."
	assert True


##################################################
def test_process_filter_all(make_napari_viewer):
	""" Test pour le filtrage complet lors de l'exécution. """
	pt = PALMTracer()

	if not pt.is_dll_valid():
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		pt.settings.localization.active = True
		# Ajout du fichier
		file_list = cast(FileList, pt.settings.batch["Files"])
		file_list.items = [f"{INPUT_DIR}/stack.tif"]
		file_list.update_box()
		# Passage en Guassian Fit ou les Sigma et Theta sont calculés
		pt.settings.localization["Gaussian Fit"]["Mode"].set_value(4)

		pt.settings.filtering["Plane"].active = True
		pt.settings.filtering["Plane"].set_value([1, 9])  # Suppression du dernier plan uniquement
		pt.settings.filtering["Intensity"].active = True
		pt.settings.filtering["Intensity"].set_value([100, 20000])
		pt.settings.filtering["Gaussian Fit"]["MSE Gaussian"].active = True
		pt.settings.filtering["Gaussian Fit"]["MSE Gaussian"].set_value([0.01, 10])
		pt.settings.filtering["Gaussian Fit"]["Sigma X"].active = True
		pt.settings.filtering["Gaussian Fit"]["Sigma X"].set_value([0, 10])
		pt.settings.filtering["Gaussian Fit"]["Sigma Y"].active = True
		pt.settings.filtering["Gaussian Fit"]["Sigma Y"].set_value([0, 10])
		pt.settings.filtering["Gaussian Fit"]["Theta"].active = True
		pt.settings.filtering["Gaussian Fit"]["Theta"].set_value([-5, 10])
		pt.settings.filtering["Gaussian Fit"]["Circularity"].active = True
		pt.settings.filtering["Gaussian Fit"]["Z"].active = True
		pt.process()
		ref = [["Plane", 1, 9], ["Integrated Intensity", 100, 20000], ["MSE Gaussian", 0.01, 10],
			   ["Sigma X", 0, 10], ["Sigma Y", 0, 10], ["Theta", -5, 10],
			   ["Circularity", 0, 1], ["Z", -1, 1]]
		for r in ref:
			assert pt.localizations[r[0]].between(r[1], r[2]).all(), f"Le DataFrame contient des valeurs hors [{r[1]}:{r[2]}] dans la colonne {r[0]}."
