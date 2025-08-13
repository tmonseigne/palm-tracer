"""
Module contenant la classe :class:`GraphViewerWidget` pour la visualisation interactive
des graphiques liés aux données PALMTracer (pile TIFF, localisations, tracking).

Ce widget fournit :
- Une interface en deux parties :
  • Colonne gauche : informations fichier + présence localisation/tracking, choix du domaine
    (Stack / Localization / Tracking) via 3 boutons exclusifs, et sélection de la source.
  • Zone droite : rendu d’un graphe Plotly dans un QWebEngineView (zoom, pan, hover, export).
- Un couplage léger avec :class:`PALMTracer` pour accéder aux fichiers en cours et charger
  automatiquement pile/CSV (localisations/tracking).
- Des exports HTML/PNG/PDF (PNG via capture Qt en fallback, si Kaleido indisponible).

Notes
-----
- Le rendu interactif utilise QtWebEngine (PySide6-Addons / PyQt6-WebEngine / PyQtWebEngine selon binding).
  Si QtWebEngine n’est pas disponible, un fallback texte explicite est affiché.
- Le widget ne copie pas l’objet :class:`PALMTracer` ; il garde une **référence** passée au constructeur.
- Le calcul/formatage des figures est délégué à :class:`palm_tracer.Processing.Grapher`.

.. todo::
    - Ajouter des filtres (bloc réservé dans l’UI).
    - Implémenter les sources Tracking (MSD, vitesse, etc.) et leurs graphes associés.
"""

import os
from typing import cast, Optional

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from qtpy import QtCore, QtGui
from qtpy.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QComboBox, QFileDialog, QFormLayout, QFrame, QGridLayout, QGroupBox, QHBoxLayout,
							QLabel, QMessageBox, QPushButton, QRadioButton, QTextBrowser, QToolButton, QVBoxLayout, QWidget)

# Tentative d'import QtWebEngine (via qtpy)
try:  # pragma: no cover - dépend de l'environnement
	from qtpy.QtWebEngineWidgets import QWebEngineView  # type: ignore

	_HAS_WEBENGINE = True
except Exception:  # pragma: no cover
	QWebEngineView = None  # type: ignore
	_HAS_WEBENGINE = False

from palm_tracer.Tools import get_last_file, open_tif, print_error
from palm_tracer.PALMTracer import PALMTracer
from palm_tracer.Processing import Grapher
from palm_tracer.Settings.Types import FileList


