"""Produit les rendus d'images haute résolution à partir des localisations."""

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
	"""
	Produit les rendus haute résolution à partir des localisations.

	La taille de sortie et le facteur d'agrandissement sont conservés par l'instance afin d'être réutilisés par les différents modes de rendu.
	"""

	_w: int = field(init=False, default=1)
	"""Largeur de l'image produite, en pixels."""
	_h: int = field(init=False, default=1)
	"""Hauteur de l'image produite, en pixels."""
	_r: int = field(init=False, default=1)
	"""Facteur d'agrandissement appliqué au rendu."""

	# ==================================================
	# region Configuration
	# ==================================================
	##################################################
	def set_size(self, width: int, height: int, ratio: int):
		"""
		Met à jour les tailles pour le rendu.

		:param width: Largeur de l'image.
		:param height: Hauteur de l'image.
		:param ratio: Ratio d'agrandissement de l'image. Les coordonnées sont multipliées par ce facteur.
		"""
		self._w, self._h, self._r = width * ratio, height * ratio, ratio

	# ==================================================
	# endregion Configuration
	# ==================================================

	# ==================================================
	# region Rendus
	# ==================================================
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
		if self._h < 1 or self._w < 1: return np.zeros((max(self._h, 1), max(self._w, 1)), dtype=np.uint16)
		res = np.zeros((self._h, self._w), dtype=float)
		if loc.ndim != 2 or loc.shape[1] < 3: return res.astype(np.uint16)

		loc_v = self.prepare_data(loc, False, gaussian is not None)
		if loc_v.shape[0] == 0: return res.astype(np.uint16)

		# Rendu
		if gaussian is None:  # .							 Calcul de l'image en mode spot
			x, y, c = np.round(loc_v[:, 0]).astype(int), np.round(loc_v[:, 1]).astype(int), loc_v[:, 2]
			valid = ((x >= 0) & (x < self._w) & (y >= 0) & (y < self._h))
			x, y, c = x[valid], y[valid], c[valid]  # .		 Avec les arrondis, on revérifie les points hors dimension
			if color_mode == 0: np.add.at(res, (y, x), c)  # Accumulation des valeurs (plus efficace qu'une boucle)
			else: np.maximum.at(res, (y, x), c)  # .		 Conservation de la valeur maximale en cas de superposition.
		else:  # .											 Calcul de l'image en mode Gaussien
			if loc.shape[1] < 6: return res.astype(np.uint16)
			x, y = loc_v[:, 0], loc_v[:, 1]
			c, sx, sy, theta = self.prepare_gaussian_data(loc_v[:, 2:6], gaussian)
			self.draw_gaussian_2d(res, x, y, c, sx, sy, theta, color_mode)

		res = res.clip(0, MAX_UI_16)  # Limite les valeurs entre 0 et la valeur maximale possible pour un uint16
		return res.astype(np.uint16)  # Forcer le type de l'image en np.uint16

	##################################################
	def tracks(self, trc: np.ndarray) -> np.ndarray:
		"""
		Construit une image haute résolution (uint16) à partir de trajectoires localisées.
		Chaque trajectoire est tracée par segments (P0→P1, P1→P2, …).

		Colonnes attendues dans ``tracks`` :
			- "Track" : identifiant de la trajectoire (:class:`int`)
			- "X", "Y" : coordonnées (:class:`float`, en pixels dans l'image de base)
			- "Color" : intensité à tracer ``(0..65535)``. Toute valeur hors bornes est tronquée.

		:param trc: Tableau des points de trajectoires sous forme de tableau 2D de N lignes et 4 colonnes (Track, X, Y, Couleur).
		:return: Nouvelle image en uint16 de forme (height*ratio, width*ratio).
		"""
		# Vérification des dimensions
		if self._h < 1 or self._w < 1: return np.zeros((max(self._h, 1), max(self._w, 1)), dtype=np.uint16)
		res = np.zeros((self._h, self._w), dtype=np.uint16)
		if trc.ndim != 2 or trc.shape[1] != 4: return res

		# Calcul des nouvelles coordonnées entières (vectorisé)
		coords = np.round(trc[:, 1:3] * self._r).astype(int)
		trc, x, y, colors = trc[:, 0].astype(int), coords[:, 0], coords[:, 1], trc[:, 3].astype(np.uint16)

		# Filtrage des points hors des dimensions initiales et retour si aucun n'est disponible
		valid = (x >= 0) & (x < self._w) & (y >= 0) & (y < self._h)
		trc, x, y, colors = trc[valid], x[valid], y[valid], colors[valid]
		if trc.size == 0: return res.astype(np.uint16)

		# Indices de début/fin de chaque groupe de trajectoire
		# tracks[1:] != tracks[:-1] Compare chaque élément au précédent
		# np.flatnonzero pour avoir les indices des True donc indique le dernier élément de chaque trajectoire
		# np.r_ concatène des séquences. On ajoute 0 et tracks.size.
		split_idx = np.r_[0, 1 + np.flatnonzero(trc[1:] != trc[:-1]), trc.size]

		# Pour chaque trajectoire, couleur unique
		for g in range(len(split_idx) - 1):
			start, end = split_idx[g], split_idx[g + 1]
			# if end - start == 0: continue impossible, on vérifie en amont les DataFrames vides pouvant provoquer ce cas

			if end - start == 1: self.draw_line(res, x[start], y[start], x[start], y[start], colors[start])  # Tracer les points isolés
			else:  # Tracer les segments successifs
				for i in range(start, end - 1): self.draw_line(res, x[i], y[i], x[i + 1], y[i + 1], colors[i])

		return res

	##################################################
	def z_stack(self, loc: np.ndarray, color_mode: int = 0, z_step: float = 20, gaussian: dict[str, Any] | None = None) -> np.ndarray:
		"""
		Construit un volume 3D Haute résolution (uint16) en fonction des éléments localisés.

		Chaque plan représente une coupe sur la hauteur Z.

		:param loc: Position des points à représenter sous forme de tableau 2D de N lignes et au moins 4 colonnes (X, Y, Z, Couleur).
		:param color_mode: Indique si le rendu en cas de superposition additionne les valeurs ou conserve la valeur la plus élevée.
		:param z_step: Distance entre deux plans (unité identique à la colonne Z généralement en nanomètres).
		:param gaussian: Paramètres pour le rendu gaussien loc doit avoir au moins 7 colonnes  (X, Y, Z, Couleur, Sigma X, Sigma Y, Theta).
		:return: Nouveau volume en uint16 de forme (Z, height*ratio, width*ratio).
		"""
		# Vérification des dimensions
		if self._h < 1 or self._w < 1: return np.zeros((1, max(self._h, 1), max(self._w, 1)), dtype=np.uint16)
		if loc.ndim != 2 or loc.shape[1] < 4 or z_step <= 0: return np.zeros((1, self._h, self._w), dtype=np.uint16)

		# Préparation des données
		loc_v = self.prepare_data(loc, True, gaussian is not None)
		if loc_v.shape[0] == 0: return np.zeros((1, self._h, self._w), dtype=np.uint16)

		# Calcul des plans Z
		z = loc_v[:, 2]
		z_min = np.nanmin(z)
		z_id = (z - z_min) / z_step  # Passage en "mode plan"
		n_planes = max(int(np.nanmax(z_id)) + 1, 1)

		res = np.zeros((n_planes, self._h, self._w), dtype=float)

		# Rendu
		if gaussian is None:  # .								   Calcul de l'image en mode spot
			x, y, c = np.round(loc_v[:, 0]).astype(int), np.round(loc_v[:, 1]).astype(int), loc_v[:, 3]
			valid = ((x >= 0) & (x < self._w) & (y >= 0) & (y < self._h))
			x, y, c = x[valid], y[valid], c[valid]  # .			   Avec les arrondis, on revérifie les points hors dimension
			z_id = np.floor(z_id[valid]).astype(int)
			if color_mode == 0: np.add.at(res, (z_id, y, x), c)  # Accumulation des valeurs (plus efficace qu'une boucle)
			else: np.maximum.at(res, (z_id, y, x), c)  # .		   Conservation de la valeur maximale en cas de superposition.
		else:  # .												   Calcul de l'image en mode Gaussien
			if loc.shape[1] < 7: return res.astype(np.uint16)
			x, y = loc_v[:, 0], loc_v[:, 1]
			c, sx, _, _ = self.prepare_gaussian_data(loc_v[:, 3:7], gaussian)
			c *= self._r  # EN 3D, on ajoute encore un scale à la couleur
			self.draw_gaussian_3d(res, x, y, z_id, c, sx, color_mode)

		res = res.clip(0, MAX_UI_16)  # Limite les valeurs entre 0 et la valeur maximale possible pour un uint16
		return res.astype(np.uint16)  # Forcer le type de l'image en np.uint16

	##################################################
	def rotation_3d(self, loc: np.ndarray, color_mode: int = 0, z_step: float = 20, frames: int = 36, axis: int = 1,
					gaussian: dict[str, Any] | None = None) -> np.ndarray:
		"""
		Construit un volume 3D Haute résolution (uint16) en fonction des éléments localisés.

		Chaque plan représente une projection selon l'axe de rotation et l'angle sélectionné.

		:param loc: Position des points à représenter sous forme de tableau 2D de N lignes et au moins 4 colonnes (X, Y, Z, Couleur).
		:param color_mode: Indique si le rendu en cas de superposition additionne les valeurs ou conserve la valeur la plus élevée.
		:param z_step: Distance entre deux plans (unité identique à la colonne Z généralement en nanomètres).
		:param frames: Nombre de plans pour effectuer une rotation complète.
		:param axis: Axe de rotation (X,Y,Z).
		:param gaussian: Paramètres pour le rendu gaussien loc doit avoir au moins 7 colonnes  (X, Y, Z, Couleur, Sigma X, Sigma Y, Theta).
		:return: Nouveau volume en uint16 de forme (Z, height*ratio, width*ratio).
		"""
		# Vérification des dimensions
		if self._h < 1 or self._w < 1: return np.zeros((1, max(self._h, 1), max(self._w, 1)), dtype=np.uint16)
		if loc.ndim != 2 or loc.shape[1] < 4 or frames < 1 or z_step <= 0: return np.zeros((1, self._h, self._w), dtype=np.uint16)

		loc_v = self.prepare_data(loc, True, gaussian is not None)
		if loc_v.shape[0] == 0: return np.zeros((1, self._h, self._w), dtype=np.uint16)

		# Préparation des données
		x, y, z, c = loc_v[:, 0], loc_v[:, 1], loc_v[:, 2], loc_v[:, 3]
		z_id = (z - np.nanmin(z)) / z_step  # .																Conversion du Z en indice de plan
		cx, cy, cz = (self._w - 1) / 2.0, (self._h - 1) / 2.0, (np.nanmax(z_id) - np.nanmin(z_id)) / 2.0  # Centre de la géométrie source
		x0, y0, z0 = x - cx, y - cy, z_id - cz  # .															Coordonnées relatives au centre

		# Taille de projection volontairement carrée pour éviter le clipping pendant la rotation.
		diameter = int(np.ceil(2.0 * np.sqrt(cx * cx + cy * cy + cz * cz))) + 3
		out_h, out_w = max(self._h, diameter), max(self._w, diameter)
		# Centre de l'image résultat
		ox, oy = (out_w - 1) / 2.0, (out_h - 1) / 2.0

		# Allocation
		res = np.zeros((frames, out_h, out_w), dtype=float)
		angles = np.linspace(0.0, 2.0 * np.pi, frames, endpoint=False)

		if gaussian is not None:
			if loc_v.shape[1] < 7: return res.astype(np.uint16)
			c, sx, sy, theta = self.prepare_gaussian_data(loc_v[:, 3:7], gaussian)

		for angle_id, angle in enumerate(angles):  # .							Pour chaque angle, calcul de la projection
			cos_a, sin_a = np.cos(angle), np.sin(angle)
			if axis == 0: xr, yr = x0, cos_a * y0 - sin_a * z0  # .				Rotation autour de X, projection sur X/Y'
			elif axis == 1: xr, yr = cos_a * x0 + sin_a * z0, y0  # .			Rotation autour de Y, projection sur X'/Y
			else: xr, yr = cos_a * x0 - sin_a * y0, sin_a * x0 + cos_a * y0  # .	Rotation autour de Z, projection sur X'/Y'
			xp, yp = xr + ox, yr + oy  # .										Position réelle (ajout du centre qui a été avant rotation)

			if gaussian is not None:
				self.draw_gaussian_2d(res[angle_id], xp, yp, c, sx, sy, theta, color_mode)
			else:
				xi, yi = np.round(xp).astype(int), np.round(yp).astype(int)  # Position en pixels
				valid = (xi >= 0) & (xi < out_w) & (yi >= 0) & (yi < out_h)
				xi, yi, ci = xi[valid], yi[valid], c[valid]  # .				Avec les arrondis, on revérifie les points hors dimension
				if color_mode == 0: np.add.at(res, (angle_id, yi, xi), ci)  # .	Accumulation des valeurs (plus efficace qu'une boucle)
				else: np.maximum.at(res, (angle_id, yi, xi), ci)  # .			Conservation de la valeur maximale en cas de superposition.

		res = res.clip(0, MAX_UI_16)  # Limite les valeurs entre 0 et la valeur maximale possible pour un uint16
		return res.astype(np.uint16)  # Forcer le type de l'image en np.uint16

	# ==================================================
	# endregion Rendus
	# ==================================================

	# ==================================================
	# region Préparation et dessin
	# ==================================================
	##################################################
	@staticmethod
	def add_colors_to_localizations(loc: pd.DataFrame, col: str = "", max_value: float = 0) -> pd.DataFrame:
		"""
		Construit un tableau NumPy contenant les coordonnées des localisations et une valeur scalaire associée à utiliser comme intensité/couleur.

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
		:return: DataFrame avec la colonne Color ajouté.
		:raises KeyError: Si les colonnes ``X`` ou ``Y`` sont absentes.

		.. note:: La normalisation n'est appliquée que si le maximum de la colonne ``Color`` après décalage est strictement positif.
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
		Construit un tableau NumPy contenant les numéros de trajectoire, les plans, les coordonnées des trajectoires
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
		:return: tableau NumPy de forme ``(N, 5)`` de type ``float64`` contenant ``Track``, ``Plane``, ``X``, ``Y`` et ``Color``.
		:raises KeyError: Si les colonnes ``X`` ou ``Y`` sont absentes.

		.. note:: La normalisation n'est appliquée que si le maximum de la colonne ``Color`` après décalage est strictement positif.
			Cela évite une division par zéro lorsque toutes les valeurs sont nulles.
		"""
		if trc.empty: return trc

		# --- Extraction des données utiles. ---
		data = trc[["Track", "Plane", "X", "Y", "Integrated Intensity"]].copy()
		data = data.sort_values(["Track", "Plane"], kind="mergesort")  # Tri stable : Track, puis Plane puis ordre d'origine.

		# --- Définition de la couleur selon la source ---
		# Numéro de la trajectoire.
		if source == "Track Number": data["Color"] = data["Track"].to_numpy(dtype=np.float64)
		# Plan de chaque point.
		elif source == "Plane": data["Color"] = data["Plane"].to_numpy(dtype=np.float64)

		# Somme des intensités intégrées par trajectoire, recopiée sur tous les points de la trajectoire.
		elif source == "Intensity": data["Color"] = data.groupby("Track")["Integrated Intensity"].transform("sum").to_numpy(dtype=np.float64)

		# Longueur totale de la trajectoire
		elif source == "Length":
			# Somme des distances euclidiennes entre points successifs d'une même trajectoire.
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
			data["Color"] = last_plane - first_plane + 1  # +1 pour inclure les deux bornes
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
	def prepare_data(self, data: np.ndarray, is_3d: bool = False, is_gaussian: bool = False) -> np.ndarray:
		"""
		Prépare les données pour le rendu :

		- Multiplie par le ratio les colonnes concernées.
		- Remplace les degrés par des gradients si nécessaire.
		- Vérifie les bornes de l'image et supprime les points hors dimensions.

		:param data: Données à préparer
		:param is_3d: Les données possèdent une composante Z.
		:param is_gaussian: Les données seront utilisées pour une représentation gaussienne.
		:return: Copie transformée des données, limitée aux dimensions du rendu.
		"""

		res = data.copy()
		scale_col = [0, 1]
		shift = 1 if is_3d else 0
		if is_gaussian and data.shape[1] > 5 + shift:
			gaussian_col = [3 + shift, 4 + shift, 5 + shift]
			scale_col += gaussian_col[:2]
			res[:, gaussian_col[-1]] = Parsing.degrees_to_radians(res[:, gaussian_col[-1]])

		res[:, scale_col] *= self._r

		# Filtrage des points hors des dimensions
		valid = (res[:, 0] >= 0) & (res[:, 0] < self._w) & (res[:, 1] >= 0) & (res[:, 1] < self._h)
		res = res[valid, :]
		return res

	##################################################
	def prepare_gaussian_data(self, loc: np.ndarray, gaussian: dict[str, Any]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
		"""
		Récupère les données Color, Sigma X, Sigma Y, Theta et les modifient en fonction des paramètres utilisateurs.

		:param loc: Position des points à représenter sous forme de tableau 2D de N lignes et 3 colonnes (Sigma X, Sigma Y, Theta).
		:param gaussian: Paramètres pour le rendu gaussien.
		:return: le quatuor de tableaux 1D pour Color, Sigma X, Sigma Y et Theta.
		"""
		c, sx, sy, theta = loc[:, 0], loc[:, 1], loc[:, 2], Parsing.degrees_to_radians(loc[:, 3])
		if gaussian["Shape"] == 0:  # .	Taille fixe isotrope
			theta.fill(0)
			s = gaussian["Size"] * self._r
			sx.fill(s)
			sy.fill(s)
		elif gaussian["Shape"] == 1:  # Isotrope (theta = 0, sigma = moyenne des deux axes)
			theta.fill(0)
			s = ((sx + sy) / 2)
			sx = sy = s
		# else: .						Anisotrope aucun changement.

		# Modification des couleurs
		r2: float = self._r * self._r  # Intensité intégrée : facteur d'agrandissement au carré en 2D, au cube en 3D.
		if gaussian["Fixed Intensity"]: c.fill(gaussian["Intensity"] * r2)
		else: c *= r2 / gaussian["Intensity"]
		return c, sx, sy, theta

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
				if color > img[y0, x0]: img[y0, x0] = color  # Changement de couleur si elle est plus élevée que la couleur courante.
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

			norm = amp / (2.0 * np.pi * sigma_x * sigma_y)
			patch = norm * np.exp(-(a * dx * dx + b * dx * dy + c * dy * dy))

			view = img[y_min:y_max + 1, x_min:x_max + 1]
			if color_mode == 0: view += patch
			else: np.maximum(view, patch, out=view)

		return img

	##################################################
	@staticmethod
	def draw_gaussian_3d(img: np.ndarray, x: np.ndarray | float, y: np.ndarray | float, z: np.ndarray | float,
						 colors: np.ndarray | float, s: np.ndarray | float, color_mode: int = 0) -> np.ndarray:
		"""
		Dessine des gaussiennes 3D isotropes dans un volume.

		:param img: Volume de sortie 3D, modifié sur place, forme (Z, Y, X).
		:param x: Coordonnées X des centres.
		:param y: Coordonnées Y des centres.
		:param z: Coordonnées Z des centres.
		:param colors: Intensité totale de chaque gaussienne.
		:param s: Sigma isotrope de chaque gaussienne.
		:param color_mode: 0 : addition des intensités, autre : conservation du maximum voxel à voxel.
		:return: Volume résultat.
		"""
		depth, h, w = img.shape
		# On force tout en tableau 1D pour que .shape[0] fonctionne toujours
		x, y, z, colors, s = np.atleast_1d(x), np.atleast_1d(y), np.atleast_1d(z), np.atleast_1d(colors), np.atleast_1d(s)

		for idx in range(x.shape[0]):
			xc, yc, zc = float(x[idx]), float(y[idx]), float(z[idx])
			sigma, amp = float(s[idx]), float(colors[idx])

			radius = 3.0 * sigma
			x_min, x_max = max(0, int(np.floor(xc - radius))), min(w - 1, int(np.ceil(xc + radius)))
			y_min, y_max = max(0, int(np.floor(yc - radius))), min(h - 1, int(np.ceil(yc + radius)))
			z_min, z_max = max(0, int(np.floor(zc - radius))), min(depth - 1, int(np.ceil(zc + radius)))

			if x_min > x_max or y_min > y_max or z_min > z_max: continue  # Arrive uniquement si l'entièreté de l'intervalle est hors dimensions.

			x_grid = np.arange(x_min, x_max + 1, dtype=np.float64)
			y_grid = np.arange(y_min, y_max + 1, dtype=np.float64)
			z_grid = np.arange(z_min, z_max + 1, dtype=np.float64)
			zz, yy, xx = np.meshgrid(z_grid, y_grid, x_grid, indexing="ij")

			dx, dy, dz = xx - xc, yy - yc, zz - zc
			r2 = dx * dx + dy * dy + dz * dz
			norm = amp / (((2.0 * np.pi) ** 1.5) * sigma ** 3)
			patch = norm * np.exp(-r2 / (2.0 * sigma * sigma))
			view = img[z_min:z_max + 1, y_min:y_max + 1, x_min:x_max + 1]

			if color_mode == 0: view += patch
			else: np.maximum(view, patch, out=view)

		return img
