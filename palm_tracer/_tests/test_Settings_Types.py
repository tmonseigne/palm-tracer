"""Teste les différents types de paramètres et leurs interfaces Qt."""

import copy
from typing import Any, cast, List

import pytest
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QCheckBox, QDoubleSpinBox, QFormLayout, QHBoxLayout, QLabel, QSpinBox, QWidget

from palm_tracer._tests.Utils import INPUT_DIR
from palm_tracer.Settings.Types import *


###################################################
def setting_base_test(setting: BaseSettingType, change, default):
	"""
	Tests de base pour un paramètre.

	:param setting: Paramètre à tester.
	:param change: Valeur à changer.
	:param default: Valeur attendue par défaut.
	"""

	# Changement de valeurs
	assert setting.value == default, "Valeur par défaut non valide."
	setting.value = change
	assert setting.value == change, "Valeur défini non valide."

	# Utilisation du dictionnaire
	min_dictionary = copy.deepcopy(setting.to_compact_dict())  # Deep Copy car les listes peuvent devenir des références
	setting.reset()
	assert setting.value == default, "Valeur par défaut après reset non valide."
	setting.update_from_compact_dict(min_dictionary)
	assert setting.value == change, "Valeur récupérée du dictionnaire non valide."

	# Hide and seek
	setting.hide()
	setting.show()

	# Interface
	_ = setting.get_ui("default")
	form = QFormLayout()
	setting.attach_to_form("default", form)  # Second appel a get_ui à l'intérieur

	setting.value = default
	setting.value = default  # Second appel vers une valeur identique

	# Signaux
	received: List[Any] = []
	setting.connect(lambda v: received.append(v))

	with setting.signal_blocked():
		setting.emit("A")
		setting.emit("B")  # Écrase A
	assert received == ["B"]

	with setting.signal_blocked(emit_last=False): setting.emit("C")  # Ne va pas le renvoyer
	assert received == ["B"]

	setting.disconnect()
	setting.clean_ui("default")
	_ = setting.get_ui("default")


###################################################
def test_base_setting():
	"""Vérifie la classe abstraite."""
	setting = BaseSettingType("Test")
	with pytest.raises(NotImplementedError) as exception_info: setting.get_ui()
	assert exception_info.type == NotImplementedError, "L'erreur relevé n'est pas correcte."


###################################################
def test_base_ui(qtbot):
	"""Vérifie l'interface de base avec libellé."""
	ui = BaseUIType(layout=QHBoxLayout(), label=QLabel("Test"), boxes=[QCheckBox()])
	ui.set_tooltip("")

	ui.hide()
	ui.show()

	form = QFormLayout()
	ui.attach_to_form(form)

	ui.hide()
	ui.show()


###################################################
def test_base_ui_no_label(qtbot):
	"""Vérifie l'interface de base sans libellé."""
	ui = BaseUIType(layout=QHBoxLayout(), boxes=[QCheckBox()])
	ui.set_tooltip("")

	ui.hide()
	ui.show()

	form = QFormLayout()
	ui.attach_to_form(form)

	ui.hide()
	ui.show()


###################################################
def test_spin_int(qtbot):
	"""Vérifie la classe (constructeur, getter, setter)."""
	setting = SpinInt("Test", "With a toooltip", 1, [0, 10], 1)
	setting_base_test(setting, 5, 1)


###################################################
def test_spin_float(qtbot):
	"""Vérifie la classe (constructeur, getter, setter)."""
	setting = SpinFloat("Test", "", 1.0, [0.0, 10.0], 1.0)
	setting_base_test(setting, 5.0, 1.0)


###################################################
def test_check_box(qtbot):
	"""Vérifie la classe (constructeur, getter, setter)."""
	setting = CheckBox("Test")
	setting_base_test(setting, True, False)
	ui = setting.get_ui("new")

	w = QWidget()
	form = QFormLayout(w)  # crée et assigne le layout au widget
	ui.attach_to_form(form)
	w.show()
	qtbot.waitExposed(w)

	qtbot.mouseClick(ui.boxes[0], Qt.MouseButton.LeftButton)
	assert setting.value

	w.close()


###################################################
def test_combo(qtbot):
	"""Vérifie la classe (constructeur, getter, setter)."""
	setting = Combo("Test", "", 0, ["Choix 1", "Choix 2"])
	setting_base_test(setting, 1, 0)
	# Get Actual Text
	assert setting.current_text == "Choix 1"
	# Change items after UI Creation
	setting.items = ["1", "2"]
	assert setting.items == ["1", "2"]


