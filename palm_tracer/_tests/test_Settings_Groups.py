"""Teste les groupes de paramètres."""

import copy
from typing import List, Type

import pytest
from qtpy.QtWidgets import QFormLayout, QWidget

from palm_tracer._tests.Utils import *
from palm_tracer.Settings.Groups import *
from palm_tracer.Settings.Types import BaseSettingType, ButtonGroup, CheckBox, CheckIntSelection, CheckRangeInt, Combo, SpinFloat, SpinInt


###################################################
def group_base_test(group: BaseSettingGroup, names: list[str],
					first_type: Type[BaseSettingType], change: Any, default: Any):
	"""
	Tests de base pour un groupe de paramètres.

	:param group: Groupe de paramètres.
	:param names: Nom des paramètres du groupe.
	:param first_type: Type du premier paramètre.
	:param change: Changement du premier paramètre.
	:param default: Valeur par défaut du premier paramètre.
	"""
	# Nom des éléments
	assert names[0] in group, "La clé n'existe pas"
	assert group.settings_names == names, "Les paramètres ne correspondent pas"
	setting = group[names[0]]
	assert isinstance(setting, first_type), "Le paramètre ne correspond pas"
	for key in group: assert key != "", "Une clé est vide"

	# Utilisation du dictionnaire
	group[names[0]].value = change
	assert group[names[0]].value == change, "Valeur défini non valide."
	min_dictionary = copy.deepcopy(group.to_compact_dict())
	group.reset()
	assert group[names[0]].value == default, "Valeur par défaut non valide."
	group.update_from_compact_dict(min_dictionary)
	assert group[names[0]].value == change, "Valeur récupérée du dictionnaire non valide."

	# Interface
	_ = group.get_ui()
	ui = group.get_ui()  # Second appel l'ui existe déjà

	w = QWidget()
	form = QFormLayout(w)  # Crée et affecte la mise en page au widget
	ui.attach_to_form(form)

	# Hide and seek
	group.hide()
	group.show()

	# Activation
	group.active = False
	assert not group.active, "Les paramètres doivent être désactivés."
	group.active = True
	assert group.active, "Les paramètres doivent être activés."
	group.set_active(1)  # Second appel qui ne fait rien

	# Print
	print(group)
	print(group.settings)

	# Signaux
	received: List[Any] = []
	group.connect(lambda v: received.append(v))
	with group.signal_blocked(): pass
	group.disconnect()
	group.clean_ui()


###################################################
def test_base_group(qtbot):
	"""Vérifie la classe abstraite."""
	group = BaseSettingGroup()
	group.value = None
	assert group.value is None, "Get Value ne doit rien retourné pour la classe mère."

	received: List[Any] = []
	group.connect(lambda v: received.append(v))
	with group.signal_blocked(): pass
	group.disconnect()


###################################################
def test_batch(qtbot):
	"""Vérifie la classe Batch (constructeur, getter, setter)."""
	batch = Batch()
	group_base_test(batch, ["Files", "Mode"], FileList, -1, -1)


###################################################
def test_batch_get_path(qtbot):
	"""Vérifie le get_paths de la classe Batch."""
	batch = Batch()

	path = batch.get_paths()
	assert len(path) == 1, "Il ne devrait y avoir qu'un seul dossier."
	assert path[0].endswith("_PALM_Tracer"), "Le nom du dossier ne correspond pas."

	file_list = cast(FileList, batch["Files"])
	file_list.items = ["output/File 1.tif", "output/File 2.tif"]

	path = batch.get_paths()
	assert len(path) == 1, "Il ne devrait y avoir qu'un seul dossier."
	assert path[0] == str(Path("output/File 1_PALM_Tracer")), "Le nom du dossier ne correspond pas."

	file_list.value = 1
	path = batch.get_paths()
	assert len(path) == 1, "Il ne devrait y avoir qu'un seul dossier."
	assert path[0] == str(Path("output/File 2_PALM_Tracer")), "Le nom du dossier ne correspond pas."

	batch["Mode"].value = 1
	path = batch.get_paths()
	assert len(path) == 2, "Il devrait y avoir deux dossiers."
	assert path[0] == str(Path("output/File 1_PALM_Tracer")), "Le nom du dossier ne correspond pas."
	assert path[1] == str(Path("output/File 2_PALM_Tracer")), "Le nom du dossier ne correspond pas."

	batch["Mode"].value = 2
	path = batch.get_paths()
	assert len(path) == 1, "Il ne devrait y avoir qu'un seul dossier."
	assert path[0] == str(Path("output/File 1_PALM_Tracer")), "Le nom du dossier ne correspond pas."


