"""
Module contenant les fonctions de traitement de PALM.
"""

import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import cast, Optional

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from palm_tracer.Processing import make_gallery, Palm, plot_histogram, plot_plane_heatmap, plot_plane_violin, render_hr_image, Tracking
from palm_tracer.Settings import Settings
from palm_tracer.Settings.Groups import Filtering, FilteringGF
from palm_tracer.Settings.Groups.VisualizationGraph import GRAPH_MODE, GRAPH_SOURCE
from palm_tracer.Settings.Groups.VisualizationHR import HR_SOURCE
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
	# gpu: DLL.GPU = field(init=False, default_factory=DLL.GPU)
	_tracking: Tracking = field(init=False, default_factory=Tracking)
	"""Interface vers la DLL C++ Tracking."""
	_logger: Logger = field(init=False, default_factory=Logger)
	"""Journal d'activité."""
	localizations: Optional[pd.DataFrame] = field(init=False, default=None)
	"""Résultat de la localisation Palm."""
	tracks: Optional[pd.DataFrame] = field(init=False, default=None)
	"""Résultat du tracking."""
	visualization: Optional[np.ndarray] = field(init=False, default=None)
	"""Résultat de la visualisation."""

	_path: str = field(init=False, default="")
	"""Dossier de sortie pour le fichier en cours de traitement."""
	_stack: Optional[np.ndarray] = field(init=False, default=None)
	"""Pile en cours de traitement."""
	_suffix: str = field(init=False, default="")
	"""Suffixe des fichiers pour un traitement (timestamp au format YYYYMMDD_HHMMSS)."""

	##################################################
	def is_dll_valid(self) -> bool:
		"""
		Vérifie la validité des DLL utilisées par le plugin.

		Cette méthode teste si les deux bibliothèques dynamiques (CPU et tracking) sont correctement chargées et prêtes à être utilisées.
		:return: True si les deux DLL sont valides, False sinon.
		"""
		return self.palm.is_valid() and self._tracking.is_valid()

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
			df = pd.DataFrame({"Height":                   [height], "Width": [width], "Plane Number": [depth],
							   "Pixel Size (nm)":          [self.settings.calibration["Pixel Size"].get_value()],
							   "Exposure Time (ms/frame)": [self.settings.calibration["Exposure"].get_value()],
							   "Intensity (photon/ADU)":   [self.settings.calibration["Intensity"].get_value()]})
			df.to_csv(f"{self._path}/meta-{self._suffix}.csv", index=False)
			self._logger.add("Fichier Meta sauvegardé.")

			# Lancement de la localisation
			if self.settings.localization.active:
				self._logger.add("Localisation activée.")
				self.__localization()
			else:
				self._logger.add("Localisation désactivé.")
				f = get_last_file(self._path, "localizations")
				if f.endswith("csv"):  # Chargement d'une localisation existante
					self._logger.add("\tChargement d'une localisation pré-calculée.")
					try:
						self.localizations = pd.read_csv(f)  # Lecture du fichier CSV avec pandas
						self._logger.add(f"\tFichier '{f}' chargé avec succès.")
						self.__filter_localizations()
						self._logger.add(f"\t\t{len(self.localizations)} localisation(s) trouvée(s).")
					except Exception as e:
						self.localizations = None
						self._logger.add(f"\tErreur lors du chargement du fichier '{f}' : {e}")
				else:  # Sinon
					self.localizations = None
					self._logger.add("\tAucune donnée de localisation pré-calculée.")

			# Lancement du tracking
			if self.settings.tracking.active:
				self._logger.add("Tracking activé.")
				self.__tracking()

			else:
				self._logger.add("Tracking désactivé.")
				f = get_last_file(self._path, "tracking")
				if f.endswith("csv"):  # Chargement d'une localisation existante
					self._logger.add("\tChargement d'un tracking pré-calculée.")
					try:
						self.tracks = pd.read_csv(f)  # Lecture du fichier CSV avec pandas
						self._logger.add(f"\tFichier '{f}' chargé avec succès.")
						self._logger.add(f"\t\t{len(self.tracks)} tracking(s) trouvée(s).")
					except Exception as e:
						self.tracks = None
						self._logger.add(f"\tErreur lors du chargement du fichier '{f}' : {e}")
				else:  # Sinon
					self.tracks = None
					self._logger.add("\tAucune donnée de tracking pré-calculée.")

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

	##################################################
	def __localization(self):
		""" Lance la localisation à partir des settings passés en paramètres. """
		# Parse settings
		s = self.settings.localization.get_settings()
		filters = self.settings.filtering
		# Filtre sur les plans
		planes = filters["Plane"].get_value()
		planes = list(range(planes[0] - 1, planes[1])) if filters["Plane"].active else None
		fit = Palm.get_fit(s["Fit"], s["Gaussian Fit Mode"])
		# Run command
		self.localizations = self.palm.localization(self._stack, s["Threshold"], s["Watershed"], fit,
													s["Gaussian Fit Sigma"], s["Gaussian Fit Theta"], s["ROI Size"], planes)

		self.__filter_localizations()
		self._logger.add("\tEnregistrement du fichier de localisation")
		self._logger.add(f"\t\t{len(self.localizations)} localisation(s) trouvée(s).")
		self.localizations.to_csv(f"{self._path}/localizations-{self._suffix}.csv", index=False)

	##################################################
	def __tracking(self):
		""" Lance le tracking à partir des settings passés en paramètres. """
		# Parse settings
		s = self.settings.tracking.get_settings()
		# Run command
		self.tracks = self._tracking.run(self.localizations, s["Max Distance"], s["Min Length"], s["Decrease"], s["Cost Birth"])

		self._logger.add("\tEnregistrement du fichier de tracking.")
		self._logger.add(f"\t\t{len(self.tracks)} tracking(s) trouvé(s).")
		self.tracks.to_csv(f"{self._path}/tracking-{self._suffix}.csv", index=False)

	##################################################
	def __visualization_hr(self):
		""" Lance la creation d'une visualisation haute résolution à partir des settings passés en paramètres. """
		# Parse settings
		s = self.settings.visualization_hr.get_settings()

		# Création de l'image finale
		depth, height, width = self._stack.shape
		if self.localizations is not None:
			sources = HR_SOURCE[1:] if s["Source"] == 0 else [HR_SOURCE[s["Source"]]]
			for source in sources:
				self.visualization = render_hr_image(width, height, s["Ratio"], self.localizations[["X", "Y", source]].to_numpy())
				self._logger.add(f"\tEnregistrement de la visualisation haute résolution (x{s['Ratio']}, {source}).")
				save_png(self.visualization, f"{self._path}/visualization_x{s['Ratio']}_{source}-{self._suffix}.png")
		else:
			self._logger.add(f"\tAucun fichier de localisation pour la visualisation.")

	##################################################
	def __visualization_graph(self):
		""" Lance la creation d'une visualisation graphique à partir des settings passés en paramètres. """
		if self.localizations is None: return

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
		if self.localizations is None: return
		gallery = make_gallery(self._stack, self.localizations, s["ROI Size"], s["ROIs Per Line"])
		self._logger.add(f"\tEnregistrement de la galerie ({s}).")
		save_tif(gallery, f"{self._path}/gallery_{s['ROI Size']}_{s['ROIs Per Line']}-{self._suffix}.tif")

	##################################################
	def __filter_localizations(self):
		""" Filtre le fichier de localisation. """
		n_init = len(self.localizations)
		self.localizations = self.filter_localizations(self.localizations)
		n_end = len(self.localizations)
		if n_init != n_end:
			self._logger.add(f"\t\tFiltrage du fichier de localisation {n_end} localisations au lieu de {n_init} : {n_init - n_end} suppression(s)")

	##################################################
	def filter_localizations(self, localizations: pd.DataFrame) -> pd.DataFrame:
		"""
		Filtre un fichier de localisation.

		:param localizations: fichier à filtrer
		:return: fichier filtré.
		"""
		f = cast(Filtering, self.settings.filtering)
		fg = cast(FilteringGF, f["Gaussian Fit"])
		filters = [[f["Plane"], "Plane"],
				   [f["Intensity"], "Integrated Intensity"],
				   [fg["MSE Gaussian"], "MSE Gaussian"],
				   [fg["Sigma X"], "Sigma X"],
				   [fg["Sigma Y"], "Sigma Y"],
				   [fg["Theta"], "Theta"],
				   [fg["Circularity"], "Circularity"],
				   [fg["Z"], "Z"]]

		for filt, col in filters:
			if isinstance(filt, CheckRangeFloat | CheckRangeInt) and filt.active:
				limits = filt.get_value()
				localizations = localizations[localizations[col].between(limits[0], limits[1])]  # Bornes incluses
		return localizations

# ##################################################
# def __filter_tracking(self):
# 	""" Filtre le fichier de tracking. """
# 	n_init = len(self.tracks)
# 	f = self.settings.filtering["Tracking"]
# 	filters = [[f["Length"], ""],
# 			   [f["D Coeff"], ""],
# 			   [f["Instant D"], ""],
# 			   [f["Speed"], ""],
# 			   [f["Alpha"], ""],
# 			   [f["Confinement"], ""]]
#
# 	n_end = len(self.tracks)
# 	if n_init != n_end:
# 		self.logger.add(f"\t\tFiltrage du fichier de tracking {n_end} tracks au lieu de {n_init} : {n_init - n_end} suppression(s)")