###################################################
def test_browse_file(qtbot, monkeypatch, fake_qfiledialog):
	"""Vérifie la classe (constructeur, getter, setter)."""
	setting = BrowseFile(label="Test")
	setting_base_test(setting, "filename.extension", "")

	fake_qfiledialog(BrowseFile, None)  # Simuler un "Cancel" sur le QFileDialog
	setting.browse_file()
	assert setting.value == "", "le paramètre devrait être vide"

	fake_qfiledialog(BrowseFile, "file.tif")  # Simuler un fichier inexistant
	setting.browse_file()
	assert setting.value == "", "le paramètre devrait être vide."

	fake_qfiledialog(BrowseFile, f"{INPUT_DIR}/stack.tif")
	setting.browse_file()
	assert "stack.tif" in setting.value, "le paramètre devrait être '...stack.tif'"


###################################################
def test_file_list(qtbot, monkeypatch, fake_qfiledialog):
	"""Vérifie la classe (constructeur, getter, setter)."""
	setting = FileList("Test")
	setting_base_test(setting, -1, -1)
	setting.remove_file()  # Suppression d'un fichier alors qu'il n'y en a jamais eu
	setting.items = ["File1", "File2", "File3"]
	setting.value = 1
	assert setting.current_text == "File2", "Valeur sélectionnée non valide."
	setting.remove_file()
	assert setting.items == ["File1", "File3"], "Liste de fichiers après suppression non valide."
	setting.clear_files()
	assert setting.items == [], "Liste de fichiers après nettoyage non valide."
	assert setting.current_text == "", "Valeur non vide."
	setting.remove_file()  # Suppression d'un fichier alors qu'il n'y en a plus

	fake_qfiledialog(BrowseFile, None)  # Simuler un "Cancel" sur le QFileDialog
	setting.add_file()
	assert setting.items == [], "Liste de fichiers non valide."

	fake_qfiledialog(BrowseFile, "file.tif")  # Simuler un fichier inexistant
	setting.add_file()
	assert setting.items == [], "Liste de fichiers non valide."

	fake_qfiledialog(BrowseFile, f"{INPUT_DIR}/stack.tif")
	setting.add_file()
	assert "stack.tif" in setting.current_text, "Le paramètre devrait être '...stack.tif'"


###################################################
def test_check_int(qtbot):
	"""Vérifie la classe (constructeur, getter, setter)."""
	setting = CheckInt("Test", "", 1, [1, 10])
	setting_base_test(setting, 2, 1)
	ui = setting.get_ui("new")

	setting.active = True
	assert setting.active, "Le paramètre doit être activés."

	setting.limits = [4, 6]
	assert setting.value == 4, "Valeur non valide."

	w = QWidget()
	form = QFormLayout(w)  # crée et assigne le layout au widget
	ui.attach_to_form(form)
	w.show()
	qtbot.waitExposed(w)

	cast(QSpinBox, ui.boxes[1]).setValue(5)
	assert setting.value == 5
	qtbot.mouseClick(ui.boxes[0], Qt.MouseButton.LeftButton)
	assert not setting.active

	w.close()


###################################################
def test_check_range_int(qtbot):
	"""Vérifie la classe (constructeur, getter, setter)."""
	setting = CheckRangeInt("Test", "", [0, 0], [-10, 10])
	setting_base_test(setting, [3, 5], [0, 0])
	ui = setting.get_ui("new")

	# Special tests
	setting.value = [9, 4]
	assert setting.value == [4, 4], "Valeur non valide."
	setting.min = 10
	assert setting.value == [10, 10], "Valeur non valide."
	setting.max = 3
	assert setting.value == [3, 3], "Valeur non valide."

	setting.active = True
	assert setting.active, "Le paramètre doit être activés."

	setting.max = 10
	assert setting.value == [3, 10], "Valeur non valide."
	setting.limits = [4, 6]
	assert setting.value == [4, 6], "Valeur non valide."

	w = QWidget()
	form = QFormLayout(w)  # crée et assigne le layout au widget
	ui.attach_to_form(form)
	w.show()
	qtbot.waitExposed(w)

	cast(QSpinBox, ui.boxes[1]).setValue(5)
	assert setting.min == 5
	cast(QSpinBox, ui.boxes[2]).setValue(5)
	assert setting.max == 5
	qtbot.mouseClick(ui.boxes[0], Qt.MouseButton.LeftButton)
	assert not setting.active

	w.close()