###################################################
def test_batch_get_stacks(qtbot):
	"""Vérifie le get_stacks de la classe Batch."""
	batch = Batch()
	stacks = batch.get_stacks()
	assert len(stacks) == 0, "Nombre de pile invalide"

	file_list = cast(FileList, batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif", f"{INPUT_DIR}/stack.tif", f"{INPUT_DIR}/stack.tif"]

	batch["Mode"].value = 0
	stacks = batch.get_stacks()
	assert len(stacks) == 1, "Nombre de pile invalide"
	assert stacks[0].shape == (10, 128, 256), "Taille de la pile non valide"

	batch["Mode"].value = 1
	stacks = batch.get_stacks()
	assert len(stacks) == 3, "Nombre de pile invalide"
	assert stacks[0].shape == (10, 128, 256), "Taille de la pile non valide"

	batch["Mode"].value = 2
	stacks = batch.get_stacks()
	assert len(stacks) == 1, "Nombre de pile invalide"
	assert stacks[0].shape == (30, 128, 256), "Taille de la pile non valide"

	file_list.items = [f"{INPUT_DIR}/stack.tif", f"{INPUT_DIR}/stack_quadrant.tif", f"{INPUT_DIR}/stack.tif"]
	batch["Mode"].value = 2
	stacks = batch.get_stacks()
	assert len(stacks) == 3, "Nombre de pile invalide"
	assert stacks[0].shape == (10, 128, 256), "Taille de la pile non valide"


###################################################
def test_calibration(qtbot):
	"""Vérifie la classe Calibration (constructeur, getter, setter)."""
	group_base_test(Calibration(), ["Pixel Size", "Exposure", "Intensity"], SpinFloat, 0.32, 0.16)


###################################################
def test_localization(qtbot):
	"""Vérifie la classe Localisation (constructeur, getter, setter)."""
	g = Localization()
	group_base_test(g, ["Preview", "Threshold", "Auto Threshold", "ROI Shape", "ROI Size", "Watershed", "Fit", "Gaussian Fit", "Spline Fit"],
					CheckBox, True, False)

	g["Fit"].value = 0
	assert g.get_fit() == 0, "Numéro du Fit incorrect"
	np.testing.assert_array_equal(g.get_fit_params(), np.array([7], dtype=np.float64))
	g["Fit"].value = 1
	assert g.get_fit() == 1, "Numéro du Fit incorrect"
	np.testing.assert_array_equal(g.get_fit_params(), np.array([7, 1, 2, 0], dtype=np.float64))
	g["Fit"].value = 2
	assert g.get_fit() == 5, "Numéro du Fit incorrect"
	with pytest.raises(OSError) as exception_info: g.get_fit_params()
	assert exception_info.type == OSError, "L'erreur relevé n'est pas correcte."
	assert isinstance(g.gaussian, GaussianFit)
	assert isinstance(g.spline, SplineFit)


###################################################
def test_localization_fit(qtbot):
	"""Vérifie la classe Localisation pour la récupération des paramètres de Fit."""
	loc = Localization()

	loc["Fit"].value = 0
	assert loc.get_fit() == 0, "Numéro du Fit incorrect"
	np.testing.assert_array_equal(loc.get_fit_params(), np.array([7], dtype=np.float64))
	loc["Fit"].value = 1
	assert loc.get_fit() == 1, "Numéro du Fit incorrect"
	np.testing.assert_array_equal(loc.get_fit_params(), np.array([7, 1, 2, 0], dtype=np.float64))
	loc["Fit"].value = 2
	assert loc.get_fit() == 5, "Numéro du Fit incorrect"
	with pytest.raises(OSError) as exception_info: loc.get_fit_params()
	assert exception_info.type == OSError, "L'erreur relevé n'est pas correcte."


###################################################
def test_gaussian_fit(qtbot):
	"""Vérifie la classe GaussianFit (constructeur, getter, setter)."""
	grp = GaussianFit()
	group_base_test(grp, ["Mode", "Sigma", "Theta", 'Z', 'Z max', 'Model'], Combo, 2, 0)


###################################################
def test_gaussian_fit_z(qtbot):
	"""Vérifie la classe GaussianFit avec affichage/masquage des éléments."""
	grp = GaussianFit()
	ui_z = grp["Z"].get_ui()
	ui_z_max = grp["Z max"].get_ui()
	assert ui_z.boxes[0].isHidden()
	grp["Mode"].value = 2
	assert not ui_z.boxes[0].isHidden()  # Ne pas utiliser isVisible, car cela demande visible à l'écran et dans les tests unitaires, c'est particulier.
	grp["Z"].value = True
	assert not ui_z_max.boxes[0].isHidden()
	grp["Z"].value = False
	assert ui_z_max.boxes[0].isHidden()
	grp["Z"].value = True
	assert not ui_z_max.boxes[0].isHidden()
	grp["Mode"].value = 0
	assert ui_z.boxes[0].isHidden()
	assert ui_z_max.boxes[0].isHidden()


###################################################
def test_spline_fit(qtbot):
	"""Vérifie la classe SplineFit (constructeur, getter, setter)."""
	group_base_test(SplineFit(), ["Sensor", "Variance Map", "File"], Combo, 1, 0)


###################################################
def test_beads(qtbot):
	"""Vérifie la classe BeadsExtraction (constructeur, getter, setter)."""
	group_base_test(BeadsExtraction(), ["Max Distance", "3D"], SpinFloat, 2, 1)


###################################################
def test_tracking(qtbot):
	"""Vérifie la classe Tracking (constructeur, getter, setter)."""
	group_base_test(Tracking(), ["Max Distance"], SpinFloat, 2, 1)


###################################################
def test_tracks_blinking_reconnection(qtbot):
	"""Vérifie la classe BlinkingReconnection (constructeur, getter, setter)."""
	group_base_test(BlinkingReconnection(), ["Mode", "Max Duration", "Max Distance"], Combo, 1, 0)


###################################################
def test_tracks_computes(qtbot):
	"""Vérifie la classe TracksCompute (constructeur, getter, setter)."""
	group_base_test(TracksCompute(), ["MSD", "Instant Diffusion", "Fit Length", "3D", "Log Scale", "Fit"], CheckBox, True, False)


###################################################
def test_filters(qtbot):
	"""Vérifie la classe Filters (constructeur, getter, setter)."""
	g = Filters()
	group_base_test(g, ["Save", "Plane", "ROI", "Localization", "Tracks"], CheckBox, True, False)
	g.deactivate_filters()
	g.update_limits(None)
	g.update_limits(10)
	assert isinstance(g.localization, FiltersL)
	assert isinstance(g.tracking, FiltersT)
	_ = g.get_ui()
	g.connect_button(lambda: print("Hi"), "default", "0")  # Bouton inexistant
	g.connect_button(lambda: print("Hi"), "new", "0")  # UI inexistante
	g.connect_button(lambda: print("Hi"), "default", "reset")

	g.show_part()
	g.show_part(localization=False, tracking=False)


###################################################
def test_filters_l(qtbot):
	"""Vérifie la classe FiltersL (constructeur, getter, setter)."""
	g = FiltersL()
	group_base_test(g, ["Z", "Intensity", "Sigma X", "Sigma Y", "Circularity", "Theta", "MSE XY", "MSE Z"], CheckRangeInt, [2, 9], [-2000, 2000])
	g.deactivate_filters()


###################################################
def test_filters_t(qtbot):
	"""Vérifie la classe FiltersT (constructeur, getter, setter)."""
	g = FiltersT()
	group_base_test(g, ["Track", "Length", "Instant D", "D Coeff", "Alpha", "Speed", "Confinement"], CheckIntSelection, "1;3-4", "")
	g.deactivate_filters()


###################################################
def test_gallery(qtbot):
	"""Vérifie la classe Gallery (constructeur, getter, setter)."""
	group_base_test(Gallery(), ["ROI Size", "ROIs Per Line"], SpinInt, 11, 9)


###################################################
def test_graph(qtbot):
	"""Vérifie la classe Graph (constructeur, getter, setter)."""
	g = Graph()
	group_base_test(Graph(), ["Type", "Source", "Dual", "Source B", "MSD Step", "Display"], ButtonGroup, 1, 0)
	g["Type"].value = 1  # Passage aux Tracks
	g["Source"].value = 3  # Passage au MSD
	assert isinstance(g.display, GraphDisplay)


###################################################
def test_graph_display(qtbot):
	"""Vérifie la classe GraphDisplay (constructeur, getter, setter)."""
	group_base_test(GraphDisplay(), ["Limits", "Sigma", "Gauss", "KDE", "Poiss", "Exp", "Cumul", "Log Scale", "Count", "Bins"], CheckBox, False, True)


###################################################
def test_hr(qtbot):
	"""Vérifie la classe HR (constructeur, getter, setter)."""
	g = HR()
	g["Type"].value = 1  # Passage aux Tracks
	g["Dimension"].value = 1  # Passage à Z-stack
	g["Dimension"].value = 2  # Passage à 3D Rotation
	g["Dimension"].reset()
	group_base_test(g, ["Dimension", "Type", "Source", "Scaling", "Color mode", "Ratio", "Crop", "Remove Beads",
						"Drift Correction", "Smooth Drift", "Gaussian", "3D"], ButtonGroup, 1, 0)
	assert isinstance(g.gaussian, HRGaussian)
	assert isinstance(g.hr_3d, HR3D)


###################################################
def test_hr_gaussian(qtbot):
	"""Vérifie la classe HRGaussian (constructeur, getter, setter)."""
	group_base_test(HRGaussian(), ["Intensity", "Fixed Intensity", "Shape", "Size"], SpinInt, 10, 100)


###################################################
def test_hr_3d(qtbot):
	"""Vérifie la classe HRGaussian (constructeur, getter, setter)."""
	group_base_test(HR3D(), ["Z Step", "Axis", "Frames"], SpinInt, 10, 20)


###################################################
def test_visualization_3d(qtbot):
	"""Vérifie la classe Visualization3D (constructeur, getter, setter)."""
	group_base_test(Visualization3D(), ["Point Size", "Pixel Size", "XY Scale", "Z Scale", "Remove Outliers"], SpinFloat, 2, 1)
