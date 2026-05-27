"""Fichier des tests pour les fonctions en lien avec l'affichage."""
from pathlib import Path

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QButtonGroup, QDoubleSpinBox, QFormLayout, QFrame, QGridLayout, QGroupBox, QLabel, QScrollArea, QSpinBox, QVBoxLayout, QWidget

from palm_tracer.Tools import Ui


##################################################
def test_builders(qtbot):
	"""Test des fonctions de build."""
	main_widget = QWidget()
	tab, layout = Ui.make_tab(main_widget)  # Création d'un onglet
	assert isinstance(tab, QWidget)
	assert isinstance(layout, QVBoxLayout)

	Ui.init_layout(layout)  # Initialisation d'un calque

	group, layout = Ui.make_group(main_widget)  # Création d'un groupe
	assert isinstance(group, QGroupBox)
	assert isinstance(layout, QVBoxLayout)

	form = Ui.make_form(main_widget)  # Création d'un formulaire
	assert isinstance(form, QFormLayout)

	Ui.add_setting_row(form, "my setting", QWidget())  # Ajout d'un paramètre au formulaire
	assert form.rowCount() == 1  # Il a maintenant 1 ligne

	label = Ui.make_path_label("my path", main_widget)  # Création d'un Qlabel d'information
	assert isinstance(label, QLabel)

	Ui.update_path_label(label, "my/path/file.txt")
	Ui.update_path_label(label, Path("my/path/file.txt"))

	separator = Ui.make_horizontal_separator()  # Création d'un séparateur horizontal
	assert isinstance(separator, QFrame)
	separator = Ui.make_vertical_separator("#000000")  # Création d'un séparateur vertival (noir)
	assert isinstance(separator, QFrame)

	scroll = Ui.make_vertical_scroll(QWidget())  # Création d'une zone scrollable vertivale
	assert isinstance(scroll, QScrollArea)

	elements = {"1": {"label": QLabel("1"), "value": QLabel("-")}, "2": {"label": QLabel("2"), "value": QLabel("-")}}

	grid = Ui.make_info_grid(elements, "title")  # Création d'un groupe
	assert isinstance(grid, QGridLayout)

	elements = {"1": {"label": QLabel("1"), "value": QLabel("-"), "unit": QLabel("unit"), "tips": "tooltips"},
				"2": {"label": QLabel("2"), "value": QLabel("-"), "unit": QLabel("unit"), "tips": ""}}
	grid = Ui.make_info_grid(elements, "title", 3)  # Création d'un groupe
	assert isinstance(grid, QGridLayout)

	grp, status = Ui.make_file_info_group()
	assert isinstance(grp, QGroupBox)


##################################################
def test_builders_spin(qtbot):
	"""Test des fonctions de build."""
	main_widget = QWidget()

	spin_1 = Ui.make_spin(main_widget, -100, 100, 10, 0, 0, True)
	assert isinstance(spin_1, QSpinBox)
	spin_2 = Ui.make_spin(main_widget, -100, 100, 10, 0, 2, False)
	assert isinstance(spin_2, QDoubleSpinBox)
	Ui.set_spin_width(spin_1)
	Ui.set_spin_width(spin_2)

	Ui.update_spin_limits(spin_1)  # Aucune mise à jour
	Ui.update_spin_limits(spin_1, 0, None)  # Mise à jour du min
	Ui.update_spin_limits(spin_1, None, 10)  # Mise à jour du max
	Ui.update_spin_limits(spin_1, 1, 9)  # Mise à jour des deux

	spin_2 = Ui.make_spin(main_widget, -100, 100, 10, 0, 0, True)
	assert isinstance(spin_2, QSpinBox)


##################################################
def test_sync_spin(qtbot):
	"""Test des fonctions de synchronisation."""
	main_widget = QWidget()

	spin_1 = Ui.make_spin(main_widget, -100, 100, 10, 0, 0, True)
	assert isinstance(spin_1, QSpinBox)
	spin_2 = Ui.make_spin(main_widget, -100, 100, 10, 0, 0, True)
	assert isinstance(spin_2, QSpinBox)

	# Synchronisation
	spin_1.valueChanged.connect(lambda v: Ui.sync_spin(spin_2, v))
	spin_2.valueChanged.connect(lambda v: Ui.sync_spin(spin_1, v))

	spin_1.setValue(4)  # Mise à jour du premier
	assert spin_2.value() == 4  # Vérificaiton sur le second

	spin_2.setValue(5)  # Mise à jour du second
	assert spin_1.value() == 5  # Vérificaiton sur le premier


##################################################
def test_sync_button_group(qtbot):
	"""Test des fonctions de synchronisation."""
	_ = QWidget()

	_, grp_1, _ = Ui.make_exclusive_btn_group(["1", "2", "3"])
	assert isinstance(grp_1, QButtonGroup)
	_, grp_2, _ = Ui.make_exclusive_btn_group(["1", "2", "3"])
	assert isinstance(grp_2, QButtonGroup)

	# Synchronisation
	grp_1.idClicked.connect(lambda v: Ui.sync_button_group(grp_2, v))
	grp_2.idClicked.connect(lambda v: Ui.sync_button_group(grp_1, v))

	qtbot.mouseClick(grp_1.button(2), Qt.MouseButton.LeftButton)
	assert grp_2.checkedId() == 2

	qtbot.mouseClick(grp_2.button(0), Qt.MouseButton.LeftButton)
	assert grp_1.checkedId() == 0


##################################################
def test_print_error():
	"""Test de la fonction print error."""
	Ui.print_error("Message d'erreur"), "L'affichage n'a pas pu être effectué"


##################################################
def test_print_warning():
	"""Test de la fonction print warning."""
	Ui.print_warning("Message d'avertissement"), "L'affichage n'a pas pu être effectué"


##################################################
def test_print_success():
	"""Test de la fonction print warning."""
	Ui.print_success("Message de succes"), "L'affichage n'a pas pu être effectué"


##################################################
def test_format_time():
	"""Test de la fonction print warning."""
	assert Ui.format_time(3666) == "01:01:06", "L'affichage n'a pas pu être effectué"
