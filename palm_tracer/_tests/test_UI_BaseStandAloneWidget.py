"""Fichier des tests pour le widget."""

import plotly.graph_objects as go
import pytest

from palm_tracer._tests.Utils import *
from palm_tracer._tests.Utils import _FakeDownload
from palm_tracer.UI.BaseStandAloneWidget import BaseStandAloneWidget  # classe


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_creation(qtbot):
	"""Test basique de création du widget."""
	w = BaseStandAloneWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)
	w.close()


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_update_plotly(qtbot):
	"""Test basique de gestion de plotly."""
	w = BaseStandAloneWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	fig = go.Figure()
	w._update_web_widget(fig)
	w._update_web_widget(fig, config={"showLinks": False})

	w.close()


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_update_plotly_no_js(qtbot):
	"""Test basique de gestion de plotly."""
	w = BaseStandAloneWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)
	w.PLOTLY_JS_PATH = Path("no_file.js")
	fig = go.Figure()
	w._update_web_widget(fig)

	w.close()

##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_download_plotly(qtbot, monkeypatch, fake_qfiledialog):
	"""Test basique de gestion de plotly."""
	w = BaseStandAloneWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	fig = go.Figure()
	w._update_web_widget(fig)

	# Simuler un "Cancel" sur le QFileDialog
	fake_qfiledialog(BaseStandAloneWidget, None)
	dl = _FakeDownload("graph.png")
	w._on_download_requested(dl)
	assert dl.canceled

	# Test d'enregistrement de l'image (avec le callback)
	target = Path(OUTPUT_DIR / "graph.png")
	fake_qfiledialog(BaseStandAloneWidget, str(target))
	dl = _FakeDownload("graph.png")
	w._on_download_requested(dl)

	w._pending_download_path = str(target)
	dl = _FakeDownload("graph.png")
	w._on_download_requested(dl)

	w.close()


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_export_plotly(qtbot, monkeypatch, fake_qfiledialog):
	"""Test basique de gestion de plotly."""
	w = BaseStandAloneWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	w._on_export()

	fig = go.Figure()
	w._update_web_widget(fig)

	# Simuler un "Cancel" sur le QFileDialog
	fake_qfiledialog(BaseStandAloneWidget, None)
	w._on_export()

	# Test d'enregistrement de l'image (avec le callback)
	target = Path(OUTPUT_DIR / "graph.png")
	fake_qfiledialog(BaseStandAloneWidget, str(target))
	w._on_export()

	target = Path(OUTPUT_DIR / "graph.svg")
	fake_qfiledialog(BaseStandAloneWidget, str(target))
	w._on_export()

	target = Path(OUTPUT_DIR / "graph.webp")
	fake_qfiledialog(BaseStandAloneWidget, str(target))
	w._on_export()

	target = Path(OUTPUT_DIR / "graph.html")
	fake_qfiledialog(BaseStandAloneWidget, str(target))
	w._on_export()

	target = Path(OUTPUT_DIR / "graph.pdf")
	fake_qfiledialog(BaseStandAloneWidget, str(target))
	w._on_export()

	target = Path(OUTPUT_DIR / "graph.txt")
	fake_qfiledialog(BaseStandAloneWidget, str(target))
	w._on_export()

	w.close()
