import ctypes
import os
from datetime import datetime
from typing import cast

import numpy as np
import pandas as pd

from palm_tracer.Processing import run_palm_stack_dll
from palm_tracer.Settings import Settings
from palm_tracer.Settings.Groups import GaussianFit
from palm_tracer.Tools import Logger, print_warning, save_json


##################################################
def _palm_to_localisation_file(data: pd.DataFrame) -> pd.DataFrame:
	"""
	Convertis la sortie de la fonction de localisation vers le format usuel de PALMTracer

	:param data: Données venant de la fonction de localisation
	:return: Données formatées
	"""
	print("TODO PALM._palm_to_localisation_file")
	return data


##################################################
def _palm_to_tracking_file(data: pd.DataFrame) -> pd.DataFrame:
	"""
	Convertis la sortie de la fonction de tracking vers le format usuel de PALMTracer

	:param data: Données venant de la fonction de tracking
	:return: Données formatées
	"""
	print("TODO _palm_to_tracking_file")
	return data


##################################################
def process(dll: dict[str, ctypes.CDLL], settings: Settings):
	"""
	Lance le process de PALM selon les éléments passés en paramètres.

	:param dll: Liste des Bibliothèques DLL contenant les fonctions de traitement d'image.
	:param settings: Paramètres de l'interface pour lancer le traitement.
	"""
	# Parsing du batch
	paths = settings.batch.get_paths()
	stacks = settings.batch.get_stacks()
	if len(stacks) == 0:
		print_warning("Aucun fichier.")
		return

	for path, stack in zip(paths, stacks):
		# Logger
		os.makedirs(path, exist_ok=True)
		logger = Logger()
		timestamp_suffix = datetime.now().strftime("%Y%d%m_%H%M%S")
		logger.open(f"{path}/log-{timestamp_suffix}.log")
		logger.add("Commencer le traitement.")
		logger.add(f"Dossier de sortie : {path}")

		# Save settings
		print(settings)
		save_json(f"{path}/settings-{timestamp_suffix}.json", settings.to_dict())
		logger.add("Paramètres sauvegardés.")

		# Si transformation de la zone en entrée (par une ROI) à faire ici.

		# Save meta file (Création du DataFrame et sauvegarde en CSV)
		depth, height, width = stack.shape
		df = pd.DataFrame({"Height":                   [height], "Width": [width], "Plane Number": [depth],
						   "Pixel Size (nm)":          [settings.calibration["Pixel Size"].get_value()],
						   "Exposure Time (ms/frame)": [settings.calibration["Exposure"].get_value()],
						   "Intensity (photon/ADU)":   [settings.calibration["Intensity"].get_value()]})
		df.to_csv(f"{path}/meta-{timestamp_suffix}.csv", index=False)
		logger.add("Fichier Meta sauvegardé.")

		# Lancement de la localisation
		if settings.localisation.active:
			loc = process_localisation(dll["CPU"], stack, settings)
			loc = _palm_to_localisation_file(loc)
			logger.add(f"{loc.size} localisation(s) trouvé.")
			logger.add("Enregistrement du fichier de localisation")
			loc.to_csv(f"{path}/localisations-{timestamp_suffix}.csv", index=False)
		else:
			logger.add("Localisation désactivé.")
			# Chargement d'une localisation existante
			logger.add("Chargement d'une localisation pré-calculée.")
			# Sinon
			logger.add("Aucune donnée de localisation pré-calculée.")
			loc = None

		# Lancement du tracking
		if settings.tracking.active:
			track = process_tracking(dll["Tracking"], loc, settings)
			track = _palm_to_tracking_file(track)
			if not track.empty: logger.add("Enregistrement du fichier de tracking.")
			else: logger.add("Aucun tracking trouvé.")
		else:
			logger.add("Tracking désactivé.")
			# Chargement d'un tracking existant
			logger.add("Chargement d'un tracking pré-calculé.")
			# Sinon
			logger.add("Aucune donnée de tracking pré-calculé.")
			track = None

		# Lancement de la visualization
		if settings.visualization.active:
			visu = process_visualization(dll["CPU"], stack, settings, loc, track)
			logger.add("Enregistrement du fichier de visualisation.")
		# if not visu: logger.add("Enregistrement du fichier de visualisation.")
		# else: logger.add("Aucune visualisation enregistrée.")
		else:
			logger.add("Visualisation désactivée.")

		# Fermeture du Log
		logger.add("Traitement terminé.")
		logger.close()


##################################################
def process_localisation(dll: ctypes.CDLL, stack: np.ndarray, settings: Settings) -> pd.DataFrame:
	"""
	Lance la localisation à partir des settings passés en paramètres.

	:param dll: Bibliothèque DLL contenant les fonctions de traitement d'image.
	:param stack: Pile d'image d'entrée sous forme de tableau numpy.
	:param settings: Paramètres de l'interface pour lancer la localisation.
	:return: Données de localisation trouvées.
	"""
	# Parse settings
	threshold = settings.localisation["Threshold"].get_value()
	watershed = settings.localisation["Watershed"].get_value()
	roi = settings.localisation["ROI Size"].get_value()
	gaussian_setting = cast(GaussianFit, settings.localisation["Gaussian Fit"])
	gaussian = gaussian_setting["Mode"].get_value()
	sigma = gaussian_setting["Sigma"].get_value()
	theta = gaussian_setting["Theta"].get_value()
	# Run command
	return run_palm_stack_dll(dll, stack, threshold, watershed, gaussian, sigma, theta, roi)


##################################################
def process_tracking(dll: ctypes.CDLL, localisations: pd.DataFrame, settings: Settings) -> pd.DataFrame:
	"""
	Lance le tracking à partir des settings passés en paramètres.

	:param dll: Bibliothèque DLL contenant les fonctions de traitement d'image.
	:param localisations: Données venant de la fonction de localisation
	:param settings: Paramètres de l'interface pour lancer la localisation.
	:return: Données de tracking trouvées.
	"""
	print("TODO PALM.tracking")
	# Parse settings
	# Run command
	return pd.DataFrame()


##################################################
def process_visualization(dll: ctypes.CDLL, stack: np.ndarray, settings: Settings,
						  localisations: pd.DataFrame = None, tracking: pd.DataFrame = None) -> np.ndarray:
	"""
	Lance la creation d'une visualisation à partir des settings passés en paramètres.

	:param dll: Bibliothèque DLL contenant les fonctions de traitement d'image.
	:param stack: Pile d'image d'entrée sous forme de tableau numpy.
	:param settings: Paramètres de l'interface pour lancer la localisation.
	:param localisations: Données venant de la fonction de localisation.
	:param tracking: Données venant de la fonction de tracking.
	:return: Nouvelle visualisation.
	"""
	print("TODO PALM.visualization")
	# Parse settings
	# Run command
	return stack
