"""Fichier des tests pour les groupes de paramètres."""
import copy
from typing import List, Type

import pytest
from qtpy.QtWidgets import QFormLayout, QWidget

from palm_tracer._tests.Utils import *
from palm_tracer.Settings.Groups import *
from palm_tracer.Settings.Types import BaseSettingType, CheckBox, CheckRangeInt, Combo, SpinFloat, SpinInt


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
	form = QFormLayout(w)  # crée et assigne le layout au widget
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


###################################################
def test_base_group(qtbot):
	"""Test basique de la classe abstraite"""
	group = BaseSettingGroup()
	group.value = None
	assert group.value is None, "Get Value ne doit rien retourné pour la classe mère."

	received: List[Any] = []
	group.connect(lambda v: received.append(v))
	with group.signal_blocked(): pass
	group.disconnect()


###################################################
def test_batch(qtbot):
	"""Test basique de la classe Batch (constructeur, getter, setter)"""
	batch = Batch()
	group_base_test(batch, ["Files", "Mode"], FileList, -1, -1)


###################################################
def test_batch_get_path(qtbot):
	"""Test du get_path de la classe Batch"""
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
	"""Test du get_path de la classe Batch"""
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
	"""Test basique de la classe Calibration (constructeur, getter, setter)"""
	group_base_test(Calibration(), ["Pixel Size", "Exposure", "Intensity"], SpinFloat, 0.32, 0.16)


###################################################
def test_localization(qtbot):
	"""Test basique de la classe Localisation (constructeur, getter, setter)"""
	loc = Localization()
	group_base_test(loc, ["Preview", "Threshold", "Auto Threshold", "ROI Shape", "ROI Size", "Watershed", "Fit", "Gaussian Fit", "Spline Fit"],
					CheckBox, True, False)

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
def test_localization_fit(qtbot):
	"""Test basique de la classe Localisation (constructeur, getter, setter)"""
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
	"""Test basique de la classe GaussianFit (constructeur, getter, setter)"""
	grp = GaussianFit()
	group_base_test(grp, ["Mode", "Sigma", "Theta", 'Z', 'Z max', 'Model'], Combo, 2, 0)


###################################################
def test_gaussian_fit_z(qtbot):
	"""Test basique de la classe GaussianFit (constructeur, getter, setter)"""
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
	"""Test basique de la classe SplineFit (constructeur, getter, setter)"""
	group_base_test(SplineFit(), ["Sensor", "Variance Map", "File"], Combo, 1, 0)


###################################################
def test_beads(qtbot):
	"""Test basique de la classe BeadsExtraction (constructeur, getter, setter)"""
	group_base_test(BeadsExtraction(), ["Max Distance", "3D"], SpinFloat, 2, 1)


###################################################
def test_tracking(qtbot):
	"""Test basique de la classe Tracking (constructeur, getter, setter)"""
	group_base_test(Tracking(), ["Max Distance"], SpinFloat, 2, 1)


###################################################
def test_tracks_blinking_reconnection(qtbot):
	"""Test basique de la classe BlinkingReconnection (constructeur, getter, setter)"""
	group_base_test(BlinkingReconnection(), ["Mode", "Max Duration", "Max Distance"], Combo, 1, 0)


###################################################
def test_tracks_computes(qtbot):
	"""Test basique de la classe TracksCompute (constructeur, getter, setter)"""
	group_base_test(TracksCompute(), ["MSD", "Instant Diffusion", "Fit Length", "3D", "Log Scale", "Fit"], CheckBox, True, False)


###################################################
def test_filters(qtbot):
	"""Test basique de la classe Filters (constructeur, getter, setter)"""
	g = Filters()
	group_base_test(g, ["Save", "Plane", "Localization", "Tracks"], CheckBox, True, False)
	g.deactivate_filters()
	g.update_limits(None, None, None)
	g.update_limits(10, 10, 10)
	assert isinstance(g.localization, FiltersL)
	assert isinstance(g.tracking, FiltersT)


###################################################
def test_filters_l(qtbot):
	"""Test basique de la classe FiltersL (constructeur, getter, setter)"""
	g = FiltersL()
	group_base_test(g, ["X", "Y", "Z", "Intensity", "Sigma X", "Sigma Y", "Circularity", "Theta", "MSE XY", "MSE Z"], CheckRangeInt, [2, 9], [0, 100000])
	g.deactivate_filters()


###################################################
def test_filters_t(qtbot):
	"""Test basique de la classe FiltersT (constructeur, getter, setter)"""
	g = FiltersT()
	group_base_test(g, ["Length", "Instant D", "D Coeff", "Alpha", "Speed", "Confinement"], CheckRangeInt, [2, 3], [1, 10000])
	g.deactivate_filters()


###################################################
def test_gallery(qtbot):
	"""Test basique de la classe VisualizationHR (constructeur, getter, setter)"""
	group_base_test(Gallery(), ["ROI Size", "ROIs Per Line"], SpinInt, 11, 9)


###################################################
def test_visualization_3d(qtbot):
	"""Test basique de la classe SplineFit (constructeur, getter, setter)"""
	group_base_test(Visualization3D(), ["Point Size", "XY Scale", "Z Scale", "Remove Outliers"], SpinFloat, 1, 0.5)


###################################################
def test_visualization_graph(qtbot):
	"""Test basique de la classe SplineFit (constructeur, getter, setter)"""
	group_base_test(VisualizationGraph(), ["Mode", "Source"], Combo, 1, 0)


###################################################
def test_visualization_hr(qtbot):
	"""Test basique de la classe VisualizationHR (constructeur, getter, setter)"""
	g = VisualizationHR()
	group_base_test(g, ["Ratio", "Type", "Source L", "Source T"], SpinInt, 1, 2)
	g["Type"].value = 1  # Afficher/masquer les sources
	g["Type"].value = 0  # Afficher/masquer les sources
	g["Type"].value = 2  # Impossible mais prévu
