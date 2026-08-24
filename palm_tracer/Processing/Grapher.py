"""Construit les figures Plotly utilisées pour visualiser les données PALM."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional

import numpy as np
import plotly.graph_objects as go
from scipy.stats import expon, gaussian_kde, multivariate_normal, poisson

from palm_tracer.Processing.Astigmatism3D import sigma_model
from palm_tracer.Processing.Parsing import SHAPE_MODEL

# Palette "deep" de seaborn (approx)
_SEABORN_DEEP = ["#4C72B0", "#55A868", "#C44E52", "#8172B2", "#CCB974", "#64B5CD", "#FFD92F", "#E7298A", "#66A61E", "#E6AB02"]
_TEMPLATE = "plotly_white"
_BLANK_ANNOTATIONS = [dict(text="No valid data.", x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False)]
_GRID_COLOR = "#e6e6e6"
_GRID_WIDTH = 0.75
_MARGIN = dict(l=60, r=30, t=60, b=50)
MESH_SIZE = 128


##################################################
@dataclass
class Grapher:
	"""
	Construit les figures Plotly utilisées pour explorer les résultats PALM.

	Les méthodes statiques produisent les histogrammes, distributions, nuages de points et autres représentations sans conserver d'état entre les appels.
	"""

	# ==================================================
	# region Statistic Figure
	# ==================================================
	##################################################
	@staticmethod
	def blank(title: str = "") -> go.Figure:
		"""
		Créé une figure vide avec une annotation standard au centre ``_BLANK_ANNOTATIONS``.

		:param title: Titre de la figure.
		:return: :class:`go.Figure <plotly.graph_objects.Figure>` Figure avec l'annotation.
		"""
		fig = go.Figure()
		fig.update_layout(title=title, template=_TEMPLATE, annotations=_BLANK_ANNOTATIONS, margin=_MARGIN)
		return fig

	##################################################
	def histogram(self, data: np.ndarray, title: str = "", xlabel: str = "", ylabel: str = "", limit: bool = False,
				  show_sigma: bool = False, kde: bool = False, gaussian: bool = False, poissonian: bool = False, exponential: bool = False,
				  density: bool = True, cumulative: bool = False, bins: int = 0) -> go.Figure:
		"""
		Trace un histogramme des données "façon" Seaborn avec Plotly et optionnellement une courbe kernel density estimation.

		:param data: Données sous forme de tableau NumPy 1D/ND (aplati).
		:param title: Titre du graphe.
		:param xlabel: Label optionnel pour l'axe X. Si la chaîne est vide, ne change rien.
		:param ylabel: Label optionnel pour l'axe Y. Si la chaîne est vide, ne change rien.
		:param limit: Si True, applique la règle des 3 sigmas pour limiter les données (trim des outliers).
		:param show_sigma: Si True, superpose la moyenne, ±1,±2,±3 sigmas.
		:param kde: Si True, superpose la KDE gaussienne.
		:param gaussian: Si True, superpose la gaussienne.
		:param poissonian: Si True, superpose la poissonnienne.
		:param exponential: Si True, superpose l'exponentielle inverse.
		:param density: Affiche l'histogramme en densité (True) ou en compte (False).
		:param bins: Nombre de bins explicite (Sturges si 0 et avec des valeurs entières si négatif).
		:param cumulative: Si True, affiche l'histogramme cumulé ainsi que les courbes KDE / gaussienne en version cumulée.
		:return: :class:`go.Figure <plotly.graph_objects.Figure>`.
		"""
		if data.ndim == 2:  # On considère la première ligne/colonne comme l'identifiant/compteur pour la valeur d'intérêt
			if data.shape[0] == 2: _, x = data[0, :], data[1, :]  # .  (2, N) -> lignes = (x, y)
			elif data.shape[1] == 2:  _, x = data[:, 0], data[:, 1]  # (N, 2) -> colonnes = (x, y)
			else: x = np.asarray(data).ravel()
		else: x = np.asarray(data).ravel()

		x = x[np.isfinite(x)]
		# Aucunes données valides
		if x.size == 0: return self.blank(title)

		fig = go.Figure()

		# Limite des données avec la règle des 3 Sigmas
		x, limits, mu, sigma = self._get_range(x, limit)

		# Récupération du nombre de bin
		if bins == 0: bins = self._get_bins_number(x)
		bin_width = (limits[1] - limits[0]) / max(int(bins), 1)
		if bins < 0:
			bin_width = 1
			limits[0] -= 0.5
			limits[1] += 0.5

		# Histogramme
		histnorm = "probability density" if density else None
		fig.add_histogram(x=x, xbins=dict(start=limits[0], end=limits[1], size=bin_width), histnorm=histnorm,
						  cumulative=dict(enabled=cumulative), marker=dict(color=_SEABORN_DEEP[0], line=dict(width=0)),
						  opacity=0.75, name="Histogram", hovertemplate="(%{x:.2f}, %{y:.2f})<extra></extra>")

		# KDE
		if x.size > 1 and sigma > 0:
			x_grid = np.linspace(limits[0], limits[1], MESH_SIZE)  # grille régulière sur l'intervalle affiché

			# Estimation par noyau
			if kde:
				kde_model = gaussian_kde(x)  # choisit sa propre bandwidth
				y_pdf = kde_model(x_grid)
				y = self._scale_curve(x_grid, y_pdf, x.size, bin_width, density, cumulative)
				fig.add_trace(go.Scatter(x=x_grid, y=y, mode="lines", line=dict(dash="dash", color=_SEABORN_DEEP[1]),
										 name="KDE", hoverinfo="skip", hovertemplate=None))

			# Gaussienne
			if gaussian:
				y_pdf = (1.0 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_grid - mu) / sigma) ** 2)
				y = self._scale_curve(x_grid, y_pdf, x.size, bin_width, density, cumulative)
				fig.add_trace(go.Scatter(x=x_grid, y=y, mode="lines", line=dict(dash="dash", color=_SEABORN_DEEP[2]),
										 name="Gaussian", hoverinfo="skip", hovertemplate=None))

			# Poissonnienne
			if poissonian and mu >= 0:
				x_poisson = np.arange(max(0, int(np.floor(limits[0]))), int(np.ceil(limits[1])) + 1)
				y_pdf = poisson.pmf(x_poisson, mu)
				y = self._scale_curve(x_poisson, y_pdf, x.size, bin_width, density, cumulative, discrete=True)
				fig.add_trace(go.Scatter(x=x_poisson, y=y, mode="lines", line=dict(dash="dash", color=_SEABORN_DEEP[3]),
										 name="Poisson", hoverinfo="skip", hovertemplate=None))

			# Exponentielle
			if exponential and mu > 0:
				x_exponential = x_grid[x_grid >= 0]
				y_pdf = expon.pdf(x_exponential, scale=mu)
				y = self._scale_curve(x_exponential, y_pdf, x.size, bin_width, density, cumulative)
				fig.add_trace(go.Scatter(x=x_exponential, y=y, mode="lines", line=dict(dash="dash", color=_SEABORN_DEEP[4]),
										 name="Exponential", hoverinfo="skip", hovertemplate=None))

		# Mu et Sigmas
		if show_sigma and x.size > 1 and sigma > 0: self._draw_sigma(fig, mu, sigma, True)

		# Style "seaborn-like" + Espacement entre barres
		xlabel = "Values" if xlabel == "" else xlabel
		ylabel = ("Density" if density else "Count") if ylabel == "" else ylabel
		fig.update_layout(title=f"{title} (μ = {mu:.2f}, σ = {sigma:.2f})", template=_TEMPLATE, margin=_MARGIN,
						  xaxis=self._axis_dict(xlabel, limits), yaxis=self._axis_dict(ylabel),
						  hovermode="x", showlegend=True, bargap=0.15, bargroupgap=0.05)
		return fig

	##################################################
	def scatter(self, data: np.ndarray, title: str = "", xlabel: str = "", ylabel: str = "", limit: bool = False, show_sigma: bool = False) -> go.Figure:
		"""
		Trace une courbe des données "façon" Seaborn avec Plotly.

		:param data: Données sous forme de tableau NumPy 1D ou 2D.
		:param title: Titre du graphe.
		:param xlabel: Label optionnel pour l'axe X. Si la chaîne est vide, ne change rien.
		:param ylabel: Label optionnel pour l'axe Y. Si la chaîne est vide, ne change rien.
		:param limit: Si True, applique la règle des 3 sigmas pour limiter les données (trim des outliers).
		:param show_sigma: Si True, superpose la moyenne, ±1,±2,±3 sigmas.
		:return: :class:`go.Figure <plotly.graph_objects.Figure>`.
		:raises ValueError: Si les dimensions du tableau ne correspondent pas à ceux attendus (1D, 2D, mais avec uniquement 2 lignes ou 2 colonnes)
		"""

		# Déterminer x,y
		if data.ndim == 1:
			y = data[np.isfinite(data)]
			x = np.arange(y.size, dtype=float)
		elif data.ndim == 2:
			if data.shape[0] == 2: x, y = data[0, :], data[1, :]  # .  (2, N) -> lignes = (x, y)
			elif data.shape[1] == 2:  x, y = data[:, 0], data[:, 1]  # (N, 2) -> colonnes = (x, y)
			else: raise ValueError("data 2D doit avoir 2 lignes ou 2 colonnes (x,y).")
			mask = np.isfinite(x) & np.isfinite(y)
			x, y = x[mask], y[mask]
		else: raise ValueError("data doit être 1D ou 2D.")

		# Aucunes données valides
		if x.size == 0: return self.blank(title)

		fig = go.Figure()

		# Limite des données avec la règle des 3 Sigmas
		_, limits, mu, sigma = self._get_range(y, limit)

		# faire une courbe style "seaborn-like"
		fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers", line=dict(color=_SEABORN_DEEP[0]), hovertemplate="x=%{x:.2f}<br>y=%{y:.2f}<extra></extra>"))

		# Mu et Sigmas
		if show_sigma and x.size > 1 and sigma > 0: self._draw_sigma(fig, mu, sigma, False)

		# Style "seaborn-like" + Espacement entre barres
		fig.update_layout(title=title, template=_TEMPLATE, margin=_MARGIN, xaxis=self._axis_dict(xlabel), yaxis=self._axis_dict(ylabel, limits),
						  hovermode="closest", showlegend=False)

		return fig

	##################################################
	def cloud(self, data: np.ndarray, title: str = "", xlabel: str = "", ylabel: str = "", limit: bool = False, show_sigma: bool = False,
			  kde: bool = False, gaussian: bool = False, poissonian: bool = False, exponential: bool = False) -> go.Figure:
		"""
		Trace une courbe des données "façon" Seaborn avec Plotly.

		:param data: Données sous forme de tableau NumPy 1D ou 2D.
		:param title: Titre du graphe.
		:param xlabel: Label optionnel pour l'axe X. Si la chaîne est vide, ne change rien.
		:param ylabel: Label optionnel pour l'axe Y. Si la chaîne est vide, ne change rien.
		:param limit: Si True, applique la règle des 3 sigmas pour limiter les données (trim des outliers).
		:param show_sigma: Si True, superpose la moyenne, ±1,±2,±3 sigmas.
		:param kde: Si True, superpose la KDE gaussienne 2D.
		:param gaussian: Si True, superpose la gaussienne 2D.
		:param poissonian: Si True, superpose la poissonnienne 2D.
		:param exponential: Si True, superpose l'exponentielle inverse 2D.
		:return: :class:`go.Figure <plotly.graph_objects.Figure>`.
		:raises ValueError: Si les dimensions du tableau ne correspondent pas à ceux attendus (1D, 2D, mais avec uniquement 2 lignes ou 2 colonnes)
		"""

		if data.size == 0: return self.blank(title)
		if data.ndim == 2:
			if data.shape[0] != 2:
				if data.shape[1] == 2:  data = data.T  # (N, 2) => passage en mode ligne
				else: raise ValueError("data doit avoir 2 lignes ou 2 colonnes (x,y).")
			mask = np.isfinite(data[0, :]) & np.isfinite(data[1, :])
			data = data[:, mask]
			x, y = data[0, :], data[1, :]
		else: raise ValueError("data doit être 2D.")

		# Aucunes données valides
		if data.size == 0: return self.blank(title)

		fig = go.Figure()

		# Test d'histogramme en heatmap de fond
		# fig.add_trace(go.Histogram2d(x=x, y=y, nbinsx=self._get_bins_number(x), nbinsy=self._get_bins_number(y), colorscale="Viridis", showscale=True,
		# 							 opacity=0.5, name="Histogramm", hoverinfo="skip", hovertemplate=None))

		# Limite des données avec la règle des 3 Sigmas
		_, limits_x, mu_x, sigma_x = self._get_range(x, limit)
		_, limits_y, mu_y, sigma_y = self._get_range(y, limit)

		if x.size > 1 and sigma_x > 0 and sigma_y > 0:
			if kde:
				xg, yg = np.linspace(limits_x[0], limits_x[1], MESH_SIZE), np.linspace(limits_y[0], limits_y[1], MESH_SIZE)
				xm, ym = np.meshgrid(xg, yg)

				k = gaussian_kde(np.vstack([x, y]))  # 2D KDE
				z = k(np.vstack([xm.ravel(), ym.ravel()])).reshape(MESH_SIZE, MESH_SIZE)

				fig.add_trace(go.Heatmap(x=xg, y=yg, z=z, colorscale="Viridis", opacity=0.5, name="KDE", hoverinfo="skip", hovertemplate=None))

			if gaussian:
				mu, cov = np.array([mu_x, mu_y]), np.cov(np.vstack([x, y]))
				xg, yg = np.linspace(limits_x[0], limits_x[1], MESH_SIZE), np.linspace(limits_y[0], limits_y[1], MESH_SIZE)
				xm, ym = np.meshgrid(xg, yg)

				rv = multivariate_normal(mean=mu, cov=cov, allow_singular=True)
				z = rv.pdf(np.dstack([xm, ym]))

				fig.add_trace(go.Heatmap(x=xg, y=yg, z=z, colorscale="Viridis", opacity=0.5, name="Gaussian", hoverinfo="skip", hovertemplate=None))

			if poissonian and mu_x >= 0 and mu_y >= 0:
				xg = np.arange(max(0, int(np.floor(limits_x[0]))), int(np.ceil(limits_x[1])) + 1, )
				yg = np.arange(max(0, int(np.floor(limits_y[0]))), int(np.ceil(limits_y[1])) + 1, )

				zx = poisson.pmf(xg, mu_x)
				zy = poisson.pmf(yg, mu_y)
				z = np.outer(zy, zx)

				fig.add_trace(go.Heatmap(x=xg, y=yg, z=z, colorscale="Viridis", opacity=0.5, name="Poisson", hoverinfo="skip", hovertemplate=None))

			if exponential and mu_x > 0 and mu_y > 0:
				xg = np.linspace(max(0.0, limits_x[0]), limits_x[1], MESH_SIZE)
				yg = np.linspace(max(0.0, limits_y[0]), limits_y[1], MESH_SIZE)

				zx = expon.pdf(xg, scale=mu_x)
				zy = expon.pdf(yg, scale=mu_y)
				z = np.outer(zy, zx)

				fig.add_trace(go.Heatmap(x=xg, y=yg, z=z, colorscale="Viridis", opacity=0.5, name="Exponential", hoverinfo="skip", hovertemplate=None))

		fig.add_trace(go.Scattergl(x=x, y=y, mode="markers", marker=dict(size=4, color=_SEABORN_DEEP[0]), opacity=0.75, name="Data",
								   hovertemplate="x=%{x:.2f}<br>y=%{y:.2f}<extra></extra>"))

		# Mu et Sigmas sur X
		if show_sigma and x.size > 1 and sigma_x > 0: self._draw_sigma(fig, mu_x, sigma_x, False)
		if show_sigma and y.size > 1 and sigma_y > 0: self._draw_sigma(fig, mu_y, sigma_y, True)

		# Style "seaborn-like" + Espacement entre barres
		fig.update_layout(title=title, template=_TEMPLATE, margin=_MARGIN, xaxis=self._axis_dict(xlabel, limits_x), yaxis=self._axis_dict(ylabel, limits_y),
						  hovermode="closest", showlegend=False)

		return fig

	# ==================================================
	# endregion Statistic Figure
	# ==================================================

	# ==================================================
	# region Astigmtism Figure
	# ==================================================
	##################################################
	def astigmatism3d(self, model: np.ndarray, data: np.ndarray | None = None, title: str = "", pixel_size: float = 160, z_max: float = 500,
					  mode: Literal["curve", "cross", "slope"] = "curve", n_points: int = 5000) -> go.Figure:
		"""
		Affiche la courbe d’astigmatisme 3D (σx, σy) issue d’un modèle analytique.

		Trois modes de visualisation sont disponibles :

		- ``"curve"`` : Représentation paramétrique (σx(z), σy(z)) dans le plan (σX, σY), colorée par la profondeur Z.
		- ``"cross"`` : Courbes σx(z) et σy(z) en fonction de Z.
		- ``"slope"`` : Courbe de la différence σx(z) - σy(z), utile pour estimer la monotonie et la sensibilité du modèle autour de Z = 0.

		Si des données expérimentales sont fournies, elles sont superposées sous forme de points (sans interaction hover)
		dans les modes ``"cross"`` et ``"slope"``.

		:param model: Modèle astigmatique de forme (2, 5) : paramètres X puis Y, chaque ligne = [Z0, W, C3, C4, A].
		:param data: Données expérimentales optionnelles de forme (N, 3) : ``[σx, σy, Z]``.
		:param title: Titre du graphe.
		:param pixel_size: Taille du pixel dans les mêmes unités que Z (ex. nm). Utilisé pour l’évaluation du modèle.
		:param z_max: Valeur maximale (en valeur absolue) de l’intervalle Z : :math:`Z \\in [-z_{max}, z_{max}]`.
		:param mode: Mode de visualisation : ``"curve"`` : σX vs σY (paramétré par Z), ``"cross"`` : σX(Z) et σY(Z), ``"slope"`` : σX(Z) - σY(Z).
		:param n_points: Nombre de points utilisés pour échantillonner la courbe. Plus la valeur est élevée, plus la courbe est lisse (coût négligeable).
		:return: Objet Plotly :class:`go.Figure <plotly.graph_objects.Figure>` prêt à être affiché.
		:raises ValueError: Si les dimensions du modèle ne correspondent pas à celles attendues (2x5).
		"""
		if model.shape != SHAPE_MODEL:
			raise ValueError(f"Le modèle doit être de dimension {SHAPE_MODEL}.")

		fig = go.Figure()

		z = np.linspace(-z_max, z_max, n_points, dtype=np.float64)
		sx = sigma_model(model[0], z, pixel_size, 1)
		sy = sigma_model(model[1], z, pixel_size, 1)

		if mode == "curve":
			fig.add_trace(go.Scatter(x=sx, y=sy, customdata=z,
									 mode="markers", marker=dict(size=6, color=z, colorscale="Viridis", colorbar=dict(title="Z (nm)"), showscale=True),
									 hovertemplate="σ(x:%{x:.3f}, y:%{y:.3f}) = %{customdata:.0f} nm<extra></extra>"))

			fig.update_layout(xaxis=self._axis_dict("σX"), yaxis=self._axis_dict("σY"))
		elif mode == "cross":
			fig.add_trace(go.Scatter(x=z, y=sx, mode="lines", line=dict(color=_SEABORN_DEEP[0]), hovertemplate="σx(%{x:.3f})=%{y:.3f}<extra></extra>"))
			fig.add_trace(go.Scatter(x=z, y=sy, mode="lines", line=dict(color=_SEABORN_DEEP[1]), hovertemplate="σy(%{x:.3f})=%{y:.3f}<extra></extra>"))

			if data is not None:
				x, y, z = data.T
				fig.add_trace(go.Scatter(x=z, y=x, mode="markers", marker=dict(color=_SEABORN_DEEP[0], size=6, symbol="circle"), hoverinfo="skip"))
				fig.add_trace(go.Scatter(x=z, y=y, mode="markers", marker=dict(color=_SEABORN_DEEP[1], size=6, symbol="circle"), hoverinfo="skip"))

			fig.update_layout(xaxis=self._axis_dict("Z (nm)"), yaxis=self._axis_dict("σX/Y"))
		elif mode == "slope":
			fig.add_trace(go.Scatter(x=z, y=sx - sy, mode="lines", line=dict(color=_SEABORN_DEEP[0]), hovertemplate="σx-σy(%{x:.3f})=%{y:.3f}<extra></extra>"))

			if data is not None:
				x, y, z = data.T
				fig.add_trace(go.Scatter(x=z, y=x - y, mode="markers", marker=dict(color=_SEABORN_DEEP[0], size=6, symbol="circle"), hoverinfo="skip"))

			fig.update_layout(xaxis=self._axis_dict("Z (nm)"), yaxis=self._axis_dict("σX - σY"))

		fig.update_layout(title=title, template=_TEMPLATE, margin=_MARGIN, hovermode="closest", showlegend=False)
		return fig

	# ==================================================
	# endregion Astigmtism Figure
	# ==================================================

	# ==================================================
	# region Tools
	# ==================================================
	##################################################
	@staticmethod
	def _get_bins_number(data: np.ndarray, limits=(30, 300)) -> int:
		"""
		Calcule un nombre de bin adaptatif pour un histogramme.

		:param data: Données à analyser.
		:param limits: Bornes pour le nombre de bins.
		:return: Nombre de bins.
		"""
		n_values = len(data)
		# bins = int(np.sqrt(n_values))				 # Règle de racine carrée
		bins = int(np.ceil(np.log2(n_values) + 1))  # .Règle de Sturges
		return max(limits[0], min(bins, limits[1]))  # Bornes pour éviter des valeurs extrêmes

	##################################################
	@staticmethod
	def _get_range(data: np.ndarray, limit: bool) -> tuple[np.ndarray, list[float], float, float]:
		"""
		Calcule les limites du graphique avec la règle des 3 sigmas et ajuste le tableau si nécessaire.

		:param data: Données à analyser.
		:param limit: Limite ou non les données.
		:return: Le tableau (en cas de modification) et les limites du graphique.
		"""
		mu, sigma = float(np.mean(data)), float(np.std(data))
		if limit and sigma > 0:
			limits = [mu - 3 * sigma, mu + 3 * sigma]  # .											 Limite théoriques des datas
			data = data[(data >= limits[0]) & (data <= limits[1])]  # .								 Suppression des datas au dela des limites
			limits = [max(limits[0], float(np.min(data))), min(limits[1], float(np.max(data))), ]  # On resserre les limites autour des datas
		else:
			limits = [float(np.min(data)), float(np.max(data))]
		return data, limits, mu, sigma

	##################################################
	@staticmethod
	def _scale_curve(x_grid: np.ndarray, y_pdf: np.ndarray, n: int, bin_width: float, density: bool = False, cumulative: bool = False, discrete: bool = False):
		"""
		Adapte une courbe PDF pour l'affichage selon les modes densité / comptes et normal / cumulé.

		:param x_grid: Abscisses régulières.
		:param y_pdf: Densité (PDF) ou masse de probabilité (PMF) à convertir.
		:param n: Nombre de données.
		:param bin_width: Largeur d'une bin de l'histogramme.
		:param density: Affiche l'histogramme en densité (True) ou en compte (False).
		:param cumulative: Si True, calcule la version cumulée de la courbe.
		:param discrete: Si True, considère ``y_pdf`` comme une PMF discrète.
		:return: Courbe prête à être affichée.
		"""
		if cumulative:
			if discrete: y = np.cumsum(y_pdf)
			else:
				dx = float(x_grid[1] - x_grid[0])
				y = np.cumsum(y_pdf) * dx

			# Protection contre les erreurs numériques et la troncature de la plage.
			if y.size > 0 and y[-1] > 0: y /= y[-1]
			y = np.clip(y, 0.0, 1.0)

			return y if density else y * n  # Conversion densité ⇾ comptes approximatifs.
		if density: return y_pdf  # Non cumulatif et densité, aucune mise à l'échelle
		return y_pdf * n if discrete else y_pdf * n * bin_width  # convertir la densité en comptes ~ dens * N * bin_width

	##################################################
	@staticmethod
	def _draw_sigma(fig, mu, sigma, x_axis: bool = True):
		"""
		Ajoute les séparations entre chaque sigma.

		:param fig: Figure à modifier.
		:param mu: Moyenne.
		:param sigma: Écart-type.
		:param x_axis: ``True`` pour des séparations verticales sur l'axe X, ``False`` sinon.
		"""
		params = [[mu, _SEABORN_DEEP[3], "μ"],
				  [mu - sigma, _SEABORN_DEEP[4], "μ - 1σ"], [mu + sigma, _SEABORN_DEEP[4], "μ + 1σ"],
				  [mu - 2 * sigma, _SEABORN_DEEP[5], "μ - 2σ"], [mu + 2 * sigma, _SEABORN_DEEP[5], "μ + 2σ"],
				  [mu - 3 * sigma, _SEABORN_DEEP[6], "μ - 3σ"], [mu + 3 * sigma, _SEABORN_DEEP[6], "μ + 3σ"]]
		if x_axis:
			for p in params: fig.add_vline(x=p[0], line_color=p[1], line_dash="dot", line_width=1.5, name=p[2])
		else:
			for p in params: fig.add_hline(y=p[0], line_color=p[1], line_dash="dot", line_width=1.5, name=p[2])

	##################################################
	@staticmethod
	def _axis_dict(title: str, limits: Optional[list] = None) -> dict:
		"""
		Construit la configuration commune d'un axe Plotly.

		:param title: Titre de l'axe.
		:param limits: Bornes de l'axe.
		:return: Configuration de l'axe Plotly.
		"""
		return dict(title=title, range=limits, zeroline=False, showgrid=True, gridcolor=_GRID_COLOR, gridwidth=_GRID_WIDTH)
