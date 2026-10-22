"""Teste la classe de base des widgets autonomes utilisant Plotly."""

from importlib import import_module
from unittest.mock import Mock

import pytest
from qtpy.QtCore import QUrl
from qtpy.QtGui import QCloseEvent
from qtpy.QtWidgets import QTextBrowser, QWidget

from palm_tracer.UI.BasePlotlyWidget import BasePlotlyWidget  # Classe
from tests.Utils import *
from tests.Utils import _FakeDownload, strip_ansi


# --------------------------------------------------
class _FakeWebEngineView(QWidget):
	"""Simule uniquement l'API WebEngine utilisée par le widget, sans moteur Chromium ni méthode ``setText``."""

	def __init__(self, parent=None):
		"""Initialise la page, le signal de chargement et l'affichage HTML simulés."""
		super().__init__(parent)
		self._page = Mock()
		self.loadFinished = Mock()
		self.html = ""

	def page(self):
		"""Renvoie la page simulée pour observer les appels JavaScript et les téléchargements."""
		return self._page

	def setHtml(self, html, base_url=None):
		"""Mémorise le contenu HTML sans charger de ressource externe."""
		self.html = html


# --------------------------------------------------
@pytest.fixture
def plotly_widget(qtbot, monkeypatch):
	"""Crée un widget Plotly avec une vue Web simulée et une URL JavaScript locale contrôlée."""
	module = import_module(BasePlotlyWidget.__module__)
	monkeypatch.setattr(module, "QWebEngineView", _FakeWebEngineView)
	monkeypatch.setattr(module, "_HAS_WEBENGINE", True)
	w = BasePlotlyWidget()
	qtbot.addWidget(w)
	monkeypatch.setattr(w, "_get_plotly_js_url", lambda: QUrl("file:///plotly.js"))
	return w


# ==================================================
# region Initialisation
# ==================================================
def test_creation(qtbot):
	"""Vérifie la création du widget."""
	w = BasePlotlyWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)
	w.close()


# --------------------------------------------------
def test_webengine_import_fallback(import_without_dependency, qtbot):
	"""Crée un affichage textuel lorsque QtWebEngine ne peut pas être importé."""
	module = import_without_dependency(BasePlotlyWidget.__module__, "qtpy.QtWebEngineWidgets")
	assert not module._HAS_WEBENGINE
	assert module.QWebEngineView is None
	w = module.BasePlotlyWidget()
	qtbot.addWidget(w)
	assert isinstance(w._web, QTextBrowser)
	assert "QtWebEngine unavailable" in w._web.toPlainText()


# ==================================================
# endregion Initialisation
# ==================================================

# ==================================================
# region Widget Web Plotly
# ==================================================

# ==================================================
# region Chargement de la page
# ==================================================
@pytest.mark.parametrize("backend", ["disabled", "wrong-view"], ids=["webengine-disabled", "text-view"])
@pytest.mark.parametrize("method", [
		pytest.param("_load_plotly_page_once", id="load-page"),
		pytest.param("_update_web_widget", id="update-figure"),
		pytest.param("_connect_web_widget", id="connect-signals")])
def test_web_widget_without_engine(plotly_widget, monkeypatch, backend, method):
	"""Affiche un avertissement ou ignore la connexion des signaux lorsqu'aucune vue WebEngine n'est utilisable."""
	w = plotly_widget
	page = w._web.page()
	page.reset_mock()
	# Le repli réel utilise un QTextBrowser ; couvre aussi un type de vue incompatible malgré le drapeau actif.
	w._web = QTextBrowser(w)
	monkeypatch.setattr(import_module(BasePlotlyWidget.__module__), "_HAS_WEBENGINE", backend != "disabled")
	getattr(w, method)()
	page.profile.assert_not_called()
	page.runJavaScript.assert_not_called()
	if method == "_connect_web_widget": assert w._web.toPlainText() == ""
	else: assert "QtWebEngine unavailable" in w._web.toPlainText()
	assert not w._plotly_page_loaded


# --------------------------------------------------
def test_load_plotly_page_missing_script(plotly_widget, monkeypatch, capsys):
	"""Affiche l'erreur dans la vue WebEngine si le fichier JavaScript local manque, sans appeler ``setText``."""
	w = plotly_widget
	monkeypatch.setattr(w, "_build_plotly_shell_html", Mock(side_effect=FileNotFoundError("Missing Plotly JavaScript")))
	# Le substitut respecte l'API WebEngine et ne dispose volontairement pas de setText().
	assert not hasattr(w._web, "setText")
	w._load_plotly_page_once()
	assert "Plotly unavailable" in w._web.html
	assert "Missing Plotly JavaScript" in w._web.html
	assert "Missing Plotly JavaScript" in strip_ansi(capsys.readouterr().out)
	assert not w._plotly_page_loaded
	w._web.page().runJavaScript.assert_not_called()


# ==================================================
# endregion Chargement de la page
# ==================================================

