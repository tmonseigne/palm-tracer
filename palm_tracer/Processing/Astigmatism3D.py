"""Fournit les fonctions de calibration et d'estimation de la position axiale par astigmatisme 3D."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

from palm_tracer.Tools import Ui


##################################################
def z_from_planes(planes: np.ndarray, z_min: float, z_max: float) -> np.ndarray:
	"""
	Estime une position Z (en unités physiques) à partir d'indices de plans.

	Les indices de plans sont supposés répartis linéairement entre ``z_min`` et ``z_max`` :
		- ``min(planes)``  ⇾ ``z_min``
		- ``max(planes)``  ⇾ ``z_max``
		- valeurs intermédiaires interpolées linéairement.

	:param planes: Tableau des indices de plans (entiers). Peut être de n'importe quelle forme.
	:param z_min: Valeur minimale de Z correspondant au premier plan.
	:param z_max: Valeur maximale de Z correspondant au dernier plan.

	:return: Tableau NumPy, de même forme que ``planes``, contenant les valeurs de Z estimées.
	"""
	planes = np.asarray(planes, dtype=np.float64)  # passage en flottant
	p_min, p_max = planes.min(), planes.max()  # Récupération des min/max
	if p_min == p_max: return np.full_like(planes, fill_value=0.5 * (z_min + z_max), dtype=np.float64)  # Cas dégénéré : un seul plan
	return z_min + (planes - p_min) * (z_max - z_min) / (p_max - p_min)  # Interpolation linéaire


##################################################
def z_from_step(n_planes: int, z_step: float, center: bool = True) -> np.ndarray:
	"""
	Estime les positions Z (en unités physiques) pour une pile de plans équidistants.

	:param n_planes: Nombre total de plans. Doit être strictement positif.
	:param z_step: Distance entre deux plans consécutifs (même unité que la sortie). Doit être strictement positive.
	:param center: Si ``True``, centre la pile autour de 0. Sinon, démarre à 0.
	:return: Tableau NumPy contenant les valeurs de Z estimées.
	"""
	# Indices centrés : impair ⇾ un plan à 0 ; pair ⇾ 0 entre les deux plans centraux.
	if center: indices = np.arange(n_planes, dtype=np.float64) - 0.5 * (n_planes - 1)
	# Indices classiques : plan 0 à 0, puis positifs.
	else: indices = np.arange(n_planes, dtype=np.float64)
	return indices * float(z_step)


##################################################
def remove_multi_beads(loc: pd.DataFrame) -> pd.DataFrame:
	"""
	Supprime les localisations multiples par plan en conservant, pour chaque plan ambigu,
	la localisation la plus proche de la position moyenne estimée à partir des plans ne contenant qu'une seule localisation.

	Le principe est le suivant :
		- si un plan ne contient qu'une seule localisation, celle-ci est conservée ;
		- si un plan contient plusieurs localisations, seule la localisation la plus proche de la moyenne ``(X, Y)``;
		- si aucun plan ne contient une unique localisation, la désambiguïsation n'est pas possible de manière fiable et le DataFrame d'origine est renvoyé.

	:param loc: DataFrame contenant au minimum les colonnes ``X``, ``Y`` et ``Plane``.
	:return: DataFrame filtré avec au plus une localisation par plan.
	"""
	if loc.empty: return loc
	required_columns = {"X", "Y", "Plane"}
	if not required_columns.issubset(loc.columns):
		Ui.print_warning("Not all valid columns in localizations. Unable to remove ambiguous localizations reliably.")
		return loc

	# Cas d'un fichier avec des billes identifiées, on prend la première, c'est plus simple.
	if "Bead" in loc.columns: return loc[loc["Bead"] == loc.loc[0, "Bead"]]

	counts_per_plane = loc.groupby("Plane").size()  # .				 Nombre de localisations par plan.
	single_planes = counts_per_plane[counts_per_plane == 1].index  # Plans non ambigus : une seule localisation.
	multi_planes = counts_per_plane[counts_per_plane > 1].index  # . Plans ambigus : plusieurs localisations.
	if len(multi_planes) == 0: return loc  # .						 Rien à faire si tous les plans ont déjà une unique localisation.

	# Si aucun plan n'est non ambigu, on ne peut pas estimer une position de référence fiable.
	if len(single_planes) == 0:
		Ui.print_warning("All planes contain multiple localizations. Unable to remove ambiguous localizations reliably.")
		return loc

	# Moyenne de référence calculée sur les plans non ambigus.
	single_loc = loc[loc["Plane"].isin(single_planes)]
	x_mean, y_mean = float(single_loc["X"].mean()), float(single_loc["Y"].mean())

	selected_rows = [single_loc]  # On conserve directement les plans avec une seule localisation.

	# Pour chaque plan ambigu, on garde la localisation la plus proche de la moyenne.
	for plane in multi_planes:
		plane_loc = loc[loc["Plane"] == plane]
		dist2 = (plane_loc["X"] - x_mean) ** 2 + (plane_loc["Y"] - y_mean) ** 2
		best_index = dist2.idxmin()
		selected_rows.append(loc.loc[[best_index]])

	res = pd.concat(selected_rows, axis=0)
	return res.sort_values("Plane").reset_index(drop=True)


##################################################
def sigma_model(model: np.ndarray, z: np.ndarray | float, pixel_size: float, sampling: float = 1) -> np.ndarray | float:
	"""
	Modèle astigmatique sigma(z).

	:param model: Modèle astigmatique de forme (2, 5) : paramètres X puis Y, chaque ligne = [Z0, W, C3, C4, A].
	:param z: Ensemble des Z à utiliser pour trouver le sigma en fonction du modèle.
	:param pixel_size: Taille des pixels en nanomètres.
	:param sampling: Facteur d'agrandissement (les fichiers de localisation sauvegardés le sont avant agrandissement donc à laisser à 1).
	:return: Tableau NumPy contenant les valeurs de sigma en fonction de Z pour le modèle.
	"""
	z0, w, c3, c4, a = model

	u = (z - z0) / w
	u2 = u * u

	poly = 1.0 + u2 + c3 * (u2 * u) + c4 * (u2 * u2)
	g = np.sqrt(np.maximum(0.0, poly))

	return (sampling / pixel_size) * a * g


##################################################
def model_validity(dataset: np.ndarray, model: np.ndarray, pixel_size: float, sampling: float = 1) -> dict:
	"""
	Calcule des métriques d'erreur entre (Sx, Sy) observés et (Sx, Sy) prédits par le modèle aux mêmes positions Z.

	- RMSE (*Root Mean Square Error*) : racine de la moyenne des erreurs quadratiques.
	  Mesure l'erreur typique en pénalisant davantage les grandes erreurs.
	  Modèle parfait : RMSE = 0 (en pratique, proche de l'écart-type du bruit si les données sont bruitées).

	- MAE (*Mean Absolute Error*) : moyenne des erreurs absolues.
	  Mesure l'erreur moyenne en valeur absolue, moins sensible aux outliers que le RMSE.
	  Modèle parfait : MAE = 0 (en pratique, proche de l'amplitude moyenne du bruit).

	- R² (*coefficient de détermination*) : fraction de la variance des observations expliquée par le modèle.
	  Modèle parfait : R² = 1.0. Un R² proche de 0 indique que le modèle n'explique pas mieux que la moyenne.
	  Note : R² peut être négatif si le modèle est très mauvais.

	:param dataset: Tableau (N, 3) contenant les colonnes [Sx, Sy, Z] (sigmas en pixels, Z en unités cohérentes avec le modèle).
	:param model: Modèle astigmatique de forme (2, 5) : paramètres X puis Y, chaque ligne = [Z0, W, C3, C4, A].
	:param pixel_size: Taille pixel dans les mêmes unités que Z (par ex. nm), utilisée dans le calcul de sigma.
	:param sampling: Facteur d'échantillonnage (adimensionnel) appliqué dans le calcul de sigma (laisser à 1).
	:return: Dictionnaire de métriques : RMSE/MAE (en pixels) et R² (adimensionnel) pour X, Y et global.
	"""
	sx_obs, sy_obs, z = dataset[:, 0], dataset[:, 1], dataset[:, 2]
	sx_hat, sy_hat = sigma_model(model[0], z, pixel_size, sampling), sigma_model(model[1], z, pixel_size, sampling)
	ex, ey = sx_hat - sx_obs, sy_hat - sy_obs

	rmse_x, rmse_y = float(np.sqrt(np.mean(ex * ex))), float(np.sqrt(np.mean(ey * ey)))
	rmse_xy = float(np.sqrt(np.mean(np.concatenate([ex, ey]) ** 2)))

	mae_x, mae_y = float(np.mean(np.abs(ex))), float(np.mean(np.abs(ey)))

	# R² (sur sigma) : utile pour un score "qualité de l'ajustement"
	def r2(y, yhat):
		"""Basic R2 Compute."""
		ss_res, ss_tot = np.sum((y - yhat) ** 2), np.sum((y - np.mean(y)) ** 2)
		return float(1.0 - ss_res / ss_tot) if ss_tot > 0 else float("nan")

	return {
			"rmse_x": rmse_x, "rmse_y": rmse_y, "rmse_xy": rmse_xy,
			"mae_x":  mae_x, "mae_y": mae_y,
			"r2_x":   r2(sx_obs, sx_hat), "r2_y": r2(sy_obs, sy_hat)
			}


##################################################
def model_projection_validity(dataset: np.ndarray, model: np.ndarray, z_max: float, pixel_size: float, n_curve: int = 5000, sampling: float = 1) -> dict:
	"""
	Évalue la validité d'un modèle astigmatique pour l'estimation de Z en projetant les observations (SigmaX, SigmaY) sur la courbe modèle.

	Le Z estimé correspond au point de la courbe le plus proche dans le plan (SigmaX, SigmaY).
	Les métriques retournées quantifient à la fois la précision axiale et la cohérence des données avec le modèle.

	- RMSE_Z (*Root Mean Square Error*) : Erreur quadratique moyenne sur Z. Mesure de la précision axiale typique.
	  Modèle parfait (sans bruit) : RMSE_Z = 0.

	- MAE_Z (*Mean Absolute Error*) : Erreur moyenne absolue sur Z, plus robuste aux outliers que le RMSE.
	  Modèle parfait : MAE_Z = 0.

	- P95_Z : 95e percentile de ΔZ. Indique une borne haute réaliste de l'erreur axiale pour la majorité des localisations.

	- Bias_Z : Moyenne de ΔZ. Reflète un biais systématique du modèle.
	  Modèle parfait : Bias_Z = 0.

	- Std_Z : Écart-type de ΔZ. Mesure de la dispersion de l'erreur axiale autour du biais.

	- Mean_dist_px : Distance moyenne (en pixels) des points observés à la courbe modèle dans l'espace (SigmaX, SigmaY).
	  Sert de score de cohérence / confiance.

	- P95_dist_px : 95e percentile de la distance à la courbe. Utile pour définir un seuil de rejet des estimations peu fiables.

	- slope_mean : Pente moyenne de la courbe σx(z) - σy(z) en pixel par nanomètres.

	:param dataset: Tableau (N, 3) contenant les colonnes [SigmaX, SigmaY, Z] (sigmas en pixels, Z dans des unités cohérentes avec le modèle).
	:param model: Modèle astigmatique de forme (2, 5) : paramètres X puis Y, chaque ligne = [Z0, W, C3, C4, A].
	:param z_max: Valeur maximale de Z (le modèle est évalué sur [-z_max, +z_max]).
	:param pixel_size: Taille du pixel dans les mêmes unités que Z (ex. nm).
	:param n_curve: Nombre de points d'échantillonnage de la courbe modèle en Z. Doit être suffisamment grand pour éviter une quantification de Z.
	:param sampling: Facteur d'échantillonnage (adimensionnel) utilisé dans le modèle de sigma (généralement égal à 1).
	:return: Dictionnaire de métriques décrivant la précision axiale (en unités de Z) et la cohérence des données avec le modèle (distances en pixels).
	"""
	sx_obs, sy_obs, z_true = dataset[:, 0], dataset[:, 1], dataset[:, 2]

	z_curve = np.linspace(-z_max, z_max, n_curve, dtype=np.float64)
	sx_curve = sigma_model(model[0], z_curve, pixel_size, sampling)
	sy_curve = sigma_model(model[1], z_curve, pixel_size, sampling)
	curve = np.column_stack((sx_curve, sy_curve))
	ds = np.gradient(sx_curve - sy_curve, z_curve)

	tree = cKDTree(curve)
	dist, idx = tree.query(np.column_stack((sx_obs, sy_obs)), k=1)

	z_est = z_curve[idx]
	dz = z_est - z_true

	return {
			# Métriques en nanomètres
			"rmse_z":     float(np.sqrt(np.mean(dz * dz))),
			"mae_z":      float(np.mean(np.abs(dz))),
			"p95_abs_z":  float(np.percentile(np.abs(dz), 95)),
			"bias_z":     float(np.mean(dz)),
			"std_z":      float(np.std(dz)),
			# Distance en pixel
			"mean_dist":  float(np.mean(dist)),
			"p95_dist":   float(np.percentile(dist, 95)),
			# Pente
			"slope_mean": float(np.mean(np.abs(ds)))
			}


##################################################
def find_model_center(model: np.ndarray, z_max: float, pixel_size: float) -> float:
	"""
	Recherche la position axiale pour laquelle les deux sigmas astigmatiques sont les plus proches.

	La méthode balaie uniformément l'intervalle couvert par ``z`` afin de détecter :
		- soit un zéro exact de la différence entre les deux courbes de sigma ;
		- soit un changement de signe, auquel cas une bissection locale est appliquée ;
		- soit, à défaut, la position minimisant la valeur absolue de cette différence.

	:param model: Modèle astigmatique de forme (2, 5) : paramètres X puis Y, chaque ligne = [Z0, W, C3, C4, A].
	:param z_max: Valeur maximale de Z (le modèle est évalué sur [-z_max, +z_max]).
	:param pixel_size: Taille du pixel dans les mêmes unités que Z (ex. nm).
	:return: Position axiale estimée du centre astigmatique.
	"""
	z_min = -z_max
	n_samples, n_bisect = 2048, 64

	z_values: np.ndarray = np.linspace(z_min, z_max, n_samples, dtype=float)
	delta_values: np.ndarray = sigma_model(model[0], z_values, pixel_size, 1.0) - sigma_model(model[1], z_values, pixel_size, 1.0)

	# Meilleure solution brute au sens |delta|.
	abs_delta = np.abs(delta_values)
	best_index = int(np.argmin(abs_delta))
	best_z, best_d = z_values[best_index], abs_delta[best_index]

	# Recherche d'un zéro exact.
	zero_indices = np.flatnonzero(delta_values == 0.0)
	if zero_indices.size > 0: return z_values[int(zero_indices[0])]

	# Recherche d'un changement de signe entre deux échantillons successifs.
	sign_change_indices = np.flatnonzero((delta_values[:-1] < 0.0) != (delta_values[1:] < 0.0))
	if sign_change_indices.size == 0: return best_z

	# On affine le premier intervalle contenant un changement de signe.
	idx = int(sign_change_indices[0])
	left_z, right_z, left_d = z_values[idx], z_values[idx + 1], delta_values[idx]

	# def delta(z: float) -> float: return sigma_model(model[0], z, pixel_size, 1.0) - sigma_model(model[1], z, pixel_size, 1.0)

	for i in range(n_bisect):
		mid_z = 0.5 * (left_z + right_z)
		mid_d = sigma_model(model[0], mid_z, pixel_size, 1.0) - sigma_model(model[1], mid_z, pixel_size, 1.0)

		abs_mid_d = abs(mid_d)
		if abs_mid_d < best_d: best_d, best_z = abs_mid_d, mid_z
		if mid_d == 0.0: return mid_z
		if (left_d < 0.0) != (mid_d < 0.0): right_z = mid_z
		else: left_z, left_d = mid_z, mid_d

	return best_z
