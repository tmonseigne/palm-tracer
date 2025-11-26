"""
Fichier contenant une classe pour utiliser la DLL externe CPU_PALM, exécuter les algorithmes de détection de points et les paramètres liés.
"""

import ctypes
from dataclasses import dataclass, field
from typing import Any, Optional

import numpy as np
import pandas as pd

from palm_tracer.Processing.Parsing import (get_max_points, log10_dataframe, N_COL_TRC, parse_irregular_array,
											parse_localization_to_tracking, parse_result, PARSING_COLUMNS)
from palm_tracer.Tools.Utils import load_dll, print_warning

N_TRC_CP_FIT = 10


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
		:return: Dictionnaire d'arguments pour la DLL (attention l'ordre doit être respecté).
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
		:return: Dictionnaire d'arguments pour la DLL (attention l'ordre doit être respecté).
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
	def __get_tracks_args(localizations: pd.DataFrame, max_distance: float, min_life: int = 1,
						  decrease: float = 10, cost_birth: float = 0.5) -> dict[str, Any]:
		"""
		Initialise les arguments necessaire au lancement de la DLL PALM externe pour le tracking.

		:param localizations: Liste des points détectés sous forme de dataframe contenant toutes les informations reçu de la DLL.
		:param max_distance: Distance maximale autorisée entre deux points pour les relier entre deux frames successives.
		:param min_life: Longueur minimale d'une trajectoire pour qu'elle soit conservée dans le résultat final.
		:param decrease: Facteur de pénalisation appliqué au coût d'association entre frames éloignées.
		:param cost_birth: Coût associé à la création d'une nouvelle trajectoire (point non associé à une trajectoire existante).
		:return: Dictionnaire d'arguments pour la DLL (attention l'ordre doit être respecté).
		"""
		n = len(localizations)
		track_size = n * N_COL_TRC
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
	@staticmethod
	def __get_blink_args(tracks: pd.DataFrame, pixel_size: float, mode: int, max_duration: int, max_speed: float) -> dict[str, Any]:
		"""
		Initialise les arguments necessaire au lancement de la DLL PALM externe pour la reconnexion du scintillement.

		:param tracks: Liste des points déjà trackés sous forme de dataframe contenant toutes les informations reçu de la DLL.
		:param pixel_size: Calibration spatiale utile pour les calculs (en micromètre)
		:param mode: Mode de dispersion des points (0: immobile, 1: diffus, 2: linéaire).
		:param max_duration: Durée maximale d'un scintillemnt.
		:param max_speed: Vitesse maximale d'un point entre deux plans (en micromètre).
		:return: Dictionnaire d'arguments pour la DLL (attention l'ordre doit être respecté).
		"""
		n = len(tracks)
		track_size = n * N_COL_TRC

		return {"input":        np.asarray(tracks, dtype=np.float64).flatten().ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
				"output":       np.zeros((track_size,), dtype=np.float64).ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
				"nRow":         ctypes.c_ulong(n),
				"pixel_size":   ctypes.c_double(pixel_size),
				"mode":         ctypes.c_ulong(mode),
				"max_duration": ctypes.c_ulong(max_duration),
				"max_speed":    ctypes.c_double(max_speed),
				}

	##################################################
	@staticmethod
	def __get_tc_args(tracks: pd.DataFrame, is_msd: bool, is_ind: bool, is_3d: bool,
					  pixel_size: float, exposure_time, fit_mode: int, fit_params: np.ndarray) -> dict[str, Any]:
		"""
		Initialise les arguments necessaire au lancement de la DLL PALM externe pour le calcul sur les trajectoires.

		:param tracks: Liste des points déjà trackés sous forme de dataframe contenant toutes les informations reçu de la DLL.
		:param is_msd: Calcul MSD à effectuer si vrai.
		:param is_ind: Calcul Instant Diffusion à effectuer si vrai.
		:param is_3d: Calcul sur la 3D.
		:param pixel_size: Calibration spatiale utile pour les calculs.
		:param exposure_time: Calibration temporelle utile pour les calculs.
		:param fit_mode: Mode d'ajustement.
		:param fit_params: Paramètres de l'ajustement (pour le moment uniquement fit length).
		:return: Dictionnaire d'arguments pour la DLL (attention l'ordre doit être respecté).
		"""
		n = len(tracks)
		o_size = n * N_TRC_CP_FIT  # Fit max N valeurs par track donc dans le pire des cas des tracks de 1 points.

		return {"input":         np.asarray(tracks, dtype=np.float64).flatten().ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
				"o_msd":         np.zeros((o_size,), dtype=np.float64).ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
				"o_ind":         np.zeros((o_size,), dtype=np.float64).ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
				"o_fit":         np.zeros((o_size,), dtype=np.float64).ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
				"nRow":          ctypes.c_ulong(n),
				"is_msd":        ctypes.c_bool(is_msd),
				"is_ind":        ctypes.c_bool(is_ind),
				"is_3d":         ctypes.c_bool(is_3d),
				"pixel_size":    ctypes.c_double(pixel_size),
				"exposure_time": ctypes.c_double(exposure_time),
				"fit_mode":      ctypes.c_ulong(fit_mode),
				"fit_params":    fit_params.ctypes.data_as(ctypes.POINTER(ctypes.c_double))  # Paramètres pour l'ajustement
				}

	##################################################
	@staticmethod
	def __get_align_args(stack: np.ndarray, height: int, width: int, planes: int, factors: np.ndarray, upsampling: int):
		"""
		Initialise les arguments necessaire au lancement de la DLL PALM externe pour l'alignement.

		:param stack: Pile d'images en entrée sous forme de tableau numpy 3D.
		:param height: Hauteur des images.
		:param width: Largeur des images.
		:param planes: Nombre de plans.
		:param factors: Facteurs d'alignement.
		:param upsampling: Facteur d'agrandissement de l'image.
		:return: Dictionnaire d'arguments pour la DLL (attention l'ordre doit être respecté).
		"""
		out = np.zeros((planes, height * upsampling, width * upsampling), dtype=np.uint16)
		return {
				"input":      stack.flatten().ctypes.data_as(ctypes.POINTER(ctypes.c_ushort)),    # Pile
				"output":     out.flatten().ctypes.data_as(ctypes.POINTER(ctypes.c_ushort)),	  # Sortie
				"height":     ctypes.c_ulong(height),											  # Hauteur (nombre de lignes)
				"width":      ctypes.c_ulong(width),											  # Largeur (nombre de colonnes)
				"planes":     ctypes.c_ulong(planes),											  # Profondeur (nombre de plans)
				"factors":    factors.flatten().ctypes.data_as(ctypes.POINTER(ctypes.c_double)),  # Factor de transformation
				"upsampling": ctypes.c_ulong(upsampling)										  # Upsampling
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
		height, width = image.shape												# Récupère les dimensions
		args = self.__get_auto_treshold_args(image, height, width, fit_params)  # Récupère les arguments pour la DLL
		self._dll.AutoThreshold.restype = ctypes.c_double						# Force le type de retour
		return self._dll.AutoThreshold(*args.values())

	##################################################
	def tracking(self, localizations: pd.DataFrame, max_distance: float, min_life: int = 1, decrease: float = 10, cost_birth: float = 0.5) -> pd.DataFrame:
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
		required = PARSING_COLUMNS["Localization"]["columns"]
		if localizations.empty or not set(required).issubset(localizations.columns): return pd.DataFrame()
		args = self.__get_tracks_args(localizations[required], max_distance, min_life, decrease, cost_birth)
		count = self._dll.Tracking(*args.values())
		return parse_result(np.ctypeslib.as_array(args["tracks"], shape=(count,)), "Tracking")

	##################################################
	def blinking_reconnection(self, tracks: pd.DataFrame, pixel_size: float, mode: int, max_duration: int, max_speed: float) -> pd.DataFrame:
		"""
		Exécute l'algorithme de reconnexion des trajectoires sur celles déjà localisées.

		:param pixel_size: Taille des pixels en micromètres.
		:param tracks: Liste des points déjà trackés sous forme de dataframe contenant toutes les informations reçu de la DLL.
		:param mode: Mode de dispersion des points (0: immobile, 1: diffus, 2: linéaire).
		:param max_duration: Durée maximale d'un scintillemnt.
		:param max_speed: Vitesse maximale d'un point entre deux plans (en pixel).
		:return: DataFrame contenant les trajectoires détectées.
		"""
		required = PARSING_COLUMNS["Tracking"]["columns"]
		if tracks.empty or not set(required).issubset(tracks.columns): return pd.DataFrame()
		args = self.__get_blink_args(tracks[required], pixel_size, mode, max_duration, max_speed)
		count = self._dll.BlinkingReconnection(*args.values())
		return parse_result(np.ctypeslib.as_array(args["output"], shape=(count,)), "Tracking")

	##################################################
	def tracks_compute(self, tracks: pd.DataFrame, is_msd: bool, is_ind: bool, is_3d: bool, is_log: bool,
					   pixel_size: float, exposure_time: float, fit_mode: int, fit_params: np.ndarray) -> dict[str, pd.DataFrame]:
		"""
		Exécute l'algorithme de calcul sur les trajectoires.

		:param pixel_size: Taille des pixels en micromètres.
		:param tracks: Liste des points déjà trackés sous forme de dataframe contenant toutes les informations reçu de la DLL.
		:param is_msd: Calcul MSD à effectuer si vrai.
		:param is_ind: Calcul Instant Diffusion à effectuer si vrai.
		:param is_3d: Calcul sur la 3D.
		:param is_log: Applique un logarithme sur le résultat.
		:param pixel_size: Calibration spatiale utile pour les calculs.
		:param exposure_time: Calibration temporelle utile pour les calculs.
		:param fit_mode: Mode d'ajustement.
		:param fit_params: Paramètres de l'ajustement (pour le moment uniquement fit length).
		:return: DataFrame contenant les trajectoires détectées.
		"""
		res: dict[str, pd.DataFrame] = {"MSD": pd.DataFrame(), "InD": pd.DataFrame(), "Fit": pd.DataFrame()}
		required = PARSING_COLUMNS["Tracking"]["columns"]
		if tracks.empty or not set(required).issubset(tracks.columns): return res
		new_tracks = tracks[required].copy()
		if not is_3d: new_tracks["Z"] = 0  # On simplifie la suite les calculs se font toujours en 3D mais la dernière dimension sera toujours nulle
		args = self.__get_tc_args(new_tracks, is_msd, is_ind, is_3d, pixel_size, exposure_time, fit_mode, fit_params)
		self._dll.TracksCompute.restype = ctypes.c_bool  # Force le type de retour
		self._dll.TracksCompute(*args.values())  # Le retour est toujours vrai pour le moment les calculs manquant sont facilement trouvable.

		# Remplissage des tableaux de sortie
		n = len(tracks) * N_TRC_CP_FIT

		if is_msd:
			res["MSD"] = parse_irregular_array(np.ctypeslib.as_array(args["o_msd"], shape=(n,)))
			ncols = res["MSD"].shape[1]
			if ncols != 0:
				cols = [f"Lag {i}" for i in range(1, ncols)]
				res["MSD"].columns = ["Track"] + cols
				# Track en entier nullable (préserve les NaN si présents)
				if "Track" in res["MSD"]: res["MSD"]["Track"] = pd.to_numeric(res["MSD"]["Track"], errors="coerce").astype("Int64")
				# Mise à jour en fonction de la mise à l'échelle du Log.
				if is_log: res["MSD"] = log10_dataframe(res["MSD"], cols)

		if is_ind:
			res["InD"] = parse_irregular_array(np.ctypeslib.as_array(args["o_ind"], shape=(n,)))
			ncols = res["InD"].shape[1]
			if ncols != 0:
				cols = [f"Window {i}" for i in range(1, ncols)]
				res["InD"].columns = ["Track"] + cols
				# Track en entier nullable (préserve les NaN si présents)
				if "Track" in res["InD"]: res["InD"]["Track"] = pd.to_numeric(res["InD"]["Track"], errors="coerce").astype("Int64")
				# Mise à jour en fonction de la mise à l'échelle du Log.
				if is_log: res["InD"] = log10_dataframe(res["InD"], cols)

		if fit_mode != 0:
			res["Fit"] = parse_irregular_array(np.ctypeslib.as_array(args["o_fit"], shape=(n,)))
			ncols = res["Fit"].shape[1]
			if ncols != 0:
				# les colonnes dépendent du fit
				cols = ["Total Intensity", "D(0) (μm²/s)", "MSD(0) (μm²)", "MSE(0)"]
				if fit_mode == 1: cols += ["A (μm²/s)", "B (μm²)", "MSE"]
				elif fit_mode == 2: cols += ["Alpha", "B (μm²)", "MSE", "Average Speed (Last-First)(μm/s)"]
				elif fit_mode == 3: cols += ["A (μm²)", "B (s)", "C (μm²)", "MSE", "Confinement Radius (μm)"]
				res["Fit"].columns = ["Track", "Length"] + cols
				# Track et length en entier nullable (préserve les NaN si présents)
				res["Fit"]["Track"] = pd.to_numeric(res["Fit"]["Track"], errors="coerce").astype("Int64")
				res["Fit"]["Length"] = pd.to_numeric(res["Fit"]["Length"], errors="coerce").astype("Int64")
				# Mise à jour en fonction de la mise à l'échelle du Log.
				if is_log: res["Fit"] = log10_dataframe(res["Fit"], cols)

		# Restauration des identifiants de trajectoire
		# TODO un fix devra être fait dans la DLL pour qu'elle stocke l'identifiant elle même et que cette partie devienne inutile
		track_ids = pd.unique(tracks["Track"])
		for key in res:
			if len(res[key]) != track_ids.size: print_warning("Problème avec les identifiants des trajectoires, attention au filtrage")
			else:
				res[key].drop(columns=["Track"], inplace=True)
				res[key].insert(0, "Track", track_ids)
		return res

	##################################################
	def align(self, stack: np.ndarray, factors: np.ndarray, upsampling: int = 1) -> np.ndarray:
		"""
		Exécute un traitement d'image avec une DLL PALM externe pour détecter des points dans une pile ou une image.

		:param stack: Pile d'images en entrée sous forme de tableau numpy (possibilité d'envoyer une image directement).
		:param factors: Facteurs d'alignement.
		:param upsampling: Facteur d'agrandissement de l'image (par défaut : `1` aucun agrandissement).
		:return: Image alignée.
		"""
		height, width = stack.shape[-2:]  # Récupère les deux dernières dimensions
		planes = 1 if stack.ndim == 2 else stack.shape[0]

		args = self.__get_align_args(stack, height, width, planes, factors, upsampling)
		self._dll.Alignment(*args.values())
		out = np.ctypeslib.as_array(args["output"], shape=(planes, height * upsampling, width * upsampling))
		return out
