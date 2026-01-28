"""
Module contenant la classe :class:`GraphViewerWidget` pour la visualisation interactive
des graphiques liés aux données PALMTracer (pile TIFF, localisations, tracking).

Ce widget fournit :
- Une interface en deux parties :
  • Colonne gauche : informations fichier + présence localisation/tracking, choix du domaine
	(Stack / Localization / Tracking) via 3 boutons exclusifs, et sélection de la source.
  • Zone droite : rendu d'un graphe Plotly dans un QWebEngineView (zoom, pan, hover, export).
- Un couplage léger avec :class:`PALMTracer` pour accéder aux fichiers en cours et charger
  automatiquement pile/CSV (localisations/tracking).
- Des exports HTML/PNG/PDF (PNG via capture Qt en fallback, si Kaleido indisponible).

Notes
-----
- Le rendu interactif utilise QtWebEngine (PySide6-Addons / PyQt6-WebEngine / PyQtWebEngine selon binding).
  Si QtWebEngine n'est pas disponible, un fallback texte explicite est affiché.
- Le widget ne copie pas l'objet :class:`PALMTracer` ; il garde une **référence** passée au constructeur.
- Le calcul/formatage des figures est délégué à :class:`palm_tracer.Processing.Grapher`.
"""

import os
from typing import Any, cast, Optional

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from qtpy.QtCore import Qt
from qtpy.QtGui import QPixmap
from qtpy.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QComboBox, QFileDialog, QFrame, QGridLayout, QGroupBox, QHBoxLayout,
							QLabel, QMessageBox, QPushButton, QRadioButton, QToolButton, QVBoxLayout, QWidget)

from palm_tracer.PALMTracer import PALMTracer
from palm_tracer.Processing import Grapher
from palm_tracer.Settings.Groups import Filtering
from palm_tracer.Settings.Types import FileList, SpinInt
from palm_tracer.Tools import open_tif, print_error
from palm_tracer.UI.StandAloneWidget import StandAloneWidget

# Tentative d'import QtWebEngine (via qtpy)
try:
	from qtpy.QtWebEngineWidgets import QWebEngineView  # type: ignore

	_HAS_WEBENGINE = True
except Exception:
	QWebEngineView = None  # type: ignore
	_HAS_WEBENGINE = False


