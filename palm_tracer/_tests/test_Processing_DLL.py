""" Fichier des tests pour l'utilisation des DLL """

import os
from pathlib import Path

import numpy as np

from palm_tracer.Processing import get_gaussian_mode, get_max_points, load_dll, parse_palm_result, run_palm_dll
from palm_tracer.Processing.DLL import N_SEGMENTS
from palm_tracer.Tools import open_tif, print_warning

INPUT_DIR = Path(__file__).parent / "input"
OUTPUT_DIR = Path(__file__).parent / "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)


##################################################
def test_get_gaussian_mode():
	"""Test basique sur la récupération du mode de gaussienne fit."""
	assert get_gaussian_mode(False, False, False) == 0, "Le mode devrait être 0 (None)"
	assert get_gaussian_mode(True, True, True) == 1, "Le mode devrait être 1 (X Y)"
	assert get_gaussian_mode(True, False, True) == 2, "Le mode devrait être 2 (X, Y sigma)"
	assert get_gaussian_mode(True, True, False) == 3, "Le mode devrait être 3 (X, Y sigmaX, sigmaY)"
	assert get_gaussian_mode(True, False, False) == 4, "Le mode devrait être 4 (X, Y sigmaX, sigmaY, Theta)"


##################################################
def test_get_max_points():
	"""Test basique sur la récupération du mode de gaussienne fit."""
	assert get_max_points(10, 10, 1, 10) == 13000, "Le nombre de points maximum théorique n'est pas le bon."


##################################################
def test_parse_palm_result():
	"""Test basique sur la récupération du mode de gaussienne fit."""
	n_lines = 10
	parsing = parse_palm_result(np.array(range(N_SEGMENTS * n_lines)))  # La première ligne sera supprimé avec le tri
	assert parsing.shape == (n_lines - 1, N_SEGMENTS), "Le nombre de ligne ou de colonne ne correspond pas."


##################################################
def test_load_dll():
	"""Test basique sur le chargement des DLL."""
	dlls = load_dll()
	assert True


##################################################
def test_run_palm_dll():
	"""
	Test basique sur le lancement d'une DLL.

	.. todo::
		Trouver un moyen de comparer avec les bons paramètres une sortie de PALM Tracer.
		Actuellement aucune correspondance.
	"""
	dll = load_dll().get("CPU", None)
	if dll is None:
		print_warning("Test non effectué car DLL manquante")
	else:
		image = open_tif(f"{INPUT_DIR}/stack.tif")
		plane = 0
		threshold = 62.4
		watershed = True
		sigma = 1.0
		theta = 0.0
		roi = 7
		for gaussian in range(5):
			points = run_palm_dll(dll, image[plane], threshold, watershed, gaussian, sigma, theta, roi)
			points.to_csv(f"{OUTPUT_DIR}/stack-{plane}_{threshold}_{watershed}_{gaussian}_{sigma}_{theta}_{roi}.csv", index=False)
	assert True
