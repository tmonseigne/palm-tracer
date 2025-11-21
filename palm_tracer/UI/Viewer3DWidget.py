"""
Widget d'affichage 3D pour napari permettant de charger un fichier CSV et de visualiser les points en 3D
avec ajustements interactifs des échelles et de la taille des points.

Ce widget ajoute dans le dock de napari :
	- un bouton de chargement de fichier CSV,
	- trois champs pour contrôler les échelles en XY et Z et la taille des points,
	- une option permettant d'exclure les points avec intensité nulle,
	- un calque napari Points mis à jour dynamiquement.

Le CSV doit contenir les colonnes ``"X"``, ``"Y"``, ``"Z"`` et ``"Integrated Intensity"``.
"""
import napari
import pandas as pd
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QFileDialog, QFormLayout, QPushButton, QWidget

from palm_tracer.Settings.Types import CheckBox, SpinFloat


class Viewer3DWidget(QWidget):  # pragma: no cover
	"""
	Widget d'affichage 3D pour un viewer napari.

	Ce widget permet :
		- de charger un fichier CSV contenant des coordonnées 3D
		- d'ajuster l'échelle XY et Z
		- de modifier la taille des points
		- d'activer ou non la suppression des points d'intensité nulle
		- de créer ou mettre à jour un calque de type :class:`napari.layers.Points`.

	:param viewer: Instance du viewer napari où sera ajouté le calque 3D.
	:type viewer: :class:`napari.Viewer`
	"""

	##################################################
	def __init__(self, viewer: napari.Viewer):
		"""
		Initialise le widget et configure l'interface graphique (boutons, champs numériques, checkbox).

		La création du calque napari se fait plus tard dans :meth:`update_layer` lorsqu'un fichier CSV est chargé.

		:param viewer: Viewer napari cible.
		:type viewer: :class:`napari.Viewer`
		"""
		super().__init__()
		self.viewer = viewer
		self.points_layer = None
		self.data = None  # DataFrame d'origine
		self.z_scale = 1.0
		self._widget = QWidget()
		layout = QFormLayout(self._widget)
		layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # Définir l'alignement du calque en haut.

		self.setLayout(layout)

		# Bouton de chargement CSV
		btn = QPushButton("Load CSV")
		btn.clicked.connect(self.load_csv)
		layout.addWidget(btn)

		# Spinbox taille des points
		self.size_spin = SpinFloat("Point Size", 0.5, 0.1, 10, 0.1, 1)
		self.size_spin.connect(self.update_layer)
		layout.addRow(self.size_spin.layout)

		# Spinbox échelle Z
		self.xy_scale_spin = SpinFloat("XY Scale", 1.0, 0.0, 1000, 1.0, 1)
		self.xy_scale_spin.connect(self.update_layer)
		layout.addRow(self.xy_scale_spin.layout)

		# Spinbox échelle Z
		self.z_scale_spin = SpinFloat("Z Scale", 1.0, 0.0, 1000, 1.0, 1)
		self.z_scale_spin.connect(self.update_layer)
		layout.addRow(self.z_scale_spin.layout)

		self.outliers = CheckBox("Remove Outliers", False)
		self.outliers.connect(self.update_layer)
		layout.addRow(self.outliers.layout)

	##################################################
	def load_csv(self):
		"""
		Ouvre une boîte de dialogue pour sélectionner un fichier ``.csv`` et charge les données associées dans un :class:`pandas.DataFrame`.

		Le fichier doit contenir les colonnes : ``"X"``, ``"Y"``, ``"Z"``, ``"Integrated Intensity"``

		Si un calque existe déjà, il est supprimé avant la création du nouveau.

		Cette méthode déclenche ensuite :meth:`update_layer` pour créer le calque 3D.
		"""
		filename, _ = QFileDialog.getOpenFileName(self, "Load CSV", ".", "Fichiers CSV (*.csv)")
		if not filename: return
		df = pd.read_csv(filename)
		if not all(col in df.columns for col in ["X", "Y", "Z", "Integrated Intensity"]):
			print("Le fichier doit contenir les colonnes X, Y, Z et Integrated Intensity.")
			return

		self.data = df.copy()
		# Supprimer le calque précédent s'il existe, (le nombre de points peu changer
		if self.points_layer is not None:
			try: self.viewer.layers.remove(self.points_layer)
			except Exception as e: print(f"Erreur lors de la suppression de l'ancien layer : {e}")
			self.points_layer = None
		self.update_layer()

	##################################################
	def update_layer(self):
		"""
		Crée ou met à jour le calque de points 3D dans le viewer napari.

		Transformations appliquées :
			- réorganisation des coordonnées sous la forme ``(Z, Y, X)``
			- mise à l'échelle par les valeurs choisies dans les widgets
			- suppression éventuelle des points dont ``Integrated Intensity == 0``
			- mise à jour dynamique du calque existant ou création d'un nouveau

		Si aucune donnée n'est encore chargée, la méthode ne fait rien.
		"""
		if self.data is None: return

		scale_xy = self.xy_scale_spin.get_value()
		scale_z = self.z_scale_spin.get_value()
		coords = self.data[["Z", "Y", "X"]].copy().to_numpy()
		coords[:, 0] *= scale_z  # Z * scale
		coords[:, 1] *= scale_xy  # Y * scale
		coords[:, 2] *= scale_xy  # X * scale

		if self.outliers.get_value(): coords = coords[self.data["Integrated Intensity"] != 0]

		# Ajout ou mise à jour du calque
		if self.points_layer is None:
			self.points_layer = self.viewer.add_points(coords, size=self.size_spin.get_value(), name="Points 3D", ndim=3)
		else:
			self.points_layer.data = coords
			self.points_layer.size = self.size_spin.get_value()


##################################################
if __name__ == "__main__":  # pragma: no cover
	import napari

	viewer = napari.Viewer(ndisplay=3)								  # Crée le viewer napari
	viewer.title = "3D Viewer"										  # Modifier le titre de la fenêtre
	viewer.window.main_menu.setVisible(False)						  # Cacher la barre de menu
	w = Viewer3DWidget(viewer)										  # Crée ton widget en lui passant le viewer
	viewer.window.add_dock_widget(w, name="Viewer 3D", area="right")  # L'ajoute comme dock widget dans la fenêtre napari
	napari.run()													  # Lance la boucle Qt gérée par napari
