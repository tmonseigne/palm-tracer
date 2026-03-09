"""Module contenant la classe mère :class:`BaseStandAloneWidget`, permettant de centraliser des fonctions communes aux widgets Stand Alone."""
import json
from pathlib import Path
from typing import Any, Optional

import plotly.graph_objects as go
import plotly.io as pio
from qtpy.QtGui import QCloseEvent
from qtpy.QtWidgets import QFileDialog, QTextBrowser, QWidget

from palm_tracer.Tools import Ui
from palm_tracer.Tools.Ui import print_warning

# Tentative d'import QtWebEngine (via qtpy)
try:
	from qtpy.QtWebEngineWidgets import QWebEngineView  # type: ignore

	_HAS_WEBENGINE = True
except Exception:
	QWebEngineView = None  # type: ignore
	_HAS_WEBENGINE = False


##################################################
class BaseStandAloneWidget(QWidget):
	"""Classe mère avec les fonctions internes aux widgets Stand Alone (hors Napari)."""

	PLOT_DIV_ID = "plotly_graph"

	##################################################
	def __init__(self, parent: Optional[QWidget] = None):
		"""
		Construit le widget et initialise l'interface.

		:param parent: Widget parent Qt, ou :obj:`None` si widget racine.
		"""
		super().__init__(parent)

		self._pending_download_path: str = ""
		self._graph_folder: Path = Path.cwd() / "image"
		self._fig: Optional[go.Figure] = None
		self._html: Optional[str] = None
		self._web = self._make_web_widget()
		self._connect_web_widget()

		# On applique un style général aux QPushButton
		self.setStyleSheet(Ui.STYLESHEET_GENERAL)

	# ==================================================
	# region Web Widget (for Plotly)
	# ==================================================
	##################################################
	def _make_web_widget(self):
		"""
		Créé un Widget pour integrer plotly

		:return: QWebEngineView ou QTextBrowser si indisponible
		"""
		# Zone droite : QWebEngineView avec Plotly
		if _HAS_WEBENGINE: res = QWebEngineView(self)
		else:  # pragma: no cover — Fallback affichant un message d'erreur explicite
			res = QTextBrowser(self)
			res.setText("<b>QtWebEngine unavailable</b><br>Install PyQtWebEngine for Plotly display.")
		return res

	##################################################
	def _update_web_widget(self, fig: go.Figure, config: dict[str, Any] | None = None):
		"""
		Créé un Widget pour integrer plotly

		:return: :class:`QWebEngineView` ou :class:`QTextBrowser` si indisponible
		"""
		if config is None: config = Ui.CONFIG_PLOTLY
		html = pio.to_html(fig, include_plotlyjs="cdn", full_html=False, config=config, div_id=self.PLOT_DIV_ID)
		self._fig = fig
		self._html = html
		if _HAS_WEBENGINE and isinstance(self._web, QWebEngineView): self._web.setHtml(html)
		else:  # pragma: no cover — Fallback affichant un message d'erreur explicite
			self._web.setText("<b>QtWebEngine unavailable</b><br>Install PyQtWebEngine for Plotly display.")

	##################################################
	def _connect_web_widget(self):
		"""Connecte les signaux des boutons aux callbacks."""
		if _HAS_WEBENGINE and isinstance(self._web, QWebEngineView):  # pragma: no cover — Vérification en cas d'UI defectueuse
			profile = self._web.page().profile()
			profile.downloadRequested.connect(self._on_download_requested)

	##################################################
	def _on_download_requested(self, download):
		"""Intercepte le téléchargement Plotly (Save image) pour demander explicitement où enregistrer le fichier."""
		if not self._pending_download_path:
			path, _ = QFileDialog.getSaveFileName(self, "Export the graph", str(self._graph_folder), "Images (*.png)")
			if not path:
				download.cancel()
				return
		else:
			path = self._pending_download_path
			self._pending_download_path = ""

		path = Path(path)
		self._graph_folder = path.parent
		print(self._graph_folder)
		# Qt6 : on règle le dossier + le nom de fichier séparément.
		download.setDownloadDirectory(str(path.parent))
		download.setDownloadFileName(path.name)
		download.accept()

	# ==================================================
	# endregion Web Widget (for Plotly)
	# ==================================================

	# ==================================================
	# region Export (for Plotly)
	# ==================================================
	##################################################
	def _export_via_plotly_download(self, path: Path, fmt: str):
		"""
		Export via Plotly.downloadImage (même mécanisme que le bouton caméra).
		Requiert QtWebEngine + QWebEngineView.
		"""
		if not (_HAS_WEBENGINE and isinstance(self._web, QWebEngineView)):  # pragma: no cover — Vérification en cas d'UI defectueuse
			raise RuntimeError("QtWebEngine is required for Plotly downloadImage export.")

		# Plotly va initier un téléchargement -> on capte le prochain downloadRequested
		self._pending_download_path = str(path)

		# Paramètres cohérents avec toImageButtonOptions
		opts = {"format": fmt, "filename": path.name, "height": 1200, "width": 1200, "scale": 2}
		# NOTE: pour SVG, plotly ignore souvent scale (c'est vectoriel), width/height restent utiles.

		js = f"""
	    (function() {{
	        const gd = document.getElementById({json.dumps(self.PLOT_DIV_ID)});
	        if (!gd || typeof Plotly === "undefined") {{return "Plotly not ready";}}
	        Plotly.downloadImage(gd, {json.dumps(opts)});
	        return "ok";
	    }})();
	    """
		self._web.page().runJavaScript(js)

	##################################################
	def _on_export(self):
		"""
		Ouvre un dialogue et exporte la figure selon l'extension choisie.

		Formats supportés :
			- .html : enregistre l'HTML interactif (incluant PlotlyJS).
			- .png  : exporte une image du rendu (fallback par capture Qt).
			- .svg  : exporte une image du rendu (fallback par capture Qt).
			- .pdf  : imprime via QWebEngineView.printToPdf (si QtWebEngine présent).

		Comportement :
			- En l'absence de figure/HTML, avertit l'utilisateur.
			- Sur échec d'écriture, affiche un message d'erreur.
		"""
		if not (_HAS_WEBENGINE and isinstance(self._web, QWebEngineView)):  # pragma: no cover — Vérification en cas d'UI defectueuse
			raise RuntimeError("QtWebEngine is required for Plotly downloadImage export.")

		if self._fig is None or self._html is None:
			print_warning("No figures to export.")
			return
		path, selected_filter = QFileDialog.getSaveFileName(self, "Export the graph", str(self._graph_folder),
															"PNG (*.png);;SVG (*.svg);;WEBP (*.webp);;HTML (*.html);;PDF (*.pdf)")
		if not path: return
		try:
			lower = path.lower()
			path = Path(path)
			if lower.endswith(".png"): self._export_via_plotly_download(path, fmt="png")
			elif lower.endswith(".svg"): self._export_via_plotly_download(path, fmt="svg")
			elif lower.endswith(".webp"): self._export_via_plotly_download(path, fmt="webp")
			elif lower.endswith(".html"):
				with open(path, "w", encoding="utf-8") as f: f.write(self._html)
			elif lower.endswith(".pdf"): self._web.page().printToPdf(str(path))
			else: self._export_via_plotly_download(path, fmt="png")  # Pas d'extension reconnue ⇾ PNG par défaut
		except Exception as e: print_warning(f"Export failed : {e}")

	# ==================================================
	# endregion Export (for Plotly)
	# ==================================================

	##################################################
	def closeEvent(self, event: QCloseEvent) -> None:
		"""Assure une destruction propre de QtWebEngine (évite warnings et crash à la sortie)."""
		try:
			if _HAS_WEBENGINE and hasattr(self, "_web") and isinstance(self._web, QWebEngineView):
				page = self._web.page()
				if page is not None:
					# Arrête chargements / timers internes WebEngine.
					page.triggerAction(page.WebAction.Stop)

					self._web.setHtml("")  # Optionnel: libère le contenu HTML pour réduire l'activité pendant le teardown.

					# Déconnecte proprement le signal de download (évite callbacks tardifs).
					try: page.profile().downloadRequested.disconnect(self._on_download_requested)
					except Exception: pass

					# Destruction différée (Qt-safe).
					page.deleteLater()

				self._web.deleteLater()
		# On ne doit jamais crasher sur un closeEvent durant des tests.
		except Exception: pass
		super().closeEvent(event)
