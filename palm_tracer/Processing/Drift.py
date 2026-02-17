"""Fichier contenant des fonctions pour le drift."""

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree


##################################################
@dataclass
class _ActiveTrack:
	"""Suivi actif d'une bille à travers les plans."""
	track_id: int
	ids: list[int]
	last_pos: np.ndarray  # shape (D,)


##################################################
def _resolve_collisions_greedy(track_indices: np.ndarray, point_indices: np.ndarray, distances: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
	"""
	Résout les collisions (plusieurs tracks pointent vers le même point du plan suivant) en gardant, pour chaque point, le suivi ayant la plus petite distance.

	.. note:: Il pourrait y avoir un ordre des points les plus au moins proche, mais, avec des paramètres cohérents,
	          on serait dans une configuration où deux billes seraient presque supporposées. Donc on préfère n'en conserver qu'une (la plus stable).

	:param track_indices: Indices des tracks (0..T-1) proposés.
	:param point_indices: Indices des points du plan suivant (0..P-1) proposés.
	:param distances: Distances associées (même taille que track_indices).
	:returns: (keep_tracks, keep_points) tableaux d'indices après résolution.
	"""
	# if track_indices.size == 0: return np.empty((0,), dtype=np.int32), np.empty((0,), dtype=np.int32)  # Impossible dans ce flux

	# Tri par point puis par distance croissante.
	order = np.lexsort((distances, point_indices))
	tr_s = track_indices[order]
	pt_s = point_indices[order]

	# Garder 1 match par point : le premier (distance min) après tri.
	keep_mask = np.ones(pt_s.shape[0], dtype=bool)
	if pt_s.shape[0] > 1: keep_mask[1:] = pt_s[1:] != pt_s[:-1]

	return tr_s[keep_mask], pt_s[keep_mask]


##################################################
def extract_beads(data: pd.DataFrame, max_distance: float = 1, is_3d: bool = True) -> pd.DataFrame:
	"""
	Extrait des billes suivies à travers les plans en ne conservant que celles qui ont un match	dans **tous** les plans
	(du premier au dernier plan présent dans ``data``).

	La correspondance entre deux plans consécutifs est réalisée avec une contrainte de distance
	de type "cube" (norme de Chebyshev, i.e. :math:`||\\Delta||_\\infty \\le d_{max}`), ce qui revient à imposer ::

	    |dx| <= max_distance
	    |dy| <= max_distance
	    |dz| <= max_distance   (si is_3d=True)

	En cas de multiples candidats, on choisit le plus proche en distance euclidienne.
	Les conflits (un même point du plan suivant proposé pour plusieurs tracks) sont résolus par un appariement glouton sur les distances croissantes
	(un point ne peut être assigné qu'à un seul track).

	:param data: DataFrame contenant au minimum les colonnes ``Plane``, ``X``, ``Y`` et éventuellement ``Z``.
				 Chaque ligne représente une détection (un point) dans un plan donné.
	:param max_distance: Distance maximale autorisée entre deux plans (en unités des coordonnées) selon la norme L∞.
	:param is_3d: Si ``True``, utilise (X,Y,Z). Sinon, utilise uniquement (X,Y).

	:returns: Un nouveau DataFrame ne contenant **que** les points appartenant à des billes valides,
			  avec une colonne ``Bead`` (1..N) indiquant l'identifiant de la bille. Les lignes sont triées par ``Bead`` puis ``Plane``.

	:raises ValueError: Si des colonnes requises sont manquantes, ou si ``max_distance`` n'est pas strictement positif.
	"""
	# ----- Vérifications initiales -----
	if max_distance <= 0: raise ValueError("max_distance must be strictly positive.")
	if data.empty: return pd.DataFrame()

	required = {"Plane", "X", "Y"} | ({"Z"} if is_3d else set())
	missing = sorted(required - set(data.columns))
	if missing: raise ValueError(f"Missing columns in data: {missing}")

	# Création d'une copie légère et on conserve l'index original pour le slicing final.
	work = data.loc[:, list(required)].copy()
	work["_index"] = data.index

	# Plans triés
	planes = np.array(sorted(pd.unique(work["Plane"])))
	if planes.size < 2: return pd.DataFrame()
	if planes[-1] != len(planes): raise ValueError(f"The planes are not consecutive from 1 to N: {planes}")

	# ----- Intialisation -----
	by_plane: dict[int, pd.DataFrame] = {p: df for p, df in work.groupby("Plane", sort=False)}
	coord_cols = ["X", "Y", "Z"] if is_3d else ["X", "Y"]
	df_0 = by_plane.get(planes[0], pd.DataFrame(columns=work.columns))
	c_0 = df_0[coord_cols].to_numpy(dtype=np.float64, copy=False)
	i_0 = df_0["_index"].to_numpy(copy=False)

	# Création d'un tableau de possibles trajectoires pour tous les points du plan 1
	active_tracks: list[_ActiveTrack] = []
	for i in range(len(df_0)): active_tracks.append(_ActiveTrack(track_id=i, ids=[i_0[i]], last_pos=c_0[i].copy()))

	# ----- Parcours -----
	p_norm = 2  # NOTE : p=2 ⇒ sphère. Mettre p=np.inf pour un cube (L∞).
	for i in planes[1:]:
		df_p = by_plane.get(i, pd.DataFrame(columns=work.columns))
		if df_p.empty or not active_tracks: return pd.DataFrame()  # Plus de points ou plus de suivi ⇒ terminé (aucune bille complète).

		c_p = df_p[coord_cols].to_numpy(dtype=np.float64, copy=False)
		i_p = df_p["_index"].to_numpy(copy=False)
		tree = cKDTree(c_p)  # KDTreee des points du plan actuel.
		last = np.stack([t.last_pos for t in active_tracks], axis=0)  # Dernier point de chaque suivi (taille N_suivi).

		# --- Query "1 plus proche voisin dans un rayon" ---
		dist, ind = tree.query(last, k=1, p=p_norm, distance_upper_bound=max_distance, workers=-1)  # SciPy récent parallélise la requête si possible
		valid = ind < tree.n  # ind == tree.n => pas de voisin dans le rayon
		if not np.any(valid): return pd.DataFrame()  # Aucun Voisin ⇒ terminé (aucune bille complète).

		t_i = np.nonzero(valid)[0].astype(np.int32, copy=False)  # Tableau d'indice des suivis valides
		p_i = ind[valid].astype(np.int32, copy=False)  # Tableau d'indices des points du plan (c_p) pour chaques suivis valides.
		d_i = dist[valid].astype(np.float64, copy=False)  # Distance entre le point du plan précédent et le match pour chaques suivis valides.

		# --- Résolution des collisions (en temps normal difficile à obtenir avec une densité une distance max cohérente.) ---
		keep_t, keep_p = _resolve_collisions_greedy(t_i, p_i, d_i)
		# if keep_t.size == 0: return pd.DataFrame()  # Impossible dans ce flux

		# --- Mise à jour des tracks actifs ---
		new_active_tracks: list[_ActiveTrack] = []
		for t_i, p_j in zip(keep_t.tolist(), keep_p.tolist(), strict=True):
			t = active_tracks[t_i]  # Récupération d'un suivi valide
			t.ids.append(i_p[p_j])  # Ajout du point au suivi
			t.last_pos = c_p[p_j].copy()  # Remplacement de la dernière position.
			new_active_tracks.append(t)

		active_tracks = new_active_tracks  # Switch

	# ----- Préparation des données à renvoyer -----
	# Les tracks restants sont des billes valides. On rassemble leurs points dnas une liste de dataframe.
	rows: list[pd.DataFrame] = []
	for i in range(len(active_tracks)):
		df_bead = data.loc[active_tracks[i].ids].copy()
		df_bead.insert(0, "Bead", int(i + 1))  # Ajout d'une colonne Bead avec le numéro de la bille de 1 à N.
		rows.append(df_bead)

	# if not rows: return pd.DataFrame()  # Aucune bille complète ⇒ terminé. Impossible dans ce flux

	out = pd.concat(rows, axis=0, ignore_index=False)
	# Tri stable pour lisibilité.
	return out.sort_values(by=["Bead", "Plane"], kind="stable").reset_index(drop=True)
