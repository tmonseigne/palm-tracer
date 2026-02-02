""" Fichier des tests pour les groupes de paramètres. """
from typing import cast, List, Type

import pytest

from palm_tracer._tests.Utils import *
from palm_tracer.Settings.Groups import *
from palm_tracer.Settings.Types import *


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

	group.toggle_active(0)
	assert group.active == False, "Les paramètres doivent être désactivés."
	group.active = True
	assert group.active == True, "Les paramètres doivent être activés."
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
	print(group.get_settings())

	received: List[Any] = []
	group.connect(lambda v: received.append(v))
	with group.signal_blocked(): pass
	group.disconnect()


###################################################
def test_base_group(make_napari_viewer):
	"""Test basique de la classe abstraite"""
	group = BaseSettingGroup()
	group.set_value(None)
	assert group.get_value() is None, "Get Value ne doit rien retourné pour la classe mère."
	group.remove_header()
	group.remove_header()  # Seconde fois pour vérifier les erreur de pointeurs QT
	group.active = False  # On change le statut malgré la suppression du Header

	received: List[Any] = []
	group.connect(lambda v: received.append(v))
	with group.signal_blocked(): pass
	group.disconnect()


###################################################
def test_batch(make_napari_viewer):
	"""Test basique de la classe Batch (constructeur, getter, setter)"""
	batch = Batch()
	group_base_test(batch, ["Files", "Mode"], FileList, -1, -1)


###################################################
def test_batch_get_path(make_napari_viewer):
	"""Test du get_path de la classe Batch"""
	batch = Batch()

	path = batch.get_paths()
	assert len(path) == 1, "Il ne devrait y avoir qu'un seul dossier."
	assert path[0].endswith("_PALM_Tracer"), "Le nom du dossier ne correspond pas."

	file_list = cast(FileList, batch["Files"])
	file_list.items = ["output/File 1.tif", "output/File 2.tif"]
	file_list.update_box()

	path = batch.get_paths()
	assert len(path) == 1, "Il ne devrait y avoir qu'un seul dossier."
	assert path[0] == "output/File 1_PALM_Tracer", "Le nom du dossier ne correspond pas."

	file_list.set_value(1)
	path = batch.get_paths()
	assert len(path) == 1, "Il ne devrait y avoir qu'un seul dossier."
	assert path[0] == "output/File 2_PALM_Tracer", "Le nom du dossier ne correspond pas."

	batch["Mode"].set_value(1)
	path = batch.get_paths()
	assert len(path) == 2, "Il devrait y avoir deux dossiers."
	assert path[0] == "output/File 1_PALM_Tracer", "Le nom du dossier ne correspond pas."
	assert path[1] == "output/File 2_PALM_Tracer", "Le nom du dossier ne correspond pas."

	batch["Mode"].set_value(2)
	path = batch.get_paths()
	assert len(path) == 1, "Il ne devrait y avoir qu'un seul dossier."
	assert path[0] == "output/File 1_PALM_Tracer", "Le nom du dossier ne correspond pas."


