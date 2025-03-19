"""
Fichier contenant des fonctions pour charger des DLLs externes,
exécuter des traitements d'image via ces DLLs et gérer des paramètres liés aux algorithmes de détection de points.

Ce module regroupe des utilitaires pour :

- Chargement de DLLs : chargement des bibliothèques nécessaires au traitement d'image.
- Traitement d'images : exécution de traitements via DLLs pour détecter des points sur une image.
- Calcul et parsing de paramètres   estimation du nombre de points détectables en fonction des dimensions de l'image et de la densité.

.. todo::
	Doit ont garder les identifiants et les plans qui vont de 1 à N au lieu du classique 0 à N-1 ?
"""

import ctypes
# from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

from palm_tracer.Tools import print_warning

# Segmentation (Localization)
N_SEGMENT = 13						 # Nombre de paramètres pour la segmentation.
SEGMENT_COLS = ["Sigma X", "Sigma Y", "Theta", "Y", "X", # X est Y sont inversés à la sortie de la DLL donc Y,X au lieu de X, Y
				"Intensity 0",		 # Intensity too ??? (I0 sometimes) Maybe different of Intensity. Have I if the offset is applied ?
				"Intensity Offset",  # Intensity Offset ???
				"MSE Gaussian",		 # MSE Gaussian
				"Intensity",		 # Intensity (Integrated Wavelet Intensity)
				"Surface", "Z", "Pair Distance", "Id"]

SEGMENT_FILE_COLS = ["Id", "Plane", "Index", "Channel", "X", "Y", "Z", "Integrated Intensity",
					 "Sigma X", "Sigma Y", "Theta", "MSE Gaussian", "MSE Z", "Pair Distance"]

# Tracking
N_TRACK = 9  # Nombre de paramètres pour le tracking.
TRACK_COLS = ["Track", "Plane", "Y", "X", "Surface", "Integrated Intensity", "Z", "Color", "Id"]
TRACK_FILE_COLS = ["Track", "Plane", "Id", "X", "Y", "Z", "Integrated Intensity"]


# ==================================================
# region Parsing
# ==================================================
##################################################
def _get_max_points(height: int = 256, width: int = 256, density: float = 0.2, n_planes: int = 1) -> int:
	"""
	Calcule le nombre maximal théorique de points détectables basé sur les dimensions et la densité de l'image.

	:param height: Hauteur de l'image (nombre de lignes). Par défaut 256.
	:param width: Largeur de l'image (nombre de colonnes). Par défaut 256.
	:param density: Densité de points par pixel. Par défaut 0.2.
	:param n_planes: Nombre de plans de l'image. Par défaut 1.

	:return: Nombre maximal théorique de points détectables.
	"""
	return int(height * width * density * n_planes) * N_SEGMENT


##################################################
def _rearrange_dataframe_columns(data: pd.DataFrame, columns: list["str"], remaining: bool = True) -> pd.DataFrame:
	"""
	Réorganise les colonnes d'un DataFrame en mettant certaines en premier, avec l'option d'ajouter les colonnes restantes dans leur ordre d'origine.

	:param data: Le DataFrame à réorganiser.
	:param columns: Liste des noms de colonnes à placer en premier.
	:param remaining: Si `True`, ajoute les colonnes non spécifiées après celles définies dans `columns`.
	:return: Un nouveau DataFrame avec les colonnes réorganisées.

    :raises ValueError: Si une colonne spécifiée dans `columns` n'existe pas dans `data`.
	"""
	# Vérifier que toutes les colonnes spécifiées existent dans le DataFrame
	missing_columns = [col for col in columns if col not in data.columns]
	if missing_columns:
		raise ValueError(f"Les colonnes suivantes sont absentes du DataFrame : {missing_columns}")

	if remaining:
		remaining_columns = [col for col in data.columns if col not in columns]  # Colonnes restantes (toutes sauf celles déjà définies)
		columns = columns + remaining_columns									 # Ajout des colonnes restantes aux colonnes de départ
	return data[columns]														 # Réorganisation du DataFrame


