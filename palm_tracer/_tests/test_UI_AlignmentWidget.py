""" Fichier des tests pour le widget. """

import pytest
from qtpy.QtCore import Qt

from palm_tracer._tests.Utils import *
from palm_tracer.UI.AlignmentWidget import AlignmentWidget  # classe

INPUT_FILE = INPUT_DIR / "stack.tif"
SIZE_X, SIZE_Y, INTENSITY, RATIO = 100, 50, 1000, 10
SIZE = int(SIZE_X * np.sqrt(SIZE_Y))
POINTS = np.stack([rng.uniform(1, SIZE_Y - 1, size=SIZE), rng.uniform(1, SIZE_X - 1, size=SIZE)], axis=1)


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_widget_creation(qtbot):
	"""Test basique de création du widget."""
	w = AlignmentWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)
	w.close()


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_bad_load_tif(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""
	Test basique de création du widget.

	- Clic sur 'Compute coefficients' sans stack -> message d'erreur.
	- Simulation de différents comportements de QFileDialog / open_tif.
	- Clic sur 'Compute coefficients' avec stack chargée -> message 'not implemented'.
	"""
	w = AlignmentWidget()
	qtbot.addWidget(w)
	w.resize(500, 250)
	w.show()
	qtbot.waitExposed(w)

	# Simuler un "Cancel" sur le QFileDialog
	fake_qfiledialog(AlignmentWidget, None)
	qtbot.mouseClick(w._btn_load_tif_compute, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "No TIFF file selected." in out  # On vérifie juste que le warning attendu est bien passé par print_warning

	# Bad Tif Input
	fake_qfiledialog(AlignmentWidget, "nofile.tif")
	qtbot.mouseClick(w._btn_load_tif_compute, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "Unable to read the TIFF file" in out
	assert w._stack is None

	w.close()


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_bad_load_coef(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""
	Test basique de création du widget.

	- Clic sur 'Compute coefficients' sans stack -> message d'erreur.
	- Simulation de différents comportements de QFileDialog / open_tif.
	- Clic sur 'Compute coefficients' avec stack chargée -> message 'not implemented'.
	"""
	w = AlignmentWidget()
	qtbot.addWidget(w)
	w.resize(500, 250)
	w.show()
	qtbot.waitExposed(w)

	# Simuler un "Cancel" sur le QFileDialog
	fake_qfiledialog(AlignmentWidget, None)
	qtbot.mouseClick(w._btn_load_coef_apply, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "No coefficient file selected." in out  # On vérifie juste que le warning attendu est bien passé par print_warning

	# Bad Coef Input
	fake_qfiledialog(AlignmentWidget, "nofile.txt")
	qtbot.mouseClick(w._btn_load_coef_apply, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "Unable to read the coefficient file" in out
	assert w._coefs is None

	# Bad Coef Input
	fake_qfiledialog(AlignmentWidget, f"{INPUT_DIR}/bad_alignment_coefficient.txt")
	qtbot.mouseClick(w._btn_load_coef_apply, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "The coefficient file is not in the correct format. Expected format: two lines of ten values (2x10)." in out
	assert w._coefs is None

	w.close()


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_bad_compute(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""
	Test basique de création du widget.

	- Clic sur 'Compute coefficients' sans stack -> message d'erreur.
	- Simulation de différents comportements de QFileDialog / open_tif.
	- Clic sur 'Compute coefficients' avec stack chargée -> message 'not implemented'.
	"""
	w = AlignmentWidget()
	qtbot.addWidget(w)
	w.resize(500, 250)
	w.show()
	qtbot.waitExposed(w)

	# Compute sans Tif
	qtbot.mouseClick(w._btn_compute_coeffs, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "Can't Compute alignment coefficients without correct tif file." in out
	w.close()


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_compute(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""
	Test basique de création du widget.

	- Clic sur 'Compute coefficients' sans stack -> message d'erreur.
	- Simulation de différents comportements de QFileDialog / open_tif.
	- Clic sur 'Compute coefficients' avec stack chargée -> message 'not implemented'.
	"""
	w = AlignmentWidget()
	qtbot.addWidget(w)
	w.resize(500, 250)
	w.show()
	qtbot.waitExposed(w)

	# Chargement du fichier Tif
	fake_qfiledialog(AlignmentWidget, f"{INPUT_DIR}/stack.tif")
	qtbot.mouseClick(w._btn_load_tif_compute, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "TIFF loaded successfully." in out  # On vérifie juste que le warning attendu est bien passé par print_warning
	assert w._stack is not None

	# Lancement du calcul
	qtbot.mouseClick(w._btn_compute_coeffs, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "Compute alignment coefficients isn't implemented yet. Use original PALMTracer." in out

	w.close()


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_bad_align(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""
	Test basique de création du widget.

	- Clic sur 'Compute coefficients' sans stack -> message d'erreur.
	- Simulation de différents comportements de QFileDialog / open_tif.
	- Clic sur 'Compute coefficients' avec stack chargée -> message 'not implemented'.
	"""
	w = AlignmentWidget()
	qtbot.addWidget(w)
	w.resize(500, 250)
	w.show()
	qtbot.waitExposed(w)

	# Align sans Tif
	qtbot.mouseClick(w._btn_start_alignment, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "Can't align without correct tif file." in out

	# Chargement du fichier Tif
	fake_qfiledialog(AlignmentWidget, f"{INPUT_DIR}/stack.tif")
	qtbot.mouseClick(w._btn_load_tif_apply, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "TIFF loaded successfully." in out  # On vérifie juste que le warning attendu est bien passé par print_warning
	assert w._stack is not None

	# Align sans Coeff
	qtbot.mouseClick(w._btn_start_alignment, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "Can't align tif file without factors." in out

	w.close()


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_align(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""
	Test basique de création du widget.

	- Clic sur 'Compute coefficients' sans stack -> message d'erreur.
	- Simulation de différents comportements de QFileDialog / open_tif.
	- Clic sur 'Compute coefficients' avec stack chargée -> message 'not implemented'.
	"""
	w = AlignmentWidget()
	qtbot.addWidget(w)
	w.resize(500, 250)
	w.show()
	qtbot.waitExposed(w)

	# Chargement du fichier Tif
	fake_qfiledialog(AlignmentWidget, f"{INPUT_DIR}/stack.tif")
	qtbot.mouseClick(w._btn_load_tif_apply, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "TIFF loaded successfully." in out  # On vérifie juste que le warning attendu est bien passé par print_warning
	assert w._stack is not None

	# Chargement du fichier Coef
	fake_qfiledialog(AlignmentWidget, f"{INPUT_DIR}/alignment_coefficient.txt", "Text files (*.txt);;All files (*.*)")
	qtbot.mouseClick(w._btn_load_coef_apply, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "Coefficients loaded successfully." in out  # On vérifie juste que le warning attendu est bien passé par print_warning
	assert w._coefs is not None

	qtbot.mouseClick(w._btn_start_alignment, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert f"File saved at " in out

	w.close()
