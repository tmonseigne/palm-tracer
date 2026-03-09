"""Fichier des tests pour l'ensemble des paramètres."""
from typing import List

from palm_tracer._tests.Utils import *
from palm_tracer.Settings import Settings
from palm_tracer.Settings.Groups import *


###################################################
def test_settings(qtbot, capsys):
	"""Test basique de la classe (constructeur, getter, setter)"""
	settings = Settings()
	settings.calibration["Pixel Size"].value = 0.32
	dictionary = settings.to_dict()
	settings.reset()
	assert settings.calibration["Pixel Size"].value == 0.16, "Le paramètre n'a pas été remis à sa valeur par défaut."
	settings = Settings.from_dict(dictionary)
	assert settings.calibration["Pixel Size"].value == 0.32, "Le paramètre n'a pas été correctement enregistré dans le dicrtionnaire."
	print(settings)
	lines = get_lines_output(capsys)
	assert len(lines) == 88


###################################################
def test_settings_group_getter(qtbot):
	"""Test de récupération des différents groupes de settings"""
	settings = Settings()
	s = settings.batch
	assert isinstance(s, Batch), "Récupération du groupe incorrecte."
	s = settings.calibration
	assert isinstance(s, Calibration), "Récupération du groupe incorrecte."
	s = settings.localization
	assert isinstance(s, Localization), "Récupération du groupe incorrecte."
	s = settings.drift
	assert isinstance(s, DriftCorrection), "Récupération du groupe incorrecte."
	s = settings.tracking
	assert isinstance(s, Tracking), "Récupération du groupe incorrecte."
	s = settings.blinking
	assert isinstance(s, BlinkingReconnection), "Récupération du groupe incorrecte."
	s = settings.tracks_compute
	assert isinstance(s, TracksCompute), "Récupération du groupe incorrecte."
	s = settings.gallery
	assert isinstance(s, Gallery), "Récupération du groupe incorrecte."
	s = settings.visualization_hr
	assert isinstance(s, VisualizationHR), "Récupération du groupe incorrecte."
	s = settings.visualization_graph
	assert isinstance(s, VisualizationGraph), "Récupération du groupe incorrecte."
	s = settings.filtering
	assert isinstance(s, Filtering), "Récupération du groupe incorrecte."


###################################################
def test_settings_signal(qtbot):
	"""Test de Connexion d'un slot Python, blocage et émission."""
	settings = Settings()

	received: List[Any] = []
	settings.connect(lambda v: received.append(v))
	with settings.signal_blocked(): pass
	settings.disconnect()
