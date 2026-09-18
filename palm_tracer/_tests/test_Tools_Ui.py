"""Teste les utilitaires de construction et de synchronisation des interfaces Qt."""

from pathlib import Path

import pytest
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QButtonGroup, QDoubleSpinBox, QFormLayout, QFrame, QGridLayout, QGroupBox, QLabel, QScrollArea, QSpinBox, QVBoxLayout, QWidget

from palm_tracer.Tools import Ui


##################################################
class _DummyLayer:
	"""Simule un calque et mémorise sa visibilité lors des affectations."""

	def __init__(self, visible: bool, invalid_property: str = ""):
		"""
		Initialise le calque avec l'état demandé.

		:param visible: Visibilité initiale du calque.
		:param invalid_property: Nom de la propriété dont l'affectation doit échouer.
		"""
		object.__setattr__(self, "visible", visible)
		object.__setattr__(self, "data", "old-data")
		object.__setattr__(self, "invalid_property", invalid_property)
		object.__setattr__(self, "updates_visibility", [])

	def __setattr__(self, name, value):
		"""Mémorise la visibilité courante ou refuse la propriété utilisée pour simuler une erreur."""
		if name == self.invalid_property: raise ValueError("Invalid property")
		if name != "visible": self.updates_visibility.append(self.visible)
		object.__setattr__(self, name, value)


# ==================================================
# region Construction de l'interface
# ==================================================
##################################################
def test_add_setting_row(qtbot):
	"""Vérifie l'ajout d'un paramètre dans un formulaire."""
	parent = QWidget()
	qtbot.addWidget(parent)
	form = Ui.make_form(parent)
	assert isinstance(form, QFormLayout)
	value = QWidget()
	Ui.add_setting_row(form, "my setting", value)
	assert form.rowCount() == 1
	assert form.itemAt(0, QFormLayout.ItemRole.FieldRole).layout().itemAt(0).widget() is value


##################################################
def test_init_layout(qtbot):
	"""Vérifie les espacements et marges demandés pour un calque."""
	parent = QWidget()
	qtbot.addWidget(parent)
	layout = QVBoxLayout(parent)
	Ui.init_layout(layout, space=3, margin=5)
	assert layout.spacing() == 3
	margins = layout.contentsMargins()
	assert (margins.left(), margins.top(), margins.right(), margins.bottom()) == (5, 5, 5, 5)


##################################################
@pytest.mark.parametrize("builder, widget_type", [pytest.param(Ui.make_tab, QWidget, id="tab"), pytest.param(Ui.make_group, QGroupBox, id="group")])
def test_make_container(qtbot, builder, widget_type):
	"""Vérifie la construction d'un conteneur et de son calque vertical."""
	widget, layout = builder()
	qtbot.addWidget(widget)
	assert isinstance(widget, widget_type)
	assert isinstance(layout, QVBoxLayout)
	assert widget.layout() is layout


##################################################
@pytest.mark.parametrize("with_units", [pytest.param(False, id="no-units"), pytest.param(True, id="with-units-and-tooltips")])
def test_make_info_grid(qtbot, with_units):
	"""Vérifie la construction de la grille avec ou sans unités et infobulles."""
	parent = QWidget()
	qtbot.addWidget(parent)
	elements = {"1": {"label": QLabel("1"), "value": QLabel("-")},
				"2": {"label": QLabel("2"), "value": QLabel("-")}}
	if with_units:
		elements["1"].update(unit=QLabel("unit"), tips="tooltips")
		elements["2"].update(unit=QLabel("unit"), tips="")
	grid = Ui.make_info_grid(elements, "title", 3 if with_units else 2, parent)
	assert isinstance(grid, QGridLayout)


##################################################
def test_make_file_info_group(qtbot):
	"""Vérifie la construction du groupe d'informations d'un fichier."""
	group, status = Ui.make_file_info_group()
	qtbot.addWidget(group)
	assert isinstance(group, QGroupBox)
	assert status


##################################################
def test_make_path_label(qtbot):
	"""Vérifie le texte initial du label de chemin."""
	label = Ui.make_path_label("my path")
	qtbot.addWidget(label)
	assert isinstance(label, QLabel)
	assert label.text() == "my path"


##################################################
@pytest.mark.parametrize("path", [pytest.param("my/path/file.txt", id="string"), pytest.param(Path("my/path/file.txt"), id="path-object")])
def test_update_path_label(qtbot, path):
	"""Vérifie le nom affiché et le chemin complet dans l'infobulle."""
	label = Ui.make_path_label()
	qtbot.addWidget(label)
	Ui.update_path_label(label, path)
	assert label.text() == "file.txt"
	assert label.toolTip() == str(Path(path))


##################################################
def test_make_vertical_scroll(qtbot):
	"""Vérifie que la zone de défilement contient le widget demandé."""
	content = QWidget()
	scroll = Ui.make_vertical_scroll(content)
	qtbot.addWidget(scroll)
	assert isinstance(scroll, QScrollArea)
	assert scroll.widget() is content
	assert scroll.widgetResizable()


##################################################
@pytest.mark.parametrize("builder, shape, color", [
		pytest.param(Ui.make_vertical_separator, QFrame.Shape.VLine, "#000000", id="vertical"),
		pytest.param(Ui.make_horizontal_separator, QFrame.Shape.HLine, "#B0B0B0", id="horizontal")])
def test_make_separator(qtbot, builder, shape, color):
	"""Vérifie l'orientation et la couleur du séparateur."""
	separator = builder(color)
	qtbot.addWidget(separator)
	assert separator.frameShape() == shape
	assert color in separator.styleSheet()


