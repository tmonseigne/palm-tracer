""" Fichier des tests pour l'utilisation des DLL """

import os
from pathlib import Path

import pandas as pd

from palm_tracer.Processing import load_dll, run_palm_image_dll, run_palm_stack_dll
from palm_tracer.Tools import open_tif, print_warning

INPUT_DIR = Path(__file__).parent / "input"
OUTPUT_DIR = Path(__file__).parent / "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)


##################################################
def compare_localisations(value: pd.DataFrame, ref: pd.DataFrame, tol: float = 1e-5) -> bool:
	return value[["X", "Y", "Z"]].sub(ref[["X", "Y", "Z"]]).abs().lt(tol).all().all()


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
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		file = "stack"
		stack = open_tif(f"{INPUT_DIR}/{file}.tif")
		threshold, watershed, sigma, theta, roi = 103.6, True, 1.0, 0.0, 7
		for plane in range(stack.shape[0]):
			for gaussian in range(5):
				localisations = run_palm_image_dll(dll, stack[plane], threshold, watershed, gaussian, sigma, theta, roi)
				# localisations.to_csv(f"{OUTPUT_DIR}/{file}-localisations_{plane}_{threshold}_{watershed}_{gaussian}_{sigma}_{theta}_{roi}.csv", index=False)
				assert len(localisations) > 0, "Aucune localisation trouvé"
				path = Path(f"{INPUT_DIR}/{file}-localisations_{plane}_{threshold}_{watershed}_{gaussian}_{sigma}_{theta}_{roi}.csv")
				if path.exists() and path.is_file():
					ref = pd.read_csv(path)
					assert compare_localisations(localisations, ref), (f"Test invalide pour les paramètres "
																	   f"{plane}_{threshold}_{watershed}_{gaussian}_{sigma}_{theta}_{roi}")
		print_warning("\n====================\nAucune comparaison avec Metamorph dans ce test.\n====================\n")
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
		file = "stack"
		stack = open_tif(f"{INPUT_DIR}/{file}.tif")
		threshold, watershed, sigma, theta, roi = 103.6, True, 1.0, 0.0, 7
		for gaussian in range(5):
			localisations = run_palm_stack_dll(dll, stack, threshold, watershed, gaussian, sigma, theta, roi)
			# localisations.to_csv(f"{OUTPUT_DIR}/{file}-localisations_{threshold}_{watershed}_{gaussian}_{sigma}_{theta}_{roi}.csv", index=False)
			assert len(localisations) > 0, "Aucune localisation trouvé"
			path = Path(f"{INPUT_DIR}/{file}-localisations_{threshold}_{watershed}_{gaussian}_{sigma}_{theta}_{roi}.csv.csv")
			if path.exists() and path.is_file():
				ref = pd.read_csv(path)
				assert compare_localisations(localisations, ref), (f"Test invalide pour les paramètres "
																   f"{threshold}_{watershed}_{gaussian}_{sigma}_{theta}_{roi}")
		print_warning("\n====================\nAucune comparaison avec Metamorph dans ce test.\n====================\n")
	assert True


##################################################
def test_run_palm_stack_dll_check_quadrant():
	"""
	Test sur le lancement de PALM sur une pile.

	.. todo::
		Trouver un moyen de comparer avec les bons paramètres une sortie de PALM Tracer.
	"""
	dll = load_dll().get("CPU", None)
	if dll is None:
		print_warning("Test non effectué car DLL manquante")
	else:
		file = "stack_quadrant"
		stack = open_tif(f"{INPUT_DIR}/{file}.tif")
		threshold, watershed, sigma, theta, roi = 103.6, False, 1.0, 0.0, 7
		localisations = run_palm_stack_dll(dll, stack, threshold, watershed, 0, sigma, theta, roi)
		quadrant = {"Top":    localisations['Plane'].isin([3, 4, 7, 8]),
					"Bottom": localisations['Plane'].isin([1, 2, 5, 6, 9, 10]),
					"Left":   localisations['Plane'].isin([1, 4, 5, 8, 9]),
					"Right":  localisations['Plane'].isin([2, 3, 6, 7, 10])}
		assert (localisations.loc[quadrant["Top"], 'Y'] <= 128).all(), "Des éléments ont été trouvé dans la zone noire en haut de l'image."
		assert (localisations.loc[quadrant["Bottom"], 'Y'] >= 128).all(), "Des éléments ont été trouvé dans la zone noire en bas de l'image."
		assert (localisations.loc[quadrant["Left"], 'X'] <= 128).all(), "Des éléments ont été trouvé dans la zone noire à gauche de l'image."
		assert (localisations.loc[quadrant["Right"], 'X'] >= 128).all(), "Des éléments ont été trouvé dans la zone noire à droite de l'image."
		path = Path(f"{INPUT_DIR}/{file}-localisations_{threshold}_{watershed}_0_{sigma}_{theta}_{roi}.csv.csv")
		if path.exists() and path.is_file():
			ref = pd.read_csv(path)
			assert compare_localisations(localisations, ref), "Test invalide pour la vérification des quadrants."
	assert True
