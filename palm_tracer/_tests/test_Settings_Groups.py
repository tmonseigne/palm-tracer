""" Fichier des tests pour l'ensemble des paramètres. """

import sys
from pathlib import Path
from typing import Any, cast, Type

from qtpy.QtCore import QCoreApplication, Qt
from qtpy.QtWidgets import QApplication

from palm_tracer.Settings.Groups import *
from palm_tracer.Settings.Types import *

INPUT_DIR = Path(__file__).parent / "input"


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


###################################################
def test_base_group():
	"""Test basique de la classe abstraite"""
	app = initialize()
	group = BaseSettingGroup()
	group.set_value(None)
	assert group.get_value() is None, "Get Value ne doit rien retourné pour la classe mère."


###################################################
def test_batch():
	"""Test basique de la classe Batch (constructeur, getter, setter)"""
	app = initialize()
	batch = Batch()
	group_base_test(batch, ["Files", "Mode"],
					FileList, -1, -1)


###################################################
def test_batch_get_path():
	"""Test du get_path de la classe Batch"""
	app = initialize()
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
def test_batch_get_stacks():
	"""Test du get_path de la classe Batch"""
	app = initialize()
	batch = Batch()
	file_list = cast(FileList, batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif", f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()

	batch["Mode"].set_value(0)
	stacks = batch.get_stacks()
	assert len(stacks) == 1, "Nombre de pile invalide"
	assert stacks[0].shape == (10, 128, 256), "Taille de la pile non valide"

	batch["Mode"].set_value(1)
	stacks = batch.get_stacks()
	assert len(stacks) == 2, "Nombre de pile invalide"
	assert stacks[0].shape == (10, 128, 256), "Taille de la pile non valide"

	batch["Mode"].set_value(2)
	stacks = batch.get_stacks()
	assert len(stacks) == 1, "Nombre de pile invalide"
	assert stacks[0].shape == (20, 128, 256), "Taille de la pile non valide"


###################################################
def test_calibration():
	"""Test basique de la classe Calibration (constructeur, getter, setter)"""
	app = initialize()
	group_base_test(Calibration(), ["Pixel Size", "Exposure", "Intensity"],
					SpinInt, 320, 160)


###################################################
def test_localisation():
	"""Test basique de la classe Localisation (constructeur, getter, setter)"""
	app = initialize()
	group_base_test(Localisation(), ["Preview", "Threshold", "ROI Size", "Watershed", "Mode", "Gaussian Fit"],
					CheckBox, True, False)


###################################################
def test_gaussian_fit():
	"""Test basique de la classe GaussianFit (constructeur, getter, setter)"""
	app = initialize()
	group_base_test(GaussianFit(), ["Mode", "Sigma", "Theta"],
					Combo, 2, 1)


###################################################
def test_spline_fit():
	"""Test basique de la classe SplineFit (constructeur, getter, setter)"""
	app = initialize()
	spline_fit = SplineFit()
	# group_base_test(SplineFit(), ["Mode", "Sigma", "Theta"], Combo, 2, 1)

###################################################
def test_filtering():
	"""Test basique de la classe Filtering (constructeur, getter, setter)"""
	app = initialize()
	group_base_test(Filtering(), ["Plane", "Intensity", "Gaussian Fit", "Tracks"],
					SpinInt, 2, 1)


###################################################
def test_filtering_gf():
	"""Test basique de la classe FilteringGF (constructeur, getter, setter)"""
	app = initialize()
	group_base_test(FilteringGF(), ["Chi²", "Sigma X", "Sigma Y", "Circularity", "Z"],
					SpinInt, 2, 0)


###################################################
def test_filtering_t():
	"""Test basique de la classe FilteringT (constructeur, getter, setter)"""
	app = initialize()
	group_base_test(FilteringT(), ["Length", "D Coeff", "Instant D", "Speed", "Alpha", "Confinement"],
					SpinInt, 2, 0)
