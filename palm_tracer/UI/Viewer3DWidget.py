import napari
import pandas as pd
from qtpy.QtWidgets import QDoubleSpinBox, QFileDialog, QPushButton, QVBoxLayout, QWidget, QFormLayout, QCheckBox, QFormLayout, QLabel, QWidget
from qtpy.QtCore import Qt

from palm_tracer.Settings.Types import CheckBox, SpinFloat


class Viewer3DWidget(QWidget):  # pragma: no cover
	##################################################
	def __init__(self, viewer: napari.Viewer):
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
		layout.addRow(self.outliers.layout)

	##################################################
	def load_csv(self):
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
		if self.data is None:
			return

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
