"""Fonction de filtrages"""
from typing import cast

import numpy as np
import pandas as pd

from palm_tracer.Settings.Groups import Filters
from palm_tracer.Settings.Types import CheckRangeFloat, CheckRangeInt


##################################################
class Filtering:
	"""Classe de filtrages"""
	filters: Filters

	##################################################
	def __init__(self, filters: Filters): self.filters = filters

	##################################################
	def localization(self, datas: pd.DataFrame) -> pd.DataFrame:
		"""
		Filtre un DataFrame de localisation.

		:param datas: DataFrame à filtrer
		:return: :class:`DataFrame <pandas.DataFrame>` filtré.
		"""
		res = datas.copy()
		if "Integrated Intensity" in res.columns: df = res[res["Integrated Intensity"] > 0]  # Suppression des éléments où l'ajustement a échoué.
		if res.empty: return res
		fl = self.filters.localization
		filters = [[self.filters["Plane"], "Plane"],
				   [fl["X"], "X"], [fl["Y"], "Y"], [fl["Z"], "Z"],
				   [fl["Intensity"], "Integrated Intensity"],
				   [fl["Sigma X"], "Sigma X"], [fl["Sigma Y"], "Sigma Y"],
				   [fl["Theta"], "Theta"], [fl["Circularity"], "Circularity"],
				   [fl["MSE XY"], "MSE XY"], [fl["MSE Z"], "MSE Z"]]

		for filt, col in filters:
			if isinstance(filt, CheckRangeFloat | CheckRangeInt) and filt.active:
				limits = filt.value
				res = res[res[col].between(limits[0], limits[1])]  # Bornes incluses
		return res

	##################################################
	def tracking(self, datas: pd.DataFrame) -> pd.DataFrame:
		"""
		Filtre un DataFrame de trajectoires.
		Simpliste uniquement sur la longueur, car il faut le calcul des statistiques sur trajectoires pour le reste.
		Cependant, il peut s'agir d'une première étape avant, justement, ces calculs de statistiques.

		:param datas: DataFrame à filtrer
		:return: :class:`DataFrame <pandas.DataFrame>` filtré.
		"""
		res = datas.copy()
		if res.empty: return res
		f = cast(CheckRangeInt, self.filters.tracking["Length"])
		if f.active:
			limits = f.value
			counts = res.groupby("Track").size()  # .								  Comptage par trajectoire
			keep_ids = counts.index[(counts >= limits[0]) & (counts <= limits[1])]  # IDs de trajectoires gardées: min_len <= nb points <= max_len
			res = res[res["Track"].isin(keep_ids)]  # .								  Filtrage (on garde l'ordre original)
		return res

	##################################################
	def tracks_compute(self, tracks: pd.DataFrame, msd: pd.DataFrame, instant_d: pd.DataFrame,
					   fit: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
		"""
		Filtre un DataFrame de calcul sur les trajectoires.

		:param tracks: DataFrame de trajectoires
		:param msd: DataFrame de calcul des MSD
		:param instant_d: DataFrame de calcul de la diffusion instantanée
		:param fit: DataFrame de calcul de l'ajustement
		:return: DataFrames filtrés.
		"""
		o_trc = tracks.copy()
		o_msd = msd.copy()
		o_ind = instant_d.copy()
		o_fit = fit.copy()
		if o_trc.empty: return o_trc, o_msd, o_ind, o_fit

		f = self.filters.tracking

		# ----- Base : IDs présents dans les 4 DataFrames (donc une intersection) -----
		id_sets: list[set[int]] = []
		for df in (o_trc, o_msd, o_ind, o_fit):
			# évite d'ajouter un set vide qui tuerait l'intersection
			if not df.empty and "Track" in df.columns: id_sets.append(set(df["Track"].unique().tolist()))
		keep_ids = set.intersection(*id_sets)

		# ----- Filtre Longueur -----
		f_tmp = cast(CheckRangeInt, f["Length"])
		if f_tmp.active:
			limits_l = f_tmp.value
			counts = o_trc.groupby("Track").size()
			ok_len_ids = set(counts.index[(limits_l[0] <= counts) & (counts <= limits_l[1])].tolist())
			keep_ids &= ok_len_ids  # intersection sur des sets d'IDs

		# ----- Filtre sur Instant D -----
		f_tmp = cast(CheckRangeInt, f["Instant D"])
		if f_tmp.active and not o_ind.empty:
			limits_d = f_tmp.value

			o_ind = o_ind[o_ind["Track"].isin(keep_ids)]  # .					 Restreindre aux trajectoires admissibles jusqu'ici
			if not o_ind.empty:
				val_cols = [c for c in o_ind.columns if c != "Track"]  # .		 Colonnes de valeurs = toutes sauf 'Track'
				vals = o_ind[val_cols]
				vals_np = vals.to_numpy(dtype=float)  # .						 Convertir en numpy pour un contrôle fin
				finite = np.isfinite(vals_np)  # .								 Masque des valeurs finies (ni NaN, ni ±inf)
				outside = (vals_np <= limits_d[0]) | (vals_np >= limits_d[1])  # Valeurs hors bornes (sur le numpy brut)
				outside &= finite  # .											 On ne compte les "outside" que là où c'est vraiment une valeur finie
				n_valid, n_out = finite.sum(axis=1), outside.sum(axis=1)  # .	 Nombre de valeurs valides/hors bornes par ligne
				pct_out_np = np.zeros_like(n_out, dtype=float)  # .				 Pourcentage hors bornes (évite la division par 0 avec where=)
				np.divide(n_out, n_valid, out=pct_out_np, where=n_valid > 0)
				pct_out = pd.Series(pct_out_np * 100.0, index=o_ind.index)

				# avec une troisieme valeur limit[2] qui serait le pourcentage de fail max autorisé
				# Ou alors un nouveau setting type Instant D Failure Tolerance (%), je vais mettre 50% ici
				ok_ids = set(map(int, np.unique(o_ind.loc[pct_out <= 50.0, "Track"].to_numpy())))
				keep_ids &= ok_ids

		# ----- Filtre sur Fit -----
		if not o_fit.empty:
			o_fit = o_fit[o_fit["Track"].isin(keep_ids)]  # Restreindre aux trajectoires admissibles jusqu'ici
			if not o_fit.empty:
				filters = [
						# Quel que soit l'ajustement.
						[f["D Coeff"], "D(0) (μm²/s)"],
						# Fit Puissance
						[f["Alpha"], "Alpha"],
						[f["Speed"], "Average Speed (Last-First)(μm/s)"],
						# Fit Exponentiel
						[f["Confinement"], "Confinement Radius (μm)"]]

				for filt, col in filters:
					if col in o_fit.columns and isinstance(filt, CheckRangeFloat | CheckRangeInt) and filt.active:
						limits = filt.value
						o_fit = o_fit[o_fit[col].between(limits[0], limits[1])]  # Bornes incluses

				keep_ids &= set(o_fit["Track"].unique().tolist())

		# ----- Filtre final des trajectoires restantes -----
		if not o_trc.empty: o_trc = o_trc[o_trc["Track"].isin(keep_ids)]
		if not o_msd.empty: o_msd = o_msd[o_msd["Track"].isin(keep_ids)]
		if not o_ind.empty: o_ind = o_ind[o_ind["Track"].isin(keep_ids)]
		if not o_fit.empty: o_fit = o_fit[o_fit["Track"].isin(keep_ids)]
		return o_trc, o_msd, o_ind, o_fit
