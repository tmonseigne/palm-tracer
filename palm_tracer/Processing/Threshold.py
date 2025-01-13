"""
Fichier contenant des fonctions pour le calcul automatique de seuils d'image, basé sur la segmentation et d'autres méthodes (en cours d'implémentation).

Ce module regroupe des utilitaires pour :

- Calcul de seuils automatiques : estimation du seuil de segmentation pour une image.
- Méthodes expérimentales : placeholders pour des méthodes avancées de calcul de seuil utilisant des DLLs ou des approches spectrales.

**Structure** :

1. **Auto Thresholding**

   - `auto_threshold` : Calcule un seuil automatique basé sur l'écart type des pixels de l'image et les régions d'intérêt (ROI).

2. **Méthodes à implémenter**

   - `auto_threshold_dll` : Placeholder pour une méthode de calcul de seuil utilisant une DLL.
   - `auto_threshold_spectral` : Placeholder pour une méthode spectrale de calcul de seuil.
   - `auto_threshold_spectral_dll` : Placeholder pour une méthode spectrale de calcul de seuil utilisant une DLL.

"""

import numpy as np


##################################################
def auto_threshold(image: np.array, max_iterations:int =4, roi_size:int =7):
	"""
	Calcule un seuil automatique basé sur la segmentation de l'image.

	:param image: Image 2D sous forme de tableau NumPy.
	:param max_iterations: Nombre d'itérations pour affiner le seuil.
	:param roi_size: Taille des régions d'intérêt (ROI) utilisées pour la segmentation.
	:return: Seuil calculé (écart type final).
	"""
	mask = np.zeros_like(image, dtype=int)

	# Calcul initial de l'écart type
	std_dev = np.std(image)

	for _ in range(max_iterations):
		# Mise à jour du masque basé sur le seuil
		mask.fill(0)
		mask[image > std_dev] = 1

		# Calcul de l'écart type pour les pixels hors segmentation
		pixels_outside = image[mask == 0]
		if len(pixels_outside) > 0: std_dev = np.std(pixels_outside)
		else: break

	return std_dev

##################################################
def auto_threshold_dll():
	print("TODO")

##################################################
def auto_threshold_spectral():
	print("TODO")

##################################################
def auto_threshold_spectral_dll():
	print("TODO")
