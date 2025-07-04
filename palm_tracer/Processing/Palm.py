"""
Fichier contenant une classe pour utiliser la DLL externe CPU_PALM, exécuter les algorithmes de détection de points et les paramètres liés.

.. todo::
	Doit-on garder les identifiants et les plans qui vont de 1 à N au lieu du classique 0 à N-1 ?
"""

import ctypes
from dataclasses import dataclass, field
from typing import Any, Optional

import numpy as np
import pandas as pd

from palm_tracer.Processing.Parsing import get_max_points, N_TRACK, parse_localization_to_tracking, parse_result
from palm_tracer.Tools.Utils import load_dll


##################################################
@dataclass
class Palm:
	""" Classe permettant d'utiliser la DLL externe PALM, exécuter les algorithmes de détection de points et les paramètres liés. """
	_type: str = field(init=True, default="CPU")
	"""Type de DLL, par défaut CPU, GPU également possible."""
	_dll: ctypes.CDLL = field(init=False)
	"""DLL chargée."""

	##################################################
	def __post_init__(self):
		"""Méthode appelée automatiquement après l'initialisation du dataclass."""
		self._dll = load_dll(self._type)

	##################################################
	def is_valid(self) -> bool:
		"""
		Vérifie la validité de la DLL utilisée pour PALM.

		:return: True si la DLL est valide, False sinon.
		"""
		return self._dll is not None

	##################################################
	@staticmethod
	def __get_auto_treshold_args(image: np.ndarray, height: int, width: int, fit_params: np.ndarray):
		"""
		Initialise les arguments necessaire au lancement de la DLL PALM externe pour la localisation.

		:param image: Image 2D sous forme de tableau NumPy.
		:param height: Hauteur des images.
		:param width: Largeur des images.
		:param fit_params: Paramètres de l'ajustement.
		:return: Dictionniare d'arguments pour la DLL (attention l'ordre doit être respecté).
		"""
		return {
				"image":      np.asarray(image, dtype=np.uint16).flatten().ctypes.data_as(ctypes.POINTER(ctypes.c_ushort)),  # Image
				"height":     ctypes.c_ulong(height),									  # Hauteur (nombre de lignes)
				"width":      ctypes.c_ulong(width),									  # Largeur (nombre de colonnes)
				"fit_params": fit_params.ctypes.data_as(ctypes.POINTER(ctypes.c_double))  # Paramètres pour l'ajustement
				}

	##################################################
	@staticmethod
	def __get_locs_args(stack: np.ndarray, height: int, width: int, planes: int, threshold: float, watershed: bool, fit: int, fit_params: np.ndarray):
		"""
		Initialise les arguments necessaire au lancement de la DLL PALM externe pour la localisation.

		:param stack: Pile d'images en entrée sous forme de tableau numpy 3D.
		:param height: Hauteur des images.
		:param width: Largeur des images.
		:param planes: Nombre de plans.
		:param threshold: Seuil pour la détection.
		:param watershed: Active ou désactive le mode watershed.
		:param fit: Mode d'ajustement.
		:param fit_params: Paramètres de l'ajustement.
		:return: Dictionniare d'arguments pour la DLL (attention l'ordre doit être respecté).
		"""
		# Parsing
		n = get_max_points(height, width, planes)  # Récupération d'un nombre de points maximum théorique
		return {
				"stack":      np.asarray(stack, dtype=np.uint16).flatten().ctypes.data_as(ctypes.POINTER(ctypes.c_ushort)),  # Pile
				"locs":       np.zeros((n,), dtype=np.float64).ctypes.data_as(ctypes.POINTER(ctypes.c_double)),				 # Tableau pour la localisation
				"n":          ctypes.c_ulong(n),						# Nombre maximum de localisation théoriques lors de la localization
				"height":     ctypes.c_ulong(height),					# Hauteur (nombre de lignes)
				"width":      ctypes.c_ulong(width),					# Largeur (nombre de colonnes)
				"planes":     ctypes.c_ulong(planes),					# Profondeur (nombre de plans)
				"threshold":  ctypes.c_double(threshold),				# Seuil de détection
				"watershed":  ctypes.c_double(0 if watershed else 10),  # Seuil du Watershed
				"fit":        ctypes.c_ushort(fit),						# Mode d'ajustement
				"fit_params": fit_params.ctypes.data_as(ctypes.POINTER(ctypes.c_double))  # Paramètres pour l'ajustement
				}

	##################################################
	@staticmethod
	def __get_tracks_args(localizations: pd.DataFrame, max_distance: float, min_life: int, decrease: float, cost_birth: float) -> dict[str, Any]:
		"""
		Initialise les arguments necessaire au lancement de la DLL PALM externe pour le tracking.

		:param localizations: Liste des points détectés sous forme de dataframe contenant toutes les informations reçu de la DLL.
		:param max_distance: Distance maximale autorisée entre deux points pour les relier entre deux frames successives.
		:param min_life: Longueur minimale d'une trajectoire pour qu'elle soit conservée dans le résultat final.
		:param decrease: Facteur de pénalisation appliqué au coût d'association entre frames éloignées.
		:param cost_birth: Coût associé à la création d'une nouvelle trajectoire (point non associé à une trajectoire existante).
		:return: Dictionniare d'arguments pour la DLL (attention l'ordre doit être respecté).
		"""
		n = len(localizations)
		track_size = n * N_TRACK
		points = parse_localization_to_tracking(localizations)

		return {"points":       points.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
				"tracks":       np.zeros((track_size,), dtype=np.float64).ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
				"max_distance": ctypes.c_double(max_distance),
				"min_life":     ctypes.c_ulong(min_life),
				"decrease":     ctypes.c_double(decrease),
				"cost_birth":   ctypes.c_double(cost_birth),
				"planes":       ctypes.c_ulong(localizations["Plane"].max()),  # Nombre de plans
				}

	##################################################
	def localization(self, stack: np.ndarray, threshold: float, watershed: bool, fit: int, fit_params: np.ndarray,
					 planes: Optional[list[int]] = None) -> pd.DataFrame:
		"""
		Exécute un traitement d'image avec une DLL PALM externe pour détecter des points dans une pile ou une image.

		:param stack: Pile d'images en entrée sous forme de tableau numpy (possibilité d'envoyer une image directement).
		:param threshold: Seuil pour la détection.
		:param watershed: Active ou désactive le mode watershed.
		:param fit: Mode d'ajustement (défini par `get_fit`).
		:param fit_params: Paramètres du mode d'ajustement.
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
		new_stack = stack[np.newaxis, :, :] if stack.ndim == 2 else stack[planes[0]:planes[-1] + 1]

		args = self.__get_locs_args(new_stack, height, width, new_n_planes, threshold, watershed, fit, fit_params)
		count = self._dll.Localization(*args.values())
		res = parse_result(np.ctypeslib.as_array(args["locs"], shape=(count,)), "Localization")
		if planes[0] != 0: res["Plane"] += planes[0]  # en cas de filtre de plans
		return res

	##################################################
	def auto_threshold(self, image: np.ndarray, fit_params: np.ndarray) -> float:
		"""
		Calcule un seuil automatique basé sur la segmentation de l'image.

		:param image: Image 2D sous forme de tableau NumPy.
		:param fit_params: Paramètres du mode d'ajustement.
		:return: Seuil calculé (écart type final).
		"""
		height, width = image.shape  # Récupère les dimensions
		args = self.__get_auto_treshold_args(image, height, width, fit_params) # Récupère les arguments pour la DLL
		self._dll.AutoThreshold.restype = ctypes.c_double					   # Force le type de retour
		return self._dll.AutoThreshold(*args.values())


	##################################################
	def tracking(self, localizations: pd.DataFrame, max_distance: float, min_life: int, decrease: float, cost_birth: float) -> pd.DataFrame:
		"""
		Exécute l'algorithme de tracking sur les points localisés.

		Cette méthode applique un algorithme de suivi (tracking) sur les données de localisation fournies,
		en prenant en compte divers paramètres influençant le coût et la durée de vie des trajectoires.

		:param localizations: Liste des points détectés sous forme de dataframe contenant toutes les informations reçu de la DLL.
		:param max_distance: Distance maximale autorisée entre deux points pour les relier entre deux frames successives.
		:param min_life: Longueur minimale d'une trajectoire pour qu'elle soit conservée dans le résultat final.
		:param decrease: Facteur de pénalisation appliqué au coût d'association entre frames éloignées.
		:param cost_birth: Coût associé à la création d'une nouvelle trajectoire (point non associé à une trajectoire existante).
		:return: DataFrame contenant les trajectoires détectées.
		"""
		args = self.__get_tracks_args(localizations, max_distance, min_life, decrease, cost_birth)
		count = self._dll.Tracking(*args.values())
		return parse_result(np.ctypeslib.as_array(args["tracks"], shape=(count,)), "Tracking")
