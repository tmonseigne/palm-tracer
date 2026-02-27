"""Fichier des tests pour les différents types de paramètres."""
from typing import Any, List

import pytest
from qtpy.QtWidgets import QFormLayout, QWidget

from palm_tracer._tests.Utils import INPUT_DIR
from palm_tracer.Settings.Types import *


###################################################
def setting_base_test(setting: BaseSettingType, change, default):
	"""
	Tests de base pour un paramètre

	:param setting: Paramètre à tester
	:param change: Valeur à changer
	:param default: Valeur attendue par défaut
	"""

	assert setting.value == default, "Valeur par défaut non valide."

	setting.value = change
	assert setting.value == change, "Valeur défini non valide."

	dictionary = setting.to_dict()
	setting.reset()
	assert setting.value == default, "Valeur par défaut après reset non valide."

	setting = create_setting_from_dict(dictionary)
	assert setting.value == change, "Valeur récupérée du dictionnaire non valide."

	# Hide and seek
	setting.hide()
	setting.show()

	# Hide and seek
	form = QFormLayout()
	setting.attach_to_form(form)
	setting.hide()
	setting.show()

	# Signal
	received: List[Any] = []
	setting.connect(lambda v: received.append(v))

	with setting.signal_blocked():
		setting.emit("A")
		setting.emit("B")  # Écrase A
	assert received == [] if isinstance(setting, Button) else ["B"]
	setting.disconnect()


###################################################
def test_base_setting(qtbot):
	"""Test basique de la classe abstraite"""
	setting = BaseSettingType("Test")
	with pytest.raises(NotImplementedError) as exception_info: setting.to_dict()
	assert exception_info.type == NotImplementedError, "L'erreur relevé n'est pas correcte."
	with pytest.raises(NotImplementedError) as exception_info: BaseSettingType.from_dict({})
	assert exception_info.type == NotImplementedError, "L'erreur relevé n'est pas correcte."
	layout = setting.layout
	assert layout is not None, "Le layout n'existe pas."
	label_widget = setting.label_widget
	assert label_widget is not None, "Le widget n'existe pas."
	box = setting.box
	assert isinstance(box, QWidget), "Le widget n'existe pas."


###################################################
def test_create_setting_from_dict(qtbot):
	"""Test de création de setting par dictionnaire vide excepté le type."""
	setting = create_setting_from_dict({"type": "BrowseFile"})
	assert isinstance(setting, BrowseFile), "La création par dictionnaire vide pour un BrowseFile à échoué."
	setting = create_setting_from_dict({"type": "Button"})
	assert isinstance(setting, Button), "La création par dictionnaire vide pour un Button à échoué."
	setting = create_setting_from_dict({"type": "CheckBox"})
	assert isinstance(setting, CheckBox), "La création par dictionnaire vide pour un CheckBox à échoué."
	setting = create_setting_from_dict({"type": "Combo"})
	assert isinstance(setting, Combo), "La création par dictionnaire vide pour un Combo à échoué."
	setting = create_setting_from_dict({"type": "FileList"})
	assert isinstance(setting, FileList), "La création par dictionnaire vide pour un FileList à échoué."
	setting = create_setting_from_dict({"type": "SpinFloat"})
	assert isinstance(setting, SpinFloat), "La création par dictionnaire vide pour un SpinFloat à échoué."
	setting = create_setting_from_dict({"type": "SpinInt"})
	assert isinstance(setting, SpinInt), "La création par dictionnaire vide pour un SpinInt à échoué."
	setting = create_setting_from_dict({"type": "CheckRangeFloat"})
	assert isinstance(setting, CheckRangeFloat), "La création par dictionnaire vide pour un CheckRangeFloat à échoué."
	setting = create_setting_from_dict({"type": "CheckRangeInt"})
	assert isinstance(setting, CheckRangeInt), "La création par dictionnaire vide pour un CheckRangeInt à échoué."


###################################################
def test_create_setting_from_dict_fail(qtbot):
	"""Test de création de setting par dictionnaire avec un type invalide ou absent."""
	with pytest.raises(ValueError) as exception_info: create_setting_from_dict({"type": "BadSetting"})
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."
	with pytest.raises(ValueError) as exception_info: create_setting_from_dict({})
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."


###################################################
def test_spin_int(qtbot):
	"""Test basique de la classe (constructeur, getter, setter)"""
	setting = SpinInt("Test", "With a toooltip", 1, [0, 10], 1)
	setting_base_test(setting, 5, 1)


###################################################
def test_spin_float(qtbot):
	"""Test basique de la classe (constructeur, getter, setter)"""
	setting = SpinFloat("Test", "", 1.0, [0.0, 10.0], 1.0)
	setting_base_test(setting, 5.0, 1.0)


