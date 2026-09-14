"""Teste les fonctions de lecture, d'écriture et de gestion des fichiers."""

import ctypes
from datetime import datetime
from unittest.mock import Mock

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


# ==================================================
# region Gestion des fichiers
# ==================================================
##################################################
@pytest.mark.parametrize("filename, extension, expected", [
		pytest.param("filename.extension", "new", "filename.extension.new", id="existing-extension"),
		pytest.param("filename", "new", "filename.new", id="no-extension"),
		pytest.param("file.name.extension", "new", "file.name.extension.new", id="multiple-dots"),
		pytest.param("file/name/extension", "new", "file/name/extension.new", id="with-directories"),
		pytest.param("filename.new", "new", "filename.new", id="extension-already-present"),
		pytest.param("filename", ".new", "filename.new", id="extension-with-dot")])
def test_add_extension(filename, extension, expected):
	"""Vérifie l'ajout d'une extension sans duplication du point ou de l'extension."""
	assert FileIO.add_extension(filename, extension) == expected


##################################################
@pytest.mark.parametrize("filename, expected", [
		pytest.param("filename.extension", "filename_suffix.extension", id="with-extension"),
		pytest.param("filename", "filename_suffix", id="no-extension")])
def test_add_suffix(filename, expected):
	"""Vérifie l'insertion du suffixe avant l'extension éventuelle."""
	assert FileIO.add_suffix(filename, "_suffix") == expected


##################################################
@pytest.mark.parametrize("with_hour, expected", [pytest.param(True, "20260102_030405", id="with-time"), pytest.param(False, "20260102", id="date-only")])
def test_get_timestamp_for_files(monkeypatch, with_hour, expected):
	"""Vérifie le format exact de l'horodatage à partir d'une date contrôlée."""
	clock = Mock()
	clock.now.return_value = datetime(2026, 1, 2, 3, 4, 5)
	monkeypatch.setattr(FileIO, "datetime", clock)
	assert FileIO.get_timestamp_for_files(with_hour) == expected


##################################################
@pytest.mark.parametrize("sort_mode, expected", [
		pytest.param("alpha", "File-03.txt", id="alphabetical-order"), pytest.param("time", "File-01.txt", id="modification-time")])
def test_get_last_file(tmp_path, sort_mode, expected):
	"""Vérifie que les tris alphabétique et temporel sélectionnent des fichiers distincts."""
	for name, timestamp in (("File-01.txt", 200), ("File-03.txt", 100), ("Other-99.txt", 300)):
		path = tmp_path / name
		path.touch()
		os.utime(path, (timestamp, timestamp))
	(tmp_path / "File-99.txt").mkdir()  # Un dossier ne doit pas être sélectionné.
	assert Path(FileIO.get_last_file(tmp_path, "File", sort_mode)).name == expected


##################################################
@pytest.mark.parametrize("folder_exists", [pytest.param(False, id="missing-directory"), pytest.param(True, id="no-match")])
def test_get_last_file_not_found(tmp_path, folder_exists):
	"""Vérifie le résultat vide en l'absence de fichier correspondant."""
	folder = tmp_path / "files"
	if folder_exists:
		folder.mkdir()
		(folder / "Other.txt").touch()
	assert FileIO.get_last_file(folder, "File") == ""


##################################################
@pytest.mark.parametrize("filename, expected", [
		pytest.param("", "", id="empty-name"), pytest.param("filename", "", id="no-extension"),
		pytest.param("filename.json", "", id="no-suffix"), pytest.param("filename-01.json", "01", id="single-suffix"),
		pytest.param("filename-01-02-03.json", "03", id="last-suffix")])
def test_extract_suffix(filename, expected):
	"""Vérifie l'extraction du dernier suffixe, ou une chaîne vide en son absence."""
	assert FileIO.extract_suffix(filename) == expected


##################################################
@pytest.mark.parametrize("files, expected", [
		pytest.param((), (), id="empty-directory"),
		pytest.param(("meta-0.csv", "settings-0.json", "log-0.log"), (), id="administrative-files-only"),
		pytest.param(("log-0.log", "file-0.csv"), ("log-0.log", "file-0.csv"), id="result-still-present"),
		pytest.param(("log-0.log", "log-1.log"), ("log-1.log",), id="other-timestamp-preserved")])
def test_cleanup_process(tmp_path, files, expected):
	"""Vérifie les fichiers supprimés ou conservés selon les sorties encore présentes."""
	for name in files: (tmp_path / name).touch()
	FileIO.cleanup_process(tmp_path, "0")
	assert {path.name for path in tmp_path.iterdir()} == set(expected)


##################################################
def test_cleanup_process_missing_folder(tmp_path):
	"""Vérifie que le nettoyage d'un dossier absent ne crée aucun fichier."""
	folder = tmp_path / "missing"
	FileIO.cleanup_process(folder, "0")
	assert not folder.exists()


