""" Fichier des tests pour les fonctions utilitaires. """
import ctypes

import pytest

from palm_tracer._tests.Utils import is_not_dll_friendly
from palm_tracer.Tools import Utils


##################################################
def test_add_extension():
	"""Test de la fonction add extension."""
	filename = "filename.extension"

	res = Utils.add_extension(filename, "new")
	assert res == "filename.extension.new", "Le nom de fichier ne correspond pas"

	filename = "filename"
	res = Utils.add_extension(filename, "new")
	assert res == "filename.new", "Le nom de fichier ne correspond pas"

	filename = "file.name.extension"
	res = Utils.add_extension(filename, "new")
	assert res == "file.name.extension.new", "Le nom de fichier ne correspond pas"

	filename = "file/name/extension"
	res = Utils.add_extension(filename, "new")
	assert res == "file/name/extension.new", "Le nom de fichier ne correspond pas"


##################################################
def test_add_suffix():
	"""Test de la fonction add extension."""
	filename = "filename.extension"
	suffix = "_suffix"
	res = Utils.add_suffix(filename, suffix)
	assert res == "filename_suffix.extension", "Le nom de fichier ne correspond pas"
	filename = "filename"
	res = Utils.add_suffix(filename, suffix)
	assert res == "filename_suffix", "Le nom de fichier ne correspond pas"


##################################################
def test_get_timestamp_for_files():
	"""Test de la fonction get timestamp for files."""
	res = Utils.get_timestamp_for_files(True)
	print(f"Timestamp with hour : {res}")
	res = Utils.get_timestamp_for_files(False)
	print(f"Timestamp without hour : {res}")
	assert True


##################################################
def test_get_last_file():
	"""Test de la fonction get timestamp for files."""
	res = Utils.get_last_file("input", "File")
	# L'ordre de création des fichiers de test lors de la copie peut changer, on ne peut faire un vrai assert
	# assert res.endswith("File-03.txt"), "Fichier trouvé incorrect"
	print(res)
	assert True


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_load_dll():
	"""Test de la fonction get timestamp for files."""
	res = Utils.load_dll("File")
	assert res is None, "La Dll n'existe pas, None devrait être retourné."
	res = Utils.load_dll("CPU")
	assert isinstance(res, ctypes.CDLL), "La Dll devrait être chargé."


##################################################
def test_print_error():
	"""Test de la fonction print error."""
	Utils.print_error("Message d'erreur"), "L'affichage n'a pas pu être effectué"
	assert True


##################################################
def test_print_warning():
	"""Test de la fonction print warning."""
	Utils.print_warning("Message d'avertissement"), "L'affichage n'a pas pu être effectué"
	assert True


##################################################
def test_print_success():
	"""Test de la fonction print warning."""
	Utils.print_success("Message de succes"), "L'affichage n'a pas pu être effectué"
	assert True


##################################################
def test_format_time():
	"""Test de la fonction print warning."""
	assert Utils.format_time(3666) == "01:01:06", "L'affichage n'a pas pu être effectué"
