""" Fichier contenant une classe pour utiliser la DLL externe Tracking. """

import ctypes
from dataclasses import dataclass, field
from typing import Any

import numpy as np
import pandas as pd

from palm_tracer.Processing.Parsing import N_TRACK, parse_localization_to_tracking, parse_tracking_result
from palm_tracer.Tools.Utils import load_dll


##################################################
@dataclass
class Tracking:
	""" Classe permettant d'utiliser la DLL externe Tracking_PALM, exécuter les algorithmes de détection de tracks et les paramètres liés. """
	_dll: ctypes.CDLL = field(init=False)
	"""DLL chargée."""
	_track_size: int = field(init=False, default=0)
	"""Taille maximale du tableau de tracking."""

	##################################################
	def __post_init__(self):
		"""Méthode appelée automatiquement après l'initialisation du dataclass."""
		self._dll = load_dll("Tracking")

	##################################################
	def is_valid(self) -> bool:
		"""
		Vérifie la validité de la DLL utilisée pour le Tracking.

		:return: True si la DLL est valide, False sinon.
		"""
		return self._dll is not None

	##################################################
	def __get_args(self, localizations: pd.DataFrame, max_distance: float, min_life: int,
				   decrease: float, cost_birth: float) -> dict[str, Any]:
		"""
		Initialise les arguments necessaire au lancement de la DLL Tracking.

		:param localizations: Liste des points détectés sous forme de dataframe contenant toutes les informations reçu de la DLL.
		:param max_distance: Distance maximale autorisée entre deux points pour les relier entre deux frames successives.
		:param min_life: Longueur minimale d'une trajectoire pour qu'elle soit conservée dans le résultat final.
		:param decrease: Facteur de pénalisation appliqué au coût d'association entre frames éloignées.
		:param cost_birth: Coût associé à la création d'une nouvelle trajectoire (point non associé à une trajectoire existante).
		:return: Dictionniare d'arguments pour la DLL (attention l'ordre doit être respecté).
		"""
		n = len(localizations)
		self._track_size = n * N_TRACK
		points = parse_localization_to_tracking(localizations)

		return {"points":       points.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
				"track":        np.zeros((self._track_size,), dtype=np.float64).ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
				"max_distance": ctypes.c_double(max_distance),
				"min_life":     ctypes.c_ulong(min_life),
				"decrease":     ctypes.c_double(decrease),
				"cost_birth":   ctypes.c_double(cost_birth),
				"planes":       ctypes.c_ulong(localizations["Plane"].max()),  # Nombre de plans
				}

	##################################################
	def run(self, localizations: pd.DataFrame, max_distance: float, min_life: int, decrease: float, cost_birth: float) -> pd.DataFrame:
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
		args = self.__get_args(localizations, max_distance, min_life, decrease, cost_birth)
		self._dll.Process(*args.values())
		return parse_tracking_result(np.ctypeslib.as_array(args["track"], shape=(self._track_size,)))
