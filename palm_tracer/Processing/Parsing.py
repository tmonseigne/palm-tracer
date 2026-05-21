"""Fichier contenant des fonctions pour parser les entrées et sorties des DLLs externes."""
from __future__ import annotations

import numpy as np
import pandas as pd

# Titre des colonnes selon les fichiers et indications des colonnes entières
FILES_COLUMNS: dict[str, dict[str, list[str]]] = {
		"Meta":                 {
				"columns": ["Height", "Width", "Plane Number", "Pixel Size (μm)", "Exposure Time (s/frame)", "Intensity (photon/ADU)"],
				"types":   ["Height", "Width", "Plane Number"]
				},
		"Localization":         {
				"columns": ["Id", "Plane", "Index", "Channel", "X", "Y", "Z", "Integrated Intensity",
							"Sigma X", "Sigma Y", "Theta", "MSE XY", "MSE Z",
							"Intensity 0", "Intensity Offset", "Intensity", "Surface", "Circularity"],
				"types":   ["Id", "Plane", "Index", "Surface", "Channel"]
				},
		"Tracking":             {
				"columns": ["Track", "Plane", "Id", "X", "Y", "Z", "Integrated Intensity", "Surface"],
				"types":   ["Track", "Plane", "Id", "Surface"]
				},
		"Beads":                {
				"columns": ["Bead", "Plane", "Id", "X", "Y", "Z", "Integrated Intensity", "Sigma X", "Sigma Y", "Theta", "Surface"],
				"types":   ["Bead", "Plane", "Id", "Surface"]
				},
		"MSD":                  {
				"columns": ["Track", "Step"],
				"types":   ["Track"]
				},
		"Instant Diffusion":    {
				"columns": ["Track", "Window"],
				"types":   ["Track"]
				},
		"Fit":                  {
				"columns": ["Track", "Length", "Total Intensity", "D(0) (μm²/s)", "MSD(0) (μm²)", "MSE(0)"],
				"types":   ["Track", "Length"]
				},
		"Fit_1":                {
				"columns": ["A (μm²/s)", "B (μm²)", "MSE"],
				"types":   []
				},
		"Fit_2":                {
				"columns": ["Alpha", "B (μm²)", "MSE", "Average Speed (Last-First)(μm/s)"],
				"types":   []
				},
		"Fit_3":                {
				"columns": ["A (μm²)", "B (s)", "C (μm²)", "MSE", "Confinement Radius (μm)"],
				"types":   []
				},
		"Astigmatism 3D Model": {
				"columns": ["Z0", "W", "C3", "C4", "A"],
				"types":   []
				},
		}

COLS_FOR_TRACKING = ["Id", "X", "Y", "Z", "Intensity", "Surface"]
MODEL_ROWS = ["X", "Y"]

# Dimensions utiles fréquement
N_COL_META = len(FILES_COLUMNS["Meta"]["columns"])  # .									  Nombre de paramètres pour les métadonnées (6).
N_COL_TRC = len(FILES_COLUMNS["Tracking"]["columns"])  # .								  Nombre de paramètres pour le tracking (8).
N_COL_LOC = len(FILES_COLUMNS["Localization"]["columns"])  # .							  Nombre de paramètres pour le tracking (18).
SHAPE_MODEL = (len(MODEL_ROWS), len(FILES_COLUMNS["Astigmatism 3D Model"]["columns"]))  # Dimensions pour le model d'astigmatisme 3D (2,5).


# ==================================================
# region Manipulation de DataFrame
# ==================================================
##################################################
def apply_dataframe_type(data: pd.DataFrame, columns: list[str], numeric_type: str = "int32"):
	"""
	Force les colonnes en paramètres à adopter un type numérique.
	Vérifie la présence des colonnes avant la transformation pour éviter les problèmes et préserve les NaN s'ils sont présents.

	:param data: DataFrame à modifier.
	:param columns: Colonnes à modifier.
	:param numeric_type: Type à adopter.
	"""
	for key in columns:
		# Vérification en cas de Dataframe Vide et conversion en entier nullable (préserve les NaN si présents)
		if key in data.columns: data[key] = pd.to_numeric(data[key], errors="coerce").astype(numeric_type)


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
	if missing_columns: raise ValueError(f"Les colonnes suivantes sont absentes du DataFrame : {missing_columns}")

	if remaining:
		remaining_columns = [col for col in data.columns if col not in columns]  # Colonnes restantes (toutes sauf celles déjà définies)
		columns += remaining_columns  # .										   Ajout des colonnes restantes aux colonnes de départ

	if list(data.columns[:len(columns)]) == columns: return data  # .			   Optimisation : évite la copie si déjà bon ordre
	return data.loc[:, columns]  # .											   Réorganisation du DataFrame


