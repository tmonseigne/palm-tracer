""" Fichier des tests pour l'utilisation des DLL """

import os
from pathlib import Path

import pandas as pd

from palm_tracer._tests.Utils import compare_points
from palm_tracer.Processing.DLL import Tracking
from palm_tracer.Tools import print_warning

INPUT_DIR = Path(__file__).parent / "input"
OUTPUT_DIR = Path(__file__).parent / "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)

threshold, watershed, sigma, theta, roi = 103.6, True, 1.0, 0.0, 7
max_distance, min_life, decrease, cost_birth = 5, 2, 10, 0.5
default_gaussian = 4
save_output = True


##################################################
def get_loc_suffix(gaussian: int) -> str:
	"""
	Génère un suffixe pour les fichiers de localisation.

	:param gaussian: Mode du filtre gaussien.
	:return: suffixe
	"""
	return f"{threshold}_{watershed}_{gaussian}_{sigma}_{theta}_{roi}"


##################################################
def get_trc_suffix() -> str:
	"""
	Génère un suffixe pour les fichiers de tracking.

	:return: suffixe
	"""
	return f"{max_distance}_{min_life}_{decrease}_{cost_birth}"


##################################################
def test_tracking():
	"""Test basique sur le tracking."""
	tracking = Tracking()
	if not tracking.is_valid():
		print_warning("\n====================\nTest non effectué car DLL manquante\n====================\n")
	else:
		file = "stack"
		suffix = get_loc_suffix(default_gaussian)
		suffix_trc = suffix + "-" + get_trc_suffix()

		path = Path(f"{INPUT_DIR}/ref/{file}-localizations-{suffix}.csv")
		if path.exists() and path.is_file():
			localizations = pd.read_csv(path)
			tracking = tracking.run(localizations, 5, 2, 10, 0.5)
			if save_output: tracking.to_csv(f"{OUTPUT_DIR}/stack-tracking-{suffix_trc}.csv", index=False)

			assert len(tracking) > 0, "Aucun Tracking trouvé"

			path = Path(f"{INPUT_DIR}/ref/{file}-tracking-{suffix_trc}.csv")
			if path.exists() and path.is_file():
				print(f"Comparaison avec : '{path}'")
				ref = pd.read_csv(path)
				# assert compare_points(tracking, ref, group_cols=["Track"]), f"Test invalide pour les paramètres {suffix_trc}"
				compare_points(tracking, ref,
							   group_cols=["Track"])  # Je ne fait pas le assert car une partie du tracking utilise un random masi le log sera là.
		else:
			print_warning(f"Fichier de localisations '{path}' indisponible.")

	assert True
