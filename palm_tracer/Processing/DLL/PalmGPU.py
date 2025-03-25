"""
Fichier contenant une classe pour utiliser la DLL externe GPU_PALM, exécuter les algorithmes de détection de points et les paramètres liés.

.. todo::
	Doit ont garder les identifiants et les plans qui vont de 1 à N au lieu du classique 0 à N-1 ?
"""

import ctypes
import math
from dataclasses import dataclass, field
from typing import Any, Optional

import numpy as np
import pandas as pd

from palm_tracer.Processing.DLL.Load import load_dll
from palm_tracer.Processing.DLL.Parsing import get_max_points, parse_palm_result


##################################################
@dataclass
class PalmGPU:
	""" Classe permettant d'utiliser la DLL externe CPU_PALM, exécuter les algorithmes de détection de points et les paramètres liés. """
	_dll: ctypes.CDLL = field(init=False)

	##################################################
	def __post_init__(self):
		"""Méthode appelée automatiquement après l'initialisation du dataclass."""
		self._dll = load_dll("GPU")

	##################################################
	def is_valid(self): return self._dll is not None

	##################################################
	@staticmethod
	def __get_args(image: np.ndarray, threshold: float, watershed: bool, gauss_fit: int,
				   sigma: float, theta: float, roi_size: int) -> dict[str, Any]:
		"""
		Récupère les arguments necessaire au lancement de la DLL PALM externe.

		:param image: Image d'entrée 2D sous forme de tableau numpy d'entier.
		:param threshold: Seuil pour la détection.
		:param watershed: Active ou désactive le mode watershed.
		:param gauss_fit: Mode d'ajustement Gaussien.
		:param sigma: Valeur initiale du sigma pour l'ajustement Gaussien.
		:param theta: Valeur initiale du theta pour l'ajustement Gaussien.
		:param roi_size: Taille de la région d'intérêt (ROI).
		:return: Dictionniare d'arguments pour la DLL (attention l'ordre doit être respecté).
		"""
		# Parsing
		image = np.asarray(image, dtype=np.uint16)  # Forcer le type de l'image en np.uint16
		height, width = image.shape  # Récupération des dimensions
		n = get_max_points(height, width)  # Récupération d'un nombre de points maximum théorique
		image = image.flatten()  # L'image est "applati"

		return {"image":          image.ctypes.data_as(ctypes.POINTER(ctypes.c_ushort)),  # Image
				"points":         np.zeros((n,), dtype=np.float64).ctypes.data_as(ctypes.POINTER(ctypes.c_double)),  # Liste de points
				"n":              ctypes.c_ulong(n),						# Nombre maximum de points théorique
				"n_plane":        ctypes.c_ulong(1),						# Profondeur (nombre de plans)
				"height":         ctypes.c_ulong(height),					# Hauteur (nombre de lignes)
				"width":          ctypes.c_ulong(width),					# Largeur (nombre de colonnes)
				"wavelet":        ctypes.c_ulong(1),						# Wavelet toujours à 1.
				"threshold":      ctypes.c_double(threshold),				# Seuil
				"watershed":      ctypes.c_double(0 if watershed else 10),  # Activation du Watershed
				"vol_min":        ctypes.c_double(4),						# Vol minimum toujours à 4.
				"int_min":        ctypes.c_double(0),						# Int minimum toujours à 0.
				"gauss_fit":      ctypes.c_ushort(gauss_fit),				# Mode du Gaussian Fit
				"sigma_x":        ctypes.c_double(sigma),					# Valeur initiale du Sigma X
				"sigma_y":        ctypes.c_double(sigma * 2),				# Valeur initiale du Sigma Y (*2 pour correspondre à métamorph, interet limité)
				"theta":          ctypes.c_double(theta),					# Valeur Initiale du Theta
				"roi_size":       ctypes.c_ushort(roi_size),				# taille de la ROI
				# Les arguments suivants sont pour la DLL GPU, mais ne seront pas utilisés
				"is_computing_z": ctypes.c_ushort(0),						# Calculs sur Z toujours à 0.
				"sigma_x_coefs":  np.zeros((5,), dtype=np.float64).ctypes.data_as(ctypes.POINTER(ctypes.c_double)),  # taille de la ROI
				"sigma_y_coefs":  np.zeros((5,), dtype=np.float64).ctypes.data_as(ctypes.POINTER(ctypes.c_double)),  # taille de la ROI
				"3d_thickness":   ctypes.c_double(0),						# taille de l'épaisseur sur Z (µm) toujours à 0.
				"3d_sampling":    ctypes.c_double(0),						# taille de la résolution sur Z (µm) toujours à 0.
				"pixel_size":     ctypes.c_double(0),						# taille des pixels (µm) toujours à 0.
				}

	##################################################
	def __run_image(self, image: np.ndarray, threshold: float, watershed: bool, gauss_fit: int,
					sigma: float, theta: float, roi_size: int, plane: int = 1) -> pd.DataFrame:
		"""
		Exécute un traitement d'image avec une DLL PALM externe pour détecter des points dans une image.

		:param image: Image d'entrée 2D sous forme de tableau numpy d'entier.
		:param threshold: Seuil pour la détection.
		:param watershed: Active ou désactive le mode watershed.
		:param gauss_fit: Mode d'ajustement Gaussien.
		:param sigma: Valeur initiale du sigma pour l'ajustement Gaussien.
		:param theta: Valeur initiale du theta pour l'ajustement Gaussien.
		:param roi_size: Taille de la région d'intérêt (ROI).
		:param plane: Numéro du plan dans la pile
		:return: Liste des points détectés sous forme de dataframe contenant toutes les informations reçu de la DLL.
		"""
		args = self.__get_args(image, threshold, watershed, gauss_fit, sigma, theta, roi_size)
		# Running
		self._dll.OpenPALMProcessing(*args.values())
		self._dll.PALMProcessing()
		self._dll.closePALMProcessing()

		return parse_palm_result(np.ctypeslib.as_array(args["points"], shape=(args["n"].value,)), plane, gauss_fit, True, True)

	##################################################
	def run(self, stack: np.ndarray, threshold: float, watershed: bool, gauss_fit: int,
			sigma: float, theta: float, roi_size: int, planes: Optional[list[int]] = None) -> pd.DataFrame:
		"""
		Exécute un traitement d'image avec une DLL PALM externe pour détecter des points dans une pile ou une image.

		:param stack: Pile d'images en entrée sous forme de tableau numpy (possibilité d'envoyer une image directement).
		:param threshold: Seuil pour la détection.
		:param watershed: Active ou désactive le mode watershed.
		:param gauss_fit: Mode d'ajustement Gaussien (défini par `get_gaussian_mode`).
		:param sigma: Valeur initiale du sigma pour l'ajustement Gaussien.
		:param theta: Valeur initiale du theta pour l'ajustement Gaussien.
		:param roi_size: Taille de la région d'intérêt (ROI).
		:param planes: Liste des plans à analyser (None pour tous les plans).
		:return: Liste des points détectés sous forme de dataframe contenant toutes les informations reçu de la DLL.
		"""
		if stack.ndim == 2: return self.__run_image(stack, threshold, watershed, gauss_fit, sigma, theta, roi_size)

		n_planes = stack.shape[0]
		if planes is None: planes = list(range(n_planes))
		else: planes = [p for p in planes if isinstance(p, int) and 0 <= p < n_planes]

		results = []
		for i in planes:
			points = self.__run_image(stack[i], threshold, watershed, gauss_fit, sigma, theta, roi_size, i + 1)
			results.append(points)  # Ajouter à la liste

		# Créer le dataframe final peut-être plus rapide que le mettre à jour à chaque iteration (réallocation des milliers de fois)
		res = pd.concat(results, ignore_index=True)
		res["Id"] = range(1, len(res) + 1)  # Mise à jour de l'ID dans le tableau
		return res

	##################################################
	def auto_threshold(self, image: np.array, roi_size: int = 7, max_iterations: int = 4):
		"""
		Calcule un seuil automatique basé sur la segmentation de l'image.

		:param image: Image 2D sous forme de tableau NumPy.
		:param roi_size: Taille des régions d'intérêt (ROI) utilisées pour la segmentation (par défaut 7).
		:param max_iterations: Nombre d'itérations pour affiner le seuil (par défaut 4).
		:return: Seuil calculé (écart type final).
		"""
		mask = np.zeros_like(image, dtype=bool)  # Creation du masque
		std_dev = np.std(image)					 # Calcul initial de l'écart type
		roi_2 = float(roi_size) / 2.0			 # Demi-taille de la zone ROI
		height, width = image.shape				 # Récupération de la taille de l'image

		for _ in range(max_iterations):
			# Lancement d'un PALM et récupération de la liste des points (format (x, y))
			points = self.__run_image(image, std_dev, False, 0, 1, math.pi / 4.0, roi_size)
			# Mise à jour du masque basé sur le résultat du PALM
			# mask.fill(0)
			for x, y in zip(points['X'], points['Y']):
				# Définir les limites de la ROI tout en respectant les bords de l'image
				x_min, x_max = max(0, int(x - roi_2)), min(width, int(x + roi_2))
				y_min, y_max = max(0, int(y - roi_2)), min(height, int(y + roi_2))
				# Mettre à jour le masque pour les pixels dans la ROI
				mask[y_min:y_max, x_min:x_max] = True

			# Calcul de l'écart type pour les pixels hors segmentation
			pixels_outside = image[~mask]
			if len(pixels_outside) > 0: std_dev = np.std(pixels_outside)
			else: break  # pragma: no cover	(ce else est presque impossible à avoir)

		return std_dev
