"""
Module contenant les fonctions de traitement de PALM.

.. todo:: Ajouter clairement un point dans la doc sur le systeme de filtre, l'enregistrement, le calcul sur l'intégralité des éléments
		  et filtre ensuite lors de la visualisation des graph et des sauvegarde si la case est coché...
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, cast, Optional

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from palm_tracer.Processing import Gallery, Palm, Parsing, Visualization as Viz
from palm_tracer.Processing.Drift import extract_beads
from palm_tracer.Settings import Settings
from palm_tracer.Settings.Groups import BaseSettingGroup, FilteringL, FilteringT
from palm_tracer.Settings.Groups.VisualizationGraph import GRAPH_MODE, GRAPH_SOURCE
from palm_tracer.Settings.Groups.VisualizationHR import HR_LOC_SOURCE, HR_TRC_SOURCE
from palm_tracer.Settings.Types import CheckRangeFloat, CheckRangeInt
from palm_tracer.Tools import FileIO, Logger, Ui
from palm_tracer.Tools.Ui import print_warning

MAX_UI_16 = np.iinfo(np.uint16).max


##################################################
@dataclass
class PALMTracer:
	"""Classe principale de PALM Tracer."""

	settings: Settings = field(init=False, default_factory=Settings)
	"""Classe principale des paramètres PALMTracer."""
	palm: Palm = field(init=False, default_factory=Palm)
	"""Interface vers la DLL C++ Palm."""
	_logger: Logger = field(init=False, default_factory=Logger)
	"""Journal d'activité."""
	df: dict[str, pd.DataFrame] = field(init=False, default_factory=lambda: {
			"loc":   pd.DataFrame(), "dft": pd.DataFrame(), "bds": pd.DataFrame(), "trc": pd.DataFrame(), "blk": pd.DataFrame(),
			"MSD":   pd.DataFrame(), "InD": pd.DataFrame(), "Fit": pd.DataFrame(),
			"f_loc": pd.DataFrame(), "f_dft": pd.DataFrame(), "f_trc": pd.DataFrame(), "f_blk": pd.DataFrame(),
			"f_MSD": pd.DataFrame(), "f_InD": pd.DataFrame(), "f_Fit": pd.DataFrame()})
	"""Résultats des différents calculs."""

	visualization: Optional[np.ndarray] = field(init=False, default=None)
	"""Résultat de la visualisation."""
	_path: str = field(init=False, default="")
	"""Dossier de sortie pour le fichier en cours de traitement."""
	_stack: Optional[np.ndarray] = field(init=False, default=None)
	"""Pile en cours de traitement."""
	_suffix: str = field(init=False, default="")
	"""Suffixe des fichiers pour un traitement (timestamp au format `YYYYMMDD_HHMMSS`)."""

	KEYS_TO_FILE: dict[str, str] = field(init=False, default_factory=lambda: {
			"loc": "localizations", "f_loc": "localizations_filtered",
			"dft": "localizations_corrected", "f_dft": "localizations_corrected_filtered", "bds": "beads",
			"trc": "tracking", "f_trc": "tracking_filtered",
			"blk": "tracking_reconnected", "f_blk": "tracking_reconnected_filtered",
			"MSD": "tracking_MSD", "f_MSD": "tracking_MSD_filtered",
			"InD": "tracking_InstantD", "f_InD": "tracking_InstantD_filtered",
			"Fit": "tracking_Fit", "f_Fit": "tracking_Fit_filtered"})
	"""Alias entre les noms de fichiers et les clé dans le dictionnaire de dataframes."""

	# ==================================================
	# region Initialization
	# ==================================================
	##################################################
	def __post_init__(self):
		"""Méthode appelée automatiquement après l'initialisation du dataclass."""
		filters = self.settings.filtering
		filters.buttons["reset"].clicked.connect(self.reset_filtered)
		filters.buttons["update"].clicked.connect(self.update_filtered)
		filters.buttons["save"].clicked.connect(self.save_filtered)

	##################################################
	def is_dll_valid(self) -> bool:
		"""
		Vérifie la validité de la DLL utilisée par le plugin.

		:return: True si la DLL est valide, False sinon.
		"""
		return self.palm.is_valid()

	##################################################
	def reset_result(self):
		"""Vide entièrement les DataFrame de résultat dans `df`."""
		for key in self.df: self.df[key] = pd.DataFrame()

	# ==================================================
	# endregion Initialization
	# ==================================================

	# ==================================================
	# region Getter / Setter
	# ==================================================
	##################################################
	def get_localization_key(self) -> str:
		"""Clé des localisations (filtrée si elle est non vide) et corrigé si elle est non vide également"""
		if self.df["f_dft"].empty:
			if self.df["dft"].empty:
				if self.df["f_loc"].empty:
					return "loc"
				return "f_loc"
			return "dft"
		return "f_dft"

	##################################################
	def get_tracks_key(self) -> str:
		"""Clé des trajectoires (filtrée si elle est non vide) et reconnectée si elle est non vide également."""
		if self.df["f_blk"].empty:
			if self.df["blk"].empty:
				if self.df["f_trc"].empty:
					return "trc"
				return "f_trc"
			return "blk"
		return "f_blk"

	##################################################
	def get_tracks_compute_key(self) -> list[str]:
		"""Clé des calculs sur trajectoires (filtrés si non vide)."""
		if self.df["f_MSD"].empty and self.df["f_InD"].empty and self.df["f_Fit"].empty:
			return ["MSD", "InD", "Fit"]
		return ["f_MSD", "f_InD", "f_Fit"]

	##################################################
	@property
	def localizations(self) -> pd.DataFrame:
		"""Getter du :class:`DataFrame <pandas.DataFrame>` de la localisation (filtrée si elle est non vide)."""
		return self.df[self.get_localization_key()]

	##################################################
	@property
	def tracks(self) -> pd.DataFrame:
		"""Getter du :class:`DataFrame <pandas.DataFrame>` du suivi (filtré s'il est non vide) et reconnecté s'il est non vide également."""
		return self.df[self.get_tracks_key()]

	##################################################
	@property
	def tracks_compute(self) -> dict[str, pd.DataFrame]:
		"""Getter du trio de :class:`DataFrame <pandas.DataFrame>` des calculs sur trajectoires (filtrés si non vide)."""
		keys = self.get_tracks_compute_key()
		return {"MSD": self.df[keys[0]], "InD": self.df[keys[1]], "Fit": self.df[keys[2]]}

	##################################################
	@property
	def path(self) -> str:
		"""Dossier de sortie pour le fichier en cours de traitement."""
		return self._path

	##################################################
	@property
	def stack(self) -> np.ndarray:
		"""Pile en cours de traitement."""
		return self._stack

	##################################################
	@property
	def suffix(self) -> str:
		"""Suffixe des fichiers pour un traitement (timestamp au format `YYYYMMDD_HHMMSS`)."""
		return self._suffix

	##################################################
	def _output_name(self, name: str, ext: str = "csv") -> str: return f"{self._path}/{name}-{self._suffix}.{ext}"

	# ==================================================
	# endregion Getter / Setter
	# ==================================================

	# ==================================================
	# region Process
	# ==================================================
	##################################################
	def load(self, path: str = ""):
		"""Charge les précédents résultats du fichier courant."""
		if not self.is_dll_valid():
			Ui.print_warning("Process not completed due to missing DLLs.")
			return

		# --- Chargement des paramètres ---
		self._path = self.settings.batch.get_paths()[0] if path == "" else path  # Parsing du batch
		settings_filename = FileIO.get_last_file(self._path, "settings")
		self._suffix = FileIO.extract_suffix(settings_filename)
		if not settings_filename or not self._suffix:
			Ui.print_warning("No valid settings file to load.")
			return

		print(f"Loading setting file '{settings_filename}'.")
		with self.settings.signal_blocked():
			cfg = FileIO.open_json(str(settings_filename))
			self.settings.update_from_dict(cfg)
			self.settings.localization["Preview"].value = False

		# --- Chargement des fichiers associés à ces paramètres. ---
		self.reset_result()  # Reset result Dataframes
		print(f"\tLoading files from the '{self._path}' folder with the timestamp {self._suffix}.")
		for key, fname in self.KEYS_TO_FILE.items():
			f = self._output_name(fname)
			try:
				if Path(f).is_file():
					self.df[key] = pd.read_csv(f)  # Lecture du fichier CSV avec pandas
					print(f"\tFile '{fname}' loaded successfully.")
				else:
					self.df[key] = pd.DataFrame()
					print(f"\tFile '{fname}' not found.")
			except Exception as e:
				self.df[key] = pd.DataFrame()
				print_warning(f"\tError loading file '{fname}': {e}")

		# --- Chargement de la pile ---
		try:
			self._stack = self.settings.batch.get_stacks()[0]
			print(f"\tStack loaded successfully (size: {self._stack.shape}).")
		except Exception as e:
			print(f"\tError loading stack: {e}")

	##################################################
	def process(self):
		"""Lance le process de PALM selon les éléments en paramètres."""

		if not self.is_dll_valid():
			Ui.print_warning("Process not completed due to missing DLLs.")
			return

		# --- Parsing du batch ---
		paths = self.settings.batch.get_paths()
		stacks = self.settings.batch.get_stacks()
		if len(stacks) == 0:
			Ui.print_warning("No files.")
			return

		# --- Parcours du batch ---
		for self._path, self._stack in zip(paths, stacks):
			# Reset result Dataframes
			self.reset_result()
			# Logger
			Path(self._path).mkdir(parents=True, exist_ok=True)
			self._suffix = FileIO.get_timestamp_for_files()
			self._logger.open(self._output_name("log", "log"))
			self._logger.add("Start Processing.")
			self._logger.add(f"Output folder: {self._path}")

			# Save settings
			FileIO.save_json(self._output_name("settings", "json"), self.settings.to_dict())
			self._logger.add("Settings saved.")

			# Save meta file (Création du DataFrame et sauvegarde en CSV)
			depth, height, width = self._stack.shape
			df = Parsing.get_meta([height, width, depth, self.settings.calibration["Pixel Size"].value,
								   self.settings.calibration["Exposure"].value, self.settings.calibration["Intensity"].value])
			df.to_csv(self._output_name("meta"), index=False)
			self._logger.add("Meta file saved.")

			# Lancement des traitements
			self._process_step(self.settings.localization, "localization", ["loc"], self._localization, self.filter_localizations)
			self._process_step(self.settings.beads, "beads extraction", ["bds"], self._beads_extraction, self.filter_localizations)
			self._process_step(self.settings.tracking, "tracking", ["trc"], self._tracking, self.filter_tracks)
			self._process_step(self.settings.blinking, "blinking reconnection", ["blk"], self._blinking_reconnection, self.filter_tracks)
			self._process_step(self.settings.tracks_compute, "tracks computes", ["MSD", "InD", "Fit"], self._tracks_compute, self._filter_tracks_compute)

			# Lancement de la Visualisation Haute Résolution
			if self.settings.visualization_hr.active:
				self._logger.add("High-resolution visualization enabled.")
				self._visualization_hr()
			else: self._logger.add("High-resolution visualization disabled.")

			# Lancement de la Visualisation graphique
			if self.settings.visualization_graph.active:
				self._logger.add("Graphical visualization enabled.")
				self._visualization_graph()
			else: self._logger.add("Graphical visualization disabled.")

			# Lancement de la génération de Galleries
			if self.settings.gallery.active:
				self._logger.add("Gallery generation enabled.")
				self._gallery()
			else: self._logger.add("Gallery generation disabled.")

			# Fermeture du Log
			self._logger.add("Processing complete.")
			self._logger.close()

	##################################################
	def _process_step(self, group: BaseSettingGroup, name: str, keys: list[str], process_func: Callable, filter_func: Callable):
		"""Etape du processus

		:param group: Groupe de paramètres lié
		:param name: Nom de l'étape
		:param keys: Clé du DataFrame dans le dictionnaire
		:param process_func: Fonction de traitement de cette étape
		:param filter_func: Fonction de filtre de cette étape
		"""
		if group.active:  # Process
			self._logger.add(f"{name.title()} enabled.")
			try: process_func()
			except Exception: raise
		else:  # Load last file possible
			self._logger.add(f"{name.title()} disabled.")
			for key in keys:
				if key in ["dft", "blk"]: continue  # On ne charge pas ceux-là
				f = FileIO.get_last_file(self._path, f"{self.KEYS_TO_FILE[key]}-")
				if f.endswith("csv"):
					try:
						self._logger.add(f"\tLoading a pre-computed {name} file.")
						self.df[key] = pd.read_csv(f)
						self._logger.add(f"\tFile '{f}' loaded successfully, {len(self.df[key])} {name}(s) found.")
					except Exception as e:
						self.df[key] = pd.DataFrame()
						self._logger.add(f"\tError loading file '{f}': {e}")
				else:  # Sinon
					self.df[key] = pd.DataFrame()
					self._logger.add(f"\tNo pre-computed {name} data.")

		if len(keys) == 1:
			f_key = f"f_{keys[0]}"
			self.df[f_key] = filter_func(self.df[keys[0]])
			n_init, n_end = len(self.df[keys[0]]), len(self.df[f_key])
			if n_init != n_end:
				self._logger.add(f"\t\tFiltering of {name} file {n_end} {name} instead of {n_init}: {n_init - n_end} deletion(s).")
				if self.settings.filtering["Save"].value and n_end != 0:
					self._logger.add(f"\tSaving the filtered {name} file.")
					self.df[f_key].to_csv(self._output_name(self.KEYS_TO_FILE[f_key]), index=False)
			else:
				self.df[f_key] = pd.DataFrame()
		else:
			filter_func()  # Cas spécial des tracks_compute qui modifient beaucoup de chose en même temps

	##################################################
	def _localization(self):
		"""Lance la localisation à partir des paramètres de l'interface."""
		# Parse settings
		s = self.settings.localization.settings
		filters = self.settings.filtering
		# Filtre sur les plans
		planes = filters["Plane"].value
		planes = list(range(planes[0] - 1, planes[1])) if filters["Plane"].active else None
		fit = self.settings.localization.get_fit()
		try: fit_params = self.settings.localization.get_fit_params()
		except Exception: raise
		# Run command
		self.df["loc"] = self.palm.localization(self._stack, s["Threshold"], s["Watershed"], fit, fit_params, planes)

		self._logger.add(f"\tSaving the localization file ({len(self.df['loc'])} localization(s) found).")
		self.df["loc"].to_csv(self._output_name(self.KEYS_TO_FILE["loc"]), index=False)

	##################################################
	def _beads_extraction(self):
		"""Lance la correction du drift à partir des paramètres de l'interface."""
		df = self.localizations  # Récupère automatiquement le "bon" dataframe (filtré ou non)
		if "Integrated Intensity" in df.columns: df = df[df["Integrated Intensity"] > 0]  # Suppression des éléments où l'ajustement a échoué.
		if df.empty:
			self._logger.add("\tNo localizations data calculated, no additional calculations can be performed.")
			return

		s = self.settings.beads.settings
		self.df["bds"] = extract_beads(df, s["Max Distance"], s["3D"], strict=False, k=2)
		if self.df["bds"].empty:
			self._logger.add("\tNo beads found.")
			return
		self._logger.add(f"\tSaving the beads file ({self.df['bds'].iloc[-1, 0]} beads(s) found).")
		self.df["bds"].to_csv(self._output_name(self.KEYS_TO_FILE["bds"]), index=False)

	##################################################
	def _tracking(self):
		"""Lance le suivi à partir des paramètres de l'interface."""
		df = self.localizations  # Récupère automatiquement le "bon" dataframe (filtré ou non)
		if "Integrated Intensity" in df.columns: df = df[df["Integrated Intensity"] > 0]  # Suppression des éléments où l'ajustement a échoué.
		if df.empty:
			self._logger.add("\tNo localizations data calculated, no additional calculations can be performed.")
			return

		s = self.settings.tracking.settings
		self.df["trc"] = self.palm.tracking(df, s["Max Distance"])

		self._logger.add(f"\tSaving the tracking file ({len(self.df['trc'])} point(s) found).")
		self.df["trc"].to_csv(self._output_name(self.KEYS_TO_FILE["trc"]), index=False)

	##################################################
	def _blinking_reconnection(self):
		"""Lance le tracking à partir des paramètres de l'interface."""
		df = self.df["trc"]  # Récupère le dataframe du suivi
		if df.empty:
			self._logger.add("\tNo tracking data calculated, no additional calculations can be performed.")
			return

		s = self.settings.blinking.settings
		pixel_size = self.settings.calibration.settings["Pixel Size"]
		self.df["blk"] = self.palm.blinking_reconnection(df, pixel_size * 1000, s["Mode"], s["Max Duration"], s["Max Distance"] * 1000)

		self._logger.add(f"\tSaving the reconnected tracking file ({len(self.df['blk'])} point(s) found).")
		self.df["blk"].to_csv(self._output_name(self.KEYS_TO_FILE["blk"]), index=False)

	##################################################
	def _tracks_compute(self):
		"""Lance les calculs sur les trajectoires à partir des paramètres de l'interface."""
		df = self.tracks  # Récupère automatiquement le "bon" dataframe (blinking et filtré ou non)
		if df.empty:
			self._logger.add("\tNo tracking data calculated, no additional calculations can be performed.")
			return

		# Parse settings
		sc = self.settings.calibration.settings
		s = self.settings.tracks_compute.settings

		if not s["MSD"] and not s["Instant Diffusion"] and s["Fit"] == 0:
			self._logger.add("\tNo metrics selected, no additional calculations can be performed.")
			return

		# Run command (pixel size doit rester en micromètre cette fois, car toutes les mesures seront en micromètres carré)
		res = self.palm.tracks_compute(df, s["MSD"], s["Instant Diffusion"], s["3D"], s["Log Scale"],
									   sc["Pixel Size"], sc["Exposure"], s["Fit"], np.array([s["Fit Length"]], dtype=np.float64))
		for key in res: self.df[key] = res[key]

		for key, name in [("MSD", "MSD"), ("InD", "Instant Diffusion"), ("Fit", "Fit")]:
			if s[name] and not res[key].empty:
				self._logger.add(f"\tSaving the {name} file.")
				res[key].to_csv(self._output_name(self.KEYS_TO_FILE[key]), index=False)

	# ==================================================
	# endregion Process
	# ==================================================

	# ==================================================
	# region Filtering
	# ==================================================
	##################################################
	def reset_filtered(self):
		"""Vide entièrement les DataFrames filtrés dans `df`."""
		with self.settings.signal_blocked(): self.settings.filtering.reset()
		for key in self.df:
			if key.startswith("f_"): self.df[key] = pd.DataFrame()

	##################################################
	def update_filtered(self, last: bool = True):
		"""
		Recalcul les filtres sur le dernier dataframe disponible pour chacun si last est sélectionné, sinon sur l'original.

		:param last: Utilise les dernières version des dataframes si `True`, sinon les données brutes serotn utilisées.
		"""
		df = {}
		for key in ["loc", "dft", "trc", "blk", "MSD", "InD", "Fit"]:
			df[key] = self.df[key] if self.df[f"f_{key}"].empty or not last else self.df[f"f_{key}"]

		self.df["f_loc"] = self.filter_localizations(df["loc"])
		self.df["f_dft"] = self.filter_localizations(df["dft"])
		self.df["f_trc"] = self.filter_tracks(df["trc"])
		self.df["f_blk"] = self.filter_tracks(df["blk"])

		o_name = "f_trc" if self.df["f_blk"].empty else "f_blk"
		self.df[o_name], self.df["f_MSD"], self.df["f_InD"], self.df["f_Fit"] \
			= self.filter_tracks_compute(self.tracks, df["MSD"], df["InD"], df["Fit"])

		for key in ["loc", "dft", "trc", "blk"]:
			f_key = f"f_{key}"
			if len(self.df[key]) == len(self.df[f_key]): self.df[f_key] = pd.DataFrame()

		if self.settings.filtering["Save"].value: self.save_filtered()

	##################################################
	def save_filtered(self):
		"""Enregistre tous les fichiers filtrés s'ils ne sont pas vide."""
		self._suffix = FileIO.get_timestamp_for_files()
		for key, fname in self.KEYS_TO_FILE.items():
			# Il s'agit d'un filtre, il n'est pas vide et il a une taille différente de l'original
			if "f_" in key and not self.df[key].empty and len(self.df[key]) != len(self.df[key[2:]]):
				self.df[key].to_csv(self._output_name(fname), index=False)

	##################################################
	def _filter_tracks_compute(self):
		"""Filtre les fichiers de metrique."""
		n_init = len(self.df["MSD"])
		o_name = self.get_tracks_key()
		if "f_" not in o_name: o_name = f"f_{o_name}"  # Si aucun filtre la clé sera sans le f_ devant
		self.df[o_name], self.df["f_MSD"], self.df["f_InD"], self.df["f_Fit"] \
			= self.filter_tracks_compute(self.tracks, self.df["MSD"], self.df["InD"], self.df["Fit"])

		n_end = len(self.df["f_MSD"])
		if n_init != n_end:
			self._logger.add(f"\t\tFiltering of tracks compute files {n_end} tracks instead of {n_init}: {n_init - n_end} deletion(s)")
			if self.settings.filtering["Save"].value:
				for key, name in [(o_name, "tracking"), ("f_MSD", "MSD"), ("f_InD", "Instant Diffusion"), ("f_Fit", "Fit")]:
					if not self.df[key].empty:
						self._logger.add(f"\tSaving the filtered {name} file.")
						self.df[key].to_csv(self._output_name(self.KEYS_TO_FILE[key]), index=False)
		else:
			for key in ["f_MSD", "f_InD", "f_Fit"]: self.df[key] = pd.DataFrame()

	##################################################
	def filter_localizations(self, datas: pd.DataFrame) -> pd.DataFrame:
		"""
		Filtre un DataFrame de localisation.

		:param datas: DataFrame à filtrer
		:return: :class:`DataFrame <pandas.DataFrame>` filtré.
		"""
		res = datas.copy()
		if "Integrated Intensity" in res.columns: df = res[res["Integrated Intensity"] > 0]  # Suppression des éléments où l'ajustement a échoué.
		if res.empty: return res
		f = self.settings.filtering
		fl = cast(FilteringL, f["Localization"])
		filters = [[f["Plane"], "Plane"],
				   [fl["X"], "X"], [fl["Y"], "Y"], [fl["Z"], "Z"],
				   [fl["Intensity"], "Integrated Intensity"],
				   [fl["Sigma X"], "Sigma X"], [fl["Sigma Y"], "Sigma Y"], [fl["Theta"], "Theta"], [fl["Circularity"], "Circularity"],
				   [fl["MSE XY"], "MSE XY"], [fl["MSE Z"], "MSE Z"]]

		for filt, col in filters:
			if isinstance(filt, CheckRangeFloat | CheckRangeInt) and filt.active:
				limits = filt.value
				res = res[res[col].between(limits[0], limits[1])]  # Bornes incluses
		return res

	##################################################
	def filter_tracks(self, datas: pd.DataFrame) -> pd.DataFrame:
		"""
		Filtre un DataFrame de trajectoires.

		:param datas: DataFrame à filtrer
		:return: :class:`DataFrame <pandas.DataFrame>` filtré.
		"""
		res = datas.copy()
		if res.empty: return res
		f = cast(CheckRangeInt, cast(FilteringT, self.settings.filtering["Tracks"])["Length"])  # Linter passage
		if f.active:
			limits = f.value
			counts = res.groupby("Track").size()  # .								  Comptage par trajectoire
			keep_ids = counts.index[(counts >= limits[0]) & (counts <= limits[1])]  # IDs de trajectoires gardées: min_len <= nb points <= max_len
			res = res[res["Track"].isin(keep_ids)]  # .								  Filtrage (on garde l'ordre original)
		return res

	##################################################
	def filter_tracks_compute(self, tracks: pd.DataFrame, msd: pd.DataFrame, instant_d: pd.DataFrame,
							  fit: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
		"""
		Filtre un DataFrame de calcul sur les trajectoires.

		:param tracks: DataFrame de trajectoires
		:param msd: DataFrame de calcul des MSD
		:param instant_d: DataFrame de calcul de la diffusion instantanée
		:param fit: DataFrame de calcul de l'ajustement
		:return: DataFrames filtrés.
		"""
		o_trc = tracks.copy()
		o_msd = msd.copy()
		o_ind = instant_d.copy()
		o_fit = fit.copy()
		if o_trc.empty: return o_trc, o_msd, o_ind, o_fit

		f = cast(FilteringT, self.settings.filtering["Tracks"])

		# ----- Base : tous les IDs présents dans la référence -----
		keep_ids: set = set(o_trc["Track"].unique().tolist())
		# ----- Filtre Longueur -----
		f_tmp = cast(CheckRangeInt, f["Length"])
		if f_tmp.active:
			limits_l = f_tmp.value
			counts = o_trc.groupby("Track").size()
			ok_len_ids = set(counts.index[(limits_l[0] <= counts) & (counts <= limits_l[1])].tolist())
			keep_ids &= ok_len_ids  # intersection sur des sets d'IDs

		# ----- Filtre sur Instant D -----
		f_tmp = cast(CheckRangeInt, f["Instant D"])
		if f_tmp.active and not o_ind.empty:
			limits_d = f_tmp.value

			o_ind = o_ind[o_ind["Track"].isin(keep_ids)]  # .					 Restreindre aux trajectoires admissibles jusqu'ici
			if not o_ind.empty:
				val_cols = [c for c in o_ind.columns if c != "Track"]  # .		 Colonnes de valeurs = toutes sauf 'Track'
				vals = o_ind[val_cols]
				vals_np = vals.to_numpy(dtype=float)  # .						 Convertir en numpy pour un contrôle fin
				finite = np.isfinite(vals_np)  # .								 Masque des valeurs finies (ni NaN, ni ±inf)
				outside = (vals_np <= limits_d[0]) | (vals_np >= limits_d[1])  # Valeurs hors bornes (sur le numpy brut)
				outside &= finite  # .											 On ne compte les "outside" que là où c'est vraiment une valeur finie
				n_valid, n_out = finite.sum(axis=1), outside.sum(axis=1)  # .	 Nombre de valeurs valides/hors bornes par ligne
				pct_out_np = np.zeros_like(n_out, dtype=float)  # .				 Pourcentage hors bornes (évite la division par 0 avec where=)
				np.divide(n_out, n_valid, out=pct_out_np, where=n_valid > 0)
				pct_out = pd.Series(pct_out_np * 100.0, index=o_ind.index)

				# avec une troisieme valeur limit[2] qui serait le pourcentage de fail max autorisé
				# Ou alors un nouveau setting type Instant D Failure Tolerance (%), je vais mettre 50% ici
				ok_ids = set(map(int, np.unique(o_ind.loc[pct_out <= 50.0, "Track"].to_numpy())))
				keep_ids &= ok_ids

		# ----- Filtre sur Fit -----
		if not o_fit.empty:
			o_fit = o_fit[o_fit["Track"].isin(keep_ids)]  # Restreindre aux trajectoires admissibles jusqu'ici
			if not o_fit.empty:
				filters = [
						# Quel que soit l'ajustement.
						[f["D Coeff"], "D(0) (μm²/s)"],
						# Fit Puissance
						[f["Alpha"], "Alpha"],
						[f["Speed"], "Average Speed (Last-First)(μm/s)"],
						# Fit Exponentiel
						[f["Confinement"], "Confinement Radius (μm)"]]

				for filt, col in filters:
					if col in o_fit.columns and isinstance(filt, CheckRangeFloat | CheckRangeInt) and filt.active:
						limits = filt.value
						o_fit = o_fit[o_fit[col].between(limits[0], limits[1])]  # Bornes incluses

				keep_ids &= set(o_fit["Track"].unique().tolist())

		# ----- Filtre final des trajectoires restantes -----
		if not o_trc.empty: o_trc = o_trc[o_trc["Track"].isin(keep_ids)]
		if not o_msd.empty: o_msd = o_msd[o_msd["Track"].isin(keep_ids)]
		if not o_ind.empty: o_ind = o_ind[o_ind["Track"].isin(keep_ids)]
		if not o_fit.empty: o_fit = o_fit[o_fit["Track"].isin(keep_ids)]
		return o_trc, o_msd, o_ind, o_fit

	# ==================================================
	# endregion Filtering
	# ==================================================

	# ==================================================
	# region Visualization
	# ==================================================
	##################################################
	def add_color_to_tracks(self, datas: pd.DataFrame, source: str) -> pd.DataFrame:
		"""
		Ajoute une couleur pour chaque point des trajectoires en fonction d'un critère agrégé au niveau **Track**.

		Règles :
			- Si source == "Track Number" : couleur = (Track-1) % MAX_UI_16 + 1
			- Si source ∈ {"Length", "Instant D", "MSD", "Total Intensity"} :
				* on utilise la table ``self.tracks_compute["Fit"]`` (1 ligne par Track) pour récupérer la métrique.
				* si `Fit` est vide, on déclenche le calcul puis on réessaie ; si toujours vide, fallback = "Track Number".
				* si une seule piste valide ou si `min==max`, toutes les pistes prennent la couleur médiane `MAX_UI_16//2`.
				* sinon, étalonnage linéaire `min→1`, `max→MAX_UI_16`.
				* toute piste absente de `Fit` ou `NaN` sur la métrique retombe sur la couleur "Track Number".

		:param datas: DataFrame des points de trajectoires, doit contenir au minimum la colonne 'Track'.
		:param source: Critère de coloration ("Track Number", "Length", "Instant D", "MSD", "Total Intensity").
		:return: Copie de `datas` avec une colonne 'Color' de type UInt16.
		"""
		res = datas.copy()
		# HR_TRC_SOURCE = ["All", "Track Number", "Length", "Instant D", "MSD", "Total Intensity"]
		# Chemin rapide : simple palette périodique par numéro de piste
		if source == "Track Number":
			res = res.assign(Color=((res["Track"] - 1) % MAX_UI_16 + 1).astype("UInt16"))
			return res

		# Récupération / calcul du Fit (1 ligne par Track) s'il manque
		fit = self.tracks_compute["Fit"]
		if fit.empty:  # .						Vide (non calculé)
			self._logger.add("\t\tTracks compute to be performed to define a color during visualization.")
			# On active le fit lineaire si aucun n'est sélectionné.
			if self.settings.tracks_compute["Fit"].value == 0: self.settings.tracks_compute["Fit"].value = 1
			self._tracks_compute()  # .			On lance le calcul
			fit = self.tracks_compute["Fit"]  # On reaffecte le resultat
		if fit.empty:  # .						Toujours vide (erreur de calcul ou autre, on prend le numéro des trajectoires par défaut).
			res = res.assign(Color=((res["Track"] - 1) % MAX_UI_16 + 1).astype("UInt16"))
			return res

		# Normalisation : mapping des noms de métriques
		metric_by_source = {
				"Length":          "Length",
				"Total Intensity": "Total Intensity",
				"Instant D":       "D(0) (μm²/s)",
				"MSD":             "MSD(0) (μm²)",
				}
		metric = metric_by_source[source]
		vmin, vmax = fit[metric].min(), fit[metric].max()
		# vmin, vmax = fit[metric].quantile([0.05, 0.95]) A envisager au lieu du min et max en cas d'outlier.
		if len(fit) == 1 or vmin >= vmax: res["Color"] = MAX_UI_16 // 2  # Cas Uniforme
		else:
			# Étalonnage linéaire : min→1, max→MAX_UI_16 (inclusif), arrondi au plus proche
			scale = (MAX_UI_16 - 1) / (vmax - vmin)
			vals = fit[metric].to_numpy(dtype=float)
			colors = np.rint(1.0 + (vals - vmin) * scale).astype(np.int64)
			np.clip(colors, 1, MAX_UI_16, out=colors)
			color_map = dict(zip(fit["Track"].to_numpy(), colors.astype(np.uint16)))
			# Application par map (vectorisé) : on remplit avec le fallback quand absent
			mapped = res["Track"].map(color_map)
			# 'mapped' est de type float si NaN possibles → on remplace NaN par fallback, puis cast en UInt16
			res["Color"] = mapped.fillna(MAX_UI_16 // 2).astype("UInt16")

		return res

	##################################################
	def _visualization_hr(self):
		"""Lance la creation d'une visualisation haute résolution à partir des paramètres passés en paramètres."""
		# Parse settings
		s = self.settings.visualization_hr.settings

		# Création de l'image finale
		depth, height, width = self._stack.shape
		if s["Type"] == 0:
			if self.localizations.empty:
				self._logger.add(f"\tNo localization data for high-resolution visualization.")
			else:
				sources = HR_LOC_SOURCE[1:] if s["Source L"] == 0 else [HR_LOC_SOURCE[s["Source L"]]]
				for source in sources:
					visualization = Viz.render_hr_image(width, height, s["Ratio"], self.localizations[["X", "Y", source]].to_numpy())
					self._logger.add(f"\tSaving high-resolution visualization (x{s['Ratio']}, {source}).")
					FileIO.save_png(visualization, self._output_name(f"visualization_x{s['Ratio']}_{source}", "png"))
		else:
			if self.tracks.empty:
				self._logger.add(f"\tNo tracking data for high-resolution visualization.")
			else:
				sources = HR_TRC_SOURCE[1:] if s["Source T"] == 0 else [HR_TRC_SOURCE[s["Source T"]]]
				for source in sources:
					tracks = self.add_color_to_tracks(self.tracks, source)
					tracks.to_csv(self._output_name("tracking_hr_color"), index=False)
					visualization = Viz.render_tracks_image(width, height, s["Ratio"], tracks)
					visualization = FileIO.grayscale_to_color(visualization, "viridis")
					self._logger.add(f"\tSaving tracking high-resolution visualization (x{s['Ratio']}, {source}).")
					FileIO.save_png(visualization, self._output_name(f"visualization_tracks_x{s['Ratio']}_{source}", "png"))

	##################################################
	def _visualization_graph(self):
		"""Lance la creation d'une visualisation graphique à partir des paramètres passés en paramètres."""
		if self.localizations.empty:
			self._logger.add(f"\tNo localization data for graphical visualization.")
			return

		# Parse settings
		s = self.settings.visualization_graph.settings
		sources = GRAPH_SOURCE[1:] if s["Source"] == 0 else [GRAPH_SOURCE[s["Source"]]]
		modes = GRAPH_MODE[1:] if s["Mode"] == 0 else [GRAPH_MODE[s["Mode"]]]

		for source in sources:
			loc = self.localizations[["Plane", source]].to_numpy()
			if np.all(loc[:, 1] == loc[0, 1]):
				self._logger.add(f"\tCanceling the graphical visualization: {source} uniform.")
				continue

			for mode in modes:
				fig, ax = plt.subplots()
				if mode == "Histogram":
					Viz.plot_histogram(ax, loc[:, 1], source + " Histogram", True, True, False)
				elif mode == "Plane Heat Map":
					Viz.plot_plane_heatmap(ax, loc, source + " Heatmap")
				else:  # elif mode == "Plane Violin":
					Viz.plot_plane_violin(ax, loc, source + " Violin")
				self._logger.add(f"\tSaving graphical visualization ({mode}, {source}).")
				fig.savefig(self._output_name(f"graph_{mode}_{source}", "png"), bbox_inches="tight")
				plt.close(fig)

	##################################################
	def _gallery(self):
		"""Lance la génération d'une galerie à partir des paramètres passés en paramètres."""
		s = self.settings.gallery.settings
		if self.localizations.empty:
			self._logger.add(f"\tNo localization data for gallery generation.")
			return
		gallery = Gallery.make_gallery(self._stack, self.localizations, s["ROI Size"], s["ROIs Per Line"])
		self._logger.add(f"\tSaving gallery ({s}).")
		FileIO.save_tif(gallery, self._output_name(f"gallery_{s['ROI Size']}_{s['ROIs Per Line']}", "tif"))
