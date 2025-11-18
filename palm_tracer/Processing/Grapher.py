""" Fichier contenant une classe pour Créé des graphiques. """

from dataclasses import dataclass
from typing import Optional

import numpy as np
import plotly.graph_objects as go
from scipy.stats import gaussian_kde

# Palette "deep" de seaborn (approx)
_SEABORN_DEEP = ["#4C72B0", "#55A868", "#C44E52", "#8172B2", "#CCB974", "#64B5CD", "#FFD92F", "#E7298A", "#66A61E", "#E6AB02"]
_TEMPLATE = "plotly_white"
_BLANK_ANNOTATIONS = [dict(text="No valid data.", x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False)]
_GRID_COLOR = "#e6e6e6"
_GRID_WIDTH = 0.75
_MARGIN = dict(l=60, r=20, t=60, b=50)


##################################################
@dataclass
class Grapher:
	"""Créateur de graphiques avec Plotly."""

	##################################################
	@staticmethod
	def blank(title: str):
		fig = go.Figure()
		fig.update_layout(title=title, template=_TEMPLATE, annotations=_BLANK_ANNOTATIONS)
		return fig

	##################################################
	def histogram(self, data: np.ndarray, title: str, limit: bool = False, show_sigma: bool = False, kde: bool = False, gaussian: bool = False,
				  density: bool = True, bins: Optional[int] = None) -> go.Figure:
		"""
		Trace un histogramme des données "façon" Seaborn avec Plotly et optionnellement une courbe kernel density estimation.

		:param data: Données sous forme de tableau numpy 1D/ND (aplati).
		:param title: titre du graphe.
		:param limit: Si True, applique la règle des 3 sigmas pour limiter les données (trim des outliers).
		:param show_sigma: Si True, superpose la moyenne, ±1,±2,±3 sigma.
		:param kde: Si True, superpose la KDE gaussienne.
		:param gaussian: Si True, superpose la gaussienne.
		:param density: affiche l'histogramme en densité (True) ou en comptes (False).
		:param bins: nbins explicite (sinon Sturges).
		:return: ``go.Figure``
		"""
		x = np.asarray(data).ravel()
		x = x[np.isfinite(x)]
		fig = go.Figure()

		# Aucunes données valides
		if x.size == 0:
			fig.update_layout(title=title, template=_TEMPLATE, annotations=_BLANK_ANNOTATIONS)
			return fig

		# Limite des données avec la règle des 3 Sigmas
		mu, sigma = float(np.mean(data)), float(np.std(data))
		x, limits = self.__get_range(x, limit)

		# Récupération du nombre de bin
		if bins is None: bins = self.__get_bins_number(x)

		# Histogramme
		histnorm = "probability density" if density else None
		fig.add_histogram(x=x, nbinsx=bins, histnorm=histnorm, marker=dict(color=_SEABORN_DEEP[0], line=dict(width=0)), opacity=0.75,
						  name="Histogram", hovertemplate="(%{x:.2f}, %{y:.2f})<extra></extra>")

		# KDE
		if kde and x.size > 1 and sigma > 0:
			# grille régulière sur l'intervalle affiché
			xk = np.linspace(limits[0], limits[1], 512)
			k = gaussian_kde(x)  # choisit sa propre bandwidth
			y = k(xk)
			if not density: y = y * x.size * ((limits[1] - limits[0]) / max(int(bins), 1))  # convertir la densité en comptes ~ dens * N * bin_width
			fig.add_trace(go.Scatter(x=xk, y=y, mode="lines", line=dict(dash="dash", color=_SEABORN_DEEP[1]),
									 name="KDE", hoverinfo="skip", hovertemplate=None))

		# Gaussian
		if gaussian and x.size > 1 and sigma > 0:
			# grille régulière sur l'intervalle affiché
			xg = np.linspace(limits[0], limits[1], 512)
			y = (1.0 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((xg - mu) / sigma) ** 2)
			if not density: y = y * x.size * ((limits[1] - limits[0]) / max(int(bins), 1))  # convertir la densité en comptes ~ dens * N * bin_width
			fig.add_trace(go.Scatter(x=xg, y=y, mode="lines", line=dict(dash="dash", color=_SEABORN_DEEP[2]),
									 name="Gaussian", hoverinfo="skip", hovertemplate=None))

		# Sigmas
		if show_sigma and x.size > 1 and sigma > 0:
			fig.add_vline(x=mu, line_color=_SEABORN_DEEP[3], name="μ")  # μ
			fig.add_vline(x=mu - sigma, line_color=_SEABORN_DEEP[4], line_dash="dot", name="μ - 1σ")  # -1σ
			fig.add_vline(x=mu + sigma, line_color=_SEABORN_DEEP[4], line_dash="dot", name="μ + 1σ")  # +1σ
			fig.add_vline(x=mu - 2 * sigma, line_color=_SEABORN_DEEP[5], line_dash="dot", name="μ - 2σ")  # -2σ
			fig.add_vline(x=mu + 2 * sigma, line_color=_SEABORN_DEEP[5], line_dash="dot", name="μ + 2σ")  # +2σ
			fig.add_vline(x=mu - 3 * sigma, line_color=_SEABORN_DEEP[6], line_dash="dot", name="μ - 3σ")  # -3σ
			fig.add_vline(x=mu + 3 * sigma, line_color=_SEABORN_DEEP[6], line_dash="dot", name="μ + 3σ")  # +3σ

		# Style "seaborn-like" + Espacement entre barres
		fig.update_layout(title=f"{title} (μ = {mu:.2f}, σ = {sigma:.2f})", template=_TEMPLATE, margin=_MARGIN,
						  xaxis=dict(title="Values", range=limits, zeroline=False, showgrid=True, gridcolor=_GRID_COLOR, gridwidth=_GRID_WIDTH),
						  yaxis=dict(title=("Density" if density else "Count"), zeroline=False, showgrid=True, gridcolor=_GRID_COLOR, gridwidth=_GRID_WIDTH),
						  hovermode="x", showlegend=True, bargap=0.15, bargroupgap=0.05)
		return fig

	##################################################
	def scatter(self, data: np.ndarray, title: str, limit: bool = False) -> go.Figure:
		"""
		Trace une courbe des données "façon" Seaborn avec Plotly.

		:param data: Données sous forme de tableau numpy 1D ou 2D.
		:param title: titre du graphe.
		:param limit: Si True, applique la règle des 3 sigmas pour limiter les données (trim des outliers).
		:return: ``go.Figure``
		"""
		# Déterminer x,y
		if data.ndim == 1:
			y = data[np.isfinite(data)]
			x = np.arange(y.size, dtype=float)
		elif data.ndim == 2:
			if data.shape[0] == 2: x, y = data[0, :], data[1, :]  # (2, N) -> lignes = (x, y)
			elif data.shape[1] == 2:  x, y = data[:, 0], data[:, 1]  # (N, 2) -> colonnes = (x, y)
			else: raise ValueError("data 2D doit avoir 2 lignes ou 2 colonnes (x,y).")
			mask = np.isfinite(x) & np.isfinite(y)
			x, y = x[mask], y[mask]
		else: raise ValueError("data doit être 1D ou 2D.")

		fig = go.Figure()

		if x.size == 0:
			fig.update_layout(title=title, template=_TEMPLATE, annotations=_BLANK_ANNOTATIONS)
			return fig

		# Limite des données avec la règle des 3 Sigmas
		x, limits = self.__get_range(x, limit)

		# faire une courbe style "seaborn-like"
		fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers", line=dict(color=_SEABORN_DEEP[0]), hovertemplate="x=%{x:.2f}<br>y=%{y:.2f}<extra></extra>"))

		# Style "seaborn-like" + Espacement entre barres
		fig.update_layout(title=title, template=_TEMPLATE, margin=_MARGIN,
						  xaxis=dict(range=limits, zeroline=False, showgrid=True, gridcolor=_GRID_COLOR, gridwidth=_GRID_WIDTH),
						  yaxis=dict(zeroline=False, showgrid=True, gridcolor=_GRID_COLOR, gridwidth=_GRID_WIDTH), hovermode="x", showlegend=False)
		return fig

	##################################################
	@staticmethod
	def __get_bins_number(data: np.ndarray, limits=(30, 300)) -> int:
		"""
		Calcule un nombre de bin adaptatif pour un histogramme.

		:param data: données à analyser.
		:param limits: bornes pour le nombre de bins.
		:return: nombre de bins.
		"""
		n_values = len(data)
		# bins = int(np.sqrt(n_values))				 # Règle de racine carrée
		bins = int(np.ceil(np.log2(n_values) + 1))  # Règle de Sturges
		return max(limits[0], min(bins, limits[1]))  # Bornes pour éviter des valeurs extrêmes

	##################################################
	@staticmethod
	def __get_range(data: np.ndarray, limit) -> tuple[np.ndarray, list[float]]:
		"""
		Calcule les limites du graphique avec la règle des 3 sigmas et ajuste le tableau si necessaire.

		:param data: données à analyser.
		:param limit: limite ou non les données.
		:return: le tableau (en cas de modification) et les limites du graphiques.
		"""
		mu, sigma = float(np.mean(data)), float(np.std(data))
		if limit and sigma > 0:
			limits = [mu - 3 * sigma, mu + 3 * sigma]  # Limite théoriques des datas
			data = data[(data >= limits[0]) & (data <= limits[1])]  # Suppression des datas au dela des limites
			limits = [max(limits[0], min(data)), min(limits[1], max(data))]  # On resserre les limites autour des datas
		else:
			limits = [min(data), max(data)]
		return data, limits
