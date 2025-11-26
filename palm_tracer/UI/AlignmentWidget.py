"""
Module contenant la classe :class:`AlignmentWidget`, un outil minimaliste pour la gestion de l’alignement géométrique entre acquisitions dans PALMTracer.

Ce widget offre une interface simple organisée en deux onglets : ``Compute Alignment Coefficients``, ``Apply Alignment``

Fonctionnalités principales
---------------------------
- Interface légère en PySide6/PyQt6 basée sur des :class:`QTabWidget`, :class:`QGroupBox` et :class:`QPushButton`.
- Gestion simple des entrées (sélection de fichiers TIFF / TXT via :class:`QFileDialog`).
- Chargement des images via :func:`palm_tracer.Tools.open_tif` et sauvegarde via :func:`palm_tracer.Tools.save_tif`.
- Chargement des coefficients d’alignement sous forme d’un tableau NumPy de taille ``(2, 10)``.
- Application de l’alignement via :meth:`Palm.align`, issue du module :mod:`palm_tracer.Processing`.

Notes
-----
- Le widget est autonome : il peut être lancé directement (``python AlignmentWidget.py``), utilisé dans PALMTracer ou dans un plugin externe.

.. todo::
   - Implémenter la méthode de calcul automatique des coefficients (méthode interne PALMTracer actuelle).
   - Prévoir une visualisation intermédiaire (overlay, difference map).
"""

import os
from typing import Optional

import numpy as np
from qtpy.QtWidgets import QApplication, QFileDialog, QGroupBox, QHBoxLayout, QLabel, QPushButton, QSpinBox, QTabWidget, QVBoxLayout, QWidget

from palm_tracer.Processing import Palm
from palm_tracer.Tools import open_tif, print_error, print_warning, save_tif

_alignment_windows = []  # pour garder une référence globale, éviter le Garbage Collector

