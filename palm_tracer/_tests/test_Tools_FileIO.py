"""Teste les fonctions de lecture, d'écriture et de gestion des fichiers."""

import ctypes
import shutil

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
NOISE_2D = np.random.default_rng(42).random((SIZE, SIZE)) * MAX_UI_8  # .Bruit sur une image 2D
REF_BOOLEAN_MASK = NOISE_2D > 128  # .									 Conversion en booléen
GRADIENT = np.linspace(0, MAX_UI_8, SIZE, dtype=float)  # .				 Création du dégradé croissant de 0 à 255
REF_GRADIENT = np.tile(GRADIENT, (SIZE, 1))  # .						 Répète le dégradé sur toutes les lignes
REF_STACK = np.stack((REF_GRADIENT, np.fliplr(REF_GRADIENT)), axis=0)  # Empilement du dégradé et son miroir horizontal


##################################################
def test_add_extension():
	"""Vérifie la fonction add extension."""
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
	"""Vérifie la fonction add extension."""
	filename = "filename.extension"
	suffix = "_suffix"
	res = FileIO.add_suffix(filename, suffix)
	assert res == "filename_suffix.extension", "Le nom de fichier ne correspond pas"
	filename = "filename"
	res = FileIO.add_suffix(filename, suffix)
	assert res == "filename_suffix", "Le nom de fichier ne correspond pas"


##################################################
def test_get_timestamp_for_files():
	"""Vérifie la fonction get timestamp for files."""
	res = FileIO.get_timestamp_for_files(True)
	print(f"Timestamp with hour : {res}")
	res = FileIO.get_timestamp_for_files(False)
	print(f"Timestamp without hour : {res}")


##################################################
def test_get_last_file():
	"""Vérifie la fonction get_last_file."""
	res = FileIO.get_last_file(INPUT_DIR, "File", "alpha")
	print(res)
	assert res.endswith("File-03.txt"), "Fichier trouvé incorrect"
	res = FileIO.get_last_file(INPUT_DIR, "File", "time")
	# L'ordre de création des fichiers de test lors de la copie peut changer, on ne peut faire un vrai assert.
	# Assert res.endswith("File-03.txt"), "Fichier trouvé incorrect."
	print(res)


##################################################
def test_extract_suffix():
	"""Vérifie la fonction extract_suffix."""
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
def test_cleanup_process():
	"""Vérifie la fonction cleanup."""
	folder = OUTPUT_DIR / "process"
	FileIO.cleanup_process(folder, "0")  # Dossier inexistant
	folder.mkdir(parents=True, exist_ok=True)
	FileIO.cleanup_process(folder, "0")  # Dossier Existant mais vide

	# Creation d'un fichier qui sera à conserver
	keep = folder / "log-0.log"
	keep.touch()
	FileIO.cleanup_process(folder, "0")  # Dossier Existant mais vide

	# Creation de fichier qui sera à supprimer
	waste = folder / "file-0.csv"
	waste.touch()
	FileIO.cleanup_process(folder, "0")  # Dossier Existant mais vide

	shutil.rmtree(folder)


##################################################
def test_load_dll():
	"""Vérifie la fonction load_dll."""
	res = FileIO.load_dll("File")
	assert res is None, "La Dll n'existe pas, None devrait être retourné."
	res = FileIO.load_dll("CPU")
	assert isinstance(res, ctypes.CDLL), "La Dll devrait être chargé."


##################################################
def test_json_roundtrip(tmp_path):
	"""Vérifie que le fichier JSON écrit restitue intégralement le dictionnaire initial."""
	path = tmp_path / "settings.json"
	FileIO.save_json(path, REF_DICT)
	assert FileIO.open_json(path) == REF_DICT, "Le dictionnaire relu doit correspondre à l'entrée."


##################################################
def test_open_json_bad_file():
	"""Vérifie la fonction open_json avec un fichier inexistant."""
	with pytest.raises(OSError) as exception_info:
		_ = FileIO.open_json("bad_filename.json")
	assert exception_info.type == OSError, "L'erreur relevé n'est pas correcte."


