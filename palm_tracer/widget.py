"""
Module contenant la classe `PALMTracerWidget` pour l'interface principale de l'application.

Ce module définit la classe `PALMTracerWidget`, qui crée et gère l'interface utilisateur principale de l'application.
Elle contient des sections de paramètres organisées sous forme de layout,
permettant de modifier différents paramètres pour l'exécution des algorithmes et l'affichage des résultats.

"""

import ctypes
import os
from datetime import datetime
from pathlib import Path
from typing import cast

import napari
import numpy as np
import pandas as pd
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QFileDialog, QPushButton, QVBoxLayout, QWidget

from palm_tracer.Settings import Settings
from palm_tracer.Settings.Types import FileList
from palm_tracer.Tools import Logger, open_json, open_tif, print_error, print_warning, save_json


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
		self.dll = dict[str, ctypes.CDLL]()
		self._load_dll()
		self._init_ui()

	##################################################
	def _load_dll(self):  # pragma: no cover
		"""Récupère les DLLs si elles existent."""
		dll_path = Path(__file__).parent / "DLL"

		# for name in ["CPU", "GPU", "Live", "Tracking"]:
		# GPU et Live n'arrivent pas à se charger (sans doute une dépendance caché autre), elles sont retirées pour le moment.
		for name in ["CPU", "Tracking"]:
			dll_filename = dll_path / f"{name}_PALM.dll"
			if dll_filename.exists(): self.dll[name] = ctypes.cdll.LoadLibrary(str(dll_filename.resolve()))
			else: print_warning(f"Le fichier DLL '{dll_filename}' est introuvable.")

	##################################################
	def _init_ui(self):
		# Base
		self.setLayout(QVBoxLayout())
		self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)

		# Load Setting Button
		btn = QPushButton("Load Setting")
		btn.clicked.connect(self.load_setting)
		self.layout().addWidget(btn)

		# Settings
		for key in self.settings: self.layout().addLayout(self.settings[key].layout)

		# Add Specific behaviour
		# Lors de l'ajout d'un fichier avec le bouton +, -, clear du setting batch -> Files, le FileList est mis à jour et le selected également
		# La mise à jour du selected fait qu'on le recharge pour la visu napari (sans doute une fonction connect ?)
		# On supprime tous les layers et on charge le fichier tif dans un layer Raw
		file_list_setting = self.settings["Batch"]["Files"]
		if file_list_setting and isinstance(file_list_setting, FileList):
			file_list_setting.signal.connect(self.reset_layer)

		# Launch Button
		btn = QPushButton("Start Processing")
		btn.clicked.connect(self.process)
		self.layout().addWidget(btn)

	##################################################
	def load_setting(self):  # pragma: no cover
		"""Action lors d'un clic sur le bouton Load setting."""
		print("Load settings...")
		file_name, _ = QFileDialog.getOpenFileName(None, "Sélectionner un fichier de paramètres", ".", "Fichiers JSON (*.json)")
		self.settings.update_from_dict(open_json(file_name))
		print(f"Setting loaded with the file \"{file_name}\".")

	##################################################
	def reset_layer(self):  # pragma: no cover
		"""Lors de la mise à jour du batch, le fichier en preview dans Napari est mis à jour."""
		#
		selected_file = cast(FileList, self.settings["Batch"]["Files"]).get_selected()
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
	def process(self):
		"""Action lors d'un clic sur le bouton process"""
		if self.last_file == "":
			print_warning("Aucun fichier en preview.")
			return

		# Output directory management
		output = self.settings.get_output_path()
		os.makedirs(output, exist_ok=True)
		print(f"Output directory: {output}")

		logger = Logger()
		timestamp_suffix = datetime.now().strftime("%Y%d%m_%H%M%S")
		logger.open(f"{output}/log-{timestamp_suffix}.log")
		logger.add("Start Processing.")

		# Save settings
		print(self.settings)
		save_json(f"{output}/settings-{timestamp_suffix}.json", self.settings.to_dict())
		logger.add("Settings Saved.")

		# Save meta file (Création du DataFrame et sauvegarde en CSV)
		depth, height, width = self.viewer.layers["Raw"].data.shape
		df = pd.DataFrame({"Height":                   [height], "Width": [width], "Plane Number": [depth],
						   "Pixel Size (nm)":          [self.settings["Calibration"]["Pixel Size"].get_value()],
						   "Exposure Time (ms/frame)": [self.settings["Calibration"]["Exposure"].get_value()],
						   "Intensity (photon/ADU)":   [self.settings["Calibration"]["Intensity"].get_value()]})
		df.to_csv(f"{output}/meta-{timestamp_suffix}.csv", index=False)
		logger.add("Meta File Saved.")

		# Process
		# ........
		logger.add("Process Finished.")
		logger.close()