class AlignmentWidget(QWidget):
	"""
	Widget minimaliste pour la gestion de l'alignement entre acquisitions.

	Ce widget fournit deux onglets :
		- ``Compute Alignment Coefficients`` :
			- Bouton pour charger un fichier TIFF contenant une seule image, composée de deux vues placées côte à côte (référence / déformation).
			- Bouton pour lancer le calcul des coefficients.

		- ``Apply Alignment`` :
			- Bouton pour charger un fichier TIFF à corriger.
			- Bouton pour charger un fichier de coefficients.
			- Bouton pour lancer l'alignement.
	"""

	##################################################
	def __init__(self, parent: Optional[QWidget] = None):
		"""
		Construit le widget et initialise l'interface.

		:param parent: Widget parent Qt, ou :obj:`None` si widget racine.
		"""
		super().__init__(parent)
		self.setWindowTitle("Alignment Tool")

		self._palm = Palm()
		self._stack: Optional[np.ndarray] = None
		self._coefs: Optional[np.ndarray] = None

		self._lbl_tif_compute: Optional[QLabel] = None
		self._lbl_tif_apply: Optional[QLabel] = None
		self._lbl_coef_apply: Optional[QLabel] = None

		self._spin_upscale: Optional[QSpinBox] = None

		self._init_ui()
		self._connect_signals()

	##################################################
	def _init_ui(self):
		"""Construit l'interface utilisateur (onglets + boutons) en conservant un style proche du Graph Viewer."""
		main_layout = QVBoxLayout(self)
		main_layout.setContentsMargins(5, 5, 5, 5)
		main_layout.setSpacing(5)

		self._tabs = QTabWidget(self)

		# ---------- Onglet 1 : Compute Alignment Coefficients ----------
		tab_compute = QWidget(self)
		tab_compute_layout = QVBoxLayout(tab_compute)
		tab_compute_layout.setContentsMargins(10, 10, 10, 10)
		tab_compute_layout.setSpacing(10)

		grp_compute_input = QGroupBox("Input image", tab_compute)
		grp_compute_layout = QVBoxLayout(grp_compute_input)
		grp_compute_layout.setContentsMargins(10, 10, 10, 10)
		grp_compute_layout.setSpacing(6)

		self._btn_load_tif_compute = QPushButton("Load TIFF file", grp_compute_input)
		self._btn_load_tif_compute.setToolTip(
				"The file must contain a single image (a single frame) composed of two regions placed side by side:\n"
				"- on the left: the reference image.\n"
				"- on the right: the distorted image."
				)

		self._lbl_tif_compute = QLabel("No file loaded", grp_compute_input)
		self._lbl_tif_compute.setStyleSheet("color: #666666; font-style: italic; padding: 2px;")

		grp_compute_layout.addWidget(QLabel("Input image for coefficient calculation:"))
		grp_compute_layout.addWidget(self._btn_load_tif_compute)
		grp_compute_layout.addWidget(self._lbl_tif_compute)

		grp_compute_action = QGroupBox("Action", tab_compute)
		grp_action_layout = QVBoxLayout(grp_compute_action)
		grp_action_layout.setContentsMargins(10, 10, 10, 10)
		grp_action_layout.setSpacing(6)

		self._btn_compute_coeffs = QPushButton("Compute coefficients (not implemented)", grp_compute_action)
		self._btn_compute_coeffs.setToolTip("Start calculating alignment coefficients from the loaded image.")

		grp_action_layout.addWidget(self._btn_compute_coeffs)

		tab_compute_layout.addWidget(grp_compute_input)
		tab_compute_layout.addWidget(grp_compute_action)
		tab_compute_layout.addStretch(1)

		# ---------- Onglet 2 : Apply Alignment ----------
		tab_apply = QWidget(self)
		tab_apply_layout = QVBoxLayout(tab_apply)
		tab_apply_layout.setContentsMargins(10, 10, 10, 10)
		tab_apply_layout.setSpacing(10)

		grp_apply_inputs = QGroupBox("Inputs", tab_apply)
		grp_apply_layout = QVBoxLayout(grp_apply_inputs)
		grp_apply_layout.setContentsMargins(10, 10, 10, 10)
		grp_apply_layout.setSpacing(6)

		self._btn_load_tif_apply = QPushButton("Load TIFF file", grp_apply_inputs)
		self._btn_load_tif_apply.setToolTip("Load the TIFF file to which the alignment should be applied.")

		self._btn_load_coef_apply = QPushButton("Load coefficients file", grp_apply_inputs)
		self._btn_load_coef_apply.setToolTip("Load the file containing the alignment coefficients.")

		self._lbl_tif_apply = QLabel("No TIFF file loaded", grp_apply_inputs)
		self._lbl_tif_apply.setStyleSheet("color: #666666; font-style: italic; padding: 2px;")

		self._lbl_coef_apply = QLabel("No coefficients file loaded", grp_apply_inputs)
		self._lbl_coef_apply.setStyleSheet("color: #666666; font-style: italic; padding: 2px;")

		hl_upscale = QHBoxLayout()
		label_upscale = QLabel("Upscaling factor:", grp_apply_inputs)
		self._spin_upscale = QSpinBox(grp_apply_inputs)
		self._spin_upscale.setMinimum(1)
		self._spin_upscale.setValue(1)
		self._spin_upscale.setToolTip("Integer upscaling factor for the output aligned image (1 = no upscaling).")

		hl_upscale.addWidget(label_upscale)
		hl_upscale.addWidget(self._spin_upscale)
		hl_upscale.addStretch(1)

		grp_apply_layout.addWidget(QLabel("Input files for alignment:"))
		grp_apply_layout.addWidget(self._btn_load_tif_apply)
		grp_apply_layout.addWidget(self._lbl_tif_apply)
		grp_apply_layout.addWidget(self._btn_load_coef_apply)
		grp_apply_layout.addWidget(self._lbl_coef_apply)
		grp_apply_layout.addLayout(hl_upscale)

		grp_apply_action = QGroupBox("Action", tab_apply)
		grp_apply_action_layout = QVBoxLayout(grp_apply_action)
		grp_apply_action_layout.setContentsMargins(10, 10, 10, 10)
		grp_apply_action_layout.setSpacing(6)

		self._btn_start_alignment = QPushButton("Start alignment", grp_apply_action)
		self._btn_start_alignment.setToolTip("Applies alignment to the image using the loaded coefficients.")

		grp_apply_action_layout.addWidget(self._btn_start_alignment)

		tab_apply_layout.addWidget(grp_apply_inputs)
		tab_apply_layout.addWidget(grp_apply_action)
		tab_apply_layout.addStretch(1)

		# ---------- Ajout des onglets ----------
		self._tabs.addTab(tab_compute, "Compute Alignment Coefficients")
		self._tabs.addTab(tab_apply, "Apply Alignment")

		main_layout.addWidget(self._tabs)

		# ---------- Style proche du GraphViewer ----------
		# On applique un style général aux QPushButton inspiré du bloc "Source"
		self.setStyleSheet("""
			QPushButton { border: 1px solid #c7c7c7; padding: 5px; background: #f7f7f7; }
			QPushButton + QPushButton { border-left: none; } /* fusion visuelle */
			QPushButton:first-child { border-top-left-radius: 5px; border-bottom-left-radius: 5px; }
			QPushButton:last-child { border-top-right-radius: 5px; border-bottom-right-radius: 5px; }
			QPushButton:pressed { background: #e9eff7; border-color: #6aa0e8; }
			QPushButton:checked	{ background: #e9eff7; border-color: #6aa0e8; }
			QPushButton:disabled { color: #999; background: #fafafa; }
		""")

	##################################################
	def _connect_signals(self):
		"""Connecte les signaux des boutons aux callbacks."""
		self._btn_load_tif_compute.clicked.connect(self._on_load_tif)
		self._btn_compute_coeffs.clicked.connect(self._on_compute_coeffs)

		self._btn_load_tif_apply.clicked.connect(self._on_load_tif)
		self._btn_load_coef_apply.clicked.connect(self._on_load_coef)
		self._btn_start_alignment.clicked.connect(self._on_start_alignment)

	##################################################
	# Callbacks : pour l'instant uniquement des print()
	##################################################
	def _on_load_tif(self):
		"""Callback du bouton 'Load TIFF file'."""
		# --- boîte de dialogue pour sélectionner un .tif ---
		filename, _ = QFileDialog.getOpenFileName(self, "Select TIFF file", "", "TIFF images (*.tif *.tiff)")

		if not filename:
			print_warning("No TIFF file selected.")
			return

		# --- lecture du fichier ---
		try:
			print(f"Selected file: {filename}.")
			folder, basename = os.path.dirname(filename), os.path.basename(filename)  # dossier du fichier, nom + extension
			name, ext = os.path.splitext(basename)  # séparation nom / extension
			self._output_filename = os.path.join(folder, f"{name}_aligned{ext}")  # Construction du chemin de sortie
			self._stack = open_tif(filename)
		except Exception as e:
			self._stack = None
			print_error(f"Unable to read the TIFF file : {e}.")
			return

		# --- mise à jour du label associé au bouton ---
		self._lbl_tif_compute.setText(basename)
		self._lbl_tif_compute.setToolTip(filename)
		self._lbl_tif_apply.setText(basename)
		self._lbl_tif_apply.setToolTip(filename)

		print(f"TIFF loaded successfully. Shape={self._stack.shape}, dtype={self._stack.dtype}")

	##################################################
	def _on_load_coef(self):
		"""
		Callback du bouton 'Load coefficients file'.

		Ouvre un fichier texte contenant les coefficients d'alignement sous la forme de deux lignes de dix valeurs (2x10),
		en ignorant la première ligne de commentaire commençant par '#'.

		À l'issue de la lecture, les coefficients sont stockés dans ``self._factors``
		sous la forme d'un tableau NumPy de taille ``(2, 10)`` et de type :class:`numpy.float64`.
		"""
		# --- boîte de dialogue pour sélectionner un fichier .txt ---
		filename, _ = QFileDialog.getOpenFileName(self, "Select coefficients file", "", "Text files (*.txt);;All files (*.*)")

		if not filename:
			print_warning("No coefficient file selected.")
			return

		# --- lecture du fichier ---
		try:
			print(f"Selected file: {filename}.")
			self._coefs = np.loadtxt(filename, comments="#", dtype=np.float64)
		except Exception as e:
			self._coefs = None
			print_error(f"Unable to read the coefficient file: {e}.")
			return

		# --- vérification de la forme des données ---
		if self._coefs.ndim != 2 or self._coefs.shape != (2, 10):
			self._coefs = None
			print_error(f"The coefficient file is not in the correct format. Expected format: two lines of ten values (2x10).")
			return

		# --- mise à jour du label de statut ---
		basename = os.path.basename(filename)
		self._lbl_coef_apply.setText(basename)
		self._lbl_coef_apply.setToolTip(filename)

		print("Coefficients loaded successfully.")

	##################################################
	def _on_compute_coeffs(self):
		"""Callback du bouton 'Compute coefficients'."""
		if self._stack is None: print("Can't Compute alignment coefficients without correct tif file.")
		else: print_warning("Compute alignment coefficients isn't implemented yet. Use original PALMTracer.")

	##################################################
	def _on_start_alignment(self):
		"""Callback du bouton 'Start alignment'."""
		if self._stack is None: print("Can't align without correct tif file.")
		elif self._coefs is None: print("Can't align tif file without factors.")
		else:
			upscale = self._spin_upscale.value()
			aligned = self._palm.align(self._stack, self._coefs, upscale)
			save_tif(aligned, self._output_filename)
			print(f"File saved at {self._output_filename} (upscale={upscale}).")


##################################################
def open_alignment():  # pragma: no cover
	"""
	Ouvre la fenêtre d'alignement en mode autonome.

	Cette fonction est utilisée par le plugin napari comme point d'entrée :
	elle crée simplement un :class:`AlignmentWidget`, l'affiche et le renvoie. Le widget ne dépend pas de napari et s'ouvre dans sa propre fenêtre.
	"""
	widget = AlignmentWidget()
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
	w = AlignmentWidget()
	w.resize(500, 250)
	w.show()
	sys.exit(app.exec_())
