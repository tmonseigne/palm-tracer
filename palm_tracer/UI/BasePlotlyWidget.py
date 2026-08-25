"""Définit la classe de base commune aux widgets autonomes utilisant Plotly."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import plotly.graph_objects as go
from qtpy.QtCore import QUrl
from qtpy.QtGui import QCloseEvent
from qtpy.QtWidgets import QFileDialog, QTextBrowser, QWidget

from palm_tracer.Processing import Grapher
from palm_tracer.Tools import Ui
from palm_tracer.Tools.Ui import print_warning

# Tentative d'import QtWebEngine (via qtpy) —En cas d'UI defectueuse
try:
	from qtpy.QtWebEngineWidgets import QWebEngineView  # type: ignore

	_HAS_WEBENGINE = True
except Exception:
	QWebEngineView = None  # type: ignore
	_HAS_WEBENGINE = False


##################################################
class BasePlotlyWidget(QWidget):
	"""
	Fournit les fonctions communes aux widgets Qt autonomes utilisant Plotly.

	La classe centralise l'affichage dans QtWebEngine ainsi que l'export des figures vers les formats pris en charge.

	:param parent: Widget Qt parent.
	"""

	PLOT_DIV_ID = "plotly_graph"
	"""Identifiant HTML du conteneur Plotly."""
	RESOURCE_DIR = Path(__file__).resolve().parent / "res"
	"""Répertoire des ressources de l'interface."""
	PLOTLY_JS_PATH = RESOURCE_DIR / "plotly.min.js"
	"""Chemin local de la bibliothèque JavaScript Plotly."""
	PLOTLY_JS_URL = "https://cdn.plot.ly/plotly-3.4.0.min.js"
	"""Adresse de secours de la bibliothèque JavaScript Plotly."""

	##################################################
	def __init__(self, parent: Optional[QWidget] = None):
		"""
		Construit le widget et initialise l'interface.

		:param parent: Widget parent Qt, ou :obj:`None` si widget racine.
		"""
		super().__init__(parent)

		self._pending_download_path: str = ""
		self._grapher = Grapher()
		self._graph_folder: Path = Path.cwd() / "image"
		self._fig: go.Figure = Grapher.blank()
		self._html: str = ""
		self._plotly_page_loaded = False
		self._web_page_ready = False
		self._web = self._make_web_widget()
		self._connect_web_widget()

	# ==================================================
	# region Widget Web Plotly
	# ==================================================
	##################################################
	def _make_web_widget(self):
		"""
		Créé un Widget pour integrer plotly.

		:return: QWebEngineView ou QTextBrowser si indisponible.
		"""
		# Zone droite : QWebEngineView avec Plotly
		if _HAS_WEBENGINE: res = QWebEngineView(self)
		else:  # pragma: no cover — Solution de repli affichant un message d'erreur explicite
			res = QTextBrowser(self)
			res.setText("<b>QtWebEngine unavailable</b><br>Install PyQtWebEngine for Plotly display.")
		return res

	##################################################
	def _get_plotly_js_url(self) -> QUrl:
		"""
		Construit l'URL locale vers le fichier JavaScript Plotly embarqué.

		Le fichier est recherché relativement à ce module, dans le dossier <c>res</c>.
		Une URL de type <c>file:///...</c> est renvoyée afin de pouvoir être injectée dans la page HTML du :class:`QWebEngineView`.

		:return: URL locale absolue vers <c>plotly.min.js</c>.
		:raises FileNotFoundError: Si le fichier JavaScript local est introuvable.
		"""
		if not self.PLOTLY_JS_PATH.is_file():
			raise FileNotFoundError(f"Plotly JavaScript file not found: {self.PLOTLY_JS_PATH}")
		return QUrl.fromLocalFile(str(self.PLOTLY_JS_PATH.resolve()))

	##################################################
	def _build_plotly_shell_html(self) -> str:
		"""
		Construit la page HTML minimale contenant le conteneur Plotly.

		La page est chargée une seule fois dans le :class:`QWebEngineView`,
		puis les mises à jour utilisent :c:`Plotly.newPlot` ou :c:`Plotly.react` via du JavaScript injecté.

		:return: HTML minimal servant de conteneur au graphe Plotly.
		"""
		config_json = json.dumps(Ui.CONFIG_PLOTLY)
		plot_div_id_json = json.dumps(self.PLOT_DIV_ID)
		try: url = self._get_plotly_js_url().toString()
		except FileNotFoundError: url = self.PLOTLY_JS_URL
		plotly_js_url_json = json.dumps(url)

		return f"""<!DOCTYPE html>
<html>
<head>
	<meta charset=\"utf-8\">
	<meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'self' 'unsafe-inline' 'unsafe-eval' data: blob: https:; script-src 'self'
	'unsafe-inline' 'unsafe-eval' https:; style-src 'self' 'unsafe-inline' https:; img-src 'self' data: blob: https:;\">
	<style>
		html, body {{ margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; background: transparent; }}

		#{self.PLOT_DIV_ID} {{ width: 100%; height: 100%; }}
	</style>
</head>
<body>
	<div id=\"{self.PLOT_DIV_ID}\"></div>
	<script>
		window._plotlyConfig = {config_json};
		window._plotlyReady = false;
		window._plotlyQueue = [];

		window._flushPlotlyQueue = function() {{
			if (!window._plotlyReady || typeof Plotly === "undefined") {{ return; }}
			while (window._plotlyQueue.length > 0) {{
				const callback = window._plotlyQueue.shift();
				try {{ callback(); }} catch (error) {{ console.error("Plotly callback failed", error); }}
			}}
		}};

		window._runWhenPlotlyReady = function(callback) {{
			if (window._plotlyReady && typeof Plotly !== "undefined") {{ callback(); return; }}
			window._plotlyQueue.push(callback);
		}};

		(function() {{
			const script = document.createElement("script");
			script.src = {plotly_js_url_json};
			script.onload = function() {{ window._plotlyReady = true; window._flushPlotlyQueue(); }};
			script.onerror = function() {{ console.error("Unable to load local Plotly JavaScript file."); }};
			document.head.appendChild(script);
		}})();

		window._renderPlotlyFigure = function(data, layout, config) {{
			window._runWhenPlotlyReady(function() {{
				const gd = document.getElementById({plot_div_id_json});
				if (!gd) {{ return; }}
				if (!gd.data) {{ Plotly.newPlot(gd, data, layout, config); return; }}
				Plotly.react(gd, data, layout, config);
			}});
		}};
	</script>
</body>
</html>
"""

	##################################################
	def _load_plotly_page_once(self):
		"""
		Charge la page HTML minimale contenant Plotly une seule fois.

		Le graphe lui-même n'est pas injecté ici. Il est créé ensuite via :c:`Plotly.newPlot`, puis mis à jour via :c:`Plotly.react`.
		"""
		if not (_HAS_WEBENGINE and isinstance(self._web, QWebEngineView)):
			self._web.setText("<b>QtWebEngine unavailable</b><br>Install PyQtWebEngine for Plotly display.")
			return

		if self._plotly_page_loaded: return

		try: html = self._build_plotly_shell_html()
		except FileNotFoundError as error:
			print_warning(str(error))
			self._web.setText(f"<b>Plotly unavailable</b><br>{error}")
			return

		self._web.setHtml(html, QUrl.fromLocalFile(str(Path(__file__).resolve().parent)))
		self._plotly_page_loaded = True

	##################################################
	def _update_web_widget(self):
		"""
		Met à jour le widget Web affichant la figure Plotly.

		La page HTML contenant le conteneur Plotly n'est chargée qu'une seule fois.
		Les mises à jour successives de la figure évitent ainsi de reconstruire toute la page et utilisent :c:`Plotly.react`,
		ce qui réduit fortement le coût des rafraîchissements fréquents.
		"""
		try: plotly_js_url = self._get_plotly_js_url().toString()
		except FileNotFoundError: plotly_js_url = self.PLOTLY_JS_URL

		self._html = self._fig.to_html(include_plotlyjs=plotly_js_url, full_html=True, config=Ui.CONFIG_PLOTLY, div_id=self.PLOT_DIV_ID)

		if not (_HAS_WEBENGINE and isinstance(self._web, QWebEngineView)):
			self._web.setText("<b>QtWebEngine unavailable</b><br>Install PyQtWebEngine for Plotly display.")
			return

		self._load_plotly_page_once()

		figure_dict = self._fig.to_plotly_json()
		data_json = json.dumps(figure_dict.get("data", []))
		layout_json = json.dumps(figure_dict.get("layout", {}))
		config_json = json.dumps(Ui.CONFIG_PLOTLY)

		js = f"""
		(function() {{
			const data = {data_json};
			const layout = {layout_json};
			const config = {config_json};

			if (typeof window._renderPlotlyFigure !== "function") {{ return "Plotly renderer not ready"; }}

			window._renderPlotlyFigure(data, layout, config);
			return "queued";
		}})();
		"""
		self._web.page().runJavaScript(js)

	##################################################
	def _connect_web_widget(self):
		"""Connecte les signaux aux callbacks."""
		if _HAS_WEBENGINE and isinstance(self._web, QWebEngineView):
			profile = self._web.page().profile()
			profile.downloadRequested.connect(self._on_download_requested)
			self._web.loadFinished.connect(self._update_web_widget)

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
	# endregion Widget Web Plotly
	# ==================================================

	# ==================================================
	# region Export Plotly
	# ==================================================
	##################################################
	def _export_via_plotly_download(self, path: Path, fmt: str):
		"""Export via Plotly.downloadImage (même mécanisme que le bouton caméra). Requiert QtWebEngine + QWebEngineView."""
		if not (_HAS_WEBENGINE and isinstance(self._web, QWebEngineView)): raise RuntimeError("QtWebEngine is required for Plotly downloadImage export.")

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
			- .html : enregistre l'HTML interactif.
			- .png  : exporte une image du rendu Plotly.
			- .svg  : exporte une image vectorielle du rendu Plotly.
			- .webp : exporte une image WebP du rendu Plotly.
			- .pdf  : imprime via QWebEngineView.printToPdf.

		Comportement :
			- En l'absence de figure/HTML, avertit l'utilisateur.
			- Sur échec d'écriture, affiche un message d'erreur.
		"""
		if not (_HAS_WEBENGINE and isinstance(self._web, QWebEngineView)): raise RuntimeError("QtWebEngine is required for Plotly downloadImage export.")

		if not self._html:
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
	# endregion Export Plotly
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


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication

	app = QApplication(sys.argv)
	w = BasePlotlyWidget()
	w.resize(1280, 720)
	w.show()
	sys.exit(app.exec_())
