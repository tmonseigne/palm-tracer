"""
Widget d'affichage Haute Résolution pour Napari permettant de charger un dossier de résultats et de visualiser les points.

Ce widget ajoute dans le dock de Napari :
	- un bouton de chargement du dossier,
	- trois champs pour contrôler les paramètres de visualisation Haute Résolution,
	- un calque Napari Points/trajectoires mis à jour dynamiquement.
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
	Widget d'affichage HR pour un viewer Napari.

	Ce widget permet :
		- de charger un dossier,
		- de modifier la taille des points
		- de modifier le facteur d'agrandissement
		- de sélectionner la source d'information permettant la coloration des points
		- de créer ou mettre à jour un calque de type :class:`napari.layers.Points` ou :class:`napari.layers.Tracks`.
		- de sauvegarder une image PNG résultat de la visualisation.

	**Remarque** : peut être lancé directement avec la commande ``napari -w palm-tracer "Viewer HR"``

	:param viewer: Instance du viewer Napari où sera ajouté le calque HR.
	:param palmtracer: Instance PALMTracer à lier.
	"""

	##################################################
	def __init__(self, viewer: napari.Viewer, palmtracer: PALMTracer):
		"""
		Initialise le widget et configure l'interface graphique (boutons, champs numériques, checkbox).

		La création du calque Napari se fait plus tard dans :meth:`update_layer` lorsqu'un fichier CSV est chargé.

		:param viewer: Viewer Napari cible.
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
		self.size_spin = SpinFloat("Point Size", "", 1, [0.1, 10], 0.1, 1)
		self.size_spin.attach_to_form(layout)

		# Spinbox facteur d'agrandissement
		self.upscale_spin = SpinInt("Upscale Ratio", "", 4, [1, 100], 2)
		self.upscale_spin.attach_to_form(layout)

		# Combo box pour la source
		self.type_cmb = Combo("Visualization Type", "", 0, ["Localization", "Tracks"])
		self.type_cmb.attach_to_form(layout)
		self.type_cmb.connect(self.update_source)

		self.source_cmb = Combo("Color Source")
		self.source_cmb.attach_to_form(layout)

		self.color_cmb = Combo("PNG Color Map", "", 0, ["grayscale", "viridis", "magma", "plasma", "inferno", "cividis", "turbo"])
		self.color_cmb.attach_to_form(layout)

		btn_generate = QPushButton("Generate")
		btn_generate.clicked.connect(self.generate)
		btn_save = QPushButton("Save")
		btn_save.clicked.connect(self.save)
		# Ligne de boutons
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
		"""Mets à jour les sources disponibles pour définir l'intensité des points."""
		with self.source_cmb.signal_blocked():
			data_type = self.type_cmb.value
			src = HR_LOC_SOURCE[1:] if data_type == 0 else HR_TRC_SOURCE[1:]
			self.source_cmb.update_box(src)
			self.color_cmb.value = data_type  # Place la color map sur grayscale par défaut pour les localisations et sur viridis pour les trajectoires.

	##################################################
	def generate(self):
		"""Crée ou mets à jour le calque de points/trajectoires HR l'image de visualisation dans le viewer Napari."""
		path, stack, suffix = self._pt.path, self._pt.stack, self._pt.suffix
		if not path or not Path(path).is_dir():
			show_warning(f"The destination path '{path}' is invalid.")
			return

		if stack is None:
			show_warning(f"No stack loaded.")
			return

		depth, height, width = stack.shape

		# On supprime les calques (la mise à jour n'est pas optimale sous Napari).
		try: self.viewer.layers.clear()
		except Exception as e: show_warning(f"Error when deleting old layers: {e}")

		data_type = self.type_cmb.value
		data_source = self.source_cmb.value
		upscale = self.upscale_spin.value
		point_size = self.size_spin.value
		color = self.color_cmb.items[self.color_cmb.value]

		if data_type == 0:  # Localisations
			loc = self._pt.localizations
			if loc.empty:
				show_warning("No localization file available.")
				return
			points = loc[["Y", "X"]].to_numpy() * upscale
			layer = self.viewer.add_points(points, size=point_size, face_color="lime", name="Points")

			src = HR_LOC_SOURCE[data_source + 1]
			self.visualization = render_hr_image(width, height, upscale, loc[["X", "Y", src]].to_numpy())

		else:  # Trajectoires
			trc = self._pt.tracks
			if trc.empty:
				show_warning("No tracking file available.")
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
			show_info("Saving the image file.")


##################################################
def create_viewerhr(palmtracer: PALMTracer) -> napari.Viewer:  # pragma: no cover — Aucun lancement de fenêtre sans controle en CI
	"""
	Crée une nouvelle fenêtre Napari HR, sans menu,
	et y ajoute le ViewerHRWidget docké à droite.

	Cette fonction NE lance PAS napari.run() : elle est faite
	pour être appelée depuis un plugin, donc dans une appli Qt déjà active.
	"""
	viewer = napari.Viewer(ndisplay=2)  # .									 Crée le viewer HR napari
	viewer.title = "HR Viewer"  # .											 Modifier le titre de la fenêtre
	viewer.window.main_menu.setVisible(False)  # .							 Cacher la barre de menu
	widget = ViewerHRWidget(viewer, palmtracer)  # .						 Crée le widget en lui passant le viewer
	viewer.window.add_dock_widget(widget, name="Viewer HR", area="right")  # L'ajoute comme dock widget dans la fenêtre napari
	return viewer


##################################################
def open_viewerhr(_viewer: "napari.viewer.Viewer" = None, ) -> QWidget:  # pragma: no cover — Aucun lancement de fenêtre sans controle en CI
	"""
	Callable utilisé par Napari pour le menu Plugins > PALM Tracer > Viewer HR.

	- Ignore le viewer courant.
	- Crée une nouvelle fenêtre Napari HR dédiée.
	- Retourne un QWidget stub (caché) juste pour satisfaire
	  l'API "widget plugin" de Napari.
	"""
	# Crée la nouvelle fenêtre HR
	pt = PALMTracer()
	create_viewerhr(pt)

	# Stub minimal pour Napari (sera docké, mais caché)
	stub = QWidget()
	stub.hide()
	return stub


##################################################
if __name__ == "__main__":  # pragma: no cover — Aucun appel de fichier lors des tests pour le code coverage
	import napari

	app = QApplication.instance() or QApplication([])
	_pt = PALMTracer()
	_v = create_viewerhr(_pt)
	napari.run()  # Lance la boucle Qt gérée par Napari
