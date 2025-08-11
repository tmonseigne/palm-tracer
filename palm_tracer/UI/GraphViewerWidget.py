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

import numpy as np
from qtpy import QtCore, QtGui, QtWidgets

from palm_tracer.Processing import Grapher

# Tentative d'import QtWebEngine (via qtpy)
try:  # pragma: no cover - dépend de l'environnement
	from qtpy.QtWebEngineWidgets import QWebEngineView  # type: ignore

	_HAS_WEBENGINE = True
except Exception:  # pragma: no cover
	QWebEngineView = None  # type: ignore
	_HAS_WEBENGINE = False

import plotly.graph_objects as go
import plotly.io as pio
from typing import Optional


class GraphViewerWidget(QtWidgets.QWidget):
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
	def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
		"""Initialise l'interface et les données minimales.

		Paramètres
		----------
		parent : QWidget | None
			Parent Qt (optionnel).
		"""
		super().__init__(parent)
		self._fig: Optional[go.Figure] = None
		self._html: Optional[str] = None
		self.grapher = Grapher()

		# Données minimales
		rng = np.random.default_rng(42)
		x = rng.normal(loc=0.0, scale=1.0, size=5_000).astype(np.float32)
		self.datas: dict[str, object] = {"type": "Intensity", "x": x, }

		# Métadonnées d'information
		self.filename: str = "blabla"
		self.has_track: bool = False
		self.has_loc: bool = False

		# Construction UI
		self._init_ui()
		self._connect_signals()

		# Tracé initial
		self._update_plot()

	# ==================================================
	# endregion Init
	# ==================================================

	# ---------------------------
	# UI
	# ---------------------------
	def _init_ui(self) -> None:
		"""Construit l'interface : panneau gauche (infos/choix) + graphe Plotly."""
		main_layout = QtWidgets.QHBoxLayout(self)
		main_layout.setContentsMargins(8, 8, 8, 8)
		main_layout.setSpacing(10)

		# Colonne gauche
		left = QtWidgets.QFrame(self)
		left.setFrameShape(QtWidgets.QFrame.StyledPanel)
		left.setMinimumWidth(280)
		vbox = QtWidgets.QVBoxLayout(left)
		vbox.setContentsMargins(8, 8, 8, 8)
		vbox.setSpacing(8)

		# Bloc Infos (lecture seule)
		grp_infos = QtWidgets.QGroupBox("Informations")
		form = QtWidgets.QFormLayout(grp_infos)
		self.lbl_filename = QtWidgets.QLabel(self.filename)
		self.lbl_has_loc = QtWidgets.QLabel("Yes" if self.has_loc else "No")
		self.lbl_has_track = QtWidgets.QLabel("Yes" if self.has_track else "No")
		form.addRow("File :", self.lbl_filename)
		form.addRow("Localization :", self.lbl_has_loc)
		form.addRow("Tracking :", self.lbl_has_track)

		# Bloc Source (donnée) + Type de graphe
		grp_source = QtWidgets.QGroupBox("Datas")
		form2 = QtWidgets.QFormLayout(grp_source)
		self.cmb_source = QtWidgets.QComboBox()
		self.cmb_source.addItems(["Intensity"])  # extensible
		self.cmb_graphtype = QtWidgets.QComboBox()
		self.cmb_graphtype.addItems(["Histogram", "Curve"])  # défaut: histo
		form2.addRow("Source :", self.cmb_source)
		form2.addRow("Type :", self.cmb_graphtype)

		# Bloc Filtres (placeholder vide pour l'instant)
		grp_filters = QtWidgets.QGroupBox("Filters (comming soon)")
		vbox_filters = QtWidgets.QVBoxLayout(grp_filters)
		vbox_filters.addWidget(QtWidgets.QLabel("—"))

		# Actions
		actions_row = QtWidgets.QHBoxLayout()
		self.btn_export = QtWidgets.QPushButton("Export…")
		actions_row.addStretch(1)
		actions_row.addWidget(self.btn_export)

		vbox.addWidget(grp_infos)
		vbox.addWidget(grp_source)
		vbox.addWidget(grp_filters)
		vbox.addLayout(actions_row)
		vbox.addStretch(1)

		# Zone droite : QWebEngineView avec Plotly
		if _HAS_WEBENGINE: self.web = QWebEngineView(self)
		else:  # Fallback affichant un message d'erreur explicite
			self.web = QtWidgets.QTextBrowser(self)
			self.web.setText("<b>QtWebEngine indisponible</b><br>Installez PyQtWebEngine pour l'affichage Plotly.")

		main_layout.addWidget(left)
		main_layout.addWidget(self.web, stretch=1)

	def _connect_signals(self) -> None:
		"""Connecte les signaux UI aux callbacks."""
		self.cmb_source.currentTextChanged.connect(self._on_change)
		self.cmb_graphtype.currentTextChanged.connect(self._on_change)
		self.btn_export.clicked.connect(self._on_export)

	# ---------------------------
	# Callbacks
	# ---------------------------
	def _on_change(self) -> None:
		"""Relance le tracé quand il y a un changement."""
		self._update_plot()

	# ---------------------------
	# Plot
	# ---------------------------
	def _update_plot(self) -> None:
		"""Construit la figure Plotly selon la source et le type choisis."""
		source = self.cmb_source.currentText()
		gtype = self.cmb_graphtype.currentText()

		x = np.asarray(self.datas.get("x", np.array([], dtype=np.float32)))
		fig: go.Figure

		if gtype == "Histogram":  # Histogramme interactif
			fig = self.grapher.histogram(x, f"{source} — {gtype}", limit=True, kde=True, density=False)
		else:  # "Courbe"
			# Courbe basée sur un histogramme (densité approx.)
			counts, edges = np.histogram(x, bins=80)
			fig = self.grapher.scatter(counts, f"{source} — {gtype}", limit=True)

		# Mode bar (export, zoom...) : laissé par défaut; on peut alléger si besoin
		html = pio.to_html(fig, include_plotlyjs="cdn", full_html=False,
						   config={"responsive": True, "displaylogo": False})
		self._fig = fig
		self._html = html

		if _HAS_WEBENGINE and isinstance(self.web, QWebEngineView): self.web.setHtml(html)
		else: self.web.setText("<b>QtWebEngine indisponible</b><br>Installez PyQtWebEngine pour l'affichage Plotly.")

	# ---------------------------
	# Export helpers & slots
	# ---------------------------
	def _export_png_via_qt(self, path: str, scale: float = 1.0) -> bool:
		"""Exporte en PNG en *capturant* la vue Qt (fallback sans Kaleido).

		Limitation: capture la zone visible (viewport). Pour une image plus
		grande, redimensionnez temporairement le widget avant capture.
		"""
		if _HAS_WEBENGINE and isinstance(self.web, QWebEngineView):
			QtWidgets.QApplication.processEvents()
			pix: QtGui.QPixmap = self.web.grab()
			if not pix.isNull():
				if scale != 1.0:
					size = pix.size() * scale
					pix = pix.scaled(size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
				return pix.save(path, "PNG")
		return False

	def _on_export(self) -> None:
		"""Ouvre une boîte de dialogue et exporte la figure (HTML/PNG/PDF).

		Stratégie:
		- HTML: sauvegarde l'HTML interactif.
		- PNG: tente Plotly+Kaleido; en cas d'échec, fallback capture Qt.
		- PDF: via QWebEngineView.printToPdf.
		"""
		if self._fig is None and self._html is None:
			QtWidgets.QMessageBox.warning(self, "Export", "Aucune figure à exporter.")
			return
		suggested = (self.filename or "graph").rsplit("/", 1)[-1]
		path, selected_filter = QtWidgets.QFileDialog.getSaveFileName(self, "Export the graph", suggested, "HTML (*.html);;PNG (*.png);;PDF (*.pdf)")
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
				if not ok: raise RuntimeError("Échec export PNG (Kaleido & fallback Qt)")

			elif path.lower().endswith(".html"):
				assert self._html is not None
				with open(path, "w", encoding="utf-8") as f: f.write(self._html)

			elif path.lower().endswith(".pdf"):
				if _HAS_WEBENGINE and isinstance(self.web, QWebEngineView):
					try: self.web.page().printToPdf(path)
					except Exception as e:
						QtWidgets.QMessageBox.warning(self, "Export PDF", f"Échec impression PDF: {e}")
						return
				else:
					QtWidgets.QMessageBox.warning(self, "Export PDF", "QtWebEngine est requis pour l'export PDF.")
					return
			else:
				# Pas d'extension reconnue -> HTML par défaut
				with open(path + ".html", "w", encoding="utf-8") as f: f.write(self._html or "")
				path = path + ".html"
			QtWidgets.QMessageBox.information(self, "Export", f"Export réussi :{path}")
		except Exception as e: QtWidgets.QMessageBox.critical(self, "Export", f"Échec de l'export : {e}")


if __name__ == "__main__":  # pragma: no cover
	import sys

	app = QtWidgets.QApplication(sys.argv)
	w = GraphViewerWidget()
	w.resize(1000, 600)
	w.show()
	sys.exit(app.exec_())
