import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

from palm_tracer.Tools import print_error, print_warning


##################################################
def is_closed(value: float, ref: float, tol: float = 1e-5):
	return (np.abs(value) - ref) <= tol


##################################################
def compare_points(a: pd.DataFrame, b: pd.DataFrame, tol: float = 1e-5,
				   sort_cols: list[str] | None = None, compare_cols: list[str] | None = None, group_cols: list[str] | None = None) -> bool:
	"""
	Compare deux DataFrames de localisation en tenant compte de la proximité spatiale.

	Laisser par défaut les colonnes pour des fichiers de localisation issues de plan-tracer python.

	Changer les colonnes à comparer si la localisaiton viens de Metamorph.
		["X", "Y", "Integrated Intensity", "Sigma X", "Sigma Y", "Theta", "MSE Gauss", "MSE Z", "Pair Distance"]

	Changer les colonnes pour le Tracking
		sort = ["Plane", "X", "Y", "Z"]
		group = ["Plane"]
		compare = ["X", "Y", "Integrated Intensity", "Pair Distance", "???"]

	:param a: Premier DataFrame.
	:param b: Second DataFrame.
	:param tol: Tolérance pour la comparaison des valeurs numériques. Defaults to 1e-5.
	:param sort_cols: Tri initial des lignes. Defaults ["Plane", "Channel", "X", "Y", "Z"]
	:param compare_cols: Colonnes à comparer. Defaults toutes les colonnes de localisations
	:param group_cols: Colonne de regroupement (pour séparer les plan et les canaux par exemple).
	:return: True si les fichiers sont similaires selon les critères définis, False sinon.
	"""
	if sort_cols is None:
		sort_cols = ["Plane", "Channel", "X", "Y", "Z"]

	if compare_cols is None:
		compare_cols = ["X", "Y", "Z", "Integrated Intensity", "Sigma X", "Sigma Y", "Theta",
						"MSE Gauss", "MSE Z", "Pair Distance", "Intensity 0", "Intensity Offset",
						"Intensity", "Surface"]

	if group_cols is None:
		group_cols = ["Plane", "Channel"]

	res = True

	# Comparaison des tailles
	if len(a) != len(b):
		print_warning("les fichiers n'ont pas le même nombre d'entrées.")
		res = False

	# Vérification de la présence des colonnes requises
	missing_a = [col for col in sort_cols + compare_cols if col not in a.columns]
	missing_b = [col for col in sort_cols + compare_cols if col not in b.columns]
	if missing_a or missing_b:
		print_error(f"Colonnes manquantes : {missing_a + missing_b}")
		return False

	# Tri des DataFrames
	a = a.sort_values(sort_cols).reset_index(drop=True)
	b = b.sort_values(sort_cols).reset_index(drop=True)

	total_points = 0
	exact_matches = 0

	# Parcours par plan et channel
	for (plane, channel), group_a in a.groupby(group_cols):
		group_b = b[(b["Plane"] == plane) & (b["Channel"] == channel)]
		group_a = group_a.reset_index(drop=True)
		group_b = group_b.reset_index(drop=True)
		print(f"Plane {plane}, Channel {channel} : {len(group_a)} points in A, {len(group_b)} points in B.")

		if group_b.empty:
			print_warning(f"Pas de correspondance pour Plane={plane}, Channel={channel} dans B.")
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
			print_warning(f"Points supplémentaires dans A pour Plane={plane}, Channel={channel} :")
			for _, row in non_matched_a.iterrows():
				print_warning(f"({row['X']:.2f}, {row['Y']:.2f}, {row['Z']:.2f}) : {row['Integrated Intensity']:.2f}")

		if not non_matched_b.empty:
			print_warning(f"Points supplémentaires dans B pour Plane={plane}, Channel={channel} :")
			for _, row in non_matched_b.iterrows():
				print_warning(f"({row['X']:.2f}, {row['Y']:.2f}, {row['Z']:.2f}) : {row['Integrated Intensity']:.2f}")

	if total_points > 0:
		exact_match_ratio = exact_matches / total_points * 100

		print(f"Comparaison terminée :")
		print(f"  Points comparés : {total_points}")
		print(f"  Points identiques : {exact_matches} ({exact_match_ratio:.2f}%)")

		res = exact_matches == total_points

	return res
