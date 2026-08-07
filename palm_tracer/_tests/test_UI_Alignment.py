"""Fichier des tests pour le widget."""

from qtpy.QtCore import Qt

from palm_tracer._tests.Utils import *
from palm_tracer.UI.AlignmentWidget import AlignmentWidget  # classe

SIZE_X, SIZE_Y, INTENSITY, RATIO = 100, 50, 1000, 10
SIZE = int(SIZE_X * np.sqrt(SIZE_Y))
POINTS = np.stack([rng.uniform(1, SIZE_Y - 1, size=SIZE), rng.uniform(1, SIZE_X - 1, size=SIZE)], axis=1)


##################################################
def test_widget_creation(qtbot):
	"""Test basique de création du widget."""
	w = AlignmentWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)
	w.close()


##################################################
def test_bad_load_tif(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Test basique d'erreurs avec la boîte de dialogue d'ouverture de fichier."""
	w = AlignmentWidget()
	qtbot.addWidget(w)
	w.resize(500, 250)
	w.show()
	qtbot.waitExposed(w)

	# Simuler un "Cancel" sur le QFileDialog
	fake_qfiledialog(AlignmentWidget, None)
	qtbot.mouseClick(w._btn_load_tif_compute, Qt.MouseButton.LeftButton)

	# Bad Tif Input
	fake_qfiledialog(AlignmentWidget, "nofile.tif")
	qtbot.mouseClick(w._btn_load_tif_compute, Qt.MouseButton.LeftButton)

	lines = get_lines_output(capsys)
	assert "No TIFF file selected." in lines[0]  # On vérifie juste que le warning attendu est bien passé par print_warning la première fois
	assert "Selected file: nofile.tif." in lines[1]  # il a vu le fichier la seconde fois
	assert "Unable to read the TIFF file" in lines[2]  # Mais erreur
	assert w._stack is None

	w.close()


##################################################
def test_bad_load_coef(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Test basique d'erreurs avec la boîte de dialogue d'ouverture de fichier."""
	w = AlignmentWidget()
	qtbot.addWidget(w)
	w.resize(500, 250)
	w.show()
	qtbot.waitExposed(w)

	# Simuler un "Cancel" sur le QFileDialog
	fake_qfiledialog(AlignmentWidget, None)
	qtbot.mouseClick(w._btn_load_coef_apply, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "No coefficient file selected." in lines[0]  # On vérifie juste que le warning attendu est bien passé par print_warning

	# Bad Coef Input
	fake_qfiledialog(AlignmentWidget, "nofile.txt")
	qtbot.mouseClick(w._btn_load_coef_apply, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Selected file: nofile.txt." in lines[0]
	assert "Unable to read the coefficient file" in lines[1]
	assert w._coefs is None

	# Bad Coef Input
	fake_qfiledialog(AlignmentWidget, f"{INPUT_DIR}/bad_alignment_coeffs.txt")
	qtbot.mouseClick(w._btn_load_coef_apply, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert f"Selected file: {INPUT_DIR}/bad_alignment_coeffs.txt." in lines[0]
	assert "The coefficient file is not in the correct format. Expected format: two lines of ten values (2x10)." in lines[1]
	assert w._coefs is None

	w.close()


##################################################
def test_bad_compute(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""
	Test basique de création du widget.

	- Clic sur 'Compute coefficients' sans stack ⇾ message d'erreur.
	- Simulation de différents comportements de QFileDialog / open_tif.
	- Clic sur 'Compute coefficients' avec stack chargée ⇾ message 'not implemented'.
	"""
	w = AlignmentWidget()
	qtbot.addWidget(w)
	w.resize(500, 250)
	w.show()
	qtbot.waitExposed(w)

	# Compute sans Tif
	qtbot.mouseClick(w._btn_compute_coeffs, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Can't Compute alignment coefficients without correct tif file." in lines[0]
	w.close()


##################################################
def test_compute(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""
	Test basique de création du widget.

	- Clic sur 'Compute coefficients' sans stack ⇾ message d'erreur.
	- Simulation de différents comportements de QFileDialog / open_tif.
	- Clic sur 'Compute coefficients' avec stack chargée ⇾ message 'not implemented'.
	"""
	w = AlignmentWidget()
	qtbot.addWidget(w)
	w.resize(500, 250)
	w.show()
	qtbot.waitExposed(w)

	# Chargement du fichier Tif
	fake_qfiledialog(AlignmentWidget, f"{INPUT_DIR}/stack.tif")
	qtbot.mouseClick(w._btn_load_tif_compute, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert f"Selected file: {INPUT_DIR}/stack.tif" in lines[0]
	assert "TIFF loaded successfully. Shape=(10, 128, 256), dtype=uint16" in lines[1]
	assert w._stack is not None

	# Lancement du calcul
	qtbot.mouseClick(w._btn_compute_coeffs, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Compute alignment coefficients isn't implemented yet. Use original PALMTracer." in lines[0]

	w.close()


##################################################
def test_bad_align(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""
	Test basique de création du widget.

	- Clic sur 'Compute coefficients' sans stack ⇾ message d'erreur.
	- Simulation de différents comportements de QFileDialog / open_tif.
	- Clic sur 'Compute coefficients' avec stack chargée ⇾ message 'not implemented'.
	"""
	w = AlignmentWidget()
	qtbot.addWidget(w)
	w.resize(500, 250)
	w.show()
	qtbot.waitExposed(w)

	# Align sans Tif
	qtbot.mouseClick(w._btn_start_alignment, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Can't align without correct tif file." in lines[0]

	# Chargement du fichier Tif
	fake_qfiledialog(AlignmentWidget, f"{INPUT_DIR}/stack.tif")
	qtbot.mouseClick(w._btn_load_tif_apply, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert f"Selected file: {INPUT_DIR}/stack.tif" in lines[0]
	assert "TIFF loaded successfully. Shape=(10, 128, 256), dtype=uint16" in lines[1]

	# Align sans Coeff
	qtbot.mouseClick(w._btn_start_alignment, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Can't align tif file without factors." in lines[0]

	w.close()


##################################################
def test_align(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""
	Test basique de création du widget.

	- Clic sur 'Compute coefficients' sans stack ⇾ message d'erreur.
	- Simulation de différents comportements de QFileDialog / open_tif.
	- Clic sur 'Compute coefficients' avec stack chargée ⇾ message 'not implemented'.
	"""
	w = AlignmentWidget()
	qtbot.addWidget(w)
	w.resize(500, 250)
	w.show()
	qtbot.waitExposed(w)

	# Chargement du fichier Tif
	fake_qfiledialog(AlignmentWidget, f"{INPUT_DIR}/stack.tif")
	qtbot.mouseClick(w._btn_load_tif_apply, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert f"Selected file: {INPUT_DIR}/stack.tif" in lines[0]
	assert "TIFF loaded successfully. Shape=(10, 128, 256), dtype=uint16" in lines[1]
	assert w._stack is not None

	# Chargement du fichier Coef
	fake_qfiledialog(AlignmentWidget, f"{INPUT_DIR}/alignment_coeffs.txt", "Text files (*.txt);;All files (*.*)")
	qtbot.mouseClick(w._btn_load_coef_apply, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert f"Selected file: {INPUT_DIR}/alignment_coeffs.txt" in lines[0]
	assert "Coefficients loaded successfully." in lines[1]
	assert w._coefs is not None

	qtbot.mouseClick(w._btn_start_alignment, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert f"File saved at {w._output_filename} (upscale=1)." in lines[0]
	output = Path(w._output_filename)
	output.unlink(missing_ok=True)
	w.close()
