"""Produit les rendus d'images haute résolution à partir des localisations."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np
import pandas as pd
from PIL import Image

from palm_tracer.Processing import Parsing
from palm_tracer.Tools import FileIO
from palm_tracer.Tools.Ui import print_warning

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

		:param trc: Tableau 2D de forme ``(N, 5)`` contenant les colonnes ``Track, Plane, X, Y, Color``.
		:param color_mode: Méthode de combinaison des valeurs superposées : ``0`` pour l'addition, ``1`` pour le maximum et ``2`` pour le minimum.
		:param bg_color: Valeur attribuée aux pixels de fond.
		:return: Nouvelle image de forme ``(height * ratio, width * ratio)`` et de type :class:`~numpy.uint16`.
		"""
		# Vérification des dimensions de sortie et des entrées
		if self._h < 1 or self._w < 1: return self.blank_rendering(bg_color, False)
		if trc.ndim != 2 or trc.shape[1] != 5: return self.blank_rendering(bg_color, False)

		# Préparation des coordonnées entières et filtrage des points hors des dimensions du rendu.
		track_ids, coords, colors, split_idx = self.prepare_tracks(trc)
		if track_ids.size == 0: return self.blank_rendering(bg_color, False)

		# Initialisation
		res, bg_mask = self.init_rendering(color_mode, self._h, self._w)

		# Vues sur les coordonnées spatiales ; les plans ne sont pas utilisés pour le rendu 2D.
		x, y = coords[:, 1], coords[:, 2]

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

	##################################################
	def track_stack(self, trc: np.ndarray, color_mode: int = 0, bg_color: int = 0, head_size: int = 1, tail_width: int = 1, tail_length: int = -1,
					fade_type: int = 0, raw: np.ndarray | None = None, upscale_type: int = 0, color_map: str = "viridis") -> np.ndarray:
		"""
		Construit une séquence de trajectoires limitée aux plans contenant des observations.

		Les données sont triées par trajectoire puis par plan. Les plans d'origine commencent à un.
		La séquence couvre les bornes inclusives du premier au dernier point valide, sans prolongation pour terminer le fade.
		Les plans sans observation sont conservés : seules les queues déjà apparues peuvent y être visibles.

		Les intensités sont combinées selon ``color_mode``, indépendamment des opacités, fusionnées par maximum.
		Toutes les queues sont dessinées avant toutes les têtes ; les têtes imposent leur couleur et une opacité de un.
		Le mélange avec le fond est effectué une seule fois, lors de la finalisation.

		:param trc: Tableau ``(N, 5)`` contenant ``Track, Plane, X, Y, Color``, trié par trajectoire puis par plan.
		:param color_mode: Combinaison des intensités des queues, avec ou sans raw : ``0`` addition, ``1`` maximum, ``2`` minimum.
		:param bg_color: Intensité du fond uniforme sans raw, sur l'échelle uint16.
		:param head_size: Diamètre entier des têtes circulaires, en pixels du rendu, ramené au minimum à un.
		:param tail_width: Largeur entière du pinceau carré des segments, en pixels du rendu, ramenée au minimum à un.
		:param tail_length: Durée de la queue en plans : ``-1`` conserve tout l'historique apparu, ``0`` ne dessine que les têtes.
			Une durée positive applique la limite d'âge décrite par :meth:`draw_track`.
		:param fade_type: ``0`` pour une coupure nette, ``1`` pour une décroissance linéaire ; ignoré si la durée vaut -1 ou 0.
		:param raw: Fond brut 3D déjà recadré spatialement sur la ROI, conservant les plans depuis le début de l'acquisition.
			Une image 2D représente une acquisition à un plan. Les intensités sont interprétées sur l'échelle fixe 0–65535.
		:param upscale_type: Agrandissement du fond brut : ``0`` plus proche voisin, ``1`` Lanczos.
		:param color_map: Colormap des trajectoires pour la sortie RGB ; le raw conserve une représentation en gris.
		:return: Volume ``(plans, hauteur, largeur)`` uint16 sans raw, ou ``(plans, hauteur, largeur, 3)`` uint8 avec raw.
			Sans point valide, un seul plan scalaire uint16 uniforme de bg_color est retourné, même si raw est fourni.
			L'indice zéro correspond au premier plan d'acquisition retenu après filtrage spatial.
		:raises ValueError: Si le raw n'est ni 2D ni 3D ou ne contient pas les plans retenus.
		"""
		# --- Vérification des dimensions de sortie et des entrées. ---
		background = int(np.clip(bg_color, 0, MAX_UI_16))
		if self._h < 1 or self._w < 1: return self.blank_rendering(background, True)
		if trc.ndim != 2 or trc.shape[1] != 5: return self.blank_rendering(background, True)

		# --- Préparation des coordonnées entières et filtrage des points hors des dimensions du rendu. ---
		track_ids, coords, colors, split_idx = self.prepare_tracks(trc)
		if track_ids.size == 0: return self.blank_rendering(background, True)

		# --- Bornes temporelles inclusives : éviter les plans inutiles en début et fin. ---
		p_min, p_max = int(np.min(coords[:, 0])), int(np.max(coords[:, 0]))
		n_planes = p_max - p_min + 1
		coords[:, 0] -= p_min  # Passage des plans d'acquisition aux indices locaux du volume de sortie.

		# --- Initialisation : intensités non prémultipliées et masque alpha flottant. ---
		init_value = 0.0 if color_mode == 0 else (-np.inf if color_mode == 1 else np.inf)
		res = np.full((n_planes, self._h, self._w), init_value, dtype=float)
		alpha_mask = np.zeros_like(res, dtype=float)
		# L'alpha vaut zéro hors dessin. Ne pas utiliser draw_line tel quel : il mélange déjà la couleur et écrit True dans le masque.

		# --- Dessin des queues, puis des têtes : deux passes sur les trajectoires. ---
		for i in range(track_ids.size):
			start, end = split_idx[i], split_idx[i + 1]
			self.draw_track(res, alpha_mask, coords[start:end], colors[start:end], tail_width, tail_length, fade_type, color_mode)
		for i in range(track_ids.size):
			start, end = split_idx[i], split_idx[i + 1]
			self.draw_track_heads(res, alpha_mask, coords[start:end], colors[start:end], head_size)

		# --- Finalisation : une seule composition avec le fond. ---
		if raw is None: return self.finalize_track_stack(res, alpha_mask, bg_color)
		if raw.ndim == 2: raw = raw[None, :, :]
		if raw.ndim != 3 or p_min < 1 or p_max > raw.shape[0]: self.finalize_track_stack(res, alpha_mask, bg_color)  # Retour sans Raw en fond.
		background = self._upscale_raw(raw[p_min - 1:p_max], upscale_type)  # Les plans d'acquisition commencent à 1 donc décallage de l'interval.
		return self.finalize_track_stack_rgb(res, alpha_mask, background, color_map)

	# ==================================================
	# endregion Rendus
	# ==================================================

	# ==================================================
	# region Manipulation du résultat
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
		img = np.full(shape, init_value, dtype=float)  # .									 Tableau de résultat.
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
	def finalize_track_stack(img: np.ndarray, alpha_mask: np.ndarray, bg_color: int = 0, clip: bool = True) -> np.ndarray:
		"""
		Finalise une séquence scalaire avec un masque alpha.

		Les pixels d'alpha nul reçoivent directement le fond, sans multiplier les infinis d'initialisation par zéro.
		Pour les pixels contribuants, calculer ``(1 - alpha) * bg_color + alpha * img``, puis saturer dans [0, 65535] si ``clip`` vaut True.
		Sinon, replier les valeurs par un modulo :math:`2^{16}`, comme dans :meth:`finalize_rendering`.
		L'intensité n'est pas prémultipliée par l'alpha en entrée. Le fond raw/RGB aura une finalisation distincte ultérieurement.

		:param img: Volume flottant ``(plans, hauteur, largeur)`` d'intensités, mélangé avec le fond puis saturé ou replié sur place.
		:param alpha_mask: Opacités de même forme, comprises entre zéro et un ; non modifiées.
		:param bg_color: Intensité du fond uniforme, sur l'échelle uint16.
		:param clip: Active la saturation des valeurs au lieu de leur repliement cyclique.
		:return: Nouveau volume uint16 de même forme ; les parties fractionnaires sont tronquées lors de la conversion.
		"""
		res = np.empty(img.shape, dtype=np.uint16)
		# Traiter les plans séparément pour limiter les masques et les copies temporaires à une image 2D.
		for plane, (view, alpha) in enumerate(zip(img, alpha_mask)):
			valid = alpha > 0.0
			view[~valid] = bg_color  # .							Remplace les éléments identifiés comme fond par la couleur choisie.
			# L'intensité des tracés n'est pas prémultipliée : appliquer l'alpha exactement une fois.
			view[valid] = (1.0 - alpha[valid]) * bg_color + alpha[valid] * view[valid]
			if clip: np.clip(view, 0, MAX_UI_16, out=view)  # .		Saturer après mélange, comme les autres rendus.
			else: np.remainder(view, MAX_UI_16 + 1, out=view)  # .	Replier cycliquement avant la conversion en uint16.
			res[plane] = view  # .									Conversion en uint16 avec troncature, sans modifier le masque alpha.
		return res

	##################################################
	@staticmethod
	def finalize_track_stack_rgb(img: np.ndarray, alpha_mask: np.ndarray, raw: np.ndarray, color_map: str = "viridis") -> np.ndarray:
		"""
		Compose les trajectoires colorées sur un fond brut en gris, plan par plan.

		Les intensités sont saturées sur l'échelle fixe 0–65535, sans normalisation par plan.
		La LUT de :func:`~palm_tracer.Tools.FileIO.grayscale_to_color` donne la couleur des trajectoires (zéro reste noir).
		Le raw est converti en gris 0–255 sur les trois canaux. Composer ``(1 - alpha) * fond + alpha * couleur``
		avant arrondi et conversion uint8. Les entrées ne sont pas modifiées et les temporaires sont limités à un plan.

		:param img: Intensités non prémultipliées, de forme ``(plans, hauteur, largeur)``.
		:param alpha_mask: Opacités de même forme dans [0, 1].
		:param raw: Fond déjà recadré temporellement et agrandi, de même forme que img, sur l'échelle uint16.
		:param color_map: Nom de colormap reconnu par Matplotlib.
		:return: Nouveau volume RGB uint8 de forme ``(plans, hauteur, largeur, 3)``.
		:raises ValueError: Si les trois volumes n'ont pas la même forme 3D.
		"""
		if img.ndim != 3 or alpha_mask.shape != img.shape or raw.shape != img.shape:
			raise ValueError("Les intensités, l'alpha et le fond doivent avoir la même forme 3D.")
		lut = FileIO.grayscale_to_color(np.arange(MAX_UI_16 + 1, dtype=np.uint16), color_map)  # Une seule correspondance pour tout le volume
		res = np.empty((*img.shape, 3), dtype=np.uint8)
		for plane in range(img.shape[0]):
			alpha = alpha_mask[plane, ..., None]
			# Écarter les valeurs initiales infinies avant conversion, même si leur alpha vaut zéro.
			indices = np.clip(np.where(alpha_mask[plane] > 0, img[plane], 0), 0, MAX_UI_16).astype(np.uint16)
			foreground = lut[indices]
			background = np.clip(raw[plane], 0, MAX_UI_16)[..., None] / 257.0
			res[plane] = np.rint((1.0 - alpha) * background + alpha * foreground).clip(0, 255).astype(np.uint8)
		return res

	##################################################
	def _upscale_raw(self, raw: np.ndarray, upscale_type: int) -> np.ndarray:
		"""
		Agrandit les axes Y et X d'un volume sans interpoler entre les plans.

		Le mode Lanczos travaille en float32 dans Pillow et peut dépasser les intensités d'origine.
		La saturation est laissée à :meth:`finalize_rendering`. Le volume d'entrée reste inchangé.

		:param raw: Image ``(hauteur, largeur)`` ou volume ``(plans, hauteur, largeur)``, déjà recadré sur la ROI.
			Une image 2D produit un volume avec un seul plan.
		:param upscale_type: ``0`` pour la duplication des pixels ; ``1`` pour Lanczos, plan par plan.
		:return: Nouveau volume float64 aux dimensions du rendu ; rempli de zéros si la taille spatiale est incompatible.
		"""
		if raw.ndim == 2: raw = raw[None, :, :]
		planes, height, width = raw.shape
		if height * self._r != self._h or width * self._r != self._w:
			print_warning("Raw shape doesn't have expected dimensions for output background will be 0.")
			return np.zeros((planes, self._h, self._w), dtype=float)

		res = np.empty((planes, self._h, self._w), dtype=float)
		# La diffusion remplit les blocs sans allouer de volume intermédiaire répété.
		if upscale_type == 0 or self._r == 1: res.reshape(planes, height, self._r, width, self._r)[:] = raw[:, :, None, :, None]
		else:
			for i, plane in enumerate(raw):
				img = Image.fromarray(plane.astype(float))
				res[i] = np.asarray(img.resize((self._w, self._h), resample=Image.Resampling.LANCZOS))
		return res

	# ==================================================
	# endregion Manipulation du résultat
	# ==================================================

	# ==================================================
	# region Préparation des données
	# ==================================================
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
		if col in loc.columns: colors = loc[col].to_numpy(dtype=float, copy=True)
		else: colors = np.ones(len(loc), dtype=float)

		# Post-traitement des couleurs.
		color_min = np.min(colors)
		if color_min < 0.0: colors -= color_min  # .					Décalage pour garantir un minimum nul.
		color_max = np.max(colors)
		if color_max <= 0.0: colors = np.ones(len(loc), dtype=float)  # Si l'on n'a que des 0, passe tout à 1.
		elif max_value > 0.0: colors *= max_value / color_max  # .		Normalisation éventuelle.

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
		if source == "Track ID": data["Color"] = data["Track"].to_numpy(dtype=float)
		# Plan de chaque point.
		elif source == "Plane Number": data["Color"] = data["Plane"].to_numpy(dtype=float)

		# Somme des intensités intégrées par trajectoire, recopiée sur tous les points de la trajectoire.
		elif source == "Track Intensity": data["Color"] = data.groupby("Track")["Integrated Intensity"].transform("sum").to_numpy(dtype=float)

		# Longueur totale de la trajectoire
		elif source == "Track Length":
			# Somme des distances euclidiennes entre points successifs d'une même trajectoire.
			dx = data.groupby("Track")["X"].diff().to_numpy(dtype=float)
			dy = data.groupby("Track")["Y"].diff().to_numpy(dtype=float)
			# Les premières valeurs de chaque trajectoire valent NaN : elles ne contribuent pas à la longueur.
			segment_lengths = np.sqrt(np.square(dx) + np.square(dy))
			segment_lengths = np.nan_to_num(segment_lengths, nan=0.0)
			data["SegmentLength"] = segment_lengths
			data["Color"] = data.groupby("Track")["SegmentLength"].transform("sum").to_numpy(dtype=float)
			data.drop(columns="SegmentLength", inplace=True)

		# Numéro du plan relatif au début de chaque trajectoire, en commençant à 1.
		elif source == "Relative Plane":
			first_plane = data.groupby("Track")["Plane"].transform("min").to_numpy(dtype=float)
			data["Color"] = data["Plane"].to_numpy(dtype=float) - first_plane + 1

		# Durée totale de la trajectoire en nombre de plans couverts.
		elif source == "Track Duration":
			first_plane = data.groupby("Track")["Plane"].transform("min").to_numpy(dtype=float)
			last_plane = data.groupby("Track")["Plane"].transform("max").to_numpy(dtype=float)
			data["Color"] = last_plane - first_plane + 1  # +1 pour inclure les deux bornes.
		# Autre source.
		else:
			data["Color"] = np.ones(len(trc), dtype=float)

		# --- Post-traitement des couleurs. ---
		color_min = data["Color"].min()
		if color_min < 0.0:  data["Color"] -= color_min  # .						Décalage pour garantir un minimum nul.
		color_max = data["Color"].max()
		if color_max <= 0.0: data["Color"] = np.ones(len(trc), dtype=float)  # Si l'on n'a que des 0, passe tout à 1.
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
		Prépare et délimite les trajectoires pour les rendus 2D et les séquences.

		Les coordonnées X et Y sont agrandies puis arrondies au pixel le plus proche.
		Les points hors du rendu sont supprimés après arrondi. Les plans restent inchangés.
		L'entrée doit être triée par trajectoire puis par plan, comme la sortie de :meth:`add_colors_to_tracks`.
		L'ordre des points est conservé et l'entrée n'est pas modifiée.

		:param data: Tableau de forme ``(N, 5)`` contenant ``Track, Plane, X, Y, Color``.
		:return: Identifiants int64 des K trajectoires, coordonnées int64 ``(N valide, 3)`` dans l'ordre ``Plane, X, Y``,
			couleurs et bornes int64 de taille K + 1. La trajectoire i occupe la tranche ``bornes[i]:bornes[i + 1]``
			des coordonnées et des couleurs, accessible sans copie. Sans point valide, les bornes valent ``[0]``.
		"""
		coords = np.empty((data.shape[0], 3), dtype=int)
		coords[:, 0] = data[:, 1]  # .									Plans
		coords[:, 1:] = np.round(data[:, 2:4] * self._r).astype(int)  # X, Y
		x, y = coords[:, 1], coords[:, 2]
		valid = (x >= 0) & (x < self._w) & (y >= 0) & (y < self._h)  # .Suppression des éléments hors cadre
		track_ids = data[valid, 0].astype(int)
		coords, colors = coords[valid], data[valid, 4]

		# Une seule délimitation pour les deux rendus ; aucune allocation par trajectoire.
		if track_ids.size == 0: return track_ids, coords, colors, np.array([0], dtype=int)
		bounds = np.r_[0, 1 + np.flatnonzero(track_ids[1:] != track_ids[:-1]), track_ids.size].astype(int)
		return track_ids[bounds[:-1]], coords, colors, bounds

	# ==================================================
	# endregion Préparation des données
	# ==================================================

	# ==================================================
	# region Dessin
	# ==================================================
	##################################################
	@staticmethod
	def _line_spans(shape: tuple[int, int], x0: int, y0: int, x1: int, y1: int, width: int = 1) -> tuple[int, np.ndarray, np.ndarray]:
		"""
		Décrit l'empreinte d'un segment, sans appliquer de couleur ni d'alpha.

		Chaque pixel de Bresenham porte un pinceau carré. Leur union forme un intervalle continu sur chaque ligne Y.
		Une largeur paire est décalée d'un demi-pixel vers les axes positifs. Les limites sont recadrées sur l'image.
		Deux tableaux de bornes suffisent : la mémoire temporaire est proportionnelle à la hauteur concernée, pas à l'aire.
		Le parcours conserve les pixels du segment d'origine, même lorsque ses extrémités sont hors cadre.

		:param shape: Hauteur et largeur de l'image cible.
		:param x0: Coordonnée X de départ.
		:param y0: Coordonnée Y de départ.
		:param x1: Coordonnée X d'arrivée.
		:param y1: Coordonnée Y d'arrivée.
		:param width: Largeur entière du pinceau carré, ramenée au minimum à un.
		:return: y_min, left et right (tableaux d'entiers) ; la ligne y_min + i couvre ``left[i]:right[i]``.
			Un intervalle vide a left >= right ; une empreinte entièrement hors cadre ou une image vide renvoie zéro et deux tableaux vides.
		"""
		width = max(1, width)
		h_max, w_max = shape
		before, after = (width - 1) // 2, width // 2  # .		Répartition du pinceau autour du pixel central.
		y_min, y_max = max(0, min(y0, y1) - before), min(h_max, max(y0, y1) + after + 1)
		if h_max <= 0 or w_max <= 0 or y_min >= y_max or max(x0, x1) + after < 0 or min(x0, x1) - before >= w_max:
			return 0, np.empty(0, dtype=int), np.empty(0, dtype=int)

		# Un intervalle initialement vide par ligne ; les empreintes successives élargissent ses bornes X.
		left, right = np.full(y_max - y_min, w_max, dtype=int), np.zeros(y_max - y_min, dtype=int)
		dx, dy = abs(x1 - x0), -abs(y1 - y0)  # .				Distance maximale sur chaque axe (dy est négatif).
		sx, sy = 1 if x0 < x1 else -1, 1 if y0 < y1 else -1  # .Orientation du parcours sur chaque axe.
		err = dx + dy  # Erreur accumulée entre la ligne idéale et les pixels parcourus.
		while True:
			# Union des empreintes du pinceau : conserver les extrémités de chaque ligne, sans dessiner plusieurs fois les recouvrements.
			# start:end désigne les lignes Y, tandis que x_min:x_max délimite les pixels X de l'empreinte courante.
			start, end = max(y_min, y0 - before) - y_min, min(y_max, y0 + after + 1) - y_min
			x_min, x_max = max(0, x0 - before), min(w_max, x0 + after + 1)
			if start < end and x_min < x_max:
				np.minimum(left[start:end], x_min, out=left[start:end])
				np.maximum(right[start:end], x_max, out=right[start:end])
			if x0 == x1 and y0 == y1: break  # .				Condition d'arrêt : le dernier pixel a été traité.
			e2 = err << 1  # .									2*err pour décider dans quelle direction avancer.
			if e2 >= dy:  # .									On avance en X si l'erreur le permet.
				err += dy
				x0 += sx
			if e2 <= dx:  # .									On avance en Y si nécessaire (les deux axes peuvent avancer pour une diagonale).
				err += dx
				y0 += sy

		# La boîte englobante peut toucher l'image alors que le segment lui-même passe à côté.
		if not np.any(left < right): return 0, np.empty(0, dtype=int), np.empty(0, dtype=int)
		return y_min, left, right

	##################################################
	@staticmethod
	def draw_line(img: np.ndarray, bg_mask: np.ndarray, x0: int, y0: int, x1: int, y1: int, color: float, color_mode: int = 0,
				  width: int = 1, alpha: float = 1.0):
		"""
		Trace une ligne de Bresenham avec une épaisseur et une transparence optionnelles.

		L'épaisseur est celle d'un pinceau carré appliqué aux pixels du tracé, sans anticrénelage.
		Une largeur impaire est centrée ; une largeur paire est décalée d'un demi-pixel vers X et Y positifs.
		Chaque pixel couvert est traité une seule fois par appel, même lorsque les empreintes du pinceau se recouvrent.

		Le résultat opaque est calculé selon ``color_mode``, puis mélangé avec le pixel existant :
		``résultat = (1 - alpha) * fond + alpha * résultat_opaque``.
		Les valeurs infinies d'initialisation des modes minimum/maximum représentent un fond nul pour ce mélange.
		Un alpha nul ne modifie ni l'image ni le masque ; un alpha égal à un conserve le comportement opaque historique.

		:param img: Image 2D de travail flottante, modifiée sur place.
		:param bg_mask: Masque booléen de même forme, positionné à True pour les pixels auxquels la ligne contribue.
		:param x0: Coordonnée X du point de départ.
		:param y0: Coordonnée Y du point de départ.
		:param x1: Coordonnée X du point d'arrivée.
		:param y1: Coordonnée Y du point d'arrivée.
		:param color: Intensité de la ligne avant mélange.
		:param color_mode: Combinaison opaque : ``0`` pour l'addition, ``1`` pour le maximum et ``2`` pour le minimum.
		:param width: Largeur entière du pinceau en pixels du rendu, ramenée à un si elle est inférieure à un.
		:param alpha: Opacité bornée entre zéro et un.
		"""
		# Bornage des paramètres.
		width, alpha = max(1, width), float(np.clip(alpha, 0.0, 1.0))
		if alpha == 0.0: return
		# --- Chemin direct sans allocation d'empreinte pour les lignes fines. ---
		if width == 1:
			h_max, w_max = img.shape
			if min(y0, y1) >= h_max or max(y0, y1) < 0 or min(x0, x1) >= w_max or max(x0, x1) < 0: return
			dx, dy = abs(x1 - x0), -abs(y1 - y0)  # .					 Distance maximale sur chaque axe (dy est négatif).
			sx, sy = 1 if x0 < x1 else -1, 1 if y0 < y1 else -1  # .	 Orientation du parcours sur chaque axe.
			err = dx + dy  # .											 Erreur accumulée entre la ligne idéale et les pixels parcourus.
			while True:
				if 0 <= x0 < w_max and 0 <= y0 < h_max:  # .			 Vérification des limites de l'image.
					old = img[y0, x0]
					if color_mode == 0: value = old + color  # .	 	 Addition de l'intensité à la valeur courante.
					elif color_mode == 1: value = max(old, color)  # .	 Conservation de la couleur la plus élevée.
					else: value = min(old, color)  # .				 	 Conservation de la couleur la plus petite.
					if alpha < 1.0:  # .							 	 Mélange avec l'existant, les infinis des modes min/max représentent un fond nul.
						background = old if np.isfinite(old) else 0.0
						value = (1.0 - alpha) * background + alpha * value
					img[y0, x0] = value
					bg_mask[y0, x0] = True
				if x0 == x1 and y0 == y1: break  # .					 Condition d'arrêt : le dernier pixel a été traité.
				e2 = err << 1  # .										 2*err pour décider dans quelle direction avancer.
				if e2 >= dy:  # .										 On avance en X si l'erreur le permet.
					err += dy
					x0 += sx
				if e2 <= dx:  # .										 On avance en Y si nécessaire (les deux axes peuvent avancer pour une diagonale).
					err += dx
					y0 += sy
			return

		# --- Epaisseur différente de 1. ---
		y_min, left, right = Renderer._line_spans(img.shape, x0, y0, x1, y1, width)
		# Appliquer couleur et alpha une seule fois à chaque pixel de l'épaisseur, puis marquer exactement la même zone dans le masque.
		for row, (start, end) in enumerate(zip(left, right)):
			if start >= end: continue
			view = img[y_min + row, start:end]
			if color_mode == 0: value = view + color
			elif color_mode == 1: value = np.maximum(view, color)
			else: value = np.minimum(view, color)
			if alpha < 1.0:
				background = np.where(np.isfinite(view), view, 0.0)
				value = (1.0 - alpha) * background + alpha * value
			view[:] = value
			bg_mask[y_min + row, start:end] = True

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

			x_grid, y_grid = np.arange(x_min, x_max + 1, dtype=float), np.arange(y_min, y_max + 1, dtype=float)
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

			x_grid = np.arange(x_min, x_max + 1, dtype=float)
			y_grid = np.arange(y_min, y_max + 1, dtype=float)
			z_grid = np.arange(z_min, z_max + 1, dtype=float)
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

	##################################################
	@staticmethod
	def draw_track(img: np.ndarray, alpha_mask: np.ndarray, track: np.ndarray, colors: np.ndarray,
				   tail_width: int = 1, tail_length: int = -1, fade_type: int = 0, color_mode: int = 0):
		"""
		Dessine les queues d'une trajectoire dans les volumes d'intensité et d'alpha.

		Relier chaque observation à la précédente avec la couleur du point d'arrivée.
		Un segment reliant les plans A et B apparaît intégralement à B, jamais avant B, même s'il manque des observations.
		Exemple 10, 12, 20 : aucun segment à 10/11 ; apparition de 10→12 à 12, puis de 12→20 à 20.
		Entre ces apparitions, aucune nouvelle géométrie n'est ajoutée, mais la durée et le fade continuent à faire vieillir les queues.

		Au plan T, l'âge du segment entier vaut ``T - B``, où B est le plan d'arrivée.
		Un seul alpha s'applique à toute son empreinte, épaisseur comprise, indépendamment de sa longueur spatiale et du plan de départ.
		Même après un long blink, le segment apparaît entièrement opaque puis s'efface uniformément.
		Aucun point intermédiaire n'est créé et aucune interpolation temporelle n'est effectuée le long du segment.

		Pour une durée positive L : coupure nette si âge > L, ou fade linéaire ``max(0, 1 - âge / (L + 1))``.
		Le fade vaut un à l'âge zéro et zéro à L + 1. Une durée -1 conserve les segments apparus sans fade ; zéro supprime les queues.
		Le traitement s'arrête toujours au dernier plan du volume, sans prolongement après la dernière observation globale.

		Combiner les intensités non prémultipliées par addition/minimum/maximum et les alphas par maximum.
		Les recouvrements peuvent associer une intensité et un alpha provenant de segments différents : simplification volontaire.
		Un pixel d'alpha nul ne contribue pas. Ne pas appliquer ici le mélange avec le fond, réservé à la finalisation.
		Les têtes sont dessinées séparément, après toutes les queues, par :meth:`draw_track_heads`.

		:param img: Volume flottant ``(plans, hauteur, largeur)`` d'intensités, modifié sur place.
		:param alpha_mask: Volume flottant de même forme, modifié sur toute l'empreinte, épaisseur comprise.
		:param track: Vue ``(N, 3)`` contenant ``Plane, X, Y`` entiers ; plans locaux triés, après soustraction de p_min.
		:param colors: Vue des N intensités, dans le même ordre que track.
		:param tail_width: Largeur entière du pinceau carré en pixels du rendu, ramenée au minimum à un.
		:param tail_length: Durée en plans ; -1 sans effacement, zéro sans queue, positive pour limiter l'historique.
		:param fade_type: Zéro pour une coupure nette, un pour un fade linéaire.
		:param color_mode: Combinaison des intensités : zéro addition, un maximum, deux minimum.
		"""
		if tail_length == 0 or len(track) < 2: return
		depth, height, width = img.shape
		# --- Pour chaque segment de ma trajectoire. ---
		for i in range(1, len(track)):
			x0, y0 = (int(value) for value in track[i - 1, 1:])
			p1, x1, y1 = (int(value) for value in track[i])

			# --- Plans nécessitant l'affichage de ce segment. ---
			first = max(0, p1)  # .									Le segment n'apparaît qu'à l'arrivée ; aucun indice négatif dans le volume.
			last = depth if tail_length < 0 else min(depth, p1 + tail_length + 1)  # Borne exclusive des plans affichant le segment.
			if first >= last: continue  # .							Segment pas encore apparu ou déjà entièrement effacé dans le volume demandé.

			# --- Un alpha par plan, commun à toute l'empreinte du segment. ---
			if tail_length < 0 or fade_type == 0: alpha = 1.0  # .	Historique illimité ou coupure nette : tous les plans de first:last sont opaques.
			else:
				age = np.arange(first, last, dtype=float) - p1
				alpha = (1.0 - age / (tail_length + 1))[:, None]  # Colonne temporelle diffusée sur tous les pixels X.

			# --- Préparer une seule empreinte par segment, puis la réutiliser sur ses plans visibles. ---
			y_min, left, right = Renderer._line_spans((height, width), x0, y0, x1, y1, tail_width)
			color = colors[i]  # .			Couleur de l'observation d'arrivée, indépendante du fade.
			for row, (start, end) in enumerate(zip(left, right)):
				if start >= end: continue
				y = y_min + row
				# Remplir tous les plans visibles en une opération, sans calcul de distance ni boucle temporelle.
				# L'intensité reste non prémultipliée : seul le masque stocke le fade, le fond sera mélangé à la finalisation.
				view = img[first:last, y, start:end]
				if color_mode == 0: np.add(view, color, out=view)
				elif color_mode == 1: np.maximum(view, color, out=view)
				else: np.minimum(view, color, out=view)
				alpha_view = alpha_mask[first:last, y, start:end]
				np.maximum(alpha_view, alpha, out=alpha_view)  # Même empreinte complète que l'intensité, épaisseur comprise.

	##################################################
	@staticmethod
	def draw_track_heads(img: np.ndarray, alpha_mask: np.ndarray, track: np.ndarray, colors: np.ndarray, head_size: int = 1):
		"""
		Dessine les têtes observées après toutes les queues, sans persistance ni fade.

		Chaque tête est un contour de cercle d'épaisseur radiale un pixel, présent uniquement sur le plan de son observation.
		Imposer sa couleur et un alpha de un sur la même empreinte, en recadrant le contour aux limites de l'image.
		Les diamètres un et deux produisent respectivement un et quatre pixels ; les diamètres pairs suivent le décalage d'un demi-pixel vers X/Y positifs.
		En cas de superposition de têtes, la dernière dessinée l'emporte, selon l'ordre des trajectoires.

		:param img: Volume flottant d'intensités, modifié sur place.
		:param alpha_mask: Volume flottant de même forme, modifié uniquement sur les contours.
		:param track: Vue ``(N, 3)`` contenant les plans locaux et les coordonnées X/Y des observations.
		:param colors: Vue des intensités associées aux observations.
		:param head_size: Diamètre extérieur entier des cercles en pixels du rendu, ramené au minimum à un.
		"""
		# Deuxième passe globale du pipeline : aucune queue ne sera dessinée après ces têtes.
		# Ne créer aucune tête pour les plans sans observation, ni conserver une tête sur les plans suivants.
		head_size = max(1, head_size)
		if len(track) == 0: return
		depth, height, width = img.shape
		before, after = (head_size - 1) // 2, head_size // 2
		# Construire une seule empreinte par appel : une couronne entre les rayons diamètre/2 - 1 et diamètre/2.
		# Les petits diamètres conservent leurs pixels minimaux ; pour les autres, ne toucher ni à l'intensité ni à l'alpha à l'intérieur.
		# Le centre vaut 0 pour un diamètre impair, 0.5 pour un diamètre pair (même convention que les lignes épaisses).
		center = 0.5 if head_size % 2 == 0 else 0.0
		offsets = np.arange(-before, after + 1, dtype=float) - center
		distance_squared = offsets[:, None] ** 2 + offsets[None, :] ** 2
		radius = head_size / 2.0
		ring = (distance_squared <= radius ** 2) & (distance_squared >= max(0.0, radius - 1.0) ** 2)
		for i, point in enumerate(track):
			plane, x, y = (int(value) for value in point)
			if plane < 0 or plane >= depth: continue  # .		Les plans sont déjà locaux ; ne jamais écrire via un indice négatif.
			x_min, x_max = max(0, x - before), min(width, x + after + 1)
			y_min, y_max = max(0, y - before), min(height, y + after + 1)
			if x_min >= x_max or y_min >= y_max: continue  # .	Cercle entièrement hors cadre.
			# Recadrer l'empreinte avec les mêmes décalages que l'image, sans déplacer le centre au voisinage d'un bord.
			patch = ring[y_min - y + before:y_max - y + before, x_min - x + before:x_max - x + before]
			view = img[plane, y_min:y_max, x_min:x_max]
			alpha_view = alpha_mask[plane, y_min:y_max, x_min:x_max]
			view[patch] = colors[i]  # .						La tête impose sa couleur, même si elle est plus faible que celle de la queue.
			alpha_view[patch] = 1.0  # .						Opacité totale sur exactement le même contour, uniquement sur le plan observé.
