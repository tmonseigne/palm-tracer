"""
Fichier contenant des fonctions pour charger des DLLs externes,
exécuter des traitements d'image via ces DLLs et gérer des paramètres liés aux algorithmes de détection de points.

Ce module regroupe des utilitaires pour :

- Chargement de DLLs : chargement des bibliothèques nécessaires au traitement d'image.
- Traitement d'images : exécution de traitements via DLLs pour détecter des points sur une image.
- Calcul de paramètres théoriques : estimation du nombre de points détectables en fonction des dimensions de l'image et de la densité.

**Structure** :

1. **DLL Loading**

   - `load_dll` : Charge les DLL nécessaires pour les traitements d'image (CPU, GPU, Live, Tracking).

2. **Image Processing**

   - `run_dll` : Exécute un traitement d'image avec une DLL PALM pour détecter des points.

3. **Gaussian Fit Mode**

   - `get_gaussian_mode` : Détermine le mode de fit Gaussien selon les paramètres fournis.

4. **Point Calculation**

   - `get_max_points` : Calcule le nombre maximal théorique de points détectables dans une image.

"""

import ctypes
from pathlib import Path

import numpy as np

from palm_tracer.Tools import print_warning

N_SEGMENTS = 13  # Nombre de paramètres pour chaque détection.
X_POS = 4  # Position du X dans les paramètres.
Y_POS = 3  # Position du Y dans les paramètres.


##################################################
def load_dll() -> dict[str, ctypes.CDLL]:
	"""Récupère les DLLs si elles existent."""
	res = dict[str, ctypes.CDLL]()
	dll_path = Path(__file__).parent.parent / "DLL"

	# GPU et Live n'arrivent pas à se charger (sans doute une dépendance caché autre).
	for name in ["CPU", "GPU", "Live", "Tracking"]:
		dll_filename = dll_path / f"{name}_PALM.dll"
		try:
			res[name] = ctypes.cdll.LoadLibrary(str(dll_filename.resolve()))
		except OSError as e:
			print_warning(f"Impossible de charger la DLL '{dll_filename}':\n\t{e}")
	return res


##################################################
def get_gaussian_mode(gaussian_fit: bool, sigma_fixed: bool, theta_fixed: bool) -> int:
	"""
    Détermine le mode de fit Gaussien basé sur les paramètres donnés.

    :param gaussian_fit: Indique si le fit Gaussien est activé.
	:param sigma_fixed: Indique si le sigma est fixe.
	:param theta_fixed: Indique si le theta est fixe.

	:return:Mode correspondant :
            - 0 : Pas de fit Gaussien
            - 1 : Mode X, Y
            - 2 : Mode X, Y, sigma
            - 3 : Mode X, Y, sigmaX, sigmaY
            - 4 : Mode X, Y, sigmaX, sigmaY, Theta

	"""
	if gaussian_fit:
		if sigma_fixed and theta_fixed: return 1	  # Mode X, Y
		if not sigma_fixed and theta_fixed: return 2  # Mode X, Y sigma
		if sigma_fixed and not theta_fixed: return 3  # Mode X, Y sigmaX, sigmaY
		return 4									  # Mode X, Y sigmaX, sigmaY, Theta
	return 0										  # Mode None


##################################################
def get_max_points(height: int = 256, width: int = 256, density: float = 0.2, n_planes: int = 1) -> int:
	"""
	Calcule le nombre maximal théorique de points détectables basé sur les dimensions et la densité de l'image.

	:param height: Hauteur de l'image (nombre de lignes). Par défaut 256.
	:param width: Largeur de l'image (nombre de colonnes). Par défaut 256.
	:param density: Densité de points par pixel. Par défaut 0.2.
	:param n_planes: Nombre de plans de l'image. Par défaut 1.

	:return: Nombre maximal théorique de points détectables.
	"""
	return int(height * width * density * n_planes * N_SEGMENTS)


##################################################
def run_dll(dll: ctypes.CDLL, image: np.ndarray, threshold: float, watershed: bool,
			gauss_fit: int, sigma: float, theta: float, roi_size: int) -> np.ndarray:
	"""
    Exécute un traitement d'image avec une DLL PALM externe pour détecter des points dans une image.

	:param dll: Bibliothèque DLL contenant les fonctions de traitement d'image.
	:param image: Image d'entrée sous forme de tableau numpy.
	:param threshold: Seuil pour la détection.
	:param watershed: Active ou désactive le mode watershed.
	:param gauss_fit: Mode de fit Gaussien (défini par `get_gaussian_mode`).
	:param sigma: Valeur initiale du sigma pour le fit Gaussien.
	:param theta: Valeur initiale du theta pour le fit Gaussien.
	:param roi_size: Taille de la région d'intérêt (ROI).

	:return: Liste des points détectés sous forme de tuples (X, Y).
	"""
	# Parsing
	c_image = image.ctypes.data_as(ctypes.POINTER(ctypes.c_ushort))					  # Image
	c_height = image.shape[0]														  # Hauteur (nombre de lignes)
	c_width = image.shape[1]														  # Largeur (nombre de colonnes)
	n_points = get_max_points(c_height, c_width)									  # Nombre maximum de points théorique
	c_points = np.zeros((n_points,)).ctypes.data_as(ctypes.POINTER(ctypes.c_double))  # Liste de points
	c_wavelet = ctypes.c_uint(1)													  # Wavelet toujours à 1.
	c_threshold = ctypes.c_double(threshold)										  # Seuil
	c_watershed = ctypes.c_double(10 if watershed else 0)							  # Activation du Watershed
	c_vol_min = ctypes.c_double(4)													  # Vol minimum toujours à 4.
	c_int_min = ctypes.c_double(0)													  # Int minimum toujours à 0.
	c_gauss_fit = ctypes.c_ushort(gauss_fit)										  # Mode du Gaussian Fit
	c_sigma = ctypes.c_double(sigma)												  # Valeur initiale du Sigma
	c_theta = ctypes.c_double(theta)												  # Valeur Initiale du Theta
	c_roi_size = ctypes.c_ushort(roi_size)											  # taille de la ROI

	# Running
	dll._OpenPALMProcessing(c_image, c_points, n_points, c_width, c_height, c_wavelet, c_threshold, c_watershed,
							c_vol_min, c_int_min, c_gauss_fit, c_sigma, c_sigma, c_theta, c_roi_size)
	dll_ret = dll._PALMProcessing()
	dll._closePALMProcessing()

	result = np.ctypeslib.as_array(c_points, shape=(n_points,))

	# Manage Result to have points
	res = []
	for i in range(0, len(result) - N_SEGMENTS, N_SEGMENTS):
		x, y = result[i + X_POS], result[i + Y_POS]
		if int(x) > 0 and int(y) > 0: res.append([result[i + 4], result[i + 3]])  # Conservation des résultats strictement positifs.
	return np.array(res, dtype=np.float32)
