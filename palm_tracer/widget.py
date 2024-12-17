"""
Module contenant la classe `PALMTracerWidget` pour l'interface principale de l'application.

Ce module définit la classe `PALMTracerWidget`, qui crée et gère l'interface utilisateur principale de l'application.
Elle contient des sections de paramètres organisées sous forme de layout,
permettant de modifier différents paramètres pour l'exécution des algorithmes et l'affichage des résultats.
"""

from typing import TYPE_CHECKING

from qtpy.QtWidgets import QHBoxLayout, QPushButton, QWidget

from palm_tracer.Settings import Settings

if TYPE_CHECKING:
	import napari


##################################################
class PALMTracerWidget(QWidget):
	""" Widget principal gérant toute l'interface """

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

		btn = QPushButton("Start Processing")
		btn.clicked.connect(self.on_click)

		self.setLayout(QHBoxLayout())
		self.layout().addWidget(btn)

	##################################################
	def on_click(self):
		""" Action lors d'un clic """
		print(f"napari has {len(self.viewer.layers)} layers")
		print(self.settings)
