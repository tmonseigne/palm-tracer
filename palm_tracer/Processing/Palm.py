"""Encapsule la DLL PALM et ses algorithmes de détection et de suivi."""

from __future__ import annotations

import ctypes
from dataclasses import dataclass, field
from typing import Optional

import numpy as np
import pandas as pd
import psutil

from palm_tracer.Processing import Parsing
from palm_tracer.Tools import FileIO

N_TRC_CP_FIT = 12
DENSITY = 0.1

C_IMG, C_TAB_DBL, C_TAB_UINT = ctypes.POINTER(ctypes.c_uint16), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_uint64)
C_UINT, C_BOOL, C_DBL = ctypes.c_uint64, ctypes.c_bool, ctypes.c_double


##################################################
@dataclass
class Palm:
	"""
	Encapsule le chargement et les appels aux algorithmes de la DLL PALM.

	L'instance configure les signatures des fonctions natives et convertit leurs entrées et sorties vers les structures Python utilisées par le pipeline.
	"""

	_type: str = field(init=False, default="CPU")
	"""Type de DLL, par défaut CPU, GPU également possible."""
	_dll: ctypes.CDLL = field(init=False)
	"""DLL chargée."""

	# ==================================================
	# region Initialization
	# ==================================================
	##################################################
	def __post_init__(self):
		"""Méthode appelée automatiquement après l'initialisation du dataclass."""
		self._dll = FileIO.load_dll(self._type)
		self._bind()

	##################################################
	def is_valid(self) -> bool:
		"""
		Vérifie la validité de la DLL utilisée pour PALM.

		:return: True si la DLL est valide, False sinon.
		"""
		return self._dll is not None

	##################################################
	def _bind(self):
		"""Déclare les signatures ctypes (argtypes/restype) une seule fois."""

		# double AutoThreshold(uint16_t* image, uint64_t h, uint64_t w, double* fit_params)
		fn = self._dll.AutoThreshold
		fn.restype = C_DBL
		fn.argtypes = [C_IMG, C_UINT, C_UINT, C_TAB_DBL]

		# uint64_t Localization(uint16_t* stack, double* locs, uint64_t n, uint64_t h, uint64_t w, uint64_t planes,
		# double thr, double watershed, uint64_t fit, double* fit_params)
		fn = self._dll.Localization
		fn.restype = C_UINT
		fn.argtypes = [C_IMG, C_TAB_DBL, C_UINT, C_UINT, C_UINT, C_UINT, C_DBL, C_DBL, C_UINT, C_TAB_DBL]

		# uint64_t Tracking(double* points, double* tracks, uint64_t n_points, double max_dist)
		fn = self._dll.Tracking
		fn.argtypes = [C_TAB_DBL, C_TAB_UINT, C_UINT, C_DBL]

		# uint64_t BlinkingReconnection(double* input, double* output, uint64_t nRow, double pixel_size, uint64_t mode,
		# uint64_t max_duration, double max_speed)
		fn = self._dll.BlinkingReconnection
		fn.restype = C_UINT
		fn.argtypes = [C_TAB_DBL, C_TAB_DBL, C_UINT, C_DBL, C_UINT, C_UINT, C_DBL]

		# bool TracksCompute(double* input, double* o_msd, double* o_ind, double* o_fit, uint64_t nRow, bool is_msd, bool is_ind, bool is_3d,
		# double pixel_size, double exposure_time, uint64_t fit_mode, double* fit_params)
		fn = self._dll.TracksCompute
		fn.restype = C_BOOL
		fn.argtypes = [C_TAB_DBL, C_TAB_DBL, C_TAB_DBL, C_TAB_DBL, C_UINT, C_BOOL, C_BOOL, C_BOOL, C_DBL, C_DBL, C_UINT, C_TAB_DBL]

		# void Alignment(uint16_t* input, uint16_t* output, uint64_t h, uint64_t w, uint64_t planes, double* factors, uint64_t upsampling)
		fn = self._dll.Alignment
		fn.restype = None
		fn.argtypes = [C_IMG, C_IMG, C_UINT, C_UINT, C_UINT, C_TAB_DBL, C_UINT]

		# void Wavelett(uint16_t* input, double* output, uint64_t h, uint64_t w, uint64_t planes, uint64_t level)
		fn = self._dll.Wavelett
		fn.restype = None
		fn.argtypes = [C_IMG, C_TAB_DBL, C_UINT, C_UINT, C_UINT, C_UINT]

		# void Astigmatism3DCalibration(const double* input, double* output, uint64_t size, double pixelSize)
		fn = self._dll.Astigmatism3DCalibration
		fn.restype = None
		fn.argtypes = [C_TAB_DBL, C_TAB_DBL, C_UINT, C_DBL, C_BOOL]

		# void Astigmatism3DEstimation(const double* input, double* output, uint64_t size, double pixelSize, double* model, double zMax)
		fn = self._dll.Astigmatism3DEstimation
		fn.restype = None
		fn.argtypes = [C_TAB_DBL, C_TAB_DBL, C_UINT, C_DBL, C_TAB_DBL, C_DBL]

	# ==================================================
	# endregion Initialization
	# ==================================================

	# ==================================================
	# region Argument Parser
	# ==================================================
	##################################################
	@staticmethod
	def _as_c_contig(a: np.ndarray, dtype: np.dtype, *, writeable: bool) -> np.ndarray:
		"""
		Retourne un tableau C-contigu du dtype demandé, sans copie si possible.

		:param a: Tableau d'entrée.
		:param dtype: Dtype souhaité.
		:param writeable: Garantit un buffer modifiable si True.
		:return: Tableau C-contigu compatible DLL.
		"""
		if not isinstance(a, np.ndarray): a = np.asarray(a)

		# Vérification de copie nécessaire ou non
		if (a.dtype != dtype) or (not a.flags["C_CONTIGUOUS"]) or (writeable and not a.flags["WRITEABLE"]):
			a = np.ascontiguousarray(a, dtype=dtype)  # Rend contigu
			if writeable: a.setflags(write=True)  # .	Rend modifiable ou non
		return a

	##################################################
	@staticmethod
	def max_allocation_bytes(fraction_available: float = 0.5, safety_gb: int = 1) -> int:
		"""
		Permet de calculer la quantité de mémoire disponible au maximum pour une allocation.

		:param fraction_available: Pourcentage de la RAM disponible à utiliser au maximum.
		:param safety_gb: Marge de sécurité à garder disponible.
		:return: Valeur en byte de l'allocation maximum tolérée.
		"""
		giga = 1024 * 1024 * 1024
		avail = psutil.virtual_memory().available
		safety = safety_gb * giga
		budget = int(max(0, avail - safety) * fraction_available)
		return max(budget, giga)

	# ==================================================
	# endregion Argument Parser
	# ==================================================

	# ==================================================
	# region DLL Call
	# ==================================================

	##################################################
	def localization(self, stack: np.ndarray, threshold: float, watershed: bool, fit: int, fit_params: np.ndarray,
					 planes: Optional[list[int]] = None) -> pd.DataFrame:
		"""
		Exécute un traitement d'image avec une DLL PALM externe pour détecter des points dans une pile ou une image.

		:param stack: Pile d'images en entrée sous forme de tableau NumPy (possibilité d'envoyer une image directement).
		:param threshold: Seuil pour la détection.
		:param watershed: Active ou désactive le mode watershed.
		:param fit: Mode d'ajustement (défini par ``get_fit``).
		:param fit_params: Paramètres du mode d'ajustement.
		:param planes: Liste des plans à analyser (None pour tous les plans, les plans sont contigus par principe).
		:return: Liste des points détectés sous forme de DataFrame contenant toutes les informations reçues de la DLL.
		"""
		# --- Initialisation ---
		stk = self._as_c_contig(stack, np.dtype(np.uint16), writeable=False)  # .		 Assurance de contiguité
		params = self._as_c_contig(fit_params, np.dtype(np.float64), writeable=False)  # Assurance de contiguité
		height, width = stk.shape[-2:]  # .												 Récupère les deux dernières dimensions
		n_planes = 1 if stk.ndim == 2 else stk.shape[0]  # .							 Récupère le nombre de plans si 3D sinon 1
		if planes is None: planes = list(range(n_planes))  # .							 Si aucune sélection, liste de tous les plans
		else: planes = [p for p in planes if 0 <= p < n_planes]  # .					 Sinon, sélection des plans valides
		n_planes = len(planes)  # .														 Nouveau nombre de plans
		# Ajoute une dimension plan artificielle pour une Image 2D ou une vue mémoire (slice) pour une pile 3D
		stk = stk[np.newaxis, :, :] if stk.ndim == 2 else stk[planes[0]:planes[0] + n_planes]

		# --- Calcul du budget RAM Disponible ---
		max_points = int(self.max_allocation_bytes() // 8)  # .				Nombre de points maximum allouable en une fois
		plane_points = int(height * width * DENSITY) * Parsing.N_COL_LOC  # Taille théorique max pour un seul plan (N points max * N Col localisation)
		if max_points < plane_points: return pd.DataFrame()  # . 			pragma: no cover — Cas extrême un seul plan est gargantuesque.
		n_plane_max = int(min(max_points // plane_points, n_planes))  # .	Nombre de plans qui tiennent dans max_allocation

		dfs: list[pd.DataFrame] = []
		i = 0
		while i < len(planes):
			k = min(n_plane_max, n_planes - i)  # .						Taille réelle du bloc, soit le max, soit "ce qui reste".
			stk_block = stk[i:i + k]  # .								Indices relatifs (0..n_planes-1)
			n_block = plane_points * k  # . 							Nombre de points pour ce bloc
			locs = np.empty((n_block,), dtype=np.float64, order="C")  # Création de la sortie

			count = self._dll.Localization(stk_block.ctypes.data_as(C_IMG), locs.ctypes.data_as(C_TAB_DBL), C_UINT(n_block), C_UINT(height), C_UINT(width),
										   C_UINT(k), C_DBL(threshold), C_DBL(0 if watershed else 10), C_UINT(fit), params.ctypes.data_as(C_TAB_DBL))

			res = Parsing.parse_result(locs[:count], "Localization")
			if "Plane" in res.columns: res["Plane"] += planes[0] + i  # . En cas de filtre des plans, on incrémente par i + premier plan.
			dfs.append(res)
			i += k

		res = pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

		if not res.empty:
			res.reset_index(drop=True, inplace=True)
			res["Id"] = res.index + 1  # .					  1-based comme attendu
			if fit == 4:  # Fit Gaussien avec Theta
				mask = res["Integrated Intensity"] > 0
				res.loc[mask, "Theta"] = Parsing.manage_theta(res.loc[mask, "Theta"])  # Clean Theta and show stats

		return res

	##################################################
	def auto_threshold(self, image: np.ndarray, fit_params: np.ndarray) -> float:
		"""
		Calcule un seuil automatique basé sur la segmentation de l'image.

		:param image: Image 2D sous forme de tableau NumPy.
		:param fit_params: Paramètres du mode d'ajustement.
		:return: Seuil calculé (écart-type final).
		"""
		img = self._as_c_contig(image, np.dtype(np.uint16), writeable=False)  # .		 Assurance de contiguité
		params = self._as_c_contig(fit_params, np.dtype(np.float64), writeable=False)  # Assurance de contiguité
		height, width = img.shape  # .													 Récupère les dimensions
		return float(self._dll.AutoThreshold(img.ctypes.data_as(C_IMG), C_UINT(height), C_UINT(width), params.ctypes.data_as(C_TAB_DBL)))

	##################################################
	def tracking(self, localizations: pd.DataFrame, max_distance: float) -> pd.DataFrame:
		"""
		Exécute l'algorithme de tracking sur les points localisés.

		Cette méthode applique un algorithme de suivi (tracking) sur les données de localisation fournies,
		en prenant en compte divers paramètres influençant le coût et la durée de vie des trajectoires.

		:param localizations: Liste des points détectés sous forme de DataFrame contenant toutes les informations reçues de la DLL.
		:param max_distance: Distance maximale autorisée entre deux points pour les relier entre deux plans successifs.
		:return: :class:`DataFrame <pandas.DataFrame>` contenant les trajectoires détectées.
		"""
		required = Parsing.FILES_COLUMNS["Localization"]["columns"]
		if localizations.empty or not set(required).issubset(localizations.columns): return pd.DataFrame()

		points = localizations.loc[localizations["Integrated Intensity"] > 0, Parsing.COLS_FOR_TRACKING]
		if points.empty: return pd.DataFrame()  # .						En cas de dataframe qui a été vidé après le masquage des mauvais points
		n = len(points)  # .											Nombre de points
		track_size = n * 2  # .											Taille du tableau final
		tracks = np.empty((track_size,), dtype=np.uint64, order="C")  # Tableau final

		p = self._as_c_contig(points.to_numpy(), np.dtype(np.float64), writeable=False)  # Assurance de contiguité
		self._dll.Tracking(p.ctypes.data_as(C_TAB_DBL), tracks.ctypes.data_as(C_TAB_UINT), C_UINT(n), C_DBL(max_distance))

		tracks = pd.DataFrame(tracks.reshape(-1, 2), columns=["Id", "Track"])  # Passage en dataframe.
		# Ajout et remplissage de la colonne Track aux localisations.
		localizations.insert(0, "Track", localizations["Id"].map(tracks.set_index("Id")["Track"]).fillna(-1).astype(int))
		res = localizations.loc[localizations["Track"] > 0, Parsing.FILES_COLUMNS["Tracking"]["columns"]]  # On ne conserve qu'une partie des colonnes
		return res.sort_values(by=["Track", "Plane"], ascending=[True, True]).reset_index(drop=True)  # On trie le résultat final

	##################################################
	def blinking_reconnection(self, tracks: pd.DataFrame, pixel_size: float, mode: int, max_duration: int, max_speed: float) -> pd.DataFrame:
		"""
		Exécute l'algorithme de reconnexion des trajectoires sur celles déjà localisées.

		:param pixel_size: Taille des pixels en nanomètres.
		:param tracks: Liste des points déjà suivis sous forme de DataFrame contenant toutes les informations reçues de la DLL.
		:param mode: Mode de dispersion des points (0: immobile, 1: diffus, 2: linéaire).
		:param max_duration: Durée maximale d'un scintillement.
		:param max_speed: Vitesse maximale d'un point entre deux plans (en pixel).
		:return: :class:`DataFrame <pandas.DataFrame>` contenant les trajectoires détectées.
		"""
		required = Parsing.FILES_COLUMNS["Tracking"]["columns"]
		if tracks.empty or not set(required).issubset(tracks.columns): return pd.DataFrame()

		in_tracks = tracks[required].to_numpy(dtype=np.float64, copy=False)
		in_tracks = self._as_c_contig(in_tracks, np.dtype(np.float64), writeable=False)

		n = len(tracks)
		track_size = n * Parsing.N_COL_TRC
		out = np.empty((track_size,), dtype=np.float64, order="C")

		count = self._dll.BlinkingReconnection(in_tracks.ctypes.data_as(C_TAB_DBL), out.ctypes.data_as(C_TAB_DBL), C_UINT(n), C_DBL(pixel_size),
											   C_UINT(mode), C_UINT(max_duration), C_DBL(max_speed))

		return Parsing.parse_result(out[:count], "Tracking")

	##################################################
	def tracks_compute(self, tracks: pd.DataFrame, is_msd: bool, is_ind: bool, is_3d: bool, is_log: bool,
					   pixel_size: float, exposure_time: float, fit_mode: int, fit_params: np.ndarray) -> dict[str, pd.DataFrame]:
		"""
		Exécute l'algorithme de calcul sur les trajectoires.

		:param tracks: Liste des points déjà suivis sous forme de DataFrame contenant toutes les informations reçues de la DLL.
		:param is_msd: Calcul MSD.
		:param is_ind: Calcul de la diffusion instantanée.
		:param is_3d: Calcul sur la 3D.
		:param is_log: Applique un logarithme sur le résultat.
		:param pixel_size: Taille des pixels en micromètre.
		:param exposure_time: Calibration temporelle utile pour les calculs.
		:param fit_mode: Mode d'ajustement.
		:param fit_params: Paramètres de l'ajustement (pour le moment uniquement fit length).
		:return: :class:`DataFrame <pandas.DataFrame>` contenant les trajectoires détectées.

		.. note:: Pour obtenir des valeurs de diffusion en **µm²**, le paramètre ``pixel_size`` doit être exprimé en micromètres par pixel (µm/px).
		"""
		res: dict[str, pd.DataFrame] = {"MSD": pd.DataFrame(), "InD": pd.DataFrame(), "Fit": pd.DataFrame()}
		required = Parsing.FILES_COLUMNS["Tracking"]["columns"]
		if tracks.empty or not set(required).issubset(tracks.columns): return res
		in_tracks = tracks[required].copy()
		if not is_3d: in_tracks["Z"] = 0  # On simplifie, la suite les calculs se font toujours en 3D, mais la dernière dimension sera nulle

		in_tracks = in_tracks.to_numpy(dtype=np.float64, copy=False)  # .				   Passage en tableau NumPy
		in_tracks = self._as_c_contig(in_tracks, np.dtype(np.float64), writeable=False)  # Assurance de contiguité
		params = self._as_c_contig(fit_params, np.dtype(np.float64), writeable=False)  # . Assurance de contiguité
		n_row = len(tracks)  # .														   Nombre de points pour les trajectoires
		n = n_row * N_TRC_CP_FIT  # .													   Taille maximale des tableaux finaux

		# Sorties : buffer réel si demandé, sinon buffer dummy (évite pointeurs NULL)
		o_msd = np.empty((n,), dtype=np.float64, order="C") if is_msd else np.empty((1,), dtype=np.float64, order="C")
		o_ind = np.empty((n,), dtype=np.float64, order="C") if is_ind else np.empty((1,), dtype=np.float64, order="C")
		o_fit = np.empty((n,), dtype=np.float64, order="C") if fit_mode != 0 else np.empty((1,), dtype=np.float64, order="C")

		self._dll.TracksCompute(in_tracks.ctypes.data_as(C_TAB_DBL), o_msd.ctypes.data_as(C_TAB_DBL), o_ind.ctypes.data_as(C_TAB_DBL),
								o_fit.ctypes.data_as(C_TAB_DBL),
								C_UINT(n_row), C_BOOL(is_msd), C_BOOL(is_ind), C_BOOL(is_3d), C_DBL(pixel_size), C_DBL(exposure_time),
								C_UINT(fit_mode), params.ctypes.data_as(C_TAB_DBL))

		if is_msd: res["MSD"] = Parsing.parse_result(o_msd[:n], "MSD", is_log)
		if is_ind: res["InD"] = Parsing.parse_result(o_ind[:n], "Instant Diffusion", is_log)
		if fit_mode != 0: res["Fit"] = Parsing.parse_result(o_fit[:n], "Fit", is_log, fit_mode)
		return res

	##################################################
	def align(self, stack: np.ndarray, factors: np.ndarray, upsampling: int = 1) -> np.ndarray:
		"""
		Exécute un traitement d'image avec une DLL PALM externe pour détecter des points dans une pile ou une image.

		:param stack: Pile d'images en entrée sous forme de tableau NumPy (possibilité d'envoyer une image directement).
		:param factors: Facteurs d'alignement.
		:param upsampling: Facteur d'agrandissement de l'image (par défaut : ``1`` aucun agrandissement).
		:return: Image alignée.
		"""

		stk = self._as_c_contig(stack, np.dtype(np.uint16), writeable=False)  # .	  Assurance de contiguité
		params = self._as_c_contig(factors, np.dtype(np.float64), writeable=False)  # Assurance de contiguité
		height, width = stk.shape[-2:]  # .											  Récupère les deux dernières dimensions
		planes = 1 if stk.ndim == 2 else stk.shape[0]  # .							  Récupère le nombre de plans si 3D sinon 1

		out = np.empty((planes, height * upsampling, width * upsampling), dtype=np.uint16, order="C")
		self._dll.Alignment(stk.ctypes.data_as(C_IMG), out.ctypes.data_as(C_IMG), C_UINT(height), C_UINT(width), C_UINT(planes),
							params.ctypes.data_as(C_TAB_DBL), C_UINT(upsampling))
		return out

	##################################################
	def wavelett(self, stack: np.ndarray, level: int = 2) -> np.ndarray:
		"""
		Exécute un traitement d'image avec une DLL PALM externe pour détecter des points dans une pile ou une image.

		:param stack: Pile d'images en entrée sous forme de tableau NumPy (possibilité d'envoyer une image directement).
		:param level: Niveau d'ondelette en sortie.
		:return: Image décomposée.
		"""
		stk = self._as_c_contig(stack, np.dtype(np.uint16), writeable=False)  # Assurance de contiguité
		height, width = stk.shape[-2:]  # .										Récupère les deux dernières dimensions
		planes = 1 if stk.ndim == 2 else stk.shape[0]  # .						Récupère le nombre de plans si 3D sinon 1

		out = np.empty((planes, height, width), dtype=np.float64, order="C")

		self._dll.Wavelett(stk.ctypes.data_as(C_IMG), out.ctypes.data_as(C_TAB_DBL), C_UINT(height), C_UINT(width), C_UINT(planes), C_UINT(level))
		return out

	##################################################
	def astigmatism_3d_calibration(self, points: np.ndarray, pixel_size: float, center: bool = True) -> pd.DataFrame:
		"""
		Exécute un traitement avec une DLL PALM externe pour calibrer un modèle d'astigmatisme permettant d'estimer une position axiale.

		:param points: Ensemble des points nécessaire à la calibration sous forme de tableau NumPy 2D avec pour colonnes [Sigma X, Sigma Y, Z].
		:param pixel_size: Taille des pixels en nanomètres.
		:param center: Permet de centrer le modèle pour que si :math:`\\sigma_x(0) \\approx \\sigma_y(0)`.
		:return: Modèle d'astigmatisme (un tableau NumPy 2D de 2 lignes et 5 paramètres par ligne).
		"""
		pts = self._as_c_contig(points, np.dtype(np.float64), writeable=False)
		out = np.empty(Parsing.SHAPE_MODEL, dtype=np.float64, order="C")
		n = pts.shape[0]

		self._dll.Astigmatism3DCalibration(pts.ctypes.data_as(C_TAB_DBL), out.ctypes.data_as(C_TAB_DBL), C_UINT(n), C_DBL(pixel_size), C_BOOL(center))
		return Parsing.parse_result(out, "Astigmatism 3D Model")

	##################################################
	def astigmatism_3d_estimation(self, sigmas: np.ndarray, pixel_size: float, model: np.ndarray, z_max: float = 800) -> np.ndarray:
		"""
		Exécute un traitement avec une DLL PALM externe pour estimer une position axiale à partir d'un modèle.

		:param sigmas: Ensemble des points à estimer sous forme de tableau NumPy 2D avec pour colonnes [sigma_x, sigma_y].
		:param pixel_size: Taille des pixels en nanomètres.
		:param model: Modèle d'astigmatisme (un tableau NumPy 2D de 2 lignes et 5 paramètres par ligne).
		:param z_max: Distance absolue maximale sur Z par rapport à l'origine.
		:return: Ensemble des Z estimés pour chaque point.
		"""

		n = len(sigmas)
		s = self._as_c_contig(sigmas, np.dtype(np.float64), writeable=False)
		m = self._as_c_contig(model, np.dtype(np.float64), writeable=False)
		out = np.empty((n, 2), dtype=np.float64, order="C")
		self._dll.Astigmatism3DEstimation(s.ctypes.data_as(C_TAB_DBL), out.ctypes.data_as(C_TAB_DBL), C_UINT(n), C_DBL(pixel_size),
										  m.ctypes.data_as(C_TAB_DBL), C_DBL(z_max))

		return out
