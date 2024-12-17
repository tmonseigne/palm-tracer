""" Fichier des tests pour les différents types de paramètres. """

import sys

import pytest
from qtpy.QtCore import QCoreApplication, Qt
from qtpy.QtWidgets import QApplication

from palm_tracer.Settings import SettingTypes


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
def setting_base_test(setting: SettingTypes.BaseSettingType, change, default_expected):
	"""
	Tests de base pour un paramètre

	:param setting: Paramètre à tester
	:param change: Valeur à changer
	:param default_expected: Valeur attendue par défaut
	"""

	assert setting.get_value() == default_expected, "Valeur par défaut non valide."
	setting.set_value(change)
	assert setting.get_value() == change, "Valeur défini non valide."
	setting.reset()
	assert setting.get_value() == default_expected, "Valeur par défaut non valide."


###################################################
def test_base_setting():
	""" Test basique de la classe abstraite """
	setting = SettingTypes.BaseSettingType("Test")
	with pytest.raises(NotImplementedError) as exception_info: setting.get_value()
	assert exception_info.type == NotImplementedError, "L'erreur relevé n'est pas correcte."
	with pytest.raises(NotImplementedError) as exception_info: setting.set_value(None)
	assert exception_info.type == NotImplementedError, "L'erreur relevé n'est pas correcte."
	with pytest.raises(NotImplementedError) as exception_info: setting.reset()
	assert exception_info.type == NotImplementedError, "L'erreur relevé n'est pas correcte."
	layout = setting.layout
	assert layout is not None, "Le layout n'existe pas."


###################################################
def test_int_setting():
	""" Test basique de la classe (constructeur, getter, setter) """
	app = initialize()
	setting = SettingTypes.IntSetting("Test", 0, 10, 1, 1)
	setting_base_test(setting, 5, 1)
	assert True


###################################################
def test_float_setting():
	""" Test basique de la classe (constructeur, getter, setter) """
	app = initialize()
	setting = SettingTypes.FloatSetting("Test", 0.0, 10.0, 1.0, 1.0)
	setting_base_test(setting, 5.0, 1.0)
	assert True


###################################################
def test_check_setting():
	""" Test basique de la classe (constructeur, getter, setter) """
	app = initialize()
	setting = SettingTypes.CheckSetting(label="Test")
	setting_base_test(setting, True, False)
	assert True


###################################################
def test_combo_setting():
	""" Test basique de la classe (constructeur, getter, setter) """
	app = initialize()
	setting = SettingTypes.ComboSetting(label="Test", choices=["Choix 1", "Choix 2"])
	setting_base_test(setting, 1, 0)
	assert True


###################################################
def test_file_setting():
	""" Test basique de la classe (constructeur, getter, setter) """
	app = initialize()
	setting = SettingTypes.FileSetting(label="Test")
	setting_base_test(setting, "filename.extension", "")
	assert True