##################################################
def log10_dataframe(data: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
	"""
	Applique un log en base 10 sur certaines colonnes du dataframe (remplace par Nan les valeurs inférieures ou égales à 0).

	:param data: Dataframe à modifier.
	:param columns: Colonnes à modifier.
	:return: Dataframe avec les colonnes ayant été modifiées.
	"""
	with np.errstate(divide='ignore', invalid='ignore'):
		logged = np.where(data[columns] > 0, np.log10(data[columns]), np.nan)  # Remplace log(x<=0) par NaN pour éviter les -inf/erreurs
	data[columns] = pd.DataFrame(logged, index=data.index, columns=columns)
	return data


# ==================================================
# endregion Manipulation de DataFrame
# ==================================================

# ==================================================
# region Gestion des angles
# ==================================================
##################################################
def degrees_to_radians(angle_deg: np.ndarray | pd.Series | float | list) -> np.ndarray:
	"""
	Convertit des angles en degrés vers des radians.

	.. math::
		\\theta_{rad} = \\theta_{deg} \\times \\frac{\\pi}{180}

	:param angle_deg: Angle(s) en degrés (scalaire, array NumPy ou Series pandas).
	:return: Angle(s) en radians.
	"""
	return np.asarray(angle_deg) * (np.pi / 180.0)


##################################################
def radians_to_degrees(angle_rad: np.ndarray | pd.Series | float | list) -> np.ndarray:
	"""
	Convertit des angles en radians vers des degrés.

	.. math::
		\\theta_{deg} = \\theta_{rad} \\times \\frac{180}{\\pi}

	:param angle_rad: Angle(s) en radians (scalaire, array NumPy ou Series pandas).
	:return: Angle(s) en degrés.
	"""
	return np.asarray(angle_rad) * (180.0 / np.pi)


##################################################
def wrap_angle(theta: np.ndarray | pd.Series | float | list, length: float = np.pi, center: bool = True) -> np.ndarray:
	"""
	Contraint des angles dans un intervalle sélectionné, exemple avec :math:`length = \\pi` et un intervalle centré.

	.. math::
		\\theta' \\in [-\\frac{\\pi}{2}, \\frac{\\pi}{2}[ \\quad\\quad \\text{and} \\quad\\quad
		\\theta' = (\\theta + \\frac{\\pi}{2}) \\bmod (\\pi) - \\frac{\\pi}{2}

	:param theta: Angles en radians.
	:param length: Longueur de l'intervalle.
	:param center: Définit l'intervalle à :math:`[-\\frac{limit}{2}, \\frac{limit}{2}[` si true, sinon :math:`[0, length[`.
	:return: Angles normalisés dans :math:`[-\\frac{\\pi}{2}, \\frac{\\pi}{2}[`.
	"""
	low = length / 2 if center else 0
	return (np.asarray(theta) + low) % length - low


##################################################
def manage_theta(theta: np.ndarray | pd.Series | float | list) -> np.ndarray:
	"""
	Contraint des angles en radians dans l'intervalle :math:`[-\\frac{\\pi}{2}, \\frac{\\pi}{2}[` (:func:`wrap_angle`).
	Puis passe des radians aux degrés pour faciliter la lisibilité.

	Définit un theta commun possible en degré de deux méthodes différentes (moyenne et médiane circulaire) ainsi qu'une mesure de la dispersion.
	Une dispersion R > 0.8 indique une bonne fiabilité de l'orientation, R < 0.5 indique une orientation mal définit.


	:param theta: Angles en radians.
	:return: Theta dans l'intervalle :math:`[-\\frac{\\pi}{2}, \\frac{\\pi}{2}[`.
	"""
	theta = wrap_angle(theta)  # Clean Theta interval

	cos_theta, sin_theta = np.cos(theta), np.sin(theta)

	# --- Moyenne circulaire ---
	cos_mean, sin_mean = np.mean(cos_theta), np.mean(sin_theta)
	theta_mean = radians_to_degrees(np.arctan2(sin_mean, cos_mean))

	# --- Médiane robuste ---
	cos_median, sin_median = np.median(cos_theta), np.median(sin_theta)
	theta_median = radians_to_degrees(np.arctan2(sin_median, cos_median))

	# --- Dispersion ---
	r = np.sqrt(sin_mean ** 2 + cos_mean ** 2)

	print(f"Theta mean: {theta_mean:.2f}°, Theta median (robust) : {theta_median:.2f}°, Concentration R: {r:.3f}")
	return radians_to_degrees(theta)


# ==================================================
# endregion Gestion des angles
# ==================================================

# ==================================================
# region Parsing
# ==================================================
##################################################
def get_meta(data: list | np.ndarray) -> pd.DataFrame:
	"""Créer le Dataframe pour les informations meta (dimensions du fichier et calibration).

	:param data: Liste des informations en entrée.
	:return: :class:`DataFrame <pandas.DataFrame>` contenant les métadonnées.
	:raises ValueError: Si le nombre d'éléments ne correspond au nombre attendu pour le fichier méta.
	"""
	columns, types = FILES_COLUMNS["Meta"]["columns"], FILES_COLUMNS["Meta"]["types"]

	arr = np.asarray(data).reshape(1, -1)  # Aplatit vers (N,) puis force (1, N)
	if arr.shape[1] != len(columns): raise ValueError(f"Le nombre d'éléments ne correspond pas : {arr.shape[1]} reçus, {len(columns)} attendus.")

	res = pd.DataFrame(arr, columns=columns, dtype=np.float32)  # Transformation en Dataframe
	apply_dataframe_type(res, types)  # Conversion en entier nullable (préserve les NaN si présents)
	return res


##################################################
def parse_irregular_array(data: np.ndarray) -> pd.DataFrame:
	"""
	Parsing du résultat de la DLL PALM.

	Entrée : un tableau 1D où chaque bloc est encodé comme : [L, x0, x1, ..., x{L-1}, L2, y0, y1, ..., ...]
	Le parsing s'arrête dès qu'un L ≤ 0 est rencontré.

	Règles :
		- Le premier élément d'un bloc (L) donne le nombre d'éléments qui suivent pour ce bloc.
		- Les longueurs négatives ou nulles (L ≤ 0) signalent la fin du flux.
		- Les blocs tronqués (pas assez d'éléments après L) lèvent une ``ValueError``.
		- Les valeurs des blocs (sans L) sont retournées dans le DataFrame.
		- Les lignes n'ayant pas le même nombre de colonnes sont complétées par NaN.

	:param data: Données 1D récupérées depuis la DLL PALM. Doit être indexable et de dimension 1.
	:return: :class:`DataFrame <pandas.DataFrame>` où chaque ligne correspond à un bloc et les colonnes contiennent les valeurs du bloc, complétées par NaN.
	:raise ValueError: Entrée invalide (nombre de dimensions ou taille finale incorrecte).
	"""
	if data.ndim != 1:
		raise ValueError("`data` doit être un tableau 1D.")

	rows: list[np.ndarray] = []
	i = 0
	n = data.size

	while i < n:
		# Lecture de L (la longueur annoncée du bloc)
		l_raw = data[i]
		try:
			l = int(l_raw)
		except (TypeError, ValueError):
			raise ValueError(f"Longueur de bloc non entière à l'indice {i}: {l_raw!r}") from None

		if l <= 0: break  # fin du flux

		i += 1  # on avance sur le premier élément du bloc
		if i + l > n: raise ValueError(f"Bloc tronqué: longueur {l} annoncée à l'indice {i - 1}, mais seulement {n - i} élément(s) disponible(s).")
		# Extraction du bloc (les L valeurs, sans L lui-même)
		rows.append(np.asarray(data[i:i + l]))
		i += l  # passer au bloc suivant

	# Construction du DataFrame avec padding NaN
	if not rows: return pd.DataFrame()  # aucun bloc valide avant un L<=0 ou tableau vide

	max_len = max(len(r) for r in rows)
	out = np.full((len(rows), max_len), np.nan, dtype=float)
	for r_idx, r in enumerate(rows):
		if r.size: out[r_idx, :r.size] = r

	columns = [f"Val_{k}" for k in range(max_len)]
	df = pd.DataFrame(out, columns=columns)
	return df


##################################################
def parse_result(data: np.ndarray, file_type: str = "Localization", is_log: bool = False, fit_mode: int = 0) -> pd.DataFrame:
	"""
	Parsing du résultat de la DLL PALM.

	Pour les localisations et les trajectoires, on a un tableau 1D de grande taille en entrée :
		- On le découpe en tableau 2D à 13 colonnes (``N_SEGMENTS``). La taille du tableau est vérifiée et tronquée si nécessaire.
		- On le transforme en dataframe avec les colonnes définies par `SEGMENTS`.
		- On supprime les lignes remplies de 0 et de -1. Un test sur les colonnes X ou Y strictement positif suffit (le SigmaX et SigmaY peuvent être à 0).

	Pour les calculs sur trajectoire, on a un tableau 1D représentant un tableau 2D irrégulier
	(avec un nombre de colonnes non constant (:func:`parse_irregular_array`).

	:param data: Données en entrée récupérées depuis la DLL PALM.
	:param file_type: Type de fichier à parser (Localization, Tracking, Astigmatism 3D Model, MSD, Instant diffusion, Fit).
	:param is_log: Applique un logarithme sur le résultat (si nécessaire, pour les calculs sur trajectoires).
	:param fit_mode: Mode d'ajustement (si nécessaire, pour les calculs sur trajectoires).
	:return: :class:`DataFrame <pandas.DataFrame>` parsé.
	"""
	# Récupération des éléments
	if file_type not in FILES_COLUMNS: raise ValueError(f"file_type incorrect.")
	columns, types = FILES_COLUMNS[file_type]["columns"], FILES_COLUMNS[file_type]["types"]
	n_columns = len(columns)
	log_col = []

	if file_type == "Localization" or file_type == "Tracking":
		# Manipulation du tableau 1D.
		size = (data.size // n_columns) * n_columns  # .Récupération de la taille correcte si non multiple de N_SEGMENT
		data = data[:size].reshape(-1, n_columns)  # .	Passage en tableau 2D
		data = data[data[:, columns.index("X")] > 0]  # Filtrage sur les X inférieurs ou égal à 0 en amont.
		res = pd.DataFrame(data, columns=columns)  # .	Transformation en Dataframe
	elif file_type == "Astigmatism 3D Model":
		res = pd.DataFrame(data, columns=columns, index=MODEL_ROWS)
	else:
		res = parse_irregular_array(data)
		ncols = res.shape[1]
		if ncols == 0: return pd.DataFrame()
		if file_type == "MSD" or file_type == "Instant Diffusion":
			log_col = [f"{columns[1]} {i}" for i in range(1, ncols)]
			res.columns = [columns[0]] + log_col
		else:
			# les colonnes dépendent de l'ajustement.
			log_col = columns[2:]
			if not 1 <= fit_mode <= 3: raise ValueError(f"fit_mode doit être entre 1 et 3 : reçu {fit_mode}.")
			log_col += FILES_COLUMNS[f"Fit_{fit_mode}"]["columns"]
			res.columns = columns[:2] + log_col

	if is_log and log_col: res = log10_dataframe(res, log_col)  # Mise à jour en fonction de la mise à l'échelle du Log.
	apply_dataframe_type(res, types)
	return res


##################################################
def parse_localization_for_tracking(data: pd.DataFrame) -> np.ndarray:
	"""
	Parsing du résultat de la localisation pour le suivi au sein de la DLL.

	:param data: Donnée en entrée récupérées depuis la localisation.
	:return: :class:`ndarray <numpy.ndarray>` transformé pour le suivi.
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
# ==================================================
# endregion Parsing
# ==================================================
