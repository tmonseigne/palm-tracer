""" Fichier des tests pour l'utilisation de la DLL CPU. """

from pathlib import Path

import pytest

from palm_tracer._tests.Utils import *
from palm_tracer.Processing import Palm
from palm_tracer.Tools import open_tif

INPUT_DIR = Path(__file__).parent / "input"
OUTPUT_DIR = Path(__file__).parent / "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_palm_cpu_image():
	""" Test sur le lancement de PALM sur une frame. """
	palm = Palm()
	file = "stack"
	stack = open_tif(f"{INPUT_DIR}/{file}.tif")
	for plane in range(stack.shape[0]):
		for fit in range(6):
			suffix = get_loc_suffix(fit)

			localizations = palm.localization(stack[plane], default_threshold, default_watershed, fit, get_fit_params(fit))
			if save_output: localizations.to_csv(f"{OUTPUT_DIR}/{file}-localizations-{plane}_{suffix}.csv", index=False)

			assert len(localizations) > 0, "Aucune localisation trouvé"

			path = Path(f"{INPUT_DIR}/ref/{file}-localizations-{plane}_{suffix}.csv")
			if path.exists() and path.is_file():
				print(f"Comparaison avec : '{path}'")
				ref = pd.read_csv(path)
				assert compare_points(localizations, ref), f"Test invalide pour les paramètres {plane}_{suffix}"
	assert True


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_palm_cpu_stack():
	""" Test sur le lancement de PALM sur une pile. """
	palm = Palm()
	file = "stack"
	stack = open_tif(f"{INPUT_DIR}/{file}.tif")
	for watershed in [True, False]:
		for fit in range(6):
			suffix = get_loc_suffix(fit, watershed)

			localizations = palm.localization(stack, default_threshold, watershed, fit, get_fit_params(fit))
			if save_output: localizations.to_csv(f"{OUTPUT_DIR}/{file}-localizations-{suffix}.csv", index=False)

			assert len(localizations) > 0, "Aucune localisation trouvé"

			path = Path(f"{INPUT_DIR}/ref/{file}-localizations-{suffix}.csv")
			if path.exists() and path.is_file():
				print(f"Comparaison avec : '{path}'")
				ref = pd.read_csv(path)
				assert compare_points(localizations, ref, 0.001), f"Test invalide pour les paramètres {suffix}"
	assert True


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_palm_cpu_stack_plane_selection():
	""" Test sur le lancement de PALM sur une pile. """
	palm = Palm()
	file = "stack"
	stack = open_tif(f"{INPUT_DIR}/{file}.tif")
	suffix = get_loc_suffix()

	localizations = palm.localization(stack, default_threshold, default_watershed, default_fit, get_fit_params(default_fit), [2, 3, 4, 5, 6])
	if save_output: localizations.to_csv(f"{OUTPUT_DIR}/{file}-localizations-plane_select-{suffix}.csv", index=False)
	assert len(localizations) > 0, "Aucune localisation trouvé"
	path = Path(f"{INPUT_DIR}/ref/{file}-localizations-plane_select-{suffix}.csv")
	if path.exists() and path.is_file():
		print(f"Comparaison avec : '{path}'")
		ref = pd.read_csv(path)
		assert compare_points(localizations, ref, 0.001), f"Test invalide pour les paramètres {suffix}"


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_palm_cpu_stack_dll_check_quadrant():
	"""	Test sur le lancement de PALM sur une pile. """
	palm = Palm()
	suffix = get_loc_suffix()
	file = "stack_quadrant"
	stack = open_tif(f"{INPUT_DIR}/{file}.tif")

	localizations = palm.localization(stack, default_threshold, default_watershed, default_fit, get_fit_params(default_fit))
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
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_cpu_auto_threshold():
	""" Test basique sur l'auto-seuillage avec la DLL CPU. """
	palm = Palm()
	image = open_tif(f"{INPUT_DIR}/stack.tif")
	ref = [63.639888, 65.789447, 63.192296, 64.375352, 63.954150,
		   63.400043, 66.521994, 63.373237, 62.515444, 63.866017]
	for i in range(image.shape[0]):
		res = palm.auto_threshold(image[i], get_fit_params(0))
		# print(f"Image {i} : {res:.6f} VS {ref[i]:.6f}")
		assert is_closed(res, ref[i]), f"Le seuil pour l'image {i} vaut {res} au lieu de {ref[i]}"


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_tracking():
	"""Test basique sur le tracking."""
	palm = Palm()
	file = "stack"
	for watershed in [True, False]:
		for fit in range(6):
			suffix = get_loc_suffix(fit, watershed)
			suffix_trc = suffix + "-" + get_trc_suffix()

			path = Path(f"{INPUT_DIR}/ref/{file}-localizations-{suffix}.csv")
			if path.exists() and path.is_file():
				localizations = pd.read_csv(path)
				tracks = palm.tracking(localizations, max_distance, min_life, decrease, cost_birth)
				if save_output: tracks.to_csv(f"{OUTPUT_DIR}/{file}-tracking-{suffix_trc}.csv", index=False)

				assert len(tracks) > 0, "Aucun Tracking trouvé"

				path = Path(f"{INPUT_DIR}/ref/{file}-tracking-{suffix_trc}.csv")
				if path.exists() and path.is_file():
					print(f"Comparaison avec : '{path}'")
					ref = pd.read_csv(path)
					assert compare_points(tracks, ref, group_cols=["Track"]), f"Test invalide pour les paramètres {suffix_trc}"
			else:
				print_warning(f"Fichier de localisations '{path}' indisponible.")
	assert True
