""" Fichier des tests pour l'utilisation de la DLL CPU. """

import os
from pathlib import Path

from palm_tracer.Processing.DLL import PalmCPU, PalmGPU
from palm_tracer.Tools import open_tif, print_warning

INPUT_DIR = Path(__file__).parent / "input"
OUTPUT_DIR = Path(__file__).parent / "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)

threshold, watershed, sigma, theta, roi = 340.6, True, 1.0, 0.0, 7
max_distance, min_life, decrease, cost_birth = 5, 2, 10, 0.5
gaussian = 4
save_output = True

##################################################
def get_loc_suffix() -> str:
	"""
	Génère un suffixe pour les fichiers de localisation.

	:return: suffixe
	"""
	return f"{threshold}_{watershed}_{gaussian}_{sigma}_{theta}_{roi}"


##################################################
def test_process_cpu_big_data(make_napari_viewer):
	"""
	Test pour le process sur des données importantes.
	par défaut 14min36, utilisation de CPU inférieur à 4% (1 seul coeur), Memory Usage 4Giga
	2930665 détections sur 22987 plans
	"""
	palm = PalmCPU()
	if not palm.is_valid():
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		file = "Tubulin-A647-3D-stacks_1"
		path = Path(f"{INPUT_DIR}/{file}.tif")
		if path.exists() and path.is_file():
			stack = open_tif(f"{INPUT_DIR}/{file}.tif")
			suffix = get_loc_suffix()
			localizations = palm.run(stack, threshold, watershed, gaussian, sigma, theta, roi)
			if save_output: localizations.to_csv(f"{OUTPUT_DIR}/{file}-localizations-{suffix}.csv", index=False)
			assert len(localizations) > 0, "Aucune localisation trouvé"
		else:
			print_warning("Test non effectué car fichier manquant.")
	assert True

##################################################
def test_process_gpu_big_data(make_napari_viewer):
	"""
	Test pour le process sur des données importantes.
	par défaut 14min36, utilisation de CPU inférieur à 4% (1 seul coeur), Memory Usage 4Giga
	2930665 détections sur 22987 plans
	"""
	palm = PalmGPU()
	if not palm.is_valid():
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		file = "Tubulin-A647-3D-stacks_1"
		path = Path(f"{INPUT_DIR}/{file}.tif")
		if path.exists() and path.is_file():
			stack = open_tif(f"{INPUT_DIR}/{file}.tif")
			suffix = get_loc_suffix()
			localizations = palm.run(stack, threshold, watershed, gaussian, sigma, theta, roi)
			if save_output: localizations.to_csv(f"{OUTPUT_DIR}/{file}-localizations-{suffix}.csv", index=False)
			assert len(localizations) > 0, "Aucune localisation trouvé"
		else:
			print_warning("Test non effectué car fichier manquant.")
	assert True
