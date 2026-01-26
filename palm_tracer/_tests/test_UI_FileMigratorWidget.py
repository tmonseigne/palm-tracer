""" Fichier des tests pour le widget. """
import shutil

import pytest
from qtpy.QtCore import Qt

from palm_tracer._tests.Utils import *
from palm_tracer.UI.FileMigratorWidget import FileMigratorWidget  # classe

INPUT_FOLDER = INPUT_DIR / "stack.PT"
OUTPUT_FOLDER = INPUT_DIR / "stack_PALM_Tracer"


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_widget_creation(qtbot):
	"""Test basique de création du widget."""
	w = FileMigratorWidget()
	qtbot.addWidget(w)
	w.resize(500, 250)
	w.show()
	qtbot.waitExposed(w)
	w.close()


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_bad_load(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Test basique d'erreurs avec la boite de dialogue d'ouverture de fichier."""
	w = FileMigratorWidget()
	qtbot.addWidget(w)
	w.resize(500, 250)
	w.show()
	qtbot.waitExposed(w)

	# Simuler un "Cancel" sur le QFileDialog
	fake_qfiledialog(FileMigratorWidget, None)
	qtbot.mouseClick(w._btn_load_folder, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "No folder selected." in out  # On vérifie juste que le warning attendu est bien passé par print_warning

	# Bad file Input
	fake_qfiledialog(FileMigratorWidget, "bad folder")
	qtbot.mouseClick(w._btn_load_folder, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "Unable to read the folder" in out

	w.close()


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_mirgate(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Test basique de lancement de la calibration"""
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
	w = FileMigratorWidget()
	qtbot.addWidget(w)
	w.resize(500, 250)
	w.show()
	qtbot.waitExposed(w)

	# Chargement du fichier de localisation
	fake_qfiledialog(FileMigratorWidget, str(INPUT_FOLDER))
	qtbot.mouseClick(w._btn_load_folder, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "Folder loaded successfully." in out

	# Lancement du calcul
	qtbot.mouseClick(w._btn_migrate, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "Migration successfull." in out

	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)

	w.close()
