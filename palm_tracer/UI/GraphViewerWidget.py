"""
GraphViewerWidget (version minimale) — Plotly + PyQt (QtWebEngine)

Objectif de l'étape 1
---------------------
- Interface en deux parties :
  • Colonne gauche : bloc infos (fichier, has_loc, has_track),
    un bloc "Source" (combo) et un bloc "Type de graphe" (combo),
    puis un bloc "Filtres" (vide pour l'instant).
  • Zone droite : affichage du graphe Plotly (interactif, hover tooltips, zoom, pan,
    export via mode bar Plotly).
- Données minimales : self.datas = {"type": "Intensity", "x": array gaussienne}.
- Survol souris : mise en valeur des points/colonnes (géré nativement par Plotly).

Remarques
---------
- Ce widget utilise QtWebEngine pour intégrer Plotly dans Qt via un QWebEngineView.
  Assurez-vous d'avoir installé le module correspondant (PySide6-Addons).
- Si QtWebEngine est indisponible, un message explicite est affiché côté droit.
"""
import os
from typing import cast, Optional

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from qtpy import QtCore, QtGui
from qtpy.QtWidgets import (QApplication, QButtonGroup, QComboBox, QFileDialog, QFormLayout, QFrame, QGroupBox, QHBoxLayout,
							QLabel, QMessageBox, QPushButton, QTextBrowser, QVBoxLayout, QWidget)

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
	"""Widget de visualisation interactive avec Plotly.

	Comportement actuel (Étape 1)
	-----------------------------
	- Données internes `self.datas` :
		{"type": "Intensity", "x": ndarray}
	- Infos affichées : `self.filename`, `self.has_loc`, `self.has_track`.
	- Deux ComboBox :
		• Source (actuellement: "Intensity")
		• Type de graphe ("Histogramme" ou "Courbe")
	- Bloc "Filtres" réservé, sans contenu pour l'instant.
	- Graphe interactif Plotly à droite (hover/zoom/pan/export natifs).
	"""

	# ==================================================
	# region Init
	# ==================================================
	##################################################
	def __init__(self, palmtracer: PALMTracer):
		"""
		Initialise l'interface et les données minimales.
		:param palmtracer:
		"""
		super().__init__()
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
		"""Construit l'interface : panneau gauche (infos/choix) + graphe Plotly."""
		main_layout = QHBoxLayout(self)
		main_layout.setContentsMargins(8, 8, 8, 8)
		main_layout.setSpacing(10)

		# Colonne gauche
		left = QFrame(self)
		left.setFrameShape(QFrame.StyledPanel)
		left.setMinimumWidth(280)
		vbox = QVBoxLayout(left)
		vbox.setContentsMargins(8, 8, 8, 8)
		vbox.setSpacing(8)

		# Bloc Infos (lecture seule)
		grp_infos = QGroupBox("Informations")
		form = QFormLayout(grp_infos)
		self._lbl_filename = QLabel(self._file if self._file != "" else "No File")
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

		# COMBO BOX
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

	def _connect_signals(self):
		"""Connecte les signaux UI aux callbacks."""
		self._btg_src.idClicked.connect(self._on_source_changed)
		self._cmb_src.currentTextChanged.connect(self._update_plot)
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
		"""Active/désactive les boutons selon disponibilité des données."""
		self._btn_loc.setEnabled(self._has_loc)
		self._btn_trk.setEnabled(self._has_trc)
		# si un bouton désactivé était sélectionné, repasse sur Stack
		if self._btn_loc.isChecked() and not self._has_loc: self._btn_stack.setChecked(True)
		if self._btn_trk.isChecked() and not self._has_trc: self._btn_stack.setChecked(True)

	def _on_source_changed(self, btn_id: int) -> None:
		"""Callback quand l'utilisateur choisit Stack/Localization/Tracking."""
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
		"""Construit la figure Plotly selon la source et le type choisis."""
		src_id = self._btg_src.checkedId()
		src_type = self._cmb_src.currentText()

		# Selection du graphique à afficher
		fig: go.Figure
		if src_id == 0:
			# filtre de la pile self._stack (par plan et par intensité selon les filtres
			# tmp = self._stack
			if src_type == "Intensity": fig = self._grapher.histogram(self._stack, f"Stack {src_type}", limit=False, kde=True, density=True)
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
					fig = self._grapher.scatter(np.column_stack((planes, counts)), src_type, limit=False)
			else :
				s = tmp.get(src_type)  # None si la colonne n'existe pas
				if s is None: fig = self._grapher.blank(f"Localizations {src_type}")
				else: fig = self._grapher.histogram(s.to_numpy(dtype=float, copy=False), f"Localizations {src_type}", limit=False, kde=True, density=True)
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
		self._on_source_changed(0)  # Change la source pour Stack

	##################################################
	def _export_png_via_qt(self, path: str, scale: float = 1.0) -> bool:
		"""Exporte en PNG en *capturant* la vue Qt (fallback sans Kaleido).

		Limitation: capture la zone visible (viewport). Pour une image plus
		grande, redimensionnez temporairement le widget avant capture.
		:param path:
		:param scale:
		:return:
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
		"""Ouvre une boîte de dialogue et exporte la figure (HTML/PNG/PDF).

		Stratégie:
		- HTML: sauvegarde l'HTML interactif.
		- PNG: tente Plotly+Kaleido; en cas d'échec, fallback capture Qt.
		- PDF: via QWebEngineView.printToPdf.
		"""
		if self._fig is None and self._html is None:
			QMessageBox.warning(self, "Export", "No figures to export.")
			return
		suggested = (self._file or "graph").rsplit("/", 1)[-1]
		path, selected_filter = QFileDialog.getSaveFileName(self, "Export the graph", suggested, "HTML (*.html);;PNG (*.png);;PDF (*.pdf)")
		if not path: return
		try:
			if path.lower().endswith(".png"):
				ok = False
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
