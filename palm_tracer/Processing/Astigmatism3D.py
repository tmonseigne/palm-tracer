""" Fichier contenant des fonctions lié à l'astigmatisme 3D (estimation de la position axiale en fonction des écart-types sur X et Y)."""
import numpy as np
from scipy.spatial import cKDTree

DLL_REQUIRED_COLS = ["Sigma X", "Sigma Y", "Z"]
MODEL_COLS = ["Z0", "W", "C3", "C4", "A"]
MODEL_ROWS = ["X", "Y"]


##################################################
def z_from_planes(planes: np.ndarray, z_min: float, z_max: float) -> np.ndarray:
	"""Estime une position Z (en unités physiques) à partir d'indices de plans.

	Les indices de plans sont supposés répartis linéairement entre ``z_min`` et ``z_max`` :
	- ``min(planes)``  -> ``z_min``
	- ``max(planes)``  -> ``z_max``
	- valeurs intermédiaires interpolées linéairement.

	:param planes: Tableau des indices de plans (entiers). Peut être de n'importe quelle forme.
	:param z_min: Valeur minimale de Z correspondant au premier plan.
	:param z_max: Valeur maximale de Z correspondant au dernier plan.

	:return: Tableau NumPy de même forme que ``planes`` contenant les valeurs de Z estimées.
	"""
	planes = np.asarray(planes, dtype=np.float64)  # passage en flottant
	p_min, p_max = planes.min(), planes.max()  # Récupération des min/max
	if p_min == p_max: return np.full_like(planes, fill_value=0.5 * (z_min + z_max), dtype=np.float64)  # Cas dégénéré : un seul plan
	return z_min + (planes - p_min) * (z_max - z_min) / (p_max - p_min)  # Interpolation linéaire


##################################################
def z_from_step(n_planes: int, z_step: float, center: bool = True) -> np.ndarray:
	"""Estime les positions Z (en unités physiques) pour une pile de plans équidistants.

	:param n_planes: Nombre total de plans. Doit être strictement positif.
	:param z_step: Distance entre deux plans consécutifs (même unité que la sortie). Doit être strictement positive.
	:param center: Si ``True``, centre la pile autour de 0. Sinon, démarre à 0.

	:return: Tableau NumPy contenant les valeurs de Z estimées.
	"""
	# Indices centrés : impair -> un plan à 0 ; pair -> 0 entre les deux plans centraux.
	if center: indices = np.arange(n_planes, dtype=np.float64) - 0.5 * (n_planes - 1)
	# Indices classiques : plan 0 à 0, puis positifs.
	else: indices = np.arange(n_planes, dtype=np.float64)
	return indices * float(z_step)


##################################################
def sigma_model(model: np.ndarray, z: np.ndarray, pixel_size: float, sampling: float) -> np.ndarray:
	"""Modèle astigmatique sigma(z).

	:param model:
	:param z:
	:param pixel_size: Taille des pixels en nanomètres.
	:param sampling: Facteur d'agrandissement (les fichiers de localisation sauvegardés, le sont avant agrandissement donc laisser à 1).
	:return:
	"""
	z0, w, c3, c4, a = model

	u = (z - z0) / w
	u2 = u * u

	poly = 1.0 + u2 + c3 * (u2 * u) + c4 * (u2 * u2)
	g = np.sqrt(np.maximum(0.0, poly))

	return (sampling / pixel_size) * a * g


##################################################
def model_validity(dataset: np.ndarray, model: np.ndarray, pixel_size: float, sampling: float) -> dict:
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

	# R² (sur sigma) : utile pour un score "qualité de fit"
	def r2(y, yhat):
		ss_res, ss_tot = np.sum((y - yhat) ** 2), np.sum((y - np.mean(y)) ** 2)
		return float(1.0 - ss_res / ss_tot) if ss_tot > 0 else float("nan")

	return {
			"rmse_x":  rmse_x,
			"rmse_y":  rmse_y,
			"rmse_xy": rmse_xy,
			"mae_x":   mae_x,
			"mae_y":   mae_y,
			"r2_x":    r2(sx_obs, sx_hat),
			"r2_y":    r2(sy_obs, sy_hat)
			}


