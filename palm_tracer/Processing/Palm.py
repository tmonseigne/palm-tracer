"""
Fichier contenant une classe pour utiliser la DLL externe CPU_PALM, exécuter les algorithmes de détection de points et les paramètres liés.

.. todo::
	Doit-on garder les identifiants et les plans qui vont de 1 à N au lieu du classique 0 à N-1 ?
"""

import ctypes
import math
import sys
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Optional

import numpy as np
import pandas as pd
from mpmath.functions.zetazeros import count_to

from palm_tracer.Processing.Parsing import get_max_points, parse_palm_result
from palm_tracer.Tools.Utils import load_dll


##################################################
@dataclass
class Palm:
	""" Classe permettant d'utiliser la DLL externe PALM, exécuter les algorithmes de détection de points et les paramètres liés. """
	_type: str = field(init=True, default="CPU")
	"""Type de DLL, par défaut CPU, GPU également possible."""
	_dll: ctypes.CDLL = field(init=False)
	"""DLL chargée."""
	_points: np.ndarray = field(init=False)
	"""Liste des points en sortie de la DLL."""
	_args: OrderedDict[str, Any] = field(init=False)
	"""Arguments à passer à la DLL."""

	##################################################
	def __post_init__(self):
		"""Méthode appelée automatiquement après l'initialisation du dataclass."""
		self._dll = load_dll(self._type)
		self._points = np.zeros((1,), dtype=np.float64)

		self._args = OrderedDict(
				[("stack", None),	   # Pile
				 ("points", None),	   # Liste de points
				 ("n", None),		   # Nombre maximum de points théorique
				 ("height", None),	   # Hauteur (nombre de lignes)
				 ("width", None),	   # Largeur (nombre de colonnes)
				 ("planes", None),	   # Profondeur (nombre de plans)
				 ("threshold", None),  # Seuil
				 ("watershed", None),  # Activation du Watershed
				 ("fit", None),		   # Mode du Gaussian Fit
				 ("sigma", None),	   # Valeur initiale du Sigma
				 ("theta", None),	   # Valeur Initiale du Theta
				 ("roi_size", None)])  # taille de la ROI

	##################################################
	def is_valid(self) -> bool:
		"""
		Vérifie la validité de la DLL utilisée pour PALM.

		:return: True si la DLL est valide, False sinon.
		"""
		return self._dll is not None

	##################################################
	def __init_args(self, stack: np.ndarray, height: int, width: int, planes: int, threshold: float, watershed: bool, fit: int,
					sigma: float, theta: float, roi_size: int):
		"""
		Initialise les arguments necessaire au lancement de la DLL PALM externe.

		:param stack: Pile d'images en entrée sous forme de tableau numpy 3D.
		:param height: Hauteur des images.
		:param width: Largeur des images.
		:param planes: Nombre de plans.
		:param threshold: Seuil pour la détection.
		:param watershed: Active ou désactive le mode watershed.
		:param fit: Mode d'ajustement Gaussien.
		:param sigma: Valeur initiale du sigma pour l'ajustement Gaussien.
		:param theta: Valeur initiale du theta pour l'ajustement Gaussien.
		:param roi_size: Taille de la région d'intérêt (ROI).
		:return: Dictionniare d'arguments pour la DLL (attention l'ordre doit être respecté).
		"""
		# Parsing
		n = get_max_points(height, width, planes)  # Récupération d'un nombre de points maximum théorique
		if n != self._args["n"]: self._points = np.zeros((n,), dtype=np.float64)
		self._args["stack"] = np.asarray(stack, dtype=np.uint16).flatten().ctypes.data_as(ctypes.POINTER(ctypes.c_ushort))
		self._args["points"] = self._points.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
		self._args["n"] = ctypes.c_ulong(n)
		self._args["height"] = ctypes.c_ulong(height)
		self._args["width"] = ctypes.c_ulong(width)
		self._args["planes"] = ctypes.c_ulong(planes)
		self._args["threshold"] = ctypes.c_double(threshold)
		self._args["watershed"] = ctypes.c_double(0 if watershed else 10)
		self._args["fit"] = ctypes.c_ushort(fit)
		self._args["sigma"] = ctypes.c_double(sigma)
		self._args["theta"] = ctypes.c_double(theta)
		self._args["roi_size"] = ctypes.c_ushort(roi_size)

	##################################################
	@staticmethod
	def get_fit(mode: int = 0, submode: int = 0) -> int:
		"""Récupère le numéro du fit pour le palm."""
		if mode == 0: return 0				# Aucun ajustement
		elif mode == 0: return 1 + submode  # Ajustement Gaussien
		else: return 0  					# Ajustement Spline

	##################################################
	def run(self, stack: np.ndarray, threshold: float, watershed: bool, fit: int,
			sigma: float, theta: float, roi_size: int, planes: Optional[list[int]] = None) -> pd.DataFrame:
		"""
		Exécute un traitement d'image avec une DLL PALM externe pour détecter des points dans une pile ou une image.

		:param stack: Pile d'images en entrée sous forme de tableau numpy (possibilité d'envoyer une image directement).
		:param threshold: Seuil pour la détection.
		:param watershed: Active ou désactive le mode watershed.
		:param fit: Mode d'ajustement Gaussien (défini par `get_gaussian_mode`).
		:param sigma: Valeur initiale du sigma pour l'ajustement Gaussien.
		:param theta: Valeur initiale du theta pour l'ajustement Gaussien.
		:param roi_size: Taille de la région d'intérêt (ROI).
		:param planes: Liste des plans à analyser (None pour tous les plans).
		:return: Liste des points détectés sous forme de dataframe contenant toutes les informations reçu de la DLL.
		"""
		height, width = stack.shape[-2:]  # Récupère les deux dernières dimensions
		n_planes = 1 if stack.ndim == 2 else stack.shape[0]

		if planes is None: planes = list(range(n_planes))
		else: planes = [p for p in planes if isinstance(p, int) and 0 <= p < n_planes]

		# cut de l'image pour n'avoir que les plans voulu
		new_n_planes = len(planes)
		# Ajoute une dimension plan artificielle pour une Image 2D ou une vue mémoire (slice) pour une pile 3D
		new_stack = stack[np.newaxis, :, :] if stack.ndim == 2  else stack[planes[0]:planes[-1]+1]

		self.__init_args(new_stack, height, width, new_n_planes, threshold, watershed, fit, sigma, theta, roi_size)
		count = self._dll.Process(*self._args.values())
		res = parse_palm_result(self._points, count)
		if planes[0] != 0 : res["Plane"] += planes[0] # en cas de filtre de plans
		return res


	##################################################
	def auto_threshold(self, image: np.ndarray, roi_size: int = 7, max_iterations: int = 4):
		"""
		Calcule un seuil automatique basé sur la segmentation de l'image.

		:param image: Image 2D sous forme de tableau NumPy.
		:param roi_size: Taille des régions d'intérêt (ROI) utilisées pour la segmentation (par défaut 7).
		:param max_iterations: Nombre d'itérations pour affiner le seuil (par défaut 4).
		:return: Seuil calculé (écart type final).
		"""
		mask = np.zeros_like(image, dtype=bool)  # Creation du masque
		std_dev = float(np.std(image))			 # Calcul initial de l'écart type
		roi_2 = float(roi_size) / 2.0			 # Demi-taille de la zone ROI
		height, width = image.shape				 # Récupération de la taille de l'image

		for _ in range(max_iterations):
			# Lancement d'un PALM et récupération de la liste des points (format (x, y))
			points = self.run(image, std_dev, False, 0, 1, math.pi / 4.0, roi_size)
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
