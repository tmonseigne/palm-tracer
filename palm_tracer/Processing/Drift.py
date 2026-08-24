"""Fournit les fonctions d'extraction des billes et de correction de la dérive."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

from palm_tracer.Processing.Parsing import apply_dataframe_type, FILES_COLUMNS


##################################################
@dataclass
class _ActiveTrack:
	"""Conserve l'état temporaire du suivi d'une bille entre plusieurs plans.

	:param track_id: Identifiant de la trajectoire en cours de construction.
	:param ids: Identifiants successifs des localisations associées.
	:param last_pos: Dernière position connue de la bille.
	"""

	track_id: int
	ids: list[int]
	last_pos: np.ndarray  # shape (D,)


##################################################
def _check_cols(data: pd.DataFrame, required: set[str]):
	"""Vérification rapide des colonnes."""
	missing = sorted(required - set(data.columns))
	if missing: raise ValueError(f"Missing columns in data: {missing}.")


##################################################
def _check_planes(data: pd.DataFrame) -> np.ndarray:
	"""
	Vérifie les plans disponibles dans le dataframe et leur continuité.
	:param data: Dataframe à analyser.
	:return: Liste des plans triés.
	"""
	planes = np.array(sorted(pd.unique(data["Plane"])))
	expected = np.arange(planes[0], planes[-1] + 1, dtype=planes.dtype)
	if planes.size < 2:
		raise ValueError(f"We need at least 2 planes.")
	if planes.size != expected.size or np.any(planes != expected):
		raise ValueError(f"The planes are not consecutive: {planes}.")
	return planes


##################################################
def _assign_tracks_to_points_greedy(indices: np.ndarray, distances: np.ndarray, n_points: int) -> tuple[np.ndarray, np.ndarray]:
	"""
	Assigne des suivis à des points du plan courant en gérant les collisions, à partir des résultats de :meth:`scipy.spatial.cKDTree.query` avec ``k>1``.

	Pour chaque suivi, on dispose d'une liste de candidats triés par distance croissante (jusqu'à k).
	On construit toutes les paires (distance, track, point) valides puis on fait un appariement glouton par distance croissante :
	- un suivi reçoit au plus 1 point ;
	- un point est assigné à au plus 1 suivi.

	.. note:: Cette stratégie permet à un suivi de "prendre son 2ᵉ choix" si son meilleur candidat est déjà pris.

	:param indices: Indices retournés par KDTree (forme (T, k) ou (T,) si k==1).
	:param distances: Distances retournées par KDTree (même forme que ``ind``).
	:param n_points: Nombre de points dans le plan courant (``tree.n``).
	:returns: (keep_tracks, keep_points) indices des suivis (0..T-1) et points (0..P-1) retenus.
	"""
	# Normalisation shape : (n, k)
	if indices.ndim == 1: indices, distances = indices[:, None], distances[:, None]

	n, k = indices.shape
	pairs: list[tuple[float, int, int]] = []

	# Construction des propositions valides.
	for i in range(n):  # .									  Pour chaque suivi.
		for j in range(k):  # .								  Pour les k plus proches voisins.
			p_j = int(indices[i, j])  # .					  Récupération du jieme voisin du suivi i.
			if p_j >= n_points: continue  # .				  >= n_points signifie "pas de voisin dans le rayon" ⇒ on ignore.
			pairs.append((float(distances[i, j]), i, p_j))  # On ajoute aux propositions, la distance, le suivi et le point.

	# Aucun voisin valide pour aucun suivi (tous les indices == n_points) ⇒ aucune paire candidate.
	if not pairs: return np.empty((0,), dtype=np.int32), np.empty((0,), dtype=np.int32)

	# Appariement glouton : plus petites distances d'abord.
	pairs.sort(key=lambda x: x[0])

	used_t: set[int] = set()
	used_p: set[int] = set()
	keep_t: list[int] = []
	keep_p: list[int] = []

	for d, i, p_j in pairs:
		if i in used_t or p_j in used_p: continue  # Le suivi/point a déjà été assigné
		used_t.add(i)
		used_p.add(p_j)
		keep_t.append(i)
		keep_p.append(p_j)

	return np.asarray(keep_t, dtype=np.int32), np.asarray(keep_p, dtype=np.int32)


##################################################
def extract_beads(data: pd.DataFrame, max_distance: float = 1, is_3d: bool = True, *, strict: bool = True, k: int = 4) -> pd.DataFrame:
	"""
	Extrait des billes suivies à travers les plans en ne conservant que celles qui ont une correspondance dans **tous** les plans
	(du premier au dernier plan présent dans ``data``).

	La correspondance entre deux plans consécutifs est réalisée avec une contrainte de distance euclidienne de type "sphère" :
	:math:`\\sqrt{x^2+y^2+z^2} \\leq max_{distance}`

	En cas de multiples candidats, on choisit le plus proche en distance euclidienne.
	Les conflits (un même point du plan suivant proposé pour plusieurs tracks) sont résolus par un appariement glouton sur les distances croissantes
	(un point ne peut être assigné qu'à un seul track).

	:param data: DataFrame contenant au minimum les colonnes ``Plane``, ``X``, ``Y`` et ``Z``.
				 Chaque ligne représente une détection (un point) dans un plan donné.
	:param max_distance: Distance maximale autorisée entre deux plans (en unités des coordonnées) selon la norme L∞.
	:param is_3d: Si ``True``, utilise (X,Y,Z). Sinon, utilise uniquement (X,Y).
	:param strict: Si ``True``, la distance doit être strictement inférieure à la distance maximale (comportement par défaut).
	:param k: Nombre de correspondances maximum pour chaque point, permet de gérer les collisions de suivis (par défaut 4 maximum).
	          Dans la réalité, avec des données et paramètres cohérents, il n'y aura qu'un seul correspondant ou aucun pour chaque point.

	:returns: Un nouveau DataFrame ne contenant **que** les points appartenant à des billes valides,
			  avec une colonne ``Bead`` (1..N) indiquant l'identifiant de la bille. Les lignes sont triées par ``Bead`` puis ``Plane``.

	:raises ValueError: Si des colonnes requises sont manquantes, ou si ``max_distance`` n'est pas strictement positif.
	"""
	# ----- Vérifications initiales -----
	if max_distance <= 0:
		raise ValueError("max_distance must be strictly positive.")
	if data.empty: return pd.DataFrame()

	columns, types = FILES_COLUMNS["Beads"]["columns"], FILES_COLUMNS["Beads"]["types"]
	common_columns = [c for c in columns if c in data.columns]  # Permissif sur les colonnes pour le fichier.
	_check_cols(data, {"Plane", "X", "Y", "Z"})  # Vérification des colonnes minimales

	# Création d'une copie légère et on conserve l'index original pour le slicing final.
	work = data.loc[:, list(common_columns)]
	work["_index"] = data.index
	planes = _check_planes(work)

	# ----- Intialisation -----
	by_plane: dict[int, pd.DataFrame] = {p: df for p, df in work.groupby("Plane", sort=False)}
	coord_cols = ["X", "Y", "Z"] if is_3d else ["X", "Y"]

	# --- petit utilitaire
	def _get_plane_infos(plane):
		"""
		Récupère rapidement les informations du plan.
		:param plane: Plan à récupérer.
		:return: DataFrame du plan, position et index des points du plan.
		"""
		df = by_plane[plane]
		return df, df[coord_cols].to_numpy(dtype=np.float64, copy=False), df["_index"].to_numpy(copy=False)

	# Création d'un tableau de possibles trajectoires pour tous les points du plan 1
	df_0, c_0, i_0 = _get_plane_infos(planes[0])
	active_tracks: list[_ActiveTrack] = []
	for pt in range(len(df_0)): active_tracks.append(_ActiveTrack(track_id=pt, ids=[i_0[pt]], last_pos=c_0[pt]))

	# ----- Parcours -----
	p_norm = 2  # NOTE : p=2 ⇒ sphère. Mettre p=np.inf pour un cube (L∞).
	if not strict: max_distance = np.nextafter(np.float64(max_distance), np.inf)
	for p in planes[1:]:
		_, c_p, i_p = _get_plane_infos(p)
		# if df_p.empty or not active_tracks: return pd.DataFrame()  # Plus de points ou plus de suivi ⇒ terminé. Impossible dans ce flux.
		tree = cKDTree(c_p)  # .										KDTreee des points du plan actuel.
		last = np.stack([t.last_pos for t in active_tracks], axis=0)  # Dernier point de chaque suivi (taille N_suivi).

		# --- Query "k plus proches voisins dans un rayon" ---
		# SciPy récent parallélise la requête si possible avec workers=-1
		dist, ind = tree.query(last, k=min(k, tree.n), p=p_norm, distance_upper_bound=max_distance, workers=-1)

		# --- Résolution des collisions (en temps normal difficile à obtenir avec une densité une distance max cohérente.) ---
		keep_t, keep_p = _assign_tracks_to_points_greedy(ind, dist, n_points=tree.n)
		if keep_t.size == 0: return pd.DataFrame()

		# --- Mise à jour des tracks actifs ---
		new_active_tracks: list[_ActiveTrack] = []
		for t_i, p_j in zip(keep_t.tolist(), keep_p.tolist(), strict=True):
			t = active_tracks[t_i]  # .		Récupération d'un suivi valide
			t.ids.append(i_p[p_j])  # .		Ajout du point au suivi
			t.last_pos = c_p[p_j].copy()  # Remplacement de la dernière position.
			new_active_tracks.append(t)

		active_tracks = new_active_tracks  # Switch

	# ----- Préparation des données à renvoyer -----
	work.drop(columns=["_index"], inplace=True)
	rows: list[pd.DataFrame] = []  # Les tracks restants sont des billes valides. On rassemble leurs points dans une liste de dataframe.
	for p in range(len(active_tracks)):
		df_bead = work.loc[active_tracks[p].ids]
		df_bead.insert(0, "Bead", int(p + 1))  # Ajout d'une colonne Bead avec le numéro de la bille de 1 à N.
		rows.append(df_bead)

	# if not rows: return pd.DataFrame()  # Aucune bille complète ⇒ terminé. Impossible dans ce flux
	beads = pd.concat(rows, axis=0, ignore_index=False)  # Concatenation en un seul dataframe
	apply_dataframe_type(beads, types)
	return beads.sort_values(by=["Bead", "Plane"], kind="stable").reset_index(drop=True)  # Tri stable pour lisibilité.


##################################################
def remove_beads(data: pd.DataFrame, beads: pd.DataFrame, decimals: int = 5) -> pd.DataFrame:
	"""
	Mets à jour data en lui enlevant les billes identifiées (correspondance exact sur Plane/X/Y/Z).

	:param data: Données de localisation (doit contenir Plane, X, Y, Z).
	:param beads: Billes à retirer (doit contenir Plane, X, Y, Z).
	:param decimals: Nombre de décimales conservées pour la comparaison (évite les problèmes d'arrondi float).
	:returns: Copie de data sans les lignes correspondant aux billes.
	"""
	if data.empty or beads.empty: return data

	required = {"X", "Y", "Z"}
	_check_cols(data, required)
	_check_cols(beads, required)

	keys = ["Plane", "X", "Y", "Z"]

	# --- Création de copies arrondies pour comparaison ---
	data_cmp = data.assign(X=data["X"].round(decimals), Y=data["Y"].round(decimals), Z=data["Z"].round(decimals))
	beads_cmp = beads.assign(X=beads["X"].round(decimals), Y=beads["Y"].round(decimals), Z=beads["Z"].round(decimals)).drop_duplicates()
	# --- Anti-join ---
	mask = ~pd.MultiIndex.from_frame(data_cmp[keys]).isin(pd.MultiIndex.from_frame(beads_cmp[keys]))
	return data.loc[mask].copy().reset_index(drop=True)


##################################################
def get_drift(beads: pd.DataFrame, is_3d: bool = True) -> pd.DataFrame:
	"""
	Calcule le drift moyen interplans à partir d'un DataFrame de billes suivies.

	Le drift est calculé pour chaque bille comme la différence entre deux plans consécutifs :

	- :math:`\\Delta X(n) = X(n) - X(n-1)`
	- :math:`\\Delta Y(n) = Y(n) - Y(n-1)`
	- :math:`\\Delta Z(n) = Z(n) - Z(n-1)` (si ``is_3d=True``)

	Et il est associé au plan ``n`` (donc le drift commence au plan 2).

	Ensuite, on moyenne ces drifts entre toutes les billes disponibles.

	:param beads: DataFrame contenant au minimum ``Bead``, ``Plane``, ``X``, ``Y``, ``Z``.
				  Chaque bille doit avoir exactement une ligne par plan et les plans doivent être consécutifs.
	:param is_3d: Si ``True``, calcule aussi le drift en Z. Sinon, la colonne Z est renvoyée à 0.

	:returns: DataFrame avec colonnes ``Plane``, ``X``, ``Y``, ``Z`` contenant le drift moyen, pour les plans de 2 à N.
	:raises ValueError: Si des colonnes sont manquantes, ou incohérence de plans au sein des billes.
	"""
	# ----- Vérifications initiales -----
	if beads.empty: return pd.DataFrame()

	required = {"Bead", "Plane", "X", "Y", "Z"}
	_check_cols(beads, required)
	work = beads.loc[:, list(required)]  # .						Copie légère : uniquement les colonnes nécessaires.
	work = work.sort_values(by=["Bead", "Plane"], kind="stable")  # Théoriquement inutile, mais en cas de mauvaise utilisation...
	planes = _check_planes(work)

	# --- Calcul des deltas par bille ---
	work["dX"] = work.groupby("Bead")["X"].diff()
	work["dY"] = work.groupby("Bead")["Y"].diff()
	work["dZ"] = work.groupby("Bead")["Z"].diff() if is_3d else 0.0
	work = work.loc[work["Plane"] != int(planes[0])]

	# --- Moyenne sur les billes, plan par plan ---
	drift = (work.groupby("Plane", as_index=False)[["dX", "dY", "dZ"]].mean().rename(columns={"dX": "X", "dY": "Y", "dZ": "Z"}))
	return drift.sort_values(by=["Plane"], kind="stable").reset_index(drop=True)


##################################################
def remove_drift(data: pd.DataFrame, drift: pd.DataFrame, is_3d: bool = True) -> pd.DataFrame:
	"""
	Applique une correction de drift à un DataFrame de points.

	Le DataFrame ``drift`` doit contenir une ligne par plan, avec les colonnes ``Plane``, ``X``, ``Y`` et ``Z``.
	Le drift est supposé défini pour les plans 2..N et associé au plan courant (même convention que :func:`get_drift`).

	La correction appliquée est :

	- :math:`X_{corr}(n) = X(n) - X_{drift}(n)`
	- :math:`Y_{corr}(n) = Y(n) - Y_{drift}(n)`
	- :math:`Z_{corr}(n) = Z(n) - Z_{drift}(n)`

	:param data: DataFrame contenant au minimum ``Plane``, ``X``, ``Y`` ``Z``.
	:param drift: DataFrame contenant au minimum ``Plane``, ``X``, ``Y`` ``Z``, typiquement pour les plans 2..N.
	:param is_3d: Si ``True``, applique aussi la correction en Z.

	:returns: Un nouveau DataFrame corrigé (mêmes colonnes que ``data``).
	:raises ValueError: Si des colonnes sont manquantes dans ``data`` ou ``drift``.
	"""
	# ----- Vérifications initiales -----
	if data.empty or drift.empty: return pd.DataFrame()

	required = {"Plane", "X", "Y", "Z"}
	_check_cols(data, required)
	_check_cols(drift, required)

	# --- drift incrémental -> drift cumulatif ---
	drift_work = drift.loc[:, list(required)].copy()
	drift_work = drift_work.sort_values("Plane", kind="stable").reset_index(drop=True)
	drift_work[["X", "Y", "Z"]] = drift_work[["X", "Y", "Z"]].cumsum()
	drift_work = drift_work.set_index("Plane")

	# --- Application : join + soustraction ---
	out = data.copy()
	out = out.join(drift_work, on="Plane", rsuffix="_drift")  # On fait un merge aligné sur Plane pour vectoriser (évite une boucle Python par plan).
	out = out.fillna(0.0)

	# Soustraction (correction).
	out["X"] -= out["X_drift"]
	out["Y"] -= out["Y_drift"]
	if is_3d: out["Z"] -= out["Z_drift"]
	out.drop(columns=[c for c in out.columns if c.endswith("_drift")], inplace=True)  # Nettoyage
	return out


##################################################
def drift_correction(data: pd.DataFrame, max_distance: float = 1, is_3d: bool = True, *, strict: bool = True, k: int = 4) -> tuple[pd.DataFrame, pd.DataFrame]:
	"""
	Trouve des billes au sein d'un jeu de donnée, calcule le drift et le corrige.

	:param data: DataFrame contenant au minimum les colonnes ``Plane``, ``X``, ``Y`` et ``Z``.
				 Chaque ligne représente une détection (un point) dans un plan donné.
	:param max_distance: Distance maximale autorisée entre deux plans (en unités des coordonnées) selon la norme L∞.
	:param is_3d: Si ``True``, utilise (X,Y,Z). Sinon, utilise uniquement (X,Y).
	:param strict: Si ``True``, la distance doit être strictement inférieure à la distance maximale (comportement par défaut).
	:param k: Nombre maximal de correspondances autorisées pour chaque point. Permet de gérer les collisions de suivi (4 au maximum par défaut).
			  En pratique, avec des données et des paramètres cohérents, chaque point ne possède qu'une seule correspondance, voire aucune.

	:returns: Les billes identifiées et un nouveau DataFrame ne contenant les données corrigées.
	"""

	beads = extract_beads(data, max_distance=max_distance, is_3d=is_3d, strict=strict, k=k)
	drift = get_drift(beads, is_3d=is_3d)
	return beads, remove_drift(data, drift, is_3d=is_3d)


##################################################
def median_filter_centered(data: np.ndarray, size: int = 5) -> np.ndarray:
	"""
	Applique un filtre médian centré sur un signal 1D ou sur un tableau 2D ``(nb_points, nb_axes)``.

	Le filtrage est effectué indépendamment sur chaque axe. Aux bords, la fenêtre est tronquée aux échantillons disponibles.

	Exemples pour ``size = 5`` :

	- indice 0  ⇾ médiane sur les 3 premiers (indices [0:3])
	- indice 1  ⇾ médiane sur les 4 premiers (indices [0:4])
	- indice 2  ⇾ médiane sur les 5 premiers (indices [0:5])
	- ...
	- avant-dernier ⇾ médiane sur les 4 derniers
	- dernier       ⇾ médiane sur les 3 derniers

	:param data: Signal à filtrer. Si ``data`` est 1D, la forme attendue est ``(nb_points,)``.
				 Si ``data`` est 2D, la forme attendue est ``(nb_points, nb_axes)``.
	:param size: Taille de la fenêtre médiane. Doit être un entier impair strictement positif.
	:return: Tableau filtré de type ``float64`` et de même forme que l'entrée.
	:raises ValueError: Levée si ``size`` n'est pas un entier impair strictement positif.
	"""
	if size <= 0 or size % 2 == 0:
		raise ValueError(f"'size' doit être un entier impair strictement positif, mais vaut {size}.")

	is_1d = data.ndim == 1

	if data.ndim == 1: work = data[:, np.newaxis]
	elif data.ndim == 2: work = data
	else: raise ValueError(f"'data' doit être un tableau 1D ou 2D, mais a {data.ndim} dimensions.")

	nb_points = work.shape[0]
	if nb_points == 0: return data.copy()

	half_window = size // 2
	result = np.empty_like(work)

	for idx in range(nb_points):
		start, end = max(0, idx - half_window), min(nb_points, idx + half_window + 1)
		result[idx] = np.nanmedian(work[start:end], axis=0)

	return result[:, 0] if is_1d else result
