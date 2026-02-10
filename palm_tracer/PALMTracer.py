"""
Module contenant les fonctions de traitement de PALM.

.. todo::
	Ajouter clairement un point dans la doc sur le systeme de filtre, l'enregistrement, le calcul sur l'intégralité des éléments et
	filtre ensuite lors de la visualisation des graph et des sauvegarde si la case est coché...
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import cast, Optional

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from palm_tracer.Processing import Gallery, Palm, Parsing, Visualization as Viz
from palm_tracer.Settings import Settings
from palm_tracer.Settings.Groups import Filtering, FilteringL, FilteringT
from palm_tracer.Settings.Groups.VisualizationGraph import GRAPH_MODE, GRAPH_SOURCE
from palm_tracer.Settings.Groups.VisualizationHR import HR_LOC_SOURCE, HR_TRC_SOURCE
from palm_tracer.Settings.Types import CheckRangeFloat, CheckRangeInt
from palm_tracer.Tools import FileIO, Logger, Ui

MAX_UI_16 = np.iinfo(np.uint16).max


##################################################
@dataclass
class PALMTracer:
	"""Classe principale de PALM Tracer."""

	settings: Settings = field(init=False, default_factory=Settings)
	"""Classe principale des paramètres PALMTracer."""
	palm: Palm = field(init=False, default_factory=lambda: Palm("CPU"))
	"""Interface vers la DLL C++ Palm."""
	_logger: Logger = field(init=False, default_factory=Logger)
	"""Journal d'activité."""
	df: dict[str, pd.DataFrame] = field(init=False, default_factory=lambda: {
			"loc":   pd.DataFrame(), "blk": pd.DataFrame(), "trc": pd.DataFrame(),
			"MSD":   pd.DataFrame(), "InD": pd.DataFrame(), "Fit": pd.DataFrame(),
			"f_loc": pd.DataFrame(), "f_blk": pd.DataFrame(), "f_trc": pd.DataFrame(),
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

	# ==================================================
	# region Initialization
	# ==================================================
	##################################################
	def is_dll_valid(self) -> bool:
		"""
		Vérifie la validité de la DLL utilisée par le plugin.

		:return: True si la DLL est valide, False sinon.
		"""
		return self.palm.is_valid()

	##################################################
	def get_localization_key(self) -> str:
		"""Clé de la localisation (filtrée si elle est non vide)"""
		return "loc" if self.df["f_loc"].empty else "f_loc"

	##################################################
	def get_tracks_key(self) -> str:
		"""Clé des trajectoires (filtrée si elle est non vide) et reconnecté si elle est non vide également."""
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
		"""Getter de la localisation (filtrée si elle est non vide)"""
		return self.df[self.get_localization_key()]

	##################################################
	@property
	def tracks(self) -> pd.DataFrame:
		"""Getter des trajectoires (filtrée si elle est non vide) et reconnecté si elle est non vide également."""
		return self.df[self.get_tracks_key()]

	##################################################
	@property
	def tracks_compute(self) -> dict[str, pd.DataFrame]:
		"""Getter des calculs sur trajectoires (filtrés si non vide)."""
		keys = self.get_tracks_compute_key()
		return {"MSD": self.df[keys[0]], "InD": self.df[keys[1]], "Fit": self.df[keys[2]]}

	##################################################
	def reset_result(self):
		"""Vide entièrement les DataFrame de résultat dans `_df`."""
		for key in self.df: self.df[key] = pd.DataFrame()
		self.visualization = None

	##################################################
	def reset_filtered(self):
		"""Vide entièrement les DataFrames filtrés dans `_df`."""
		for key in self.df:
			if key.startswith("f_"): self.df[key] = pd.DataFrame()

	# ==================================================
	# endregion Initialization
	# ==================================================

	##################################################
	def load(self, path: str = ""):
		"""Charge les précédents résultats du fichier courant."""
		if not self.is_dll_valid():
			Ui.print_warning("Process not completed due to missing DLLs.")
			return

		# Chargement des settings
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
			self.settings.localization["Preview"].set_value(False)

		# Chargement des fichiers associés à ce setting.
		params = [["localizations", "loc"], ["localizations_filtered", "f_loc"],
				  ["tracking", "trc"], ["tracking_filtered", "f_trc"],
				  ["tracking-reconnected", "blk"], ["tracking_filtered_reconnected", "f_blk"],
				  ["tracking_MSD", "MSD"], ["tracking_MSD_filtered", "f_MSD"],
				  ["tracking_InstantD", "InD"], ["tracking_InstantD_filtered", "f_InD"],
				  ["tracking_Fit", "Fit"], ["tracking_Fit_filtered", "f_Fit"]]

		# Reset result Dataframes
		self.reset_result()
		print(f"\tLoading files from the '{self._path}' folder with the timestamp {self._suffix}.")
		for p in params:
			f = f"{self._path}/{p[0]}-{self._suffix}.csv"
			try:
				self.df[p[1]] = pd.read_csv(f)  # Lecture du fichier CSV avec pandas
				print(f"\tFile '{p[0]}' loaded successfully.")
			except Exception as e:
				self.df[p[1]] = pd.DataFrame()
				print(f"\tError loading file '{p[0]}': {e}")

		# Chargement de la pile
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

		# Parsing du batch
		paths = self.settings.batch.get_paths()
		stacks = self.settings.batch.get_stacks()
		if len(stacks) == 0:
			Ui.print_warning("No files.")
			return

		# Parcours du batch
		for self._path, self._stack in zip(paths, stacks):
			# Reset result Dataframes
			self.reset_result()
			# Logger
			Path(self._path).mkdir(parents=True, exist_ok=True)
			self._suffix = FileIO.get_timestamp_for_files()
			self._logger.open(f"{self._path}/log-{self._suffix}.log")
			self._logger.add("Start Processing.")
			self._logger.add(f"Output folder: {self._path}")

			# Save settings
			FileIO.save_json(f"{self._path}/settings-{self._suffix}.json", self.settings.to_dict())
			self._logger.add("Settings saved.")

			# Si transformation de la zone en entrée (par une ROI) à faire ici.

			# Save meta file (Création du DataFrame et sauvegarde en CSV)
			depth, height, width = self._stack.shape
			df = Parsing.get_meta([height, width, depth, self.settings.calibration["Pixel Size"].get_value(),
								   self.settings.calibration["Exposure"].get_value(), self.settings.calibration["Intensity"].get_value()])
			df.to_csv(f"{self._path}/meta-{self._suffix}.csv", index=False)
			self._logger.add("Meta file saved.")

			# Lancement de la localisation
			if self.settings.localization.active:
				self._logger.add("Localization enabled.")
				try: self._localization()
				except Exception as e: raise
			else:  # Chargement d'une localisation existante
				self._logger.add("Localization disabled.")
				f = FileIO.get_last_file(self._path, "localizations-")
				if f.endswith("csv"):
					self._logger.add("\tLoading a pre-computed localization.")
					try:
						self.df["loc"] = pd.read_csv(f)
						self._logger.add(f"\tFile '{f}' loaded successfully.")
						self._filter_localizations()
						self._logger.add(f"\t\t{len(self.localizations)} localization(s) found.")
					except Exception as e:
						self.df["loc"] = pd.DataFrame()
						self._logger.add(f"\tError loading file '{f}': {e}")
				else:  # Sinon
					self.df["loc"] = pd.DataFrame()
					self._logger.add("\tNo pre-computed localization data.")

			# Lancement du tracking
			if self.settings.tracking.active:
				self._logger.add("Tracking enabled.")
				self._tracking()
			else:  # Chargement d'un tracking existant
				self._logger.add("Tracking disabled.")
				# Les fichiers reconnectés se nomment tracking-reconnected pour être pris en compte automatiquement.
				f = FileIO.get_last_file(self._path, "tracking-")
				if f.endswith("csv"):
					self._logger.add("\tLoading a pre-computed tracking.")
					try:
						self.df["trc"] = pd.read_csv(f)
						self._logger.add(f"\tFile '{f}' loaded successfully.")
						self._filter_tracks("trc")
						self._logger.add(f"\t\t{len(self.tracks)} track(s) found.")
					except Exception as e:
						self.df["trc"] = pd.DataFrame()
						self._logger.add(f"\tError loading file '{f}': {e}")
				else:  # Sinon
					self.df["trc"] = pd.DataFrame()
					self._logger.add("\tNo pre-computed tracking data.")

			# Lancement des calculs sur les trajectoires
			if self.settings.tracks_compute.active:
				self._logger.add("Tracks computes enabled.")
				self._tracks_compute()
			else:
				self._logger.add("Tracks computes disabled.")

			# Lancement de la Visualisation Haute Résolution
			if self.settings.visualization_hr.active:
				self._logger.add("High-resolution visualization enabled.")
				self._visualization_hr()
			else:
				self._logger.add("High-resolution visualization disabled.")
				self.visualization = None

			# Lancement de la Visualisation graphique
			if self.settings.visualization_graph.active:
				self._logger.add("Graphical visualization enabled.")
				self._visualization_graph()
			else:
				self._logger.add("Graphical visualization disabled.")

			# Lancement de la génération de Galleries
			if self.settings.gallery.active:
				self._logger.add("Gallery generationenabled.")
				self._gallery()
			else:
				self._logger.add("Gallery generationdisabled.")

			# Fermeture du Log
			self._logger.add("Processing complete.")
			self._logger.close()

	# ==================================================
	# region Basic Process
	# ==================================================
	##################################################
	def _localization(self):
		"""Lance la localisation à partir des settings passés en paramètres."""
		# Parse settings
		s = self.settings.localization.get_settings()
		filters = self.settings.filtering
		# Filtre sur les plans
		planes = filters["Plane"].get_value()
		planes = list(range(planes[0] - 1, planes[1])) if filters["Plane"].active else None
		fit = self.settings.localization.get_fit()
		try: fit_params = self.settings.localization.get_fit_params()
		except Exception as e: raise
		# Run command
		self.df["loc"] = self.palm.localization(self._stack, s["Threshold"], s["Watershed"], fit, fit_params, planes)

		self._logger.add("\tSaving the localization file.")
		self._logger.add(f"\t\t{len(self.df['loc'])} localization(s) found.")
		self.df["loc"].to_csv(f"{self._path}/localizations-{self._suffix}.csv", index=False)
		self._filter_localizations()

	##################################################
	def _tracking(self):
		"""Lance le tracking à partir des settings passés en paramètres."""
		df = self.localizations  # Récupère automatiquement le "bon" dataframe (filtré ou non)
		if df.empty:
			self._logger.add("\tNo location data calculated, no additional calculations can be performed.")
			return
		# Parse settings
		s = self.settings.tracking.get_settings()
		# Run command (par défaut Min Length = 1, Decrease = 10, Cost Birth = 0.5)
		self.df["trc"] = self.palm.tracking(df, s["Max Distance"])

		self._logger.add("\tSaving the tracking file.")
		self._logger.add(f"\t\t{len(self.df['trc'])} point(s) found.")
		self.df["trc"].to_csv(f"{self._path}/tracking-{self._suffix}.csv", index=False)
		self._filter_tracks("trc")

		# La reconnexion ne peut se faire que lors d'un (re)calcul de trajectoire, donc il n'est pas séparer du process initial.
		# Le but est d'éviter des erreurs de manipulations de reconnexions succesives instables.
		if self.settings.tracking["Blinking Reconnection"].active:
			self._logger.add("\tReconnection of tracks after blinking.")
			s = self.settings.tracking["Blinking Reconnection"].get_settings()
			pixel_size = self.settings.calibration.get_settings()["Pixel Size"]
			# Run command sur la version non filtrée des trajectoires
			self.df["blk"] = self.palm.blinking_reconnection(self.df["trc"], pixel_size * 1000, s["Mode"], s["Max Duration"], s["Max Speed"] * 1000)

			self._logger.add("\tSaving the reconnected tracking file.")
			self._logger.add(f"\t\t{len(self.df['blk'])} point(s) found.")
			self.df["blk"].to_csv(f"{self._path}/tracking-reconnected-{self._suffix}.csv", index=False)
			self._filter_tracks("blk", "_reconnected")

	##################################################
	def _tracks_compute(self):
		"""Lance le tracking à partir des settings passés en paramètres."""
		df = self.tracks  # Récupère automatiquement le "bon" dataframe (blinking et filtré ou non)
		if df.empty:
			self._logger.add("\tNo tracking data calculated, no additional calculations can be performed.")
			return

		# Parse settings
		sc = self.settings.calibration.get_settings()
		s = self.settings.tracks_compute.get_settings()

		if not s["MSD"] and not s["Instant Diffusion"] and s["Fit"] == 0:
			self._logger.add("\tNo metrics selected, no additional calculations can be performed.")
			return

		# Run command (pixel size doit rester en micromètre cette fois, car toutes les mesures seront en micromètres carré)
		res = self.palm.tracks_compute(df, s["MSD"], s["Instant Diffusion"], s["3D"], s["Log Scale"],
									   sc["Pixel Size"], sc["Exposure"], s["Fit"], np.array([s["Fit Length"]], dtype=np.float64))
		for key in res: self.df[key] = res[key]

		if s["MSD"] and not res["MSD"].empty:
			self._logger.add("\tSaving the MSD file.")
			res["MSD"].to_csv(f"{self._path}/tracking_MSD-{self._suffix}.csv", index=False)
		if s["Instant Diffusion"] and not res["InD"].empty:
			self._logger.add("\tSaving the Instant diffusion file.")
			res["InD"].to_csv(f"{self._path}/tracking_InstantD-{self._suffix}.csv", index=False)
		if s["Fit"] != 0 and not res["Fit"].empty:
			self._logger.add("\tSaving the fit file.")
			res["Fit"].to_csv(f"{self._path}/tracking_Fit-{self._suffix}.csv", index=False)
		self._filter_tracks_compute()

	# ==================================================
	# endregion Basic Process
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
			if self.settings.tracks_compute["Fit"].get_value() == 0: self.settings.tracks_compute["Fit"].set_value(1)
			self._tracks_compute()  # .			On lance le calcul
			fit = self.tracks_compute["Fit"]  # On reaffecte le resultat
		if fit.empty:  # .						Toujours vide (erreur de calcul ou autre, on prend le numéro des trajectoires par défaut)
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
		"""Lance la creation d'une visualisation haute résolution à partir des settings passés en paramètres."""
		# Parse settings
		s = self.settings.visualization_hr.get_settings()

		# Création de l'image finale
		depth, height, width = self._stack.shape
		if s["Type"] == 0:
			if self.localizations.empty:
				self._logger.add(f"\tNo localization data for high-resolution visualization.")
			else:
				sources = HR_LOC_SOURCE[1:] if s["Source L"] == 0 else [HR_LOC_SOURCE[s["Source L"]]]
				for source in sources:
					self.visualization = Viz.render_hr_image(width, height, s["Ratio"], self.localizations[["X", "Y", source]].to_numpy())
					self._logger.add(f"\tSaving high-resolution visualization (x{s['Ratio']}, {source}).")
					FileIO.save_png(self.visualization, f"{self._path}/visualization_x{s['Ratio']}_{source}-{self._suffix}.png")
		else:
			if self.tracks.empty:
				self._logger.add(f"\tNo tracking data for high-resolution visualization.")
			else:
				sources = HR_TRC_SOURCE[1:] if s["Source T"] == 0 else [HR_TRC_SOURCE[s["Source T"]]]
				for source in sources:
					tracks = self.add_color_to_tracks(self.tracks, source)
					tracks.to_csv(f"{self._path}/tracking_hr_color-{self._suffix}.csv", index=False)
					self.visualization = Viz.render_tracks_image(width, height, s["Ratio"], tracks)
					self.visualization = FileIO.grayscale_to_color(self.visualization, "viridis")
					self._logger.add(f"\tSaving tracking high-resolution visualization (x{s['Ratio']}, {source}).")
					FileIO.save_png(self.visualization, f"{self._path}/visualization_tracks_x{s['Ratio']}_{source}-{self._suffix}.png")

	##################################################
	def _visualization_graph(self):
		"""Lance la creation d'une visualisation graphique à partir des settings passés en paramètres."""
		if self.localizations.empty:
			self._logger.add(f"\tNo localization data for graphical visualization.")
			return

		# Parse settings
		s = self.settings.visualization_graph.get_settings()
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
				fig.savefig(f"{self._path}/graph_{mode}_{source}-{self._suffix}.png", bbox_inches="tight")
				plt.close(fig)

	##################################################
	def _gallery(self):
		"""Lance la génération d'une galerie à partir des settings passés en paramètres."""
		s = self.settings.gallery.get_settings()
		if self.localizations.empty:
			self._logger.add(f"\tNo localization data for gallery generation.")
			return
		gallery = Gallery.make_gallery(self._stack, self.localizations, s["ROI Size"], s["ROIs Per Line"])
		self._logger.add(f"\tSaving gallery ({s}).")
		FileIO.save_tif(gallery, f"{self._path}/gallery_{s['ROI Size']}_{s['ROIs Per Line']}-{self._suffix}.tif")

	# ==================================================
	# endregion Visualization
	# ==================================================

	# ==================================================
	# region Filtering
	# ==================================================
	##################################################
	def _filter_localizations(self):
		"""Filtre le fichier de localisation."""
		n_init = len(self.df["loc"])
		self.df["f_loc"] = self.filter_localizations(self.df["loc"])
		n_end = len(self.df["f_loc"])
		if n_init != n_end:
			self._logger.add(f"\t\tFiltering of localization file {n_end} localizations instead of {n_init}: {n_init - n_end} deletion(s).")
		if self.settings.filtering["Save"].get_value():
			self._logger.add("\tSaving the filtered localization file.")
			self.df["f_loc"].to_csv(f"{self._path}/localizations_filtered-{self._suffix}.csv", index=False)

	##################################################
	def _filter_tracks(self, name: str, suffix: str = ""):
		"""Filtre le fichier de tracking."""
		n_init = len(self.df[name])
		o_name = f"f_{name}"
		self.df[o_name] = self.filter_tracks(self.df[name])
		n_end = len(self.df[o_name])
		if n_init != n_end:
			self._logger.add(f"\t\tFiltering of tracking file {n_end} points instead of {n_init}: {n_init - n_end} deletion(s)")
		if self.settings.filtering["Save"].get_value():
			self._logger.add("\tSaving the filtered tracking file.")
			self.df[o_name].to_csv(f"{self._path}/tracking_filtered{suffix}-{self._suffix}.csv", index=False)

	##################################################
	def _filter_tracks_compute(self):
		"""Filtre les fichiers de metrique."""
		n_init = len(self.df["MSD"])
		o_name = self.get_tracks_key()
		self.df[o_name], self.df["f_MSD"], self.df["f_InD"], self.df["f_Fit"] \
			= self.filter_tracks_compute(self.tracks, self.df["MSD"], self.df["InD"], self.df["Fit"])

		n_end = len(self.df["f_MSD"])
		if n_init != n_end:
			self._logger.add(f"\t\tFiltering of tracks compute files {n_end} tracks instead of {n_init}: {n_init - n_end} deletion(s)")
		if self.settings.filtering["Save"].get_value():
			if not self.df["f_MSD"].empty:
				self._logger.add("\tSaving the filtered MSD file.")
				self.df["f_MSD"].to_csv(f"{self._path}/tracking_MSD_filtered-{self._suffix}.csv", index=False)
			if not self.df["f_InD"].empty:
				self._logger.add("\tSaving the filtered instant diffusion file.")
				self.df["f_InD"].to_csv(f"{self._path}/tracking_InstantD_filtered-{self._suffix}.csv", index=False)
			if not self.df["f_Fit"].empty:
				self._logger.add("\tSaving the filtered fit file.")
				self.df["f_Fit"].to_csv(f"{self._path}/tracking_Fit_filtered-{self._suffix}.csv", index=False)

	##################################################
	def filter_localizations(self, datas: pd.DataFrame) -> pd.DataFrame:
		"""
		Filtre un DataFrame de localisation.

		:param datas: DataFrame à filtrer
		:return: DataFrame filtré.
		"""
		res = datas.copy()
		if res.empty: return res
		f = cast(Filtering, self.settings.filtering)
		fl = cast(FilteringL, f["Localization"])
		filters = [[f["Plane"], "Plane"],
				   [fl["X"], "X"], [fl["Y"], "Y"], [fl["Z"], "Z"],
				   [fl["Intensity"], "Integrated Intensity"],
				   [fl["Sigma X"], "Sigma X"], [fl["Sigma Y"], "Sigma Y"], [fl["Theta"], "Theta"], [fl["Circularity"], "Circularity"],
				   [fl["MSE XY"], "MSE XY"], [fl["MSE Z"], "MSE Z"]]

		for filt, col in filters:
			if isinstance(filt, CheckRangeFloat | CheckRangeInt) and filt.active:
				limits = filt.get_value()
				res = res[res[col].between(limits[0], limits[1])]  # Bornes incluses
		return res

	##################################################
	def filter_tracks(self, datas: pd.DataFrame) -> pd.DataFrame:
		"""
		Filtre un DataFrame de trajectoires.

		:param datas: DataFrame à filtrer
		:return: DataFrame filtré.
		"""
		res = datas.copy()
		if res.empty: return res
		f = cast(CheckRangeInt, cast(FilteringT, self.settings.filtering["Tracks"])["Length"])  # Linter passage
		if f.active:
			limits = f.get_value()
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
		:param instant_d: DataFrame de calcul de la diffusion instantannée
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
			limits_l = f_tmp.get_value()
			counts = o_trc.groupby("Track").size()
			ok_len_ids = set(counts.index[(limits_l[0] <= counts) & (counts <= limits_l[1])].tolist())
			keep_ids &= ok_len_ids  # intersection sur des sets d'IDs

		# ----- Filtre sur Instant D -----
		f_tmp = cast(CheckRangeInt, f["Instant D"])
		if f_tmp.active and not o_ind.empty:
			limits_d = f_tmp.get_value()

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
						# Quelque soit le Fit
						[f["D Coeff"], "D(0) (μm²/s)"],
						# Fit Puissance
						[f["Alpha"], "Alpha"],
						[f["Speed"], "Average Speed (Last-First)(μm/s)"],
						# Fit Exponentiel
						[f["Confinement"], "Confinement Radius (μm)"]]

				for filt, col in filters:
					if col in o_fit.columns and isinstance(filt, CheckRangeFloat | CheckRangeInt) and filt.active:
						limits = filt.get_value()
						o_fit = o_fit[o_fit[col].between(limits[0], limits[1])]  # Bornes incluses

				keep_ids &= set(o_fit["Track"].unique().tolist())

		# ----- Filtre final des trajectoires restantes -----
		if not o_trc.empty: o_trc = o_trc[o_trc["Track"].isin(keep_ids)]
		if not o_msd.empty: o_msd = o_msd[o_msd["Track"].isin(keep_ids)]
		if not o_ind.empty: o_ind = o_ind[o_ind["Track"].isin(keep_ids)]
		if not o_fit.empty: o_fit = o_fit[o_fit["Track"].isin(keep_ids)]
		return o_trc, o_msd, o_ind, o_fit

	##################################################
	def update_filtered(self, last: bool = True):
		"""Recalcul les filtres sur le dernier dataframe disponible pour chacun si last est sélectionné, sinon sur l'original."""

		self._suffix = FileIO.get_timestamp_for_files()
		loc = self.df["loc"] if self.df["f_loc"].empty or not last else self.df["f_loc"]
		trc = self.df["trc"] if self.df["f_trc"].empty or not last else self.df["f_trc"]
		blk = self.df["blk"] if self.df["f_blk"].empty or not last else self.df["f_blk"]
		tc = self.tracks_compute if last else {"MSD": self.df["MSD"], "InD": self.df["InD"], "Fit": self.df["Fit"]}

		self.df["f_loc"] = self.filter_localizations(loc)
		self.df["f_trc"] = self.filter_tracks(trc)
		self.df["f_blk"] = self.filter_tracks(blk)

		o_name = "f_trc" if self.df["blk"].empty else "f_blk"
		self.df[o_name], self.df["f_MSD"], self.df["f_InD"], self.df["f_Fit"] \
			= self.filter_tracks_compute(self.tracks, tc["MSD"], tc["InD"], tc["Fit"])

		if self.settings.filtering["Save"].get_value():
			to_save = [["f_loc", "localizations_filtered"], ["f_trc", "tracking_filtered"], ["f_blk", "tracking_filtered_reconnected"],
					   ["f_MSD", "tracking_MSD_filtered"], ["f_InD", "tracking_InstantD_filtered"], ["f_Fit", "tracking_Fit_filtered"]]
			for n in to_save:
				if not self.df[n[0]].empty: self.df[n[0]].to_csv(f"{self._path}/{n[1]}-{self._suffix}.csv", index=False)
