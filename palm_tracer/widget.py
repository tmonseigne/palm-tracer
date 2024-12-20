"""
Module contenant la classe `PALMTracerWidget` pour l'interface principale de l'application.

Ce module définit la classe `PALMTracerWidget`, qui crée et gère l'interface utilisateur principale de l'application.
Elle contient des sections de paramètres organisées sous forme de layout,
permettant de modifier différents paramètres pour l'exécution des algorithmes et l'affichage des résultats.
"""

import ctypes
from pathlib import Path
from typing import TYPE_CHECKING

from qtpy.QtWidgets import QHBoxLayout, QPushButton, QWidget

from palm_tracer.Settings import Settings
from palm_tracer.Tools import print_warning

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

		btn = QPushButton("Start Processing")
		btn.clicked.connect(self.on_click)

		self.setLayout(QHBoxLayout())
		self.layout().addWidget(btn)

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
	def on_click(self):
		"""Action lors d'un clic"""
		print(f"napari has {len(self.viewer.layers)} layers")
		print(self.settings)