##################################################
@pytest.mark.parametrize("image", [pytest.param(REF_STACK, id="pile"), pytest.param(REF_GRADIENT, id="image-2d")])
def test_tif_roundtrip(image, tmp_path):
	"""Vérifie les pixels, le type et les dimensions du TIFF écrit puis relu."""
	path = tmp_path / "image.tif"
	original = image.copy()
	FileIO.save_tif(image, path)
	result = FileIO.open_tif(path)
	expected = image if image.ndim == 3 else image[None]
	assert result.shape == expected.shape
	assert result.dtype == np.uint16
	np.testing.assert_allclose(result, expected, atol=1, rtol=0)
	np.testing.assert_array_equal(image, original)


##################################################
def test_save_tif_rgb():
	"""Vérifie l'export RGB, les métadonnées, la saturation et la conservation de l'entrée."""
	import tifffile

	stack = np.array([[[[-10, 12.9, 300], [255, 0, 128]]], [[[1, 2, 3], [4, 5, 6]]]], dtype=float)
	original = stack.copy()
	path = OUTPUT_DIR / "test_save_stack_rgb.tif"
	FileIO.save_tif(stack, path)
	with tifffile.TiffFile(path) as tif:
		res = tif.asarray()
		assert tif.series[0].axes == "TYXS"
		assert tif.pages[0].photometric == tifffile.PHOTOMETRIC.RGB
	np.testing.assert_array_equal(res, [[[[0, 12, 255], [255, 0, 128]]], [[[1, 2, 3], [4, 5, 6]]]])
	assert res.dtype == np.uint8 and res.shape == stack.shape
	np.testing.assert_array_equal(stack, original)
	# Une séquence à un seul plan doit conserver sa dimension temporelle.
	FileIO.save_tif(res[:1], path)
	np.testing.assert_array_equal(tifffile.imread(path), res[:1])


##################################################
def test_save_tif_bad_stack():
	"""Vérifie la fonction save_tif avec une image de dimension incorrecte."""
	for shape in (1, (1, 2, 3, 4, 3), (2, 3, 4, 2), (2, 3, 4, 4)):
		with pytest.raises(ValueError): FileIO.save_tif(np.zeros(shape), OUTPUT_DIR / "test_save_stack_invalid.tif")


##################################################
def test_open_tif():
	"""Vérifie la fonction open_tif."""
	stack = FileIO.open_tif(f"{INPUT_DIR}/stack2D.tif")
	assert stack.shape == (1, 128, 128)


##################################################
def test_open_tif_bad_file():
	"""Vérifie la fonction open_tif avec un fichier inexistant."""
	with pytest.raises(OSError) as exception_info: _ = FileIO.open_tif("bad_filename.png")
	assert exception_info.type == OSError, "L'erreur relevé n'est pas correcte."

	with pytest.raises(ValueError) as exception_info: _ = FileIO.open_tif(f"{INPUT_DIR}/stack4D.tif")
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."


##################################################
def test_save_png():
	"""Vérifie la fonction save_png."""
	FileIO.save_png(REF_GRADIENT, f"{OUTPUT_DIR}/test_save.png")
	FileIO.save_png(REF_GRADIENT, f"{OUTPUT_DIR}/test_save_no_normalization.png", False)
	FileIO.save_png(np.zeros_like(REF_GRADIENT), f"{OUTPUT_DIR}/test_save_black.png")


##################################################
def test_save_png_color():
	"""Vérifie la fonction save_png."""
	img = (REF_GRADIENT * MAX_UI_16 / MAX_UI_8).astype(np.uint16)  # Passage en uint 16
	FileIO.save_png(FileIO.grayscale_to_color(img), f"{OUTPUT_DIR}/test_save_color.png", normalization=False)


##################################################
def test_save_png_bad_sample():
	"""Vérifie la fonction save_png avec un tableau 1D."""
	with pytest.raises(ValueError) as exception_info:
		FileIO.save_png(REF_GRADIENT[1, :], f"{OUTPUT_DIR}/test_save_bad.png")
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."


##################################################
def test_open_calibration_mat_bad_file():
	"""Vérifie la fonction open_tif avec un fichier inexistant."""
	with pytest.raises(OSError) as exception_info:
		_ = FileIO.open_calibration_mat("bad_filename.mat")
	assert exception_info.type == OSError, "L'erreur relevé n'est pas correcte."


##################################################
def test_open_calibration_mat():
	"""Vérifie la fonction open_tif avec un fichier inexistant."""
	calib = FileIO.open_calibration_mat(f"{INPUT_DIR}/calibration.mat")
	res, ref = calib["coeff"].shape, (14, 14, 6, 64)
	assert res == ref, f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"
