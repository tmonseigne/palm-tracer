""" Fichier contenant des fonctions pour la création de galeries. """
import numpy as np
import pandas as pd


##################################################
def make_gallery(stack: np.ndarray, localizations: pd.DataFrame, roi_size: int, rois_per_line: int) -> np.ndarray:
	"""
    Génère une galerie d'images extraites d'une pile d'images en fonction des localisations spécifiées.

    :param stack: Un tableau 3D (n_planes, height, width) représentant la pile d'images.
    :param localizations: DataFrame contenant au minimum les colonnes ['Plane', 'Y', 'X'] avec les coordonnées des ROIs.
    :param roi_size: Taille de chaque ROI (carré de dimensions roi_size x roi_size).
    :param rois_per_line: Nombre de ROIs par ligne dans la galerie.
    :return: np.ndarray, un tableau 3D (n_planes, size, size) contenant la galerie.
	"""
	size = roi_size * rois_per_line  # Taille d'un plan de la galerie
	rois_per_plane = rois_per_line ** 2  # Nombre de ROIs maximum par plan
	n_rois = len(localizations)
	n_planes = (n_rois + rois_per_plane - 1) // rois_per_plane  # Calcul du nombre de plans nécessaires
	max_height, max_width = stack.shape[1], stack.shape[2]  # Récupération des limites de l'image
	res = np.zeros((n_planes, size, size), dtype=stack.dtype)  # Résultat final

	for idx, (plane, y, x) in enumerate(zip(localizations["Plane"], localizations["Y"], localizations["X"])):
		gallery_plane = idx // rois_per_plane  # Déterminer sur quel plan on est
		pos_in_plane = idx % rois_per_plane  # Position dans la grille du plan
		row, col = divmod(pos_in_plane, rois_per_line)  # Calculer la ligne et la colonne dans la grille

		# Déterminer les bornes de la ROI (méthode non sure car avec les arrondis la ROI peut avoir une taille de roi_size ou roi_size + 1)
		# half_size = roi_size / 2
		# x_min, x_max = max(0, int(round(x - half_size))), min(max_width, int(round(x + half_size)))
		# y_min, y_max = max(0, int(round(y - half_size))), min(max_height, int(round(y + half_size)))

		# Déterminer les bornes de la ROI
		half_size = roi_size // 2
		# Calcul centre arrondi
		x_center = int(round(x))
		y_center = int(round(y))

		# Bornes en X
		x_min = max(0, x_center - half_size)
		x_max = x_min + roi_size
		if x_max > max_width: x_max, x_min = max_width, max_width - roi_size

		# Bornes en Y
		y_min = max(0, y_center - half_size)
		y_max = y_min + roi_size
		if y_max > max_height: y_max, y_min = max_height, max_height - roi_size

		# Extraire la région de l'image originale et la copier dans la grille
		roi = stack[plane - 1, y_min:y_max, x_min:x_max]

		# Déterminer la position de copie dans la galerie
		gy_min, gy_max = row * roi_size, (row + 1) * roi_size
		gx_min, gx_max = col * roi_size, (col + 1) * roi_size

		# Vérifier si la ROI extraite doit être remplie à une taille fixe (si proche des bords)
		res[gallery_plane, gy_min:gy_max, gx_min:gx_max] = roi

	return res
