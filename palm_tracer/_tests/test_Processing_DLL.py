""" Fichier des tests pour l'utilisation des DLL """

import os
from pathlib import Path

from palm_tracer.Processing import load_dll, run_palm_image_dll, run_palm_stack_dll
from palm_tracer.Tools import open_tif, print_warning

INPUT_DIR = Path(__file__).parent / "input"
OUTPUT_DIR = Path(__file__).parent / "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)

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
			localisations = run_palm_image_dll(dll, image[plane], threshold, watershed, gaussian, sigma, theta, roi)
			localisations.to_csv(f"{OUTPUT_DIR}/image-{plane}_{threshold}_{watershed}_{gaussian}_{sigma}_{theta}_{roi}.csv", index=False)
		print_warning("Aucune comparaison avec Metamorph dans ce test.")
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
			localisations = run_palm_stack_dll(dll, stack, threshold, watershed, gaussian, sigma, theta, roi)
			localisations.to_csv(f"{OUTPUT_DIR}/stack-{threshold}_{watershed}_{gaussian}_{sigma}_{theta}_{roi}.csv", index=False)
		print_warning("Aucune comparaison avec Metamorph dans ce test.")
	assert True
