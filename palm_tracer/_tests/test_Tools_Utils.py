""" Fichier des tests pour les fonctions utilitaires """

from palm_tracer.Tools.Utils import add_extension, add_suffix, get_timestamp_for_files, print_error, print_warning


##################################################
def test_add_extension():
	""" Test de la fonction add extension. """
	filename = "filename.extension"

	res = add_extension(filename, "new")
	assert res == "filename.extension.new", f"Le nom de fichier ne correspond pas"

	filename = "filename"
	res = add_extension(filename, "new")
	assert res == "filename.new", f"Le nom de fichier ne correspond pas"

	filename = "file.name.extension"
	res = add_extension(filename, "new")
	assert res == "file.name.extension.new", f"Le nom de fichier ne correspond pas"

	filename = "file/name/extension"
	res = add_extension(filename, "new")
	assert res == "file/name/extension.new", f"Le nom de fichier ne correspond pas"


##################################################
def test_add_suffix():
	""" Test de la fonction add extension. """
	filename = "filename.extension"
	suffix = "_suffix"
	res = add_suffix(filename, suffix)
	assert res == "filename_suffix.extension", f"Le nom de fichier ne correspond pas"
	filename = "filename"
	res = add_suffix(filename, suffix)
	assert res == "filename_suffix", f"Le nom de fichier ne correspond pas"


##################################################
def test_get_timestamp_for_files():
	""" Test de la fonction get timestamp for files. """
	res = get_timestamp_for_files(True)
	print(res)
	res = get_timestamp_for_files(False)
	print(res)
	assert True


##################################################
def test_print_error():
	""" Test de la fonction print error. """
	print_error("Message d'erreur"), "L'affichage n'a pas pu être effectué"
	assert True


##################################################
def test_print_warning():
	""" Test de la fonction print warning. """
	print_warning("Message d'avertissement"), "L'affichage n'a pas pu être effectué"
	assert True
