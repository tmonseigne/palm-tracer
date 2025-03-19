""" Fichier contenant des fonctions pour parser les entrées et sorties des DLLs externes. """

import numpy as np
import pandas as pd

# Segmentation (Localization)
N_SEGMENT = 13  # Nombre de paramètres pour la segmentation.
SEGMENT_COLS = ["Sigma X", "Sigma Y", "Theta", "Y", "X",  # X est Y sont inversés à la sortie de la DLL donc Y,X au lieu de X, Y
				"Intensity 0",  # Intensity too ??? (I0 sometimes) Maybe different of Intensity. Have I if the offset is applied ?
				"Intensity Offset",  # Intensity Offset ???
				"MSE Gaussian",  # MSE Gaussian
				"Intensity",  # Intensity (Integrated Wavelet Intensity)
				"Surface", "Z", "Pair Distance", "Id"]

SEGMENT_FILE_COLS = ["Id", "Plane", "Index", "Channel", "X", "Y", "Z", "Integrated Intensity",
					 "Sigma X", "Sigma Y", "Theta", "MSE Gaussian", "MSE Z", "Pair Distance"]

# Tracking
N_TRACK = 9  # Nombre de paramètres pour le tracking.
TRACK_COLS = ["Track", "Plane", "Y", "X", "Surface", "Integrated Intensity", "Z", "Color", "Id"]
TRACK_FILE_COLS = ["Track", "Plane", "Id", "X", "Y", "Z", "Integrated Intensity"]


##################################################
def rearrange_dataframe_columns(data: pd.DataFrame, columns: list["str"], remaining: bool = True) -> pd.DataFrame:
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
		columns = columns + remaining_columns  # Ajout des colonnes restantes aux colonnes de départ
	return data[columns]  # Réorganisation du DataFrame


##################################################
def parse_palm_result(data: np.ndarray, plane: int, gauss_fit: int, sort: bool = False) -> pd.DataFrame:
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
	size = (data.size // N_SEGMENT) * N_SEGMENT  # Récupération de la taille correcte si non multiple de N_SEGMENT
	res = pd.DataFrame(data[:size].reshape(-1, N_SEGMENT), columns=SEGMENT_COLS)  # Transformation en Dataframe
	res = res[res["X"] > 0]  # Filtrage des lignes remplies de 0 et -1

	if sort: res = res.sort_values(by=["Y", "X"], ascending=[True, True])  # Tri (un tri uniquement sur Y est possible, car peu de chance de doublons)
	res = res.reset_index(drop=True)  # Remise à 0 des index
	res["Id"] = range(1, len(res) + 1)  # Mise à jour de l'ID dans le tableau.
	res["Index"] = range(1, len(res) + 1)  # Ajout de l'index (au sein du plan) dans le tableau.
	res["Plane"] = plane  # Ajout d'un plan dans le tableau
	res["Channel"] = -1  # Ajout d'un channel dans le tableau
	res["MSE Z"] = -1  # Ajout d'un MSE pour Z dans le tableau

	# Ajout de l'intensité intégré (si on à les sigma du gaussian fit ou non)
	if gauss_fit != 0: res["Integrated Intensity"] = 2 * np.pi * res["Intensity 0"] * res["Sigma X"] * res["Sigma Y"]
	else: res["Integrated Intensity"] = res["Intensity"]

	# Ajout de la circularité, on complique un peu pour éviter les cas ou Sigma X et Y valent 0
	# Normalement uniquement lorsque  gauss_fit == 0 comme précédemment mais en prévision du futur (autres méthodes), on sécurise le process
	# L'utilisation de Numpy permet de passer les divisions par 0 (résultat Nan)
	circularity = np.minimum(res["Sigma X"], res["Sigma Y"]) / np.maximum(res["Sigma X"], res["Sigma Y"])
	res["Circularity"] = circularity.fillna(1)  # Remplacement des Nan par 1.

	return rearrange_dataframe_columns(res, SEGMENT_FILE_COLS, True)  # Réorganisation du DataFrame


##################################################
def parse_tracking_result(data: np.ndarray) -> pd.DataFrame:
	"""
	Parsing du résultat de la DLL Tracking.

	:param data: Donnée en entrée récupérées depuis la DLL Tracking.
	:return: Dataframe
	"""
	size = (data.size // N_TRACK) * N_TRACK  # Récupération de la taille correcte si non multiple de N_TRACK
	res = pd.DataFrame(data[:size].reshape(-1, N_TRACK), columns=TRACK_COLS)  # Transformation en Dataframe
	res = res[res["X"] > 0]  # Filtrage des lignes remplies de 0 et -1
	res = res.reset_index(drop=True)  # Remise à 0 des index

	# Liste des colonnes à placer en premier
	return rearrange_dataframe_columns(res, TRACK_FILE_COLS, True)  # Réorganisation du DataFrame


##################################################
def parse_localization_to_tracking(data: pd.DataFrame) -> np.ndarray:
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
	res = rearrange_dataframe_columns(res, SEGMENT_COLS, False)
	return np.asarray(res.to_numpy().flatten(), dtype=np.float64)