###################################################
def test_batch_get_stacks(make_napari_viewer):
	"""Test du get_path de la classe Batch"""
	batch = Batch()
	stacks = batch.get_stacks()
	assert len(stacks) == 0, "Nombre de pile invalide"

	file_list = cast(FileList, batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif", f"{INPUT_DIR}/stack.tif", f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()

	batch["Mode"].set_value(0)
	stacks = batch.get_stacks()
	assert len(stacks) == 1, "Nombre de pile invalide"
	assert stacks[0].shape == (10, 128, 256), "Taille de la pile non valide"

	batch["Mode"].set_value(1)
	stacks = batch.get_stacks()
	assert len(stacks) == 3, "Nombre de pile invalide"
	assert stacks[0].shape == (10, 128, 256), "Taille de la pile non valide"

	batch["Mode"].set_value(2)
	stacks = batch.get_stacks()
	assert len(stacks) == 1, "Nombre de pile invalide"
	assert stacks[0].shape == (30, 128, 256), "Taille de la pile non valide"

	file_list.items = [f"{INPUT_DIR}/stack.tif", f"{INPUT_DIR}/stack_quadrant.tif", f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	batch["Mode"].set_value(2)
	stacks = batch.get_stacks()
	assert len(stacks) == 3, "Nombre de pile invalide"
	assert stacks[0].shape == (10, 128, 256), "Taille de la pile non valide"


###################################################
def test_calibration(make_napari_viewer):
	"""Test basique de la classe Calibration (constructeur, getter, setter)"""
	group_base_test(Calibration(), ["Pixel Size", "Exposure", "Intensity"], SpinFloat, 0.32, 0.16)


###################################################
def test_localization(make_napari_viewer):
	"""Test basique de la classe Localisation (constructeur, getter, setter)"""
	loc = Localization()

	group_base_test(loc, ["Preview", "Threshold", "Auto Threshold", "ROI Shape", "ROI Size", "Watershed", "Fit", "Gaussian Fit", "Spline Fit"],
					CheckBox, True, False)

	loc["Fit"].set_value(0)
	assert loc.get_fit() == 0, "Numéro du Fit incorrect"
	np.testing.assert_array_equal(loc.get_fit_params(), np.array([7], dtype=np.float64))

	loc["Fit"].set_value(1)
	assert loc.get_fit() == 1, "Numéro du Fit incorrect"
	np.testing.assert_array_equal(loc.get_fit_params(), np.array([7, 1, 2, 0], dtype=np.float64))

	loc["Fit"].set_value(2)
	assert loc.get_fit() == 5, "Numéro du Fit incorrect"
	with pytest.raises(OSError) as exception_info:
		loc.get_fit_params()
	assert exception_info.type == OSError, "L'erreur relevé n'est pas correcte."


###################################################
def test_gaussian_fit(make_napari_viewer):
	"""Test basique de la classe GaussianFit (constructeur, getter, setter)"""
	group_base_test(GaussianFit(), ["Mode", "Sigma", "Theta"], Combo, 2, 0)


###################################################
def test_spline_fit(make_napari_viewer):
	"""Test basique de la classe SplineFit (constructeur, getter, setter)"""
	group_base_test(SplineFit(), ["Sensor", "Variance Map", "File"], Combo, 1, 0)


###################################################
def test_tracking(make_napari_viewer):
	"""Test basique de la classe Tracking (constructeur, getter, setter)"""
	group_base_test(Tracking(), ["Max Distance", "Blinking Reconnection"], SpinFloat, 2, 1)


###################################################
def test_gallery(make_napari_viewer):
	"""Test basique de la classe VisualizationHR (constructeur, getter, setter)"""
	group_base_test(Gallery(), ["ROI Size", "ROIs Per Line"], SpinInt, 11, 9)


###################################################
def test_visualization_hr(make_napari_viewer):
	"""Test basique de la classe VisualizationHR (constructeur, getter, setter)"""
	g = VisualizationHR()
	group_base_test(g, ["Ratio", "Type", "Source L", "Source T"], SpinInt, 1, 2)
	g["Type"].set_value(1)  # Afficher/masquer les sources
	g["Type"].set_value(0)  # Afficher/masquer les sources
	g["Type"].set_value(2)  # Impossible mais prévu


###################################################
def test_visualization_graph(make_napari_viewer):
	"""Test basique de la classe SplineFit (constructeur, getter, setter)"""
	group_base_test(VisualizationGraph(), ["Mode", "Source"], Combo, 1, 0)


###################################################
def test_filtering(make_napari_viewer):
	"""Test basique de la classe Filtering (constructeur, getter, setter)"""
	g = Filtering()
	group_base_test(g, ["Save", "Plane", "Localization", "Tracks"], CheckBox, True, False)
	g.deactivate_filters()


###################################################
def test_filtering_l(make_napari_viewer):
	"""Test basique de la classe FilteringL (constructeur, getter, setter)"""
	g = FilteringL()
	group_base_test(g, ["X", "Y", "Z", "Intensity", "Sigma X", "Sigma Y", "Circularity", "Theta", "MSE XY", "MSE Z"], CheckRangeInt, [2, 9], [0, 100000])
	g.deactivate_filters()


###################################################
def test_filtering_t(make_napari_viewer):
	"""Test basique de la classe FilteringT (constructeur, getter, setter)"""
	g = FilteringT()
	group_base_test(g, ["Length", "Instant D", "D Coeff", "Alpha", "Speed", "Confinement"], CheckRangeInt, [2, 3], [1, 10000])
	g.deactivate_filters()


###################################################
def test_tracks_blinking_reconnection(make_napari_viewer):
	"""Test basique de la classe TracksBlinkingReconnection (constructeur, getter, setter)"""
	group_base_test(TracksBlinkingReconnection(), ["Mode", "Max Duration", "Max Speed"], Combo, 1, 0)


###################################################
def test_tracks_computes(make_napari_viewer):
	"""Test basique de la classe TracksCompute (constructeur, getter, setter)"""
	group_base_test(TracksCompute(), ["MSD", "Instant Diffusion", "Fit Length", "3D", "Log Scale", "Fit"], CheckBox, True, False)
