"""
Module contenant les fonctions de visualization pouyr palm-tracer.
"""
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

MAX_UINT16 = np.iinfo(np.uint16).max


##################################################
def get_bins_number(data: np.ndarray, limits=(30, 300)) -> int:
	"""
	Calcule un nombre de bin adaptatif pour un histogramme.

	:param data: données à analyser
	:param limits: bornes pour le nombre de bins.
	:return: nombre de bins.
	"""
	n_values = len(data)
	# bins = int(np.sqrt(n_values))				 # Règle de racine carrée
	bins = int(np.ceil(np.log2(n_values) + 1))	 # Règle de Sturges
	return max(limits[0], min(bins, limits[1]))  # Bornes pour éviter des valeurs extrêmes


##################################################
def hr_visualization(width: int, height: int, ratio: int, points: np.ndarray, normalization: bool = True) -> np.ndarray:
	"""
	Construit une image Haute résolution en fonction des éléments localisés.

	:param width: Largeur de l'image.
	:param height: Hauteur de l'image.
	:param ratio: Ratio d'aggrandissement de l'image.
	:param points: Localisations des points.
	:param normalization: Normalisation des valeurs (pour les mettre entre 0 et 65 535.
	:return: Nouvelle image.
	"""

	if ratio <= 1: return np.zeros((width, height), dtype=np.uint16)
	if width < 1 or height < 1: return np.zeros((max(int(width * ratio), 1), max(int(height * ratio), 1)), dtype=np.uint16)

	res = np.zeros((int(width * ratio), int(height * ratio)), dtype=float)

	# Filtrage des points hors des dimensions initiales
	mask = (points[:, 0] <= width) & (points[:, 1] <= height)
	points = points[mask]
	if points is None or points.size == 0 or points.shape[1] != 3: return res.astype(np.uint16)

	# Calcul des nouvelles coordonnées (vectorisé)
	coords = (points[:, :2] * ratio).astype(int)
	x, y = coords[:, 0], coords[:, 1]

	# Accumulation des valeurs (plus efficace qu'une boucle)
	np.add.at(res, (x, y), points[:, 2])

	# Normalisation ou autre pour les Z par exemple ?
	diff = res.max() - res.min()
	if normalization and diff != 0:
		res = (res - res.min()) / diff * MAX_UINT16

	res = res.clip(0, MAX_UINT16)			 # Limite les valeurs entre 0 et la valeur maximale possible pour un uint16
	return np.asarray(res, dtype=np.uint16)  # Forcer le type de l'image en np.uint16


##################################################
def plot_histogram(ax: plt.axes, data: np.ndarray, title: str, limit: bool = True, kde: bool = True, density: bool = True):
	"""
	Trace un histogramme des données avec Seaborn, et optionnellement une courbe gaussienne.

	:param ax: Axe sur lequel tracer l'histogramme.
    :param data: Données sous forme de tableau numpy.
	:param title: Titre de l'histogramme.
    :param limit: Si True, applique la règle des 3 sigmas pour limiter les données.
    :param kde: Si True, superpose une courbe gaussienne.
    :param density: Si True, normalise l'histogramme pour afficher une densité de probabilité.
	"""
	data = data.ravel()  # Convertit en un tableau 1D
	if len(data) == 0: return

	# Ajout d'un style avec Seaborn
	sns.set_style("white")

	# Limite des données avec la règle des 3 Sigmas
	if limit:
		mu, sigma = np.mean(data), np.std(data)
		if sigma == 0: return
		limits = [mu - 3 * sigma, mu + 3 * sigma]						 # Limite théoriques des datas
		data = data[(data >= limits[0]) & (data <= limits[1])]			 # Suppression des datas au dela des limites
		limits = [max(limits[0], min(data)), min(limits[1], max(data))]  # On resserre les limites autour des datas
	else:
		limits = [min(data), max(data)]

	# Tracé de l'histogramme avec Seaborn
	hist_plot = sns.histplot(data, bins=get_bins_number(data), kde=False, stat="density" if density else "count", ax=ax, alpha=0.75)

	if kde:
		kde_plot = sns.kdeplot(data, ax=ax, linestyle="--", color=sns.color_palette()[1])  # Prend la deuxième couleur de Seaborn
		if not density:
			# Adapter le KDE à l'échelle de l'histogramme (calcul du facteur d'ajustement)
			max_count = max([patch.get_height() for patch in hist_plot.patches])
			kde_scale = max_count / max(kde_plot.get_lines()[0].get_ydata())
			kde_plot.get_lines()[0].set_ydata(kde_plot.get_lines()[0].get_ydata() * kde_scale)

	ax.set_title(title)
	ax.set_xlim(limits)
	ax.set_xlabel("Values")
	ax.set_ylabel("Density" if density else "Count")


##################################################
def plot_plane_violin(ax: plt.axes, data: np.ndarray, title: str):
	"""
	Trace un graphique type violon pour les données en entrée .

	:param ax: Axe sur lequel tracer l'histogramme.
	:param data: Données à tracer sous forme de tableau numpy.
	:param title: Titre du graphique.
	"""
	if len(data) == 0: return
	sns.set_style("white")
	# Conversion des données en DataFrame pour seaborn
	df = pd.DataFrame(data, columns=["Plane", "Value"])
	sns.violinplot(x="Plane", y="Value", data=df, ax=ax, inner="quartile")

	ax.set_title(title)
	ax.set_xlabel("Planes")
	ax.set_ylabel("Density")


##################################################
def plot_plane_heatmap(ax: plt.Axes, data: np.ndarray, title: str, cmap="magma"):
	"""
	Trace une heatmap montrant la densité des valeurs par plan.

	:param ax: Axe sur lequel tracer la heatmap.
	:param data: Données sous forme de tableau numpy.
	             La première colonne représente les plans, la deuxième les valeurs.
	:param title: Titre du graphique.
	:param cmap: Color Map utilisé pour tracer la heatmap (liste des colormaps : https://matplotlib.org/stable/tutorials/colors/colormaps.html).
	"""

	if data.shape[0] == 0 or data.shape[1] < 2:    return
	sns.set_style("white")

	# Création d'un histogramme 2D pour la densité des points
	planes = data[:, 0].astype(int)  # S'assurer que les plans sont bien des entiers
	values = data[:, 1]
	n_planes = planes.max() + 1

	hist, x_edges, y_edges = np.histogram2d(planes, values, bins=[n_planes, get_bins_number(data)])

	# Tracé de la heatmap avec pcolormesh
	mesh = ax.pcolormesh(x_edges, y_edges, hist.T, shading='auto', cmap=cmap)

	# Ajout d'une barre de couleur
	plt.colorbar(mesh, ax=ax, label="Densité")

	# Paramètres du graphique
	ax.set_title(title)
	ax.set_xlabel("Planes")
	ax.set_ylabel("Values")
