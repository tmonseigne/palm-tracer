""" Fichier des tests pour l'utilisation des DLL """

import os
from pathlib import Path

import pandas as pd

from palm_tracer._tests.Utils import compare_points
from palm_tracer.Processing import load_dll, run_palm_image_dll, run_palm_stack_dll, run_tracking_dll
from palm_tracer.Tools import open_tif, print_warning

INPUT_DIR = Path(__file__).parent / "input"
OUTPUT_DIR = Path(__file__).parent / "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)

threshold, watershed, sigma, theta, roi = 103.6, True, 1.0, 0.0, 7
default_gaussian = 2
save_output = True


##################################################
def compare_localizations(value: pd.DataFrame, ref: pd.DataFrame, tol: float = 1e-5) -> bool:
	return value[["X", "Y", "Z"]].sub(ref[["X", "Y", "Z"]]).abs().lt(tol).all().all()


##################################################
def get_suffix(gaussian: int) -> str:
	return f"{threshold}_{watershed}_{gaussian}_{sigma}_{theta}_{roi}"


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
		Comparer avec une sortie de PALM Tracer.
		Actuellement différence de résultat, nécessite une investigation.
	"""
	dll = load_dll().get("CPU", None)
	if dll is None:
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		file = "stack"
		stack = open_tif(f"{INPUT_DIR}/{file}.tif")
		for plane in range(stack.shape[0]):
			for gaussian in range(5):
				suffix = get_suffix(gaussian)

				localizations = run_palm_image_dll(dll, stack[plane], threshold, watershed, gaussian, sigma, theta, roi)
				if save_output: localizations.to_csv(f"{OUTPUT_DIR}/{file}-localisations-{plane}_{suffix}.csv", index=False)

				assert len(localizations) > 0, "Aucune localisation trouvé"

				path = Path(f"{INPUT_DIR}/{file}-localizations-{plane}_{suffix}.csv")
				if path.exists() and path.is_file():
					ref = pd.read_csv(path)
					assert compare_points(localizations, ref), f"Test invalide pour les paramètres {plane}_{suffix}"

		print_warning("\n====================\nAucune comparaison avec Metamorph dans ce test.\n====================\n")
	assert True


##################################################
def test_run_palm_stack_dll():
	"""
	Test sur le lancement de PALM sur une pile.

	.. todo::
		Comparer avec une sortie de PALM Tracer.
		Actuellement différence de résultat, nécessite une investigation.
	"""
	dll = load_dll().get("CPU", None)
	if dll is None:
		print_warning("Test non effectué car DLL manquante")
	else:
		file = "stack"
		stack = open_tif(f"{INPUT_DIR}/{file}.tif")
		for gaussian in range(5):
			suffix = get_suffix(gaussian)

			localizations = run_palm_stack_dll(dll, stack, threshold, watershed, gaussian, sigma, theta, roi)
			if save_output: localizations.to_csv(f"{OUTPUT_DIR}/{file}-localizations-{suffix}.csv", index=False)

			assert len(localizations) > 0, "Aucune localisation trouvé"

			path = Path(f"{INPUT_DIR}/{file}-localizations-{suffix}.csv")
			if path.exists() and path.is_file():
				ref = pd.read_csv(path)
				assert compare_points(localizations, ref), f"Test invalide pour les paramètres {suffix}"

		print_warning("\n====================\nAucune comparaison avec Metamorph dans ce test.\n====================\n")
	assert True


##################################################
def test_run_palm_stack_dll_check_quadrant():
	"""
	Test sur le lancement de PALM sur une pile.

	.. todo::
		Comparer avec une sortie de PALM Tracer.
		Actuellement différence de résultat, nécessite une investigation
	"""
	dll = load_dll().get("CPU", None)
	if dll is None:
		print_warning("Test non effectué car DLL manquante")
	else:
		suffix = get_suffix(default_gaussian)
		file = "stack_quadrant"
		stack = open_tif(f"{INPUT_DIR}/{file}.tif")

		localizations = run_palm_stack_dll(dll, stack, threshold, watershed, default_gaussian, sigma, theta, roi)
		if save_output: localizations.to_csv(f"{OUTPUT_DIR}/{file}-localizations-{suffix}.csv", index=False)

		quadrant = {"Top":    localizations['Plane'].isin([3, 4, 7, 8]),
					"Bottom": localizations['Plane'].isin([1, 2, 5, 6, 9, 10]),
					"Left":   localizations['Plane'].isin([1, 4, 5, 8, 9]),
					"Right":  localizations['Plane'].isin([2, 3, 6, 7, 10])}
		assert (localizations.loc[quadrant["Top"], 'Y'] <= 128).all(), "Des éléments ont été trouvé dans la zone noire en haut de l'image."
		assert (localizations.loc[quadrant["Bottom"], 'Y'] >= 128).all(), "Des éléments ont été trouvé dans la zone noire en bas de l'image."
		assert (localizations.loc[quadrant["Left"], 'X'] <= 128).all(), "Des éléments ont été trouvé dans la zone noire à gauche de l'image."
		assert (localizations.loc[quadrant["Right"], 'X'] >= 128).all(), "Des éléments ont été trouvé dans la zone noire à droite de l'image."

		path = Path(f"{INPUT_DIR}/{file}-localizations-{suffix}.csv")
		if path.exists() and path.is_file():
			ref = pd.read_csv(path)
			assert compare_points(localizations, ref), "Test invalide pour la vérification des quadrants."

		print_warning("\n====================\nAucune comparaison avec Metamorph dans ce test.\n====================\n")
	assert True


##################################################
def test_run_tracking_dll():
	"""Test basique sur le tracking."""
	dll = load_dll().get("Tracking", None)
	if dll is None:
		print_warning("Test non effectué car DLL manquante")
	else:
		suffix = get_suffix(default_gaussian)

		path = Path(f"{INPUT_DIR}/stack-localizations-{suffix}.csv")
		if path.exists() and path.is_file():
			localizations = pd.read_csv(path)
			tracking = run_tracking_dll(dll, localizations, 5, 1, 10, 0.5)
			if save_output: tracking.to_csv(f"{OUTPUT_DIR}/stack-tracking-{suffix}.csv", index=False)

			assert len(tracking) > 0, "Aucun Tracking trouvé"
			print_warning("\n====================\nAucune comparaison avec Metamorph dans ce test.\n====================\n")
		else:
			print_warning(f"Fichier de localisations '{path}' indisponible.")

	assert True
