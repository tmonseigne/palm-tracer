"""
Module contenant les fonctions de visualization pouyr palm-tracer.
"""
import numpy as np


##################################################
def hr_visualization(width: int, height: int, ratio: int, points: np.ndarray) -> np.ndarray:
	"""
	Construit une image Haute résolution en fonction des éléments localisés.

	:param width: Largeur de l'image.
	:param height: Hauteur de l'image.
	:param ratio: Ratio d'aggrandissement de l'image.
	:param points: Localisations des points.
	:return: Nouvelle image.
	"""

	if ratio <=1: return np.zeros((width, height), dtype=np.uint16)
	if width < 1 or height < 1: return np.zeros((max(int(width * ratio), 1), max(int(height * ratio), 1)), dtype=np.uint16)

	res = np.zeros((int(width * ratio), int(height * ratio)), dtype=float)

	# Filtrage des points hors des dimensions initiales
	mask = (points[:, 0] <= width) & (points[:, 1] <= height)
	points = points[mask]
	if points is None or points.size == 0 or points.shape[1] != 3: return res.astype(np.uint16)

	# Calcul des nouvelles coordonnées (vectorisé)
	coords = (points[:, :2] * ratio).astype(int)
	x, y = coords[:, 0], coords[:, 1]

	# Accumulation des valeurs (plus efficace qu'une boucle)
	np.add.at(res, (x, y), points[:, 2])

	# Normalisation ou autre pour les Z par exemple ?

	res = res.clip(0, np.iinfo(np.uint16).max)  # Limite les valeurs entre 0 et la valeur maximale possible pour un uint16
	return np.asarray(res, dtype=np.uint16)		# Forcer le type de l'image en np.uint16
