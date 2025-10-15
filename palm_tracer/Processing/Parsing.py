""" Fichier contenant des fonctions pour parser les entrées et sorties des DLLs externes. """
from typing import Any

import numpy as np
import pandas as pd

# Segmentation (Localization)
PARSING_COLUMNS: dict[str, dict[str, Any]] = {
		"Localization": {
				"columns": ["Id", "Plane", "Index", "Channel", "X", "Y", "Z", "Integrated Intensity",
							"Sigma X", "Sigma Y", "Theta", "MSE XY", "MSE Z",
							"Intensity 0", "Intensity Offset", "Intensity", "Surface", "Circularity"],
				"types":   {"Id": "int32", "Plane": "int32", "Index": "int32", "Surface": "int32", "Channel": "int32"}
				},
		"Tracking":     {
				"columns": ["Track", "Plane", "Id", "X", "Y", "Z", "Integrated Intensity", "Surface"],
				"types":   {"Track": "int32", "Plane": "int32", "Id": "int32", "Surface": "int32"}
				},
		}

COLS_FOR_TRACKING = ["Id", "X", "Y", "Z", "Intensity", "Surface"]

# Tracking
N_TRACK = 8  # Nombre de paramètres pour le tracking.


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
	return int(height * width * density * n_planes) * len(PARSING_COLUMNS["Localization"]["columns"])


##################################################
def rearrange_dataframe_columns(data: pd.DataFrame, columns: list[str], remaining: bool = True) -> pd.DataFrame:
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
def log10_dataframe(data: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
	"""
	Applique un log en base 10 sur certaines colonnes du dataframe (remplace par Nan les valeurs inférieures ou égale à 0).
	:param data: dataframe à modifier
	:param columns:
	:return:
	"""
	# Remplace log(x<=0) par NaN pour éviter les -inf/erreurs
	pos = data[columns] > 0
	logged = np.where(pos, np.log10(data[columns]), np.nan)
	data[columns] = pd.DataFrame(logged, index=data.index, columns=columns)
	return data


##################################################
def parse_result(data: np.ndarray, file_type: str = "Localization") -> pd.DataFrame:
	"""
	Parsing du résultat de la DLL PALM.

	On a un tableau 1D de grande taille en entrée :
		- On le découpe en tableau 2D à 13 colonnes (`N_SEGMENTS`).	La taille du tableau est vérifié et tronqué si nécessaire.
		- On le transforme en dataframe avec les colonnes définies par `SEGMENTS`.
		- On supprime les lignes remplies de 0 et de -1. Un test sur les colonnes X ou Y strictement positif suffit (le SigmaX et SigmaY peuvent être à 0).

	:param data: Donnée en entrée récupérées depuis la DLL PALM.
	:param file_type: Type de fichier à parser ("Localization" ou "Tracking")
	:return: Dataframe filtré
	"""
	# Récupération des éléments
	columns = PARSING_COLUMNS[file_type]["columns"]
	n_columns = len(columns)
	types = PARSING_COLUMNS[file_type]["types"]

	# Manipulation du tableau 1D.
	size = (data.size // n_columns) * n_columns	  # Récupération de la taille correcte si non multiple de N_SEGMENT
	data = data[:size].reshape(-1, n_columns)	  # Passage en tableau 2D
	data = data[data[:, columns.index("X")] > 0]  # Filtrage en amont
	# data = data.astype(np.float32)			  # Conversion en float pour alléger la mémoire (à ce stade la précision est suffisante)
	res = pd.DataFrame(data, columns=columns)	  # Transformation en Dataframe
	res = res.astype(types)
	return res


##################################################
def parse_irregular_array(data: np.ndarray) -> pd.DataFrame:
	"""
	Parsing du résultat de la DLL PALM.

	Entrée : un tableau 1D où chaque bloc est encodé comme : [L, x0, x1, ..., x{L-1}, L2, y0, y1, ..., ...]
	Le parsing s'arrête dès qu'un L <= 0 est rencontré.

	Règles :
	- Le premier élément d'un bloc (L) donne le nombre d'éléments qui suivent pour ce bloc.
	- Les longueurs négatives ou nulle (L <= 0) signalent la fin du flux.
	- Les blocs tronqués (pas assez d'éléments après L) lèvent une ValueError.
	- Les valeurs des blocs (sans L) sont retournées dans le DataFrame.
	- Les lignes n'ayant pas le même nombre de colonnes sont complétées par NaN.

	:param data: Données 1D récupérées depuis la DLL PALM. Doit être indexable et de dimension 1.
	:return: DataFrame où chaque ligne correspond à un bloc et les colonnes (Val_0, Val_1, ...) contiennent les valeurs du bloc, complétées par NaN si
	nécessaire.
	:raise ValueError: entrée invalide (nombre de dimensions ou taille finale)

	Exceptions
	----------
	ValueError
	    - Si `data` n'est pas 1D.
	    - Si un bloc est tronqué (L annonce plus d'éléments que disponibles).
	"""
	if data.ndim != 1:
		raise ValueError("`data` doit être un tableau 1D.")

	rows: list[np.ndarray] = []
	i = 0
	N = data.size

	while i < N:
		# Lecture de L (la longueur annoncée du bloc)
		L_raw = data[i]
		try:
			L = int(L_raw)
		except (TypeError, ValueError):
			raise ValueError(f"Longueur de bloc non entière à l'indice {i}: {L_raw!r}") from None

		if L <= 0: break  # fin du flux

		i += 1  # on avance sur le premier élément du bloc
		if i + L > N: raise ValueError(f"Bloc tronqué: longueur {L} annoncée à l'indice {i - 1}, mais seulement {N - i} élément(s) disponible(s).")
		# Extraction du bloc (les L valeurs, sans L lui-même)
		rows.append(np.asarray(data[i:i + L]))
		i += L  # passer au bloc suivant

	# Construction du DataFrame avec padding NaN
	if not rows: return pd.DataFrame()  # aucun bloc valide avant un L<=0 ou tableau vide

	max_len = max(len(r) for r in rows)
	out = np.full((len(rows), max_len), np.nan, dtype=float)
	for r_idx, r in enumerate(rows):
		if r.size:
			out[r_idx, :r.size] = r

	columns = [f"Val_{k}" for k in range(max_len)]
	df = pd.DataFrame(out, columns=columns)
	return df


##################################################
def parse_localization_to_tracking(data: pd.DataFrame) -> np.ndarray:
	"""
	Parsing du résultat de la localisation pour la DLL de Tracking.

	:param data: Donnée en entrée récupérées depuis la localisation.
	:return: Dataframe
	"""
	# Ajoute une ligne de -1 à chaque changement de Plan dans la localisation
	res = []
	previous_plan = None
	blank = [-1 for _ in COLS_FOR_TRACKING]
	for _, row in data.iterrows():
		if previous_plan is not None and row["Plane"] != previous_plan:
			res += blank
		res += row[COLS_FOR_TRACKING].to_list()
		previous_plan = row["Plane"]

	res += blank  # Ajout d'une dernière ligne -1 à la fin
	return np.asarray(res, dtype=np.float64)
