""" Fichier contenant des fonctions lié à l'astigmatisme 3D (estimation de la position axiale en fonction des écart-types sur X et Y)."""
import numpy as np

DLL_REQUIRED_COLS = ["Sigma X", "Sigma Y", "Z"]
MODEL_COLS = ["Z0", "W", "C3", "C4", "A"]
MODEL_ROWS = ["X", "Y"]


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
def get_z_from_planes(planes: np.ndarray, z_min: float, z_max: float) -> np.ndarray:
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
def get_z_from_step(n_planes: int, z_step: float, center: bool = True) -> np.ndarray:
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
