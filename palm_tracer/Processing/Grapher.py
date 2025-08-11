""" Fichier contenant une classe pour Créé des graphiques. """

from dataclasses import dataclass
from typing import Optional

import numpy as np
import plotly.graph_objects as go
from scipy.stats import gaussian_kde

# Palette "deep" de seaborn (approx)
_SEABORN_DEEP = ["#4c72b0", "#55a868", "#c44e52", "#8172b2", "#ccb974", "#64b5cd"]


##################################################
@dataclass
class Grapher:
	"""Créateur de graphiques avec Plotly."""

	def histogram(self, data: np.ndarray, title: str, limit: bool = True, kde: bool = True, density: bool = True, bins: Optional[int] = None,
				  color_hist: str = _SEABORN_DEEP[0], color_kde: str = _SEABORN_DEEP[2]) -> go.Figure:
		"""
		Trace un histogramme des données "façon" Seaborn avec Plotly et optionnellement une courbe kernel density estimation.

		:param data: tableau numpy 1D/ND (aplati).
		:param title: titre du graphe.
		:param limit: règle des 3σ (trim des outliers).
		:param kde: superpose la KDE gaussienne.
		:param density: histogramme en densité (True) ou en comptes (False).
		:param bins: nbins explicite (sinon Freedman–Diaconis).
		:param color_hist: couleur de l'histogramme (seaborn deep).
		:param color_kde: couleur de la courbe KDE (seaborn deep).
		:return: go.Figure
		"""
		x = np.asarray(data).ravel()
		x = x[np.isfinite(x)]
		fig = go.Figure()

		# Aucunes données valides
		if x.size == 0:
			fig.update_layout(title=title, template="plotly_white",
							  annotations=[dict(text="Aucune donnée valide", x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False)], )
			return fig

		# Limite des données avec la règle des 3 Sigmas
		mu, sigma = float(np.mean(x)), float(np.std(x))
		if limit and sigma > 0:
			limits = [mu - 3 * sigma, mu + 3 * sigma]				   # Limite théoriques des datas
			x = x[(x >= limits[0]) & (x <= limits[1])]				   # Suppression des datas au dela des limites
			limits = [max(limits[0], min(x)), min(limits[1], max(x))]  # On resserre les limites autour des datas
		else:
			limits = [min(x), max(x)]

		# Récupération du nombre de bin
		if bins is None: bins = self._get_bins_number(x)

		# Histogramme
		histnorm = "probability density" if density else None
		fig.add_histogram(x=x, nbinsx=bins, histnorm=histnorm, marker=dict(color=color_hist, line=dict(width=0)), opacity=0.75,
						  name="Histogram", hovertemplate=("x=%{x:.2f}<br>" + ("density=%{y:.2f}" if density else "count=%{y}") + "<extra></extra>"))

		# KDE
		if kde and x.size > 1 and sigma > 0:
			# grille régulière sur l'intervalle affiché
			grid = np.linspace(limits[0], limits[1], 512)
			gkde = gaussian_kde(x)  # choisit sa propre bandwidth
			y = gkde(grid)
			if not density:
				# convertir la densité en comptes ~ dens * N * bin_width
				bin_width = (limits[1] - limits[0]) / max(int(bins), 1)
				y = y * x.size * bin_width

			fig.add_trace(go.Scatter(x=grid, y=y, mode="lines", line=dict(dash="dash", width=2, color=color_kde),
									 name="KDE", hovertemplate="x=%{x:.2f}<br>y=%{y:.2f}<extra></extra>"))

		# Style "seaborn-like" + Espacement entre barres
		fig.update_layout(title=title, template="plotly_white", margin=dict(l=60, r=20, t=60, b=50),
						  xaxis=dict(title="Values", range=limits, zeroline=False, showgrid=True, gridcolor="#e6e6e6", gridwidth=0.8),
						  yaxis=dict(title=("Density" if density else "Count"), zeroline=False, showgrid=True, gridcolor="#e6e6e6", gridwidth=0.8),
						  hovermode="x", showlegend=True, bargap=0.15, bargroupgap=0.05)
		return fig

	def scatter(self, data: np.ndarray, title: str, limit: bool = True, color: str = _SEABORN_DEEP[0]) -> go.Figure:
		"""
		Trace une courbe des données "façon" Seaborn avec Plotly.

		:param data: tableau numpy 1D ou 2D.
		:param title: titre du graphe.
		:param limit: règle des 3σ (trim des outliers).
		:param color: couleur de la courbe (seaborn deep).
		:return: go.Figure
		"""
		# Déterminer x,y
		if data.ndim == 1:
			y = data[np.isfinite(data)]
			x = np.arange(y.size, dtype=float)
		elif data.ndim == 2:
			if data.shape[0] == 2:  # (2, N) -> lignes = (x, y)
				x = data[0, :]
				y = data[1, :]
			elif data.shape[1] == 2:  # (N, 2) -> colonnes = (x, y)
				x = data[:, 0]
				y = data[:, 1]
			else: raise ValueError("data 2D doit avoir 2 lignes ou 2 colonnes (x,y).")
			mask = np.isfinite(x) & np.isfinite(y)
			x = x[mask]
			y = y[mask]
		else: raise ValueError("data doit être 1D ou 2D.")

		fig = go.Figure()

		if x.size == 0:
			fig.update_layout(title=title, template="plotly_white",
							  annotations=[dict(text="Aucune donnée valide", x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False)], )
			return fig

		# Limite des données avec la règle des 3 Sigmas
		mu, sigma = float(np.mean(x)), float(np.std(x))
		if limit and sigma > 0:
			limits = [mu - 3 * sigma, mu + 3 * sigma]				   # Limite théoriques des datas
			x = x[(x >= limits[0]) & (x <= limits[1])]				   # Suppression des datas au dela des limites
			limits = [max(limits[0], min(x)), min(limits[1], max(x))]  # On resserre les limites autour des datas
		else:
			limits = [min(x), max(x)]

		# faire une courbe style "seaborn-like"
		fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers", line=dict(color=color), hovertemplate="x=%{x:.2f}<br>y=%{y:.2f}<extra></extra>"))

		# Style "seaborn-like" + Espacement entre barres
		fig.update_layout(title=title, template="plotly_white", margin=dict(l=60, r=20, t=60, b=50),
						  xaxis=dict(range=limits, zeroline=False, showgrid=True, gridcolor="#e6e6e6", gridwidth=0.8),
						  yaxis=dict(zeroline=False, showgrid=True, gridcolor="#e6e6e6", gridwidth=0.8), hovermode="x", showlegend=True)
		return fig

	@staticmethod
	def _get_bins_number(data: np.ndarray, limits=(30, 300)) -> int:
		"""
		Calcule un nombre de bin adaptatif pour un histogramme.

		:param data: données à analyser
		:param limits: bornes pour le nombre de bins.
		:return: nombre de bins.
		"""
		n_values = len(data)
		# bins = int(np.sqrt(n_values))				 # Règle de racine carrée
		bins = int(np.ceil(np.log2(n_values) + 1))   # Règle de Sturges
		return max(limits[0], min(bins, limits[1]))  # Bornes pour éviter des valeurs extrêmes
