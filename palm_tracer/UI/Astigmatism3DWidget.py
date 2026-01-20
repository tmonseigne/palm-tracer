"""
Module contenant la classe :class:`Astigmatism3DWidget`, un outil minimaliste pour le calcul d'un modèle d’astigmatisme en lien avec la position axiale.

Ce widget offre une interface simple organisée en deux onglets : ``Compute Astigmatism Model``, ``Estimate Z``

Notes
-----
- Le widget est autonome : il peut être lancé directement (``python Astigmatism3DWidget.py``), utilisé dans PALMTracer ou dans un plugin externe.

.. todo::
   - Vérifier si les fichiers de calib vont sur un Z croissant ou décroissant
"""

import shutil
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
from qtpy.QtCore import Qt
from qtpy.QtWidgets import (QApplication, QCheckBox, QDoubleSpinBox, QFileDialog, QGridLayout, QHBoxLayout, QLabel, QPushButton, QSpinBox, QTabWidget,
							QWidget)

from palm_tracer.Processing import Grapher, Palm
from palm_tracer.Processing.Astigmatism3D import DLL_REQUIRED_COLS, MODEL_COLS, model_projection_validity, MODEL_ROWS, model_validity, z_from_planes
from palm_tracer.Tools import print_error, print_success, print_warning
from palm_tracer.UI.StandAloneWidget import StandAloneWidget

_windows = []  # pour garder une référence globale, éviter le Garbage Collector


