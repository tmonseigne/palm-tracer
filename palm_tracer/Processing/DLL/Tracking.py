""" Fichier contenant une classe pour utiliser la DLL externe Tracking. """

import ctypes
from dataclasses import dataclass, field
# from concurrent.futures import ProcessPoolExecutor, as_completed, ThreadPoolExecutor
from typing import Any

import numpy as np
import pandas as pd

from palm_tracer.Processing.DLL.Load import load_dll
from palm_tracer.Processing.DLL.Parsing import N_TRACK, parse_localization_to_tracking, parse_tracking_result


##################################################
@dataclass
class Tracking:
	""" Classe permettant d'utiliser la DLL externe Tracking_PALM, exécuter les algorithmes de détection de tracks et les paramètres liés. """
	_dll: ctypes.CDLL = field(init=False)
	_track_size: int = field(init=False, default=0)

	##################################################
	def __post_init__(self):
		"""Méthode appelée automatiquement après l'initialisation du dataclass."""
		self._dll = load_dll("Tracking")

	##################################################
	def is_valid(self): return self._dll is not None

	##################################################
	def __get_args(self, localizations: pd.DataFrame, max_distance: float, min_life: int,
				   decrease: float, cost_birth: float) -> dict[str, Any]:
		"""
		Exécute un traitement d'image avec une DLL PALM externe pour détecter des points dans une image.

		:param localizations: Liste des points détectés sous forme de dataframe contenant toutes les informations reçu de la DLL.
		:param max_distance:
		:param min_life:
		:param decrease:
		:param cost_birth:
		:return:
		"""
		n = len(localizations)
		self._track_size = n * N_TRACK
		points = parse_localization_to_tracking(localizations)

		return {"points":       points.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),  # Liste de points
				"track":        np.zeros((self._track_size,), dtype=np.float64).ctypes.data_as(ctypes.POINTER(ctypes.c_double)),  # Liste de tracks
				"max_distance": ctypes.c_double(max_distance),  #
				"min_life":     ctypes.c_ulong(min_life),  #
				"decrease":     ctypes.c_double(decrease),  #
				"cost_birth":   ctypes.c_double(cost_birth),  #
				"planes":       ctypes.c_ulong(localizations["Plane"].max()),  # Nombre de plans
				}

	##################################################
	def run(self, localizations: pd.DataFrame, max_distance: float, min_life: int, decrease: float, cost_birth: float) -> pd.DataFrame:
		"""

		:param localizations: Liste des points détectés sous forme de dataframe contenant toutes les informations reçu de la DLL.
		:param max_distance:
		:param min_life:
		:param decrease:
		:param cost_birth:
		:return:
		"""
		args = self.__get_args(localizations, max_distance, min_life, decrease, cost_birth)
		# Running
		self._dll.Process(*args.values())
		# self._dll.Tracking(*args.values())

		return parse_tracking_result(np.ctypeslib.as_array(args["track"], shape=(self._track_size,)))
