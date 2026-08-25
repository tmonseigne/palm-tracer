"""Teste le widget de migration des anciens résultats Metamorph."""

import shutil

from qtpy.QtCore import Qt

from palm_tracer._tests.Utils import *
from palm_tracer.UI.FileMigratorWidget import FileMigratorWidget  # Classe

INPUT_FOLDER = INPUT_DIR / "stack.PT"
OUTPUT_FOLDER = INPUT_DIR / "stack_PALM_Tracer"


##################################################
def test_widget_creation(qtbot):
	"""Vérifie la création du widget."""
	w = FileMigratorWidget()
	qtbot.addWidget(w)
	w.resize(500, 250)
	w.show()
	qtbot.waitExposed(w)
	w.close()


##################################################
def test_bad_load(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Vérifie la gestion des erreurs avec la boîte de dialogue d'ouverture de fichier."""
	w = FileMigratorWidget()
	qtbot.addWidget(w)
	w.resize(500, 250)
	w.show()
	qtbot.waitExposed(w)

	# Simuler un "Cancel" sur le QFileDialog
	fake_qfiledialog(FileMigratorWidget, None)
	qtbot.mouseClick(w._btn_load_folder, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "No folder selected." in lines[-1]

	# Bad file Input
	fake_qfiledialog(FileMigratorWidget, "bad folder")
	qtbot.mouseClick(w._btn_load_folder, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Unable to read the folder" in lines[-1]

	w.close()


##################################################
def test_mirgate(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Vérifie le lancement de la calibration."""
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
	w = FileMigratorWidget()
	qtbot.addWidget(w)
	w.resize(500, 250)
	w.show()
	qtbot.waitExposed(w)

	# Chargement du fichier de localisation
	fake_qfiledialog(FileMigratorWidget, str(INPUT_FOLDER))
	qtbot.mouseClick(w._btn_load_folder, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Folder loaded successfully." in lines[-1]

	# Lancement du calcul
	qtbot.mouseClick(w._btn_migrate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Migration successfull." in lines[-1]

	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)

	w.close()
