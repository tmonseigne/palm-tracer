""" Fichier des tests pour l'utilisation des DLL """

import os
from pathlib import Path

import numpy as np

from palm_tracer.Processing import get_gaussian_mode, get_max_points, load_dll, parse_palm_result, run_palm_image_dll, run_palm_stack_dll
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
	parsing = parse_palm_result(np.array(range(N_SEGMENTS * n_lines)))
	assert parsing.shape == (n_lines, N_SEGMENTS), "Le nombre de ligne ou de colonne ne correspond pas."


##################################################
def test_load_dll():
	"""Test basique sur le chargement des DLL."""
	dlls = load_dll()
	assert True


##################################################
def test_run_palm_image_dll():
	"""
	Test sur le lancement de PALM sur une frame.

	.. todo::
		Trouver un moyen de comparer avec les bons paramètres une sortie de PALM Tracer.
	"""
	dll = load_dll().get("CPU", None)
	if dll is None:
		print_warning("Test non effectué car DLL manquante")
	else:
		image = open_tif(f"{INPUT_DIR}/stack.tif")
		plane, threshold, watershed, sigma, theta, roi = 0, 62.4, True, 1.0, 0.0, 7
		for gaussian in range(5):
			points = run_palm_image_dll(dll, image[plane], threshold, watershed, gaussian, sigma, theta, roi)
			points.to_csv(f"{OUTPUT_DIR}/image-{plane}_{threshold}_{watershed}_{gaussian}_{sigma}_{theta}_{roi}.csv", index=False)
	assert True


##################################################
def test_run_palm_stack_dll():
	"""
	Test sur le lancement de PALM sur une pile.

	.. todo::
		Trouver un moyen de comparer avec les bons paramètres une sortie de PALM Tracer.
	"""
	dll = load_dll().get("CPU", None)
	if dll is None:
		print_warning("Test non effectué car DLL manquante")
	else:
		stack = open_tif(f"{INPUT_DIR}/stack.tif")
		threshold, watershed, sigma, theta, roi = 62.4, True, 1.0, 0.0, 7
		for gaussian in range(5):
			points = run_palm_stack_dll(dll, stack, threshold, watershed, gaussian, sigma, theta, roi)
			points.to_csv(f"{OUTPUT_DIR}/stack-{threshold}_{watershed}_{gaussian}_{sigma}_{theta}_{roi}.csv", index=False)
	assert True