##################################################
def test_load_dll():
	"""Vérifie le chargement de la bibliothèque de calcul CPU."""
	assert isinstance(FileIO.load_dll("CPU"), ctypes.CDLL)


##################################################
def test_load_dll_missing():
	"""Vérifie qu'une bibliothèque absente ne peut pas être chargée."""
	assert FileIO.load_dll("File") is None


# ==================================================
# endregion Gestion des fichiers
# ==================================================

# ==================================================
# region Entrées-sorties JSON
# ==================================================
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


# ==================================================
# endregion Entrées-sorties JSON
# ==================================================

# ==================================================
# region Entrées-sorties TIFF
# ==================================================
##################################################
@pytest.mark.parametrize("image", [pytest.param(REF_STACK, id="stack"), pytest.param(REF_GRADIENT, id="2d-image")])
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
def test_save_tif_rgb(tmp_path):
	"""Vérifie l'export RGB, les métadonnées, la saturation et la conservation de l'entrée."""
	import tifffile

	stack = np.array([[[[-10, 12.9, 300], [255, 0, 128]]], [[[1, 2, 3], [4, 5, 6]]]], dtype=float)
	original = stack.copy()
	path = tmp_path / "image_rgb.tif"
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
@pytest.mark.parametrize("shape", [
		pytest.param((1,), id="1d-array"),
		pytest.param((1, 2, 3, 4, 3), id="5d-array"),
		pytest.param((2, 3, 4, 2), id="two-channels"),
		pytest.param((2, 3, 4, 4), id="four-channels")])
def test_save_tif_bad_stack(shape, tmp_path):
	"""Vérifie le rejet des dimensions et nombres de canaux non pris en charge."""
	with pytest.raises(ValueError): FileIO.save_tif(np.zeros(shape), tmp_path / "invalid.tif")


##################################################
def test_open_tif():
	"""Vérifie la fonction open_tif."""
	stack = FileIO.open_tif(f"{INPUT_DIR}/stack2D.tif")
	assert stack.shape == (1, 128, 128)


##################################################
@pytest.mark.parametrize("filename, error", [
		pytest.param("bad_filename.png", OSError, id="missing-file"),
		pytest.param(INPUT_DIR / "stack4D.tif", ValueError, id="invalid-dimensions")])
def test_open_tif_bad_file(filename, error):
	"""Vérifie les erreurs de lecture pour un fichier absent ou incompatible."""
	with pytest.raises(error): FileIO.open_tif(filename)


# ==================================================
# endregion Entrées-sorties TIFF
# ==================================================

# ==================================================
# region Entrées-sorties PNG
# ==================================================
##################################################
@pytest.mark.parametrize("image, normalization", [
		pytest.param(REF_GRADIENT, True, id="normalization"),
		pytest.param(REF_GRADIENT, False, id="no-normalization"),
		pytest.param(np.zeros_like(REF_GRADIENT), True, id="black-image")])
def test_save_png(image, normalization, tmp_path):
	"""Vérifie les pixels de l'image PNG écrite puis relue."""
	from PIL import Image

	path = tmp_path / "image.png"
	FileIO.save_png(image, path, normalization)
	with Image.open(path) as saved:
		result = np.array(saved)
	assert result.shape == image.shape
	np.testing.assert_allclose(result, image, atol=1, rtol=0)


##################################################
def test_save_png_color(tmp_path):
	"""Vérifie la fonction save_png."""
	img = (REF_GRADIENT * MAX_UI_16 / MAX_UI_8).astype(np.uint16)  # Passage en uint 16
	FileIO.save_png(FileIO.grayscale_to_color(img), tmp_path / "color.png", normalization=False)


##################################################
def test_save_png_bad_sample(tmp_path):
	"""Vérifie la fonction save_png avec un tableau 1D."""
	with pytest.raises(ValueError) as exception_info:
		FileIO.save_png(REF_GRADIENT[1, :], tmp_path / "invalid.png")
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."


# ==================================================
# endregion Entrées-sorties PNG
# ==================================================

# ==================================================
# region Entrées-sorties MATLAB
# ==================================================
##################################################
def test_open_calibration_mat_bad_file():
	"""Vérifie le rejet d’un fichier de calibration MATLAB inexistant."""
	with pytest.raises(OSError) as exception_info:
		_ = FileIO.open_calibration_mat("bad_filename.mat")
	assert exception_info.type == OSError, "L'erreur relevé n'est pas correcte."


##################################################
def test_open_calibration_mat():
	"""Vérifie les dimensions des coefficients de calibration MATLAB."""
	calib = FileIO.open_calibration_mat(f"{INPUT_DIR}/calibration.mat")
	res, ref = calib["coeff"].shape, (14, 14, 6, 64)
	assert res == ref, f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"

# ==================================================
# endregion Entrées-sorties MATLAB
# ==================================================
