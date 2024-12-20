""" Fichier des tests pour les différents types de paramètres. """

import sys

import pytest
from qtpy.QtCore import QCoreApplication, Qt
from qtpy.QtWidgets import QApplication

from palm_tracer.Settings.SettingTypes import *


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
def setting_base_test(setting: BaseSettingType, change, default):
	"""
	Tests de base pour un paramètre

	:param setting: Paramètre à tester
	:param change: Valeur à changer
	:param default: Valeur attendue par défaut
	"""

	assert setting.get_value() == default, "Valeur par défaut non valide."

	setting.set_value(change)
	assert setting.get_value() == change, "Valeur défini non valide."

	dictionary = setting.to_dict()
	setting.reset()
	assert setting.get_value() == default, "Valeur par défaut non valide."

	setting = create_setting(dictionary)
	assert setting.get_value() == change, "Valeur récupérée du dictionnaire non valide."


###################################################
def test_base_setting():
	"""Test basique de la classe abstraite"""
	setting = BaseSettingType("Test")
	with pytest.raises(NotImplementedError) as exception_info: setting.get_value()
	assert exception_info.type == NotImplementedError, "L'erreur relevé n'est pas correcte."
	with pytest.raises(NotImplementedError) as exception_info: setting.set_value(None)
	assert exception_info.type == NotImplementedError, "L'erreur relevé n'est pas correcte."
	with pytest.raises(NotImplementedError) as exception_info: setting.to_dict()
	assert exception_info.type == NotImplementedError, "L'erreur relevé n'est pas correcte."
	with pytest.raises(NotImplementedError) as exception_info: BaseSettingType.from_dict({})
	assert exception_info.type == NotImplementedError, "L'erreur relevé n'est pas correcte."
	with pytest.raises(NotImplementedError) as exception_info: setting.reset()
	assert exception_info.type == NotImplementedError, "L'erreur relevé n'est pas correcte."
	layout = setting.layout
	assert layout is not None, "Le layout n'existe pas."


###################################################
def test_create_setting_from_dict():
	"""Test de création de setting par dictionnaire vide excepté le type."""
	app = initialize()
	setting = create_setting({"type": "IntSetting"})
	assert isinstance(setting, IntSetting), "La création par dictionnaire vide pour un IntSetting à échoué."
	setting = create_setting({"type": "FloatSetting"})
	assert isinstance(setting, FloatSetting), "La création par dictionnaire vide pour un FloatSetting à échoué."
	setting = create_setting({"type": "CheckSetting"})
	assert isinstance(setting, CheckSetting), "La création par dictionnaire vide pour un CheckSetting à échoué."
	setting = create_setting({"type": "ComboSetting"})
	assert isinstance(setting, ComboSetting), "La création par dictionnaire vide pour un ComboSetting à échoué."
	setting = create_setting({"type": "FileSetting"})
	assert isinstance(setting, FileSetting), "La création par dictionnaire vide pour un FileSetting à échoué."


###################################################
def test_create_setting_from_dict_fail():
	"""Test de création de setting par dictionnaire avec un type invalide ou absent."""
	with pytest.raises(ValueError) as exception_info: create_setting({"type": "BadSetting"})
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."
	with pytest.raises(ValueError) as exception_info: create_setting({})
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."


###################################################
def test_int_setting():
	"""Test basique de la classe (constructeur, getter, setter)"""
	app = initialize()
	setting = IntSetting("Test", 1, 0, 10, 1)
	setting_base_test(setting, 5, 1)
	assert True


###################################################
def test_float_setting():
	"""Test basique de la classe (constructeur, getter, setter)"""
	app = initialize()
	setting = FloatSetting("Test", 1.0, 0.0, 10.0, 1.0)
	setting_base_test(setting, 5.0, 1.0)
	assert True


###################################################
def test_check_setting():
	"""Test basique de la classe (constructeur, getter, setter)"""
	app = initialize()
	setting = CheckSetting("Test")
	setting_base_test(setting, True, False)
	assert True


###################################################
def test_combo_setting():
	"""Test basique de la classe (constructeur, getter, setter)"""
	app = initialize()
	setting = ComboSetting("Test", ["Choix 1", "Choix 2"])
	setting_base_test(setting, 1, 0)
	assert True


###################################################
def test_file_setting():
	"""Test basique de la classe (constructeur, getter, setter)"""
	app = initialize()
	setting = FileSetting(label="Test")
	setting_base_test(setting, "filename.extension", "")
	assert True
