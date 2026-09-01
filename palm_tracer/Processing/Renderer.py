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
	def localizations(self, loc: np.ndarray, color_mode: int = 0, bg_color: int = 0, gaussian: dict[str, Any] | None = None) -> np.ndarray:
		"""
		Construit une image haute résolution à partir d'un ensemble de localisations.

		Chaque localisation est projetée dans l'image selon ses coordonnées et sa valeur d'intensité.
		En cas de superposition, ``color_mode`` détermine la méthode utilisée pour combiner les valeurs :

			- ``0`` : addition des valeurs ;
			- ``1`` : conservation de la valeur maximale ;
			- ``2`` : conservation de la valeur minimale.

		Lorsque ``gaussian`` est renseigné, chaque localisation est représentée par une gaussienne 2D anisotrope.
		Dans ce cas, ``loc`` doit contenir au moins six colonnes : X, Y, intensité, Sigma X, Sigma Y et angle de rotation.

		Les pixels auxquels aucune localisation ne contribue reçoivent la valeur ``bg_color``.

		:param loc: Tableau 2D contenant au minimum les colonnes X, Y et intensité.
		:param color_mode: Méthode de combinaison des valeurs superposées : ``0`` pour l'addition, ``1`` pour le maximum et ``2`` pour le minimum.
		:param bg_color: Valeur attribuée aux pixels de fond.
		:param gaussian: Paramètres optionnels du rendu gaussien. Lorsque la valeur est ``None``, les localisations sont rendues sous forme de pixels.
		:return: Nouvelle image de forme ``(height * ratio, width * ratio)`` et de type :class:`~numpy.uint16`.
		"""
		# Vérification des dimensions de sortie et des entrées
		if self._h < 1 or self._w < 1: return self.blank_rendering(bg_color, False)
		if loc.ndim != 2 or loc.shape[1] < 3 or (gaussian is not None and loc.shape[1] < 6): return self.blank_rendering(bg_color, False)

		# Préparation des données
		loc_v = self.prepare_localizations(loc, False, gaussian)
		if loc_v.shape[0] == 0: return self.blank_rendering(bg_color, False)

		# Initialisation
		res, bg_mask = self.init_rendering(color_mode, self._h, self._w)

		# Rendu
		if gaussian is None:  # .								   Calcul de l'image en mode spot.
			x, y, c = np.round(loc_v[:, 0]).astype(int), np.round(loc_v[:, 1]).astype(int), loc_v[:, 2]
			valid = ((x >= 0) & (x < self._w) & (y >= 0) & (y < self._h))
			x, y, c = x[valid], y[valid], c[valid]  # .		 	   Avec les arrondis, on revérifie les points hors dimension.
			bg_mask[y, x] = True  # .		 					   Mise à jour du masque du fond.
			if color_mode == 0: np.add.at(res, (y, x), c)  # .	   Accumulation des valeurs (plus efficace qu'une boucle).
			elif color_mode == 1: np.maximum.at(res, (y, x), c)  # Conservation de la valeur maximale en cas de superposition.
			else: np.minimum.at(res, (y, x), c)  # .			   Conservation de la valeur minimale en cas de superposition.
		else:  # .												   Calcul de l'image en mode Gaussien
			x, y, c, sx, sy, theta = loc_v[:, 0:6].T
			self.draw_gaussian_2d(res, bg_mask, x, y, c, sx, sy, theta, color_mode)

		return self.finalize_rendering(res, bg_mask, bg_color)

	##################################################
	def tracks(self, trc: np.ndarray, color_mode: int = 0, bg_color: int = 0) -> np.ndarray:
		"""
		Construit une image haute résolution (uint16) à partir de trajectoires localisées.

		Chaque trajectoire est tracée sous forme de segments successifs entre ses points.
		Une trajectoire ne contenant qu'un point est représentée par un pixel unique.

		Les lignes appartenant à une même trajectoire doivent être consécutives dans ``trc``.
		En cas de superposition, ``color_mode`` détermine la méthode utilisée pour combiner les intensités.

		Les pixels auxquels aucune trajectoire ne contribue reçoivent ``bg_color``.

		:param trc: Tableau 2D de forme ``(N, 4)`` contenant, dans l'ordre, l'identifiant de la trajectoire, la coordonnée X, la coordonnée Y et l'intensité.
		:param color_mode: Méthode de combinaison des valeurs superposées : ``0`` pour l'addition, ``1`` pour le maximum et ``2`` pour le minimum.
		:param bg_color: Valeur attribuée aux pixels de fond.
		:return: Nouvelle image de forme ``(height * ratio, width * ratio)`` et de type :class:`~numpy.uint16`.
		"""
		# Vérification des dimensions de sortie et des entrées
		if self._h < 1 or self._w < 1: return self.blank_rendering(bg_color, False)
		if trc.ndim != 2 or trc.shape[1] != 4: return self.blank_rendering(bg_color, False)

		# Préparation des coordonnées entières et filtrage des points hors des dimensions du rendu.
		track_ids, x, y, colors = self.prepare_tracks(trc)
		if track_ids.size == 0: return self.blank_rendering(bg_color, False)

		# Initialisation
		res, bg_mask = self.init_rendering(color_mode, self._h, self._w)

		# Délimitation des groupes de trajectoires consécutives.
		split_idx = np.r_[0, 1 + np.flatnonzero(track_ids[1:] != track_ids[:-1]), track_ids.size]

		# Pour chaque trajectoire, couleur unique
		for g in range(len(split_idx) - 1):
			start, end = split_idx[g], split_idx[g + 1]
			# if end - start == 0: continue impossible, on vérifie en amont les DataFrames vides pouvant provoquer ce cas

			if end - start == 1: self.draw_line(res, bg_mask, x[start], y[start], x[start], y[start], colors[start], color_mode)  # Tracer les points isolés
			else:  # Tracer les segments successifs
				for i in range(start, end - 1): self.draw_line(res, bg_mask, x[i], y[i], x[i + 1], y[i + 1], colors[i], color_mode)

		return self.finalize_rendering(res, bg_mask, bg_color)

	##################################################
	def z_stack(self, loc: np.ndarray, color_mode: int = 0, z_step: float = 20, bg_color: int = 0, gaussian: dict[str, Any] | None = None) -> np.ndarray:
		"""
		Construit un volume haute résolution à partir d'un ensemble de localisations.

		Chaque plan du volume représente un intervalle de hauteur Z de taille ``z_step``.
		L'indice du premier plan est calculé à partir de la plus petite coordonnée Z disponible.

		Lorsque ``gaussian`` est renseigné, chaque localisation est représentée par une gaussienne 3D isotrope.
		Dans ce cas, ``loc`` doit contenir au moins sept colonnes : X, Y, Z, intensité, Sigma X, Sigma Y et Theta.

		Les voxels auxquels aucune localisation ne contribue reçoivent ``bg_color``.

		:param loc: Tableau 2D contenant au minimum les colonnes X, Y, Z et intensité.
		:param color_mode: Méthode de combinaison des valeurs superposées : ``0`` pour l'addition, ``1`` pour le maximum et ``2`` pour le minimum.
		:param z_step: Distance strictement positive entre deux plans, exprimée dans la même unité que la colonne Z, généralement en nanomètres.
		:param bg_color: Valeur attribuée aux voxels de fond.
		:param gaussian: Paramètres optionnels du rendu gaussien. Lorsque la valeur est ``None``, les localisations sont rendues sous forme de voxels.
		:return: Nouveau volume de forme ``(depth, height * ratio, width * ratio)`` et de type :class:`~numpy.uint16`.
		"""
		# Vérification des dimensions de sortie et des entrées
		if self._h < 1 or self._w < 1: return self.blank_rendering(bg_color, True)
		if loc.ndim != 2 or loc.shape[1] < 4 or z_step <= 0 or (gaussian is not None and loc.shape[1] < 7): return self.blank_rendering(bg_color, True)

		# Préparation des données
		loc_v = self.prepare_localizations(loc, True, gaussian)
		if loc_v.shape[0] == 0: return self.blank_rendering(bg_color, True)

		# Calcul des plans Z
		z = loc_v[:, 2]
		z_min = np.nanmin(z)
		z_id = (z - z_min) / z_step  # Passage en "mode plan"
		n_planes = max(int(np.nanmax(z_id)) + 1, 1)

		# Initialisation
		res, bg_mask = self.init_rendering(color_mode, self._h, self._w, n_planes)

		# Rendu
		if gaussian is None:  # .								   Calcul de l'image en mode spot
			x, y, c = np.round(loc_v[:, 0]).astype(int), np.round(loc_v[:, 1]).astype(int), loc_v[:, 3]
			valid = ((x >= 0) & (x < self._w) & (y >= 0) & (y < self._h))
			x, y, c = x[valid], y[valid], c[valid]  # .			   Avec les arrondis, on revérifie les points hors dimension
			z_id = np.floor(z_id[valid]).astype(int)
			bg_mask[z_id, y, x] = True  # .		 						Mise à jour du masque du fond.
			if color_mode == 0: np.add.at(res, (z_id, y, x), c)  # .		Accumulation des valeurs (plus efficace qu'une boucle).
			elif color_mode == 1: np.maximum.at(res, (z_id, y, x), c)  # Conservation de la valeur maximale en cas de superposition.
			else: np.minimum.at(res, (z_id, y, x), c)  # .				Conservation de la valeur minimale en cas de superposition.
		else:  # .												   Calcul de l'image en mode Gaussien
			x, y, _, c, s = loc_v[:, 0:5].T
			c *= self._r  # En 3D, un facteur d'agrandissement supplémentaire est appliqué à l'intensité.
			self.draw_gaussian_3d(res, bg_mask, x, y, z_id, c, s, color_mode)

		return self.finalize_rendering(res, bg_mask, bg_color)

	##################################################
	def rotation_3d(self, loc: np.ndarray, color_mode: int = 0, z_step: float = 20, frames: int = 36, axis: int = 1,
					bg_color: int = 0, gaussian: dict[str, Any] | None = None) -> np.ndarray:
		"""
		Construit une séquence de projections haute résolution en rotation 3D.

		Chaque image du résultat représente une projection des localisations après rotation autour de l'axe sélectionné.
		Les angles sont répartis uniformément sur une rotation complète.

		Lorsque ``gaussian`` est renseigné, les localisations projetées sont représentées par des gaussiennes 2D.
		Les pixels auxquels aucune localisation ne contribue reçoivent ``bg_color``.

		:param loc: Tableau 2D contenant au minimum les colonnes X, Y, Z et intensité.
			Le rendu gaussien requiert également les colonnes Sigma X, Sigma Y et Theta.
		:param color_mode: Méthode de combinaison des valeurs superposées : ``0`` pour l'addition, ``1`` pour le maximum et ``2`` pour le minimum.
		:param z_step: Distance strictement positive entre deux plans, exprimée dans la même unité que la colonne Z.
		:param frames: Nombre strictement positif de projections générées sur une rotation complète.
		:param axis: Axe de rotation : ``0`` pour X, ``1`` pour Y et ``2`` pour Z.
		:param bg_color: Valeur attribuée aux pixels de fond.
		:param gaussian: Paramètres optionnels du rendu gaussien. Lorsque la valeur est ``None``, les localisations sont rendues sous forme de pixels.
		:return: Nouvelle séquence de forme ``(frames, output_height, output_width)`` et de type :class:`~numpy.uint16`.
		"""
		# Vérification des dimensions
		if self._h < 1 or self._w < 1: return self.blank_rendering(bg_color, True)
		if loc.ndim != 2 or loc.shape[1] < 4 or frames < 1 or z_step <= 0 or (gaussian is not None and loc.shape[1] < 7):
			return self.blank_rendering(bg_color, True)

		loc_v = self.prepare_localizations(loc, True, gaussian)
		if loc_v.shape[0] == 0: return self.blank_rendering(bg_color, True)

		# Préparation des données
		x, y, z, c = loc_v[:, 0], loc_v[:, 1], loc_v[:, 2], loc_v[:, 3]
		z_id = (z - np.nanmin(z)) / z_step  # .																Conversion du Z en indice de plan
		cx, cy, cz = (self._w - 1) / 2.0, (self._h - 1) / 2.0, (np.nanmax(z_id) - np.nanmin(z_id)) / 2.0  # Centre de la géométrie source
		x0, y0, z0 = x - cx, y - cy, z_id - cz  # .															Coordonnées relatives au centre
		# Récupération unique des paramètres gaussiens avant le calcul des projections.
		if gaussian is not None: sx, sy, theta = loc_v[:, 4:7].T

		# Taille de projection volontairement carrée pour éviter le clipping pendant la rotation.
		diameter = int(np.ceil(2.0 * np.sqrt(cx * cx + cy * cy + cz * cz))) + 3
		out_h, out_w = max(self._h, diameter), max(self._w, diameter)
		# Centre de l'image résultat
		ox, oy = (out_w - 1) / 2.0, (out_h - 1) / 2.0

		# Initialisation
		res, bg_mask = self.init_rendering(color_mode, out_h, out_w, frames)
		angles = np.linspace(0.0, 2.0 * np.pi, frames, endpoint=False)

		for angle_id, angle in enumerate(angles):  # .								--- Pour chaque angle, calcul de la projection ---
			cos_a, sin_a = np.cos(angle), np.sin(angle)
			if axis == 0: xr, yr = x0, cos_a * y0 - sin_a * z0  # .					Rotation autour de X, projection sur X/Y'
			elif axis == 1: xr, yr = cos_a * x0 + sin_a * z0, y0  # .				Rotation autour de Y, projection sur X'/Y
			else: xr, yr = cos_a * x0 - sin_a * y0, sin_a * x0 + cos_a * y0  # .	Rotation autour de Z, projection sur X'/Y'
			xp, yp = xr + ox, yr + oy  # .											Position réelle (ajout du centre qui a été avant rotation)

			if gaussian is None:  # .												--- Calcul de l'image en mode Spot ---
				xi, yi = np.round(xp).astype(int), np.round(yp).astype(int)  # .	Position en pixels
				valid = (xi >= 0) & (xi < out_w) & (yi >= 0) & (yi < out_h)
				xi, yi, ci = xi[valid], yi[valid], c[valid]  # .					Avec les arrondis, on revérifie les points hors dimension.
				bg_mask[angle_id, yi, xi] = True  # .		 						Mise à jour du masque du fond.
				if color_mode == 0: np.add.at(res, (angle_id, yi, xi), ci)  # .		Accumulation des valeurs (plus efficace qu'une boucle).
				elif color_mode == 1: np.maximum.at(res, (angle_id, yi, xi), ci)  # Conservation de la valeur maximale en cas de superposition.
				else: np.minimum.at(res, (angle_id, yi, xi), ci)  # .				Conservation de la valeur minimale en cas de superposition.
			else:  # .																--- Calcul de l'image en mode Gaussien ---
				self.draw_gaussian_2d(res[angle_id], bg_mask[angle_id], xp, yp, c, sx, sy, theta, color_mode)

		return self.finalize_rendering(res, bg_mask, bg_color)

	# ==================================================
	# endregion Rendus
	# ==================================================

	# ==================================================
	# region Préparation et dessin
	# ==================================================
	##################################################
	def blank_rendering(self, bg_color: int = 0, is_3d: bool = False):
		"""
		Crée une image ou un volume vide rempli avec la couleur de fond.

		Les dimensions spatiales du résultat sont toujours au minimum égales à un pixel.

		:param bg_color: Valeur attribuée aux pixels ou aux voxels de fond.
		:param is_3d: Ajoute un axe de profondeur de taille un lorsque la valeur est ``True``.
		:return: Nouvelle image ou nouveau volume de type :class:`~numpy.uint16`.
		"""
		if is_3d: return np.full((1, max(self._h, 1), max(self._w, 1)), bg_color, dtype=np.uint16)
		return np.full((max(self._h, 1), max(self._w, 1)), bg_color, dtype=np.uint16)

	##################################################
	@staticmethod
	def init_rendering(color_mode: int, height: int, width: int, depth: int = -1) -> tuple[np.ndarray, np.ndarray]:
		"""
		Initialise une image de travail et son masque de contribution.

		L'image est remplie avec l'élément neutre du mode de combinaison :
			- zéro pour l'addition ;
			- moins l'infini pour le maximum ;
			- plus l'infini pour le minimum.

		Le masque est initialisé à ``False``. Une valeur vraie indiquera qu'au moins un élément contribue au pixel ou au voxel correspondant.

		:param color_mode: Méthode de combinaison des valeurs superposées : ``0`` pour l'addition, ``1`` pour le maximum et ``2`` pour le minimum.
		:param height: Hauteur de l'image, en pixels.
		:param width: Largeur de l'image, en pixels.
		:param depth: Profondeur du volume. Une valeur inférieure ou égale à zéro produit une image 2D.
		:return: Couple contenant l'image de travail de type :class:`~numpy.float64` et le masque booléen de même forme.
		"""
		init_value = 0.0 if color_mode == 0 else (-np.inf if color_mode == 1 else np.inf)  # Valeur initiale du fond.
		shape = (depth, height, width) if depth > 0 else (height, width)  # .				 Forme du Tableau (2D ou 3D).
		img = np.full(shape, init_value, dtype=np.float64)  # .								 Tableau de résultat.
		mask = np.zeros_like(img, dtype=bool)  # .											 Masque pour le fond.
		return img, mask

	##################################################
	@staticmethod
	def finalize_rendering(img: np.ndarray, bg_mask: np.ndarray, bg_color: int = 0, clip: bool = True) -> np.ndarray:
		"""
		Applique la couleur de fond et convertit une image de rendu en entiers non signés sur 16 bits.

		Les pixels pour lesquels ``bg_mask`` vaut ``False`` reçoivent la valeur ``bg_color``.
		Cette application de la couleur de fond modifie ``img`` sur place.

		Lorsque ``clip`` vaut ``True``, les valeurs sont saturées dans l'intervalle ``[0, 65535]``.
		Sinon, elles sont repliées cycliquement dans cet intervalle par un modulo :math:`2^{16}`.
		La partie fractionnaire éventuelle est tronquée lors de la conversion.

		:param img: Image ou volume de rendu. Les éléments de fond sont modifiés sur place avant la conversion.
		:param bg_mask: Masque booléen de même forme que ``img``. Une valeur vraie indique qu'au moins un élément contribue au pixel ou au voxel.
		:param bg_color: Valeur attribuée aux éléments de fond.
		:param clip: Active la saturation des valeurs au lieu de leur repliement cyclique.
		:return: Nouvelle image ou nouveau volume de même forme que ``img`` et de type :class:`~numpy.uint16`.
		"""
		img[~bg_mask] = bg_color  # .					Remplace les éléments identifiés comme fond par la couleur choisie.
		if clip: img = img.clip(0, MAX_UI_16)  # .		Limite les valeurs entre 0 et la valeur maximale possible pour un uint16.
		else: img = np.remainder(img, MAX_UI_16 + 1)  # Rend cyclique les valeurs entre 0 et la valeur maximale pour un uint16.
		return img.astype(np.uint16)  # .				Conversion de l'image en np.uint16.

	##################################################
	@staticmethod
	def add_colors_to_localizations(loc: pd.DataFrame, col: str = "", max_value: float = 0) -> pd.DataFrame:
		"""
		Ajoute au DataFrame des localisations une composante ``Color`` utilisée comme intensité ou couleur.

		- La colonne ``Color`` provient de ``col`` lorsque cette colonne existe.
		- Si ``col`` est absente, la colonne ``Color`` est remplie avec la valeur 1.
		- Si la valeur minimale de ``Color`` est négative, toutes les valeurs sont décalées afin que le minimum devienne nul.
		  :math:`C_{Shifted} = C - C_{min}`
		- Si ``max_value > 0``, les valeurs de ``Color`` sont normalisées linéairement dans l'intervalle ``[0, max_value]``.
		  :math:`C_{Norm} = C_{Shifted} \\times \\frac{C}{C_{max}}`

		La fonction modifie le DataFrame reçu et le retourne.

		:param loc: DataFrame des localisations à compléter.
		:param col: Nom de la colonne à utiliser pour calculer la composante ``Color``.
		:param max_value: Valeur maximale cible pour la normalisation. Si ``max_value ≤ 0``, aucune normalisation n'est appliquée.
		:return: DataFrame avec la colonne ``Color`` ajoutée.

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
		Construit un DataFrame contenant les numéros de trajectoire, les plans, les coordonnées des trajectoires
		ainsi qu'une valeur scalaire associée à utiliser comme intensité/couleur.

		Le DataFrame retourné contient, dans l'ordre, les colonnes ``Track``, ``Plane``, ``X``, ``Y`` et ``Color``.

		- Les colonnes ``Track``, ``Plane``, ``X``, ``Y`` et ``Integrated Intensity`` sont toujours extraites du DataFrame.
		- La colonne ``Color`` est définie selon ``source`` ; si la source n'est pas prise en charge, elle est remplie avec la valeur 1.
		- Si la valeur minimale de ``Color`` est négative, toutes les valeurs sont décalées afin que le minimum devienne nul.
		  :math:`C_{Shifted} = C - C_{min}`
		- Si ``max_value > 0``, les valeurs de ``Color`` sont normalisées linéairement dans l'intervalle ``[0, max_value]``.
		  :math:`C_{Norm} = C_{Shifted} \\times \\frac{C}{C_{max}}`

		:param trc: DataFrame contenant au minimum les colonnes ``Track``, ``Plane``, ``X``, ``Y`` et ``Integrated Intensity``.
		:param source: Type de données à utiliser pour calculer la composante ``Color``.
		:param max_value: Valeur maximale cible pour la normalisation. Si ``max_value ≤ 0``, aucune normalisation n'est appliquée.
		:return: DataFrame contenant les colonnes ``Track``, ``Plane``, ``X``, ``Y`` et ``Color``.
		:raises KeyError: Si l'une des colonnes requises est absente.

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
	def prepare_localizations(self, data: np.ndarray, is_3d: bool = False, gaussian: dict[str, Any] | None = None) -> np.ndarray:
		"""
		Prépare les localisations utilisées par les différents modes de rendu.

		Les coordonnées X et Y sont multipliées par le facteur d'agrandissement.
		Pour un rendu gaussien, les sigmas sont également mis à l'échelle et Theta est converti des degrés vers les radians.

		Les paramètres géométriques et l'intensité des gaussiennes sont ensuite adaptés aux réglages utilisateur.
		Les localisations situées hors des dimensions du rendu sont supprimées.

		:param data: Tableau 2D contenant les localisations à préparer.
		:param is_3d: Indique que les données possèdent une composante Z.
		:param gaussian: Paramètres optionnels du rendu gaussien.
		:return: Copie préparée et filtrée des localisations.
		"""
		res = data.copy()
		shift = 1 if is_3d else 0
		scale_columns = [0, 1]
		color_col, sigma_x_col, sigma_y_col, theta_col = 2 + shift, 3 + shift, 4 + shift, 5 + shift

		if gaussian is not None:
			scale_columns.extend((sigma_x_col, sigma_y_col))
			res[:, theta_col] = Parsing.degrees_to_radians(res[:, theta_col])

		res[:, scale_columns] *= self._r

		# Suppression des localisations situées hors des dimensions du rendu.
		valid = (res[:, 0] >= 0) & (res[:, 0] < self._w) & (res[:, 1] >= 0) & (res[:, 1] < self._h)
		res = res[valid, :]

		if gaussian is None or res.shape[0] == 0: return res

		# Référence (vue NumPy) vers les colonnes
		colors = res[:, color_col]
		sigma_x = res[:, sigma_x_col]
		sigma_y = res[:, sigma_y_col]
		theta = res[:, theta_col]

		if gaussian["Shape"] == 0:  # Taille fixe isotrope.
			sigma = gaussian["Size"] * self._r
			sigma_x.fill(sigma)  # Fill remplis la vue avec une valeur unique et conserve le système de référence.
			sigma_y.fill(sigma)
			theta.fill(0.0)
		elif gaussian["Shape"] == 1:  # Taille isotrope calculée à partir de la moyenne des deux axes.
			sigma = (sigma_x + sigma_y) / 2.0
			sigma_x[:] = sigma  # Utiliser [:] pour conserver le système de référence et ne pas faire une copie qui ne modifie pas res.
			sigma_y[:] = sigma
			theta.fill(0.0)

		# L'intensité intégrée est mise à l'échelle selon la surface en 2D.
		r2 = float(self._r * self._r)
		if gaussian["Fixed Intensity"]: colors.fill(gaussian["Intensity"] * r2)
		else: colors *= r2 / gaussian["Intensity"]

		return res

	##################################################
	def prepare_tracks(self, data: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
		"""
		Prépare les données utilisées pour le rendu des trajectoires.

		Les coordonnées X et Y sont multipliées par le facteur d'agrandissement, arrondies au pixel le plus proche puis converties en indices entiers.

		Les points situés hors des dimensions du rendu sont supprimés.

		:param data: Tableau 2D de forme ``(N, 4)`` contenant, dans l'ordre, l'identifiant de la trajectoire, la coordonnée X, la coordonnée Y et l'intensité.
		:return: Quatre tableaux contenant respectivement les identifiants des trajectoires, les coordonnées X, les coordonnées Y et les intensités.
		"""
		track_ids = data[:, 0].astype(np.int64)
		coords = np.round(data[:, 1:3] * self._r).astype(np.intp)
		x, y = coords[:, 0], coords[:, 1]
		colors = data[:, 3]

		valid = (x >= 0) & (x < self._w) & (y >= 0) & (y < self._h)

		return track_ids[valid], x[valid], y[valid], colors[valid]

	##################################################
	@staticmethod
	def draw_line(img: np.ndarray, bg_mask: np.ndarray, x0: int, y0: int, x1: int, y1: int, color: float, color_mode: int = 0):
		"""
		Trace une ligne discrète entre deux points avec l'algorithme de Bresenham.

		La ligne est rastérisée uniquement avec des opérations entières et prend en charge toutes les orientations.
		Pour chaque pixel visité dans les limites de l'image, l'intensité est combinée à la valeur existante selon ``color_mode``.

		L'image et le masque sont modifiés sur place. Le masque est positionné à ``True`` pour chaque pixel valide traversé par la ligne.

		:param img: Image 2D modifiée sur place.
		:param bg_mask: Masque booléen de même forme que ``img``, modifié sur place. Une valeur vraie indique qu'au moins une ligne traverse le pixel.
		:param x0: Coordonnée X du point de départ.
		:param y0: Coordonnée Y du point de départ.
		:param x1: Coordonnée X du point d'arrivée.
		:param y1: Coordonnée Y du point d'arrivée.
		:param color: Intensité de la ligne.
		:param color_mode: Méthode de combinaison des valeurs superposées : ``0`` pour l'addition, ``1`` pour le maximum et ``2`` pour le minimum.
		"""
		h_max, w_max = img.shape[0], img.shape[1]
		dx, dy = abs(x1 - x0), -abs(y1 - y0)  # .			   Distance maximale
		sx, sy = 1 if x0 < x1 else -1, 1 if y0 < y1 else -1  # Orientation
		err = dx + dy  # .									   Erreur accumulée (dy est négatif)
		while True:
			if 0 <= x0 < w_max and 0 <= y0 < h_max:  # .	   Vérification des limites de l'image
				bg_mask[y0, x0] = True
				if color_mode == 0: img[y0, x0] += color  # Addition de l'intensité à la valeur courante.
				elif color_mode == 1:
					if color > img[y0, x0]: img[y0, x0] = color  # Changement de couleur si elle est plus élevée que la couleur courante.
				else:
					if color < img[y0, x0]: img[y0, x0] = color  # Changement de couleur si elle est plus petite que la couleur courante.
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
	def draw_gaussian_2d(img: np.ndarray, bg_mask: np.ndarray, x: np.ndarray | float, y: np.ndarray | float, colors: np.ndarray | float,
						 sx: np.ndarray | float, sy: np.ndarray | float, theta: np.ndarray | float, color_mode: int = 0) -> np.ndarray:
		"""
		Dessine des gaussiennes 2D anisotropes dans une image.

		Chaque gaussienne est évaluée dans une zone limitée à trois fois son plus grand sigma autour de son centre.
		Seules les contributions strictement positives sont appliquées et signalées dans ``bg_mask``.

		L'image et le masque sont modifiés sur place.

		:param img: Image 2D de sortie, modifiée sur place.
		:param bg_mask: Masque booléen de même forme que ``img``, modifié sur place. Une valeur vraie indique qu'au moins une gaussienne contribue au pixel.
		:param x: Coordonnées X des centres.
		:param y: Coordonnées Y des centres.
		:param colors: Intensités totales des gaussiennes.
		:param sx: Sigmas selon l'axe principal X.
		:param sy: Sigmas selon l'axe principal Y.
		:param theta: Angles de rotation en radians.
		:param color_mode: Méthode de combinaison des intensités superposées : ``0`` pour l'addition, ``1`` pour le maximum et ``2`` pour le minimum.
		:return: Référence vers l'image ``img`` modifiée.
		"""
		h, w = img.shape
		# Normalisation des entrées scalaires et vectorielles sous forme de tableaux 1D.
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
			mask_view = bg_mask[y_min:y_max + 1, x_min:x_max + 1]
			patch_mask = patch > 0.0
			mask_view |= patch_mask
			if color_mode == 0: np.add(view, patch, out=view, where=patch_mask)
			elif color_mode == 1: np.maximum(view, patch, out=view, where=patch_mask)
			else: np.minimum(view, patch, out=view, where=patch_mask)

		return img

	##################################################
	@staticmethod
	def draw_gaussian_3d(img: np.ndarray, bg_mask: np.ndarray, x: np.ndarray | float, y: np.ndarray | float, z: np.ndarray | float,
						 colors: np.ndarray | float, s: np.ndarray | float, color_mode: int = 0) -> np.ndarray:
		"""
		Dessine des gaussiennes 3D isotropes dans un volume.

		Chaque gaussienne est évaluée dans une zone limitée à trois fois son sigma autour de son centre.
		Seules les contributions strictement positives sont appliquées et signalées dans ``bg_mask``.

		Le volume et le masque sont modifiés sur place.

		:param img: Volume de sortie 3D de forme ``(Z, Y, X)``, modifié sur place.
		:param bg_mask: Masque booléen de même forme que ``img``, modifié sur place. Une valeur vraie indique qu'au moins une gaussienne contribue au voxel.
		:param x: Coordonnées X des centres.
		:param y: Coordonnées Y des centres.
		:param z: Coordonnées Z des centres.
		:param colors: Intensités totales des gaussiennes.
		:param s: Sigmas isotropes strictement positifs des gaussiennes.
		:param color_mode: Méthode de combinaison des intensités superposées : ``0`` pour l'addition, ``1`` pour le maximum et ``2`` pour le minimum.
		:return: Référence vers le volume ``img`` modifié.
		"""
		depth, h, w = img.shape
		# Normalisation des entrées scalaires et vectorielles sous forme de tableaux 1D.
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
			mask_view = bg_mask[z_min:z_max + 1, y_min:y_max + 1, x_min:x_max + 1]
			patch_mask = patch > 0.0
			mask_view |= patch_mask
			if color_mode == 0: np.add(view, patch, out=view, where=patch_mask)
			elif color_mode == 1: np.maximum(view, patch, out=view, where=patch_mask)
			else: np.minimum(view, patch, out=view, where=patch_mask)

		return img
