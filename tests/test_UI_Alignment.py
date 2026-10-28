"""Teste le widget de calcul et d'application des alignements géométriques."""

from unittest.mock import Mock

import pytest
import tifffile
from qtpy.QtCore import Qt

from palm_tracer.UI.AlignmentWidget import AlignmentWidget  # Classe
from tests.Utils import *
from tests.Utils import send_file_drop

SIZE_X, SIZE_Y, INTENSITY, RATIO = 100, 50, 1000, 10
SIZE = int(SIZE_X * np.sqrt(SIZE_Y))
rng = np.random.default_rng(42)  # Générateur propre au jeu de données de ce module.
POINTS = np.stack([rng.uniform(1, SIZE_Y - 1, size=SIZE), rng.uniform(1, SIZE_X - 1, size=SIZE)], axis=1)


# ==================================================
# region Initialisation
# ==================================================
def test_widget_creation(qtbot):
	"""Vérifie la création du widget."""
	w = AlignmentWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)
	w.close()


# ==================================================
# endregion Initialisation
# ==================================================

# ==================================================
# region Glisser-déposer
# ==================================================
@pytest.mark.parametrize("scenario", ["stack", "coefficients", "pair", "reversed-pair", "legacy-text"],
						 ids=["single-stack", "single-csv", "stack-and-csv", "csv-and-stack", "legacy-text"])
def test_alignment_drop_loads_inputs(qtbot, tmp_path, scenario):
	"""Vérifie les chargements réels des entrées d'alignement et l'indépendance de l'ordre du dépôt."""
	widget = AlignmentWidget()
	qtbot.addWidget(widget)
	stack = np.arange(2 * 4 * 5, dtype=np.uint16).reshape(2, 4, 5)
	stack_file = tmp_path / "stack.STK"
	tifffile.imwrite(stack_file, stack, photometric="minisblack")
	coefficients = np.arange(20, dtype=float).reshape(2, 10)
	coefficient_file = tmp_path / ("coefficients.txt" if scenario == "legacy-text" else "coefficients.CSV")
	np.savetxt(coefficient_file, coefficients, delimiter=" " if scenario == "legacy-text" else ",")
	paths = {"stack":         [stack_file], "coefficients": [coefficient_file], "pair": [stack_file, coefficient_file],
			 "reversed-pair": [coefficient_file, stack_file], "legacy-text": [coefficient_file]}[scenario]

	widget.show()
	send_file_drop(widget, paths)

	if stack_file in paths: np.testing.assert_array_equal(widget._stack, stack)
	if coefficient_file in paths: np.testing.assert_array_equal(widget._coeffs, coefficients)


# --------------------------------------------------
@pytest.mark.parametrize("names", [
		pytest.param(["first.tif", "second.stk"], id="two-stacks"),
		pytest.param(["first.csv", "second.csv"], id="two-coefficient-files"),
		pytest.param(["first.tif", "second.csv", "third.csv"], id="three-files"),
		pytest.param(["first.tif", "second.png"], id="unsupported-file")])
def test_alignment_drop_rejects_ambiguous_batch(qtbot, tmp_path, monkeypatch, names):
	"""Vérifie qu'un lot invalide ne déclenche aucun chargement partiel."""
	widget = AlignmentWidget()
	qtbot.addWidget(widget)
	load_stack, load_coefficients = Mock(), Mock()
	monkeypatch.setattr(widget, "_load_tif", load_stack)
	monkeypatch.setattr(widget, "_load_coef", load_coefficients)
	paths = [tmp_path / name for name in names]
	for path in paths: path.touch()

	widget.show()
	send_file_drop(widget, paths)

	load_stack.assert_not_called()
	load_coefficients.assert_not_called()


# ==================================================
# endregion Glisser-déposer
# ==================================================

# ==================================================
# region Fonctions de rappel
# ==================================================

# ==================================================
# region Chargement des TIFF et calcul des coefficients
# ==================================================
def test_bad_load_tif(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Vérifie la gestion des erreurs avec la boîte de dialogue d'ouverture de fichier."""
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
	assert "Selected file: nofile.tif." in lines[1]  # Le fichier a été détecté la seconde fois
	assert "Unable to read the TIFF file" in lines[2]  # Mais erreur
	assert w._stack is None

	w.close()


# --------------------------------------------------
def test_bad_compute(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Vérifie la création du widget."""
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


# --------------------------------------------------
def test_compute(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Vérifie la création du widget."""
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


# ==================================================
# endregion Chargement des TIFF et calcul des coefficients
# ==================================================

# ==================================================
# region Chargement des coefficients et alignement
# ==================================================
def test_bad_load_coef(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Vérifie la gestion des erreurs avec la boîte de dialogue d'ouverture de fichier."""
	w = AlignmentWidget()
	qtbot.addWidget(w)
	w.resize(500, 250)
	w.show()
	qtbot.waitExposed(w)

	# Simuler un "Cancel" sur le QFileDialog
	fake_qfiledialog(AlignmentWidget, None)
	qtbot.mouseClick(w._btn_load_coeff_apply, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "No coefficient file selected." in lines[0]  # On vérifie juste que le warning attendu est bien passé par print_warning

	# Bad Coeffs Input
	fake_qfiledialog(AlignmentWidget, "nofile.txt")
	qtbot.mouseClick(w._btn_load_coeff_apply, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Selected file: nofile.txt." in lines[0]
	assert "Unable to read the coefficient file" in lines[1]
	assert w._coeffs is None

	# Bad Coeffs Input
	fake_qfiledialog(AlignmentWidget, f"{INPUT_DIR}/bad_alignment_coeffs.txt")
	qtbot.mouseClick(w._btn_load_coeff_apply, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert f"Selected file: {INPUT_DIR}/bad_alignment_coeffs.txt." in lines[0]
	assert "The coefficient file is not in the correct format. Expected format: two lines of ten values (2x10)." in lines[1]
	assert w._coeffs is None

	w.close()


# --------------------------------------------------
def test_bad_align(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Vérifie la création du widget."""
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


# --------------------------------------------------
def test_align(qtbot, capsys, monkeypatch, fake_qfiledialog, input_stack):
	"""Vérifie la création du widget."""
	w = AlignmentWidget()
	qtbot.addWidget(w)
	w.resize(500, 250)
	w.show()
	qtbot.waitExposed(w)

	# Chargement du fichier Tif
	fake_qfiledialog(AlignmentWidget, str(input_stack))
	qtbot.mouseClick(w._btn_load_tif_apply, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert f"Selected file: {input_stack}" in lines[0]
	assert "TIFF loaded successfully. Shape=(10, 128, 256), dtype=uint16" in lines[1]
	assert w._stack is not None

	# Chargement du fichier Coef
	fake_qfiledialog(AlignmentWidget, f"{INPUT_DIR}/alignment_coeffs.txt", "Text files (*.txt);;All files (*.*)")
	qtbot.mouseClick(w._btn_load_coeff_apply, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert f"Selected file: {INPUT_DIR}/alignment_coeffs.txt" in lines[0]
	assert "Coefficients loaded successfully." in lines[1]
	assert w._coeffs is not None

	qtbot.mouseClick(w._btn_start_alignment, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert f"File saved at {w._output_filename} (upscale=1)." in lines[0]
	output = Path(w._output_filename)
	assert output.parent == input_stack.parent
	w.close()

# ==================================================
# endregion Chargement des coefficients et alignement
# ==================================================

# ==================================================
# endregion Fonctions de rappel
# ==================================================
