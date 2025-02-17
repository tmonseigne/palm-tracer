""" Fichier des tests pour l'utilisation des DLL """

from pathlib import Path

import numpy as np

from palm_tracer.Processing import auto_threshold, auto_threshold_dll, load_dll
from palm_tracer.Tools import open_tif, print_warning

INPUT_DIR = Path(__file__).parent / "input"


##################################################
def is_closed(value: float, ref: float, tol: float = 1e-5):
	return (np.abs(value) - ref) <= tol


##################################################
def test_auto_threshold():
	"""Test basique sur l'auto-seuillage avec la DLL."""
	image = open_tif(f"{INPUT_DIR}/stack.tif")
	res = auto_threshold(image[0])
	ref = 104.247804
	assert is_closed(res, ref), f"Le seuil vaut {res} au lieu de {ref}"


##################################################
def test_auto_threshold_dll():
	"""
	Test basique sur l'auto-seuillage avec la DLL.

	.. todo::
		Comparer avec une sortie de PALM Tracer.
		Actuellement différence de résultat, nécessite une investigation
	"""
	dll = load_dll().get("CPU", None)
	if dll is None: print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		image = open_tif(f"{INPUT_DIR}/stack.tif")
		roi, iterations = 7, 4
		ref = [102.749661, 107.684024, 101.971399, 103.139405, 106.806511,
			   101.999329, 104.997113, 092.055165, 098.834634, 096.873310]
		for i in range(image.shape[0]):
			res = auto_threshold_dll(dll, image[i], roi, iterations)
			# print(f"Image {i} : {res:.6f}")
			assert is_closed(res, ref[i]), f"Le seuil pour l'image {i} vaut {res} au lieu de {ref[i]}"
		print_warning("\n====================\nAucune comparaison avec Metamorph dans ce test.\n====================\n")
	assert True
