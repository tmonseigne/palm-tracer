"""Fournit le widget Napari de visualisation 3D des localisations."""

from __future__ import annotations

from pathlib import Path

import napari
import numpy as np
import pandas as pd
from napari.utils.notifications import show_warning
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QFileDialog, QFormLayout, QPushButton, QWidget

from palm_tracer.Settings.Groups import Visualization3D


class Viewer3DWidget(QWidget):
	"""
	Affiche les localisations tridimensionnelles dans un calque Napari.

	Le widget charge un fichier CSV, règle les échelles XY et Z, ajuste la taille des points et peut exclure les localisations d'intensité nulle.

	:param viewer: Visionneuse Napari recevant le calque de points.

	.. note:: Le widget peut être lancé avec la commande ``napari -w palm-tracer "Viewer 3D"``.
	"""

	##################################################
	def __init__(self, viewer: napari.Viewer):
		"""
		Initialise le widget et configure l'interface graphique (boutons, champs numériques, checkbox).

		La création du calque Napari se fait plus tard dans :meth:`update_layer` lorsqu'un fichier CSV est chargé.

		:param viewer: Viewer Napari cible.
		:type viewer: :class:`napari.Viewer`
		"""
		super().__init__()
		self.viewer: napari.Viewer = viewer
		self.layer = self.viewer.add_points(np.empty((0, 3), dtype=float), size=1, name="Points 3D", ndim=3)
		self.layer.locked = True
		self.data = pd.DataFrame()  # DataFrame d'origine
		self.z_scale = 1.0
		self._widget = QWidget()
		layout = QFormLayout(self._widget)
		layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # Définir l'alignement du calque en haut.

		self.setLayout(layout)

		# Bouton de chargement CSV
		btn = QPushButton("Load CSV")
		btn.clicked.connect(self.load_csv)
		layout.addWidget(btn)

		self.settings = Visualization3D()
		ui = self.settings.get_ui()
		layout.addWidget(ui.widget)

		self.settings.connect(self.update_layer)

	##################################################
	def load_csv(self):
		"""
		Ouvre une boîte de dialogue pour sélectionner un fichier ``.csv`` et charge les données associées dans un :class:`pandas.DataFrame`.

		Le fichier doit contenir les colonnes : ``"X"``, ``"Y"``, ``"Z"``, ``"Integrated Intensity"``

		Si un calque existe déjà, il est supprimé avant la création du nouveau.

		Cette méthode déclenche ensuite :meth:`update_layer` pour créer le calque 3D.
		"""
		path, _ = QFileDialog.getOpenFileName(self, "Load CSV", ".", "Fichiers CSV (*.csv)")
		if not path or not Path(path).is_file(): return
		self.data = pd.read_csv(path)
		if not all(col in self.data.columns for col in ["X", "Y", "Z", "Integrated Intensity"]):
			self.data = pd.DataFrame()
			show_warning("The file must contain the columns X, Y, Z, and Integrated Intensity.")
			return

		self.update_layer()

	##################################################
	def update_layer(self):
		"""
		Crée ou mets à jour le calque de points 3D dans le viewer Napari.

		Transformations appliquées :
			- réorganisation des coordonnées sous la forme ``(Z, Y, X)``
			- mise à l'échelle par les valeurs choisies dans les widgets
			- suppression éventuelle des points dont ``Integrated Intensity == 0``
			- mise à jour dynamique du calque existant ou création d'un nouveau

		Si aucune donnée n'est encore chargée, la méthode ne fait rien.
		"""
		if self.data.empty: return
		s = self.settings.settings
		px_size, size, scale_xy, scale_z, outliers = s["Pixel Size"], s["Point Size"], s["XY Scale"], s["Z Scale"], s["Remove Outliers"]
		coords = self.data[["Z", "Y", "X"]].to_numpy(dtype=float, copy=True)
		coords[:, 1:3] *= px_size  # .											 Passage en nanomètres pour X et Y précédemment en pixel
		coords *= np.array([scale_z, scale_xy, scale_xy], dtype=coords.dtype)  # Changemenet des échelles

		if outliers: coords = coords[self.data["Integrated Intensity"] > 0]

		# mise à jour du calque
		self.layer.data = coords
		self.layer.size = size


##################################################
def create_viewer3d() -> tuple[napari.Viewer, QWidget]:
	"""
	Crée une nouvelle fenêtre Napari 3D, sans menu, et y ajoute le Viewer3DWidget docké à droite.

	Cette fonction NE lance PAS napari.run() : elle est faite pour être appelée depuis un plugin, donc dans une appli Qt déjà active.
	"""
	viewer = napari.Viewer(ndisplay=3)  # .									 Crée le viewer 3D napari
	viewer.title = "3D Viewer"  # .											 Modifier le titre de la fenêtre
	viewer.window.main_menu.setVisible(False)  # .							 Cacher la barre de menu
	widget = Viewer3DWidget(viewer)  # .									 Crée le widget en lui passant le viewer
	viewer.window.add_dock_widget(widget, name="Viewer 3D", area="right")  # L'ajoute comme dock widget dans la fenêtre napari
	return viewer, widget


##################################################
def open_viewer3d(_viewer: "napari.viewer.Viewer" = None, ) -> QWidget:
	"""
	Callable utilisé par Napari pour le menu Plugins > PALM Tracer > Viewer 3D.

	- Ignore le viewer courant.
	- Crée une nouvelle fenêtre Napari 3D dédiée.
	- Retourne un QWidget stub (caché) juste pour satisfaire
	  l'API "widget plugin" de Napari.
	"""
	# Crée la nouvelle fenêtre 3D
	create_viewer3d()

	# Stub minimal pour Napari (sera docké, mais caché)
	stub = QWidget()
	stub.hide()
	return stub


##################################################
if __name__ == "__main__":
	import napari

	_v, _w = create_viewer3d()
	napari.run()  # Lance la boucle Qt gérée par Napari