##################################################
@pytest.mark.parametrize("decimals, buttons, spin_type", [
		pytest.param(0, True, QSpinBox, id="integer-with-buttons"),
		pytest.param(2, False, QDoubleSpinBox, id="decimal-without-buttons")])
def test_make_spin(qtbot, decimals, buttons, spin_type):
	"""Vérifie le type et les paramètres du champ numérique."""
	spin = Ui.make_spin(None, -100, 100, 10, 0, decimals, buttons)
	qtbot.addWidget(spin)
	assert isinstance(spin, spin_type)
	assert (spin.minimum(), spin.maximum(), spin.singleStep(), spin.value()) == (-100, 100, 10, 0)
	assert (spin.buttonSymbols() != QSpinBox.ButtonSymbols.NoButtons) == buttons
	if decimals: assert spin.decimals() == decimals
	Ui.set_spin_width(spin)
	assert spin.minimumWidth() == spin.maximumWidth() > 0


# ==================================================
# endregion Construction de l'interface
# ==================================================

# ==================================================
# region Fonctions de rappel
# ==================================================
##################################################
@pytest.mark.parametrize("initial_visibility, visible, expected_visibility", [
		pytest.param(False, None, False, id="preserve-hidden"),
		pytest.param(True, None, True, id="preserve-visible"),
		pytest.param(False, True, True, id="force-visible"),
		pytest.param(True, False, False, id="force-hidden")])
def test_update_layer(initial_visibility, visible, expected_visibility):
	"""Vérifie la mise à jour du calque et les différentes politiques de visibilité."""
	layer = _DummyLayer(initial_visibility)
	Ui.update_layer(layer, "new-data", visible, face_color="lime", blending="translucent")

	assert layer.data == "new-data"
	assert layer.face_color == "lime"
	assert layer.blending == "translucent"
	assert layer.updates_visibility == [True, True, True]
	assert layer.visible is expected_visibility


##################################################
def test_update_layer_restores_visibility_on_error():
	"""Vérifie la restauration de la visibilité lorsqu'une propriété ne peut pas être affectée."""
	layer = _DummyLayer(False, "invalid")
	with pytest.raises(ValueError, match="Invalid property"): Ui.update_layer(layer, "new-data", invalid=True)
	assert layer.visible is False


##################################################
def test_sync_button_group(qtbot):
	"""Vérifie les fonctions de synchronisation."""

	layout_1, grp_1, _ = Ui.make_exclusive_btn_group(["1", "2", "3"])
	assert isinstance(grp_1, QButtonGroup)
	layout_2, grp_2, _ = Ui.make_exclusive_btn_group(["1", "2", "3"])
	assert isinstance(grp_2, QButtonGroup)

	parents = []  # Conserve les deux conteneurs pendant les clics et assertions.
	for layout in (layout_1, layout_2):
		parent = QWidget()
		parents.append(parent)
		parent.setLayout(layout)
		qtbot.addWidget(parent)

	# Synchronisation
	grp_1.idClicked.connect(lambda v: Ui.sync_button_group(grp_2, v))
	grp_2.idClicked.connect(lambda v: Ui.sync_button_group(grp_1, v))

	qtbot.mouseClick(grp_1.button(2), Qt.MouseButton.LeftButton)
	assert grp_2.checkedId() == 2

	qtbot.mouseClick(grp_2.button(0), Qt.MouseButton.LeftButton)
	assert grp_1.checkedId() == 0


##################################################
def test_sync_spin(qtbot):
	"""Vérifie les fonctions de synchronisation."""
	main_widget = QWidget()
	qtbot.addWidget(main_widget)

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
@pytest.mark.parametrize("minimum, maximum, expected", [
		pytest.param(None, None, (-100, 100), id="no-change"),
		pytest.param(0, None, (0, 100), id="minimum-only"),
		pytest.param(None, 10, (-100, 10), id="maximum-only"),
		pytest.param(1, 9, (1, 9), id="both-bounds")])
def test_update_spin_limits(qtbot, minimum, maximum, expected):
	"""Vérifie chaque combinaison de mise à jour des bornes indépendamment."""
	spin = Ui.make_spin(None, -100, 100)
	qtbot.addWidget(spin)
	Ui.update_spin_limits(spin, minimum, maximum)
	assert (spin.minimum(), spin.maximum()) == expected


# ==================================================
# endregion Fonctions de rappel
# ==================================================

# ==================================================
# region Affichages
# ==================================================
##################################################
@pytest.mark.parametrize("printer, message", [
		pytest.param(Ui.print_error, "Message d'erreur", id="error"),
		pytest.param(Ui.print_warning, "Message d'avertissement", id="warning"),
		pytest.param(Ui.print_success, "Message de succès", id="success")])
def test_print_message(capsys, printer, message):
	"""Vérifie que chaque fonction affiche le message demandé."""
	printer(message)
	captured = capsys.readouterr()
	assert message in captured.out
	assert captured.out.endswith("\n")
	assert captured.err == ""


##################################################
@pytest.mark.parametrize("seconds, expected", [
		pytest.param(0, "00:00:00", id="zero-duration"),
		pytest.param(59, "00:00:59", id="seconds"),
		pytest.param(60, "00:01:00", id="minute-boundary"),
		pytest.param(3666, "01:01:06", id="hours-minutes-seconds")])
def test_format_time(seconds, expected):
	"""Vérifie le format heures, minutes et secondes de la durée."""
	assert Ui.format_time(seconds) == expected

# ==================================================
# endregion Affichages
# ==================================================