# ==================================================
# region Affichage et téléchargements
# ==================================================
@pytest.mark.parametrize("missing_script", [False, True], ids=["local-script", "missing-script"])
def test_update_plotly(qtbot, missing_script):
	"""Vérifie gestion de plotly."""
	w = BasePlotlyWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	if missing_script: w.PLOTLY_JS_PATH = Path("no_file.js")
	w._update_web_widget()

	w.close()


# --------------------------------------------------
def test_download_plotly(qtbot, monkeypatch, fake_qfiledialog):
	"""Vérifie gestion de plotly."""
	w = BasePlotlyWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	w._update_web_widget()

	# Simuler un "Cancel" sur le QFileDialog
	fake_qfiledialog(BasePlotlyWidget, None)
	dl = _FakeDownload("graph.png")
	w._on_download_requested(dl)
	assert dl.canceled

	# Test d'enregistrement de l'image (avec le callback)
	target = Path(OUTPUT_DIR / "graph.png")
	fake_qfiledialog(BasePlotlyWidget, str(target))
	dl = _FakeDownload("graph.png")
	w._on_download_requested(dl)

	w._pending_download_path = str(target)
	dl = _FakeDownload("graph.png")
	w._on_download_requested(dl)

	w.close()


# ==================================================
# endregion Affichage et téléchargements
# ==================================================


# ==================================================
# endregion Widget Web Plotly
# ==================================================

# ==================================================
# region Export Plotly
# ==================================================
@pytest.mark.parametrize("backend", ["disabled", "wrong-view"], ids=["webengine-disabled", "text-view"])
@pytest.mark.parametrize("method", ["_export_via_plotly_download", "_on_export"], ids=["download-image", "export-button"])
def test_export_without_engine(plotly_widget, tmp_path, monkeypatch, backend, method):
	"""Refuse explicitement l'export d'une figure lorsque la vue WebEngine n'est pas disponible."""
	w = plotly_widget
	w._web = QTextBrowser(w)
	monkeypatch.setattr(import_module(BasePlotlyWidget.__module__), "_HAS_WEBENGINE", backend != "disabled")
	args = (tmp_path / "graph.png", "png") if method == "_export_via_plotly_download" else ()
	with pytest.raises(RuntimeError, match="QtWebEngine is required"): getattr(w, method)(*args)
	assert w._pending_download_path == ""
	assert not (tmp_path / "graph.png").exists()


# --------------------------------------------------
@pytest.mark.parametrize("extension", [
		pytest.param("png", id="png"), pytest.param("svg", id="svg"), pytest.param("webp", id="webp"),
		pytest.param("html", id="html"), pytest.param("pdf", id="pdf"), pytest.param("txt", id="fallback-png")])
def test_export_plotly(qtbot, monkeypatch, fake_qfiledialog, extension):
	"""Vérifie gestion de plotly."""
	w = BasePlotlyWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	w._on_export()

	w._update_web_widget()

	# Simuler un "Cancel" sur le QFileDialog
	fake_qfiledialog(BasePlotlyWidget, None)
	w._on_export()

	# Export du format sélectionné après l'annulation d'un premier dialogue.
	target = OUTPUT_DIR / f"graph.{extension}"
	fake_qfiledialog(BasePlotlyWidget, str(target))
	w._on_export()
	w.close()


# --------------------------------------------------
def test_export_write_error(plotly_widget, tmp_path, fake_qfiledialog, capsys):
	"""Signale un échec d'écriture HTML sans propager l'erreur au callback d'export."""
	w = plotly_widget
	w._html = "<html>Graph</html>"
	# Un dossier portant l'extension HTML provoque une erreur d'ouverture portable, même avec des droits élevés.
	path = tmp_path / "graph.html"
	path.mkdir()
	fake_qfiledialog(BasePlotlyWidget, str(path))
	w._on_export()
	assert "Export failed :" in strip_ansi(capsys.readouterr().out)
	assert path.is_dir()
	w._web.page().printToPdf.assert_not_called()
	w._web.page().runJavaScript.assert_not_called()


# ==================================================
# endregion Export Plotly
# ==================================================

# ==================================================
# region Fermeture
# ==================================================
@pytest.mark.parametrize("has_page", [False, True], ids=["missing-page", "existing-page"])
def test_close_web_widget(plotly_widget, monkeypatch, has_page):
	"""Détruit la vue même sans page et arrête proprement une page encore présente."""
	w = plotly_widget
	web = w._web
	page = web.page()
	page.reset_mock()
	if not has_page: web._page = None
	delete_view = Mock()
	monkeypatch.setattr(web, "deleteLater", delete_view)
	# Appel explicite du callback pour observer la fermeture sans attendre la destruction différée Qt.
	event = QCloseEvent()
	w.closeEvent(event)
	delete_view.assert_called_once_with()
	assert event.isAccepted()
	if has_page:
		page.triggerAction.assert_called_once_with(page.WebAction.Stop)
		page.profile().downloadRequested.disconnect.assert_called_once_with(w._on_download_requested)
		page.deleteLater.assert_called_once_with()
		assert web.html == ""
	else:
		page.triggerAction.assert_not_called()
		page.deleteLater.assert_not_called()

# ==================================================
# endregion Fermeture
# ==================================================
