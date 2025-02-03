"""
Fichier contenant des fonctions pour charger des DLLs externes,
exécuter des traitements d'image via ces DLLs et gérer des paramètres liés aux algorithmes de détection de points.

Ce module regroupe des utilitaires pour :

- Chargement de DLLs : chargement des bibliothèques nécessaires au traitement d'image.
- Traitement d'images : exécution de traitements via DLLs pour détecter des points sur une image.
- Calcul et parsing de paramètres   estimation du nombre de points détectables en fonction des dimensions de l'image et de la densité.

**Structure** :

1. **Parsing**

   - `get_gaussian_mode` : Détermine le mode de fit Gaussien selon les paramètres fournis.
   - `get_max_points` : Calcule le nombre maximal théorique de points détectables dans une image.
   - `parse_palm_result` : Transforme le résultat de la DLL PALM en Dataframe lisible.

2. **DLL Manipulation**

   - `load_dll` : Charge les DLL nécessaires pour les traitements d'image (CPU, GPU, Live, Tracking).
   - `run_palm_dll` : Exécute un traitement d'image avec une DLL PALM pour détecter des points.

.. todo::
	Les différentes DLL PALM nécessitent des dépendances supplémentaires, le code source me permettrait de définir lesquelles.
	GPU et Live ne peuvent être chargé sur mon ordinateur (certainement CUDA 7.5).
	CPU n'est que si vcredist 2010 n'est pas installé, en revanche Tracking n'a aucun problème.

"""

import ctypes
from pathlib import Path

import numpy as np
import pandas as pd

from palm_tracer.Tools import print_warning

N_SEGMENTS = 13  # Nombre de paramètres pour chaque détection.
SEGMENTS = ["Sigma X", "Sigma Y", "Theta", "X", "Y",
			"Intensity 0",		 # Intensity too ?????? (I0 sometimes) Maybe different of Intensity. Have I if the offset is applied ?
			"Intensity Offset",  # Intensity Offset ???
			"MSE Gauss",		 # MSE Gauss
			"Intensity",		 # Intensity (Integrated Wavelet Intensity)
			"Surface", "Z", "Pair Distance", "Id"]


# ==================================================
# region Parsing
# ==================================================
##################################################
def _get_max_points(height: int = 256, width: int = 256, density: float = 0.2, n_planes: int = 1) -> int:
	"""
	Calcule le nombre maximal théorique de points détectables basé sur les dimensions et la densité de l'image.

	:param height: Hauteur de l'image (nombre de lignes). Par défaut 256.
	:param width: Largeur de l'image (nombre de colonnes). Par défaut 256.
	:param density: Densité de points par pixel. Par défaut 0.2.
	:param n_planes: Nombre de plans de l'image. Par défaut 1.

	:return: Nombre maximal théorique de points détectables.
	"""
	return int(height * width * density * n_planes) * N_SEGMENTS


