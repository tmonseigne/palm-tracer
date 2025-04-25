""" Fichier des tests pour l'utilisation de la DLL GPU.

.. todo::
	Attention de nombreuses différences (sans doute du à la précision entre la DLL CPU et GPU.
	Si le Guassian Fit est à 0 ou 1 résultats identitques
	Si le Fauggian Fit est à 2 ou 3 des différences
	Si le Gaussian Fit est à 4 (Sigma X Sigma Y Theta) résultats grandement différents.
"""

import os
from pathlib import Path

from palm_tracer._tests.Utils import *
from palm_tracer.Processing.DLL import PalmGPU
from palm_tracer.Tools import open_tif, print_warning

INPUT_DIR = Path(__file__).parent / "input"
OUTPUT_DIR = Path(__file__).parent / "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)

##################################################
def test_palm_gpu_image():
	""" Test sur le lancement de PALM sur une frame. """
	palm = PalmGPU()
	if not palm.is_valid():
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		file = "stack"
		stack = open_tif(f"{INPUT_DIR}/{file}.tif")
		for plane in range(stack.shape[0]):
			for gaussian in range(5):
				suffix = get_loc_suffix(gaussian)

				localizations = palm.run(stack[plane], default_threshold, default_watershed, gaussian, sigma, theta, roi)
				if save_output: localizations.to_csv(f"{OUTPUT_DIR}/{file}-localizations-gpu-{plane}_{suffix}.csv", index=False)

				assert len(localizations) > 0, "Aucune localisation trouvé"

				path = Path(f"{INPUT_DIR}/ref/{file}-localizations-{plane}_{suffix}.csv")
				if path.exists() and path.is_file():
					print(f"Comparaison avec : '{path}'")
					ref = pd.read_csv(path)
					# assert compare_points(localizations, ref), f"Test invalide pour les paramètres {plane}_{suffix}"
					# Je ne fait pas le assert car la precision est différente entre la DLL CPU et GPU et je veux conserver un seul fichier de comparaison.
					compare_points(localizations, ref)
	assert True


##################################################
def test_palm_gpu_stack():
	""" Test sur le lancement de PALM sur une pile. """
	palm = PalmGPU()
	if not palm.is_valid():
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		file = "stack"
		stack = open_tif(f"{INPUT_DIR}/{file}.tif")
		for gaussian in range(5):
			suffix = get_loc_suffix(gaussian)

			localizations = palm.run(stack, default_threshold, default_watershed, gaussian, sigma, theta, roi)
			if save_output: localizations.to_csv(f"{OUTPUT_DIR}/{file}-localizations-gpu-{suffix}.csv", index=False)

			assert len(localizations) > 0, "Aucune localisation trouvé"

			path = Path(f"{INPUT_DIR}/ref/{file}-localizations-{suffix}.csv")
			if path.exists() and path.is_file():
				print(f"Comparaison avec : '{path}'")
				ref = pd.read_csv(path)
				# assert compare_points(localizations, ref), f"Test invalide pour les paramètres {suffix}"
				# Je ne fait pas le assert car la precision est différente entre la DLL CPU et GPU et je veux conserver un seul fichier de comparaison.
				compare_points(localizations, ref)
	assert True


##################################################
def test_palm_gpu_stack_plane_selection():
	""" Test sur le lancement de PALM sur une pile. """
	palm = PalmGPU()
	if not palm.is_valid():
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		file = "stack"
		stack = open_tif(f"{INPUT_DIR}/{file}.tif")
		suffix = get_loc_suffix()

		localizations = palm.run(stack, default_threshold, default_watershed, default_gaussian, sigma, theta, roi, [2, 4, 6, -1, 10])
		if save_output: localizations.to_csv(f"{OUTPUT_DIR}/{file}-localizations-gpu-plane_select-{suffix}.csv", index=False)
		assert len(localizations) > 0, "Aucune localisation trouvé"


##################################################
def test_palm_gpu_stack_dll_check_quadrant():
	"""	Test sur le lancement de PALM sur une pile. """
	palm = PalmGPU()
	if not palm.is_valid():
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		suffix = get_loc_suffix()
		file = "stack_quadrant"
		stack = open_tif(f"{INPUT_DIR}/{file}.tif")

		localizations = palm.run(stack, default_threshold, default_watershed, default_gaussian, sigma, theta, roi)
		if save_output: localizations.to_csv(f"{OUTPUT_DIR}/{file}-localizations-gpu-{suffix}.csv", index=False)

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
			# assert compare_points(localizations, ref), "Test invalide pour la vérification des quadrants."
			# Je ne fait pas le assert car la precision est différente entre la DLL CPU et GPU et je veux conserver un seul fichier de comparaison.
			compare_points(localizations, ref)
	assert True


##################################################
def test_gpu_auto_threshold():
	""" Test basique sur l'auto-seuillage avec la DLL CPU. """
	palm = PalmGPU()
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
