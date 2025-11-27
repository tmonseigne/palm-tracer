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

.. todo::
	- Implémenter les sources Tracking (MSD, vitesse, etc.) et leurs graphes associés.
"""

import os
from typing import cast, Optional

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from qtpy.QtCore import Qt
from qtpy.QtGui import QPixmap
from qtpy.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QComboBox, QFileDialog, QFormLayout, QFrame, QGridLayout, QGroupBox, QHBoxLayout,
							QLabel, QMessageBox, QPushButton, QRadioButton, QTextBrowser, QToolButton, QVBoxLayout, QWidget)

from palm_tracer.Settings.Groups import Filtering

# Tentative d'import QtWebEngine (via qtpy)
try:
	from qtpy.QtWebEngineWidgets import QWebEngineView  # type: ignore

	_HAS_WEBENGINE = True
except Exception:
	QWebEngineView = None  # type: ignore
	_HAS_WEBENGINE = False

from palm_tracer.Tools import open_tif, print_error
from palm_tracer.PALMTracer import PALMTracer
from palm_tracer.Processing import Grapher
from palm_tracer.Settings.Types import FileList

FILE_STATUS = ["No", "Yes", "Yes (Filtered)", "Yes (Reconnected)", "Yes (Reconnected and Filtered)"]

DATA_SRC: dict[str, list] = {
		"stk": ["Intensity"],
		"loc": ["Localizations Count", "Integrated Intensity", "Intensity", "Sigma X", "Sigma Y", "Circularity", "Theta", "MSE XY", "Z", "MSE Z"],
		"trc": ["Length"],
		"MSD": ["MSD"],
		"InD": ["Instant Diffusion"],
		"Fit": [["Total Intensity", "D(0) (μm²/s)", "MSD(0) (μm²)", "MSE(0)"],		# Pour tous Fit
				["A (μm²/s)", "B (μm²)", "MSE"],									# Fit Linéaire
				["Alpha", "B (μm²)", "MSE", "Average Speed (Last-First)(μm/s)"],    # Fit Puissance
				["A (μm²)", "B (s)", "C (μm²)", "MSE", "Confinement Radius (μm)"]]  # Fit Exponentiel
		}


##################################################
class GraphViewerWidget(QWidget):
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
		main_layout.setContentsMargins(5, 5, 5, 5)
		main_layout.setSpacing(5)

		# Colonne gauche
		left = QFrame(self)
		left.setFrameShape(QFrame.Shape.StyledPanel)
		left.setMinimumWidth(300)
		vbox = QVBoxLayout(left)
		vbox.setContentsMargins(5, 5, 5, 5)
		vbox.setSpacing(5)

		# Bloc Infos (lecture seule)
		grp_infos = QGroupBox("Informations")
		form = QFormLayout(grp_infos)

		# Nom de fichier courant
		self._lbl_filename = QLabel(self._file if self._file != "" else "No file")

		# Statut des différentes tables (localisation / tracking / MSD / D / fit)
		self._status = {"loc": QLabel("No"), "trc": QLabel("No"), "MSD": QLabel("No"), "InD": QLabel("No"), "Fit": QLabel("No")}

		form.addRow("File :", self._lbl_filename)
		form.addRow("Localization :", self._status["loc"])
		form.addRow("Tracking :", self._status["trc"])
		form.addRow("MSD :", self._status["MSD"])
		form.addRow("Instant D :", self._status["InD"])
		form.addRow("Fit :", self._status["Fit"])

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
		form = QFormLayout(grp_source)
		self._cmb_src = QComboBox()
		form.addRow(h)
		form.addRow("Source :", self._cmb_src)

		grp_source.setStyleSheet("""
			QPushButton { border: 1px solid #c7c7c7; padding: 6px 12px; background: #f7f7f7; }
			QPushButton + QPushButton { border-left: none; } /* fusion visuelle */
			QPushButton:first-child { border-top-left-radius: 8px; border-bottom-left-radius: 8px; }
			QPushButton:last-child { border-top-right-radius: 8px; border-bottom-right-radius: 8px; }
			QPushButton:pressed { background: #e9eff7; border-color: #6aa0e8; }
			QPushButton:checked	{ background: #e9eff7; border-color: #6aa0e8; }
			QPushButton:disabled { color: #999; background: #fafafa; }
		""")

		# Bloc Affichage (2 colonnes)
		grp_display = QGroupBox("Display")
		grid = QGridLayout(grp_display)
		# Appliquer limites + bouton info
		self._chk_limits = QCheckBox("Apply limits")
		self._chk_limits.setChecked(True)
		info_btn = QToolButton()
		info_btn.setText("?")
		info_btn.setAutoRaise(True)
		info_btn.setToolTip("Limits data to ±3σ around the mean (3-sigma rule).")
		row0 = QWidget()
		row0_l = QHBoxLayout(row0)
		row0_l.setContentsMargins(0, 0, 0, 0)
		row0_l.addWidget(self._chk_limits)
		row0_l.addWidget(info_btn)
		# Autres options
		self._chk_sigma = QCheckBox("Show σ")
		self._chk_sigma.setChecked(False)
		self._chk_gauss = QCheckBox("Show gaussian")
		self._chk_gauss.setChecked(False)
		self._chk_kde = QCheckBox("Show KDE")
		self._chk_kde.setChecked(False)
		# Sélecteur d'échelle Y : Densité / Comptes
		self._rb_density = QRadioButton("Density")
		self._rb_count = QRadioButton("Count")
		self._rb_density.setChecked(True)
		self._grp_y_mode = QButtonGroup(self)
		self._grp_y_mode.addButton(self._rb_density)
		self._grp_y_mode.addButton(self._rb_count)
		# Placement 2 colonnes
		grid.addWidget(row0, 0, 0)
		grid.addWidget(self._chk_sigma, 0, 1)
		grid.addWidget(self._chk_gauss, 1, 0)
		grid.addWidget(self._chk_kde, 1, 1)
		grid.addWidget(self._rb_density, 2, 0)
		grid.addWidget(self._rb_count, 2, 1)

		# Bloc Filtres (placeholder vide pour l'instant)
		grp_filters = QGroupBox("Filters (comming soon)")
		vbox_filters = QVBoxLayout(grp_filters)
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

		# Zone droite : QWebEngineView avec Plotly
		if _HAS_WEBENGINE: self._web = QWebEngineView(self)
		else:  # pragma: no cover - Fallback affichant un message d'erreur explicite
			self._web = QTextBrowser(self)
			self._web.setText("<b>QtWebEngine unavailable</b><br>Install PyQtWebEngine for Plotly display.")

		main_layout.addWidget(left)
		main_layout.addWidget(self._web, stretch=1)

	##################################################
	def _connect_signals(self):
		"""Connecte les signaux UI aux callbacks."""
		self._btg_src.idClicked.connect(self._on_source_changed)
		self._cmb_src.currentTextChanged.connect(self._update_filters_ui)
		self._cmb_src.currentTextChanged.connect(self._update_plot)
		self._chk_limits.stateChanged.connect(self._update_plot)
		self._chk_sigma.stateChanged.connect(self._update_plot)
		self._chk_gauss.stateChanged.connect(self._update_plot)
		self._chk_kde.stateChanged.connect(self._update_plot)
		self._grp_y_mode.idClicked.connect(self._update_plot)
		self._btn_actualize.clicked.connect(self._actualize)
		self._btn_export.clicked.connect(self._on_export)
		self._btn_reset_f.clicked.connect(self._reset_filtered)
		self._btn_update_f.clicked.connect(self._update_filtered)

	# ==================================================
	# endregion Initialisation
	# ==================================================

	# ==================================================
	# region Callback
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
		Met à jour la liste des sources selon le domaine choisi puis redessine.

		:param btn_id: Identifiant du bouton domaine sélectionné (0=Stack, 1=Localization, 2=Tracking).
		"""
		## Exemple: remplir ta combo 'Source' en fonction du domaine
		self._cmb_src.blockSignals(True)
		self._cmb_src.clear()
		if btn_id == 0: self._cmb_src.addItems(DATA_SRC["stk"])    # Stack
		elif btn_id == 1: self._cmb_src.addItems(DATA_SRC["loc"])  # Localization
		elif btn_id == 2: self._cmb_src.addItems(self._get_tracks_src())  # Tracking
		self._cmb_src.setCurrentIndex(0)
		self._cmb_src.blockSignals(False)

		self._update_filters_ui()  # Mise à jour des filtres à afficher
		self._update_plot()		   # puis redessiner le graphe si besoin

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

		self._update_df()			# Récupération des bons dataframe
		self._update_plot()			# puis redessiner le graphe si besoin

	##################################################
	def _update_filters_ui(self):
		"""
		Mets à jour les filtres à afficher.
		Selon la source, les filtres ne seront pas les mêmes (pour ne pas surcharger l'interface de filtres inutiles.
		"""
		src_id = self._btg_src.checkedId()
		src_type = self._cmb_src.currentText()

		if src_id == 0:  # Stack
			self._filters["Localization"].hide()
			self._filters["Tracks"].hide()
		elif src_id == 1:  # Localisation
			self._filters["Localization"].show()
			self._filters["Tracks"].hide()
		else:  # Tracking
			self._filters["Localization"].hide()
			self._filters["Tracks"].show()

	##################################################
	def _update_plot(self):
		"""Construit la figure Plotly courante en fonction du domaine et de la source."""
		src_id = self._btg_src.checkedId()
		src_type = self._cmb_src.currentText()
		limit = self._chk_limits.checkState() == Qt.CheckState.Checked
		sigma = self._chk_sigma.checkState() == Qt.CheckState.Checked
		kde = self._chk_kde.checkState() == Qt.CheckState.Checked
		gauss = self._chk_gauss.checkState() == Qt.CheckState.Checked
		density = self._rb_density.isChecked()
		# Selection du graphique à afficher
		fig: go.Figure
		if src_id == 0:
			# filtre de la pile self._stack (par plan et par intensité selon les filtres
			# tmp = self._stack
			# if src_type == "Intensity": fig = self._grapher.histogram(self._stack, f"Stack {src_type}", limit=limit, show_sigma=sigma,
			# 														  kde=kde, gaussian=gauss, density=density)
			# else: fig = self._grapher.blank("Invalid Selection")
			fig = self._grapher.histogram(self._stack, f"Stack {src_type}", limit=limit, show_sigma=sigma, kde=kde, gaussian=gauss, density=density)
		elif src_id == 1:
			# filtre du panda self._loc
			tmp = self._df["loc"]
			if src_type == "Localizations Count":
				s = tmp["Plane"].astype(np.int64, copy=False)
				if s.empty: fig = self._grapher.blank(src_type)
				else:
					planes = np.arange(int(s.min()), int(s.max()) + 1, dtype=int)  # Récupération des plans du min au max (si plans vide, ils seront compris)
					counts = (s.groupby(s).size().reindex(pd.Index(planes), fill_value=0).to_numpy(dtype=int))  # Comptage par groupe
					fig = self._grapher.scatter(np.column_stack((planes, counts)), f"Localizations {src_type}", limit=limit, xlabel="Plane", ylabel="Count")
			else:
				s = tmp.get(src_type)  # None si la colonne n'existe pas
				if s is None: fig = self._grapher.blank(f"Localizations {src_type}")
				else: fig = self._grapher.histogram(s.to_numpy(dtype=float, copy=False), f"Localizations {src_type}", limit=limit,
													show_sigma=sigma, kde=kde, gaussian=gauss, density=density)
		else:
			if src_type == "Length": # Cas particulier, il est peut-être dans le tableau Fit, mais on va utiliser le tableau Tracks initial.
				group = self._df["trc"].groupby("Track")["Plane"].agg(["min", "max"]) # Groupement par track + calcul min et max
				group["delta"] = group["max"] - group["min"] # Calcul du delta
				res = np.column_stack((group.index.to_numpy(), group["delta"].to_numpy())) # Conversion vers numpy 2D : colonne Track + delta
				fig = self._grapher.scatter(res, f"Tracks {src_type}", limit=limit, xlabel="Track", ylabel="Length")
			elif src_type == "MSD":
				# TODO que faire pour celui là un histogramme par lag ? le MSD moyen par track, l'histogramme des MSD peu importe le lag ?
				fig = self._grapher.blank(f"Tracking {src_type} Not Yet Implemented.")
			elif src_type == "Instant Diffusion":
				# TODO que faire pour celui là un histogramme par fenêtre ? le Instant D moyen par track, l'histogramme des Instant D peu importe la fenêtre ?
				fig = self._grapher.blank(f"Tracking {src_type} Not Yet Implemented.")
			else:
				s = self._df["Fit"].get(src_type)  # None si la colonne n'existe pas
				if s is None: fig = self._grapher.blank(f"Tracks {src_type}")
				else: fig = self._grapher.histogram(s.to_numpy(dtype=float, copy=False), f"Tracks {src_type}", limit=limit,
													show_sigma=sigma, kde=kde, gaussian=gauss, density=density)

			#fig = self._grapher.blank(f"Tracking {src_type} Not Yet Implemented.")

		# Mode bar (export, zoom...) : laissé par défaut; on peut alléger si besoin
		html = pio.to_html(fig, include_plotlyjs="cdn", full_html=False, config={"responsive": True, "displaylogo": False})
		self._fig = fig
		self._html = html

		if _HAS_WEBENGINE and isinstance(self._web, QWebEngineView): self._web.setHtml(html)
		else:  # pragma: no cover - Fallback affichant un message d'erreur explicite
			self._web.setText("<b>QtWebEngine unavailable</b><br>Install PyQtWebEngine for Plotly display.")

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
	def _get_status(self, loc_key: str, trc_key: str, tc_key: list[str]) -> dict[str, str]:
		"""
		Retourne un dictionnaire décrivant le statut des tableaux actuellement chargés dans ``self._df``
		pour les différentes catégories de données (Localisation, Trajectoires, MSD, Diffusion instantanée, Fit).

		Cette méthode analyse les clés fournies (``loc_key``, ``trc_key``, ``tc_key``) afin de déterminer si chaque tableau correspond :
			- à un tableau standard,
			- à un tableau filtré,
			- à un tableau reconnecté (pour les trajectoires),
			- ou à une absence de données.

		Les statuts retournés sont des chaînes de caractères provenant de la constante globale :data:`FILE_STATUS`.

		Le dictionnaire retourné contient systématiquement les clés suivantes : ``"loc"``, ``"trc"``, ``"MSD"``, ``"InD"``, ``"Fit"``

		:param loc_key: Nom de la clé du tableau de localisation.
		:param trc_key: Nom de la clé du tableau de trajectoires.
		:param tc_key: Liste de trois clés correspondant respectivement aux tableaux MSD, diffusion instantanée et Fit.
		:return: Un dictionnaire ``{str: str}`` contenant le statut de chaque type de tableau.
		"""
		res = {"loc": FILE_STATUS[0], "trc": FILE_STATUS[0], "MSD": FILE_STATUS[0], "InD": FILE_STATUS[0], "Fit": FILE_STATUS[0]}

		if self._df["loc"].empty: res["loc"] = FILE_STATUS[0]  # Aucun tableau ou tableau vide
		elif "f_" in loc_key: res["loc"] = FILE_STATUS[2]	   # Tableau filtré
		else: res["loc"] = FILE_STATUS[1]					   # Tableau standard

		if self._df["trc"].empty: res["trc"] = FILE_STATUS[0]  # Aucun tableau ou tableau vide
		elif "f_" in trc_key:
			if "blk" in trc_key: res["trc"] = FILE_STATUS[4]  # Tableau reconnecté filtré
			else: res["trc"] = FILE_STATUS[2]				  # Tableau filtré
		else:
			if "blk" in trc_key: res["trc"] = FILE_STATUS[3]  # Tableau reconnecté non filtré
			else: res["trc"] = FILE_STATUS[1]				  # Tableau standard

		tcs = ["MSD", "InD", "Fit"]
		for i in range(3):
			if self._df[tcs[i]].empty: res[tcs[i]] = FILE_STATUS[0]  # Aucun tableau ou tableau vide
			elif "f_" in tc_key[i]: res[tcs[i]] = FILE_STATUS[2]	 # Tableau filtré
			else: res[tcs[i]] = FILE_STATUS[1]						 # Tableau standard
		return res

	##################################################
	def _get_tracks_src(self) -> list[str]:
		"""

		:return: La liste des sources disponible pour les trajectoires.
		"""
		res = list(DATA_SRC["trc"])
		if not self._df["MSD"].empty: res+=DATA_SRC["MSD"]
		if not self._df["InD"].empty: res+=DATA_SRC["InD"]
		if not self._df["Fit"].empty: res+=self._df["Fit"].columns[2:].tolist()

		return res

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
	# endregion Callback
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
