"""Module contenant les fonctions de visualisation."""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

MAX_UI_16 = np.iinfo(np.uint16).max
MAX_UI_8 = np.iinfo(np.uint8).max
SCALE = MAX_UI_16 / 8  # Échelle cible de normalization (permet une résolution de superposition de points de 8 fois)


##################################################
def normalize_data(data: np.ndarray, scale: int = SCALE) -> np.ndarray:
	"""
	Normalisation des données avec prise en compte de l'ordre de grandeur et adaptation des plages.

	Règles :
		- Si toutes les valeurs sont dans `[0,1]`, normalisation vers `[0, SCALE]`.
		- Si valeurs négatives et positives, on prend la puissance de 2 la plus proche de ``max(abs(min), abs(max))`` et on transpose vers `[0, SCALE]`.
		- Colonne uniforme : on force une valeur constante de ``SCALE``.
		- Si toutes les valeurs sont positives, on considère 0 comme min et on normalise avec la puissance de 2 la plus proche du max.

	:param data: Données à normaliser.
	:param scale: échelle de normalisation
	:return: Données normalisées.
	"""
	if data is None or data.size == 0: return np.zeros_like(data)
	min_val, max_val = data.min(), data.max()

	# Cas 1 : Colonne uniforme (toutes les valeurs identiques)
	if min_val == max_val: return np.full_like(data, scale)

	# Cas 2 : Valeurs entre 0 et 1
	if min_val >= 0 and max_val <= 1: return scale * data

	# Cas 3 : Valeurs négatives et positives -> on centre autour de 0
	if min_val < 0 < max_val:
		bound = 2 ** np.ceil(np.log2(max(abs(min_val), abs(max_val))))
		return (scale / (2 * bound)) * (data + bound)

	# Cas 4 : Valeurs positives -> on prend 0 comme min et on ajuste avec la puissance de 2 la plus proche du max
	bound = 2 ** np.ceil(np.log2(max_val))
	return (scale / bound) * data


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
	bins = int(np.ceil(np.log2(n_values) + 1))  # .Règle de Sturges
	return max(limits[0], min(bins, limits[1]))  # Bornes pour éviter des valeurs extrêmes


##################################################
def render_hr_image(width: int, height: int, ratio: int, points: np.ndarray, normalization: bool = True) -> np.ndarray:
	"""
	Construit une image Haute résolution en fonction des éléments localisés.

	:param width: Largeur de l'image.
	:param height: Hauteur de l'image.
	:param ratio: Ratio d'aggrandissement de l'image.
	:param points: Localisations des points.
	:param normalization: Normalisation des valeurs (pour les mettre entre `0` et `SCALE`).
	:return: Nouvelle image en uint16 de forme (height*ratio, width*ratio).
	"""

	if ratio < 1: return np.zeros((height, width), dtype=np.uint16)
	if width < 1 or height < 1: return np.zeros((max(int(height * ratio), 1), max(int(width * ratio), 1)), dtype=np.uint16)

	res = np.zeros((int(height * ratio), int(width * ratio)), dtype=float)

	# Filtrage des points hors des dimensions initiales
	mask = (points[:, 0] < width) & (points[:, 1] < height)
	points = points[mask]
	if points is None or points.size == 0 or points.shape[1] != 3: return res.astype(np.uint16)

	# Calcul des nouvelles coordonnées (vectorisé)
	coords = np.round(points[:, :2] * ratio).astype(int)
	x, y = coords[:, 0], coords[:, 1]

	values = normalize_data(points[:, 2]) if normalization else points[:, 2]

	np.add.at(res, (y, x), values)  # .		   Accumulation des valeurs (plus efficace qu'une boucle)
	res = res.clip(0, MAX_UI_16)  # .		   Limite les valeurs entre 0 et la valeur maximale possible pour un uint16
	return np.asarray(res, dtype=np.uint16)  # Forcer le type de l'image en np.uint16


