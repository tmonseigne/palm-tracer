"""Fichier contenant une classe pour créer des rendus."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np
import pandas as pd

from palm_tracer.Processing import Parsing

MAX_UI_16 = np.iinfo(np.uint16).max


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
		Mets à jour les tailles pour le rendu.

		:param width: Largeur de l'image.
		:param height: Hauteur de l'image.
		:param ratio: Ratio d'agrandissement de l'image. Les coordonnées sont multipliées par ce facteur.
		"""
		self._width, self._height, self._ratio = width, height, ratio

	##################################################
	def localizations(self, loc: np.ndarray, color_mode: int = 0, gaussian: dict[str, Any] | None = None) -> np.ndarray:
		"""
		Construit une image Haute résolution (uint16) en fonction des éléments localisés.

		:param loc: Position des points à représenter sous forme de tableau 2D de N lignes et au moins 3 colonnes (X, Y, Couleur).
		:param color_mode: Indique si le rendu en cas de superposition additionne les valeurs ou conserve la valeur la plus élevée.
		:param gaussian: Paramètres pour le rendu gaussien loc doit avoir au moins 6 colonnes  (X, Y, Couleur, Sigma X, Sigma Y, Theta).
		:return: Nouvelle image en uint16 de forme (height*ratio, width*ratio).
		"""
		# Vérification des dimensions
		new_h, new_w = int(self._height * self._ratio), int(self._width * self._ratio)
		if new_h < 1 or new_w < 1: return np.zeros((max(new_h, 1), max(new_w, 1)), dtype=np.uint16)
		res = np.zeros((new_h, new_w), dtype=float)
		if loc.ndim != 2 or loc.shape[1] < 3: return res.astype(np.uint16)

		# Calcul des nouvelles coordonnées entières (vectorisé)
		coords = np.round(loc[:, :2] * self._ratio).astype(int)
		x, y, colors = coords[:, 0], coords[:, 1], loc[:, 2]

		# Filtrage des points hors des dimensions initiales et retour si aucun n'est disponible
		valid = (x >= 0) & (x < new_w) & (y >= 0) & (y < new_h)
		x, y, colors = x[valid], y[valid], colors[valid]
		if x.size == 0: return res.astype(np.uint16)

		# Rendu
		if gaussian is None:  # .								  Calcul de l'image en mode spot
			if color_mode == 0: np.add.at(res, (y, x), colors)  # Accumulation des valeurs (plus efficace qu'une boucle)
			else: np.maximum.at(res, (y, x), colors)  # .		  Max par pixel
		else:  # .												  Calcul de l'image en mode Gaussien
			if loc.shape[1] < 6: return res.astype(np.uint16)
			sx, sy, theta = loc[:, 3] * self._ratio, loc[:, 4] * self._ratio, Parsing.degrees_to_radians(loc[:, 5])
			if gaussian["Shape"] == 0:  # .						  Taille fixe isotrope
				theta.fill(0)
				s = gaussian["Size"] * self._ratio
				sx.fill(s)
				sy.fill(s)
			elif gaussian["Shape"] == 1:  # .					  Isotrope (theta = 0, sigma = moyenne des deux axes)
				theta.fill(0)
				s = (sx + sy) / 2
				sx = sy = s
			# else: .											  Anisotrope aucun changement.

			# Modification des couleurs
			if gaussian["Fixed Intensity"]: colors.fill(gaussian["Intensity"])
			else: colors /= gaussian["Intensity"]
			self.draw_gaussian_2d(res, x, y, colors, sx, sy, theta, color_mode)

		res = res.clip(0, MAX_UI_16)  # Limite les valeurs entre 0 et la valeur maximale possible pour un uint16
		return res.astype(np.uint16)  # Forcer le type de l'image en np.uint16

	##################################################
	def tracks(self, trc: np.ndarray) -> np.ndarray:
		"""
		Construit une image haute résolution (uint16) à partir de trajectoires localisées.
		Chaque trajectoire est tracée par segments (P0→P1, P1→P2, …).

		Colonnes attendues dans `tracks` :
			- "Track" : identifiant de la trajectoire (:class:`int`)
			- "X", "Y" : coordonnées (:class:`float`, en pixels dans l'image de base)
			- "Color" : intensité à tracer ``(0..65535)``. Toute valeur hors bornes est tronquée.

		:param trc: Tableau des points de trajectoires sous forme de tableau 2D de N lignes et 4 colonnes (Track, X, Y, Couleur).
		:return: Nouvelle image en uint16 de forme (height*ratio, width*ratio).
		"""
		# Vérification des dimensions
		new_h, new_w = int(self._height * self._ratio), int(self._width * self._ratio)
		if new_h < 1 or new_w < 1: return np.zeros((max(new_h, 1), max(new_w, 1)), dtype=np.uint16)
		res = np.zeros((new_h, new_w), dtype=np.uint16)
		if trc.ndim != 2 or trc.shape[1] != 4: return res

		# Filtrage des points hors des dimensions initiales et retour si aucun n'est disponible
		mask = ((trc[:, 1] >= 0) & (trc[:, 1] < self._width) & (trc[:, 2] >= 0) & (trc[:, 2] < self._height))
		trc = trc[mask]
		if trc.size == 0: return res

		# Calcul des nouvelles coordonnées entières (vectorisé)
		coords = np.round(trc[:, 1:3] * self._ratio).astype(int)
		trc, x, y, colors = trc[:, 0].astype(int), coords[:, 0], coords[:, 1], trc[:, 3].astype(np.uint16)

		# Indices de début/fin de chaque groupe Track
		# tracks[1:] != tracks[:-1] Compare chaque élément au précédent
		# np.flatnonzero pour avoir les indices des True donc indique le dernier élément de chaque trajectoire
		# np.r_ concatène des séquences. On ajoute 0 et tracks.size.
		split_idx = np.r_[0, 1 + np.flatnonzero(trc[1:] != trc[:-1]), trc.size]

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
	def add_colors_to_localizations(loc: pd.DataFrame, col: str = "", max_value: float = 0) -> pd.DataFrame:
		"""
		Construit un tableau numpy contenant les coordonnées des localisations et une valeur scalaire associée à utiliser comme intensité/couleur.

		Le tableau retourné est de forme ``(N, 3)`` et contient, dans l'ordre : ``X``, ``Y`` et ``Color``.

		- Les colonnes ``X`` et ``Y`` sont toujours extraites du DataFrame.
		- La colonne ``Color`` provient de ``col`` si elle existe.
		- Si ``col`` est absente, la colonne ``Color`` est remplie avec la valeur 1.
		- Si la valeur minimale de ``Color`` est négative, toutes les valeurs sont décalées afin que le minimum devienne nul.
		  :math:`C_{Shifted} = C - C_{min}`
		- Si ``max_value > 0``, les valeurs de ``Color`` sont normalisées linéairement dans l'intervalle ``[0, max_value]``.
		  :math:`C_{Norm} = C_{Shifted} \\times \\frac{C}{C_{max}}`

		La fonction ne modifie pas le DataFrame d'origine.

		:param loc: DataFrame à modifier.
		:param col: Nom de la colonne à utiliser pour calculer la composante ``Color``.
		:param max_value: Valeur maximale cible pour la normalisation. Si ``max_value ≤ 0``, aucune normalisation n'est appliquée.
		:return: Dataframe avec la colonne Color ajouté.
		:raises KeyError: Si les colonnes ``X`` ou ``Y`` sont absentes.

		.. note::
			La normalisation n'est appliquée que si le maximum de la colonne ``Color`` après décalage est strictement positif.
			Cela évite une division par zéro lorsque toutes les valeurs sont nulles.
		"""
		if loc.empty: return loc

		# Extraction directe en numpy pour éviter les copies/alignements pandas inutiles.
		if col in loc.columns: colors = loc[col].to_numpy(dtype=np.float64, copy=True)
		else: colors = np.ones(len(loc), dtype=np.float64)

		# Post-traitement des couleurs.
		color_min = np.min(colors)
		if color_min < 0.0: colors -= color_min  # .						 Décalage pour garantir un minimum nul.
		color_max = np.max(colors)
		if color_max <= 0.0: colors = np.ones(len(loc), dtype=np.float64)  # Si l'on n'a que des 0, passe tout à 1.
		elif max_value > 0.0: colors *= max_value / color_max  # .			 Normalisation éventuelle.

		loc["Color"] = colors

		return loc

	##################################################
	@staticmethod
	def add_colors_to_tracks(trc: pd.DataFrame, source: str = "", max_value: float = 0) -> pd.DataFrame:
		"""
		Construit un tableau numpy contenant les numéros, plans et coordonnées des trajectoires
		ainsi qu'une valeur scalaire associée à utiliser comme intensité/couleur.

		Le tableau retourné est de forme ``(N, 5)`` et contient, dans l'ordre : ``Track``, ``Plane``, ``X``, ``Y`` et ``Color``.

		- Les colonnes ``Track``, ``Plane``, ``X``, ``Y`` et ``Integrated Intensity`` sont toujours extraites du DataFrame.
		- La colonne ``Color`` est défini selon la source, si la source n'est pas prévu, la colonne ``Color`` est remplie avec la valeur 1.
		- Si la valeur minimale de ``Color`` est négative, toutes les valeurs sont décalées afin que le minimum devienne nul.
		  :math:`C_{Shifted} = C - C_{min}`
		- Si ``max_value > 0``, les valeurs de ``Color`` sont normalisées linéairement dans l'intervalle ``[0, max_value]``.
		  :math:`C_{Norm} = C_{Shifted} \\times \\frac{C}{C_{max}}`

		:param trc: DataFrame contenant au minimum les colonnes ``Track``, ``Plane``, ``X``, ``Y`` et ``Integrated Intensity``.
		:param source: Type de données à utiliser pour calculer la composante ``Color``.
		:param max_value: Valeur maximale cible pour la normalisation. Si ``max_value ≤ 0``, aucune normalisation n'est appliquée.
		:return: Tableau numpy de forme ``(N, 5)`` de type ``float64`` contenant ``Track``, ``Plane``, ``X``, ``Y`` et ``Color``.
		:raises KeyError: Si les colonnes ``X`` ou ``Y`` sont absentes.

		.. note::
			La normalisation n'est appliquée que si le maximum de la colonne ``Color`` après décalage est strictement positif.
			Cela évite une division par zéro lorsque toutes les valeurs sont nulles.
		"""
		if trc.empty: return trc

		# --- Extraction des données utiles. ---
		data = trc[["Track", "Plane", "X", "Y", "Integrated Intensity"]].copy()
		data = data.sort_values(["Track", "Plane"], kind="mergesort")  # Tri stable : Track puis Plane puis ordre d'origine.

		# --- Définition de la couleur selon la source ---
		# Numéro de la trajectoire.
		if source == "Track Number": data["Color"] = data["Track"].to_numpy(dtype=np.float64)
		# Plan de chaque point.
		elif source == "Plane": data["Color"] = data["Plane"].to_numpy(dtype=np.float64)

		# Somme des intensités intégrées par trajectoire, recopiée sur tous les points de la trajectoire.
		elif source == "Intensity": data["Color"] = data.groupby("Track")["Integrated Intensity"].transform("sum").to_numpy(dtype=np.float64)

		# Longueur totale de la trajectoire
		elif source == "Length":
			# somme des distances euclidiennes entre points successifs d'une même trajectoire.
			dx = data.groupby("Track")["X"].diff().to_numpy(dtype=np.float64)
			dy = data.groupby("Track")["Y"].diff().to_numpy(dtype=np.float64)
			# Les premières valeurs de chaque trajectoire valent NaN : elles ne contribuent pas à la longueur.
			segment_lengths = np.sqrt(np.square(dx) + np.square(dy))
			segment_lengths = np.nan_to_num(segment_lengths, nan=0.0)
			data["SegmentLength"] = segment_lengths
			data["Color"] = data.groupby("Track")["SegmentLength"].transform("sum").to_numpy(dtype=np.float64)
			data.drop(columns="SegmentLength", inplace=True)

		# Durée en nombre de plans couverts par la trajectoire.
		elif source == "Duration":
			first_plane = data.groupby("Track")["Plane"].transform("min").to_numpy(dtype=np.float64)
			last_plane = data.groupby("Track")["Plane"].transform("max").to_numpy(dtype=np.float64)
			data["Color"] = last_plane - first_plane + 1  # +1 pour etre inclusif
		# Autre source.
		else:
			data["Color"] = np.ones(len(trc), dtype=np.float64)

		# --- Post-traitement des couleurs. ---
		color_min = data["Color"].min()
		if color_min < 0.0:  data["Color"] -= color_min  # .						Décalage pour garantir un minimum nul.
		color_max = data["Color"].max()
		if color_max <= 0.0: data["Color"] = np.ones(len(trc), dtype=np.float64)  # Si l'on n'a que des 0, passe tout à 1.
		elif max_value > 0.0: data["Color"] *= max_value / color_max  # .			Normalisation éventuelle.

		return data[["Track", "Plane", "X", "Y", "Color"]]

	##################################################
	@staticmethod
	def draw_line(img: np.ndarray, x0: int, y0: int, x1: int, y1: int, color: np.uint16):
		"""
		Trace une ligne discrète entre deux points dans une image 2D en utilisant l'algorithme de Bresenham (version entière, sans flottants).

		La ligne est rastérisée en parcourant les pixels entre les coordonnées (x0, y0) et (x1, y1),
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

	##################################################
	@staticmethod
	def draw_gaussian_2d(img: np.ndarray, x: np.ndarray | float, y: np.ndarray | float, colors: np.ndarray | float,
						 sx: np.ndarray | float, sy: np.ndarray | float, theta: np.ndarray | float, color_mode: int = 0) -> np.ndarray:
		"""
		Dessine des gaussiennes 2D anisotropes dans une image.

		:param img: Image de sortie 2D, modifiée sur place.
		:param x: Coordonnées X des centres.
		:param y: Coordonnées Y des centres.
		:param colors: Intensité totale de chaque gaussienne.
		:param sx: Sigma selon l'axe principal X.
		:param sy: Sigma selon l'axe principal Y.
		:param theta: Angle de rotation en radians.
		:param color_mode: 0 : addition des intensités, autre : conservation du maximum pixel à pixel.
		:return: Image résultat.
		"""
		h, w = img.shape
		# On force tout en tableau 1D pour que .shape[0] fonctionne toujours
		x, y, colors = np.atleast_1d(x), np.atleast_1d(y), np.atleast_1d(colors)
		sx, sy, theta = np.atleast_1d(sx), np.atleast_1d(sy), np.atleast_1d(theta)

		for idx in range(x.shape[0]):
			xc, yc = float(x[idx]), float(y[idx])
			sigma_x, sigma_y, angle = float(sx[idx]), float(sy[idx]), float(theta[idx])
			amp = float(colors[idx])

			if sigma_x <= 0.0 or sigma_y <= 0.0: continue

			sigma_max = 3.0 * max(sigma_x, sigma_y)
			x_min, x_max = max(0, int(np.floor(xc - sigma_max))), min(w - 1, int(np.ceil(xc + sigma_max)))
			y_min, y_max = max(0, int(np.floor(yc - sigma_max))), min(h - 1, int(np.ceil(yc + sigma_max)))

			if x_min > x_max or y_min > y_max: continue  # Arrive uniquement si l'entièreté de l'intervalle est hors dimensions.

			x_grid, y_grid = np.arange(x_min, x_max + 1, dtype=np.float64), np.arange(y_min, y_max + 1, dtype=np.float64)
			xx, yy = np.meshgrid(x_grid, y_grid)

			dx, dy = xx - xc, yy - yc
			cos_t, sin_t, sin_2t = np.cos(angle), np.sin(angle), np.sin(2.0 * angle)
			cos_t2, sin_t2 = cos_t * cos_t, sin_t * sin_t
			sx2, sy2 = (2.0 * sigma_x * sigma_x), (2.0 * sigma_y * sigma_y)

			a = sin_t2 / sx2 + cos_t2 / sy2
			b = sin_2t / sx2 - sin_2t / sy2
			c = cos_t2 / sx2 + sin_t2 / sy2

			patch = (amp / (2.0 * np.pi * sigma_x * sigma_y)) * np.exp(-(a * dx * dx + b * dx * dy + c * dy * dy))

			view = img[y_min:y_max + 1, x_min:x_max + 1]
			if color_mode == 0: view += patch
			else: np.maximum(view, patch, out=view)

		return img
