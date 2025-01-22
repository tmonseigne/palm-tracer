"""
Module contenant la classe `PALMTracerWidget` pour l'interface principale de l'application.

Ce module définit la classe `PALMTracerWidget`, qui crée et gère l'interface utilisateur principale de l'application.
Elle contient des sections de paramètres organisées sous forme de layout,
permettant de modifier différents paramètres pour l'exécution des algorithmes et l'affichage des résultats.

"""

from typing import cast

import napari
import numpy as np
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QFileDialog, QPushButton, QVBoxLayout, QWidget

from palm_tracer.Processing import auto_threshold, load_dll, PALM
from palm_tracer.Settings import Settings
from palm_tracer.Settings.Types import FileList
from palm_tracer.Tools import open_json, open_tif, print_error, print_warning


##################################################
class PALMTracerWidget(QWidget):
	"""Widget principal gérant toute l'interface"""

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
		self.settings = Settings()
		self.dll = load_dll()
		self._init_ui()

	##################################################
	def _init_ui(self):
		# Base
		self.setLayout(QVBoxLayout())
		self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)

		# Load Setting Button
		btn = QPushButton("Load Setting")
		btn.clicked.connect(self._load_setting)
		self.layout().addWidget(btn)

		# Settings
		for layout in self.settings.get_layouts(): self.layout().addLayout(layout)

		# Add Specific behaviour
		# Lors de l'ajout d'un fichier avec le bouton +, -, clear du setting batch -> Files, le FileList est mis à jour et le selected également.
		# La mise à jour du selected fait qu'on le recharge pour la visu napari.
		# On supprime tous les layers et on charge le fichier tif dans un layer Raw
		file_list_setting = self.settings.batch["Files"]
		if file_list_setting and isinstance(file_list_setting, FileList):
			file_list_setting.connect(self._reset_layer)

		# Launch Button
		btn = QPushButton("Start Processing")
		btn.clicked.connect(self.process)
		self.layout().addWidget(btn)

	##################################################
	def _load_setting(self):  # pragma: no cover
		"""Action lors d'un clic sur le bouton Load setting."""
		print("Load settings...")
		file_name, _ = QFileDialog.getOpenFileName(None, "Sélectionner un fichier de paramètres", ".", "Fichiers JSON (*.json)")
		self.settings.update_from_dict(open_json(file_name))
		print(f"Setting loaded with the file \"{file_name}\".")

	##################################################
	def _reset_layer(self):
		"""Lors de la mise à jour du batch, le fichier en preview dans Napari est mis à jour."""
		selected_file = cast(FileList, self.settings.batch["Files"]).get_selected()
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
	def _get_actual_image(self) -> np.ndarray | None:
		if self.last_file == "":
			print_warning("Aucun fichier en preview.")
			return None
		layer = self.viewer.layers["Raw"]			  # Récupération du layer Raw
		plane_idx = self.viewer.dims.current_step[0]  # Récupération de l'index du plan actuellement affiché
		plane = layer.data[plane_idx]				  # Récupération des données du plan affiché
		return np.asarray(plane, dtype=np.float32)	  # Renvoie sous le format numpy

	##################################################
	def auto_threshold(self):
		"""Action lors d'un clic sur le bouton auto du seuillage."""
		image = self._get_actual_image()
		if image is None: return
		threshold = auto_threshold(image)							  # Calcul du seuil automatique
		self.settings.localisation["Threshold"].set_value(threshold)  # Changement du seuil dans les settings

	##################################################
	def process(self):
		"""Action lors d'un clic sur le bouton process"""
		if self.last_file == "":
			print_warning("Aucun fichier en preview.")
			return
		if self.dll.get("CPU", None) is None or self.dll.get("Tracking", None) is None:
			print_warning("Process non effectué car DLL manquantes.")
			return
		PALM.process(self.dll, self.settings)
