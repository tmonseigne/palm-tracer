""" Fichier des tests pour l'ensemble des paramètres. """

import sys
from pathlib import Path
from typing import Type

from qtpy.QtCore import QCoreApplication, Qt
from qtpy.QtWidgets import QApplication

from palm_tracer.Settings.Group import *
from palm_tracer.Settings.SettingTypes import BaseSettingType, CheckSetting, FileSetting, FloatSetting, IntSetting

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
def group_base_test(group: BaseSettingGroup, names: list[str], first_type: Type[BaseSettingType]):
	"""
	Tests de base pour un groupe de paramètres

	:param group: Groupe de paramètres
	:param names: Nom des paramètres du groupe
	:param first_type: Type du premier paramètre
	"""

	assert names[0] in group, "La clé n'existe pas"
	assert group.get_setting_names() == names, "Les paramètres ne correspondent pas"
	setting = group[names[0]]
	assert isinstance(setting, first_type), "Le paramètre ne correspond pas"
	for key in group: assert key != "", "Une clé est vide"

	group.reset()
	print(group)
	print(group.to_dict())


###################################################
def test_batch():
	""" Test basique de la classe Batch (constructeur, getter, setter) """
	app = initialize()
	group_base_test(Batch(), ["Add File", "Files", "Mode"], FileSetting)


###################################################
def test_calibration():
	""" Test basique de la classe Calibration (constructeur, getter, setter) """
	app = initialize()
	group_base_test(Calibration(), ["Pixel Size", "Exposure", "Intensity"], IntSetting)


###################################################
def test_localisation():
	""" Test basique de la classe Calibration (constructeur, getter, setter) """
	app = initialize()
	group_base_test(Localisation(), ["Preview", "Threshold", "ROI Size","Watershed","Mode", "Gaussian Fit"], CheckSetting)


###################################################
def test_gaussian_fit():
	""" Test basique de la classe Calibration (constructeur, getter, setter) """
	app = initialize()
	group_base_test(GaussianFit(), ["Sigma", "Sigma Fixed", "Theta", "Theta Fixed"], FloatSetting)
