""" Fichier des tests pour l'ensemble des paramètres. """

from palm_tracer.Settings import Settings
from palm_tracer.Settings.Groups import *


###################################################
def test_settings(make_napari_viewer):
	"""Test basique de la classe (constructeur, getter, setter)"""
	settings = Settings()
	settings.calibration["Pixel Size"].set_value(320)
	dictionary = settings.to_dict()
	settings.reset()
	assert settings.calibration["Pixel Size"].get_value() == 160, "Le paramètre n'a pas été remis à sa valeur par défaut."
	settings = Settings.from_dict(dictionary)
	assert settings.calibration["Pixel Size"].get_value() == 320, "Le paramètre n'a pas été correctement enregistré dans le dicrtionnaire."
	print(settings)

###################################################
def test_settings_group_getter(make_napari_viewer):
	"""Test de récupération des différents groupes de settings"""
	settings = Settings()
	s = settings.batch
	assert isinstance(s, Batch), "Récupération du groupe incorrecte."
	s = settings.calibration
	assert isinstance(s, Calibration), "Récupération du groupe incorrecte."
	s = settings.localization
	assert isinstance(s, Localization), "Récupération du groupe incorrecte."
	s = settings.tracking
	assert isinstance(s, Tracking), "Récupération du groupe incorrecte."
	s = settings.visualization_hr
	assert isinstance(s, VisualizationHR), "Récupération du groupe incorrecte."
	s = settings.visualization_graph
	assert isinstance(s, VisualizationGraph), "Récupération du groupe incorrecte."


###################################################
def test_settings_getter(make_napari_viewer):
	settings = Settings()
	s = settings.get_localisation_settings()
	assert len(s.keys()) == 6, "Le nombre de settings ne correspond pas."
	s = settings.get_tracking_settings()
	assert len(s.keys()) == 4, "Le nombre de settings ne correspond pas."
	s = settings.get_hr_settings()
	assert len(s.keys()) == 2, "Le nombre de settings ne correspond pas."
	s = settings.get_graph_settings()
	assert len(s.keys()) == 2, "Le nombre de settings ne correspond pas."
