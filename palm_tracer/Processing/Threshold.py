"""
Fichier contenant des fonctions pour le calcul automatique de seuils d'image, basé sur la segmentation et d'autres méthodes (en cours d'implémentation).

Ce module regroupe des utilitaires pour :

- Calcul de seuils automatiques : estimation du seuil de segmentation pour une image.

**Structure** :

   - :func:`auto_threshold` : Calcule un seuil automatique basé sur l'écart type des pixels de l'image et les régions d'intérêt (ROI).
   - :func:`auto_threshold_dll` : Calcule un seuil automatique basé sur l'écart type des pixels de l'image et les régions d'intérêt (ROI).

.. note::
	Lors de la mise à jour du masque, il n'est pas remis à 0 à chaque iteration, cela ne change pas grand chose au final, mais c'est étrange.

"""

import ctypes
import math

import numpy as np

from palm_tracer.Processing import run_palm_image_dll


##################################################
def auto_threshold(image: np.array):
	"""
	Calcule un seuil automatique basé sur la segmentation de l'image.

	:param image: Image 2D sous forme de tableau NumPy.
	:return: Seuil calculé (écart type final).
	"""
	mask = np.zeros_like(image, dtype=int)						  # Creation du masque
	std_dev = np.std(image)										  # Calcul initial de l'écart type
	mask[image > std_dev] = 1									  # Mise à jour du masque
	pixels_outside = image[mask == 0]							  # Récupération des pixel hors segmentation
	if len(pixels_outside) > 0: std_dev = np.std(pixels_outside)  # Mise à jour de l'écart type
	return std_dev


##################################################
def auto_threshold_dll(dll: ctypes.CDLL, image: np.array, roi_size: int = 7, max_iterations: int = 4):
	"""
	Calcule un seuil automatique basé sur la segmentation de l'image.

	:param dll: Bibliothèque DLL contenant les fonctions de traitement d'image.
	:param image: Image 2D sous forme de tableau NumPy.
	:param roi_size: Taille des régions d'intérêt (ROI) utilisées pour la segmentation (par défaut 7).
	:param max_iterations: Nombre d'itérations pour affiner le seuil (par défaut 4).
	:return: Seuil calculé (écart type final).
	"""
	mask = np.zeros_like(image, dtype=int) # Creation du masque
	std_dev = np.std(image)				   # Calcul initial de l'écart type
	roi_2 = float(roi_size) / 2.0		   # Demi-taille de la zone ROI
	height, width = image.shape			   # Récupération de la taille de l'image

	for _ in range(max_iterations):
		# Lancement d'un PALM et récupération de la liste des points (format (x, y))
		points = run_palm_image_dll(dll, image, std_dev, False, 0, 1, math.pi / 4.0, roi_size)
		# Mise à jour du masque basé sur le résultat du PALM
		# mask.fill(0)
		for x, y in zip(points['X'], points['Y']):
			# Définir les limites de la ROI tout en respectant les bords de l'image
			x_min, x_max = max(0, int(x - roi_2)), min(width, int(x + roi_2))
			y_min, y_max = max(0, int(y - roi_2)), min(height, int(y + roi_2))
			# Mettre à jour le masque pour les pixels dans la ROI
			mask[y_min:y_max, x_min:x_max] = 1

		# Calcul de l'écart type pour les pixels hors segmentation
		pixels_outside = image[mask == 0]
		if len(pixels_outside) > 0: std_dev = np.std(pixels_outside)
		else: break  # pragma: no cover	(ce else est presque impossible à avoir)

	return std_dev
