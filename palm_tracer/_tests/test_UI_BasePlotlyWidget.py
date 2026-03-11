"""Fichier des tests pour le widget."""

import pytest

from palm_tracer._tests.Utils import *
from palm_tracer._tests.Utils import _FakeDownload
from palm_tracer.UI.BasePlotlyWidget import BasePlotlyWidget  # classe


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_creation(qtbot):
	"""Test basique de création du widget."""
	w = BasePlotlyWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)
	w.close()


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_update_plotly(qtbot):
	"""Test basique de gestion de plotly."""
	w = BasePlotlyWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	w._update_web_widget()

	w.close()


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_update_plotly_no_js(qtbot):
	"""Test basique de gestion de plotly."""
	w = BasePlotlyWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)
	w.PLOTLY_JS_PATH = Path("no_file.js")
	w._update_web_widget()

	w.close()


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_download_plotly(qtbot, monkeypatch, fake_qfiledialog):
	"""Test basique de gestion de plotly."""
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


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_export_plotly(qtbot, monkeypatch, fake_qfiledialog):
	"""Test basique de gestion de plotly."""
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

	# Test d'enregistrement de l'image (avec le callback)
	target = Path(OUTPUT_DIR / "graph.png")
	fake_qfiledialog(BasePlotlyWidget, str(target))
	w._on_export()

	target = Path(OUTPUT_DIR / "graph.svg")
	fake_qfiledialog(BasePlotlyWidget, str(target))
	w._on_export()

	target = Path(OUTPUT_DIR / "graph.webp")
	fake_qfiledialog(BasePlotlyWidget, str(target))
	w._on_export()

	target = Path(OUTPUT_DIR / "graph.html")
	fake_qfiledialog(BasePlotlyWidget, str(target))
	w._on_export()

	target = Path(OUTPUT_DIR / "graph.pdf")
	fake_qfiledialog(BasePlotlyWidget, str(target))
	w._on_export()

	target = Path(OUTPUT_DIR / "graph.txt")
	fake_qfiledialog(BasePlotlyWidget, str(target))
	w._on_export()

	w.close()