##################################################
def _parse_palm_result(data: np.ndarray, gauss_fit: int, sort: bool = False) -> pd.DataFrame:
	"""
	Parsing du résultat de la DLL PALM.

	On a un tableau 1D de grande taille en entrée :
		- On le découpe en tableau 2D à 13 colonnes (`N_SEGMENTS`).	La taille du tableau est vérifié et tronqué si nécessaire.
		- On le transforme en dataframe avec les colonnes définies par `SEGMENTS`.
		- On supprime les lignes remplies de 0 et de -1. Un test sur les colonnes X ou Y strictement positif suffit (le SigmaX et SigmaY peuvent être à 0).

	:param data: Donnée en entrée récupérées depuis la DLL PALM.
	:param gauss_fit: Mode d'ajustement Gaussien.
	:param sort: Tri des points par Y puis X (sens de lecture Gauche à droite du haut vers le bas).
	:return: Dataframe filtré
	"""
	# Manipulation du tableau 1D.
	size = (data.size // N_SEGMENTS) * N_SEGMENTS							   # Récupération de la taille correcte si non multiple de N_SEGMENTS
	res = pd.DataFrame(data[:size].reshape(-1, N_SEGMENTS), columns=SEGMENTS)  # Transformation en Dataframe
	res = res[res['X'] > 0]													   # Filtrage des lignes remplies de 0 et -1

	if sort: res = res.sort_values(by=['Y', 'X'], ascending=[True, True])	   # Tri (un tri uniquement sur Y est possible, car peu de chance de doublons)
	res = res.reset_index(drop=True)										   # Remise à 0 des index
	res["Index"] = range(1, len(res) + 1)									   # Ajout d'un index dans le tableau
	res["Plane"] = 1														   # Ajout d'un plan dans le tableau
	res["Channel"] = -1														   # Ajout d'un channel dans le tableau
	res["MSE Z"] = -1														   # Ajout d'un MSE pour Z dans le tableau
	# Ajout de l'intensité intégré (si on à les sigma du gaussian fit ou non)
	if gauss_fit != 0: res["Integrated Intensity"] = 2 * np.pi * res["Intensity 0"] * res["Sigma X"] * res["Sigma Y"]
	else: res["Integrated Intensity"] = res["Intensity"]

	# Réorganisation des colonnes
	new_columns = ["Plane", "Index", "Channel", "Integrated Intensity", "X", "Y", "Sigma X", "Sigma Y", "Theta", "MSE Gauss", "Z", "MSE Z", "Pair Distance"]
	return res[new_columns]  # Sélection des colonnes


# ==================================================
# endregion Parsing
# ==================================================

# ==================================================
# region DLL Manipulation
# ==================================================
##################################################
def load_dll() -> dict[str, ctypes.CDLL]:
	"""Récupère les DLLs si elles existent."""
	res = dict[str, ctypes.CDLL]()
	dll_path = Path(__file__).parent.parent / "DLL"

	# GPU et Live n'arrivent pas à se charger (sans doute une dépendance cachée autre).
	for name in ["CPU", "GPU", "Live", "Tracking"]:
		dll_filename = dll_path / f"{name}_PALM.dll"
		try:
			res[name] = ctypes.cdll.LoadLibrary(str(dll_filename.resolve()))
			print(f"DLL '{dll_filename}' chargée.")
		except OSError as e:
			print_warning(f"Impossible de charger la DLL '{dll_filename}':\n\t{e}")
	return res


##################################################
def run_palm_image_dll(dll: ctypes.CDLL, image: np.ndarray, threshold: float, watershed: bool,
					   gauss_fit: int, sigma: float, theta: float, roi_size: int) -> pd.DataFrame:
	"""
	Exécute un traitement d'image avec une DLL PALM externe pour détecter des points dans une image.

	:param dll: Bibliothèque DLL contenant les fonctions de traitement d'image.
	:param image: Image d'entrée 2D sous forme de tableau numpy d'entier.
	:param threshold: Seuil pour la détection.
	:param watershed: Active ou désactive le mode watershed.
	:param gauss_fit: Mode d'ajustement Gaussien.
	:param sigma: Valeur initiale du sigma pour l'ajustement Gaussien.
	:param theta: Valeur initiale du theta pour l'ajustement Gaussien.
	:param roi_size: Taille de la région d'intérêt (ROI).
	:return: Liste des points détectés sous forme de dataframe contenant toutes les informations reçu de la DLL.
	"""
	# Parsing
	image = np.asarray(image, dtype=np.uint16)  # Forcer le type de l'image en np.uint16
	height, width = image.shape					# Récupération des dimensions
	n = _get_max_points(height, width)			# Récupération d'un nombre de points maximum théorique
	image = image.T.flatten()					# L'image est transposé car la DLL fonctionne en column Major

	c_image = image.ctypes.data_as(ctypes.POINTER(ctypes.c_ushort))			   # Image
	c_height = ctypes.c_ushort(height)										   # Hauteur (nombre de lignes)
	c_width = ctypes.c_ushort(width)										   # Largeur (nombre de colonnes)
	n_points = ctypes.c_ushort(n)											   # Nombre maximum de points théorique
	c_points = np.zeros((n,)).ctypes.data_as(ctypes.POINTER(ctypes.c_double))  # Liste de points
	c_wavelet = ctypes.c_uint(1)											   # Wavelet toujours à 1.
	c_threshold = ctypes.c_double(threshold)								   # Seuil
	c_watershed = ctypes.c_double(10 if watershed else 0)					   # Activation du Watershed
	c_vol_min = ctypes.c_double(4)											   # Vol minimum toujours à 4.
	c_int_min = ctypes.c_double(0)											   # Int minimum toujours à 0.
	c_gauss_fit = ctypes.c_ushort(gauss_fit)								   # Mode du Gaussian Fit
	c_sigma = ctypes.c_double(sigma)										   # Valeur initiale du Sigma
	c_theta = ctypes.c_double(theta)										   # Valeur Initiale du Theta
	c_roi_size = ctypes.c_ushort(roi_size)									   # taille de la ROI

	# Running
	dll._OpenPALMProcessing(c_image, c_points, n_points, c_width, c_height, c_wavelet, c_threshold, c_watershed,
							c_vol_min, c_int_min, c_gauss_fit, c_sigma, c_sigma, c_theta, c_roi_size)
	dll._PALMProcessing()
	dll._closePALMProcessing()

	return _parse_palm_result(np.ctypeslib.as_array(c_points, shape=(n,)), gauss_fit, False)


##################################################
def run_palm_stack_dll(dll: ctypes.CDLL, stack: np.ndarray, threshold: float, watershed: bool,
					   gauss_fit: int, sigma: float, theta: float, roi_size: int) -> pd.DataFrame:
	"""
	Exécute un traitement d'image avec une DLL PALM externe pour détecter des points dans une image.

	:param dll: Bibliothèque DLL contenant les fonctions de traitement d'image.
	:param stack: Pile d'image d'entrée sous forme de tableau numpy.
	:param threshold: Seuil pour la détection.
	:param watershed: Active ou désactive le mode watershed.
	:param gauss_fit: Mode d'ajustement Gaussien (défini par `get_gaussian_mode`).
	:param sigma: Valeur initiale du sigma pour l'ajustement Gaussien.
	:param theta: Valeur initiale du theta pour l'ajustement Gaussien.
	:param roi_size: Taille de la région d'intérêt (ROI).
	:return: Liste des points détectés sous forme de dataframe contenant toutes les informations reçu de la DLL.
	"""
	results = []

	for i in range(stack.shape[0]):
		points = run_palm_image_dll(dll, stack[i], threshold, watershed, gauss_fit, sigma, theta, roi_size)
		points["Plane"] = i + 1  # Modifier une colonne 'Plane' au DataFrame temporaire
		results.append(points)   # Ajouter à la liste

	# Créer le dataframe final peut-être plus rapide que le mettre à jour à chaque iteration (réallocation des milliers de fois)
	return pd.concat(results, ignore_index=True)

# ==================================================
# endregion DLL Manipulation
# ==================================================
