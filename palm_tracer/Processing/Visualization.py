"""
Module contenant les fonctions de visualization pouyr palm-tracer.
"""
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

##################################################
def hr_visualization(width: int, height: int, ratio: int, points: np.ndarray) -> np.ndarray:
	"""
	Construit une image Haute résolution en fonction des éléments localisés.

	:param width: Largeur de l'image.
	:param height: Hauteur de l'image.
	:param ratio: Ratio d'aggrandissement de l'image.
	:param points: Localisations des points.
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

	res = res.clip(0, np.iinfo(np.uint16).max)  # Limite les valeurs entre 0 et la valeur maximale possible pour un uint16
	return np.asarray(res, dtype=np.uint16)		# Forcer le type de l'image en np.uint16


##################################################
def plot_histogram(ax: plt.axes, data: np.ndarray, title: str, limit: bool = True, gaussian: bool = True):
	"""
	Trace un histogramme pour les données en entrée en utilisant la méthode des "3 sigma" pour supprimer les valeurs extrêmes.
	:param ax: Axe sur lequel tracer l'histogramme.
	:param data: Données à tracer sous forme de tableau numpy.
	:param title: Titre de l'histogramme.
	:param limit: Ajoute une limite avec la règle des 3 sigmas.
	:param gaussian: Trace une gaussienne sur l'histogramme.
	"""
	if len(data) == 0: return
	mu, sigma = np.mean(data), np.std(data)
	if sigma == 0: return

	# Ajout d'un style avec Seaborn
	sns.set_style("white")

	# Limite des données avec la règle des 3 Sigmas
	if limit:
		limits = [mu - 3 * sigma, mu + 3 * sigma]						 # Limite théoriques des datas
		data = data[(data >= limits[0]) & (data <= limits[1])]			 # Suppression des datas au dela des limites
		limits = [max(limits[0], min(data)), min(limits[1], max(data))]  # On resserre les limites autour des datas
	else:
		limits = [min(data), max(data)]

	_, _, _ = ax.hist(data, bins=30, alpha=0.75, density=True)
	ax.set_title(title)
	ax.set_xlim(limits)
	ax.set_xlabel("Values")
	ax.set_ylabel("Density")

	# Ajout d'une courbe gaussienne
	if gaussian:
		x = np.linspace(limits[0], limits[1], 100)
		ax.plot(x, 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-(x - mu) ** 2 / (2 * sigma ** 2)), linestyle="--")