##################################################
def _parse_palm_result(data: np.ndarray, plane: int, gauss_fit: int, sort: bool = False) -> pd.DataFrame:
	"""
	Parsing du résultat de la DLL PALM.

	On a un tableau 1D de grande taille en entrée :
		- On le découpe en tableau 2D à 13 colonnes (`N_SEGMENTS`).	La taille du tableau est vérifié et tronqué si nécessaire.
		- On le transforme en dataframe avec les colonnes définies par `SEGMENTS`.
		- On supprime les lignes remplies de 0 et de -1. Un test sur les colonnes X ou Y strictement positif suffit (le SigmaX et SigmaY peuvent être à 0).

	:param data: Donnée en entrée récupérées depuis la DLL PALM.
	:param plane: Numéro du plan dans la pile
	:param gauss_fit: Mode d'ajustement Gaussien.
	:param sort: Tri des points par Y puis X (sens de lecture Gauche à droite du haut vers le bas).
	:return: Dataframe filtré
	"""
	# Manipulation du tableau 1D.
	size = (data.size // N_SEGMENT) * N_SEGMENT									  # Récupération de la taille correcte si non multiple de N_SEGMENT
	res = pd.DataFrame(data[:size].reshape(-1, N_SEGMENT), columns=SEGMENT_COLS)  # Transformation en Dataframe
	res = res[res["X"] > 0]														  # Filtrage des lignes remplies de 0 et -1

	if sort: res = res.sort_values(by=["Y", "X"], ascending=[True, True])		  # Tri (un tri uniquement sur Y est possible, car peu de chance de doublons)
	res = res.reset_index(drop=True)	 								 		  # Remise à 0 des index
	res["Id"] = range(1, len(res) + 1)	 								 		  # Mise à jour de l'ID dans le tableau.
	res["Index"] = range(1, len(res) + 1)								 		  # Ajout de l'index (au sein du plan) dans le tableau.
	res["Plane"] = plane					 								 	  # Ajout d'un plan dans le tableau
	res["Channel"] = -1					 								 		  # Ajout d'un channel dans le tableau
	res["MSE Z"] = -1					 								 		  # Ajout d'un MSE pour Z dans le tableau

	# Ajout de l'intensité intégré (si on à les sigma du gaussian fit ou non)
	if gauss_fit != 0: res["Integrated Intensity"] = 2 * np.pi * res["Intensity 0"] * res["Sigma X"] * res["Sigma Y"]
	else: res["Integrated Intensity"] = res["Intensity"]

	# Ajout de la circularité, on complique un peu pour éviter les cas ou Sigma X et Y valent 0
	# Normalement uniquement lorsque  gauss_fit == 0 comme précédemment mais en prévision du futur (autres méthodes), on sécurise le process
	# L'utilisation de Numpy permet de passer les divisions par 0 (résultat Nan)
	circularity = np.minimum(res["Sigma X"], res["Sigma Y"]) / np.maximum(res["Sigma X"], res["Sigma Y"])
	res["Circularity"] = circularity.fillna(1)  # Remplacement des Nan par 1.

	return _rearrange_dataframe_columns(res, SEGMENT_FILE_COLS, True)  # Réorganisation du DataFrame


##################################################
def _parse_tracking_result(data: np.ndarray) -> pd.DataFrame:
	"""
	Parsing du résultat de la DLL Tracking.

	:param data: Donnée en entrée récupérées depuis la DLL Tracking.
	:return: Dataframe
	"""
	size = (data.size // N_TRACK) * N_TRACK									  # Récupération de la taille correcte si non multiple de N_TRACK
	res = pd.DataFrame(data[:size].reshape(-1, N_TRACK), columns=TRACK_COLS)  # Transformation en Dataframe
	res = res[res["X"] > 0]													  # Filtrage des lignes remplies de 0 et -1
	res = res.reset_index(drop=True)	 								 	  # Remise à 0 des index

	# Liste des colonnes à placer en premier
	return _rearrange_dataframe_columns(res, TRACK_FILE_COLS, True)			  # Réorganisation du DataFrame

##################################################
def _parse_localization_for_tracking_dll(data: pd.DataFrame) -> np.ndarray:
	"""
	Parsing du résultat de la localisation pour la DLL de Tracking.

	:param data: Donnée en entrée récupérées depuis la localisation.
	:return: Dataframe
	"""
	# Ajoute une ligne de -1 à chaque changement de Plan dans la localisation
	# Création d'un nouveau DataFrame avec les séparateurs -1 insérés
	rows = []
	previous_plan = None
	columns = data.columns  # Récupérer toutes les colonnes

	for _, row in data.iterrows():
		if previous_plan is not None and row["Plane"] != previous_plan:
			rows.append({col: -1 for col in columns})  # Ajout de la ligne -1
		rows.append(row.to_dict())  # Ajout de la ligne actuelle
		previous_plan = row["Plane"]

	# Ajout d'une dernière ligne -1 à la fin
	rows.append({col: -1 for col in columns})

	# Conversion en DataFrame final
	res = pd.DataFrame(rows)
	res = _rearrange_dataframe_columns(res, SEGMENT_COLS, False)
	return np.asarray(res.to_numpy().flatten(), dtype=np.float64)


# ==================================================
# endregion Parsing
# ==================================================

# ==================================================
# region DLL Manipulation
# ==================================================
##################################################
def load_dll() -> dict[str, ctypes.CDLL]:
	"""Récupère les DLLs si elles existent."""
	res = dict[str, ctypes.CDLL]()
	dll_path = Path(__file__).parent.parent / "DLL"

	# GPU et Live n'arrivent pas à se charger (sans doute une dépendance cachée autre).
	for name in ["CPU", "GPU", "Live", "Tracking"]:
		dll_filename = dll_path / f"{name}_PALM.dll"
		try:
			res[name] = ctypes.cdll.LoadLibrary(str(dll_filename.resolve()))
			print(f"DLL '{dll_filename}' chargée.")
		except OSError as e:
			print_warning(f"Impossible de charger la DLL '{dll_filename}':\n\t{e}")
	return res


##################################################
def run_palm_image_dll(dll: ctypes.CDLL, image: np.ndarray, threshold: float, watershed: bool,
					   gauss_fit: int, sigma: float, theta: float, roi_size: int, plane: int = 1) -> pd.DataFrame:
	"""
	Exécute un traitement d'image avec une DLL PALM externe pour détecter des points dans une image.

	:param dll: Bibliothèque DLL contenant les fonctions de traitement d'image.
	:param image: Image d'entrée 2D sous forme de tableau numpy d'entier.
	:param threshold: Seuil pour la détection.
	:param watershed: Active ou désactive le mode watershed.
	:param gauss_fit: Mode d'ajustement Gaussien.
	:param sigma: Valeur initiale du sigma pour l'ajustement Gaussien.
	:param theta: Valeur initiale du theta pour l'ajustement Gaussien.
	:param roi_size: Taille de la région d'intérêt (ROI).
	:param plane: Numéro du plan dans la pile
	:return: Liste des points détectés sous forme de dataframe contenant toutes les informations reçu de la DLL.
	"""
	# En multithreading, la dll doit être chargé pour chaque process
	# dll = ctypes.cdll.LoadLibrary(....)
	# Parsing
	image = np.asarray(image, dtype=np.uint16)  # Forcer le type de l'image en np.uint16
	height, width = image.shape					# Récupération des dimensions
	n = _get_max_points(height, width)			# Récupération d'un nombre de points maximum théorique
	image = image.flatten()						# L'image est "applati"

	c_image = image.ctypes.data_as(ctypes.POINTER(ctypes.c_ushort))			   # Image
	c_height = ctypes.c_ulong(height)										   # Hauteur (nombre de lignes)
	c_width = ctypes.c_ulong(width)											   # Largeur (nombre de colonnes)
	n_points = ctypes.c_ulong(n)											   # Nombre maximum de points théorique
	c_points = np.zeros((n,), dtype=np.float64).ctypes.data_as(ctypes.POINTER(ctypes.c_double))  # Liste de points
	c_wavelet = ctypes.c_ulong(1)											   # Wavelet toujours à 1.
	c_threshold = ctypes.c_double(threshold)								   # Seuil
	c_watershed = ctypes.c_double(0 if watershed else 10)					   # Activation du Watershed
	c_vol_min = ctypes.c_double(4)											   # Vol minimum toujours à 4.
	c_int_min = ctypes.c_double(0)											   # Int minimum toujours à 0.
	c_gauss_fit = ctypes.c_ushort(gauss_fit)								   # Mode du Gaussian Fit
	c_sigma_x = ctypes.c_double(sigma)										   # Valeur initiale du Sigma X
	c_sigma_y = ctypes.c_double(sigma * 2)									   # Valeur initiale du Sigma Y (*2 pour correspondre à métamorph, interet limité)
	c_theta = ctypes.c_double(theta)										   # Valeur Initiale du Theta
	c_roi_size = ctypes.c_ushort(roi_size)									   # taille de la ROI

	# Running
	dll._OpenPALMProcessing(c_image, c_points, n_points, c_height, c_width, c_wavelet, c_threshold, c_watershed,
							c_vol_min, c_int_min, c_gauss_fit, c_sigma_x, c_sigma_y, c_theta, c_roi_size)
	dll._PALMProcessing()
	dll._closePALMProcessing()

	return _parse_palm_result(np.ctypeslib.as_array(c_points, shape=(n,)), plane, gauss_fit, True)


##################################################
def run_palm_stack_dll(dll: ctypes.CDLL, stack: np.ndarray, threshold: float, watershed: bool,
					   gauss_fit: int, sigma: float, theta: float, roi_size: int, planes: Optional[list[int]] = None) -> pd.DataFrame:
	"""
	Exécute un traitement d'image avec une DLL PALM externe pour détecter des points dans une image.

	:param dll: Bibliothèque DLL contenant les fonctions de traitement d'image.
	:param stack: Pile d'image d'entrée sous forme de tableau numpy.
	:param threshold: Seuil pour la détection.
	:param watershed: Active ou désactive le mode watershed.
	:param gauss_fit: Mode d'ajustement Gaussien (défini par `get_gaussian_mode`).
	:param sigma: Valeur initiale du sigma pour l'ajustement Gaussien.
	:param theta: Valeur initiale du theta pour l'ajustement Gaussien.
	:param roi_size: Taille de la région d'intérêt (ROI).
    :param planes: Liste des plans à analyser (None = tous les plans).
    :return: Liste des points détectés sous forme de dataframe contenant toutes les informations reçu de la DLL.
	"""
	n_planes = stack.shape[0]
	if planes is None : planes =  list(range(n_planes))
	else: planes = [p for p in planes if isinstance(p, int) and 0 <= p < n_planes]

	# # Exécution parallèle impossible tant que la DLL ne fonctionne pas en une fonction unique et utilise un objet palm en pointeur
	# results = []
	# with ProcessPoolExecutor() as executor:
	# 	futures = {executor.submit(run_palm_image_dll, dll, stack[i], threshold, watershed, gauss_fit, sigma, theta, roi_size, i + 1): i for i in planes}
	# 	for future in as_completed(futures): results.append(future.result())

	results = []
	for i in planes:
		points = run_palm_image_dll(dll, stack[i], threshold, watershed, gauss_fit, sigma, theta, roi_size, i + 1)
		results.append(points)			# Ajouter à la liste

	# Créer le dataframe final peut-être plus rapide que le mettre à jour à chaque iteration (réallocation des milliers de fois)
	res = pd.concat(results, ignore_index=True)
	# res = res.sort_values(by=["Plane", "Index"]).reset_index(drop=True)	# Tri si jamais le multithread à mélangé les sorties
	res["Id"] = range(1, len(res) + 1)  # Mise à jour de l'ID dans le tableau
	return res


##################################################
def run_tracking_dll(dll: ctypes.CDLL, localizations: pd.DataFrame,
					 max_distance: float, min_life: float, decrease: float, cost_birth: float) -> pd.DataFrame:
	"""

	:param dll: Bibliothèque DLL contenant les fonctions de traitement d'image.
	:param localizations: Liste des points détectés sous forme de dataframe contenant toutes les informations reçu de la DLL.
	:param max_distance:
	:param min_life:
	:param decrease:
	:param cost_birth:
	:return:
	"""
	n = len(localizations)
	loc_size = n * N_SEGMENT
	track_size = n * N_TRACK
	points = _parse_localization_for_tracking_dll(localizations)

	c_points = points.ctypes.data_as(ctypes.POINTER(ctypes.c_double))				   # Liste de points
	c_loc_size = ctypes.c_ulong(loc_size)											   #
	c_track = np.zeros((track_size,), dtype=np.float64).ctypes.data_as(ctypes.POINTER(ctypes.c_double))  # Liste de points
	c_track_size = ctypes.c_ulong(track_size)										   #
	c_max_distance = ctypes.c_double(max_distance)									   #
	c_dz_dx = ctypes.c_double(1)													   # dZdX toujours à 1.
	c_min_life = ctypes.c_double(min_life)											   #
	c_decrease = ctypes.c_double(decrease)											   #
	c_fusion_disso = ctypes.c_ulong(0)												   # allowFusiondisso toujours à 0.
	c_cost_birth = ctypes.c_double(cost_birth)										   #
	c_dim = ctypes.c_ulong(2)														   # Nombre de dimensions toujours à 2 mais inutilisé dans la DLL.
	c_model = ctypes.c_ulong(2)														   # Model toujours à 2 pour DistanceIntensity (1 pour CloserNeighbors).
	c_planes = ctypes.c_ulong(localizations["Plane"].max())							   # Nombre de plans

	# Running
	dll.tracking(c_points, c_loc_size, c_track, c_track_size, c_max_distance, c_dz_dx,
				 c_min_life, c_decrease, c_fusion_disso, c_cost_birth, c_dim, c_model, c_planes)

	return _parse_tracking_result(np.ctypeslib.as_array(c_track, shape=(track_size,)))
# ==================================================
# endregion DLL Manipulation
# ==================================================
