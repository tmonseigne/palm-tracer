""" Fichier des tests pour l'utilisation de la DLL CPU. """

import os
from pathlib import Path

import pandas as pd

from palm_tracer._tests.Utils import compare_points, is_closed
from palm_tracer.Processing.DLL import PalmCPU
from palm_tracer.Tools import open_tif, print_warning

INPUT_DIR = Path(__file__).parent / "input"
OUTPUT_DIR = Path(__file__).parent / "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)

threshold, watershed, sigma, theta, roi = 103.6, True, 1.0, 0.0, 7
max_distance, min_life, decrease, cost_birth = 5, 2, 10, 0.5
default_gaussian = 4
save_output = True


##################################################
def get_loc_suffix(gaussian: int = default_gaussian) -> str:
	"""
	Génère un suffixe pour les fichiers de localisation.

	:param gaussian: Mode du filtre gaussien.
	:return: suffixe
	"""
	return f"{threshold}_{watershed}_{gaussian}_{sigma}_{theta}_{roi}"


##################################################
def test_palm_cpu_image():
	""" Test sur le lancement de PALM sur une frame. """
	palm = PalmCPU()
	if not palm.is_valid():
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		file = "stack"
		stack = open_tif(f"{INPUT_DIR}/{file}.tif")
		for plane in range(stack.shape[0]):
			for gaussian in range(5):
				suffix = get_loc_suffix(gaussian)

				localizations = palm.run_image(stack[plane], threshold, watershed, gaussian, sigma, theta, roi, plane + 1)
				if save_output: localizations.to_csv(f"{OUTPUT_DIR}/{file}-localizations-{plane}_{suffix}.csv", index=False)

				assert len(localizations) > 0, "Aucune localisation trouvé"

				path = Path(f"{INPUT_DIR}/ref/{file}-localizations-{plane}_{suffix}.csv")
				if path.exists() and path.is_file():
					print(f"Comparaison avec : '{path}'")
					ref = pd.read_csv(path)
					assert compare_points(localizations, ref), f"Test invalide pour les paramètres {plane}_{suffix}"
	assert True


##################################################
def test_palm_cpu_stack():
	""" Test sur le lancement de PALM sur une pile. """
	palm = PalmCPU()
	if not palm.is_valid():
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		file = "stack"
		stack = open_tif(f"{INPUT_DIR}/{file}.tif")
		for gaussian in range(5):
			suffix = get_loc_suffix(gaussian)

			localizations = palm.run_stack(stack, threshold, watershed, gaussian, sigma, theta, roi)
			if save_output: localizations.to_csv(f"{OUTPUT_DIR}/{file}-localizations-{suffix}.csv", index=False)

			assert len(localizations) > 0, "Aucune localisation trouvé"

			path = Path(f"{INPUT_DIR}/ref/{file}-localizations-{suffix}.csv")
			if path.exists() and path.is_file():
				print(f"Comparaison avec : '{path}'")
				ref = pd.read_csv(path)
				assert compare_points(localizations, ref), f"Test invalide pour les paramètres {suffix}"
	assert True


##################################################
def test_palm_cpu_stack_plane_selection():
	""" Test sur le lancement de PALM sur une pile. """
	palm = PalmCPU()
	if not palm.is_valid():
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		file = "stack"
		stack = open_tif(f"{INPUT_DIR}/{file}.tif")
		suffix = get_loc_suffix()

		localizations = palm.run_stack(stack, threshold, watershed, default_gaussian, sigma, theta, roi, [2, 4, 6, -1, 10])
		if save_output: localizations.to_csv(f"{OUTPUT_DIR}/{file}-localizations-plane_select-{suffix}.csv", index=False)
		assert len(localizations) > 0, "Aucune localisation trouvé"


##################################################
def test_palm_cpu_stack_dll_check_quadrant():
	"""	Test sur le lancement de PALM sur une pile. """
	palm = PalmCPU()
	if not palm.is_valid():
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		suffix = get_loc_suffix()
		file = "stack_quadrant"
		stack = open_tif(f"{INPUT_DIR}/{file}.tif")

		localizations = palm.run_stack(stack, threshold, watershed, default_gaussian, sigma, theta, roi)
		if save_output: localizations.to_csv(f"{OUTPUT_DIR}/{file}-localizations-{suffix}.csv", index=False)

		quadrant = {"Top":    localizations['Plane'].isin([3, 4, 7, 8]),
					"Bottom": localizations['Plane'].isin([1, 2, 5, 6, 9, 10]),
					"Left":   localizations['Plane'].isin([1, 4, 5, 8, 9]),
					"Right":  localizations['Plane'].isin([2, 3, 6, 7, 10])}
		assert (localizations.loc[quadrant["Top"], 'Y'] <= 128).all(), "Des éléments ont été trouvé dans la zone noire en haut de l'image."
		assert (localizations.loc[quadrant["Bottom"], 'Y'] >= 128).all(), "Des éléments ont été trouvé dans la zone noire en bas de l'image."
		assert (localizations.loc[quadrant["Left"], 'X'] <= 128).all(), "Des éléments ont été trouvé dans la zone noire à gauche de l'image."
		assert (localizations.loc[quadrant["Right"], 'X'] >= 128).all(), "Des éléments ont été trouvé dans la zone noire à droite de l'image."

		path = Path(f"{INPUT_DIR}/ref/{file}-localizations-{suffix}.csv")
		if path.exists() and path.is_file():
			ref = pd.read_csv(path)
			assert compare_points(localizations, ref), "Test invalide pour la vérification des quadrants."
	assert True


##################################################
def test_auto_threshold():
	""" Test basique sur l'auto-seuillage avec la DLL CPU. """
	palm = PalmCPU()
	if not palm.is_valid():
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		image = open_tif(f"{INPUT_DIR}/stack.tif")
		iterations = 4
		ref = [63.634560, 63.701586, 63.058853, 62.557870, 62.474888,
			   63.374433, 63.857703, 63.368484, 62.613244, 63.833786]
		for i in range(image.shape[0]):
			res = palm.auto_threshold(image[i], roi, iterations)
			# print(f"Image {i} : {res:.6f}")
			assert is_closed(res, ref[i]), f"Le seuil pour l'image {i} vaut {res} au lieu de {ref[i]}"

# ##################################################
# def test_process_big_data(make_napari_viewer):
# 	"""
# 	Test pour le process sur des données importantes.
# 	par défaut 14min36, utilisation de CPU inférieur à 4% (1 seul coeur), Memory Usage 4Giga
# 	2930665 détections sur 22987 plans
# 	"""
# 	palm = PalmCPU()
# 	if not palm.is_valid():
# 		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
# 	else:
# 		file = "Tubulin-A647-3D-stacks_1"
# 		path = Path(f"{INPUT_DIR}/{file}.tif")
# 		if path.exists() and path.is_file():
# 			stack = open_tif(f"{INPUT_DIR}/{file}.tif")
# 			suffix = get_loc_suffix()
# 			localizations = palm.run_multithread_stack(stack, threshold, watershed, default_gaussian, sigma, theta, roi)
# 			if save_output: localizations.to_csv(f"{OUTPUT_DIR}/{file}-localizations-{suffix}.csv", index=False)
# 			assert len(localizations) > 0, "Aucune localisation trouvé"
# 		else:
# 			print_warning("Test non effectué car fichier manquant.")
# 	assert True
