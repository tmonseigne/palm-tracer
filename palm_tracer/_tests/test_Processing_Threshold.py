""" Fichier des tests pour l'utilisation des DLL """

from pathlib import Path

from palm_tracer._tests.Utils import is_closed
from palm_tracer.Processing import auto_threshold, auto_threshold_dll, load_dll
from palm_tracer.Tools import open_tif, print_warning

INPUT_DIR = Path(__file__).parent / "input"


##################################################
def test_auto_threshold():
	"""Test basique sur l'auto-seuillage avec la DLL."""
	image = open_tif(f"{INPUT_DIR}/stack.tif")
	res = auto_threshold(image[0])
	ref = 104.247804
	assert is_closed(res, ref), f"Le seuil vaut {res} au lieu de {ref}"


##################################################
def test_auto_threshold_dll():
	""" Test basique sur l'auto-seuillage avec la DLL. """
	dll = load_dll().get("CPU", None)
	if dll is None: print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		image = open_tif(f"{INPUT_DIR}/stack.tif")
		roi, iterations = 7, 4
		ref = [63.634560, 63.701586, 63.058853, 62.557870, 62.474888,
			   63.374433, 63.857703, 63.368484, 62.613244, 63.833786]
		for i in range(image.shape[0]):
			res = auto_threshold_dll(dll, image[i], roi, iterations)
			# print(f"Image {i} : {res:.6f}")
			assert is_closed(res, ref[i]), f"Le seuil pour l'image {i} vaut {res} au lieu de {ref[i]}"
	assert True