###################################################
def test_check_range_float(qtbot):
	"""Vérifie la classe (constructeur, getter, setter)."""
	setting = CheckRangeFloat("Test", "", [0.0, 0.0], [-10, 10])
	setting_base_test(setting, [3.0, 5.0], [0.0, 0.0])
	ui = setting.get_ui("new")

	# Special tests
	setting.value = [9, 4]
	assert setting.value == [4, 4], "Valeur non valide."
	setting.min = 10
	assert setting.value == [10, 10], "Valeur non valide."
	setting.max = 3
	assert setting.value == [3, 3], "Valeur non valide."

	setting.active = True
	assert setting.active, "Le paramètre doit être activés."

	setting.max = 10
	assert setting.value == [3, 10], "Valeur non valide."
	setting.limits = [4, 6]
	assert setting.value == [4, 6], "Valeur non valide."

	w = QWidget()
	form = QFormLayout(w)  # crée et assigne le layout au widget
	ui.attach_to_form(form)
	w.show()
	qtbot.waitExposed(w)

	cast(QDoubleSpinBox, ui.boxes[1]).setValue(5)
	assert setting.min == 5
	cast(QDoubleSpinBox, ui.boxes[2]).setValue(5)
	assert setting.max == 5
	qtbot.mouseClick(ui.boxes[0], Qt.MouseButton.LeftButton)
	assert not setting.active

	w.close()


###################################################
def test_check_int_selection(qtbot):
	"""Vérifie la classe (constructeur, getter, setter)."""
	setting = CheckIntSelection("Test", "")
	setting_base_test(setting, "1;3-4", "")
	ui = setting.get_ui("new")

	setting.active = True
	assert setting.active, "Le paramètre doit être activés."

	assert setting.value == "", "Valeur non valide."
	assert setting.ranges == [], "Valeur non valide."
	assert not setting.contains(7), "Valeur non valide."
	# Gestion des cas problématiques (plusieurs fois ; ou -, caractère non valide et min/max inversé et fusion d'intevalles
	setting.value = "4-6;10-8;7--7;;9;8:6;2"
	assert setting.value == "2;4-10", "Valeur non valide."
	assert setting.ranges == [(2, 2), (4, 10)], "Valeur non valide."
	assert setting.contains(7), "Valeur non valide."

	w = QWidget()
	form = QFormLayout(w)  # crée et assigne le layout au widget
	ui.attach_to_form(form)
	w.show()
	qtbot.waitExposed(w)

	qtbot.mouseClick(ui.boxes[0], Qt.MouseButton.LeftButton)
	assert not setting.active
	w.close()


###################################################
def test_button(qtbot, capsys):
	"""Vérifie la classe (constructeur, getter, setter)."""
	setting = Button("Test")
	setting_base_test(setting, True, True)
	setting.connect_button(lambda: print("Hi"), "default", 0)  # Ui sur laquelle on ne va pas cliquer
	setting.connect_button(lambda: print("Hello"), "new", 0)  # Ui sur laquelle on va cliquer
	ui = setting.get_ui("new")

	w = QWidget()
	form = QFormLayout(w)  # crée et assigne le layout au widget
	ui.attach_to_form(form)
	w.show()
	qtbot.waitExposed(w)

	qtbot.mouseClick(ui.boxes[0], Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "Hello" in out
	assert "Hi" not in out

	w.close()


###################################################
def test_button_group(qtbot):
	"""Vérifie la classe (constructeur, getter, setter)."""
	setting = ButtonGroup("Test", "", 0, ["Choix 1", "Choix 2"])
	setting_base_test(setting, 1, 0)
	assert setting.current_text == "Choix 1"
	ui = setting.get_ui("default")
	setting.active_item(0, False)
	assert not ui.boxes[0].isEnabled()
	setting.active_item(0, True)
	assert ui.boxes[0].isEnabled()


###################################################
def test_sync(qtbot):
	"""Vérifie la classe abstraite."""
	spin_1 = SpinInt("Test", "With a toooltip", 1, [0, 10], 1)
	spin_2 = SpinInt("Test", "With a toooltip", 1, [0, 10], 1)
	spin_1.sync(spin_2)
	spin_1.value = 5
	assert spin_2.value == 5, "Valeur non valide."

	spin_2.value = 3
	assert spin_1.value == 3, "Valeur non valide."
