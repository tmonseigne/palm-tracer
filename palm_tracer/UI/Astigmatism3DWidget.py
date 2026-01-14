"""
Module contenant la classe :class:`Astigmatism3DWidget`, un outil minimaliste pour le calcul d'un modèle d’astigmatisme en lien avec la position axiale.

Ce widget offre une interface simple organisée en deux onglets : ``Compute Astigmatism Model``, ``Estimate Z``

Notes
-----
- Le widget est autonome : il peut être lancé directement (``python Astigmatism3DWidget.py``), utilisé dans PALMTracer ou dans un plugin externe.

.. todo::
   - Ajouter une visualisation (la ligne coloré avec ou sans un scatter des points ?)
   - Ajouter une métrique type MSE du modèle par rapport aux datas ?
"""

import os
import shutil
from typing import Optional

import pandas as pd
from qtpy.QtWidgets import (QApplication, QCheckBox, QDoubleSpinBox, QFileDialog, QLabel, QPushButton, QSpinBox,
							QTabWidget, QVBoxLayout, QWidget)

from palm_tracer.Processing import Palm
from palm_tracer.Processing.Astigmatism3D import DLL_REQUIRED_COLS, MODEL_ROWS, MODEL_COLS
from palm_tracer.Tools import print_error, print_warning
from palm_tracer.UI.Utils import add_setting_row, init_layout, make_form, make_group, make_tab, STYLESHEET_GENERAL, STYLESHEET_INFO

_alignment_windows = []  # pour garder une référence globale, éviter le Garbage Collector

