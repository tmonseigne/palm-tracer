"""Fichier des tests pour la lecture/écriture des fichiers."""
import ctypes

import pytest

from palm_tracer._tests.Utils import *
from palm_tracer.Tools import FileIO

REF_DICT = {"First param":  [0, 1, 2],
			"2nd param":    True,
			"3rd param":    "True",
			"élément":      0,
			"Inception":    {"intern": 0},
			"setting":      {"value": 0},
			"setting list": {"value": [0, 1]}}

MAX_UI_16 = np.iinfo(np.uint16).max
MAX_UI_8 = np.iinfo(np.uint8).max

SIZE = 512  # .															 Taille de l'image de test
NOISE_2D = np.random.rand(SIZE, SIZE) * MAX_UI_8  # .					 Bruit sur une image 2D
REF_BOOLEAN_MASK = NOISE_2D > 128  # .									 Conversion en booléen
GRADIENT = np.linspace(0, MAX_UI_8, SIZE, dtype=np.float32)  # .		 Création du dégradé croissant de 0 à 255
REF_GRADIENT = np.tile(GRADIENT, (SIZE, 1))  # .						 Répète le dégradé sur toutes les lignes
REF_STACK = np.stack((REF_GRADIENT, np.fliplr(REF_GRADIENT)), axis=0)  # Empilement du dégradé et son miroir horizontal


##################################################
def test_add_extension():
	"""Test de la fonction add extension."""
	filename = "filename.extension"

	res = FileIO.add_extension(filename, "new")
	assert res == "filename.extension.new", "Le nom de fichier ne correspond pas"

	filename = "filename"
	res = FileIO.add_extension(filename, "new")
	assert res == "filename.new", "Le nom de fichier ne correspond pas"

	filename = "file.name.extension"
	res = FileIO.add_extension(filename, "new")
	assert res == "file.name.extension.new", "Le nom de fichier ne correspond pas"

	filename = "file/name/extension"
	res = FileIO.add_extension(filename, "new")
	assert res == "file/name/extension.new", "Le nom de fichier ne correspond pas"


##################################################
def test_add_suffix():
	"""Test de la fonction add extension."""
	filename = "filename.extension"
	suffix = "_suffix"
	res = FileIO.add_suffix(filename, suffix)
	assert res == "filename_suffix.extension", "Le nom de fichier ne correspond pas"
	filename = "filename"
	res = FileIO.add_suffix(filename, suffix)
	assert res == "filename_suffix", "Le nom de fichier ne correspond pas"


##################################################
def test_get_timestamp_for_files():
	"""Test de la fonction get timestamp for files."""
	res = FileIO.get_timestamp_for_files(True)
	print(f"Timestamp with hour : {res}")
	res = FileIO.get_timestamp_for_files(False)
	print(f"Timestamp without hour : {res}")


##################################################
def test_get_last_file():
	"""Test de la fonction get_last_file."""
	res = FileIO.get_last_file(INPUT_DIR, "File", "alpha")
	print(res)
	assert res.endswith("File-03.txt"), "Fichier trouvé incorrect"
	res = FileIO.get_last_file(INPUT_DIR, "File", "time")
	# L'ordre de création des fichiers de test lors de la copie peut changer, on ne peut faire un vrai assert.
	# assert res.endswith("File-03.txt"), "Fichier trouvé incorrect."
	print(res)


##################################################
def test_extract_suffix():
	"""Test de la fonction extract_suffix."""
	res = FileIO.extract_suffix("")
	assert res == "", f"Suffixe incorrect.\nAttendu : \"\"\tObtenu : {res}"

	res = FileIO.extract_suffix("filename")
	assert res == "", f"Suffixe incorrect.\nAttendu : \"\"\tObtenu : {res}"

	res = FileIO.extract_suffix("filename.json")
	assert res == "", f"Suffixe incorrect.\nAttendu : \"\"\tObtenu : {res}"

	res = FileIO.extract_suffix("filename-01.json")
	assert res == "01", f"Suffixe incorrect.\nAttendu : \"\"\tObtenu : {res}"

	res = FileIO.extract_suffix("filename-01-02-03.json")
	assert res == "03", f"Suffixe incorrect.\nAttendu : \"\"\tObtenu : {res}"


