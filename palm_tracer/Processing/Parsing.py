""" Fichier contenant des fonctions pour parser les entrées et sorties des DLLs externes. """

import numpy as np
import pandas as pd

# Segmentation (Localization)
N_SEGMENT = 16  # Nombre de paramètres pour la segmentation.
SEGMENT_COLS = ["Id", "Plane", "Index", "X", "Y", "Z", "Integrated Intensity", "Sigma X", "Sigma Y", "Theta",
				"Intensity 0", "Intensity Offset", "Intensity", "Surface", "MSE Gaussian", "Circularity"]

SEGMENT_COLS_FOR_TRACKING = ["Sigma X", "Sigma Y", "Theta", "Y", "X", "Intensity 0", "Intensity Offset",
							 "MSE Gaussian", "Intensity", "Surface", "Z", "Pair Distance", "Id"]

SEGMENT_FILE_COLS = ["Id", "Plane", "Index", "Channel", "X", "Y", "Z", "Integrated Intensity",
					 "Sigma X", "Sigma Y", "Theta", "MSE Gaussian", "MSE Z", "Pair Distance"]

# Tracking
N_TRACK = 9  # Nombre de paramètres pour le tracking.
TRACK_COLS = ["Track", "Plane", "Y", "X", "Surface", "Integrated Intensity", "Z", "Color", "Id"]
TRACK_FILE_COLS = ["Track", "Plane", "Id", "X", "Y", "Z", "Integrated Intensity"]


##################################################
def get_max_points(height: int = 256, width: int = 256, n_planes: int = 1, density: float = 0.2) -> int:
	"""
	Calcule le nombre maximal théorique de points détectables basé sur les dimensions et la densité de l'image.

	:param height: Hauteur de l'image (nombre de lignes). Par défaut 256.
	:param width: Largeur de l'image (nombre de colonnes). Par défaut 256.
	:param n_planes: Nombre de plans de l'image. Par défaut 1.
	:param density: Densité de points par pixel. Par défaut 0.2.

	:return: Nombre maximal théorique de points détectables.
	"""
	return int(height * width * density * n_planes) * N_SEGMENT


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
		columns = columns + remaining_columns									 # Ajout des colonnes restantes aux colonnes de départ

	if list(data.columns[:len(columns)]) == columns: return data				 # Optimisation : évite la copie si déjà bon ordre

	return data.loc[:, columns]													 # Réorganisation du DataFrame


##################################################
def parse_palm_result(data: np.ndarray, count: int) -> pd.DataFrame:
	"""
	Parsing du résultat de la DLL PALM.

	On a un tableau 1D de grande taille en entrée :
		- On le découpe en tableau 2D à 13 colonnes (`N_SEGMENTS`).	La taille du tableau est vérifié et tronqué si nécessaire.
		- On le transforme en dataframe avec les colonnes définies par `SEGMENTS`.
		- On supprime les lignes remplies de 0 et de -1. Un test sur les colonnes X ou Y strictement positif suffit (le SigmaX et SigmaY peuvent être à 0).

	:param data: Donnée en entrée récupérées depuis la DLL PALM.
	:return: Dataframe filtré
	"""
	# Manipulation du tableau 1D.
	size = (count // N_SEGMENT) * N_SEGMENT							  # Récupération de la taille correcte si non multiple de N_SEGMENT
	data = data[:size].reshape(-1, N_SEGMENT)						  # Passage en tableau 2D
	data = data[data[:, SEGMENT_COLS.index("X")] > 0]				  # Filtrage en amont
	data = data.astype(np.float32)									  # Conversion en float pour alléger la mémoire (à ce stade la précision est suffisante)
	res = pd.DataFrame(data, columns=SEGMENT_COLS)  				  # Transformation en Dataframe
	res["Channel"] = np.full(len(res), -1, dtype=np.int32)			  # Ajout d'un channel dans le tableau
	res["MSE Z"] = np.full(len(res), -1, dtype=np.float32)			  # Ajout d'un MSE pour Z dans le tableau
	res["Pair Distance"] = np.zeros(len(res), dtype=np.float32)		  # Ajout d'un Pair Distance dans le tableau
	res = res.astype({"Id": "int32", "Plane": "int32", "Index": "int32", "Surface": "int32", "Channel": "int32"})
	return rearrange_dataframe_columns(res, SEGMENT_FILE_COLS, True)  # Réorganisation du DataFrame


##################################################
def parse_tracking_result(data: np.ndarray) -> pd.DataFrame:
	"""
	Parsing du résultat de la DLL Tracking.

	:param data: Donnée en entrée récupérées depuis la DLL Tracking.
	:return: Dataframe
	"""
	size = (data.size // N_TRACK) * N_TRACK									  # Récupération de la taille correcte si non multiple de N_TRACK
	res = pd.DataFrame(data[:size].reshape(-1, N_TRACK), columns=TRACK_COLS)  # Transformation en Dataframe
	res = res[res["X"] > 0]													  # Filtrage des lignes remplies de 0 et -1
	res = res.reset_index(drop=True)										  # Remise à 0 des index
	return rearrange_dataframe_columns(res, TRACK_FILE_COLS, True)			  # Réorganisation du DataFrame


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
			rows.append({col: -1 for col in columns})  # Ajout de la ligne de -1
		rows.append(row.to_dict())					   # Ajout de la ligne actuelle
		previous_plan = row["Plane"]

	# Ajout d'une dernière ligne -1 à la fin
	rows.append({col: -1 for col in columns})

	# Conversion en DataFrame final
	res = pd.DataFrame(rows)
	res = rearrange_dataframe_columns(res, SEGMENT_COLS_FOR_TRACKING, False)
	return np.asarray(res.to_numpy().flatten(), dtype=np.float64)