def model_projection_validity(dataset: np.ndarray, model: np.ndarray, z_max: float, n_curve: int, pixel_size: float, sampling: float) -> dict:
	"""
	Évalue la validité d'un modèle astigmatique pour l'estimation de Z en projetant les observations (SigmaX, SigmaY) sur la courbe modèle.

	Le Z estimé correspond au point de la courbe le plus proche dans le plan (SigmaX, SigmaY).
	Les métriques retournées quantifient à la fois la précision	axiale et la cohérence des données avec le modèle.

	- RMSE_Z (*Root Mean Square Error*) : Erreur quadratique moyenne sur Z. Mesure la précision axiale typique.
	  Modèle parfait (sans bruit) : RMSE_Z = 0.

	- MAE_Z (*Mean Absolute Error*) : Erreur moyenne absolue sur Z, plus robuste aux outliers que le RMSE.
	  Modèle parfait : MAE_Z = 0.

	- P95_|Z| : 95e percentile de |ΔZ|. Indique une borne haute réaliste de l'erreur axiale pour la majorité des localisations.

	- Bias_Z : Moyenne de ΔZ. Reflète un biais systématique du modèle.
	  Modèle parfait : Bias_Z = 0.

	- Std_Z : Écart-type de ΔZ. Mesure la dispersion de l'erreur axiale autour du biais.

	- Mean_dist_px : Distance moyenne (en pixels) des points observés à la courbe modèle dans l'espace (SigmaX, SigmaY).
	  Sert de score de cohérence / confiance.

	- P95_dist_px : 95e percentile de la distance à la courbe. Utile pour définir un seuil de rejet des estimations peu fiables.

	:param dataset: Tableau (N, 3) contenant les colonnes [SigmaX, SigmaY, Z]
	                (sigmas en pixels, Z dans des unités cohérentes avec le modèle).
	:param model: Modèle astigmatique de forme (2, 5) :
	              paramètres X puis Y, chaque ligne = [Z0, W, C3, C4, A].
	:param z_max: Valeur maximale de Z (le modèle est évalué sur [-z_max, +z_max]).
	:param n_curve: Nombre de points d'échantillonnage de la courbe modèle en Z.
	                Doit être suffisamment grand pour éviter une quantification de Z.
	:param pixel_size: Taille du pixel dans les mêmes unités que Z (ex. nm).
	:param sampling: Facteur d'échantillonnage (adimensionnel) utilisé dans le modèle
	                 de sigma (généralement égal à 1).
	:return: Dictionnaire de métriques décrivant la précision axiale (en unités de Z)
	         et la cohérence des données avec le modèle (distances en pixels).
	"""
	"""
	Estime Z par projection sur la courbe (sigmaX(Z), sigmaY(Z)) du modèle, puis calcule RMSE/MAE sur Z + score de confiance (distance à la courbe).

	:param dataset: Tableau (N, 3) contenant les colonnes [Sx, Sy, Z] (sigmas en pixels, Z en unités cohérentes avec le modèle).
	:param model: Modèle astigmatique de forme (2, 5) : paramètres X puis Y, chaque ligne = [Z0, W, C3, C4, A].
	:param pixel_size: Taille pixel dans les mêmes unités que Z (par ex. nm), utilisée dans le calcul de sigma.
	:param sampling: Facteur d'échantillonnage (adimensionnel) appliqué dans le calcul de sigma (laisser à 1).
	:param z_max:
	:param n_curve:
	:return: Dictionnaire de métriques : RMSE/MAE (en pixels) et R² (adimensionnel) pour Z.
	"""
	sx_obs, sy_obs, z_true = dataset[:, 0], dataset[:, 1], dataset[:, 2]

	z_curve = np.linspace(-z_max, z_max, n_curve, dtype=np.float64)
	sx_curve = sigma_model(model[0], z_curve, pixel_size, sampling)
	sy_curve = sigma_model(model[1], z_curve, pixel_size, sampling)
	curve = np.column_stack((sx_curve, sy_curve))

	tree = cKDTree(curve)
	dist, idx = tree.query(np.column_stack((sx_obs, sy_obs)), k=1)

	z_est = z_curve[idx]
	dz = z_est - z_true

	return {
			# Métriques en nanomètres
			"rmse_z":    float(np.sqrt(np.mean(dz * dz))),
			"mae_z":     float(np.mean(np.abs(dz))),
			"p95_abs_z": float(np.percentile(np.abs(dz), 95)),
			"bias_z":    float(np.mean(dz)),
			"std_z":     float(np.std(dz)),
			# Distance en pixel
			"mean_dist": float(np.mean(dist)),
			"p95_dist":  float(np.percentile(dist, 95)),
			}