class Astigmatism3DWidget(QWidget):
	"""
	Widget minimaliste pour le calcul d'un modèle d’astigmatisme en lien avec la position axiale et l'estimation d'une position axiale en fonction d'un modèle.

	Ce widget fournit deux onglets :
		- ``Compute Astigmatism Model`` :
			- Bouton pour charger un fichier de localisation contenant au moins les colonnes Sigma X, Sigma Y, Z.
			- Spin float pour la taille des pixel en micromètres (μm/px) avec 3 décimales.
			- Bouton pour lancer le calcul du modèle.

		- ``Estimate Z`` :
			- Bouton pour charger un fichier de localisation contenant au moins les colonnes Sigma X,Sigma Y.
			- Spin float pour la taille des pixel en micromètres (μm) avec 3 décimales.
			- Spin float pour la hauteur max sur Z.
			- Checkbox pour sauvegarder l'original dans un dossier backup.
			- Bouton pour lancer l'estimation.

	 La partie de droite sert à visualiser le modèle calculé ou chargé.
	"""

	##################################################
	def __init__(self, parent: Optional[QWidget] = None):
		"""
		Construit le widget et initialise l'interface.

		:param parent: Widget parent Qt, ou :obj:`None` si widget racine.
		"""
		super().__init__(parent)
		self.setWindowTitle("Astigmatism 3D Tool")

		self._palm = Palm()
		self._folder = ""
		self._filename: str = ""
		self._loc: Optional[pd.DataFrame] = None
		self._model: Optional[pd.DataFrame] = None

		self._init_ui()
		self._connect_signals()

	##################################################
	def _init_ui(self):
		"""Construit l'interface utilisateur (onglets + boutons) en conservant un style proche du Graph Viewer."""
		main_layout = QVBoxLayout(self)
		init_layout(main_layout)

		self._tabs = QTabWidget(self)

		# ---------- Onglet 1 : Compute Model ----------
		tab_compute, tab_layout = make_tab(self._tabs)
		grp, grp_layout = make_group(tab_compute, "Inputs")

		self._btn_load_compute = QPushButton("Load Localization file (CSV)", grp)
		self._btn_load_compute.setToolTip("The file must contain at least 3 columns : Sigma X, Sigma Y, Z")

		self._lbl_compute = QLabel("No file loaded", grp)
		self._lbl_compute.setStyleSheet(STYLESHEET_INFO)

		self._spin_px_compute = QDoubleSpinBox(grp, decimals=3, minimum=0.001, maximum=1, singleStep=0.010, value=0.160)
		self._spin_px_compute.setToolTip("Pixel size in micrometers.")

		form = make_form(None)
		add_setting_row(form, "Pixel Size (µm/px):", self._spin_px_compute)

		grp_layout.addWidget(self._btn_load_compute)
		grp_layout.addWidget(self._lbl_compute)
		grp_layout.addLayout(form)

		self._btn_compute = QPushButton("Compute model", tab_compute)
		self._btn_compute.setToolTip("Start calculating model coefficients from the localization file.")

		tab_layout.addWidget(grp)
		tab_layout.addWidget(self._btn_compute)
		tab_layout.addStretch(1)

		# ---------- Onglet 2 : Estimate Z ----------
		tab_estimate, tab_layout = make_tab(self._tabs)
		grp, grp_layout = make_group(tab_estimate, "Inputs")

		self._btn_load_loc_estimate = QPushButton("Load Localization file (CSV)", grp)
		self._btn_load_loc_estimate.setToolTip("The file must contain at least 3 columns : Sigma X, Sigma Y, Z")

		self._lbl_loc_estimate = QLabel("No file loaded", grp)
		self._lbl_loc_estimate.setStyleSheet(STYLESHEET_INFO)

		self._btn_load_model_estimate = QPushButton("Load Model file (CSV)", grp)
		self._btn_load_model_estimate.setToolTip("The file is a csv with 2 lines and 5 columns.")

		self._lbl_model_estimate = QLabel("No Model file loaded", grp)
		self._lbl_model_estimate.setStyleSheet(STYLESHEET_INFO)

		self._spin_px_estimate = QDoubleSpinBox(grp, decimals=3, minimum=0.001, maximum=1, singleStep=0.010, value=0.160)
		self._spin_px_estimate.setToolTip("Pixel size in micrometers.")

		self._spin_z_estimate = QSpinBox(grp, minimum=1, maximum=1000, singleStep=10, value=600)
		self._spin_z_estimate.setToolTip("Maximum absolute value of Z.")

		self._check_b_estimate = QCheckBox(grp)
		self._check_b_estimate.setChecked(True)
		self._check_b_estimate.setToolTip("Save original localisation file in backup folder.")

		form = make_form(None)
		add_setting_row(form, "Pixel Size (µm/px):", self._spin_px_estimate)
		add_setting_row(form, "Z Max (nm):", self._spin_z_estimate)
		add_setting_row(form, "Save Backup:", self._check_b_estimate)

		grp_layout.addWidget(self._btn_load_loc_estimate)
		grp_layout.addWidget(self._lbl_loc_estimate)
		grp_layout.addWidget(self._btn_load_model_estimate)
		grp_layout.addWidget(self._lbl_model_estimate)
		grp_layout.addLayout(form)

		self._btn_estimate = QPushButton("Estimate Z", tab_estimate)
		self._btn_estimate.setToolTip("Estimate Z for all points in localizaation file with the loaded model.")

		tab_layout.addWidget(grp)
		tab_layout.addWidget(self._btn_estimate)
		tab_layout.addStretch(1)

		# ---------- Ajout des onglets ----------
		self._tabs.addTab(tab_compute, "Compute Model")
		self._tabs.addTab(tab_estimate, "Estimate Z")

		main_layout.addWidget(self._tabs)

		# ---------- Style proche du GraphViewer ----------
		# On applique un style général aux QPushButton
		self.setStyleSheet(STYLESHEET_GENERAL)

	##################################################
	def _connect_signals(self):
		"""Connecte les signaux des boutons aux callbacks."""
		self._btn_load_compute.clicked.connect(self._on_load_loc)
		self._btn_compute.clicked.connect(self._on_compute)

		self._btn_load_loc_estimate.clicked.connect(self._on_load_loc)
		self._btn_load_model_estimate.clicked.connect(self._on_load_model)
		self._btn_estimate.clicked.connect(self._on_estimate)

	##################################################
	# Callbacks : pour l'instant uniquement des print()
	##################################################
	def _on_load_loc(self):
		"""Callback du bouton 'Load Localization file (CSV)'."""
		# --- boîte de dialogue pour sélectionner un .csv ---
		self._filename, _ = QFileDialog.getOpenFileName(self, "Select Localization CSV file", "", "CSV files (*.csv)")

		if not self._filename:
			print_warning("No file selected.")
			return

		# --- lecture du fichier ---
		try:
			print(f"Selected file: {self._filename}.")
			self._folder, self._basename = os.path.dirname(self._filename), os.path.basename(self._filename)  # dossier du fichier, nom + extension
			self._loc = pd.read_csv(self._filename)
		except Exception as e:
			self._loc = None
			print_error(f"Unable to read the CSV file : {e}.")
			return

		# --- vérification de la forme des données ---
		if not set(DLL_REQUIRED_COLS).issubset(self._loc.columns):
			print_error(f"The localization file is not in the correct format.\n"
						f"\tExpected format, at least columns: {', '.join(sorted(DLL_REQUIRED_COLS))}.\n"
						f"\tFound columns: {', '.join(self._loc.columns)}")
			self._loc = None
			return

		# --- mise à jour du label associé au bouton ---
		self._lbl_compute.setText(self._basename)
		self._lbl_compute.setToolTip(self._filename)
		self._lbl_loc_estimate.setText(self._basename)
		self._lbl_loc_estimate.setToolTip(self._filename)

		print(f"CSV loaded successfully. {len(self._loc)} points, {len(self._loc.columns)} columns")

	##################################################
	def _on_load_model(self):
		"""
		Callback du bouton 'Load coefficients file'.

		À l'issue de la lecture, les coefficients sont stockés dans ``self._factors``
		sous la forme d'un tableau NumPy de taille ``(2, 10)`` et de type :class:`numpy.float64`.
		"""
		# --- boîte de dialogue pour sélectionner un fichier .txt ---
		filename, _ = QFileDialog.getOpenFileName(self, "Select Model CSV file", "", "CSV files (*.csv)")

		if not filename:
			print_warning("No model file selected.")
			return

		# --- lecture du fichier ---
		try:
			print(f"Selected file: {filename}.")
			self._model = pd.read_csv(filename, index_col=0)
		except Exception as e:
			self._model = None
			print_error(f"Unable to read the model file: {e}.")
			return

		# --- vérification de la forme des données ---
		if len(self._model) != len(MODEL_ROWS) or len(self._model.columns) != len(MODEL_COLS):
			self._model = None
			print_error(f"The model file is not in the correct format. Expected format: two lines of five values (2x5).")
			return

		# --- mise à jour du label de statut ---
		basename = os.path.basename(filename)
		self._lbl_model_estimate.setText(basename)
		self._lbl_model_estimate.setToolTip(filename)

		print("Model loaded successfully.")

	##################################################
	def _on_compute(self):
		"""Callback du bouton 'Compute coefficients'."""
		if self._loc is None: print("Can't Compute model without correct file loaded.")
		else:
			pixel_size = self._spin_px_compute.value()
			points = self._loc.loc[:, DLL_REQUIRED_COLS].to_numpy(dtype=float, copy=True)
			self._model = self._palm.astigmatism_3d_calibration(points, pixel_size)
			model = pd.DataFrame(self._model, columns=MODEL_COLS, index=MODEL_ROWS)
			model.to_csv(os.path.join(self._folder, "astigmatism_3d_model.csv"))
			print("Model saved successfully.")

	##################################################
	def _on_estimate(self):
		"""Callback du bouton 'Start alignment'."""
		if self._loc is None: print("Can't estimate without correct localization file loaded.")
		elif self._model is None: print("Can't estimate without correct model file loaded.")
		else:
			if self._check_b_estimate.isChecked():
				backup_dir = os.path.join(self._folder, "backup")
				os.makedirs(backup_dir, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)
				name, ext = os.path.splitext(self._basename)  # Séparation extension et nom de fichier
				backup_filename = os.path.join(backup_dir, self._basename)
				i = 1
				# si le fichier existe déjà, on ajoute un _1 à la fin si _1 existe _2......
				while os.path.exists(backup_filename):
					backup_filename = os.path.join(backup_dir, f"{name}_{i}{ext}")
					i += 1
				shutil.copy2(self._filename, backup_filename)
				print(f"Backup done at {backup_filename}.")

			pixel_size = self._spin_px_estimate.value()
			z_max = self._spin_z_estimate.value()
			points = self._loc.loc[:, DLL_REQUIRED_COLS[:-1]].to_numpy(dtype=float, copy=True)
			estimated_z = self._palm.astigmatism_3d_estimation(points, pixel_size, self._model.to_numpy(), z_max)
			self._loc[DLL_REQUIRED_COLS[-1]] = estimated_z
			self._loc.to_csv(self._filename)
			print("Localization file with estimation saved successfully.")


##################################################
def open_astigmatism3d():  # pragma: no cover
	"""
	Ouvre la fenêtre d'alignement en mode autonome.

	Cette fonction est utilisée par le plugin napari comme point d'entrée :
	elle crée simplement un :class:`Astigmatism3DWidget`, l'affiche et le renvoie. Le widget ne dépend pas de napari et s'ouvre dans sa propre fenêtre.
	"""
	widget = Astigmatism3DWidget()
	widget.resize(500, 250)
	widget.show()
	_alignment_windows.append(widget)  # éviter que Python le détruise en le stockant
	# Stub minimal pour napari (c'est moche il créé un widget vide, je prefere laisser sans rien avec un Warning)
	# stub = QWidget()
	# stub.hide()
	# return stub

##################################################
if __name__ == "__main__":  # pragma: no cover
	import sys

	app = QApplication(sys.argv)
	w = Astigmatism3DWidget()
	w.resize(500, 250)
	w.show()
	sys.exit(app.exec_())
