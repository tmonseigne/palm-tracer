""" Fichier des tests pour l'ensemble des paramètres. """

import sys
from pathlib import Path

from qtpy.QtCore import QCoreApplication, Qt
from qtpy.QtWidgets import QApplication

from palm_tracer.Settings import Settings
from palm_tracer.Settings.Group import Calibration

INPUT_DIR = Path(__file__).parent / "Input"


##################################################
def initialize():
	"""Fixture pour initialiser l'application Qt"""
	# Si nous sommes dans un environnement CI, forcez l'application à ne pas afficher les fenêtres graphiques
	if not sys.stdout.isatty():  # Vérifie si on est dans un terminal (et donc potentiellement CI)
		QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_DisableHighDpiScaling)
		QApplication.setAttribute(Qt.ApplicationAttribute.AA_Use96Dpi)

	app = QApplication([])  # Initialisation de QApplication
	return app


###################################################
def test_settings():
	"""Test basique de la classe (constructeur, getter, setter)"""
	app = initialize()
	settings = Settings()
	names = ["Batch", "Calibration", "Localisation"]
	assert "Calibration" in settings, "Le groupe Calibration n'existe pas"
	assert settings.get_group_names() == names, "Les groupes de paramètres ne correspondent pas"

	group = settings["Calibration"]
	assert isinstance(group, Calibration), "Le paramètre ne correspond pas"

	for key in settings: assert key != "", "Une clé est vide"
	settings.reset()
	print(settings)