class Astigmatism3DWidget(StandAloneWidget):
	"""
	Widget minimaliste pour le calcul d'un modèle d’astigmatisme en lien avec la position axiale et l'estimation d'une position axiale en fonction d'un modèle.

	Ce widget fournit deux onglets :
		- ``Compute Astigmatism Model`` :
			- Bouton pour charger un fichier de localisation contenant au moins les colonnes Sigma X, Sigma Y, Z.
			- Spin float pour la taille des pixel en micromètres (μm/px) avec 3 décimales.
			- Spin float pour la hauteur max sur Z (utilisé si le Z doit être calculé à partir des plans).
			- Bouton pour lancer le calcul du modèle.

		- ``Estimate Z`` :
			- Bouton pour charger un fichier de localisation contenant au moins les colonnes Sigma X,Sigma Y.
			- Spin float pour la taille des pixel en micromètres (μm) avec 3 décimales.
			- Spin float pour la hauteur max sur Z.
			- Checkbox pour sauvegarder l'original dans un dossier backup.
			- Bouton pour lancer l'estimation.

	 La partie de droite sert à visualiser le modèle calculé ou chargé.
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
		self.setWindowTitle("Astigmatism 3D Tool")

		self._palm = Palm()
		self._loc_filename: Path = Path()
		self._mod_filename: Path = Path()
		self._png_filename: Path = Path()
		self._loc: pd.DataFrame = pd.DataFrame()
		self._model: pd.DataFrame = pd.DataFrame()

		self._grapher = Grapher()

		self._init_ui()
		self._connect_signals()
		self._update_plot()

	##################################################
	def _init_ui(self):
		"""Construit l'interface utilisateur (onglets + boutons) en conservant un style proche du Graph Viewer."""

		main_layout = QHBoxLayout(self)
		self._init_layout(main_layout)

		self._tabs = QTabWidget(self)

		# ---------- Onglet 1 : Compute Model ----------
		tab_compute, tab_layout = self._make_tab(self._tabs)
		grp, grp_layout = self._make_group(tab_compute, "Inputs")

		self._btn_load_compute = QPushButton("Load Localization file (CSV)", grp)
		self._btn_load_compute.setToolTip("The file must contain at least 3 columns : Sigma X, Sigma Y, Z")

		self._lbl_compute = QLabel("No file loaded", grp)
		self._lbl_compute.setStyleSheet(self.STYLESHEET_INFO)

		self._spin_px_compute = QDoubleSpinBox(grp, decimals=3, minimum=0.001, maximum=1, singleStep=0.010, value=0.160)
		self._spin_px_compute.setToolTip("Pixel size in micrometers.")

		self._check_z_from_plane = QCheckBox(grp)
		self._check_z_from_plane.setToolTip("Use the plane column to define the Z column.")

		self._spin_z_compute = QSpinBox(grp, minimum=1, maximum=1000, singleStep=10, value=500)
		self._spin_z_compute.setToolTip("Maximum absolute value of Z.")

		form = self._make_form(None)
		self._add_setting_row(form, "Pixel Size (µm/px):", self._spin_px_compute)
		self._add_setting_row(form, "Z Max (nm):", self._spin_z_compute)
		self._add_setting_row(form, "Get Z from plane:", self._check_z_from_plane)

		grp_layout.addWidget(self._btn_load_compute)
		grp_layout.addWidget(self._lbl_compute)
		grp_layout.addLayout(form)

		self._btn_compute = QPushButton("Compute model", tab_compute)
		self._btn_compute.setToolTip("Start calculating model coefficients from the localization file.")

		tab_layout.addWidget(grp)
		tab_layout.addWidget(self._btn_compute)

		# --- Groupe Vérification de cohérence ---
		self._sanity: list[dict[str, dict[str, QLabel | str]]] = [{
				# Columns 1 title "Sigma Sanity Check"
				"rmse_x":  {"label": QLabel("RMSE x:"), "value": QLabel("     --"), "unit": QLabel("px"),
							"tips":  "Root Mean Square Error on x (0 for a perfect model)."},
				"rmse_y":  {"label": QLabel("RMSE y:"), "value": QLabel("     --"), "unit": QLabel("px"),
							"tips":  "Root Mean Square Error on y (0 for a perfect model)."},
				"rmse_xy": {"label": QLabel("RMSE xy:"), "value": QLabel("     --"), "unit": QLabel("px"),
							"tips":  "Root Mean Square Error on x and y (0 for a perfect model)."},
				"mae_x":   {"label": QLabel("MAE x:"), "value": QLabel("     --"), "unit": QLabel("px"),
							"tips":  "Mean Absolute Error on x (0 for a perfect model)."},
				"mae_y":   {"label": QLabel("MAE y"), "value": QLabel("     --"), "unit": QLabel("px"),
							"tips":  "Mean Absolute Error on y (0 for a perfect model)."},
				"r2_x":    {"label": QLabel("R² x:"), "value": QLabel("     --"), "unit": QLabel("%"),
							"tips":  "Percent of variance explained on x (100 % for a perfect model)."},
				"r2_y":    {"label": QLabel("R² y:"), "value": QLabel("     --"), "unit": QLabel("%"),
							"tips":  "Percent of variance explained on y (100 % for a perfect model)."}}, {

				# Columns 2 title "Z Sanity Check"
				"rmse_z":    {"label": QLabel("RMSE z:"), "value": QLabel("     --"), "unit": QLabel("nm"),
							  "tips":  "Root Mean Square Error on z (0 for a perfect model)."},
				"mae_z":     {"label": QLabel("MAE z:"), "value": QLabel("     --"), "unit": QLabel("nm"),
							  "tips":  "Mean Absolute Error on z (0 for a perfect model)."},
				"p95_abs_z": {"label": QLabel("P95 z:"), "value": QLabel("     --"), "unit": QLabel("nm"),
							  "tips":  "95e percentile of error distance on z."},
				"bias_z":    {"label": QLabel("Bias z:"), "value": QLabel("     --"), "unit": QLabel("nm"),
							  "tips":  "Mean of error distance on z."},
				"std_z":     {"label": QLabel("STD z"), "value": QLabel("     --"), "unit": QLabel("nm"),
							  "tips":  "Standard deviation of error distance on z."},
				"mean_dist": {"label": QLabel("Curve Mean dist:"), "value": QLabel("     --"), "unit": QLabel("px"),
							  "tips":  "Mean of error distance with the curve."},
				"p95_dist":  {"label": QLabel("Curve P95 dist:"), "value": QLabel("     --"), "unit": QLabel("px"),
							  "tips":  "95e percentile of error distance with the curve."}}]

		grp, grp_layout = self._make_group(tab_compute, "Sanity Check")
		grp_layout.addLayout(self._init_sanity_check_layout(self._sanity, titles=["Sigma Sanity Check", "Z Sanity Check"]))

		tab_layout.addWidget(grp)
		tab_layout.addStretch(1)

		# ---------- Onglet 2 : Estimate Z ----------
		tab_estimate, tab_layout = self._make_tab(self._tabs)
		grp, grp_layout = self._make_group(tab_estimate, "Inputs")

		self._btn_load_loc_estimate = QPushButton("Load Localization file (CSV)", grp)
		self._btn_load_loc_estimate.setToolTip("The file must contain at least 3 columns : Sigma X, Sigma Y, Z")

		self._lbl_loc_estimate = QLabel("No file loaded", grp)
		self._lbl_loc_estimate.setStyleSheet(self.STYLESHEET_INFO)

		self._btn_load_model_estimate = QPushButton("Load Model file (CSV)", grp)
		self._btn_load_model_estimate.setToolTip("The file is a csv with 2 lines and 5 columns.")

		self._lbl_model_estimate = QLabel("No Model file loaded", grp)
		self._lbl_model_estimate.setStyleSheet(self.STYLESHEET_INFO)

		self._spin_px_estimate = QDoubleSpinBox(grp, decimals=3, minimum=0.001, maximum=1, singleStep=0.010, value=0.160)
		self._spin_px_estimate.setToolTip("Pixel size in micrometers.")

		self._spin_z_estimate = QSpinBox(grp, minimum=1, maximum=1000, singleStep=10, value=500)
		self._spin_z_estimate.setToolTip("Maximum absolute value of Z.")

		self._check_b_estimate = QCheckBox(grp)
		self._check_b_estimate.setChecked(True)
		self._check_b_estimate.setToolTip("Save original localisation file in backup folder.")

		form = self._make_form(None)
		self._add_setting_row(form, "Pixel Size (µm/px):", self._spin_px_estimate)
		self._add_setting_row(form, "Z Max (nm):", self._spin_z_estimate)
		self._add_setting_row(form, "Save Backup:", self._check_b_estimate)

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

		self._web = self._make_web_widget()

		main_layout.addWidget(self._tabs)
		main_layout.addWidget(self._web, stretch=1)

	##################################################
	def _init_sanity_check_layout(self, sanity: list[dict[str, dict[str, QLabel | str]]], titles: list[str]) -> QHBoxLayout:
		"""
		Construit le layout du groupe "Sanity Check" avec 2 colonnes d'indicateurs.

		Chaque colonne affiche :
		- un titre de colonne
		- une liste de lignes, chaque ligne contenant : label | value | unit
		  avec l'alignement : gauche | droite | gauche.

		:param sanity: Structure de données : liste de 2 dictionnaires (une colonne par dict).
					   Chaque entrée attend : "label": QLabel, "value": QLabel, "unit": QLabel, "tips": str
		:param titles: Titres des 2 colonnes.
		:return: Un QHBoxLayout prêt à être ajouté au calque du groupe.
		"""
		res = QHBoxLayout()
		res.setContentsMargins(0, 0, 0, 0)
		res.setSpacing(self.COMMON_SPACE)

		res.addLayout(self._make_column_grid(sanity[0], titles[0]), stretch=1)
		res.addWidget(self._make_vertical_separator())
		res.addLayout(self._make_column_grid(sanity[1], titles[1]), stretch=1)
		return res

	##################################################
	def _make_column_grid(self, elements: dict[str, dict[str, QLabel | str]], title: str) -> QGridLayout:
		"""Construit une colonne (titre + lignes) sous forme de QGridLayout."""
		grid = QGridLayout()
		grid.setContentsMargins(0, 0, 0, 0)
		grid.setHorizontalSpacing(self.COMMON_SPACE)
		grid.setVerticalSpacing(self.COMMON_SPACE)

		# Titre de colonne
		title_lbl = QLabel(title)
		title_lbl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
		title_lbl.setStyleSheet("font-weight: 600;")
		grid.addWidget(title_lbl, 0, 0, 1, 3)  # Titre
		grid.addWidget(self._make_horizontal_separator(), 1, 0, 1, 3)  # Séparateur horizontal

		# Colonnes fixes : label | value | unit. On force la colonne "value" à s’étendre, pour garder l’alignement propre.
		grid.setColumnStretch(0, 0)  # label
		grid.setColumnStretch(1, 1)  # value (s'étire)
		grid.setColumnStretch(2, 0)  # unit

		row = 2
		for key, item in elements.items():
			lbl: QLabel = item["label"]
			val: QLabel = item["value"]
			unit: QLabel = item["unit"]
			tips: str = item["tips"]

			lbl.setToolTip(tips)  # Tooltips collé au label

			# Alignements : gauche | droite | gauche
			lbl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
			val.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
			unit.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

			grid.addWidget(lbl, row, 0)
			grid.addWidget(val, row, 1)
			grid.addWidget(unit, row, 2)

			row += 1

		return grid

	##################################################
	def _connect_signals(self):
		"""Connecte les signaux des boutons aux callbacks."""
		self._btn_load_compute.clicked.connect(self._on_load_loc)
		self._btn_compute.clicked.connect(self._on_compute)

		self._btn_load_loc_estimate.clicked.connect(self._on_load_loc)
		self._btn_load_model_estimate.clicked.connect(self._on_load_model)
		self._btn_estimate.clicked.connect(self._on_estimate)

		# --- Lien entre les deux spin ---
		self._spin_px_compute.valueChanged.connect(lambda v: self._sync_spin(self._spin_px_estimate, v))
		self._spin_px_estimate.valueChanged.connect(lambda v: self._sync_spin(self._spin_px_compute, v))
		self._spin_z_compute.valueChanged.connect(lambda v: self._sync_spin(self._spin_z_estimate, v))
		self._spin_z_estimate.valueChanged.connect(lambda v: self._sync_spin(self._spin_z_compute, v))

		# --- Mise à jour de l'affichage de la courbe ---
		self._spin_px_compute.valueChanged.connect(self._update_plot)
		self._spin_px_estimate.valueChanged.connect(self._update_plot)
		self._spin_z_estimate.valueChanged.connect(self._update_plot)

		self._connect_web_widget(self._web)

	# ==================================================
	# endregion Initialisation
	# ==================================================

	# ==================================================
	# region UI
	# ==================================================
	##################################################
	def _update_sanity_values(self, points: np.ndarray, model: np.ndarray, pixel_size: float):
		"""
		Mise à jour de l'onglet Sanity Check
		:param points: points du jeu de donnée.
		:param model: Modèle astigmatique de forme (2, 5) : paramètres X puis Y, chaque ligne = [Z0, W, C3, C4, A].
		:param pixel_size: Taille du pixel dans les mêmes unités que Z (ex. nm).
		"""
		metrics = model_validity(points, model, pixel_size, 1)
		for key in metrics:
			val: QLabel = self._sanity[0][key]["value"]
			if "r2" in key: val.setText(f"{100 * metrics[key]:0.2f}")
			else: val.setText(f"{metrics[key]:0.4f}")

		z_max = np.max(np.abs(points[:, 2]))
		metrics = model_projection_validity(points, model, z_max, 5000, pixel_size, 1)
		for key in metrics:
			val = self._sanity[1][key]["value"]
			val.setText(f"{metrics[key]:0.4f}")

	##################################################
	def _update_plot(self):
		"""Construit la figure Plotly courante en fonction du domaine et de la source."""
		pixel_size = self._spin_px_compute.value() * 1000  # Passage en nanomètres
		z_max = self._spin_z_estimate.value()
		fig = self._grapher.astigmatism3d_curve("Astigmatism model", self._model.to_numpy(), pixel_size, z_max)
		self._update_web_widget(self._web, fig)

	# ==================================================
	# endregion UI
	# ==================================================

	# ==================================================
	# region Callbacks
	# ==================================================
	##################################################
	def _download_initial_path(self) -> Path:
		""" Renvoie un chemin initial pour le téléchargement par plotly."""
		parent: Path = self._mod_filename.parent if self._mod_filename != Path() else self._loc_filename.parent if self._loc_filename != Path() else Path.cwd()
		return parent / "astigmatism_3d_model"

	##################################################
	def _on_load_loc(self):
		"""Callback du bouton 'Load Localization file (CSV)'."""
		# --- boîte de dialogue pour sélectionner un .csv ---
		filename, _ = QFileDialog.getOpenFileName(self, "Select Localization CSV file", "", "CSV files (*.csv)")

		if not filename:
			print_warning("No file selected.")
			return

		# --- lecture du fichier ---
		try:
			print(f"Selected file: {filename}.")
			self._loc_filename = Path(filename)
			self._loc = pd.read_csv(filename)
		except Exception as e:
			self._loc = pd.DataFrame()
			print_error(f"Unable to read the CSV file : {e}.")
			return

		# --- vérification de la forme des données ---
		if not set(DLL_REQUIRED_COLS).issubset(self._loc.columns):
			print_error(f"The localization file is not in the correct format.\n"
						f"\tExpected format, at least columns: {', '.join(sorted(DLL_REQUIRED_COLS))}.\n"
						f"\tFound columns: {', '.join(self._loc.columns)}")
			self._loc = pd.DataFrame()
			return

		# --- mise à jour du label associé au bouton ---
		self._lbl_compute.setText(self._loc_filename.name)
		self._lbl_compute.setToolTip(filename)
		self._lbl_loc_estimate.setText(self._loc_filename.name)
		self._lbl_loc_estimate.setToolTip(filename)

		# --- mise à jour du Z Max ---
		self._spin_z_estimate.setValue(self._loc["Z"].abs().max())

		print_success(f"CSV loaded successfully. {len(self._loc)} points, {len(self._loc.columns)} columns")

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
			self._mod_filename = Path(filename)
			self._model = pd.read_csv(filename, index_col=0)
		except Exception as e:
			self._model = pd.DataFrame()
			print_error(f"Unable to read the model file: {e}.")
			return

		# --- vérification de la forme des données ---
		if len(self._model) != len(MODEL_ROWS) or len(self._model.columns) != len(MODEL_COLS):
			self._model = pd.DataFrame()
			print_error(f"The model file is not in the correct format. Expected format: two lines of five values (2x5).")
			return

		# --- mise à jour du label de statut ---
		self._lbl_model_estimate.setText(self._mod_filename.name)
		self._lbl_model_estimate.setToolTip(filename)

		# --- mise à jour de l'affichage ---
		self._update_plot()

		print_success("Model loaded successfully.")

	##################################################
	def _on_compute(self):
		"""Callback du bouton 'Compute model'."""
		# --- Vérification ---
		if self._loc.empty:
			print_warning("Can't Compute model without correct file loaded.")
			return

		pixel_size = self._spin_px_compute.value() * 1000  # Passage en nanomètres
		points = self._loc.loc[:, DLL_REQUIRED_COLS].to_numpy(dtype=float, copy=True)

		# --- Mise à jour de Z (si sélectionné) ---
		if self._check_z_from_plane.isChecked():
			if "Plane" not in self._loc.columns:
				print_warning("No Plane Column in file. We can't use it to intialize Z.")
				return
			z_max = self._spin_z_compute.value()
			z = z_from_planes(self._loc["Plane"].to_numpy(), -z_max, z_max)  # Attention, savoir si on va de -Zmax à + Zmax ou de +Zmax à -Zmax
			points[:, 2] = z

		# --- Calcul ---
		model = self._palm.astigmatism_3d_calibration(points, pixel_size)
		self._model = pd.DataFrame(model, columns=MODEL_COLS, index=MODEL_ROWS)

		# --- Fichier de sortie ---
		self._mod_filename = self._loc_filename.with_name("astigmatism_3d_model.csv")
		self._model.to_csv(str(self._mod_filename))
		print_success("Model saved successfully.")

		# --- Mise à jour des affichages (sanity check, plot et model dans estimate) ---
		self._update_sanity_values(points, model, pixel_size)
		self._update_plot()
		self._lbl_model_estimate.setText(self._mod_filename.name)
		self._lbl_model_estimate.setToolTip(str(self._mod_filename))

	##################################################
	def _on_estimate(self):
		"""Callback du bouton 'Estimate'."""
		# --- Vérifications ---
		if self._loc.empty:
			print_warning("Can't estimate without correct localization file loaded.")
			return
		if self._model.empty:
			print_warning("Can't estimate without correct model file loaded.")
			return

		# --- Enregistre un backup (si sélectionné) ---
		if self._check_b_estimate.isChecked():
			backup_dir: Path = self._loc_filename.parent / "backup"
			backup_dir.mkdir(parents=True, exist_ok=True)

			name: str = self._loc_filename.stem  # "fichier"
			ext: str = self._loc_filename.suffix  # ".csv"

			backup_filename: Path = backup_dir / self._loc_filename.name
			i = 1

			# Si le fichier existe déjà, on ajoute _1, _2, ...
			while backup_filename.exists():
				backup_filename = backup_dir / f"{name}_{i}{ext}"
				i += 1

			shutil.copy2(self._loc_filename, backup_filename)
			print(f"Backup done at {backup_filename}")

		# --- Estimation ---
		pixel_size = self._spin_px_estimate.value() * 1000  # Passage en nanomètres
		z_max = self._spin_z_estimate.value()
		points = self._loc.loc[:, DLL_REQUIRED_COLS[:-1]].to_numpy(dtype=float, copy=True)
		estimated_z = self._palm.astigmatism_3d_estimation(points, pixel_size, self._model.to_numpy(), z_max)
		self._loc[DLL_REQUIRED_COLS[-1]] = estimated_z
		self._loc.to_csv(self._loc_filename, index=False)
		print_success("Localization file with estimation saved successfully.")

	# ==================================================
	# endregion Callbacks
	# ==================================================


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
	_windows.append(widget)  # éviter que Python le détruise en le stockant

##################################################
if __name__ == "__main__":  # pragma: no cover
	import sys

	app = QApplication(sys.argv)
	w = Astigmatism3DWidget()
	w.resize(1000, 600)
	w.show()
	sys.exit(app.exec_())