##################################################
class GraphViewerWidget(StandAloneWidget):
	"""Widget de visualisation interactive (Plotly + QtWebEngine) pour PALMTracer.

	Ce widget expose une UI compacte pour :
		- afficher des graphes à partir de la pile TIFF (Stack) ou des CSV (Localization/Tracking),
		- choisir la *famille* de données (Stack / Localization / Tracking) via 3 boutons exclusifs,
		- sélectionner la *source* dans une combo (ex. Intensité, Localizations Count, etc.),
		- exporter la figure (HTML/PNG/PDF).

	Attributs :
		- _pt (:class:`PALMTracer <palm_tracer.PALMTracer>`) : Référence vers l'instance principale de PALMTracer (aucune copie).
		- _fig  (:class:`Optional[go.Figure]`) : Dernière figure Plotly produite (pour export/maj).
		- _html  (:class:`Optional[str]`)  : Dernier HTML généré pour la figure (export .html).
		- _grapher  (:class:`Grapher <palm_tracer.Processing.Grapher>`) : Utilitaire de création de figures (histogrammes, scatter, etc.).
		- _file  (:class:`str`) : Chemin du fichier image courant (TIF).
		- _stack  (:class:`numpy.ndarray`) : Pile d'images (chargée depuis `_file`).
		- _df  (:class:`pandas.DataFrame`) : Dictionnaires de dataframe.

	Remarques :
		- Les boutons de domaine "Localization"/"Tracking" sont automatiquement désactivés si
		  aucune donnée correspondante n'est trouvée (cf. :meth:`_refresh_source_buttons`).
		- L'export PNG utilise un fallback par capture du widget Qt si Kaleido n'est pas utilisé.
	"""

	FILE_STATUS: list[str] = ["No", "Yes", "Yes (Filtered)", "Yes (Reconnected)", "Yes (Reconnected and Filtered)"]

	DATA_SRC: dict[str, list] = {
			"stk": ["Intensity"],
			"loc": ["Localizations Count", "Intensity", "Sigma X", "Sigma Y", "Circularity", "Theta", "MSE XY", "Z", "MSE Z"],
			"trc": ["Length"],
			"MSD": ["MSD"],
			"InD": ["Instant Diffusion"],
			"Fit": [["Total Intensity", "D(0) (μm²/s)", "MSD(0) (μm²)", "MSE(0)"],		# Pour Tous Fit
					["A (μm²/s)", "B (μm²)", "MSE"],									# Fit Linéaire
					["Alpha", "B (μm²)", "MSE", "Average Speed (Last-First)(μm/s)"],	# Fit Puissance
					["A (μm²)", "B (s)", "C (μm²)", "MSE", "Confinement Radius (μm)"]]  # Fit Exponentiel
			}

	# ==================================================
	# region Initialisation
	# ==================================================
	##################################################
	def __init__(self, palmtracer: PALMTracer):
		"""
		Initialise le widget (UI, connexions, état initial) et lie PALMTracer.

		:param palmtracer: Instance principale :class:`PALMTracer <palm_tracer.PALMTracer>`. sans copie (référence partagée).
		"""
		super().__init__()
		self.setWindowTitle("Graph Viewer")
		# Initialisation des membres
		self._pt = palmtracer
		self._fig: Optional[go.Figure] = None
		self._html: Optional[str] = None
		self._grapher = Grapher()
		self._file: str = ""
		self._density: bool = False

		self._stack: np.ndarray = np.empty(0)
		self._df = {"loc": pd.DataFrame(), "trc": pd.DataFrame(), "MSD": pd.DataFrame(), "InD": pd.DataFrame(), "Fit": pd.DataFrame()}

		# Construction UI
		self._init_ui()
		self._connect_signals()

		# Tracé initial
		self._actualize()

	##################################################
	def _init_ui(self):
		"""
		Construit l'interface utilisateur :
			- Colonne gauche :
				- Informations : nom du fichier, présence Localizations/Tracking.
				- Domaine : 3 boutons exclusifs (Stack/Localization/Tracking).
				- Source : combo dépendante du domaine sélectionné.
				- Filtres : section réservée (non implémentée).
				- Actions : Actualize files / Export…
			- Zone droite :
				- QWebEngineView hébergeant la figure Plotly (ou fallback texte si indisponible).
		"""

		main_layout = QHBoxLayout(self)
		self._init_layout(main_layout)

		# Colonne gauche
		left = QFrame(self)
		left.setFrameShape(QFrame.Shape.StyledPanel)
		left.setMinimumWidth(300)
		vbox = QVBoxLayout(left)
		self._init_layout(vbox)

		# Bloc Infos (lecture seule)
		grp_infos = QGroupBox("Informations")

		# Nom de fichier courant
		self._lbl_filename = QLabel(self._file if self._file != "" else "No file")

		# Statut des différentes tables (localisation / tracking / MSD / D / fit)
		self._status = {"loc": QLabel("No"), "trc": QLabel("No"), "MSD": QLabel("No"), "InD": QLabel("No"), "Fit": QLabel("No")}

		form = self._make_form(grp_infos)
		self._add_setting_row(form, "File :", self._lbl_filename)
		self._add_setting_row(form, "Localization :", self._status["loc"])
		self._add_setting_row(form, "Tracking :", self._status["trc"])
		self._add_setting_row(form, "MSD :", self._status["MSD"])
		self._add_setting_row(form, "Instant D :", self._status["InD"])
		self._add_setting_row(form, "Fit :", self._status["Fit"])

		# Bloc Source (donnée) + Type de graphe
		grp_source = QGroupBox("Source")

		h = QHBoxLayout()
		h.setSpacing(0)
		self._btn_stack, self._btn_loc, self._btn_trc = QPushButton("Stack"), QPushButton("Localization"), QPushButton("Tracks")
		for b in (self._btn_stack, self._btn_loc, self._btn_trc):
			b.setCheckable(True)
			b.setFocusPolicy(Qt.FocusPolicy.NoFocus)  # évite le focus rectangle
			h.addWidget(b)

		# Groupe exclusif
		self._btg_src = QButtonGroup(self)
		self._btg_src.setExclusive(True)
		self._btg_src.addButton(self._btn_stack, 0)
		self._btg_src.addButton(self._btn_loc, 1)
		self._btg_src.addButton(self._btn_trc, 2)

		# État initial
		self._btn_stack.setChecked(True)

		# Combo box
		form = self._make_form(grp_source)
		self._cmb_src = QComboBox()
		form.addRow(h)
		form.addRow("Source :", self._cmb_src)

		# Bloc Affichage (2 colonnes)
		grp_display = QGroupBox("Display")
		grid = QGridLayout(grp_display)
		self._display_settings: dict[str, Any] = {
				"MSD":     SpinInt("MSD Step", 1, 1, 10000, 1),
				"Log":     QCheckBox("Use Log Scale"),
				"Limits":  QCheckBox("Apply Limits"),
				"Sigma":   QCheckBox("Show σ"),
				"Gauss":   QCheckBox("Show Gaussian"),
				"KDE":     QCheckBox("Show KDE"),
				"Y Scale": QButtonGroup(None)
				}

		# Sélection du Step pour MSD (dans la partie source)
		form.addRow(self._display_settings["MSD"].layout)
		self._display_settings["MSD"].hide()  # Masquage initial

		# Appliquer limites + bouton info
		self._display_settings["Limits"].setChecked(True)
		info_btn = QToolButton()
		info_btn.setText("?")
		info_btn.setAutoRaise(True)
		info_btn.setToolTip("Limits data to ±3σ around the mean (3-sigma rule).")
		row_limits = QWidget()
		row_l = QHBoxLayout(row_limits)
		row_l.setContentsMargins(0, 0, 0, 0)
		row_l.addWidget(self._display_settings["Limits"])
		row_l.addWidget(info_btn)

		# Autres options
		self._display_settings["Sigma"].setChecked(False)
		self._display_settings["Gauss"].setChecked(False)
		self._display_settings["KDE"].setChecked(False)

		# Sélecteur d'échelle Y : Densité / Comptes
		self._rb_density = QRadioButton("Density")
		self._rb_count = QRadioButton("Count")
		self._rb_density.setChecked(True)
		self._display_settings["Y Scale"].addButton(self._rb_density)
		self._display_settings["Y Scale"].addButton(self._rb_count)

		# Placement 2 colonnes
		grid.addWidget(row_limits, 0, 0)
		grid.addWidget(self._display_settings["Sigma"], 0, 1)
		grid.addWidget(self._display_settings["Gauss"], 1, 0)
		grid.addWidget(self._display_settings["KDE"], 1, 1)
		grid.addWidget(self._rb_density, 2, 0)
		grid.addWidget(self._rb_count, 2, 1)
		grid.addWidget(self._display_settings["Log"], 3, 0)

		# Bloc Filtres (placeholder vide pour l'instant)
		grp_filters, vbox_filters = self._make_group(self, "Filters")
		# Integration des Filtres
		self._filters = Filtering()
		self._filters.update_from_dict(self._pt.settings.filtering.to_dict())
		vbox_filters.addWidget(self._filters.widget)
		# Masquage initial
		self._filters["Save"].hide()
		self._filters["Localization"].remove_header()
		self._filters["Tracks"].remove_header()
		self._filters["Localization"].hide()
		self._filters["Tracks"].hide()

		# Bouttons de gestion des filtres
		self._btn_reset_f = QPushButton("Reset")
		self._btn_update_f = QPushButton("Update")
		actions_row = QHBoxLayout()
		actions_row.addStretch(1)
		actions_row.addWidget(self._btn_reset_f)
		actions_row.addWidget(self._btn_update_f)
		vbox_filters.addLayout(actions_row)

		# Actions
		actions_row = QHBoxLayout()
		self._btn_actualize = QPushButton("Actualize files")
		self._btn_export = QPushButton("Export…")
		actions_row.addStretch(1)
		actions_row.addWidget(self._btn_actualize)
		actions_row.addWidget(self._btn_export)

		vbox.addWidget(grp_infos)
		vbox.addWidget(grp_source)
		vbox.addWidget(grp_display)
		vbox.addWidget(grp_filters)
		vbox.addLayout(actions_row)
		vbox.addStretch(1)

		self._web = self._make_web_widget()

		main_layout.addWidget(left)
		main_layout.addWidget(self._web, stretch=1)

	##################################################
	def _connect_signals(self):
		"""Connecte les signaux UI aux callbacks."""
		self._connect_web_widget(self._web)

		# Sources
		self._btg_src.idClicked.connect(self._on_source_changed)
		self._cmb_src.currentIndexChanged.connect(self._on_source_cmb_changed)

		# Display Options Connexion
		for _, setting in self._display_settings.items():
			if isinstance(setting, QCheckBox): setting.stateChanged.connect(self._update_plot)
			elif isinstance(setting, QButtonGroup): setting.idClicked.connect(self._update_plot)
			elif isinstance(setting, SpinInt): setting.connect(self._update_plot)

		# Updates
		self._btn_actualize.clicked.connect(self._actualize)
		self._btn_export.clicked.connect(self._on_export)

		# Filters
		self._btn_reset_f.clicked.connect(self._reset_filtered)
		self._btn_update_f.clicked.connect(self._update_filtered)
		self._filters.connect(self._update_plot)

	# ==================================================
	# endregion Initialisation
	# ==================================================

	# ==================================================
	# region UI Callback
	# ==================================================
	##################################################
	def _refresh_source_buttons(self) -> None:
		"""
		Active/désactive les boutons de domaine selon la disponibilité des données.
		Si le bouton actif devient indisponible (ex. pas de localisation), bascule automatiquement sur "Stack".
		"""
		self._update_df()
		self._btn_loc.setEnabled(not self._df["loc"].empty)
		self._btn_trc.setEnabled(not self._df["trc"].empty)
		# si un bouton désactivé était sélectionné, repasse sur Stack
		if self._btn_loc.isChecked() and self._df["loc"].empty: self._btn_stack.setChecked(True)
		if self._btn_trc.isChecked() and self._df["trc"].empty: self._btn_stack.setChecked(True)

	##################################################
	def _on_source_changed(self, btn_id: int) -> None:
		"""
		Mets à jour la liste des sources selon le domaine choisi puis redessine.

		:param btn_id: Identifiant du bouton domaine sélectionné (0=Stack, 1=Localization, 2=Tracking).
		"""
		## Exemple: remplir ta combo 'Source' en fonction du domaine
		self._cmb_src.blockSignals(True)
		self._cmb_src.clear()
		if btn_id == 0: self._cmb_src.addItems(self.DATA_SRC["stk"])	  # Stack
		elif btn_id == 1: self._cmb_src.addItems(self.DATA_SRC["loc"])	  # Localization
		elif btn_id == 2: self._cmb_src.addItems(self._get_tracks_src())  # Tracking
		self._cmb_src.setCurrentIndex(0)
		self._cmb_src.blockSignals(False)

		self._update_filters_ui()  # Mise à jour des filtres à afficher
		self._update_plot()		   # puis redessiner le graphe si besoin

	##################################################
	def _on_source_cmb_changed(self, btn_id: int) -> None:
		"""
		Mets à jour les filtres et l'affichage lors du changement de la variable d'intérêt.

		:param btn_id: Identifiant de la variable d'intérêt sélectionnée.
		"""
		# Affichage de l'option lors de la selection MSD pour choisir le Step et faire Histogram par ce Step
		if self._btg_src.checkedId() == 2 and btn_id == 1: self._display_settings["MSD"].show()
		else: self._display_settings["MSD"].hide()
		self._update_filters_ui()  # Mise à jour des filtres à afficher
		self._update_plot()		   # puis redessiner le graphe si besoin

	##################################################
	def _update_filters_ui(self):
		"""
		Mets à jour les filtres à afficher.
		Selon la source, les filtres ne seront pas les mêmes (pour ne pas surcharger l'interface de filtres inutiles.
		"""
		src_id = self._btg_src.checkedId()

		if src_id == 0:  # Stack
			self._filters["Save"].hide()
			self._filters["Tracks"].hide()
		elif src_id == 1:  # Localisation
			self._filters["Localization"].show()
			self._filters["Tracks"].hide()
		else:  # Tracking
			self._filters["Localization"].hide()
			self._filters["Tracks"].show()

	##################################################
	def _get_tracks_src(self) -> list[str]:
		"""
		Génère la liste des variables d'intérêt pour les Trajectoires en fonction des fichiers disponibles.

		:return: La liste des sources disponible pour les trajectoires.
		"""
		res = list(self.DATA_SRC["trc"])
		if not self._df["MSD"].empty: res += self.DATA_SRC["MSD"]
		if not self._df["InD"].empty: res += self.DATA_SRC["InD"]
		if not self._df["Fit"].empty: res += self._df["Fit"].columns[2:].tolist()

		return res

	# ==================================================
	# endregion UI Callback
	# ==================================================

	# ==================================================
	# region PALMTracer Link
	# ==================================================
	##################################################
	def _get_status(self, loc_key: str, trc_key: str, tc_key: list[str]) -> dict[str, str]:
		"""
		Retourne un dictionnaire décrivant le statut des tableaux actuellement chargés dans ``self._df``
		pour les différentes catégories de données (Localisation, Trajectoires, MSD, Diffusion instantanée, Fit).

		Cette méthode analyse les clés fournies (``loc_key``, ``trc_key``, ``tc_key``) afin de déterminer si chaque tableau correspond :
			- à un tableau standard,
			- à un tableau filtré,
			- à un tableau reconnecté (pour les trajectoires),
			- ou à une absence de données.

		Les statuts retournés sont des chaînes de caractères provenant de la constante globale :data:`self.FILE_STATUS`.

		Le dictionnaire retourné contient systématiquement les clés suivantes : ``"loc"``, ``"trc"``, ``"MSD"``, ``"InD"``, ``"Fit"``

		:param loc_key: Nom de la clé du tableau de localisation.
		:param trc_key: Nom de la clé du tableau de trajectoires.
		:param tc_key: Liste de trois clés correspondant respectivement aux tableaux MSD, diffusion instantanée et Fit.
		:return: Un dictionnaire ``{str: str}`` contenant le statut de chaque type de tableau.
		"""
		res = {"loc": self.FILE_STATUS[0], "trc": self.FILE_STATUS[0], "MSD": self.FILE_STATUS[0], "InD": self.FILE_STATUS[0], "Fit": self.FILE_STATUS[0]}

		if self._df["loc"].empty: res["loc"] = self.FILE_STATUS[0]  # Aucun tableau ou tableau vide
		elif "f_" in loc_key: res["loc"] = self.FILE_STATUS[2]		# Tableau filtré
		else: res["loc"] = self.FILE_STATUS[1]						# Tableau standard

		if self._df["trc"].empty: res["trc"] = self.FILE_STATUS[0]  # Aucun tableau ou tableau vide
		elif "f_" in trc_key:
			if "blk" in trc_key: res["trc"] = self.FILE_STATUS[4]   # Tableau reconnecté filtré
			else: res["trc"] = self.FILE_STATUS[2]					# Tableau filtré
		else:
			if "blk" in trc_key: res["trc"] = self.FILE_STATUS[3]   # Tableau reconnecté non filtré
			else: res["trc"] = self.FILE_STATUS[1]					# Tableau standard

		tcs = ["MSD", "InD", "Fit"]
		for i in range(3):
			if self._df[tcs[i]].empty: res[tcs[i]] = self.FILE_STATUS[0]  # Aucun tableau ou tableau vide
			elif "f_" in tc_key[i]: res[tcs[i]] = self.FILE_STATUS[2]	  # Tableau filtré
			else: res[tcs[i]] = self.FILE_STATUS[1]						  # Tableau standard
		return res

	##################################################
	def _update_df(self):
		"""Récupère les dataframes et met à jour les status."""
		# Récupération des clés
		loc_key = self._pt.get_localization_key()
		trc_key = self._pt.get_tracks_key()
		tc_key = self._pt.get_tracks_compute_key()

		# Mise à jour des Dataframe
		self._df["loc"] = self._pt.df[loc_key]
		self._df["trc"] = self._pt.df[trc_key]
		self._df["MSD"] = self._pt.df[tc_key[0]]
		self._df["InD"] = self._pt.df[tc_key[1]]
		self._df["Fit"] = self._pt.df[tc_key[2]]

		# Mise à jour des Status
		status = self._get_status(loc_key, trc_key, tc_key)
		for key in status: self._status[key].setText(status[key])

	##################################################
	def _actualize(self):
		"""
		Actualise les fichiers/données depuis l'état PALMTracer :
			- Lit le TIF sélectionné (pile `_stack`) pour l'affichage Stack.
			- Met à jour les libellés d'information et l'état d'activation des boutons de domaine.
			- Sélectionne par défaut le domaine "Stack" et redessine.

		En cas d'erreur de lecture, logue l'erreur via :func:`print_error`.
		"""
		self._filters.update_from_dict(self._pt.settings.filtering.to_dict())

		# Métadonnées d'information
		self._file = (cast(FileList, self._pt.settings.batch["Files"]).get_selected())
		if self._file != "":
			try: self._stack = open_tif(self._file)
			except Exception as e: print_error(f"Error loading {self._file} in GraphViewer : {e}")

		self._lbl_filename.setText(os.path.basename(self._file) if self._file != "" else "No File")
		self._refresh_source_buttons()  # Applique has_loc/has_track
		self._on_source_changed(0)		# Change la source pour Stack

	##################################################
	def _reset_filtered(self):
		"""Supprime les dataframes de filtre."""
		self._pt.reset_filtered()  # Nettoyage des dataframes filtrés
		self._update_df()		   # Récupération des bons dataframe
		self._update_plot()		   # puis redessiner le graphe si besoin

	##################################################
	def _update_filtered(self):
		"""Applique les filtres sur les dataframes."""
		with self._pt.settings.signal_blocked():
			self._pt.settings.filtering.update_from_dict(self._filters.to_dict())
			self._pt.update_filtered()  # Mise à jour des filtres

		self._update_df()	 # Récupération des bons dataframe
		self._update_plot()  # puis redessiner le graphe si besoin

	# ==================================================
	# endregion PALMTracer Link
	# ==================================================

	# ==================================================
	# region Drawing
	# ==================================================
	##################################################
	def _update_plot(self):
		"""Construit la figure Plotly courante en fonction du domaine et de la source."""
		src_id = self._btg_src.checkedId()
		src_type = self._cmb_src.currentText()
		limit = self._display_settings["Limits"].checkState() == Qt.CheckState.Checked
		sigma = self._display_settings["Sigma"].checkState() == Qt.CheckState.Checked
		kde = self._display_settings["KDE"].checkState() == Qt.CheckState.Checked
		gauss = self._display_settings["Gauss"].checkState() == Qt.CheckState.Checked
		density = self._rb_density.isChecked()

		# Préparation des Données
		data, title = self.get_plot_data()

		# Selection du graphique à afficher
		fig: go.Figure
		if src_id == 1 and src_type == "Localizations Count":
			fig = self._grapher.scatter(data, title, xlabel="Plane", ylabel="Count", limit=limit, show_sigma=sigma)
		elif src_id == 2 and src_type == "Length":
			fig = self._grapher.scatter(data, title, xlabel="Track", ylabel="Length", limit=limit, show_sigma=sigma)
		else:
			fig = self._grapher.histogram(data, title, limit=limit, show_sigma=sigma, kde=kde, gaussian=gauss, density=density)

		self._update_web_widget(self._web, fig)

	##################################################
	def get_plot_data(self) -> tuple[np.ndarray, str]:
		""" Récupère et prépare les données pour l'affichage."""
		src_id = self._btg_src.checkedId()
		src_type = self._cmb_src.currentText()
		log_scale = self._display_settings["Log"].isChecked()

		# Stack
		if src_id == 0:
			tmp = self._stack
			# Filtrage par PLan, si sélectionné
			if self._filters["Plane"].active:
				limits = self._filters["Plane"].get_value()
				tmp = tmp[max(limits[0] - 1, 0):min(limits[1], int(tmp.shape[0])), ...]
			return self._log_data(tmp, log_scale), f"Stack {src_type}"

		# Localizations
		elif src_id == 1:
			if src_type == "Localizations Count":
				s = self._df["loc"]["Plane"].astype(np.int64)
				if s.empty:  return np.empty(0), src_type
				else:
					planes = np.arange(int(s.min()), int(s.max()) + 1, dtype=int)  # Récupération des plans du min au max (si plans vide, ils seront compris)
					counts = (s.groupby(s).size().reindex(pd.Index(planes), fill_value=0).to_numpy(dtype=int))  # Comptage par groupe
					return np.column_stack((planes, counts)), src_type
			else:
				s = self._df["loc"].get(src_type)  # None si la colonne n'existe pas
				if s is None: return np.empty(0), f"Localizations {src_type}"
				return self._log_data(s.to_numpy(dtype=float), log_scale), f"Localizations {src_type}"

		# Tracks
		else:
			if src_type == "Length":  # Cas particulier, il est peut-être dans le tableau Fit, mais on va utiliser le tableau Tracks initial.
				group = self._df["trc"].groupby("Track")["Plane"].agg(["min", "max"])		# Groupement par track + calcul min et max
				group["delta"] = group["max"] - group["min"]								# Calcul du delta
				res = np.column_stack((group.index.to_numpy(), group["delta"].to_numpy()))  # Conversion vers numpy 2D : colonne Track + delta
				return res, f"Tracks {src_type}"

			elif src_type == "MSD":
				res = self._df["MSD"]
				step = self._display_settings["MSD"].get_value()											# Récupération du numéro du Step.
				col = f"Step {step}"																		# Récupération du nom de la colonne.
				if not {"Track", col}.issubset(res.columns): return np.empty(0), f"Tracks MSD Step {step}"  # Vérification  de présence des colonnes
				track, values = res["Track"].astype(int).to_numpy(), res[col].astype(float).to_numpy()		# Séparation track et valeur
				res = np.column_stack((track, self._log_data(values, log_scale)))							# Application du log sur les valeurs
				return res[np.isfinite(res).all(axis=1)], f"Tracks MSD Step {step}"							# Retour avec filtrage des Lignes NaN

			elif src_type == "Instant Diffusion":
				res = self._df["InD"].drop(columns=["Track"], errors="ignore").to_numpy().ravel()			# Récupération des colonnes
				res = self._log_data(res, log_scale)														# Application du log sur les valeurs
				return res[np.isfinite(res)], f"Tracks {src_type}"											# Retour avec filtrage des Lignes NaN

			else:
				res = self._df["Fit"]
				if not {"Track", src_type}.issubset(res.columns): return np.empty(0), f"Tracks {src_type}"   # Vérification de présence des colonnes
				track, values = res["Track"].astype(int).to_numpy(), res[src_type].astype(float).to_numpy()  # Séparation track et valeur
				res = np.column_stack((track, self._log_data(values, log_scale)))							 # Application du log sur les valeurs
				return res[np.isfinite(res).all(axis=1)], f"Tracks {src_type}"								 # Retour avec filtrage des Lignes NaN

	##################################################
	@staticmethod
	def _log_data(data: np.ndarray, log: bool) -> np.ndarray:
		"""
		Application du log avec suppression du warning pour les valeurs <= 0 et remplacement par Nan de ces valeurs.

		:param data: Données à transformer
		:param log: Application du log ou non
		:return: Données transformées
		"""
		with np.errstate(divide='ignore', invalid='ignore'): return np.where(data > 0, np.log10(data), np.nan) if log else data

	##################################################
	def _export_png_via_qt(self, path: str, scale: float = 1.0) -> bool:  # pragma: no cover pytest à du mal avec les ouvertures en série de fenêtres
		"""
		Exporte en PNG via capture du widget QWebEngineView (fallback sans Kaleido).

		Limitations :
			- Capture la zone visible (viewport) : pour une image plus grande, redimensionner temporairement le widget avant capture.
			- Nécessite QtWebEngine pour capturer le rendu.

		:param path: Chemin de sortie du PNG.
		:param scale: Facteur d'échelle appliqué à la capture.
		:return: True si le fichier a été écrit, False sinon.
		"""
		if _HAS_WEBENGINE and isinstance(self._web, QWebEngineView):
			QApplication.processEvents()
			pix: QPixmap = self._web.grab()
			if not pix.isNull():
				if scale != 1.0:
					size = pix.size() * scale
					pix = pix.scaled(size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
				return pix.save(path, "PNG")
		return False

	##################################################
	def _on_export(self):  # pragma: no cover pytest à du mal avec les ouvertures en série de fenêtres
		"""
		Ouvre un dialogue et exporte la figure selon l'extension choisie.

		Formats supportés :
			- .html : enregistre l'HTML interactif (incluant PlotlyJS).
			- .png  : exporte une image du rendu (fallback par capture Qt).
			- .pdf  : imprime via QWebEngineView.printToPdf (si QtWebEngine présent).

		Comportement :
			- En l'absence de figure/HTML, avertit l'utilisateur.
			- Sur échec d'écriture, affiche un message d'erreur.
		"""
		if self._fig is None and self._html is None:
			QMessageBox.warning(self, "Export", "No figures to export.")
			return
		suggested = (self._file or "graph").rsplit("/", 1)[-1]
		path, selected_filter = QFileDialog.getSaveFileName(self, "Export the graph", suggested, "HTML (*.html);;PNG (*.png);;PDF (*.pdf)")
		if not path: return
		try:
			if path.lower().endswith(".png"):
				# ok = False
				# Kaleido tourne à l'infini donc capture de widget QT...
				# try:  				# 1) Essai Kaleido (si dispo)
				#	import kaleido
				#	assert self._fig is not None
				#	self._fig.write_image(path, scale=2.0)
				#	ok = True
				# except Exception:  # 2) Fallback: capture Qt du QWebEngineView
				#	ok = self._export_png_via_qt(path, scale=2)
				ok = self._export_png_via_qt(path, scale=2)
				if not ok: raise RuntimeError("PNG export failure (Kaleido & Qt fallback).")

			elif path.lower().endswith(".html"):
				assert self._html is not None
				with open(path, "w", encoding="utf-8") as f: f.write(self._html)

			elif path.lower().endswith(".pdf"):
				if _HAS_WEBENGINE and isinstance(self._web, QWebEngineView):
					try: self._web.page().printToPdf(path)
					except Exception as e:
						QMessageBox.warning(self, "Export PDF", f"PDF printing failure : {e}")
						return
				else:
					QMessageBox.warning(self, "Export PDF", "QtWebEngine is required for PDF export.")
					return
			else:
				# Pas d'extension reconnue -> HTML par défaut
				with open(path + ".html", "w", encoding="utf-8") as f: f.write(self._html or "")
				path = path + ".html"
			QMessageBox.information(self, "Export", f"Export successful : {path}")
		except Exception as e: QMessageBox.critical(self, "Export", f"Export failed : {e}")

	# ==================================================
	# endregion Drawing
	# ==================================================


##################################################
if __name__ == "__main__":  # pragma: no cover
	import sys

	app = QApplication(sys.argv)
	pt = PALMTracer()
	w = GraphViewerWidget(pt)
	w.resize(1000, 600)
	w.show()
	sys.exit(app.exec_())
