"""
Module contenant la classe `PALMTracerWidget` pour l'interface principale de l'application.

Ce module définit la classe `PALMTracerWidget`, qui crée et gère l'interface utilisateur principale de l'application.
Elle contient des sections de paramètres organisées sous forme de layout,
permettant de modifier différents paramètres pour l'exécution des algorithmes et l'affichage des résultats.

.. todo::
   Ajouter un logger

"""

import ctypes
import os
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QFileDialog, QPushButton, QVBoxLayout, QWidget

from palm_tracer.Settings import Settings
from palm_tracer.Tools import Logger, open_json, print_warning, save_json

if TYPE_CHECKING: import napari  # pragma: no cover


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
		# Lors de l'ajout d'un fichier avec le bouton + du setting batch -> Files, le FileList est mis à jour et le selected également
		# La mise à jour du selected fait qu'on le recharge pour la visu napari

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
	def process(self):
		"""Action lors d'un clic sur le bouton process"""
		print(f"napari has {len(self.viewer.layers)} layers")

		# Output directory management
		output = self.settings.get_output_path()
		os.makedirs(output, exist_ok=True)
		print(f"Output directory: {output}")

		logger = Logger()
		timestamp_suffix = datetime.now().strftime("%Y%d%m_%H%M%S")
		logger.open(f"{output}/log-{timestamp_suffix}.log")
		logger.add("Start Processing.")

		# Save settings
		print("Settings :")
		print(self.settings)
		save_json(f"{output}/settings-{timestamp_suffix}.json", self.settings.to_dict())
		logger.add("Settings saved.")

		# Process
		# ........
		logger.add("Process Finished.")
		logger.close()
