""" Fichier des tests pour l'utilisation des DLL """

import os
import shutil
import sys
from pathlib import Path
from typing import cast

from qtpy.QtCore import QCoreApplication, Qt
from qtpy.QtWidgets import QApplication

from palm_tracer.Processing import load_dll, PALM
from palm_tracer.Settings import Settings
from palm_tracer.Settings.Types import FileList
from palm_tracer.Tools import print_warning

INPUT_DIR = Path(__file__).parent / "input"
OUTPUT_DIR = Path(__file__).parent / "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)


##################################################
def initialize():
	"""Fixture pour initialiser l'application Qt"""
	# Si nous sommes dans un environnement CI, forcez l'application à ne pas afficher les fenêtres graphiques
	if not sys.stdout.isatty():  # Vérifie si on est dans un terminal (et donc potentiellement CI)
		QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_DisableHighDpiScaling)
		QApplication.setAttribute(Qt.ApplicationAttribute.AA_Use96Dpi)

	app = QApplication([])  # Initialisation de QApplication
	return app


##################################################
def test_process_no_input():
	"""Test pour le process sans fichiers en entrée."""
	dll = load_dll()
	if dll.get("CPU", None) is None or dll.get("Tracking", None) is None:
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		app = initialize()
		settings = Settings()
		PALM.process(dll, settings)
		print_warning("\n====================\nAucune comparaison avec Metamorph dans ce test.\n====================\n")
	assert True

##################################################
def test_process_nothing():
	""" Test pour le process avec tout les élément à False et aucun fichier chargeable. """
	dll = load_dll()
	if dll.get("CPU", None) is None or dll.get("Tracking", None) is None:
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		app = initialize()
		settings = Settings()
		file_list = cast(FileList, settings.batch["Files"])
		file_list.items = [f"{INPUT_DIR}/stack.tif"]
		file_list.update_box()
		paths = settings.batch.get_paths()
		for path in paths:
			shutil.rmtree(path, ignore_errors=True)  # Supprime récursivement le dossier et tout son contenu pour n'avoir rien à charger.
		PALM.process(dll, settings)


##################################################
def test_process_multiple_stack():
	dll = load_dll()
	if dll.get("CPU", None) is None or dll.get("Tracking", None) is None:
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		app = initialize()
		settings = Settings()
		file_list = cast(FileList, settings.batch["Files"])
		file_list.items = [f"{INPUT_DIR}/stack.tif", f"{INPUT_DIR}/stack_quadrant.tif"]
		file_list.update_box()
		settings.batch["Mode"].set_value(1)
		PALM.process(dll, settings)

##################################################
def test_process_only_localization():
	"""
	Test pour le process de localisation.

	.. todo::
		Comparer avec une sortie de PALM Tracer.
		Actuellement différence de résultat, nécessite une investigation
	"""
	dll = load_dll()
	if dll.get("CPU", None) is None or dll.get("Tracking", None) is None:
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		app = initialize()
		settings = Settings()
		file_list = cast(FileList, settings.batch["Files"])
		file_list.items = [f"{INPUT_DIR}/stack.tif"]
		file_list.update_box()
		PALM.process(dll, settings)  # First Time without localization active and no files to load.
		settings.localization.active = True
		PALM.process(dll, settings)
		print_warning("\n====================\nAucune comparaison avec Metamorph dans ce test.\n====================\n")
	assert True


##################################################
def test_process_only_tracking():
	"""
	Test pour le process de localisation.

	.. todo::
		Comparer avec une sortie de PALM Tracer.
		Actuellement différence de résultat, nécessite une investigation
	"""
	dll = load_dll()
	if dll.get("CPU", None) is None or dll.get("Tracking", None) is None:
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		app = initialize()
		settings = Settings()
		settings.tracking.active = True
		file_list = cast(FileList, settings.batch["Files"])
		file_list.items = [f"{INPUT_DIR}/stack.tif"]
		file_list.update_box()
		PALM.process(dll, settings)
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
	dll = load_dll()
	if dll.get("CPU", None) is None or dll.get("Tracking", None) is None:
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		app = initialize()
		settings = Settings()
		settings.visualization.active = True
		file_list = cast(FileList, settings.batch["Files"])
		file_list.items = [f"{INPUT_DIR}/stack.tif"]
		file_list.update_box()
		PALM.process(dll, settings)
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
	dll = load_dll()
	if dll.get("CPU", None) is None or dll.get("Tracking", None) is None:
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		app = initialize()
		settings = Settings()
		settings.localization.active = True
		settings.tracking.active = True
		settings.visualization.active = True
		file_list = cast(FileList, settings.batch["Files"])
		file_list.items = [f"{INPUT_DIR}/stack.tif"]
		file_list.update_box()
		PALM.process(dll, settings)
		print_warning("\n====================\nAucune comparaison avec Metamorph dans ce test.\n====================\n")
	assert True