class GraphViewerWidget(QWidget):
	"""Widget de visualisation interactive (Plotly + QtWebEngine) pour PALMTracer.

    Ce widget expose une UI compacte pour :
    - afficher des graphes à partir de la pile TIFF (Stack) ou des CSV (Localization/Tracking),
    - choisir la *famille* de données (Stack / Localization / Tracking) via 3 boutons exclusifs,
    - sélectionner la *source* dans une combo (ex. Intensité, Localizations Count, etc.),
    - exporter la figure (HTML/PNG/PDF).

    Attributs principaux
    --------------------
    _pt : PALMTracer
        Référence vers l’instance principale de PALMTracer (aucune copie).
    _fig : Optional[go.Figure]
        Dernière figure Plotly produite (pour export/maj).
    _html : Optional[str]
        Dernier HTML généré pour la figure (export .html).
    _grapher : Grapher
        Utilitaire de création de figures (histogrammes, scatter, etc.).
    _file : str
        Chemin du fichier image courant (TIF).
    _csv_path : str
        Chemin de base servant à rechercher les CSV de localisation/tracking.
    _loc_file, _trc_file : str
        Derniers CSV de localisation/tracking détectés.
    _has_loc, _has_trc : bool
        Présence de données de localisation/tracking.
    _stack : np.ndarray
        Pile d’images (chargée depuis `_file`).
    _loc, _trc : pd.DataFrame
        Données tabulaires (localisations / tracking) si présentes.

    Remarques
    ---------
    - Les boutons de domaine "Localization"/"Tracking" sont automatiquement désactivés si
      aucune donnée correspondante n’est trouvée (cf. `_refresh_source_buttons`).
    - L’export PNG utilise un fallback par capture du widget Qt si Kaleido n’est pas utilisé.
    """

	# ==================================================
	# region Init
	# ==================================================
	##################################################
	def __init__(self, palmtracer: PALMTracer):
		"""
		Initialise le widget (UI, connexions, état initial) et lie PALMTracer.

		:param palmtracer: Instance principale :class:`PALMTracer`. sans copie (référence partagée).
		"""
		super().__init__()
		# Initialisation des membres
		self._pt = palmtracer
		self._fig: Optional[go.Figure] = None
		self._html: Optional[str] = None
		self._grapher = Grapher()
		self._file: str = ""
		self._csv_path: str = ""
		self._loc_file: str = ""
		self._trc_file: str = ""
		self._has_loc: bool = False
		self._has_trc: bool = False
		self._density: bool = False

		self._stack: np.ndarray = np.empty(0)
		self._loc: pd.DataFrame = pd.DataFrame()
		self._trc: pd.DataFrame = pd.DataFrame()

		# Construction UI
		self._init_ui()
		self._connect_signals()

		# Tracé initial
		self._actualize()

	##################################################
	def _init_ui(self):
		"""
		Construit l'interface utilisateur.

		- Colonne gauche :
		  • Informations : nom du fichier, présence Localizations/Tracking.
		  • Domaine : 3 boutons exclusifs (Stack/Localization/Tracking).
		  • Source : combo dépendante du domaine sélectionné.
		  • Filtres : section réservée (non implémentée).
		  • Actions : Actualize files / Export…
		- Zone droite :
		  • QWebEngineView hébergeant la figure Plotly (ou fallback texte si indisponible).
		"""

		main_layout = QHBoxLayout(self)
		main_layout.setContentsMargins(5, 5, 5, 5)
		main_layout.setSpacing(5)

		# Colonne gauche
		left = QFrame(self)
		left.setFrameShape(QFrame.StyledPanel)
		left.setMinimumWidth(280)
		vbox = QVBoxLayout(left)
		vbox.setContentsMargins(5, 5, 5, 5)
		vbox.setSpacing(5)

		# Bloc Infos (lecture seule)
		grp_infos = QGroupBox("Informations")
		form = QFormLayout(grp_infos)
		self._lbl_filename = QLabel(self._file if self._file != "" else "No")
		self._lbl_has_loc = QLabel("Yes" if self._has_loc else "No")
		self._lbl_has_trc = QLabel("Yes" if self._has_trc else "No")
		form.addRow("File :", self._lbl_filename)
		form.addRow("Localization :", self._lbl_has_loc)
		form.addRow("Tracking :", self._lbl_has_trc)

		# Bloc Source (donnée) + Type de graphe
		grp_source = QGroupBox("Source")

		h = QHBoxLayout()
		h.setSpacing(0)
		self._btn_stack, self._btn_loc, self._btn_trk = QPushButton("Stack"), QPushButton("Localization"), QPushButton("Tracking")
		for b in (self._btn_stack, self._btn_loc, self._btn_trk):
			b.setCheckable(True)
			b.setFocusPolicy(QtCore.Qt.NoFocus)  # évite le focus rectangle
			h.addWidget(b)

		# Groupe exclusif
		self._btg_src = QButtonGroup(self)
		self._btg_src.setExclusive(True)
		self._btg_src.addButton(self._btn_stack, 0)
		self._btg_src.addButton(self._btn_loc, 1)
		self._btg_src.addButton(self._btn_trk, 2)

		# État initial
		self._btn_stack.setChecked(True)

		# Combo box
		form = QFormLayout(grp_source)
		self._cmb_src = QComboBox()
		form.addRow(h)
		form.addRow("Source :", self._cmb_src)

		grp_source.setStyleSheet("""
				       QPushButton {
				           border: 1px solid #c7c7c7;
				           padding: 6px 12px;
				           background: #f7f7f7;
				       }
				       QPushButton + QPushButton { border-left: none; } /* fusion visuelle */
				       QPushButton:first-child { border-top-left-radius: 8px; border-bottom-left-radius: 8px; }
				       QPushButton:last-child  { border-top-right-radius: 8px; border-bottom-right-radius: 8px; }
				       QPushButton:checked     { background: #e9eff7; border-color: #6aa0e8; }
				       QPushButton:disabled    { color: #999; background: #fafafa; }
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
		vbox_filters.addWidget(QLabel("—"))

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
		else:  # Fallback affichant un message d'erreur explicite
			self._web = QTextBrowser(self)
			self._web.setText("<b>QtWebEngine unavailable</b><br>Install PyQtWebEngine for Plotly display.")

		main_layout.addWidget(left)
		main_layout.addWidget(self._web, stretch=1)

	##################################################
	def _connect_signals(self):
		"""Connecte les signaux UI aux callbacks."""
		self._btg_src.idClicked.connect(self._on_source_changed)
		self._cmb_src.currentTextChanged.connect(self._update_plot)
		self._chk_limits.stateChanged.connect(self._update_plot)
		self._chk_sigma.stateChanged.connect(self._update_plot)
		self._chk_gauss.stateChanged.connect(self._update_plot)
		self._chk_kde.stateChanged.connect(self._update_plot)
		self._grp_y_mode.idClicked.connect(self._update_plot)
		self._btn_actualize.clicked.connect(self._actualize)
		self._btn_export.clicked.connect(self._on_export)

	# ==================================================
	# endregion Init
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
		self._btn_loc.setEnabled(self._has_loc)
		self._btn_trk.setEnabled(self._has_trc)
		# si un bouton désactivé était sélectionné, repasse sur Stack
		if self._btn_loc.isChecked() and not self._has_loc: self._btn_stack.setChecked(True)
		if self._btn_trk.isChecked() and not self._has_trc: self._btn_stack.setChecked(True)

	##################################################
	def _on_source_changed(self, btn_id: int) -> None:
		"""
		Met à jour la liste des sources selon le domaine choisi puis redessine.

		:param btn_id: Identifiant du bouton domaine sélectionné (0=Stack, 1=Localization, 2=Tracking).
		"""
		## Exemple: remplir ta combo 'Source' en fonction du domaine
		self._cmb_src.blockSignals(True)
		self._cmb_src.clear()
		if btn_id == 0: self._cmb_src.addItems(["Intensity"])  # Stack
		elif btn_id == 1: self._cmb_src.addItems(["Localizations Count", "Integrated Intensity", "Intensity", "Sigma X", "Sigma Y",
												  "Circularity", "Theta", "MSE XY", "Z", "MSE Z"])  # Localization
		elif btn_id == 2: self._cmb_src.addItems(["MSD", "Velocity", "Displacement"])  # Tracking
		self._cmb_src.setCurrentIndex(0)
		self._cmb_src.blockSignals(False)
		# puis redessiner le graphe si besoin
		self._update_plot()

	##################################################
	def _on_hist_type_changed(self, btn_id: int) -> None:
		"""
		Met à jour la liste des sources selon le domaine choisi puis redessine.

		:param btn_id: Identifiant du bouton domaine sélectionné (0=Stack, 1=Localization, 2=Tracking).
		"""
		## Exemple: remplir ta combo 'Source' en fonction du domaine
		self._cmb_src.blockSignals(True)
		self._cmb_src.clear()
		if btn_id == 0: self._cmb_src.addItems(["Intensity"])  # Stack
		elif btn_id == 1: self._cmb_src.addItems(["Localizations Count", "Integrated Intensity", "Intensity", "Sigma X", "Sigma Y",
												  "Circularity", "Theta", "MSE XY", "Z", "MSE Z"])  # Localization
		elif btn_id == 2: self._cmb_src.addItems(["MSD", "Velocity", "Displacement"])  # Tracking
		self._cmb_src.setCurrentIndex(0)
		self._cmb_src.blockSignals(False)
		# puis redessiner le graphe si besoin
		self._update_plot()

	##################################################
	def _update_plot(self):
		"""Construit la figure Plotly courante en fonction du domaine et de la source."""
		src_id = self._btg_src.checkedId()
		src_type = self._cmb_src.currentText()
		limit = self._chk_limits.checkState() == QtCore.Qt.CheckState.Checked
		sigma = self._chk_sigma.checkState() == QtCore.Qt.CheckState.Checked
		kde = self._chk_kde.checkState() == QtCore.Qt.CheckState.Checked
		gauss = self._chk_gauss.checkState() == QtCore.Qt.CheckState.Checked
		density = self._rb_density.isChecked()
		# Selection du graphique à afficher
		fig: go.Figure
		if src_id == 0:
			# filtre de la pile self._stack (par plan et par intensité selon les filtres
			# tmp = self._stack
			if src_type == "Intensity": fig = self._grapher.histogram(self._stack, f"Stack {src_type}", limit=limit, show_sigma=sigma,
																	  kde=kde, gaussian=gauss, density=density)
			else: fig = self._grapher.blank("Invalid Selection")
		elif src_id == 1:
			# filtre du panda self._loc
			tmp = self._loc
			if src_type == "Localizations Count":
				s = tmp["Plane"].astype(np.int64, copy=False)
				if s.empty: fig = self._grapher.blank(src_type)
				else:
					planes = np.arange(int(s.min()), int(s.max()) + 1, dtype=int)  # Récupération des plans du min au max (si plans vide, ils seront compris)
					counts = (s.groupby(s).size().reindex(pd.Index(planes), fill_value=0).to_numpy(dtype=int))  # Comptage par groupe
					fig = self._grapher.scatter(np.column_stack((planes, counts)), src_type, limit=limit)
			else:
				s = tmp.get(src_type)  # None si la colonne n'existe pas
				if s is None: fig = self._grapher.blank(f"Localizations {src_type}")
				else: fig = self._grapher.histogram(s.to_numpy(dtype=float, copy=False), f"Localizations {src_type}", limit=limit, show_sigma=sigma,
													kde=kde, gaussian=gauss, density=density)
		else:
			fig = self._grapher.blank(f"Tracking {src_type} Not Yet Implemented.")

		# Mode bar (export, zoom...) : laissé par défaut; on peut alléger si besoin
		html = pio.to_html(fig, include_plotlyjs="cdn", full_html=False, config={"responsive": True, "displaylogo": False})
		self._fig = fig
		self._html = html

		if _HAS_WEBENGINE and isinstance(self._web, QWebEngineView): self._web.setHtml(html)
		else: self._web.setText("<b>QtWebEngine unavailable</b><br>Install PyQtWebEngine for Plotly display.")

	##################################################
	def _actualize(self):
		"""
		Actualise les fichiers/données depuis l’état PALMTracer :
		- Lit le TIF sélectionné (pile `_stack`) pour l’affichage Stack.
		- Déduit les chemins CSV "localizations"/"tracking" et charge les DataFrame `_loc`/`_trc`.
		- Met à jour les libellés d’information et l’état d’activation des boutons de domaine.
		- Sélectionne par défaut le domaine "Stack" et redessine.

		En cas d’erreur de lecture, logue l’erreur via :func:`print_error`.
		"""

		# Métadonnées d'information
		self._file = (cast(FileList, self._pt.settings.batch["Files"]).get_selected())
		if self._file != "":
			try: self._stack = open_tif(self._file)
			except Exception as e: print_error(f"Error loading {self._file} in GraphViewer : {e}")

		base_path, _ = os.path.splitext(self._file)
		self._csv_path = f"{base_path}_PALM_Tracer"

		self._loc_file = get_last_file(self._csv_path, "localizations")
		self._has_loc = self._loc_file.endswith("csv")
		if self._has_loc: self._loc = pd.read_csv(self._loc_file)

		self._trc_file = get_last_file(self._csv_path, "tracking")
		self._has_trc = self._trc_file.endswith("csv")
		if self._has_trc: self._trc = pd.read_csv(self._trc_file)

		self._lbl_filename.setText(os.path.basename(self._file) if self._file != "" else "No File")
		self._lbl_has_loc.setText("Yes" if self._has_loc else "No")
		self._lbl_has_trc.setText("Yes" if self._has_trc else "No")
		self._refresh_source_buttons()  # Applique has_loc/has_track
		self._on_source_changed(0)		# Change la source pour Stack

	##################################################
	def _export_png_via_qt(self, path: str, scale: float = 1.0) -> bool:
		"""
		Exporte en PNG via capture du widget QWebEngineView (fallback sans Kaleido).

		Limitations
		-----------
		- Capture la zone visible (viewport) : pour une image plus grande, redimensionner temporairement le widget avant capture.
		- Nécessite QtWebEngine pour capturer le rendu.

		:param path: Chemin de sortie du PNG.
		:param scale: Facteur d’échelle appliqué à la capture.
		:return: True si le fichier a été écrit, False sinon.
		"""
		if _HAS_WEBENGINE and isinstance(self._web, QWebEngineView):
			QApplication.processEvents()
			pix: QtGui.QPixmap = self._web.grab()
			if not pix.isNull():
				if scale != 1.0:
					size = pix.size() * scale
					pix = pix.scaled(size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
				return pix.save(path, "PNG")
		return False

	##################################################
	def _on_export(self):
		"""
		Ouvre un dialogue et exporte la figure selon l’extension choisie.

		Formats supportés
		-----------------
		- .html : enregistre l’HTML interactif (incluant PlotlyJS).
		- .png  : exporte une image du rendu (fallback par capture Qt).
		- .pdf  : imprime via QWebEngineView.printToPdf (si QtWebEngine présent).

		Comportement
		------------
		- En l’absence de figure/HTML, avertit l’utilisateur.
		- Sur échec d’écriture, affiche un message d’erreur.
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