###################################################
def test_check_box(qtbot):
	"""Test basique de la classe (constructeur, getter, setter)"""
	setting = CheckBox("Test")
	setting_base_test(setting, True, False)


###################################################
def test_combo(qtbot):
	"""Test basique de la classe (constructeur, getter, setter)"""
	setting = Combo("Test", "", 0, ["Choix 1", "Choix 2"])
	setting_base_test(setting, 1, 0)
	assert setting.current_text == "Choix 1"


###################################################
def test_browse_file(qtbot, monkeypatch, fake_qfiledialog):
	"""Test basique de la classe (constructeur, getter, setter)"""
	setting = BrowseFile(label="Test")
	setting_base_test(setting, "filename.extension", "")

	fake_qfiledialog(BrowseFile, None)  # Simuler un "Cancel" sur le QFileDialog
	setting.browse_file()
	assert setting.value == "", "Le setting devrait être vide"

	fake_qfiledialog(BrowseFile, "file.tif")  # Simuler un fichier inexistant
	setting.browse_file()
	assert setting.value == "", "Le setting devrait être vide."

	fake_qfiledialog(BrowseFile, f"{INPUT_DIR}/stack.tif")
	setting.browse_file()
	assert "stack.tif" in setting.value, "Le setting devrait être '...stack.tif'"


###################################################
def test_file_list(qtbot, monkeypatch, fake_qfiledialog):
	"""Test basique de la classe (constructeur, getter, setter)"""
	setting = FileList("Test")
	setting_base_test(setting, -1, -1)
	setting.remove_file()  # Suppression d'un fichier alors qu'il n'y en a jamais eu
	setting.update_box(["File1", "File2", "File3"])
	setting.value = 1
	assert setting.get_selected() == "File2", "Valeur sélectionnée non valide."
	setting.remove_file()
	assert setting.get_list() == ["File1", "File3"], "Liste de fichiers après suppression non valide."
	setting.clear_files()
	assert setting.get_list() == [], "Liste de fichiers après nettoyage non valide."
	assert setting.get_selected() == "", "Valeur non vide."
	setting.remove_file()  # Suppression d'un fichier alors qu'il n'y en a plus

	fake_qfiledialog(BrowseFile, None)  # Simuler un "Cancel" sur le QFileDialog
	setting.add_file()
	assert setting.get_list() == [], "Liste de fichiers non valide."

	fake_qfiledialog(BrowseFile, "file.tif")  # Simuler un fichier inexistant
	setting.add_file()
	assert setting.get_list() == [], "Liste de fichiers non valide."

	fake_qfiledialog(BrowseFile, f"{INPUT_DIR}/stack.tif")
	setting.add_file()
	assert "stack.tif" in setting.get_selected(), "Le setting devrait être '...stack.tif'"


###################################################
def test_check_range_int(qtbot):
	"""Test basique de la classe (constructeur, getter, setter)"""
	setting = CheckRangeInt("Test", "", [0, 0], [-10, 10])
	setting_base_test(setting, [5, 3], [0, 0])

	# Special tests
	setting.value = [9, 3]
	assert setting.value == [9, 9], "Valeur non valide."
	setting.box[0].setValue(10)
	assert setting.value == [10, 10], "Valeur non valide."
	setting.box[1].setValue(3)
	assert setting.value == [3, 3], "Valeur non valide."

	setting.active = True
	assert setting.active == True, "Le paramètre doit être activés."

	setting.box[1].setValue(10)
	assert setting.value == [3, 10], "Valeur non valide."
	setting.update_limits(4, 6)
	assert setting.value == [4, 6], "Valeur non valide."


###################################################
def test_check_range_float(qtbot):
	"""Test basique de la classe (constructeur, getter, setter)"""
	setting = CheckRangeFloat("Test", "", [0.0, 0.0], [-10, 10])
	setting_base_test(setting, [5.0, 3.0], [0.0, 0.0])

	# Special tests
	setting.value = [9, 3]
	assert setting.value == [9, 9], "Valeur non valide."
	setting.box[0].setValue(10)
	assert setting.value == [10, 10], "Valeur non valide."
	setting.box[1].setValue(3)
	assert setting.value == [3, 3], "Valeur non valide."

	setting.active = True
	assert setting.active == True, "Le paramètre doit être activés."

	setting.box[1].setValue(10)
	assert setting.value == [3, 10], "Valeur non valide."
	setting.update_limits(4, 6)
	assert setting.value == [4, 6], "Valeur non valide."


###################################################
def test_button(qtbot):
	"""Test basique de la classe (constructeur, getter, setter)"""
	setting = Button("Test")
	setting_base_test(setting, True, True)
