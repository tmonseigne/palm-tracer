"""Fichier des tests pour les fonctions en lien avec l'affichage."""

from palm_tracer.Tools import Ui


##################################################
def test_print_error():
	"""Test de la fonction print error."""
	Ui.print_error("Message d'erreur"), "L'affichage n'a pas pu être effectué"


##################################################
def test_print_warning():
	"""Test de la fonction print warning."""
	Ui.print_warning("Message d'avertissement"), "L'affichage n'a pas pu être effectué"


##################################################
def test_print_success():
	"""Test de la fonction print warning."""
	Ui.print_success("Message de succes"), "L'affichage n'a pas pu être effectué"


##################################################
def test_format_time():
	"""Test de la fonction print warning."""
	assert Ui.format_time(3666) == "01:01:06", "L'affichage n'a pas pu être effectué"
