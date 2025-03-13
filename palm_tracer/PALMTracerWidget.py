"""
Module contenant la classe :class:`PALMTracerWidget` pour l'interface principale de l'application.

Ce module définit la classe :class:`.PALMTracerWidget`, qui crée et gère l'interface utilisateur principale de l'application.
Elle contient des sections de paramètres organisées sous forme de layout,
permettant de modifier différents paramètres pour l'exécution des algorithmes et l'affichage des résultats.

"""

from typing import cast

import napari
import numpy as np
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QFileDialog, QPushButton, QTabWidget, QVBoxLayout, QWidget

from palm_tracer.PALMTracer import PALMTracer
from palm_tracer.Processing import auto_threshold_dll, run_palm_image_dll
from palm_tracer.Settings.Types import Button, FileList
from palm_tracer.Tools import open_json, open_tif, print_error, print_warning


##################################################
class PALMTracerWidget(QWidget):
	"""Widget principal gérant toute l'interface"""

	# ==================================================
	# region Init
	# ==================================================
	##################################################
	def __init__(self, viewer: "napari.viewer.Viewer"):
		"""
		Initialise le widget principal de l'interface utilisateur.

		Cette méthode configure l'interface en ajoutant différentes sections de paramètres dans la mise en page.

		:param viewer: Viewer napari.
		"""
		super().__init__()
		self.viewer = viewer
		self.last_file = ""
		self.pt = PALMTracer()
		self.__init_ui()

	##################################################
	def __init_ui(self):
		# Base
		self.setLayout(QVBoxLayout())
		self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)

		# Load Setting Button
		btn = QPushButton("Load Setting")
		btn.clicked.connect(self._load_setting)
		self.layout().addWidget(btn)

		self.layout().addWidget(self.pt.settings.batch.widget)
		self.layout().addWidget(self.pt.settings.calibration.widget)

		# Ajout des onglets
		tabs = QTabWidget()  # Création du QTabWidget
		tabs.addTab(self.__create_tab([self.pt.settings.localization.widget, self.pt.settings.tracking.widget]), "Processing")
		tabs.addTab(self.__create_tab([self.pt.settings.visualization_hr.widget, self.pt.settings.visualization_graph.widget]), "Visualization")
		tabs.addTab(self.__create_tab([self.pt.settings.filtering.widget]), "Filtering")

		# Layout principal
		self.layout().addWidget(tabs)

		# Add Specific behaviour
		# Lors de l'ajout d'un fichier avec le bouton +, -, clear du setting batch -> Files, le FileList est mis à jour et le selected également.
		# La mise à jour du selected fait qu'on le recharge pour la visu napari.
		# On supprime tous les layers et on charge le fichier tif dans un layer Raw
		setting = self.pt.settings.batch["Files"]
		if setting and isinstance(setting, FileList):  # pragma: no cover (toujours vrai)
			setting.connect(self._reset_layer)

		# Calcul de la preview
		setting = self.pt.settings.localization["Preview"]
		if setting and isinstance(setting, Button):  # pragma: no cover (toujours vrai)
			setting.connect(self._preview)

		# Calcul automatique du Seuil
		setting = self.pt.settings.localization["Auto Threshold"]
		if setting and isinstance(setting, Button):  # pragma: no cover (toujours vrai)
			setting.connect(self._auto_threshold)

		self.viewer.dims.events.current_step.connect(self._on_plane_change)

		# Launch Button
		btn = QPushButton("Start Processing")
		btn.clicked.connect(self._process)
		self.layout().addWidget(btn)

	##################################################
	@staticmethod
	def __create_tab(widgets: list[QWidget]) -> QWidget:
		"""Crée l'onglet 'Processing' avec son QFormLayout"""
		widget = QWidget()
		layout = QVBoxLayout()
		layout.setAlignment(Qt.AlignmentFlag.AlignTop)

		for w in widgets: layout.addWidget(w)

		widget.setLayout(layout)
		return widget

	# ==================================================
	# endregion Init
	# ==================================================

	# ==================================================
	# region Callback
	# ==================================================
	##################################################
	def _load_setting(self):  # pragma: no cover
		"""Action lors d'un clic sur le bouton Load setting."""
		file_name, _ = QFileDialog.getOpenFileName(None, "Sélectionner un fichier de paramètres", ".", "Fichiers JSON (*.json)")
		try:
			self.pt.settings.update_from_dict(open_json(file_name))
			print(f"Chargement du fichier de configuration '{file_name}'.")
		except Exception as e:
			print_warning(f"Erreur lors du chargement du fichier '{file_name}' : {e}")

	##################################################
	def _reset_layer(self):
		"""Lors de la mise à jour du batch, le fichier en preview dans Napari est mis à jour."""
		selected_file = cast(FileList, self.pt.settings.batch["Files"]).get_selected()
		if not selected_file:
			self.last_file = ""
			print_warning("Aucun fichier sélectionné.")
			return

		if self.last_file == selected_file: return
		else: self.last_file = selected_file

		# Nettoyez tous les layers existants dans le viewer
		self.viewer.layers.clear()

		# Chargez le fichier TIF sélectionné comme un layer Raw dans le viewer
		try:
			raw_data = open_tif(selected_file)
			self.viewer.add_image(raw_data, name="Raw")
			print(f"Loaded {selected_file} into Napari viewer.")
		except Exception as e:
			print_error(f"Error loading {selected_file}: {e}")

	##################################################
	def _add_detection_layers(self, points: np.ndarray):
		"""
		Ajoute deux calques à Napari :
		- Un calque de formes avec des carrés verts pour les ROIs
		- Un calque de points avec des points rouges pour les détections

		:param points: Numpy array de y et x (dans ce sens)
		"""
		if points.size == 0: # Pas de points, pas de calques à ajouter
			print_warning("Aucun point détecté, les calques ne seront pas créés.")
			return

		# Création des points rouges
		if "Points" in self.viewer.layers: self.viewer.layers["Points"].data = points
		else: self.viewer.add_points(points, size=1, face_color="red", name="Points")

		# Création des ROIs (carrés verts)
		roi_size = self.pt.settings.localization["ROI Size"].get_value()
		half_size = roi_size / 2
		rois = []
		for y, x in points:
			rois.append([[y - half_size, x - half_size], [y - half_size, x + half_size],   # Haut gauche, droit
						 [y + half_size, x + half_size], [y + half_size, x - half_size]])  # Bas droit, gauche

		if "ROI" in self.viewer.layers: self.viewer.layers["ROI"].data = rois
		else: self.viewer.add_shapes(rois, shape_type="polygon", edge_color="green", edge_width=0.5, face_color="transparent", name="ROI")

	##################################################
	def _get_actual_image(self) -> np.ndarray | None:
		if self.last_file == "":
			print_warning("Aucun fichier en preview.")
			return None
		layer = self.viewer.layers["Raw"]			  # Récupération du layer Raw
		plane_idx = self.viewer.dims.current_step[0]  # Récupération de l'index du plan actuellement affiché
		plane = layer.data[plane_idx]				  # Récupération des données du plan affiché
		return np.asarray(plane, dtype=np.uint16)	  # Renvoie sous le format numpy

	##################################################
	def _on_plane_change(self, event):
		# Relancer la prévisualisation si elle à déjà été lancé
		if "ROI" in self.viewer.layers: self._preview()

	##################################################
	def _preview(self):
		"""Action lors d'un clic sur le bouton de preview."""
		image = self._get_actual_image()
		if image is None: return
		s = self.pt.settings.localization.get_settings()
		localizations = run_palm_image_dll(self.pt.dlls["CPU"], image, s["Threshold"], s["Watershed"], s["Gaussian Fit Mode"],
										   s["Gaussian Fit Sigma"], s["Gaussian Fit Theta"], s["ROI Size"])
		self._add_detection_layers(localizations[["Y", "X"]].to_numpy())
		print(f"Preview des {len(localizations)} points détectés.")

	##################################################
	def _auto_threshold(self):
		"""Action lors d'un clic sur le bouton auto du seuillage."""
		image = self._get_actual_image()
		if image is None: return
		threshold = auto_threshold_dll(self.pt.dlls["CPU"], image)		 # Calcul du seuil automatique
		print(f"Auto Threshold : {threshold}")
		self.pt.settings.localization["Threshold"].set_value(threshold)  # Changement du seuil dans les settings

	##################################################
	def _process(self):
		"""Action lors d'un clic sur le bouton process"""
		if self.last_file == "":
			print_warning("Aucun fichier en preview.")
			return
		self.pt.process()

# ==================================================
# endregion Callback
# ==================================================
