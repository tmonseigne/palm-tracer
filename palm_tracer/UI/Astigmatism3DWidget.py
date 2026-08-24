"""Fournit le widget de calibration et d'estimation axiale par astigmatisme 3D."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
from qtpy.QtWidgets import QApplication, QCheckBox, QDoubleSpinBox, QFileDialog, QGroupBox, QHBoxLayout, QLabel, QPushButton, QSpinBox, QTabWidget, QWidget

from palm_tracer.Processing import Palm
from palm_tracer.Processing.Astigmatism3D import find_model_center, model_projection_validity, model_validity, remove_multi_beads
from palm_tracer.Processing.Parsing import FILES_COLUMNS, MODEL_ROWS, SHAPE_MODEL
from palm_tracer.Tools import Ui
from palm_tracer.UI.BasePlotlyWidget import BasePlotlyWidget

DLL_REQUIRED_COLS = ["Sigma X", "Sigma Y", "Z"]

_windows = []  # pour garder une référence globale, éviter le Garbage Collector


class Astigmatism3DWidget(BasePlotlyWidget):
	"""
	Widget minimaliste pour le calcul d'un modèle d'astigmatisme en lien avec la position axiale et l'estimation d'une position axiale en fonction d'un modèle.

	Ce widget fournit deux onglets :
		- ``Compute Astigmatism Model`` :
			- Bouton pour charger un fichier de localisation contenant au moins les colonnes Sigma X, Sigma Y, Z.
			- Spin float pour la taille des pixels en micromètres (μm/px) avec 3 décimales.
			- Spin float pour la hauteur max sur Z (utilisé si le Z doit être calculé à partir des plans).
			- Bouton pour lancer le calcul du modèle.

		- ``Estimate Z`` :
			- Bouton pour charger un fichier de localisation contenant au moins les colonnes Sigma X,Sigma Y.
			- Spin float pour la taille des pixels en micromètres (μm) avec 3 décimales.
			- Spin float pour la hauteur max sur Z.
			- Checkbox pour sauvegarder l'original dans un dossier backup.
			- Bouton pour lancer l'estimation.

	 La partie de droite sert à visualiser le modèle calculé ou chargé.
	"""

	GRAPH_TITLE: str = "Astigmatism model"
	GRAPH_TYPE: list["str"] = ["Curve", "Cross", "Slope"]

	# ==================================================
	# region Initialization
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
		self._fig = self._grapher.blank(self.GRAPH_TITLE)

		self._init_ui()
		self._connect_signals()
		self._update_plot()

	##################################################
	def _init_ui(self):
		"""Construit l'interface utilisateur (onglets + boutons) en conservant un style proche du Graph Viewer."""

		main_layout = QHBoxLayout(self)
		Ui.init_layout(main_layout)

		self._tabs = QTabWidget(self)

		# ---------- Onglet 1 : Compute Model ----------
		tab_compute, tab_layout = Ui.make_tab(self._tabs)
		grp, grp_layout = Ui.make_group(tab_compute, "Inputs")

		self._btn_load_compute = QPushButton("Load Localization file (CSV)", grp)
		self._btn_load_compute.setToolTip("The file must contain at least 3 columns : Sigma X, Sigma Y, Z")

		self._lbl_compute = Ui.make_path_label("No file loaded", grp)

		self._spin_px_compute = QDoubleSpinBox(grp, decimals=3, minimum=0.001, maximum=1, singleStep=0.010, value=0.160)
		self._spin_px_compute.setToolTip("Pixel size in micrometers.")
		self._spin_z_compute = QSpinBox(grp, minimum=10, maximum=2000, singleStep=10, value=500)
		self._spin_z_compute.setToolTip("Maximum absolute value of Z.")
		self._check_z_from_plane = QCheckBox(grp)
		self._check_z_from_plane.setToolTip("Use the plane column to define the Z column.")
		self._spin_z_interval = QSpinBox(grp, minimum=1, maximum=1000, singleStep=10, value=20)
		self._spin_z_interval.setToolTip("Interval in nanometers between two planes.")
		self._check_z_center = QCheckBox(grp)
		self._check_z_center.setChecked(True)
		self._check_z_center.setToolTip("Center the image so that σx(0) ≈ σy(0).\nUncheck this box only if you understand and want this specific behavior.")
		self._check_z_flip = QCheckBox(grp)
		self._check_z_flip.setToolTip("Flip Sign of Z.")
		self._check_only_one = QCheckBox(grp)
		self._check_only_one.setToolTip("If more than one localization appears on a plane, the one closest to the other localization is retained.")

		form = Ui.make_form(None)
		Ui.add_setting_row(form, "Only one bead:", self._check_only_one)
		Ui.add_setting_row(form, "Pixel Size (µm/px):", self._spin_px_compute)
		Ui.add_setting_row(form, "Z Max (nm):", self._spin_z_compute)
		Ui.add_setting_row(form, "Get Z from plane:", self._check_z_from_plane)
		Ui.add_setting_row(form, "Plane Interval (nm):", self._spin_z_interval)
		Ui.add_setting_row(form, "Center Z:", self._check_z_center)
		Ui.add_setting_row(form, "Flip Z:", self._check_z_flip)

		grp_layout.addWidget(self._btn_load_compute)
		grp_layout.addWidget(self._lbl_compute)
		grp_layout.addLayout(form)

		# Bloc Type de graphe
		grp_type = QGroupBox("Graph Type")
		h, self._btg_type_compute, self._btn_type_compute = Ui.make_exclusive_btn_group(self.GRAPH_TYPE, 0)
		form = Ui.make_form(grp_type)
		form.addRow(h)

		# Bouton compute
		self._btn_compute = QPushButton("Compute model", tab_compute)
		self._btn_compute.setToolTip("Start calculating model coefficients from the localization file.")

		tab_layout.addWidget(grp)
		tab_layout.addWidget(grp_type)
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
							"tips":  "Percent of variance explained on y (100 % for a perfect model)."},
				"blank":   {"label": QLabel(""), "value": QLabel(""), "unit": QLabel(""), "tips": ""}}, {

				# Columns 2 title "Z Sanity Check"
				"rmse_z":     {"label": QLabel("RMSE z:"), "value": QLabel("     --"), "unit": QLabel("nm"),
							   "tips":  "Root Mean Square Error on z (0 for a perfect model)."},
				"mae_z":      {"label": QLabel("MAE z:"), "value": QLabel("     --"), "unit": QLabel("nm"),
							   "tips":  "Mean Absolute Error on z (0 for a perfect model)."},
				"p95_abs_z":  {"label": QLabel("P95 z:"), "value": QLabel("     --"), "unit": QLabel("nm"),
							   "tips":  "95e percentile of error distance on z."},
				"bias_z":     {"label": QLabel("Bias z:"), "value": QLabel("     --"), "unit": QLabel("nm"),
							   "tips":  "Mean of error distance on z."},
				"std_z":      {"label": QLabel("STD z"), "value": QLabel("     --"), "unit": QLabel("nm"),
							   "tips":  "Standard deviation of error distance on z."},
				"mean_dist":  {"label": QLabel("Curve Mean dist:"), "value": QLabel("     --"), "unit": QLabel("px"),
							   "tips":  "Mean of error distance with the curve."},
				"p95_dist":   {"label": QLabel("Curve P95 dist:"), "value": QLabel("     --"), "unit": QLabel("px"),
							   "tips":  "95e percentile of error distance with the curve."},
				"slope_mean": {"label": QLabel("Slope:"), "value": QLabel("     --"), "unit": QLabel("px/nm"),
							   "tips":  "Slope of curve σx(z) - σy(z)."}}]

		grp, grp_layout = Ui.make_group(tab_compute, "Sanity Check")
		grp_layout.addLayout(self._init_sanity_check_layout(self._sanity, titles=["Sigma Sanity Check", "Z Sanity Check"]))

		tab_layout.addWidget(grp)
		tab_layout.addStretch(1)

		# ---------- Onglet 2 : Estimate Z ----------
		tab_estimate, tab_layout = Ui.make_tab(self._tabs)
		grp, grp_layout = Ui.make_group(tab_estimate, "Inputs")

		self._btn_load_loc_estimate = QPushButton("Load Localization file (CSV)", grp)
		self._btn_load_loc_estimate.setToolTip("The file must contain at least 3 columns : Sigma X, Sigma Y, Z")

		self._btn_load_model_estimate = QPushButton("Load Model file (CSV)", grp)
		self._btn_load_model_estimate.setToolTip("The file is a csv with 2 lines and 5 columns.")

		self._lbl_loc_estimate = Ui.make_path_label("No file loaded", grp)
		self._lbl_model_estimate = Ui.make_path_label("No Model file loaded", grp)

		self._spin_px_estimate = QDoubleSpinBox(grp, decimals=3, minimum=0.001, maximum=1, singleStep=0.010, value=0.160)
		self._spin_px_estimate.setToolTip("Pixel size in micrometers.")

		self._spin_z_estimate = QSpinBox(grp, minimum=10, maximum=2000, singleStep=10, value=500)
		self._spin_z_estimate.setToolTip("Maximum absolute value of Z.")

		self._check_b_estimate = QCheckBox(grp)
		self._check_b_estimate.setChecked(True)
		self._check_b_estimate.setToolTip("Save original localisation file in backup folder.")

		form = Ui.make_form(None)
		Ui.add_setting_row(form, "Pixel Size (µm/px):", self._spin_px_estimate)
		Ui.add_setting_row(form, "Z Max (nm):", self._spin_z_estimate)
		Ui.add_setting_row(form, "Save Backup:", self._check_b_estimate)

		grp_layout.addWidget(self._btn_load_loc_estimate)
		grp_layout.addWidget(self._lbl_loc_estimate)
		grp_layout.addWidget(self._btn_load_model_estimate)
		grp_layout.addWidget(self._lbl_model_estimate)
		grp_layout.addLayout(form)

		# Bloc Type de graphe
		grp_type = QGroupBox("Graph Type")
		h, self._btg_type_estimate, self._btn_type_estimate = Ui.make_exclusive_btn_group(self.GRAPH_TYPE, 0)
		form = Ui.make_form(grp_type)
		form.addRow(h)

		self._btn_estimate = QPushButton("Estimate Z", tab_estimate)
		self._btn_estimate.setToolTip("Estimate Z for all points in localizaation file with the loaded model.")

		tab_layout.addWidget(grp)
		tab_layout.addWidget(grp_type)
		tab_layout.addWidget(self._btn_estimate)
		tab_layout.addStretch(1)

		# ---------- Ajout des onglets ----------
		self._tabs.addTab(tab_compute, "Compute Model")
		self._tabs.addTab(tab_estimate, "Estimate Z")

		main_layout.addWidget(self._tabs)
		main_layout.addWidget(self._web, stretch=1)

	##################################################
	@staticmethod
	def _init_sanity_check_layout(sanity: list[dict[str, dict[str, QLabel | str]]], titles: list[str]) -> QHBoxLayout:
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
		Ui.init_layout(res, 0, 0)

		res.addLayout(Ui.make_info_grid(sanity[0], titles[0], 3), stretch=1)
		res.addWidget(Ui.make_vertical_separator())
		res.addLayout(Ui.make_info_grid(sanity[1], titles[1], 3), stretch=1)
		return res

	##################################################
	def _connect_signals(self):
		"""Connecte les signaux aux callbacks."""
		self._btn_load_compute.clicked.connect(self._on_load_loc)
		self._btn_load_compute.clicked.connect(self._check_loc)
		self._btn_compute.clicked.connect(self._on_compute)

		self._btn_load_loc_estimate.clicked.connect(self._on_load_loc)
		self._btn_load_model_estimate.clicked.connect(self._on_load_model)
		self._btn_estimate.clicked.connect(self._on_estimate)

		# --- Lien entre les spins et les groueps de boutons ---
		self._spin_px_compute.valueChanged.connect(lambda v: Ui.sync_spin(self._spin_px_estimate, v))
		self._spin_px_estimate.valueChanged.connect(lambda v: Ui.sync_spin(self._spin_px_compute, v))
		self._spin_z_compute.valueChanged.connect(lambda v: Ui.sync_spin(self._spin_z_estimate, v))
		self._spin_z_estimate.valueChanged.connect(lambda v: Ui.sync_spin(self._spin_z_compute, v))
		self._btg_type_compute.idClicked.connect(lambda i: Ui.sync_button_group(self._btg_type_estimate, i))
		self._btg_type_estimate.idClicked.connect(lambda i: Ui.sync_button_group(self._btg_type_compute, i))

		# --- Mise à jour de l'affichage de la courbe ---
		self._spin_px_compute.valueChanged.connect(self._update_plot)
		self._spin_px_estimate.valueChanged.connect(self._update_plot)
		self._spin_z_estimate.valueChanged.connect(self._update_plot)
		self._btg_type_compute.idClicked.connect(self._update_plot)
		self._btg_type_estimate.idClicked.connect(self._update_plot)

	# ==================================================
	# endregion Initialization
	# ==================================================

	# ==================================================
	# region UI
	# ==================================================
	##################################################
	def _update_sanity_values(self, points: np.ndarray, model: np.ndarray, pixel_size: float):
		"""
		Mise à jour de l'onglet Sanity Check.

		:param points: Points du jeu de donnée.
		:param model: Modèle astigmatique de forme (2, 5) : paramètres X puis Y, chaque ligne = [Z0, W, C3, C4, A].
		:param pixel_size: Taille du pixel dans les mêmes unités que Z (ex. nm).
		"""
		metrics = model_validity(points, model, pixel_size, 1)
		for key in metrics:
			val: QLabel = self._sanity[0][key]["value"]
			if "r2" in key: val.setText(f"{100 * metrics[key]:0.2f}")
			else: val.setText(f"{metrics[key]:0.4f}")

		z_max = np.max(np.abs(points[:, 2]))
		metrics = model_projection_validity(points, model, z_max, pixel_size)
		for key in metrics:
			val = self._sanity[1][key]["value"]
			val.setText(f"{metrics[key]:0.4f}")

	##################################################
	def _update_plot(self):
		"""Construit la figure Plotly courante en fonction du domaine et de la source."""
		try:
			pixel_size = self._spin_px_compute.value() * 1000  # Passage en nanomètres
			z_max = self._spin_z_estimate.value()
			data = None if self._loc.empty or self._loc["Z"].nunique() <= 1 else self._loc[DLL_REQUIRED_COLS].to_numpy()
			mode = self._btg_type_compute.checkedId()
			if mode == 1: mode = "cross"
			elif mode == 2: mode = "slope"
			else: mode = "curve"
			self._fig = self._grapher.astigmatism3d(self._model.to_numpy(), data, title=self.GRAPH_TITLE, pixel_size=pixel_size, z_max=z_max, mode=mode)
		except ValueError:
			self._fig = self._grapher.blank(self.GRAPH_TITLE)
		self._update_web_widget()

	# ==================================================
	# endregion UI
	# ==================================================

	# ==================================================
	# region Callbacks
	# ==================================================
	##################################################
	def _check_loc(self):
		"""Vérifie la validité du fichier de localisation et modifie les options sélectionnables en conséquence."""
		if "Plane" not in self._loc.columns:
			Ui.print_warning("No 'Plane' Column in file. 'Get Z from plane' and 'Only one bead' options can't be used.")
			self._check_only_one.setChecked(False)
			self._check_only_one.setEnabled(False)
			self._check_z_from_plane.setChecked(False)
			self._check_z_from_plane.setEnabled(False)
			self._spin_z_interval.setEnabled(False)
		else:
			planes = self._loc["Plane"]
			n_planes = planes.max() - planes.min() + 1  # Nombre de plans
			s_p = f"There are {n_planes} planes"
			self._check_z_from_plane.setEnabled(True)
			self._spin_z_interval.setEnabled(True)
			self._check_only_one.setEnabled(True)
			if "Bead" in self._loc.columns:
				n_beads = self._loc["Bead"].nunique()  # Nombre de billes
				Ui.print_success(f"{s_p} and {n_beads} beads in file.")
			else:
				counts_per_plane = self._loc.groupby("Plane").size()  # .		 Nombre de localisations par plan.
				single_planes = counts_per_plane[counts_per_plane == 1].index  # Plans non ambigus : une seule localisation.
				multi_planes = counts_per_plane[counts_per_plane > 1].index  # . Plans ambigus : plusieurs localisations.
				if len(multi_planes) == 0:
					Ui.print_success(f"{s_p} and only one bead.")
				elif len(single_planes) == 0:
					Ui.print_warning(f"{s_p} and at least two localizations per plane. The 'Only one bead' option can't be used.")
					self._check_only_one.setChecked(False)
					self._check_only_one.setEnabled(False)
				else:
					Ui.print_warning(f"{s_p} and some planes contain multiple localizations. It is recommended to use the 'Only one bead' option.")
					self._check_only_one.setChecked(True)

			# --- mise à jour du Z Max ---
			if "Z" in self._loc.columns:
				z_max = self._loc["Z"].abs().max()
				if z_max > 10: self._spin_z_estimate.setValue(z_max)

	##################################################
	def _on_load_loc(self):
		"""Callback du bouton 'Load Localization file (CSV)'."""
		# --- boîte de dialogue pour sélectionner un .csv ---
		filename, _ = QFileDialog.getOpenFileName(self, "Select Localization CSV file", "", "CSV files (*.csv)")

		if not filename:
			Ui.print_warning("No file selected.")
			return

		# --- lecture du fichier ---
		try:
			print(f"Selected file: {filename}.")
			self._loc_filename = Path(filename)
			self._graph_folder = self._loc_filename.parent / "astigmatism_3d_model"
			self._loc = pd.read_csv(filename)
		except Exception as e:
			self._loc = pd.DataFrame()
			Ui.print_error(f"Unable to read the CSV file : {e}.")
			return

		# --- vérification de la forme des données ---
		if not set(DLL_REQUIRED_COLS).issubset(self._loc.columns):
			Ui.print_error(f"The localization file is not in the correct format.\n"
						   f"\tExpected format, at least columns: {', '.join(sorted(DLL_REQUIRED_COLS))}.\n"
						   f"\tFound columns: {', '.join(self._loc.columns)}")
			self._loc = pd.DataFrame()
			return

		# --- mise à jour du label associé au bouton ---
		Ui.update_path_label(self._lbl_compute, self._loc_filename)
		Ui.update_path_label(self._lbl_loc_estimate, self._loc_filename)

		Ui.print_success(f"CSV loaded successfully with {len(self._loc)} points and {len(self._loc.columns)} columns.")

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
			Ui.print_warning("No model file selected.")
			return

		# --- lecture du fichier ---
		try:
			print(f"Selected file: {filename}.")
			self._mod_filename = Path(filename)
			self._graph_folder = self._mod_filename.parent / "astigmatism_3d_model"
			self._model = pd.read_csv(filename, index_col=0)
		except Exception as e:
			self._model = pd.DataFrame()
			Ui.print_error(f"Unable to read the model file: {e}.")
			return

		# --- vérification de la forme des données ---
		if self._model.shape != SHAPE_MODEL:
			self._model = pd.DataFrame()
			Ui.print_error(f"The model file is not in the correct format. Expected format: two lines of five values (2x5).")
			return

		# --- mise à jour du label de statut ---
		Ui.update_path_label(self._lbl_model_estimate, self._mod_filename)

		# --- mise à jour de l'affichage ---
		self._update_plot()

		Ui.print_success("Model loaded successfully.")

	##################################################
	def _on_compute(self):
		"""Callback du bouton 'Compute model'."""
		# --- Vérification ---
		if self._loc.empty:
			Ui.print_warning("Can't Compute model without correct file loaded.")
			return

		z_max = self._spin_z_compute.value()
		pixel_size = self._spin_px_compute.value() * 1000  # Passage en nanomètres

		work = self._loc.copy()

		# --- Mise à jour de Z (si sélectionné) ---
		if self._check_z_from_plane.isChecked():
			if "Plane" not in work.columns:
				Ui.print_warning("No Plane Column in file. We can't use it to intialize Z.")
				return
			work["Z"] = work["Plane"] * self._spin_z_interval.value()

		if self._check_z_flip.isChecked(): work["Z"] *= -1

		default_w = (work["Z"].max() - work["Z"].min()) / 4

		# --- Suppression des artefacts ou autres billes ---
		if self._check_only_one.isChecked(): work = remove_multi_beads(work)

		# --- Préparation des data ---
		beads: list[np.ndarray] = []
		if "Bead" in work.columns:  # Une ou plusieurs billes identifiées
			for _, df in work.groupby("Bead", sort=True): beads.append(df.loc[:, DLL_REQUIRED_COLS].to_numpy(dtype=float, copy=True))
		else:  beads.append(work.loc[:, DLL_REQUIRED_COLS].to_numpy(dtype=float, copy=True))

		# --- Calcul ---
		models: list[pd.DataFrame] = []
		for i in range(len(beads)):
			models.append(self._palm.astigmatism_3d_calibration(beads[i], pixel_size, self._check_z_center.isChecked()))
			print(f"Model for bead {i + 1}:\n{models[-1]}")
			for axis in range(2):
				if np.allclose(models[-1].iloc[axis, 1:4], (default_w, 0, 0), atol=1e-6):
					Ui.print_warning(f"\tModel Calibration keep initial state on axis {MODEL_ROWS[axis]}.")

		if len(models) == 1: self._model = models[0].copy()
		else:
			# Moyenne des modèles
			mean_model = np.stack([model.to_numpy(dtype=float, copy=True) for model in models], axis=0).mean(axis=0)
			# Recentrage du modèle
			if self._check_z_center.isChecked():
				model_center = find_model_center(mean_model, z_max, pixel_size)
				mean_model[0][0] -= model_center
				mean_model[1][0] -= model_center
			self._model = pd.DataFrame(mean_model, columns=FILES_COLUMNS["Astigmatism 3D Model"]["columns"], index=MODEL_ROWS)
			print(f"Average model:\n{self._model}")

		# --- Mise à jour du Z dans loc ---
		points = self._loc.loc[:, DLL_REQUIRED_COLS[:-1]].to_numpy(dtype=float, copy=True)
		estimated_z = self._palm.astigmatism_3d_estimation(points, pixel_size, self._model.to_numpy(), z_max)
		self._loc[["Z", "MSE Z"]] = estimated_z

		# --- Mise à jour de l'affichage ---
		self._update_plot()

		# --- Fichier de sortie ---
		self._mod_filename = self._loc_filename.with_name("astigmatism_3d_model.csv")
		self._model.to_csv(str(self._mod_filename))
		Ui.print_success(f"Model saved successfully.")

		# --- Mise à jour des affichages (sanity check, plot et model dans estimate) ---
		self._update_sanity_values(self._loc.loc[:, DLL_REQUIRED_COLS].to_numpy(dtype=float, copy=True), self._model.to_numpy(), pixel_size)
		self._update_plot()
		Ui.update_path_label(self._lbl_model_estimate, self._mod_filename)

	##################################################
	def _on_estimate(self):
		"""Callback du bouton 'Estimate'."""
		# --- Vérifications ---
		if self._loc.empty:
			Ui.print_warning("Can't estimate without correct localization file loaded.")
			return
		if self._model.empty:
			Ui.print_warning("Can't estimate without correct model file loaded.")
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
		self._loc[["Z", "MSE Z"]] = estimated_z
		self._loc.to_csv(self._loc_filename, index=False)
		Ui.print_success("Localization file with estimation saved successfully.")


##################################################
def open_astigmatism3d():  # pragma: no cover — Aucun lancement de fenêtre sans controle en CI
	"""
	Ouvre la fenêtre d'alignement en mode autonome.

	Cette fonction est utilisée par le plugin Napari comme point d'entrée :
	elle crée simplement un :class:`Astigmatism3DWidget`, l'affiche et le renvoie. Le widget ne dépend pas de Napari et s'ouvre dans sa propre fenêtre.
	"""
	widget = Astigmatism3DWidget()
	widget.resize(1280, 720)
	widget.show()
	_windows.append(widget)  # éviter que Python le détruise en le stockant


##################################################
if __name__ == "__main__":
	import sys

	app = QApplication(sys.argv)
	w = Astigmatism3DWidget()
	w.resize(1280, 720)
	w.show()
	sys.exit(app.exec_())
