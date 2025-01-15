""" Fichier des tests pour l'utilisation des DLL """

from pathlib import Path

from palm_tracer.Processing import auto_threshold_dll, auto_threshold, get_gaussian_mode, load_dll, run_palm_image_dll
from palm_tracer.Tools import open_tif, print_warning

INPUT_DIR = Path(__file__).parent / "input"


##################################################
def test_auto_threshold():
	"""Test basique sur l'auto-seuillage avec la DLL."""
	image = open_tif(f"{INPUT_DIR}/stack.tif")
	threshold = auto_threshold(image[0])
	print(threshold)
	assert True

##################################################
def test_auto_threshold_dll():
	"""
	Test basique sur l'auto-seuillage avec la DLL.

	.. todo::
		Trouver un moyen de comparer avec les bons paramètres une sortie de PALM Tracer.
	"""
	dll = load_dll().get("CPU", None)
	if dll is None: print_warning("Test non effectué car DLL manquante")
	else:
		image = open_tif(f"{INPUT_DIR}/stack.tif")
		roi, iterations = 7, 4
		threshold = auto_threshold_dll(dll, image[0], roi, iterations)
		print(threshold)
	assert True
