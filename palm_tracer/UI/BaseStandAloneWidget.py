"""Module contenant la classe mère :class:`BaseStandAloneWidget`, permettant de centraliser des fonctions communes aux widgets Stand Alone."""

from pathlib import Path
from typing import Any, Optional

import plotly.graph_objects as go
import plotly.io as pio
from qtpy.QtGui import QCloseEvent
from qtpy.QtWidgets import QFileDialog, QTextBrowser, QWidget

from palm_tracer.Tools import Ui

# Tentative d'import QtWebEngine (via qtpy)
try:
	from qtpy.QtWebEngineWidgets import QWebEngineView  # type: ignore

	_HAS_WEBENGINE = True
except Exception:
	QWebEngineView = None  # type: ignore
	_HAS_WEBENGINE = False


##################################################
class BaseStandAloneWidget(QWidget):
	"""Classe mère avec les fonctions internes aux widgets Stand Alone (Hors Napari)."""

	##################################################
	def __init__(self, parent: Optional[QWidget] = None):
		"""
		Construit le widget et initialise l'interface.

		:param parent: Widget parent Qt, ou :obj:`None` si widget racine.
		"""
		super().__init__(parent)

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
	def _update_web_widget(self, web: QWebEngineView | QTextBrowser, fig: go.Figure, config: dict[str, Any] | None = None):
		"""
		Créé un Widget pour integrer plotly

		:return: :class:`QWebEngineView` ou :class:`QTextBrowser` si indisponible
		"""
		if config is None: config = Ui.CONFIG_PLOTLY
		html = pio.to_html(fig, include_plotlyjs="cdn", full_html=False, config=config)
		self._fig = fig
		self._html = html
		if _HAS_WEBENGINE and isinstance(web, QWebEngineView): web.setHtml(html)
		else:  # pragma: no cover — Fallback affichant un message d'erreur explicite
			web.setText("<b>QtWebEngine unavailable</b><br>Install PyQtWebEngine for Plotly display.")

	##################################################
	def _connect_web_widget(self, web: QWebEngineView | QTextBrowser | None):
		"""Connecte les signaux des boutons aux callbacks."""
		if _HAS_WEBENGINE and isinstance(web, QWebEngineView):  # pragma: no cover Vérification en cas d'UI defectueuse
			profile = web.page().profile()
			profile.downloadRequested.connect(self._on_download_requested)

	##################################################
	def _on_download_requested(self, download):
		"""Intercepte le téléchargement Plotly (Save image) pour demander explicitement où enregistrer le fichier."""
		path, _ = QFileDialog.getSaveFileName(self, "Enregistrer l'image", str(self._download_initial_path()), "Images (*.png)")

		if not path:
			download.cancel()
			return

		path = Path(path)
		# Qt6 : on règle le dossier + le nom de fichier séparément.
		download.setDownloadDirectory(str(path.parent))
		download.setDownloadFileName(path.name)
		download.accept()

	##################################################
	def _download_initial_path(self) -> Path:
		"""Renvoie un chemin initial pour le téléchargement par plotly. À Définir dans les classes filles."""
		return Path.cwd() / "image"

	# ==================================================
	# endregion Web Widget (for Plotly)
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
