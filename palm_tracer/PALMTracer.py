"""
Module contenant les fonctions de traitement de PALM.

.. todo::
	Ajouter clairement un point dans la doc sur le systeme de filtre, l'enregistrement, le calcul sur l'intégralité des éléments et
	filtre ensuite lors de la visualisation des graph et des sauvegarde si la case est coché...
"""

import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import cast, Optional

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from palm_tracer.Processing import make_gallery, Palm, plot_histogram, plot_plane_heatmap, plot_plane_violin, render_hr_image, render_tracks_image
from palm_tracer.Settings import Settings
from palm_tracer.Settings.Groups import Filtering, FilteringL, FilteringT
from palm_tracer.Settings.Groups.VisualizationGraph import GRAPH_MODE, GRAPH_SOURCE
from palm_tracer.Settings.Groups.VisualizationHR import HR_LOC_SOURCE, HR_TRC_SOURCE
from palm_tracer.Settings.Types import CheckRangeFloat, CheckRangeInt
from palm_tracer.Tools import get_last_file, Logger, print_warning, save_json, save_tif
from palm_tracer.Tools.FileIO import grayscale_to_color, save_png

MAX_UI_16 = np.iinfo(np.uint16).max


##################################################
@dataclass
class PALMTracer:
	""" Classe principale de PALM Tracer. """

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
		"""Clé de la localisation (filtrée si elle est non vide) """
		return "loc" if self.df["f_loc"].empty else "f_loc"

	##################################################
	def get_tracks_key(self) -> str:
		"""Clé des trajectoires (filtrée si elle est non vide) et reconnecté si elle est non vide également. """
		if self.df["f_blk"].empty:
			if self.df["blk"].empty:
				if self.df["f_trc"].empty:
					return "trc"
				return "f_trc"
			return "blk"
		return "f_blk"

	##################################################
	def get_tracks_compute_key(self) -> list[str]:
		"""Clé des calculs sur trajectoires (filtrés si non vide). """
		if self.df["f_MSD"].empty and self.df["f_InD"].empty and self.df["f_Fit"].empty:
			return ["MSD", "InD", "Fit"]
		return ["f_MSD", "f_InD", "f_Fit"]

	##################################################
	@property
	def localizations(self) -> pd.DataFrame:
		"""Getter de la localisation (filtrée si elle est non vide) """
		return self.df[self.get_localization_key()]

	##################################################
	@property
	def tracks(self) -> pd.DataFrame:
		"""Getter des trajectoires (filtrée si elle est non vide) et reconnecté si elle est non vide également. """
		return self.df[self.get_tracks_key()]

	##################################################
	@property
	def tracks_compute(self) -> dict[str, pd.DataFrame]:
		"""Getter des calculs sur trajectoires (filtrés si non vide). """
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
	def process(self):
		""" Lance le process de PALM selon les éléments en paramètres. """

		if not self.is_dll_valid():
			print_warning("Process non effectué car DLL manquantes.")
			return

		# Parsing du batch
		paths = self.settings.batch.get_paths()
		stacks = self.settings.batch.get_stacks()
		if len(stacks) == 0:
			print_warning("Aucun fichier.")
			return

		# Parcours du batch
		for self._path, self._stack in zip(paths, stacks):
			# Reset result Dataframes
			self.reset_result()
			# Logger
			os.makedirs(self._path, exist_ok=True)
			self._suffix = datetime.now().strftime("%Y%d%m_%H%M%S")
			self._logger.open(f"{self._path}/log-{self._suffix}.log")
			self._logger.add("Commencer le traitement.")
			self._logger.add(f"Dossier de sortie : {self._path}")

			# Save settings
			save_json(f"{self._path}/settings-{self._suffix}.json", self.settings.to_dict())
			self._logger.add("Paramètres sauvegardés.")

			# Si transformation de la zone en entrée (par une ROI) à faire ici.

			# Save meta file (Création du DataFrame et sauvegarde en CSV)
			depth, height, width = self._stack.shape
			df = pd.DataFrame({"Height":                  [height], "Width": [width], "Plane Number": [depth],
							   "Pixel Size (μm)":         [self.settings.calibration["Pixel Size"].get_value()],
							   "Exposure Time (s/frame)": [self.settings.calibration["Exposure"].get_value()],
							   "Intensity (photon/ADU)":  [self.settings.calibration["Intensity"].get_value()]})
			df.to_csv(f"{self._path}/meta-{self._suffix}.csv", index=False)
			self._logger.add("Fichier Meta sauvegardé.")

			# Lancement de la localisation
			if self.settings.localization.active:
				self._logger.add("Localisation activée.")
				try: self.__localization()
				except Exception as e: raise
			else:
				self._logger.add("Localisation désactivé.")
				f = get_last_file(self._path, "localizations-")
				if f.endswith("csv"):  # Chargement d'une localisation existante
					self._logger.add("\tChargement d'une localisation pré-calculée.")
					try:
						self.df["loc"] = pd.read_csv(f)  # Lecture du fichier CSV avec pandas
						self._logger.add(f"\tFichier '{f}' chargé avec succès.")
						self.__filter_localizations()
						self._logger.add(f"\t\t{len(self.localizations)} localisation(s) trouvée(s).")
					except Exception as e:
						self.df["loc"] = pd.DataFrame()
						self._logger.add(f"\tErreur lors du chargement du fichier '{f}' : {e}")
				else:  # Sinon
					self.df["loc"] = pd.DataFrame()
					self._logger.add("\tAucune donnée de localisation pré-calculée.")

			# Lancement du tracking
			if self.settings.tracking.active:
				self._logger.add("Tracking activé.")
				self.__tracking()
			else:
				self._logger.add("Tracking désactivé.")
				f = get_last_file(self._path, "tracking-")
				if f.endswith("csv"):  # Chargement d'une localisation existante
					self._logger.add("\tChargement d'un tracking pré-calculée.")
					try:
						self.df["trc"] = pd.read_csv(f)  # Lecture du fichier CSV avec pandas
						self._logger.add(f"\tFichier '{f}' chargé avec succès.")
						self._logger.add(f"\t\t{len(self.tracks)} trajectoire(s) trouvée(s).")
					except Exception as e:
						self.df["trc"] = pd.DataFrame()
						self._logger.add(f"\tErreur lors du chargement du fichier '{f}' : {e}")
				else:  # Sinon
					self.df["trc"] = pd.DataFrame()
					self._logger.add("\tAucune donnée de tracking pré-calculée.")

			# Lancement des calculs sur les trajectoires
			if self.settings.tracks_compute.active:
				self._logger.add("Calcul sur les trajectoires activé.")
				self.__tracks_compute()
			else:
				self._logger.add("Calcul sur les trajectoires désactivé.")

			# Lancement de la Visualisation Haute Résolution
			if self.settings.visualization_hr.active:
				self._logger.add("Visualisation haute résolution activée.")
				self.__visualization_hr()
			else:
				self._logger.add("Visualisation haute résolution désactivée.")
				self.visualization = None

			# Lancement de la Visualisation graphique
			if self.settings.visualization_graph.active:
				self._logger.add("Visualisation graphique activée.")
				self.__visualization_graph()
			else:
				self._logger.add("Visualisation graphique désactivée.")

			# Lancement de la génération de Galleries
			if self.settings.gallery.active:
				self._logger.add("Génération de la galerie activée.")
				self.__gallery()
			else:
				self._logger.add("Génération de la galerie désactivée.")

			# Fermeture du Log
			self._logger.add("Traitement terminé.")
			self._logger.close()

	# ==================================================
	# region Basic Process
	# ==================================================
	##################################################
	def __localization(self):
		""" Lance la localisation à partir des settings passés en paramètres. """
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

		self._logger.add("\tEnregistrement du fichier de localisation")
		self._logger.add(f"\t\t{len(self.df['loc'])} localisation(s) trouvée(s).")
		self.df["loc"].to_csv(f"{self._path}/localizations-{self._suffix}.csv", index=False)
		self.__filter_localizations()

	##################################################
	def __tracking(self):
		""" Lance le tracking à partir des settings passés en paramètres. """
		df = self.localizations  # Récupère automatiquement le "bon" dataframe (filtré ou non)
		if df.empty:
			self._logger.add("\tAucune donnée de localisation calculée, aucun calcul supplémentaire ne peut être effectué.")
			return
		# Parse settings
		s = self.settings.tracking.get_settings()
		# Run command (par défaut Min Length = 1, Decrease = 10, Cost Birth = 0.5)
		self.df["trc"] = self.palm.tracking(df, s["Max Distance"])

		self._logger.add("\tEnregistrement du fichier de trajectoires.")
		self._logger.add(f"\t\t{len(self.df['trc'])} point(s) trouvé(s).")
		self.df["trc"].to_csv(f"{self._path}/tracking-{self._suffix}.csv", index=False)
		self.__filter_tracks("trc")

		if self.settings.tracking["Blinking Reconnection"].active:
			self._logger.add("\tReconnexion des trajectoires après scintillement.")
			s = self.settings.tracking["Blinking Reconnection"].get_settings()
			pixel_size = self.settings.calibration.get_settings()["Pixel Size"]
			# Run command sur la version non filtrée des trajectoires
			self.df["blk"] = self.palm.blinking_reconnection(self.df["trc"], pixel_size, s["Mode"], s["Max Duration"], s["Max Speed"])

			self._logger.add("\tEnregistrement du fichier de trajectoires reconnectées.")
			self._logger.add(f"\t\t{len(self.df['blk'])} point(s) trouvé(s).")
			self.df["blk"].to_csv(f"{self._path}/tracking-reconnected-{self._suffix}.csv", index=False)
			self.__filter_tracks("blk", "_reconnected")


	##################################################
	def __tracks_compute(self):
		""" Lance le tracking à partir des settings passés en paramètres. """
		df = self.tracks  # Récupère automatiquement le "bon" dataframe (blinking et filtré ou non)
		if df.empty:
			self._logger.add("\tAucune donnée de tracking calculée, aucun calcul supplémentaire ne peut être effectué.")
			return

		# Parse settings
		sc = self.settings.calibration.get_settings()
		s = self.settings.tracks_compute.get_settings()

		if not s["MSD"] and not s["Instant Diffusion"] and s["Fit"] == 0:
			self._logger.add("\tAucune métrique de sélectionnée, aucun calcul supplémentaire ne peut être effectué.")
			return

		# Run command
		res = self.palm.tracks_compute(self.df["trc"], s["MSD"], s["Instant Diffusion"], s["3D"], s["Log Scale"],
									   sc["Pixel Size"], sc["Exposure"], s["Fit"], np.array([s["Fit Length"]], dtype=np.float64))
		self.df["MSD"] = res["MSD"]
		self.df["InD"] = res["InD"]
		self.df["Fit"] = res["Fit"]

		if s["MSD"] and not res["MSD"].empty:
			self._logger.add("\tEnregistrement du fichier de calcul des MSD.")
			res["MSD"].to_csv(f"{self._path}/tracking_MSD-{self._suffix}.csv", index=False)
		if s["Instant Diffusion"] and not res["InD"].empty:
			self._logger.add("\tEnregistrement du fichier de calcul des diffusions instantannées.")
			res["InD"].to_csv(f"{self._path}/tracking_InstantD-{self._suffix}.csv", index=False)
		if s["Fit"] != 0 and not res["Fit"].empty:
			self._logger.add("\tEnregistrement du fichier de calcul des métriques de l'ajustement.")
			res["Fit"].to_csv(f"{self._path}/tracking_Fit-{self._suffix}.csv", index=False)
		self.__filter_tracks_compute()

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
		if fit.empty:  # Vide (non calculé)
			self._logger.add("\t\tCalcul sur les trajectoires à effectuer pour définir une couleur lors de la visualisation.")
			if self.settings.tracks_compute["Fit"].get_value() == 0:  # On active le fit lineaire si aucun n'est sélectionné.
				self.settings.tracks_compute["Fit"].set_value(1)
			self.__tracks_compute()  # On lance le calcul
			fit = self.tracks_compute["Fit"]  # On reaffecte le resultat
		if fit.empty:  # Toujours vide (erreur de calcul ou autre, on prend le numéro des trajectoires par défaut)
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
	def __visualization_hr(self):
		""" Lance la creation d'une visualisation haute résolution à partir des settings passés en paramètres. """
		# Parse settings
		s = self.settings.visualization_hr.get_settings()

		# Création de l'image finale
		depth, height, width = self._stack.shape
		if s["Type"] == 0:
			if self.localizations.empty:
				self._logger.add(f"\tAucune donnée de localisation pour la visualisation.")
			else:
				sources = HR_LOC_SOURCE[1:] if s["Source L"] == 0 else [HR_LOC_SOURCE[s["Source L"]]]
				for source in sources:
					self.visualization = render_hr_image(width, height, s["Ratio"], self.localizations[["X", "Y", source]].to_numpy())
					self._logger.add(f"\tEnregistrement de la visualisation haute résolution (x{s['Ratio']}, {source}).")
					save_png(self.visualization, f"{self._path}/visualization_x{s['Ratio']}_{source}-{self._suffix}.png")
		else:
			if self.tracks.empty:
				self._logger.add(f"\tAucune donnée de trajectoires pour la visualisation.")
			else:
				sources = HR_TRC_SOURCE[1:] if s["Source T"] == 0 else [HR_TRC_SOURCE[s["Source T"]]]
				for source in sources:
					tracks = self.add_color_to_tracks(self.tracks, source)
					tracks.to_csv(f"{self._path}/tracking_hr_color-{self._suffix}.csv", index=False)
					self.visualization = render_tracks_image(width, height, s["Ratio"], tracks)
					self.visualization = grayscale_to_color(self.visualization, "viridis")
					self._logger.add(f"\tEnregistrement de la visualisation des trajectoires haute résolution (x{s['Ratio']}, {source}).")
					save_png(self.visualization, f"{self._path}/visualization_tracks_x{s['Ratio']}_{source}-{self._suffix}.png")

	##################################################
	def __visualization_graph(self):
		""" Lance la creation d'une visualisation graphique à partir des settings passés en paramètres. """
		if self.localizations.empty:
			self._logger.add(f"\tAucune donnée de localisation pour la visualisation de graphiques.")
			return

		# Parse settings
		s = self.settings.visualization_graph.get_settings()
		sources = GRAPH_SOURCE[1:] if s["Source"] == 0 else [GRAPH_SOURCE[s["Source"]]]
		modes = GRAPH_MODE[1:] if s["Mode"] == 0 else [GRAPH_MODE[s["Mode"]]]

		for source in sources:
			loc = self.localizations[["Plane", source]].to_numpy()
			if np.all(loc[:, 1] == loc[0, 1]):
				self._logger.add(f"\tAnnulation de la visualisation graphique : {source} uniforme.")
				continue

			for mode in modes:
				fig, ax = plt.subplots()
				if mode == "Histogram":
					plot_histogram(ax, loc[:, 1], source + " Histogram", True, True, False)
				elif mode == "Plane Heat Map":
					plot_plane_heatmap(ax, loc, source + " Heatmap")
				else:  # elif mode == "Plane Violin":
					plot_plane_violin(ax, loc, source + " Violin")
				self._logger.add(f"\tEnregistrement de la visualisation graphique ({mode}, {source}).")
				fig.savefig(f"{self._path}/graph_{mode}_{source}-{self._suffix}.png", bbox_inches="tight")
				plt.close(fig)

	##################################################
	def __gallery(self):
		""" Lance la génération d'une galerie à partir des settings passés en paramètres. """
		s = self.settings.gallery.get_settings()
		if self.localizations.empty:
			self._logger.add(f"\tAucune donnée de localisation pour la génération d'une galerie.")
			return
		gallery = make_gallery(self._stack, self.localizations, s["ROI Size"], s["ROIs Per Line"])
		self._logger.add(f"\tEnregistrement de la galerie ({s}).")
		save_tif(gallery, f"{self._path}/gallery_{s['ROI Size']}_{s['ROIs Per Line']}-{self._suffix}.tif")

	# ==================================================
	# endregion Visualization
	# ==================================================

	# ==================================================
	# region Filtering
	# ==================================================
	##################################################
	def __filter_localizations(self):
		""" Filtre le fichier de localisation. """
		n_init = len(self.df["loc"])
		self.df["f_loc"] = self.filter_localizations(self.df["loc"])
		n_end = len(self.df["f_loc"])
		if n_init != n_end:
			self._logger.add(f"\t\tFiltrage du fichier de localisation {n_end} localisations au lieu de {n_init} : {n_init - n_end} suppression(s)")
		if self.settings.filtering["Save"].get_value():
			self._logger.add("\tEnregistrement du fichier de localisation filtré")
			self.df["f_loc"].to_csv(f"{self._path}/localizations_filtered-{self._suffix}.csv", index=False)

	##################################################
	def __filter_tracks(self, name: str, suffix: str = ""):
		""" Filtre le fichier de tracking. """
		n_init = len(self.df[name])
		o_name = f"f_{name}"
		self.df[o_name] = self.filter_tracks(self.df[name])
		n_end = len(self.df[o_name])
		if n_init != n_end:
			self._logger.add(f"\t\tFiltrage du fichier de trajectoires {n_end} points au lieu de {n_init} : {n_init - n_end} suppression(s)")
		if self.settings.filtering["Save"].get_value():
			self._logger.add("\tEnregistrement du fichier de trajectoires filtré")
			self.df[o_name].to_csv(f"{self._path}/tracking_filtered{suffix}-{self._suffix}.csv", index=False)

	##################################################
	def __filter_tracks_compute(self):
		""" Filtre les fichiers de metrique. """
		n_init = len(self.df["MSD"])
		o_name = "f_trc" if self.df["blk"].empty else "f_blk"
		self.df[o_name], self.df["f_MSD"], self.df["f_InD"], self.df["f_Fit"] \
			= self.filter_tracks_compute(self.tracks, self.df["MSD"], self.df["InD"], self.df["Fit"])

		n_end = len(self.df["f_MSD"])
		if n_init != n_end:
			self._logger.add(f"\t\tFiltrage du fichier de calcul sur trajectoires {n_end} trajectoires au lieu de {n_init} : {n_init - n_end} suppression(s)")
		if self.settings.filtering["Save"].get_value():
			if not self.df["f_MSD"].empty:
				self._logger.add("\tEnregistrement du fichier de calcul des MSD filtré.")
				self.df["f_MSD"].to_csv(f"{self._path}/tracking_MSD_filtered-{self._suffix}.csv", index=False)
			if not self.df["f_InD"].empty:
				self._logger.add("\tEnregistrement du fichier de calcul des diffusions instantannées filtré.")
				self.df["f_InD"].to_csv(f"{self._path}/tracking_InstantD_filtered-{self._suffix}.csv", index=False)
			if not self.df["f_Fit"].empty:
				self._logger.add("\tEnregistrement du fichier de calcul des métriques de l'ajustement filtré.")
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
		fg = cast(FilteringL, f["Localization"])
		filters = [[f["Plane"], "Plane"],
				   [f["Intensity"], "Integrated Intensity"],
				   [fg["MSE"], "MSE XY"],
				   [fg["Sigma X"], "Sigma X"],
				   [fg["Sigma Y"], "Sigma Y"],
				   [fg["Theta"], "Theta"],
				   [fg["Circularity"], "Circularity"],
				   [fg["Z"], "Z"]]

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
		f = cast(FilteringT, self.settings.filtering["Tracks"])
		if isinstance(f["Length"], CheckRangeInt) and f["Length"].active:
			limits = f["Length"].get_value()
			counts = res.groupby("Track").size()  # Comptage par trajectoire
			keep_ids = counts.index[(counts >= limits[0]) & (counts <= limits[1])]  # IDs de trajectoires gardées: min_len <= nb points <= max_len
			res = res[res["Track"].isin(keep_ids)]  # Filtrage (on garde l'ordre original)
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

		# ===== Base : tous les IDs présents dans la référence =====
		keep_ids: set = set(o_trc["Track"].unique().tolist())
		# print(f"Base ID ({len(keep_ids)}) : {keep_ids}")
		# ===== Filtre Longueur =====
		if isinstance(f["Length"], CheckRangeInt) and f["Length"].active:
			limits_l = f["Length"].get_value()
			counts = o_trc.groupby("Track").size()
			ok_len_ids = set(counts.index[(limits_l[0] <= counts) & (counts <= limits_l[1])].tolist())
			keep_ids &= ok_len_ids  # intersection sur des sets d'IDs

		# print(f"ID After Length filter ({len(keep_ids)}) : {keep_ids}")
		# ===== Filtre sur Instant D =====
		if isinstance(f["Instant D"], CheckRangeFloat) and f["Instant D"].active and not o_ind.empty:
			limits_d = f["Instant D"].get_value()

			o_ind = o_ind[o_ind["Track"].isin(keep_ids)]  # Restreindre aux trajectoires admissibles jusqu'ici
			if not o_ind.empty:
				# colonnes de valeurs = toutes sauf 'Track'
				val_cols = [c for c in o_ind.columns if c != "Track"]

				# masque valeurs valides et hors bornes
				vals = o_ind[val_cols]
				valid = vals.notna()
				outside = (vals <= limits_d[0]) | (limits_d[1] <= vals)

				# % hors bornes par ligne (NaN ignorés)
				n_valid = valid.sum(axis=1)
				n_out = (outside & valid).sum(axis=1)
				pct_out = (n_out / n_valid).fillna(0.0) * 100.0
				# avec une troisieme valeur limit[2] qui serait le pourcentage de fail max autorisé
				# Ou alors un nouveau setting type Instant D Failure Tolerance (%), je vais mettre 50% ici
				ok_ids = set(map(int, np.unique(o_ind.loc[pct_out <= 50.0, "Track"].to_numpy())))
				keep_ids &= ok_ids
		# for track_id, pct in zip(df["Track"], pct_out): print(f"Track {track_id}: {pct:.1f}% outside {limits}")

		# print(f"ID After Instant D ({len(keep_ids)}) : {keep_ids}")
		# ===== Filtre sur Fit =====
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

		# print(f"ID After Fit ({len(keep_ids)}) : {keep_ids}")
		# ===== Filtre final des trajectoires restantes =====
		if not o_trc.empty: o_trc = o_trc[o_trc["Track"].isin(keep_ids)]
		if not o_msd.empty: o_msd = o_msd[o_msd["Track"].isin(keep_ids)]
		if not o_ind.empty: o_ind = o_ind[o_ind["Track"].isin(keep_ids)]
		if not o_fit.empty: o_fit = o_fit[o_fit["Track"].isin(keep_ids)]
		return o_trc, o_msd, o_ind, o_fit

	##################################################
	def update_filtered(self, last:bool = True):
		"""Recalcul les filtres sur le dernier dataframe disponible pour chacun si last est sélectionné, sinon sur l'original."""

		self._suffix = datetime.now().strftime("%Y%d%m_%H%M%S")
		loc = self.df["loc"] if self.df["f_loc"].empty or not last else self.df["f_loc"]
		trc = self.df["trc"] if self.df["f_trc"].empty or not last else self.df["f_trc"]
		blk = self.df["blk"] if self.df["f_blk"].empty or not last else self.df["f_blk"]
		if last : tc = self.tracks_compute
		else : tc =  {"MSD": self.df["MSD"], "InD": self.df["InD"], "Fit": self.df["Fit"]}

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
# ==================================================
# endregion Filtering
# ==================================================
