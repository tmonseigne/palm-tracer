"""
Module contenant les fonctions de traitement de PALM.
"""

import ctypes
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import cast

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from palm_tracer.Processing import render_hr_image, load_dll, plot_histogram, plot_plane_heatmap, plot_plane_violin, run_palm_stack_dll, run_tracking_dll
from palm_tracer.Settings import Settings
from palm_tracer.Settings.Groups import GaussianFit
from palm_tracer.Settings.Groups.VisualizationGraph import GRAPH_SOURCE
from palm_tracer.Settings.Groups.VisualizationHR import HR_SOURCE
from palm_tracer.Tools import get_last_file, Logger, print_warning, save_json
from palm_tracer.Tools.FileIO import save_png


@dataclass
class PALMTracer:
	""" Classe principale de PALM Tracer. """

	settings: Settings = field(init=False, default_factory=Settings)
	dlls: dict[str, ctypes.CDLL] = field(init=False, default_factory=dict)
	logger: Logger = field(init=False, default_factory=Logger)
	localizations: pd.DataFrame | None = field(init=False, default=None)
	tracks: pd.DataFrame | None = field(init=False, default=None)
	visualization: np.ndarray | None = field(init=False, default=None)
	graph: plt.Figure | None = field(init=False, default=None)

	__path: str = field(init=False, default="")
	__stack: np.ndarray | None = field(init=False, default=None)
	__suffix: str = field(init=False, default="")

	##################################################
	def __post_init__(self):
		"""Méthode appelée automatiquement après l'initialisation du dataclass."""
		self.dlls = load_dll()

	##################################################
	def is_dll_valid(self):
		return self.dlls.get("CPU", None) is not None and self.dlls.get("Tracking", None) is not None

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

		for self.__path, self.__stack in zip(paths, stacks):
			# Logger
			os.makedirs(self.__path, exist_ok=True)
			self.__suffix = datetime.now().strftime("%Y%d%m_%H%M%S")
			self.logger.open(f"{self.__path}/log-{self.__suffix}.log")
			self.logger.add("Commencer le traitement.")
			self.logger.add(f"Dossier de sortie : {self.__path}")

			# Save settings
			save_json(f"{self.__path}/settings-{self.__suffix}.json", self.settings.to_dict())
			self.logger.add("Paramètres sauvegardés.")

			# Si transformation de la zone en entrée (par une ROI) à faire ici.

			# Save meta file (Création du DataFrame et sauvegarde en CSV)
			depth, height, width = self.__stack.shape
			df = pd.DataFrame({"Height":                   [height], "Width": [width], "Plane Number": [depth],
							   "Pixel Size (nm)":          [self.settings.calibration["Pixel Size"].get_value()],
							   "Exposure Time (ms/frame)": [self.settings.calibration["Exposure"].get_value()],
							   "Intensity (photon/ADU)":   [self.settings.calibration["Intensity"].get_value()]})
			df.to_csv(f"{self.__path}/meta-{self.__suffix}.csv", index=False)
			self.logger.add("Fichier Meta sauvegardé.")

			# Lancement de la localisation
			if self.settings.localization.active:
				self.logger.add("Localisation activée.")
				self.__localization()
			else:
				self.logger.add("Localisation désactivé.")
				f = get_last_file(self.__path, "localizations")
				if f.endswith("csv"):  # Chargement d'une localisation existante
					self.logger.add("\tChargement d'une localisation pré-calculée.")
					try:
						self.localizations = pd.read_csv(f)  # Lecture du fichier CSV avec pandas
						self.logger.add(f"\tFichier '{f}' chargé avec succès.")
						self.logger.add(f"\t\t{len(self.localizations)} localisation(s) trouvée(s).")
					except Exception as e:
						self.localizations = None
						self.logger.add(f"\tErreur lors du chargement du fichier '{f}' : {e}")
				else:  # Sinon
					self.localizations = None
					self.logger.add("\tAucune donnée de localisation pré-calculée.")

			# Lancement du tracking
			if self.settings.tracking.active:
				self.logger.add("Tracking activé.")
				self.__tracking()

			else:
				self.logger.add("Tracking désactivé.")
				f = get_last_file(self.__path, "tracking")
				if f.endswith("csv"):  # Chargement d'une localisation existante
					self.logger.add("\tChargement d'un tracking pré-calculée.")
					try:
						self.tracks = pd.read_csv(f)  # Lecture du fichier CSV avec pandas
						self.logger.add(f"\tFichier '{f}' chargé avec succès.")
						self.logger.add(f"\t\t{len(self.tracks)} tracking(s) trouvée(s).")
					except Exception as e:
						self.tracks = None
						self.logger.add(f"\tErreur lors du chargement du fichier '{f}' : {e}")
				else:  # Sinon
					self.tracks = None
					self.logger.add("\tAucune donnée de tracking pré-calculée.")

			# Lancement de la Visualisation Haute Résolution
			if self.settings.visualization_hr.active:
				self.logger.add("Visualisation haute résolution activée.")
				self.__visualization_hr()
			else:
				self.logger.add("Visualisation haute résolution désactivée.")
				self.visualization = None

			# Lancement de la Visualisation graphique
			if self.settings.visualization_graph.active:
				self.logger.add("Visualisation graphique activée.")
				self.__visualization_graph()
			else:
				self.logger.add("Visualisation graphique désactivée.")
				self.graph = None

			# Fermeture du Log
			self.logger.add("Traitement terminé.")
			self.logger.close()

	##################################################
	def __localization(self):
		"""
		Lance la localisation à partir des settings passés en paramètres.

		:return: Données de localisation trouvées.
		"""
		# Parse settings
		s = self.settings.localization.get_settings()
		# Run command
		self.localizations = run_palm_stack_dll(self.dlls["CPU"], self.__stack, s["Threshold"], s["Watershed"],
												s["Gaussian Fit Mode"], s["Gaussian Fit Sigma"], s["Gaussian Fit Theta"], s["ROI Size"])

		self.logger.add("\tEnregistrement du fichier de localisation")
		self.logger.add(f"\t\t{len(self.localizations)} localisation(s) trouvée(s).")
		self.localizations.to_csv(f"{self.__path}/localizations-{self.__suffix}.csv", index=False)

	##################################################
	def __tracking(self):
		"""
		Lance le tracking à partir des settings passés en paramètres.

		:return: Données de tracking trouvées.
		"""
		# Parse settings
		s = self.settings.tracking.get_settings()
		# Run command
		self.tracks = run_tracking_dll(self.dlls["Tracking"], self.localizations, s["Max Distance"], s["Min Length"], s["Decrease"], s["Cost Birth"])

		self.logger.add("\tEnregistrement du fichier de tracking.")
		self.logger.add(f"\t\t{len(self.tracks)} tracking(s) trouvé(s).")
		self.tracks.to_csv(f"{self.__path}/tracking-{self.__suffix}.csv", index=False)

	##################################################
	def __visualization_hr(self):
		"""
		Lance la creation d'une visualisation haute résolution à partir des settings passés en paramètres.

		:return: Nouvelle visualisation.
		"""
		# Parse settings
		s = self.settings.visualization_hr.get_settings()

		# Création de l'image finale
		depth, height, width = self.__stack.shape
		if self.localizations is not None:
			self.visualization = render_hr_image(width, height, s["Ratio"], self.localizations[["X", "Y", HR_SOURCE[s['Source']]]].to_numpy())
			self.logger.add(f"\tEnregistrement du fichier de visualisation haute résolution (x{s['Ratio']}, s{s['Source']}).")
			save_png(self.visualization, f"{self.__path}/visualization_x{s['Ratio']}_s{s['Source']}-{self.__suffix}.png")
		else:
			self.logger.add(f"\tAucun fichier de localisation pour la visualisation.")

	##################################################
	def __visualization_graph(self):
		"""
		Lance la creation d'une visualisation graphique à partir des settings passés en paramètres.

		"""
		# Parse settings
		s = self.settings.visualization_graph.get_settings()

		self.graph, ax = plt.subplots()
		if self.localizations is None: return

		source = GRAPH_SOURCE[s["Source"]]
		if s["Mode"] == 0:  # Histogram
			plot_histogram(ax, self.localizations[source].to_numpy(), source + " Histogram", True, True, False)
		elif s["Mode"] == 1:  # Plane Heat Map
			plot_plane_heatmap(ax, self.localizations[["Plane", source]].to_numpy(), source + " Heatmap")
		else: # elif mode == 2:  # Plane Violin
			plot_plane_violin(ax, self.localizations[["Plane", source]].to_numpy(), source + " Violin")

		self.logger.add("\tEnregistrement du fichier de visualisation graphique.")
		self.graph.savefig(f"{self.__path}/graph_m{s['Mode']}_s{s['Source']}-{self.__suffix}.png", bbox_inches="tight")
