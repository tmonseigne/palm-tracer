"""
Widget d'affichage Haute Résolution pour napari permettant de charger un dossier de résultats et de visualiser les points.

Ce widget ajoute dans le dock de napari :
	- un bouton de chargement du dossier,
	- trois champs pour contrôler les paramètres de visualisation Haute Résolution,
	- un calque napari Points/trajectoires mis à jour dynamiquement.
	- Un boutotn pour sauvegarder une image PNG résultat
"""
from pathlib import Path

import napari
import numpy as np
from napari.utils.notifications import show_info, show_warning
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QApplication, QFileDialog, QFormLayout, QHBoxLayout, QPushButton, QWidget

from palm_tracer.PALMTracer import PALMTracer
from palm_tracer.Processing.Visualization import render_hr_image, render_tracks_image
from palm_tracer.Settings.Groups.VisualizationHR import HR_LOC_SOURCE, HR_TRC_SOURCE
from palm_tracer.Settings.Types import Combo, SpinFloat, SpinInt
from palm_tracer.Tools.FileIO import grayscale_to_color, save_png


class ViewerHRWidget(QWidget):
	"""
	Widget d'affichage HR pour un viewer napari.

	Ce widget permet :
		- de charger un dossier,
		- de modifier la taille des points
		- de modifier le facteur d'agrandissement
		- de sélectionner la source d"information permettant la coloration des points
		- de créer ou mettre à jour un calque de type :class:`napari.layers.Points` ou :class:`napari.layers.Tracks`.
		- de sauvegarder une image PNG résultat de la visualisation.

	**Remarque** : peut être lancé directement avec la commande ``napari -w palm-tracer "Viewer HR"``

	:param viewer: Instance du viewer napari où sera ajouté le calque HR.
	:type viewer: :class:`napari.Viewer`
	"""

	##################################################
	def __init__(self, viewer: napari.Viewer, palmtracer: PALMTracer):
		"""
		Initialise le widget et configure l'interface graphique (boutons, champs numériques, checkbox).

		La création du calque napari se fait plus tard dans :meth:`update_layer` lorsqu'un fichier CSV est chargé.

		:param viewer: Viewer napari cible.
		:type viewer: :class:`napari.Viewer`
		"""
		super().__init__()
		self.viewer = viewer
		self._stack: np.ndarray = np.zeros((1, 1), dtype=np.uint16)
		self.visualization: np.ndarray = np.zeros((1, 1), dtype=np.uint16)
		self._filename: str = ""
		self._pt = palmtracer
		self._widget = QWidget()
		layout = QFormLayout(self._widget)
		layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # Définir l'alignement du calque en haut.

		self.setLayout(layout)

		# Bouton de chargement du dossier
		btn = QPushButton("Select Folder")
		btn.clicked.connect(self.load_folder)
		layout.addWidget(btn)

		# Spinbox taille des points
		self.size_spin = SpinFloat("Point Size", 1, [0.1, 10], 0.1, 1)
		layout.addRow(self.size_spin.layout)

		# Spinbox facteur d'agrandissement
		self.upscale_spin = SpinInt("Upscale Ratio", 4, [1, 100], 2)
		layout.addRow(self.upscale_spin.layout)

		# Combo box pour la source
		self.type_cmb = Combo("Visualization Type", 0, ["Localization", "Tracks"])
		self.type_cmb.connect(self.update_source)
		layout.addRow(self.type_cmb.layout)

		self.source_cmb = Combo("Color Source")
		layout.addRow(self.source_cmb.layout)

		self.color_cmb = Combo("PNG Color Map", 0, ["grayscale", "viridis", "magma", "plasma", "inferno", "cividis", "turbo"])
		layout.addRow(self.color_cmb.layout)

		btn_generate = QPushButton("Generate")
		btn_generate.clicked.connect(self.generate)
		btn_save = QPushButton("Save")
		btn_save.clicked.connect(self.save)
		# Ligne de bouttons
		action_row = QHBoxLayout()
		action_row.addWidget(btn_generate)
		action_row.addWidget(btn_save)
		# Encapsulation dans un QWidget
		action_widget = QWidget()
		action_widget.setLayout(action_row)
		# Ajout au layout
		layout.addRow(action_widget)
		self.update_source()

		# Chargement et génération par défaut (si l'objet palmtracer est déjà configuré avec une pile, il lancera une première génération)
		self._pt.load()
		self.generate()

	##################################################
	def load_folder(self):
		"""
		Ouvre une boîte de dialogue pour sélectionner un dossier contenant les résultats d'une analyse PALMTracer.

		Cette méthode déclenche ensuite :meth:`generate` pour créer le calque HR.
		"""
		path = QFileDialog.getExistingDirectory(self, "Load Folder", ".")
		self._pt.load(path)
		self.generate()

	##################################################
	def update_source(self):
		"""Met à jour les sources disponibles pour définir l'intensité des points. """
		with self.source_cmb.signal_blocked():
			data_type = self.type_cmb.get_value()
			src = HR_LOC_SOURCE[1:] if data_type == 0 else HR_TRC_SOURCE[1:]
			self.source_cmb.items = src
			self.source_cmb.update_box()
			self.color_cmb.set_value(data_type)  # Place la color map sur grayscale par défaut pour les localisations et sur viridis pour les trajectoires.

	##################################################
	def generate(self):
		"""Crée ou met à jour le calque de points/trajectoires HR l'image de visualisation dans le viewer napari."""
		path, stack, suffix = self._pt._path, self._pt._stack, self._pt._suffix
		if not path or not Path(path).is_dir():
			show_warning(f"Le chemin de destination \"{path}\" n'est pas valide.")
			return

		if stack is None:
			show_warning(f"Aucune Pile de chargée.")
			return

		depth, height, width = stack.shape

		# On supprime les calques (la mise à jour n'est pas optimale sous Napari)
		try: self.viewer.layers.clear()
		except Exception as e: show_warning(f"Erreur lors de la suppression des anciens calques : {e}")

		data_type = self.type_cmb.get_value()
		data_source = self.source_cmb.get_value()
		upscale = self.upscale_spin.get_value()
		point_size = self.size_spin.get_value()
		color = self.color_cmb.items[self.color_cmb.get_value()]

		if data_type == 0:  # Localisations
			loc = self._pt.localizations
			if loc.empty:
				show_warning("Aucun fichier de localisation disponible.")
				return
			points = loc[["Y", "X"]].to_numpy() * upscale
			layer = self.viewer.add_points(points, size=point_size, face_color="lime", name="Points")

			src = HR_LOC_SOURCE[data_source + 1]
			self.visualization = render_hr_image(width, height, upscale, loc[["X", "Y", src]].to_numpy())

		else:  # Trajectoires
			trc = self._pt.tracks
			if trc.empty:
				show_warning("Aucun fichier de trajectoires disponible.")
				return
			tracks_data = trc[["Track", "Plane", "Y", "X"]].to_numpy(dtype=float)
			tracks_data[:, 2:4] *= upscale
			layer = self.viewer.add_tracks(tracks_data, name="Tracks", blending="translucent")

			src = HR_TRC_SOURCE[data_source + 1]
			trc = self._pt.add_color_to_tracks(trc, src)
			trc.to_csv(f"{path}/tracking_hr_color-{suffix}.csv", index=False)
			self.visualization = render_tracks_image(width, height, upscale, trc)

		layer.editable = False
		if color != "grayscale": self.visualization = grayscale_to_color(self.visualization, color)
		self._filename = f"{path}/visualization_{data_type}_x{upscale}_{src}-{suffix}.png"
		layer = self.viewer.add_image(self.visualization, name="Visualization", visible=False)
		self.viewer.layers.move(self.viewer.layers.index(layer), 0)

	##################################################
	def save(self):
		"""Créé une image PNG de la visualisation actuelle."""
		if self._filename:
			save_png(self.visualization, self._filename)
			show_info("Sauvegarde du fichier image.")


