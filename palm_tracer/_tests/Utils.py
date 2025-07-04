import os
import platform
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

from palm_tracer.Tools import FileIO, print_error, print_success, print_warning

INPUT_DIR = Path(__file__).parent / "input"
default_threshold, default_watershed, sigma, theta, roi = 103.6, True, 1.0, 0.0, 7
max_distance, min_life, decrease, cost_birth = 5, 2, 10, 0.5
default_fit = 4
save_output = True


##################################################
def is_headless_macos():
	return platform.system() == "Darwin" and not os.environ.get("DISPLAY") and os.environ.get("CI") == "true"


##################################################
def is_not_dll_friendly():
	return platform.system() != "Windows"


##################################################
def get_loc_suffix(gaussian: int = default_fit, watershed: bool = default_watershed, threshold: float = default_threshold) -> str:
	"""
	Génère un suffixe pour les fichiers de localisation.

	:param gaussian: Mode du filtre gaussien.
	:param watershed: Mode du watershed.
	:param threshold: Seuil.
	:return: suffixe
	"""
	return f"{threshold}_{watershed}_{gaussian}_{sigma}_{theta}_{roi}"


##################################################
def get_fit_params(fit: int) -> np.ndarray:
	if fit == 0: return np.array([roi], dtype=np.float64)
	if fit != 5: return np.array([roi, sigma, 2 * sigma, theta], dtype=np.float64)
	calib = FileIO.open_calibration_mat(f"{INPUT_DIR}/calibration.mat")
	sx, sy, sz = calib["coeff"].shape[:3]
	return np.concatenate([np.array([roi, sx, sy, sz, calib["z0"], calib["dz"]], dtype=np.float64), calib["coeff"].flatten()])
	# np.random.seed(42)
	# shape = [roi, 16, 16, 297, 0, 10]  # les premiers éléments
	# nb_random = 16 * 16 * 297 * 64
	# coeff = np.random.uniform(low=1e-8, high=1e-4, size=nb_random)
	# coeff = np.asfortranarray(np.load("input/coefficients.npy")) # en colonne major comme matlab
	# return np.concatenate([np.array(shape, dtype=np.float64), coeff.flatten()])


##################################################
def get_trc_suffix() -> str:
	"""
	Génère un suffixe pour les fichiers de tracking.

	:return: suffixe
	"""
	return f"{max_distance}_{min_life}_{decrease}_{cost_birth}"


##################################################
def is_closed(a: float, b: float, tol: float = 1e-5) -> bool:
	"""
	Vérifie que deux valeurs flottantes sont proche avec une tolérance.

	:param a: Première valeur.
	:param b: Seconde valeur.
	:param tol: tolérance (par défaut 0.00001)
	:return: Vrai si les deux valeurs sont proches
	"""

	return np.abs(a - b) <= tol


