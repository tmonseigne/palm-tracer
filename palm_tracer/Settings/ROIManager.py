"""
Ce fichier définit la classe :class:`.ROIManager`, utilisée pour gérer les zones d'intérêts dans Napari.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

import numpy as np
import pandas as pd
from matplotlib.path import Path as MatplotlibPath
from napari.layers import Shapes

from palm_tracer.Settings.ROI import ROI
from palm_tracer.Settings.Types import CheckInt, SpinInt
from palm_tracer.Tools.Ui import print_warning


##################################################
@dataclass
class ROIManager:
	"""Classe permettant de gérer les ROI de filtrage des résultats."""
	roi_selection: CheckInt
	hr_ratio: SpinInt

	width: int = field(init=False, default=1)
	height: int = field(init=False, default=1)

	_rois: list[ROI] = field(init=False, default_factory=list)
	hr_box: tuple[int, int, int, int] = field(init=False, default=(0, 1, 0, 1))

	_layer_main: Optional[Shapes] = field(init=False, default=None)
	_layer_hr: Optional[Shapes] = field(init=False, default=None)

	_default_color: str = field(init=False, default="white")
	_selected_color: str = field(init=False, default="yellow")
	_is_synchronizing: bool = field(init=False, default=False)

	##################################################
	def __post_init__(self) -> None:
		"""Initialise les connexions du gestionnaire de ROI."""
		self.roi_selection.connect(self._on_roi_selection_changed)

	# ==================================================
	# region Getter/Setter
	# ==================================================
	##################################################
	@property
	def layer_main(self) -> Optional[Shapes]:
		"""Calque de l'interface principale."""
		return self._layer_main

	##################################################
	@layer_main.setter
	def layer_main(self, layer: Shapes):
		"""
		Enregistre le calque de l'interface principale.

		:param layer: Calque de l'interface principale.
		"""
		self._layer_main = layer
		layer.editable = True
		layer.current_edge_color = self._default_color
		layer.current_face_color = "transparent"
		layer.events.data.connect(self.update_from_main)
		layer.selected_data.events.items_changed.connect(self.on_main_selection_changed)
		self.update_main()

	##################################################
	@property
	def layer_hr(self) -> Optional[Shapes]:
		"""Calque de l'interface haute résolution."""
		return self._layer_hr

	##################################################
	@layer_hr.setter
	def layer_hr(self, layer: Shapes):
		"""
		Enregistre le calque de l'interface haute résolution.

		:param layer: Calque de l'interface haute résolution.
		"""
		self._layer_hr = layer
		layer.editable = True
		layer.current_edge_color = self._default_color
		layer.current_face_color = "transparent"
		layer.events.data.connect(self.update_from_hr)
		layer.selected_data.events.items_changed.connect(self.on_hr_selection_changed)
		self.update_hr()

	##################################################
	@property
	def rois(self) -> list[ROI]:
		"""Calque de l'interface haute résolution."""
		return self._rois

	##################################################
	@rois.setter
	def rois(self, rois: list[ROI]):
		"""
		Mets à jour la liste des zones d'intérêts.

		:param rois: Liste à appliquer.
		"""
		intial_l = len(self._rois)
		new_l = len(rois)
		self._rois = rois
		if intial_l != new_l and new_l != 0: self.roi_selection.limits = [1, new_l]

	##################################################
	def set_size(self, width, height):
		"""
		Mets à jour la hauteur et largeur maximale de la ROI.

		:param width: Largeur en pixel.
		:param height: Hauteur en pixel.
		"""
		self.width, self.height = width, height

	##################################################
	def set_xy_roi(self, x_min: float, x_max: float, y_min: float, y_max: float, add: bool = True):
		"""
		Ajoute une zone d'intérêt type rectangle pour un filtre rapide sur X et Y (utile pour simplifier le filtre par ROI en script).

		:param x_min: Position minimale sur X.
		:param x_max: Position maximale sur X.
		:param y_min: Position minimale sur Y.
		:param y_max: Position maximale sur Y.
		:param add: Ajoute la zone aux zones éxistantes si ``True``, sinon remplace les zones par la nouvelle.
		"""
		roi = ROI("rectangle", np.array([[y_min, x_min], [y_min, x_max], [y_max, x_max], [y_max, x_min]], dtype=float))
		if add: self.rois = [*self.rois, roi]  # += ne doit pas être utilisé pour appeler le setter.
		else: self.rois = [roi]

	# ==================================================
	# endregion Getter/Setter
	# ==================================================

	# ==================================================
	# region Synchronization
	# ==================================================
	##################################################
	def update_from_main(self):
		"""Mets à jour la liste des ROI à partir du calque principal (callback appelé à chaque modification dans le calque principal)."""
		if self._layer_main is None or self._is_synchronizing: return
		self._is_synchronizing = True

		self.rois = [ROI(type=self._shape_to_str(s_type), data=np.array(s_data, copy=True))
					 for s_type, s_data in zip(self._layer_main.shape_type, self._layer_main.data, strict=True)]
		self.update_hr()

		self._is_synchronizing = False

	##################################################
	def update_from_hr(self):
		"""Mets à jour la liste des ROI à partir du calque haute résolution (callback appelé à chaque modification dans le calque haute résolution)."""
		if self._layer_hr is None or self._is_synchronizing: return
		self._is_synchronizing = True

		upscale = self.hr_ratio.value  # .		Ratio d'agrandissement
		x0_crop, _, y0_crop, _ = self.hr_box  # Anciens x0, x1, y0, y1 sans l'upscale
		translation = np.array([y0_crop, x0_crop], dtype=float)
		rois: list[ROI] = []

		for shape_type, data in zip(self._layer_hr.shape_type, self._layer_hr.data, strict=True):
			coord = np.asarray(data.data, dtype=float).copy()  # Coordonnées des ROIS
			coord[:, -2:] = (coord[:, -2:] / upscale) + translation  # Transformation des coordonnées (Napari utilise l'ordre (..., Y, X)).
			rois.append(ROI(type=self._shape_to_str(shape_type), data=coord, ))

		self.rois = rois
		self.update_main()

		self._is_synchronizing = False

	##################################################
	def update_main(self):
		"""Mets à jour le calque principal."""
		if self._layer_main is None or len(self.rois) == 0: return
		self._layer_main.data = [np.array(roi.data, copy=True) for roi in self._rois]
		self._layer_main.shape_type = [roi.type for roi in self._rois]

	##################################################
	def update_hr(self):
		"""
		Mets à jour le calque Haute Résolution.

		Les zones d'intérêts doivent être adaptées au ratio d'agrandissement et aux dimensions maximales de l'image.
		"""
		if self._layer_hr is None or len(self.rois) == 0: return
		upscale = self.hr_ratio.value  # .		Ratio d'agrandissement
		x0_crop, _, y0_crop, _ = self.hr_box  # Anciens x0, x1, y0, y1 sans l'upscale
		translation = np.array([y0_crop, x0_crop], dtype=float)
		data = []

		for roi in self._rois:
			coord = np.asarray(roi.data, dtype=float).copy()  # Coordonnées des ROIS
			coord[:, -2:] = (coord[:, -2:] - translation) * upscale  # Transformation des coordonnées (Napari utilise l'ordre (..., Y, X)).
			data.append(coord)

		self._layer_hr.data = data
		self._layer_hr.shape_type = [roi.type for roi in self._rois]

	##################################################
	def on_main_selection_changed(self, event: Any = None):
		"""
		Traite un changement de sélection.

		:param event: Événement napari associé au changement.
		"""
		del event
		self.update_colors(self._layer_main)

	##################################################
	def on_hr_selection_changed(self, event: Any = None):
		"""
		Traite un changement de sélection.

		:param event: Événement napari associé au changement.
		"""
		del event
		self.update_colors(self._layer_hr)

	##################################################
	def _on_roi_selection_changed(self):
		"""
		Sélectionne dans Napari la ROI choisie dans le paramètre.

		L'indice affiché commence à 1 tandis que les indices Napari commencent à 0.
		"""
		selection = self.roi_selection.value - 1
		if selection < 0 or selection >= len(self._rois): return
		selected_data = {selection}
		if self.layer_main is not None: self.layer_main.selected_data = selected_data
		if self.layer_hr is not None: self.layer_hr.selected_data = selected_data

	# ==================================================
	# endregion Synchronization
	# ==================================================

	# ==================================================
	# region IO
	# ==================================================
	##################################################
	def from_dict_list(self, rois: list[dict[str, Any]]):
		"""
		Importe une liste de dictionnaires de formes depuis un enregistrement json.

		:param rois: Liste récupérée.
		"""
		res = []
		for roi in rois: res.append(ROI(roi["type"], np.asarray(roi["data"], dtype=float)))
		self.rois = res

	##################################################
	def to_dict_list(self):
		"""Exporte une liste de dictionnaires de formes pour le format json."""
		res = []
		for roi in self.rois: res.append({"type": roi.type, "data": roi.data.tolist()})
		return res

	# ==================================================
	# endregion IO
	# ==================================================

	# ==================================================
	# region Misc
	# ==================================================
	##################################################
	@staticmethod
	def _shape_to_str(shape_type: Any) -> str:
		"""
		Convertit un type de forme Napari en chaîne de caractères.

		:param shape_type: Type de forme retourné par Napari.
		:return: Nom sérialisable du type de forme.
		"""
		return str(getattr(shape_type, "value", shape_type))

	##################################################
	def update_colors(self, layer: Shapes):
		"""Met à jour les couleurs selon la sélection courante."""
		edge_colors = [self._default_color] * layer.nshapes
		for index in layer.selected_data: edge_colors[index] = self._selected_color
		layer.edge_color = edge_colors

	##################################################
	def get_roi_limits(self) -> tuple[int, int, int, int]:
		"""
		Définit la bounding box de la zone d'intérêt (utile pour la génération HR).

		:return: Positions x_min, x_max, y_min, y_max.
		"""

		selection = self.roi_selection.value - 1
		if not self.roi_selection.active or not 0 <= selection < len(self._rois): return 0, self.width, 0, self.height

		points = np.asarray(self._rois[selection].data)

		x0, x1 = int(np.floor(points[:, -1].min())), int(np.ceil(points[:, -1].max()))
		y0, y1 = int(np.floor(points[:, -2].min())), int(np.ceil(points[:, -2].max()))

		# Limitation aux dimensions de l'image.
		return max(0, x0), min(self.width, x1), max(0, y0), min(self.height, y1)

	##################################################
	def update_hr_box(self):
		"""Mets à jour la bounding box actuelle de la génération Haute résolution."""
		self.hr_box = self.get_roi_limits()

	##################################################
	def filtering_dataframe(self, dataframe: pd.DataFrame, strict: bool = True) -> pd.DataFrame:
		"""
		Filtre un DataFrame selon la ROI sélectionnée.

		Un premier filtrage rapide est effectué à partir de la bounding box.
		Si ``strict`` vaut ``True``, les points sont ensuite filtrés selon la géométrie exacte de la ROI.

		:param dataframe: DataFrame contenant les colonnes ``X`` et ``Y``.
		:param strict: Filtre selon la forme exacte et non uniquement selon la bounding box.
		:return: Copie filtrée du DataFrame.
		"""
		if not self.roi_selection.active or dataframe.empty or not {"X", "Y"}.issubset(dataframe.columns): return dataframe

		selection = self.roi_selection.value - 1
		if not 0 <= selection < len(self._rois): return dataframe

		roi = self._rois[selection]
		x_min, x_max, y_min, y_max = self.get_roi_limits()

		# Premier filtrage rapide avec la bounding box.
		mask = (dataframe["X"].between(x_min, x_max, inclusive="both") & dataframe["Y"].between(y_min, y_max, inclusive="both"))
		df = dataframe.loc[mask].copy()

		if not strict or df.empty: return df

		points = df[["X", "Y"]].to_numpy(dtype=float, copy=False)
		roi_type = roi.type.lower()

		if roi_type in {"polygon", "rectangle"}: strict_mask = self._points_in_polygon(points, roi.data)
		elif roi_type == "ellipse": strict_mask = self._points_in_ellipse(points, roi.data)
		else:
			print_warning(f"Le type de ROI {roi.type!r} ne définit pas une surface compatible avec le filtrage strict.")
			return df

		return df.loc[strict_mask]

	##################################################
	@staticmethod
	def _points_in_polygon(points: np.ndarray, roi_data: np.ndarray) -> np.ndarray:
		"""
		Détermine quels points appartiennent à un polygone.

		:param points: Coordonnées des points sous la forme ``(X, Y)``.
		:param roi_data: Sommets Napari sous la forme ``(Y, X)``.
		:return: Masque booléen indiquant les points contenus dans le polygone.
		"""
		path = MatplotlibPath(np.asarray(roi_data, dtype=float)[:, [-1, -2]])  # passage de Y, X vers X, Y et création du chemin
		return path.contains_points(points, radius=1.0e-9)  # Un petit rayon positif permet d'inclure les points situés sur le bord.

	##################################################
	@staticmethod
	def _points_in_ellipse(points: np.ndarray, roi_data: np.ndarray) -> np.ndarray:
		"""
		Détermine quels points appartiennent à une ellipse.

		:param points: Coordonnées des points sous la forme ``(X, Y)``.
		:param roi_data: Sommets Napari définissant l'ellipse.
		:return: Masque booléen indiquant les points contenus dans l'ellipse.
		"""
		vertices = np.asarray(roi_data, dtype=float)
		x_min, x_max, = vertices[:, -1].min(), vertices[:, -1].max()
		y_min, y_max = vertices[:, -2].min(), vertices[:, -2].max()
		x_center, y_center = (x_min + x_max) / 2.0, (y_min + y_max) / 2.0
		x_radius, y_radius = (x_max - x_min) / 2.0, (y_max - y_min) / 2.0

		if x_radius <= 0.0 or y_radius <= 0.0: return np.zeros(len(points), dtype=bool)

		normalized_distance = (((points[:, 0] - x_center) / x_radius) ** 2 + ((points[:, 1] - y_center) / y_radius) ** 2)
		return normalized_distance <= 1.0