##################################################
def create_viewerhr(palmtracer: PALMTracer) -> napari.Viewer:  # pragma: no cover
	"""
	Crée une nouvelle fenêtre napari HR, sans menu,
	et y ajoute le ViewerHRWidget docké à droite.

	Cette fonction NE lance PAS napari.run() : elle est faite
	pour être appelée depuis un plugin, donc dans une appli Qt déjà active.
	"""
	viewer = napari.Viewer(ndisplay=2)									   # Crée le viewer HR napari
	viewer.title = "HR Viewer"											   # Modifier le titre de la fenêtre
	viewer.window.main_menu.setVisible(False)							   # Cacher la barre de menu
	widget = ViewerHRWidget(viewer, palmtracer)							   # Crée le widget en lui passant le viewer
	viewer.window.add_dock_widget(widget, name="Viewer HR", area="right")  # L'ajoute comme dock widget dans la fenêtre napari
	return viewer


##################################################
def open_viewerhr(_viewer: "napari.viewer.Viewer" = None, ) -> QWidget:  # pragma: no cover
	"""
	Callable utilisé par napari pour le menu Plugins > PALM Tracer > Viewer HR.

	- Ignore le viewer courant.
	- Crée une nouvelle fenêtre napari HR dédiée.
	- Retourne un QWidget stub (caché) juste pour satisfaire
	  l'API "widget plugin" de napari.
	"""
	# Crée la nouvelle fenêtre HR
	pt = PALMTracer()
	create_viewerhr(pt)

	# Stub minimal pour napari (sera docké, mais caché)
	stub = QWidget()
	stub.hide()
	return stub


##################################################
if __name__ == "__main__":  # pragma: no cover
	import napari

	app = QApplication.instance() or QApplication([])
	_pt = PALMTracer()
	_v = create_viewerhr(_pt)
	napari.run()  # Lance la boucle Qt gérée par napari