##################################################
def test_load_dll():
	"""Test de la fonction load_dll."""
	res = FileIO.load_dll("File")
	assert res is None, "La Dll n'existe pas, None devrait être retourné."
	res = FileIO.load_dll("CPU")
	assert isinstance(res, ctypes.CDLL), "La Dll devrait être chargé."


##################################################
def test_save_json():
	"""Test de la fonction save_json."""
	FileIO.save_json(f"{OUTPUT_DIR}/test_save_json.json", REF_DICT)


##################################################
def test_open_json():
	"""Test de la fonction open_json."""
	dictionary = FileIO.open_json(f"{OUTPUT_DIR}/test_save_json.json")
	assert dictionary == REF_DICT, "Le dictionnaire devrait correspondre à la référence."


##################################################
def test_open_json_bad_file():
	"""Test de la fonction open_json avec un fichier inexistant."""
	with pytest.raises(OSError) as exception_info:
		_ = FileIO.open_json("bad_filename.json")
	assert exception_info.type == OSError, "L'erreur relevé n'est pas correcte."


##################################################
def test_save_tif():
	"""	Test de la fonction save_tif."""
	FileIO.save_tif(REF_STACK, f"{OUTPUT_DIR}/test_save_stack.tif")


##################################################
def test_save_tif_2d():
	"""Test de la fonction save_tif avec une image 2D."""
	FileIO.save_tif(REF_GRADIENT, f"{OUTPUT_DIR}/test_save_stack_2D.tif")


##################################################
def test_save_tif_bad_stack():
	"""Test de la fonction save_tif avec une image 1D."""
	with pytest.raises(ValueError) as exception_info:
		FileIO.save_tif(REF_GRADIENT[1, :], f"{OUTPUT_DIR}/test_save_stack_1D.tif")
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."


##################################################
def test_open_tif():
	"""Test de la fonction open_tif."""
	stack = FileIO.open_tif(f"{OUTPUT_DIR}/test_save_stack.tif")
	assert np.allclose(REF_STACK, stack, atol=1), "L'échantillon devrait correspondre à la référence avec une tolérance d'erreur (passage en entier)."


##################################################
def test_open_tif_bad_file():
	"""Test de la fonction open_tif avec un fichier inexistant."""
	with pytest.raises(OSError) as exception_info:
		_ = FileIO.open_tif("bad_filename.png")
	assert exception_info.type == OSError, "L'erreur relevé n'est pas correcte."


##################################################
def test_save_png():
	"""Test de la fonction save_png."""
	FileIO.save_png(REF_GRADIENT, f"{OUTPUT_DIR}/test_save.png")
	FileIO.save_png(REF_GRADIENT, f"{OUTPUT_DIR}/test_save_no_normalization.png", False)
	FileIO.save_png(np.zeros_like(REF_GRADIENT), f"{OUTPUT_DIR}/test_save_black.png")


##################################################
def test_save_png_color():
	"""Test de la fonction save_png."""
	img = (REF_GRADIENT * MAX_UI_16 / MAX_UI_8).astype(np.uint16)  # Passage en uint 16
	FileIO.save_png(FileIO.grayscale_to_color(img), f"{OUTPUT_DIR}/test_save_color.png", normalization=False)


##################################################
def test_save_png_bad_sample():
	"""Test de la fonction save_png avec un tableau 1D."""
	with pytest.raises(ValueError) as exception_info:
		FileIO.save_png(REF_GRADIENT[1, :], f"{OUTPUT_DIR}/test_save_bad.png")
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."


##################################################
def test_open_calibration_mat_bad_file():
	"""Test de la fonction open_tif avec un fichier inexistant."""
	with pytest.raises(OSError) as exception_info:
		_ = FileIO.open_calibration_mat("bad_filename.mat")
	assert exception_info.type == OSError, "L'erreur relevé n'est pas correcte."


##################################################
def test_open_calibration_mat():
	"""Test de la fonction open_tif avec un fichier inexistant."""
	calib = FileIO.open_calibration_mat(f"{INPUT_DIR}/calibration.mat")
	res, ref = calib["coeff"].shape, (14, 14, 6, 64)
	assert res == ref, f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"
