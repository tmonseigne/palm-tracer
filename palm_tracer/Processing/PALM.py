"""
Module contenant les fonctions de traitement de PALM.
"""

import ctypes
import os
from datetime import datetime
from typing import cast

import numpy as np
import pandas as pd

from palm_tracer.Processing import run_palm_stack_dll, run_tracking_dll
from palm_tracer.Settings import Settings
from palm_tracer.Settings.Groups import GaussianFit
from palm_tracer.Tools import get_last_file, Logger, print_warning, save_json
from palm_tracer.Tools.FileIO import save_png

# ==================================================
# region Process
# ==================================================
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
			logger.add("Localisation commencée.")
			loc = process_localisation(dll["CPU"], stack, settings)
			logger.add("\tEnregistrement du fichier de localisation")
			logger.add(f"\t\t{len(loc)} localisation(s) trouvée(s).")
			loc.to_csv(f"{path}/localisations-{timestamp_suffix}.csv", index=False)
		else:
			logger.add("Localisation désactivé.")
			f = get_last_file(path, "localisations")
			if f.endswith("csv"):  # Chargement d'une localisation existante
				logger.add("\tChargement d'une localisation pré-calculée.")
				try:
					loc = pd.read_csv(f)  # Lecture du fichier CSV avec pandas
					logger.add(f"\tFichier '{f}' chargé avec succès.")
					logger.add(f"\t\t{len(loc)} localisation(s) trouvée(s).")
				except Exception as e:
					loc = None
					logger.add(f"\tErreur lors du chargement du fichier '{f}' : {e}")
			else:  # Sinon
				loc = None
				logger.add("\tAucune donnée de localisation pré-calculée.")

		# Lancement du tracking
		if settings.tracking.active:
			logger.add("Tracking commencé.")
			track = process_tracking(dll["Tracking"], loc, settings)
			logger.add("\tEnregistrement du fichier de tracking.")
			logger.add(f"\t\t{len(track)} tracking(s) trouvé(s).")
			track.to_csv(f"{path}/tracking-{timestamp_suffix}.csv", index=False)
		else:
			logger.add("Tracking désactivé.")
			f = get_last_file(path, "tracking")
			if f.endswith("csv"):  # Chargement d'une localisation existante
				logger.add("\tChargement d'un tracking pré-calculée.")
				try:
					track = pd.read_csv(f)  # Lecture du fichier CSV avec pandas
					logger.add(f"\tFichier '{f}' chargé avec succès.")
					logger.add(f"\t\t{len(loc)} tracking(s) trouvée(s).")
				except Exception as e:
					track = None
					logger.add(f"\tErreur lors du chargement du fichier '{f}' : {e}")
			else:  # Sinon
				track = None
				logger.add("\tAucune donnée de tracking pré-calculée.")

		# Lancement de la visualization
		if settings.visualization.active:
			logger.add("Visualisation commencé.")
			visu = process_visualization(stack, settings, loc, track)
			logger.add("\tEnregistrement du fichier de visualisation.")
			save_png(visu, f"{path}/visualization-{timestamp_suffix}.png")
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
	# Parse settings
	max_distance = settings.tracking["Max Distance"].get_value()
	min_length = settings.tracking["Min Length"].get_value()
	decrease = settings.tracking["Decrease"].get_value()
	cost_birth = settings.tracking["Cost Birth"].get_value()
	# Run command
	return run_tracking_dll(dll, localisations, max_distance, min_length, decrease, cost_birth)


##################################################
def process_visualization(stack: np.ndarray, settings: Settings,
						  localisations: pd.DataFrame = None, tracking: pd.DataFrame = None) -> np.ndarray:
	"""
	Lance la creation d'une visualisation à partir des settings passés en paramètres.

	:param stack: Pile d'image d'entrée sous forme de tableau numpy.
	:param settings: Paramètres de l'interface pour lancer la localisation.
	:param localisations: Données venant de la fonction de localisation.
	:param tracking: Données venant de la fonction de tracking.
	:return: Nouvelle visualisation.
	"""
	# Parse settings
	ratio = settings.visualization["Ratio"].get_value()
	source = settings.visualization["Source"].get_value()

	# Création de l'image finale
	depth, width, height = stack.shape
	new_width, new_height = int(width * ratio), int(height * ratio)
	res = np.zeros((new_width, new_height), dtype=float)

	# Remplissage de l'image
	if source == 0: # Integrated intensity
		for index, row in localisations.iterrows():
			x, y = int(row["X"] * ratio), int(row["Y"] * ratio)
			res[x, y] += row["Integrated Intensity"]

	return np.asarray(res, dtype=np.uint16)  # Forcer le type de l'image en np.uint16

# ==================================================
# endregion Process
# ==================================================
