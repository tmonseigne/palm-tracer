"""
Module contenant la classe :class:`AlignmentWidget`, un outil minimaliste pour la gestion de l'alignement géométrique entre acquisitions dans PALMTracer.

Ce widget offre une interface simple organisée en deux onglets : ``Compute Alignment Coefficients``, ``Apply Alignment``

Fonctionnalités principales
---------------------------
- Interface légère en PySide6/PyQt6 basée sur des :class:`QTabWidget`, :class:`QGroupBox` et :class:`QPushButton`.
- Gestion simple des entrées (sélection de fichiers TIFF / TXT via :class:`QFileDialog`).
- Chargement des images via :func:`palm_tracer.Tools.open_tif` et sauvegarde via :func:`palm_tracer.Tools.save_tif`.
- Chargement des coefficients d'alignement sous forme d'un tableau NumPy de taille ``(2, 10)``.
- Application de l'alignement via :meth:`Palm.align`, issue du module :mod:`palm_tracer.Processing`.

Notes
-----
- Le widget est autonome : il peut être lancé directement (``python AlignmentWidget.py``), utilisé dans PALMTracer ou dans un plugin externe.

.. todo:: Implémenter la méthode de calcul automatique des coefficients (méthode interne PALMTracer actuelle).
		  Prévoir une visualisation intermédiaire (overlay, difference map).
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import numpy as np
from qtpy.QtWidgets import QApplication, QFileDialog, QPushButton, QSpinBox, QTabWidget, QVBoxLayout, QWidget

from palm_tracer.Processing import Palm
from palm_tracer.Tools import Ui
from palm_tracer.Tools.FileIO import open_tif, save_tif

_windows = []  # pour garder une référence globale, éviter le Garbage Collector


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

	# ==================================================
	# region Initialisation
	# ==================================================
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
		self._output_filename: str = ""

		self._init_ui()
		self._connect_signals()
		self.setStyleSheet(Ui.STYLESHEET_GENERAL)  # On applique un style général

	##################################################
	def _init_ui(self):
		"""Construit l'interface utilisateur (onglets + boutons) en conservant un style proche du Graph Viewer."""
		main_layout = QVBoxLayout(self)
		Ui.init_layout(main_layout)

		self._tabs = QTabWidget(self)

		# ---------- Onglet 1 : Compute Alignment Coefficients ----------
		tab_compute, tab_layout = Ui.make_tab(self._tabs)
		grp, grp_layout = Ui.make_group(tab_compute, "Inputs")

		self._btn_load_tif_compute = QPushButton("Load image file (TIFF)", grp)
		self._btn_load_tif_compute.setToolTip(
				"The file must contain a single image (a single frame) composed of two regions placed side by side:\n"
				"- on the left: the reference image.\n"
				"- on the right: the distorted image."
				)

		self._lbl_tif_compute = Ui.make_path_label("No file loaded", grp)

		grp_layout.addWidget(self._btn_load_tif_compute)
		grp_layout.addWidget(self._lbl_tif_compute)

		self._btn_compute_coeffs = QPushButton("Compute coefficients (not implemented)", tab_compute)
		self._btn_compute_coeffs.setToolTip("Start calculating alignment coefficients from the loaded image.")

		tab_layout.addWidget(grp)
		tab_layout.addWidget(self._btn_compute_coeffs)
		tab_layout.addStretch(1)

		# ---------- Onglet 2 : Apply Alignment ----------
		tab_apply, tab_layout = Ui.make_tab(self._tabs)
		grp, grp_layout = Ui.make_group(tab_apply, "Inputs")

		self._btn_load_tif_apply = QPushButton("Load image file (TIFF)", grp)
		self._btn_load_tif_apply.setToolTip("Load the TIFF file to which the alignment should be applied.")

		self._btn_load_coef_apply = QPushButton("Load coefficients file", grp)
		self._btn_load_coef_apply.setToolTip("Load the file containing the alignment coefficients.")

		self._lbl_tif_apply = Ui.make_path_label("No TIFF file loaded", grp)
		self._lbl_coef_apply = Ui.make_path_label("No coefficients file loaded", grp)

		self._spin_upscale = QSpinBox(grp, minimum=1, maximum=1000, singleStep=1, value=1)
		self._spin_upscale.setToolTip("Integer upscaling factor for the output aligned image (1 = no upscaling).")

		form = Ui.make_form(None)
		Ui.add_setting_row(form, "Upscaling factor:", self._spin_upscale)

		grp_layout.addWidget(self._btn_load_tif_apply)
		grp_layout.addWidget(self._lbl_tif_apply)
		grp_layout.addWidget(self._btn_load_coef_apply)
		grp_layout.addWidget(self._lbl_coef_apply)
		grp_layout.addLayout(form)

		self._btn_start_alignment = QPushButton("Start alignment", tab_apply)
		self._btn_start_alignment.setToolTip("Applies alignment to the image using the loaded coefficients.")

		tab_layout.addWidget(grp)
		tab_layout.addWidget(self._btn_start_alignment)
		tab_layout.addStretch(1)

		# ---------- Ajout des onglets ----------
		self._tabs.addTab(tab_compute, "Compute Alignment Coefficients")
		self._tabs.addTab(tab_apply, "Apply Alignment")

		main_layout.addWidget(self._tabs)

	##################################################
	def _connect_signals(self):
		"""Connecte les signaux aux callbacks."""
		self._btn_load_tif_compute.clicked.connect(self._on_load_tif)
		self._btn_compute_coeffs.clicked.connect(self._on_compute_coeffs)

		self._btn_load_tif_apply.clicked.connect(self._on_load_tif)
		self._btn_load_coef_apply.clicked.connect(self._on_load_coef)
		self._btn_start_alignment.clicked.connect(self._on_start_alignment)

	# ==================================================
	# endregion Initialisation
	# ==================================================

	# ==================================================
	# region Callbacks
	# ==================================================
	def _on_load_tif(self):
		"""Callback du bouton 'Load TIFF file'."""
		# --- boîte de dialogue pour sélectionner un .tif ---
		filename, _ = QFileDialog.getOpenFileName(self, "Select TIFF file", "", "TIFF images (*.tif *.tiff)")

		if not filename:
			Ui.print_warning("No TIFF file selected.")
			return

		# --- lecture du fichier ---
		try:
			print(f"Selected file: {filename}.")
			filename = Path(filename)
			self._output_filename = str(filename.with_name(f"{filename.stem}_aligned{filename.suffix}"))  # Construction du chemin de sortie
			self._stack = open_tif(str(filename))
		except Exception as e:
			self._stack = None
			Ui.print_error(f"Unable to read the TIFF file : {e}.")
			return

		# --- mise à jour du label associé au bouton ---
		Ui.update_path_label(self._lbl_tif_compute, filename)
		Ui.update_path_label(self._lbl_tif_apply, filename)

		Ui.print_success(f"TIFF loaded successfully. Shape={self._stack.shape}, dtype={self._stack.dtype}")

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
			Ui.print_warning("No coefficient file selected.")
			return

		# --- lecture du fichier ---
		try:
			print(f"Selected file: {filename}.")
			self._coefs = np.loadtxt(filename, comments="#", dtype=np.float64)
		except Exception as e:
			self._coefs = None
			Ui.print_error(f"Unable to read the coefficient file: {e}.")
			return

		# --- vérification de la forme des données ---
		if self._coefs.ndim != 2 or self._coefs.shape != (2, 10):
			self._coefs = None
			Ui.print_error(f"The coefficient file is not in the correct format. Expected format: two lines of ten values (2x10).")
			return

		# --- mise à jour du label de statut ---
		Ui.update_path_label(self._lbl_coef_apply, Path(filename))

		Ui.print_success("Coefficients loaded successfully.")

	##################################################
	def _on_compute_coeffs(self):
		"""Callback du bouton 'Compute coefficients'."""
		if self._stack is None: Ui.print_warning("Can't Compute alignment coefficients without correct tif file.")
		else: Ui.print_warning("Compute alignment coefficients isn't implemented yet. Use original PALMTracer.")

	##################################################
	def _on_start_alignment(self):
		"""Callback du bouton 'Start alignment'."""
		if self._stack is None: Ui.print_warning("Can't align without correct tif file.")
		elif self._coefs is None: Ui.print_warning("Can't align tif file without factors.")
		else:
			upscale = self._spin_upscale.value()
			aligned = self._palm.align(self._stack, self._coefs, upscale)
			save_tif(aligned, self._output_filename)
			Ui.print_success(f"File saved at {self._output_filename} (upscale={upscale}).")


##################################################
def open_alignment():  # pragma: no cover — Aucun lancement de fenêtre sans controle en CI
	"""
	Ouvre la fenêtre d'alignement en mode autonome.

	Cette fonction est utilisée par le plugin Napari comme point d'entrée :
	elle crée simplement un :class:`AlignmentWidget`, l'affiche et le renvoie. Le widget ne dépend pas de Napari et s'ouvre dans sa propre fenêtre.
	"""
	widget = AlignmentWidget()
	widget.resize(500, 250)
	widget.show()
	_windows.append(widget)  # éviter que Python le détruise en le stockant


##################################################
if __name__ == "__main__":
	import sys

	app = QApplication(sys.argv)
	w = AlignmentWidget()
	w.resize(500, 250)
	w.show()
	sys.exit(app.exec_())
