""" Fichier des tests pour l'utilisation des DLL """

from pathlib import Path

from palm_tracer.Processing import get_gaussian_mode, load_dll, run_dll
from palm_tracer.Tools import open_tif, print_warning

INPUT_DIR = Path(__file__).parent / "input"


##################################################
def test_load_dll():
	"""Test basique sur le chargement des DLL."""
	dlls = load_dll()
	assert True


##################################################
def test_get_gaussian_mode():
	"""Test basique sur la récupération du mode de gaussienne fit."""
	get_gaussian_mode(False, False, False)
	get_gaussian_mode(True, False, False)
	get_gaussian_mode(True, True, False)
	get_gaussian_mode(True, False, True)
	get_gaussian_mode(True, True, True)
	assert True


##################################################
def test_run_dll():
	"""Test basique sur le lancement d'une DLL."""
	dll = load_dll().get("CPU", None)
	if dll is None:
		print_warning("Test non effectué car DLL manquante")
	else:
		image = open_tif(f"{INPUT_DIR}/stack.tif")
		points = run_dll(dll, image[0], 100, False, False, 1.0, 1.0, 7)
	assert True
