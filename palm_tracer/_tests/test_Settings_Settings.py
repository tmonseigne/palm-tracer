""" Fichier des tests pour l'ensemble des paramètres. """

from palm_tracer._tests.Utils import initialize_qt_app_for_testing
from palm_tracer.Settings import Settings


###################################################
def test_settings():
	"""Test basique de la classe (constructeur, getter, setter)"""
	app = initialize_qt_app_for_testing()
	settings = Settings()
	settings.calibration["Pixel Size"].set_value(320)
	dictionary = settings.to_dict()
	settings.reset()
	assert settings.calibration["Pixel Size"].get_value() == 160, "Le paramètre n'a pas été remis à sa valeur par défaut."
	settings = Settings.from_dict(dictionary)
	assert settings.calibration["Pixel Size"].get_value() == 320, "Le paramètre n'a pas été correctement enregistré dans le dicrtionnaire."
	print(settings)
