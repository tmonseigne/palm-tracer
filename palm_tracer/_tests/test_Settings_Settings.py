""" Fichier des tests pour l'ensemble des paramètres. """

import sys

from qtpy.QtCore import QCoreApplication, Qt
from qtpy.QtWidgets import QApplication

from palm_tracer.Settings import Settings
from palm_tracer.Settings.Groups import Calibration


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
	settings.calibration["Pixel Size"].set_value(320)
	dictionary = settings.to_dict()
	settings.reset()
	assert settings.calibration["Pixel Size"].get_value() == 160, "Le paramètre n'a pas été remis à sa valeur par défaut."
	settings = Settings.from_dict(dictionary)
	assert settings.calibration["Pixel Size"].get_value() == 320, "Le paramètre n'a pas été correctement enregistré dans le dicrtionnaire."
	print(settings)
