""" Fichier des tests pour les différents types de paramètres. """

import pytest

from palm_tracer._tests.Utils import initialize_qt_app_for_testing
from palm_tracer.Settings.Types import *


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
	assert setting.get_value() == default, "Valeur par défaut après reset non valide."

	setting = create_setting_from_dict(dictionary)
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
	app = initialize_qt_app_for_testing()
	setting = create_setting_from_dict({"type": "SpinInt"})
	assert isinstance(setting, SpinInt), "La création par dictionnaire vide pour un SpinInt à échoué."
	setting = create_setting_from_dict({"type": "SpinFloat"})
	assert isinstance(setting, SpinFloat), "La création par dictionnaire vide pour un SpinFloat à échoué."
	setting = create_setting_from_dict({"type": "CheckBox"})
	assert isinstance(setting, CheckBox), "La création par dictionnaire vide pour un CheckBox à échoué."
	setting = create_setting_from_dict({"type": "Combo"})
	assert isinstance(setting, Combo), "La création par dictionnaire vide pour un Combo à échoué."
	setting = create_setting_from_dict({"type": "BrowseFile"})
	assert isinstance(setting, BrowseFile), "La création par dictionnaire vide pour un BrowseFile à échoué."
	setting = create_setting_from_dict({"type": "FileList"})
	assert isinstance(setting, FileList), "La création par dictionnaire vide pour un FileList à échoué."


###################################################
def test_create_setting_from_dict_fail():
	"""Test de création de setting par dictionnaire avec un type invalide ou absent."""
	with pytest.raises(ValueError) as exception_info: create_setting_from_dict({"type": "BadSetting"})
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."
	with pytest.raises(ValueError) as exception_info: create_setting_from_dict({})
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."


###################################################
def test_spin_int():
	"""Test basique de la classe (constructeur, getter, setter)"""
	app = initialize_qt_app_for_testing()
	setting = SpinInt("Test", 1, 0, 10, 1)
	setting_base_test(setting, 5, 1)
	assert True


###################################################
def test_spin_float():
	"""Test basique de la classe (constructeur, getter, setter)"""
	app = initialize_qt_app_for_testing()
	setting = SpinFloat("Test", 1.0, 0.0, 10.0, 1.0)
	setting_base_test(setting, 5.0, 1.0)
	assert True


###################################################
def test_check_box():
	"""Test basique de la classe (constructeur, getter, setter)"""
	app = initialize_qt_app_for_testing()
	setting = CheckBox("Test")
	setting_base_test(setting, True, False)
	assert True


###################################################
def test_combo():
	"""Test basique de la classe (constructeur, getter, setter)"""
	app = initialize_qt_app_for_testing()
	setting = Combo("Test", 0, ["Choix 1", "Choix 2"])
	setting_base_test(setting, 1, 0)
	assert True


###################################################
def test_browse_file():
	"""Test basique de la classe (constructeur, getter, setter)"""
	app = initialize_qt_app_for_testing()
	setting = BrowseFile(label="Test")
	setting_base_test(setting, "filename.extension", "")
	assert True


###################################################
def test_file_list():
	"""Test basique de la classe (constructeur, getter, setter)"""
	app = initialize_qt_app_for_testing()
	setting = FileList("Test")
	setting_base_test(setting, -1, -1)
	setting.items = ["File1", "File2", "File3"]
	setting.update_box()
	setting.set_value(1)
	assert setting.get_selected() == "File2", "Valeur sélectionnée non valide."
	setting.remove_file()
	assert setting.get_list() == ["File1", "File3"], "Liste de fichiers après suppression non valide."
	setting.clear_files()
	assert setting.get_list() == [], "Liste de fichiers après nettoyage non valide."
	assert setting.get_selected() == "", "Valeur non vide."


###################################################
def test_check_range_int():
	"""Test basique de la classe (constructeur, getter, setter)"""
	app = initialize_qt_app_for_testing()
	setting = CheckRangeInt("Test", [0, 0], [-10, 10])
	setting_base_test(setting, [5, 3], [0, 0])

	# Special tests
	setting.set_value([9, 3])
	assert setting.get_value() == [9, 9], "Valeur non valide."
	setting.box[0].setValue(10)
	assert setting.get_value() == [10, 10], "Valeur non valide."
	setting.box[1].setValue(3)
	assert setting.get_value() == [3, 3], "Valeur non valide."

	setting.active = True
	assert setting.active == True, "Le paramètre doit être activés."


###################################################
def test_check_range_float():
	"""Test basique de la classe (constructeur, getter, setter)"""
	app = initialize_qt_app_for_testing()
	setting = CheckRangeFloat("Test", [0.0, 0.0], [-10, 10])
	setting_base_test(setting, [5.0, 3.0], [0.0, 0.0])

	# Special tests
	setting.set_value([9, 3])
	assert setting.get_value() == [9, 9], "Valeur non valide."
	setting.box[0].setValue(10)
	assert setting.get_value() == [10, 10], "Valeur non valide."
	setting.box[1].setValue(3)
	assert setting.get_value() == [3, 3], "Valeur non valide."

	setting.active = True
	assert setting.active == True, "Le paramètre doit être activés."
