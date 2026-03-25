"""Fichier contenant une classe pour créer des rendus."""

from dataclasses import dataclass, field

import numpy as np

MAX_UI_16 = np.iinfo(np.uint16).max
MAX_UI_8 = np.iinfo(np.uint8).max
# SCALE = MAX_UI_16 // 8  # Échelle cible de normalization (permet une résolution de superposition de points de 8 fois)
SCALE = 1  # Échelle cible de normalization à 1 chaque supperposition incrémente de 1.


##################################################
@dataclass
class Renderer:
	"""Créateur de graphiques avec Plotly."""

	_width: int = field(init=False, default=1)
	_height: int = field(init=False, default=1)
	_ratio: int = field(init=False, default=1)

	##################################################
	def set_size(self, width: int, height: int, ratio: int):
		"""
		Mets à jour les tailles pour le rendu

		:param width: Largeur de l'image.
		:param height: Hauteur de l'image.
		:param ratio: Ratio d'agrandissement de l'image. Les coordonnées sont multipliées par ce facteur.
		"""
		self._width, self._height, self._ratio = width, height, ratio

	##################################################
	def localizations(self, points: np.ndarray) -> np.ndarray:
		"""
		Construit une image Haute résolution (uint16) en fonction des éléments localisés.

		:param points: Position des points à représenter sous forme de tableau 2D de N lignes et 3 colonnes (X, Y, Couleur).
		:return: Nouvelle image en uint16 de forme (height*ratio, width*ratio).
		"""
		# Vérification des dimensions
		new_h, new_w = int(self._height * self._ratio), int(self._width * self._ratio)
		if new_h < 1 or new_w < 1: return np.zeros((max(new_h, 1), max(new_w, 1)), dtype=np.uint16)
		res = np.zeros((new_h, new_w), dtype=float)
		if points.ndim != 2 or points.shape[1] != 3: return res.astype(np.uint16)

		# Filtrage des points hors des dimensions initiales et retour si aucun n'est disponible
		mask = (points[:, 0] < self._width) & (points[:, 1] < self._height)
		points = points[mask]
		if points.size == 0: return res.astype(np.uint16)

		# Calcul des nouvelles coordonnées entières (vectorisé)
		coords = np.round(points[:, :2] * self._ratio).astype(int)
		x, y, colors = coords[:, 0], coords[:, 1], points[:, 2]

		# Calcul de l'image finale
		np.add.at(res, (y, x), colors)  # Accumulation des valeurs (plus efficace qu'une boucle)
		res = res.clip(0, MAX_UI_16)  # . Limite les valeurs entre 0 et la valeur maximale possible pour un uint16
		return res.astype(np.uint16)  # . Forcer le type de l'image en np.uint16

	##################################################
	def tracks(self, tracks: np.ndarray) -> np.ndarray:
		"""
		Construit une image haute résolution (uint16) à partir de trajectoires localisées.
		Chaque trajectoire est tracée par segments (P0→P1, P1→P2, …).

		Colonnes attendues dans `tracks` :
			- "Track" : identifiant de la trajectoire (:class:`int`)
			- "X", "Y" : coordonnées (:class:`float`, en pixels dans l'image de base)
			- "Color" : intensité à tracer ``(0..65535)``. Toute valeur hors bornes est tronquée.

		:param tracks: Tableau des points de trajectoires sous forme de tableau 2D de N lignes et 4 colonnes (Track, X, Y, Couleur).
		:return: Nouvelle image en uint16 de forme (height*ratio, width*ratio).
		"""
		# Vérification des dimensions
		new_h, new_w = int(self._height * self._ratio), int(self._width * self._ratio)
		if new_h < 1 or new_w < 1: return np.zeros((max(new_h, 1), max(new_w, 1)), dtype=np.uint16)
		res = np.zeros((new_h, new_w), dtype=np.uint16)
		if tracks.ndim != 2 or tracks.shape[1] != 4: return res

		# Filtrage des points hors des dimensions initiales et retour si aucun n'est disponible
		mask = (tracks[:, 1] < self._width) & (tracks[:, 2] < self._height)
		tracks = tracks[mask]
		if tracks.size == 0: return res

		# Calcul des nouvelles coordonnées entières (vectorisé)
		coords = np.round(tracks[:, 1:3] * self._ratio).astype(int)
		tracks, x, y, colors = tracks[:, 0].astype(int), coords[:, 0], coords[:, 1], tracks[:, 3].astype(np.uint16)

		# Indices de début/fin de chaque groupe Track
		# tracks[1:] != tracks[:-1] Compare chaque élément au précédent
		# np.flatnonzero pour avoir les indices des True donc indique le dernier élément de chaque trajectoire
		# np.r_ concatène des séquences. On ajoute 0 et tracks.size.
		split_idx = np.r_[0, 1 + np.flatnonzero(tracks[1:] != tracks[:-1]), tracks.size]

		# Pour chaque trajectoire, couleur unique
		for g in range(len(split_idx) - 1):
			start, end = split_idx[g], split_idx[g + 1]
			# if end - start == 0: continue impossible, on vérifie en amont les dataframe vide pouvant provoquer ce cas

			if end - start == 1: self.draw_line(res, x[start], y[start], x[start], y[start], colors[start])  # tracer des points isolés
			else:  # tracer segments successifs
				for i in range(start, end - 1): self.draw_line(res, x[i], y[i], x[i + 1], y[i + 1], colors[i])

		return res

	# ==================================================
	# region Tools
	# ==================================================
	##################################################
	@staticmethod
	def normalize_data(data: np.ndarray, scale: int = SCALE) -> np.ndarray:
		"""
		Normalisation des données avec prise en compte de l'ordre de grandeur et adaptation des plages.

		Règles :
			- Si toutes les valeurs sont dans `[0,1]`, normalisation vers `[0, SCALE]`.
			- Si valeurs négatives et positives, on prend la puissance de 2 la plus proche de ``max(abs(min), abs(max))`` et on transpose vers `[0, SCALE]`.
			- Colonne uniforme : on force une valeur constante de ``SCALE``.
			- Si toutes les valeurs sont positives, on considère 0 comme min et on normalise avec la puissance de 2 la plus proche du max.

		:param data: Données à normaliser.
		:param scale: Échelle de normalisation
		:return: Données normalisées.
		"""
		if data is None or data.size == 0: return np.zeros_like(data)
		min_val, max_val = data.min(), data.max()

		# Cas 1 : Colonne uniforme (toutes les valeurs identiques)
		if min_val == max_val: return np.full_like(data, scale)

		# Cas 2 : Valeurs entre 0 et 1.
		if min_val >= 0 and max_val <= 1: return scale * data

		# Cas 3 : Valeurs négatives et positives ⇾ on centre autour de 0.
		if min_val < 0 < max_val:
			bound = 2 ** np.ceil(np.log2(max(abs(min_val), abs(max_val))))
			return (scale / (2 * bound)) * (data + bound)

		# Cas 4 : Valeurs positives ⇾ on prend 0 comme min et on ajuste avec la puissance de 2 la plus proche du max
		bound = 2 ** np.ceil(np.log2(max_val))
		return (scale / bound) * data

	##################################################
	@staticmethod
	def draw_line(img: np.ndarray, x0: int, y0: int, x1: int, y1: int, color: np.uint16):
		"""
		Trace une ligne discrète entre deux points dans une image 2D en utilisant l'algorithme de Bresenham (version entière, sans flottants).

		La ligne est rasterisée en parcourant les pixels entre les coordonnées (x0, y0) et (x1, y1),
		avec une gestion robuste de toutes les pentes (horizontales, verticales, diagonales, fortes et faibles).

		Pour chaque pixel visité, la valeur est mise à jour uniquement si la nouvelle couleur est strictement supérieure à la valeur déjà présente.
		Cela permet de conserver l'intensité maximale (utile par exemple pour des accumulations de tracés ou des cartes d'intensité).

		:param img: Image 2D (numpy.ndarray) modifiée *in-place*. Doit être indexable sous la forme ``img[y, x]``.
		:param x0: Coordonnée X du point de départ.
		:param y0: Coordonnée Y du point de départ.
		:param x1: Coordonnée X du point d'arrivée.
		:param y1: Coordonnée Y du point d'arrivée.
		:param color: Intensité à écrire dans les pixels traversés.
		"""
		h_max, w_max = img.shape[0], img.shape[1]
		dx, dy = abs(x1 - x0), -abs(y1 - y0)  # .			   Distance maximale
		sx, sy = 1 if x0 < x1 else -1, 1 if y0 < y1 else -1  # Orientation
		err = dx + dy  # .									   Erreur accumulée (dy est négatif)
		while True:
			if 0 <= x0 < w_max and 0 <= y0 < h_max:  # .	   Vérification des limites de l'image
				if color > img[y0, x0]: img[y0, x0] = color  # Changement de couleur si elle est plus élevé que la couleur courante.
			if x0 == x1 and y0 == y1: break  # .			   Condition d'arrêt
			e2 = err << 1  # .								   2*err pour décider dans quelle direction avancer.
			if e2 >= dy:  # .								   On avance en X si l’erreur le permet
				err += dy
				x0 += sx
			if e2 <= dx:  # .								   On avance en Y si nécessaire
				err += dx
				y0 += sy
