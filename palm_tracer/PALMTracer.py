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
from palm_tracer.Settings.Groups import Filtering, FilteringGF, FilteringT
from palm_tracer.Settings.Groups.VisualizationGraph import GRAPH_MODE, GRAPH_SOURCE
from palm_tracer.Settings.Groups.VisualizationHR import HR_LOC_SOURCE, HR_TRC_SOURCE
from palm_tracer.Settings.Types import CheckRangeFloat, CheckRangeInt
from palm_tracer.Tools import get_last_file, Logger, print_warning, save_json, save_tif
from palm_tracer.Tools.FileIO import save_png


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
	_df: dict[str, pd.DataFrame] = field(init=False, default_factory=lambda: {
			"loc":            pd.DataFrame(),
			"blk":            pd.DataFrame(),
			"trc":            pd.DataFrame(),
			"trc_MSD":        pd.DataFrame(),
			"trc_InstantD":   pd.DataFrame(),
			"trc_Fit":        pd.DataFrame(),
			"f_loc":          pd.DataFrame(),
			"f_blk":          pd.DataFrame(),
			"f_trc":          pd.DataFrame(),
			"f_trc_MSD":      pd.DataFrame(),
			"f_trc_InstantD": pd.DataFrame(),
			"f_trc_Fit":      pd.DataFrame()})
	"""Résultats des différents calculs."""

	visualization: Optional[np.ndarray] = field(init=False, default=None)
	"""Résultat de la visualisation."""
	_path: str = field(init=False, default="")
	"""Dossier de sortie pour le fichier en cours de traitement."""
	_stack: Optional[np.ndarray] = field(init=False, default=None)
	"""Pile en cours de traitement."""
	_suffix: str = field(init=False, default="")
	"""Suffixe des fichiers pour un traitement (timestamp au format YYYYMMDD_HHMMSS)."""

	# ==================================================
	# region Initialization
	# ==================================================
	##################################################
	def is_dll_valid(self) -> bool:
		"""
		Vérifie la validité des DLL utilisées par le plugin.

		Cette méthode teste si les deux bibliothèques dynamiques (CPU et tracking) sont correctement chargées et prêtes à être utilisées.
		:return: True si les deux DLL sont valides, False sinon.
		"""
		return self.palm.is_valid()

	##################################################
	@property
	def localizations(self) -> pd.DataFrame:
		"""Getter de la localisation (filtrée si elle est non vide) """
		return self._df["loc"] if self._df["f_loc"].empty else self._df["f_loc"]

	##################################################
	@property
	def tracks(self) -> pd.DataFrame:
		"""Getter des trajectoires (filtrée si elle est non vide) et reconnecté si elle est non vide également. """
		if self._df["f_blk"].empty:
			if self._df["blk"].empty:
				if self._df["f_trc"].empty:
					return self._df["trc"]
				return self._df["f_trc"]
			return self._df["blk"]
		return self._df["f_blk"]

	##################################################
	@property
	def tracks_compute(self) -> dict[str, pd.DataFrame]:
		"""Getter des calculs sur trajectoires (filtrés si non vide). """
		if self._df["f_trc_MSD"].empty and self._df["f_trc_InstantD"].empty and self._df["f_trc_Fit"].empty:
			return {"MSD": self._df["trc_MSD"], "InstantD": self._df["trc_InstantD"], "Fit": self._df["trc_Fit"]}
		return {"MSD": self._df["f_trc_MSD"], "InstantD": self._df["f_trc_InstantD"], "Fit": self._df["f_trc_Fit"]}

	##################################################
	def reset_result(self):
		"""Vide entièrement les DataFrame de résultat dans `_cp`."""
		for key, value in self._df.items():
			self._df[key] = pd.DataFrame()
		self.visualization = None

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
						self._df["loc"] = pd.read_csv(f)  # Lecture du fichier CSV avec pandas
						self._logger.add(f"\tFichier '{f}' chargé avec succès.")
						self.__filter_localizations()
						self._logger.add(f"\t\t{len(self.localizations)} localisation(s) trouvée(s).")
					except Exception as e:
						self._df["loc"] = pd.DataFrame()
						self._logger.add(f"\tErreur lors du chargement du fichier '{f}' : {e}")
				else:  # Sinon
					self._df["loc"] = pd.DataFrame()
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
						self._df["trc"] = pd.read_csv(f)  # Lecture du fichier CSV avec pandas
						self._logger.add(f"\tFichier '{f}' chargé avec succès.")
						self._logger.add(f"\t\t{len(self.tracks)} trajectoire(s) trouvée(s).")
					except Exception as e:
						self._df["trc"] = pd.DataFrame()
						self._logger.add(f"\tErreur lors du chargement du fichier '{f}' : {e}")
				else:  # Sinon
					self._df["trc"] = pd.DataFrame()
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
		self._df["loc"] = self.palm.localization(self._stack, s["Threshold"], s["Watershed"], fit, fit_params, planes)

		self._logger.add("\tEnregistrement du fichier de localisation")
		self._logger.add(f"\t\t{len(self._df['loc'])} localisation(s) trouvée(s).")
		self._df["loc"].to_csv(f"{self._path}/localizations-{self._suffix}.csv", index=False)
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
		self._df["trc"] = self.palm.tracking(df, s["Max Distance"])

		self._logger.add("\tEnregistrement du fichier de trajectoires.")
		self._logger.add(f"\t\t{len(self._df['trc'])} point(s) trouvé(s).")
		self._df["trc"].to_csv(f"{self._path}/tracking-{self._suffix}.csv", index=False)
		self.__filter_tracks("trc")

		if self.settings.tracking["Blinking Reconnection"].active:
			self._logger.add("\tReconnexion des trajectoires après scintillement.")
			s = self.settings.tracking["Blinking Reconnection"].get_settings()
			pixel_size = self.settings.calibration.get_settings()["Pixel Size"]
			# Run command sur la version non filtrée des trajectoires
			self._df["blk"] = self.palm.blinking_reconnection(self._df["trc"], pixel_size, s["Mode"], s["Max Duration"], s["Max Speed"])

			self._logger.add("\tEnregistrement du fichier de trajectoires reconnectées.")
			self._logger.add(f"\t\t{len(self._df['blk'])} point(s) trouvé(s).")
			self._df["blk"].to_csv(f"{self._path}/tracking-reconnected-{self._suffix}.csv", index=False)
			self.__filter_tracks("blk", "_reconnected")

		if not self._df["blk"].empty:
			self._df["trc"] = self._df["blk"]
			self._df["blk"] = pd.DataFrame()

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
		res = self.palm.tracks_compute(self._df["trc"], s["MSD"], s["Instant Diffusion"], s["3D"], s["Log Scale"],
									   sc["Pixel Size"], sc["Exposure"], s["Fit"], np.array([s["Fit Length"]], dtype=np.float64))
		self._df["trc_MSD"] = res["MSD"]
		self._df["trc_InstantD"] = res["InstantD"]
		self._df["trc_Fit"] = res["Fit"]

		if s["MSD"] and not res["MSD"].empty:
			self._logger.add("\tEnregistrement du fichier de calcul des MSD.")
			res["MSD"].to_csv(f"{self._path}/tracking_MSD-{self._suffix}.csv", index=False)
		if s["Instant Diffusion"] and not res["InstantD"].empty:
			self._logger.add("\tEnregistrement du fichier de calcul des diffusions instantannées.")
			res["InstantD"].to_csv(f"{self._path}/tracking_InstantD-{self._suffix}.csv", index=False)
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
	def __add_color_to_tracks(self, datas: pd.DataFrame) -> pd.DataFrame:
		""""""
		res = datas.copy()
		res["Color"] = 65535
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
				sources = HR_LOC_SOURCE[1:] if s["Source T"] == 0 else [HR_TRC_SOURCE[s["Source T"]]]
				for source in sources:
					tracks = self.__add_color_to_tracks(self.tracks)
					self.visualization = render_tracks_image(width, height, s["Ratio"], tracks)
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
		n_init = len(self._df["loc"])
		self._df["f_loc"] = self.filter_localizations(self._df["loc"])
		n_end = len(self._df["f_loc"])
		if n_init != n_end:
			self._logger.add(f"\t\tFiltrage du fichier de localisation {n_end} localisations au lieu de {n_init} : {n_init - n_end} suppression(s)")
		if self.settings.filtering["Save"].get_value():
			self._logger.add("\tEnregistrement du fichier de localisation filtré")
			self._df["f_loc"].to_csv(f"{self._path}/localizations_filtered-{self._suffix}.csv", index=False)

	##################################################
	def __filter_tracks(self, name: str, suffix: str = ""):
		""" Filtre le fichier de tracking. """
		n_init = len(self._df[name])
		output_name = f"f_{name}"
		self._df[output_name] = self.filter_tracks(self._df[name])
		n_end = len(self._df[output_name])
		if n_init != n_end:
			self._logger.add(f"\t\tFiltrage du fichier de trajectoires {n_end} points au lieu de {n_init} : {n_init - n_end} suppression(s)")
		if self.settings.filtering["Save"].get_value():
			self._logger.add("\tEnregistrement du fichier de trajectoires filtré")
			self._df[output_name].to_csv(f"{self._path}/tracking_filtered{suffix}-{self._suffix}.csv", index=False)

	##################################################
	def __filter_tracks_compute(self):
		""" Filtre les fichiers de metrique. """
		n_init = len(self._df["f_trc_MSD"])
		self._df["f_trc_MSD"], self._df["f_trc_InstantD"], self._df["f_trc_Fit"] \
			= self.filter_tracks_compute(self.tracks, self._df["trc_MSD"], self._df["trc_InstantD"], self._df["trc_Fit"])

		n_end = len(self._df["f_trc_MSD"])
		if n_init != n_end:
			self._logger.add(f"\t\tFiltrage du fichier de calcul sur trajectoires {n_end} trajectoires au lieu de {n_init} : {n_init - n_end} suppression(s)")
		if self.settings.filtering["Save"].get_value():
			if not self._df["f_trc_MSD"].empty:
				self._logger.add("\tEnregistrement du fichier de calcul des MSD filtré.")
				self._df["f_trc_MSD"].to_csv(f"{self._path}/tracking_MSD_filtered-{self._suffix}.csv", index=False)
			if not self._df["f_trc_InstantD"].empty:
				self._logger.add("\tEnregistrement du fichier de calcul des diffusions instantannées filtré.")
				self._df["f_trc_InstantD"].to_csv(f"{self._path}/tracking_InstantD_filtered-{self._suffix}.csv", index=False)
			if not self._df["f_trc_Fit"].empty:
				self._logger.add("\tEnregistrement du fichier de calcul des métriques de l'ajustement filtré.")
				self._df["f_trc_Fit"].to_csv(f"{self._path}/tracking_Fit_filtered-{self._suffix}.csv", index=False)

	##################################################
	def filter_localizations(self, datas: pd.DataFrame) -> pd.DataFrame:
		"""
		Filtre un DataFrame de localisation.

		:param datas: DataFrame à filtrer
		:return: DataFrame filtré.
		"""
		res = datas.copy()
		f = cast(Filtering, self.settings.filtering)
		fg = cast(FilteringGF, f["Gaussian Fit"])
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
		f = cast(FilteringT, self.settings.filtering["Tracks"])
		if isinstance(f["Length"], CheckRangeInt) and f["Length"].active:
			limits = f["Length"].get_value()
			counts = res.groupby("Track").size()  # Comptage par trajectoire
			keep_ids = counts.index[(counts >= limits[0]) & (counts <= limits[1])]  # IDs de trajectoires gardées: min_len <= nb points <= max_len
			print(keep_ids)
			res = res[res["Track"].isin(keep_ids)]  # Filtrage (on garde l'ordre original)
		return res

	##################################################
	def filter_tracks_compute(self, tracks: pd.DataFrame, msd: pd.DataFrame, instant_d: pd.DataFrame,
							  fit: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
		"""
		Filtre un DataFrame de calcul sur les trajectoires.

		:param tracks: DataFrame de trajectoires
		:param msd: DataFrame de calcul des MSD
		:param instant_d: DataFrame de calcul de la diffusion instantannée
		:param fit: DataFrame de calcul de l'ajustement
		:return: DataFrames filtrés.
		"""
		o_msd = msd.copy()
		o_ind = instant_d.copy()
		o_fit = fit.copy()
		if tracks.empty: return o_msd, o_ind, o_fit

		f = cast(FilteringT, self.settings.filtering["Tracks"])

		# ===== Base : tous les IDs présents dans la référence =====
		keep_ids: set = set(tracks["Track"].unique().tolist())
		# print(f"Base ID ({len(keep_ids)}) : {keep_ids}")
		# ===== Filtre Longueur =====
		if isinstance(f["Length"], CheckRangeInt) and f["Length"].active:
			limits_l = f["Length"].get_value()
			counts = tracks.groupby("Track").size()
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
		if not o_msd.empty: o_msd = o_msd[o_msd["Track"].isin(keep_ids)]
		if not o_ind.empty: o_ind = o_ind[o_ind["Track"].isin(keep_ids)]
		if not o_fit.empty: o_fit = o_fit[o_fit["Track"].isin(keep_ids)]
		return o_msd, o_ind, o_fit

# ==================================================
# endregion Filtering
# ==================================================