##################################################
def compare_points(a: pd.DataFrame, b: pd.DataFrame, tol: float = 1e-5,
				   group_cols: Optional[list[str]] = None, compare_cols: Optional[list[str]] = None) -> bool:
	"""
	Compare deux DataFrames de localisation en tenant compte de la proximité spatiale.

	Laisser par défaut les colonnes pour des fichiers de localisation issues de plan-tracer python.

	Changer les colonnes à comparer si la localisaiton viens de Metamorph.
		["X", "Y", "Integrated Intensity", "Sigma X", "Sigma Y", "Theta", "MSE XY", "MSE Z", "Pair Distance"]

	Changer les colonnes pour le Tracking
		sort = ["Track"]
		group = ["Track"]
		compare = TRACK_FILE_COLS

	:param a: Premier DataFrame.
	:param b: Second DataFrame.
	:param tol: Tolérance pour la comparaison des valeurs numériques. Defaults to 1e-5.
	:param group_cols: Colonne de regroupement (pour séparer les plan et les canaux par exemple).
	:param compare_cols: Colonnes à comparer. Defaults toutes les colonnes de localisations
	:return: True si les fichiers sont similaires selon les critères définis, False sinon.
	"""
	if group_cols is None: group_cols = ["Plane", "Channel"]
	if compare_cols is None: compare_cols = list(set(a.columns) - set(group_cols))
	res = True

	# Comparaison des tailles
	if len(a) != len(b):
		print_warning("les fichiers n'ont pas le même nombre d'entrées.")
		res = False

	# Vérification de la présence des colonnes requises
	missing_a = [col for col in compare_cols if col not in a.columns]
	missing_b = [col for col in compare_cols if col not in b.columns]
	if missing_a or missing_b:
		print_error(f"Colonnes manquantes : {missing_a + missing_b}")
		return False

	total_points = 0
	exact_matches = 0

	# Parcours par plan et channel
	for group_values, group_a in a.groupby(group_cols):
		# Si group_cols contient une seule colonne, group_values sera un scalaire, sinon un tuple
		group_values = (group_values,) if isinstance(group_values, (int, float, str)) else group_values
		# Construire un masque dynamique pour filtrer `b`
		mask = (b[col] == val for col, val in zip(group_cols, group_values))
		group_b = b.loc[pd.concat(mask, axis=1).all(axis=1)]  # Conserver les lignes où toutes les conditions sont vraies
		group_a = group_a.reset_index(drop=True)
		group_b = group_b.reset_index(drop=True)
		if len(group_a) != len(group_b):
			print_warning(f"{len(group_a)} points in A, {len(group_b)} points in B pour { {col: int(val) for col, val in zip(group_cols, group_values)} }.")

		if group_b.empty:
			print_warning(f"Pas de correspondance pour {dict(zip(group_cols, group_values))} dans B.")
			continue

		# Utilisation d'un KDTree pour accélérer la recherche des plus proches voisins
		tree = cKDTree(group_b[["X", "Y", "Z"]].values)
		distances, indices = tree.query(group_a[["X", "Y", "Z"]].values, k=1)

		# Suivi des indices déjà utilisés pour garantir une correspondance unique
		used_indices = set()
		unique_matches = []
		for i, idx in enumerate(indices):
			if idx not in used_indices:
				unique_matches.append((i, idx))
				used_indices.add(idx)

		matched_a_indices, matched_b_indices = zip(*unique_matches) if unique_matches else ([], [])
		matched_a_indices, matched_b_indices = list(matched_a_indices), list(matched_b_indices)
		# Création des DataFrames correspondants
		matched_a = group_a.iloc[matched_a_indices].reset_index(drop=True)
		matched_b = group_b.iloc[matched_b_indices].reset_index(drop=True)

		# Parcours des lignes dans a
		for i, row_a in matched_a.iterrows():
			row_b = matched_b.iloc[i]  # Récupération du point le plus proche

			total_points += 1  # Un point est comparé donc incrémentaiton du compteur
			diff = {}  # Dictionnaire de différence
			exact_match = True  # Le point est identique

			# Vérification des correspondances exactes
			for col in compare_cols:
				if not np.isclose(row_a[col], row_b[col], atol=tol):
					diff[col] = (row_a[col], row_b[col])
					exact_match = False

			# S'il y a eu des différences
			if diff:
				print_warning(f"Différences pour Point ({row_a['X']:.2f}, {row_a['Y']:.2f}, {row_a['Z']:.2f}) :")
				for key, (val_a, val_b) in diff.items():
					print_warning(f"  {key}: {val_a:.5f} vs {val_b:.5f}")

			if exact_match: exact_matches += 1  # Incrémentation du compteur

		# Gestion des points non appariés
		non_matched_a = group_a.drop(index=matched_a_indices, errors="ignore")
		non_matched_b = group_b.drop(index=matched_b_indices, errors="ignore")

		if not non_matched_a.empty:
			print_warning(f"Points supplémentaires dans A pour { {col: int(val) for col, val in zip(group_cols, group_values)} } :")
			for _, row in non_matched_a.iterrows():
				print_warning(f"({row['X']:.2f}, {row['Y']:.2f}, {row['Z']:.2f}) : {row['Integrated Intensity']:.2f}")

		if not non_matched_b.empty:
			print_warning(f"Points supplémentaires dans B pour  { {col: int(val) for col, val in zip(group_cols, group_values)} } :")
			for _, row in non_matched_b.iterrows():
				print_warning(f"({row['X']:.2f}, {row['Y']:.2f}, {row['Z']:.2f}) : {row['Integrated Intensity']:.2f}")

	if total_points > 0:
		exact_match_ratio = exact_matches / total_points * 100
		msg = f"Comparaison terminée : {total_points} Points comparés, {exact_matches} Points identiques ({exact_match_ratio:.2f}%)"
		if total_points == exact_matches: print_success(msg)
		else: print_warning(msg)

		res = exact_matches == total_points

	return res