##################################################
def render_tracks_image(width: int, height: int, ratio: int, tracks: pd.DataFrame) -> np.ndarray:
	"""
	Construit une image haute résolution (uint16) à partir de trajectoires localisées.
	Chaque trajectoire est tracée par segments (P0→P1, P1→P2, …) avec une couleur unique.

	Colonnes attendues dans `tracks` :
		- "Track" : identifiant de la trajectoire (:class:`int`)
		- "Plane" : ordre/plan (:class:`int`) ; uniquement utilisé pour trier temporellement
		- "X", "Y" : coordonnées (``float``, en pixels dans l'image de base)
		- "Color" : intensité à tracer ``(0..65535)``. Toute valeur hors bornes est tronquée.

	:param width: Largeur de l'image de base.
	:param height: Hauteur de l'image de base.
	:param ratio: Ratio d'aggrandissement de l'image (>=1). Les coordonnées sont multipliées par ce facteur.
	:param tracks: Tableau des points de trajectoires.
	:return: Nouvelle image en uint16 de forme (height*ratio, width*ratio).
	"""

	if ratio < 1: return np.zeros((height, width), dtype=np.uint16)
	H, W = int(height * ratio), int(width * ratio)
	if width < 1 or height < 1: return np.zeros((max(H, 1), max(W, 1)), dtype=np.uint16)

	res = np.zeros((H, W), dtype=np.uint16)
	cols = {"Track", "Plane", "X", "Y", "Color"}
	if not cols.issubset(tracks.columns):
		# Rien à tracer si les colonnes ne sont pas toutes présentes
		return res

	# Copie minimale + nettoyage
	df = tracks.loc[:, ["Track", "Plane", "X", "Y", "Color"]].copy()

	# Suppression des lignes invalides sur X/Y (nan/inf)
	df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["X", "Y"])
	if df.empty: return res

	# Mise à l'échelle et conversion entiers rapides
	# np.rint() pour arrondir au plus proche avant cast en int64
	df["X"] = np.rint(df["X"].to_numpy(dtype=float) * ratio)
	df["Y"] = np.rint(df["Y"].to_numpy(dtype=float) * ratio)

	df["Color"] = np.clip(df["Color"], 0, MAX_UI_16).astype(np.uint16, copy=False)

	# Tri stable : par Track puis Plane puis index (ordre d'origine)
	df = df.sort_values(["Track", "Plane"], kind="mergesort")

	# Conversion en tableaux numpy pour itération rapide
	track_ids = df["Track"].to_numpy().astype(int)
	xs = df["X"].to_numpy().astype(int)
	ys = df["Y"].to_numpy().astype(int)
	cs = df["Color"].to_numpy().astype(int)

	# Indices de début/fin de chaque groupe Track
	# track_ids[1:] != track_ids[:-1] Compare chaque élément au précédent
	# np.flatnonzero pour avoir les indices des True donc indique le dernier élément de chaque trajectoire
	# np.r_ concatène des séquences. on ajoute 0 et track_ids.size.
	split_idx = np.r_[0, 1 + np.flatnonzero(track_ids[1:] != track_ids[:-1]), track_ids.size]

	# Dessin : Bresenham entier avec écriture max()
	def _draw_segment_max(x_0: int, y_0: int, x_1: int, y_1: int, c: np.uint16) -> None:
		dx, dy = abs(x_1 - x_0), -abs(y_1 - y_0)
		sx, sy = 1 if x_0 < x_1 else -1, 1 if y_0 < y_1 else -1
		err = dx + dy
		while True:
			if 0 <= x_0 < W and 0 <= y_0 < H:
				# garde la valeur maximale pour conserver la luminosité (en cas de superposition de plusieurs trajectoires)
				cur = res[y_0, x_0]
				if c > cur: res[y_0, x_0] = c
			if x_0 == x_1 and y_0 == y_1: break
			e2 = err << 1  # 2*err
			if e2 >= dy:
				err += dy
				x_0 += sx
			if e2 <= dx:
				err += dx
				y_0 += sy

	# Pour chaque trajectoire, couleur unique
	for g in range(len(split_idx) - 1):
		start, end = split_idx[g], split_idx[g + 1]
		# if end - start == 0: continue impossible, on vérifie en amont les dataframe vide pouvant provoquer ce cas
		c_track = cs[start]

		# tracer points isolés
		if end - start == 1:
			_draw_segment_max(xs[start], ys[start], xs[start], ys[start], np.uint16(c_track))
			continue

		# tracer segments successifs
		for i in range(start, end - 1):
			x0, y0, x1, y1 = xs[i], ys[i], xs[i + 1], ys[i + 1]
			_draw_segment_max(x0, y0, x1, y1, np.uint16(c_track))

	return res


##################################################
def render_roi(image: np.ndarray, points: np.ndarray, roi_size: int, color: list[int]) -> np.ndarray:
	"""
	Construit une image RGB à partir d'une image en niveaux de gris et ajoute des contours de ROIs autour des points donnés.

	:param image: Image d'entrée en niveaux de gris (numpy array 2D).
	:param points: Tableau 2D des coordonnées (X, Y) des points, sous forme de flottants.
	:param roi_size: Taille du carré à dessiner autour de chaque point.
	:param color: Couleur du contour du ROI en RGB (tuple ou liste de trois valeurs).
	:return: Image RGB avec les contours des ROIs dessinés.
	"""
	# Normalisation des niveaux de gris sur 0-255
	min_val, max_val = image.min(), image.max()
	if max_val > min_val: image = ((image - min_val) / (max_val - min_val) * MAX_UI_8).astype(np.uint8)
	else: image = np.zeros_like(image, dtype=np.uint8)  # .	   Cas d'une image uniforme

	# Conversion en RGB
	res = np.stack([image] * 3, axis=-1)

	if points is None or points.size == 0 or points.shape[1] != 2: return res
	# Dessin des contours des ROIs
	half_size = (roi_size / 2.0)  # .						   Demi taille de la ROI.
	max_height, max_width = image.shape[0], image.shape[1]
	for x, y in points:
		y_min, y_max = max(0, int(round(y - half_size))), min(max_height, int(round(y + half_size)))
		x_min, x_max = max(0, int(round(x - half_size))), min(max_width, int(round(x + half_size)))

		# Dessiner le contour du carré
		res[y_min:y_max, x_min] = color  # .				   Ligne gauche
		res[y_min:y_max, x_max] = color  # .				   Ligne droite
		res[y_min, x_min:x_max] = color  # .				   Ligne haut
		res[y_max, x_min:min(max_width, x_max + 1)] = color  # Ligne bas (distance +1 pour avoir un carré "fini")

	return res


##################################################
def plot_histogram(ax: plt.Axes, data: np.ndarray, title: str, limit: bool = True, kde: bool = True, density: bool = True):
	"""
	Trace un histogramme des données avec Seaborn, et optionnellement une courbe kernel density estimation.

	:param ax: Axe sur lequel tracer l'histogramme.
	:param data: Données sous forme de tableau numpy.
	:param title: Titre de l'histogramme.
	:param limit: Si True, applique la règle des 3 sigmas pour limiter les données.
	:param kde: Si True, superpose une kde gaussienne.
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
		limits = [mu - 3 * sigma, mu + 3 * sigma]  # .					   Limite théoriques des datas
		data = data[(data >= limits[0]) & (data <= limits[1])]  # .		   Suppression des datas au dela des limites
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
def plot_plane_violin(ax: plt.Axes, data: np.ndarray, title: str):
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
