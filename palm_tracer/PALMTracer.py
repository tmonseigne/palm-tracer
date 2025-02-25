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

from palm_tracer.Processing import hr_visualization, load_dll, run_palm_stack_dll, run_tracking_dll
from palm_tracer.Settings import Settings
from palm_tracer.Settings.Groups import GaussianFit
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

		for path, stack in zip(paths, stacks):
			# Logger
			os.makedirs(path, exist_ok=True)
			timestamp_suffix = datetime.now().strftime("%Y%d%m_%H%M%S")
			self.logger.open(f"{path}/log-{timestamp_suffix}.log")
			self.logger.add("Commencer le traitement.")
			self.logger.add(f"Dossier de sortie : {path}")

			# Save settings
			save_json(f"{path}/settings-{timestamp_suffix}.json", self.settings.to_dict())
			self.logger.add("Paramètres sauvegardés.")

			# Si transformation de la zone en entrée (par une ROI) à faire ici.

			# Save meta file (Création du DataFrame et sauvegarde en CSV)
			depth, height, width = stack.shape
			df = pd.DataFrame({"Height":                   [height], "Width": [width], "Plane Number": [depth],
							   "Pixel Size (nm)":          [self.settings.calibration["Pixel Size"].get_value()],
							   "Exposure Time (ms/frame)": [self.settings.calibration["Exposure"].get_value()],
							   "Intensity (photon/ADU)":   [self.settings.calibration["Intensity"].get_value()]})
			df.to_csv(f"{path}/meta-{timestamp_suffix}.csv", index=False)
			self.logger.add("Fichier Meta sauvegardé.")

			# Lancement de la localisation
			if self.settings.localization.active:
				self.logger.add("Localisation commencée.")
				self.localizations = self.__localization(stack)
				self.logger.add("\tEnregistrement du fichier de localisation")
				self.logger.add(f"\t\t{len(self.localizations)} localisation(s) trouvée(s).")
				self.localizations.to_csv(f"{path}/localizations-{timestamp_suffix}.csv", index=False)
			else:
				self.logger.add("Localisation désactivé.")
				f = get_last_file(path, "localizations")
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
				self.logger.add("Tracking commencé.")
				self.tracks = self.__tracking()
				self.logger.add("\tEnregistrement du fichier de tracking.")
				self.logger.add(f"\t\t{len(self.tracks)} tracking(s) trouvé(s).")
				self.tracks.to_csv(f"{path}/tracking-{timestamp_suffix}.csv", index=False)
			else:
				self.logger.add("Tracking désactivé.")
				f = get_last_file(path, "tracking")
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

			# Lancement de la visualisation Haute Résolution
			if self.settings.visualization_hr.active:
				self.logger.add("Visualisation Haute Résolution commencé.")
				self.visualization = self.__visualization(stack)
				self.logger.add("\tEnregistrement du fichier de visualisation Haute Résolution.")
				save_png(self.visualization, f"{path}/visualization-{timestamp_suffix}.png")
			else:
				self.logger.add("Visualisation Haute Résolution désactivée.")
				self.visualization = None

			# Fermeture du Log
			self.logger.add("Traitement terminé.")
			self.logger.close()

	##################################################
	def __localization(self, stack: np.ndarray) -> pd.DataFrame:
		"""
		Lance la localisation à partir des settings passés en paramètres.

		:param stack: Pile d'image d'entrée sous forme de tableau numpy.
		:return: Données de localisation trouvées.
		"""
		# Parse settings
		threshold = self.settings.localization["Threshold"].get_value()
		watershed = self.settings.localization["Watershed"].get_value()
		roi = self.settings.localization["ROI Size"].get_value()
		gaussian_setting = cast(GaussianFit, self.settings.localization["Gaussian Fit"])
		gaussian = gaussian_setting["Mode"].get_value()
		sigma = gaussian_setting["Sigma"].get_value()
		theta = gaussian_setting["Theta"].get_value()
		# Run command
		return run_palm_stack_dll(self.dlls["CPU"], stack, threshold, watershed, gaussian, sigma, theta, roi)

	##################################################
	def __tracking(self) -> pd.DataFrame:
		"""
		Lance le tracking à partir des settings passés en paramètres.

		:return: Données de tracking trouvées.
		"""
		# Parse settings
		max_distance = self.settings.tracking["Max Distance"].get_value()
		min_length = self.settings.tracking["Min Length"].get_value()
		decrease = self.settings.tracking["Decrease"].get_value()
		cost_birth = self.settings.tracking["Cost Birth"].get_value()
		# Run command
		return run_tracking_dll(self.dlls["Tracking"], self.localizations, max_distance, min_length, decrease, cost_birth)

	##################################################
	def __visualization(self, stack: np.ndarray) -> np.ndarray:
		"""
		Lance la creation d'une visualisation à partir des settings passés en paramètres.

		:param stack: Pile d'image d'entrée sous forme de tableau numpy.
		:return: Nouvelle visualisation.
		"""
		# Parse settings
		ratio = self.settings.visualization_hr["Ratio"].get_value()
		source = self.settings.visualization_hr["Source"].get_value()

		# Création de l'image finale
		depth, width, height = stack.shape
		new_width, new_height = int(width * ratio), int(height * ratio)
		res = np.zeros((new_width, new_height), dtype=float)
		if self.localizations is not None:
			# Integrated intensity
			col = "Integrated Intensity"
			# if source == 0: col = "Integrated Intensity"
			# elif source ==.....
			return hr_visualization(width, height, ratio, self.localizations[["X", "Y", col]].to_numpy())
		return np.asarray(res, dtype=np.uint16)
