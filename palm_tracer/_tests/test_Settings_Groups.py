""" Fichier des tests pour l'ensemble des paramètres. """

import sys
from pathlib import Path
from typing import Any, Type

from qtpy.QtCore import QCoreApplication, Qt
from qtpy.QtWidgets import QApplication

from palm_tracer.Settings.Groups import *
from palm_tracer.Settings.Types import *

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
def group_base_test(group: BaseSettingGroup, names: list[str],
					first_type: Type[BaseSettingType], change: Any, default: Any):
	"""
	Tests de base pour un groupe de paramètres

	:param group: Groupe de paramètres
	:param names: Nom des paramètres du groupe
	:param first_type: Type du premier paramètre
	:param change: Changement du premier paramètre
	:param default: Valeur par défaut du premier paramètre
	"""

	assert names[0] in group, "La clé n'existe pas"
	assert group.get_setting_names() == names, "Les paramètres ne correspondent pas"
	setting = group[names[0]]
	assert isinstance(setting, first_type), "Le paramètre ne correspond pas"
	for key in group: assert key != "", "Une clé est vide"

	group[names[0]].set_value(change)
	assert group[names[0]].get_value() == change, "Valeur défini non valide."

	dictionary = group.to_dict()
	group.reset()
	assert group[names[0]].get_value() == default, "Valeur par défaut non valide."

	group = create_group_from_dict(dictionary)
	assert group[names[0]].get_value() == change, "Valeur récupérée du dictionnaire non valide."
	print(group)


###################################################
def test_batch():
	"""Test basique de la classe Batch (constructeur, getter, setter)"""
	app = initialize()
	group_base_test(Batch(), ["Files", "Mode"],
					FileList, -1, -1)


###################################################
def test_calibration():
	"""Test basique de la classe Calibration (constructeur, getter, setter)"""
	app = initialize()
	group_base_test(Calibration(), ["Pixel Size", "Exposure", "Intensity"],
					SpinInt, 320, 160)


###################################################
def test_localisation():
	"""Test basique de la classe Calibration (constructeur, getter, setter)"""
	app = initialize()
	group_base_test(Localisation(), ["Preview", "Threshold", "ROI Size", "Watershed", "Mode", "Gaussian Fit"],
					CheckBox, True, False)


###################################################
def test_gaussian_fit():
	"""Test basique de la classe Calibration (constructeur, getter, setter)"""
	app = initialize()
	group_base_test(GaussianFit(), ["Sigma", "Sigma Fixed", "Theta", "Theta Fixed"],
					SpinFloat, 2.0, 1.0)
