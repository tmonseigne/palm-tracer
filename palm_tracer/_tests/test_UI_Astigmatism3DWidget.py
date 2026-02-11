"""Fichier des tests pour le widget."""
import shutil

import pytest
from qtpy.QtCore import Qt

from palm_tracer._tests.Utils import *
from palm_tracer._tests.Utils import _FakeDownload
from palm_tracer.UI.Astigmatism3DWidget import Astigmatism3DWidget  # classe

LOC_FILE = INPUT_DIR / "astigmatism_3d_calibration.csv"
MODEL_FILE = "astigmatism_3d_model.csv"
PNG_FILE = "astigmatism_3d_model.png"
BACKUP_DIR = INPUT_DIR / "backup"


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_widget_creation(qtbot):
	"""Test basique de création du widget."""
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)
	w.close()


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_bad_load_loc(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Test basique d'erreurs avec la boite de dialogue d'ouverture de fichier."""
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	# Simuler un "Cancel" sur le QFileDialog
	fake_qfiledialog(Astigmatism3DWidget, None)
	qtbot.mouseClick(w._btn_load_compute, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "No file selected." in out  # On vérifie juste que le warning attendu est bien passé par print_warning

	# Bad file Input
	fake_qfiledialog(Astigmatism3DWidget, "nofile.csv")
	qtbot.mouseClick(w._btn_load_compute, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "Unable to read the CSV file" in out
	assert w._loc.empty

	# Bad Localization Input
	fake_qfiledialog(Astigmatism3DWidget, f"{INPUT_DIR}/tracking.csv")
	qtbot.mouseClick(w._btn_load_compute, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "The localization file is not in the correct format." in out
	assert w._loc.empty

	# Simuler un "Cancel" sur le QFileDialog
	fake_qfiledialog(Astigmatism3DWidget, None)
	qtbot.mouseClick(w._btn_load_loc_estimate, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "No file selected." in out  # On vérifie juste que le warning attendu est bien passé par print_warning

	# Bad file Input
	fake_qfiledialog(Astigmatism3DWidget, "nofile.csv")
	qtbot.mouseClick(w._btn_load_loc_estimate, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "Unable to read the CSV file" in out
	assert w._loc.empty

	# Bad Localization Input
	fake_qfiledialog(Astigmatism3DWidget, f"{INPUT_DIR}/tracking.csv")
	qtbot.mouseClick(w._btn_load_loc_estimate, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "The localization file is not in the correct format." in out
	assert w._loc.empty

	w.close()


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_bad_load_model(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Test basique d'erreurs avec la boite de dialogue d'ouverture de fichier."""
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	# Simuler un "Cancel" sur le QFileDialog
	fake_qfiledialog(Astigmatism3DWidget, None)
	qtbot.mouseClick(w._btn_load_model_estimate, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "No model file selected." in out  # On vérifie juste que le warning attendu est bien passé par print_warning

	# Bad Coef Input
	fake_qfiledialog(Astigmatism3DWidget, "nofile.txt")
	qtbot.mouseClick(w._btn_load_model_estimate, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "Unable to read the model file:" in out
	assert w._model.empty

	# Bad Model Input
	fake_qfiledialog(Astigmatism3DWidget, f"{INPUT_DIR}/tracking.csv")
	qtbot.mouseClick(w._btn_load_model_estimate, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "The model file is not in the correct format. Expected format: two lines of five values (2x5)." in out
	assert w._model.empty

	w.close()


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_bad_compute(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Test basique de lancement de la calibration sans fichier chargé."""
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	# Compute sans Tif
	qtbot.mouseClick(w._btn_compute, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "Can't Compute model without correct file loaded." in out
	w.close()


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_compute(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Test basique de lancement de la calibration"""
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	# Chargement du fichier de localisation
	fake_qfiledialog(Astigmatism3DWidget, str(LOC_FILE))
	qtbot.mouseClick(w._btn_load_compute, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "CSV loaded successfully." in out
	assert not w._loc.empty

	# Lancement du calcul
	qtbot.mouseClick(w._btn_compute, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "Model saved successfully." in out

	os.remove(INPUT_DIR / MODEL_FILE)

	w.close()


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_compute_z(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Test basique de lancement de la calibration"""
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	# Chargement du fichier de localisation
	fake_qfiledialog(Astigmatism3DWidget, str(LOC_FILE))
	qtbot.mouseClick(w._btn_load_compute, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "CSV loaded successfully." in out
	assert not w._loc.empty

	# passage de Zmax à 460, coche de get Z from plane et Z flip
	w._spin_z_compute.setValue(460)
	w._check_z_from_plane.setChecked(True)
	w._check_z_flip.setChecked(True)

	# Lancement du calcul
	qtbot.mouseClick(w._btn_compute, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "No Plane Column in file. We can't use it to intialize Z." in out

	# Ajout d'une colonne Plane de 1 à N.
	w._loc["Plane"] = range(1, len(w._loc) + 1)
	qtbot.mouseClick(w._btn_compute, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "Model saved successfully." in out

	os.remove(INPUT_DIR / MODEL_FILE)

	w.close()


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_bad_estimate(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Test basique de lancement de l'estimation sans fichier chargé."""
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	# Estimation sans localisation
	qtbot.mouseClick(w._btn_estimate, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "Can't estimate without correct localization file loaded." in out

	# Chargement du fichier de localisation
	fake_qfiledialog(Astigmatism3DWidget, str(LOC_FILE))
	qtbot.mouseClick(w._btn_load_loc_estimate, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "CSV loaded successfully." in out
	assert not w._loc.empty

	# Estimation sans model
	qtbot.mouseClick(w._btn_estimate, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "Can't estimate without correct model file loaded." in out

	w.close()


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_estimate(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Test basique de lancement de l'estimation."""
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	backup_file = f"{LOC_FILE}.tmp"
	shutil.copy2(LOC_FILE, backup_file)

	# Chargement du fichier de localisation
	fake_qfiledialog(Astigmatism3DWidget, str(LOC_FILE))
	qtbot.mouseClick(w._btn_load_loc_estimate, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "CSV loaded successfully." in out
	assert not w._loc.empty

	# Chargement du fichier model
	fake_qfiledialog(Astigmatism3DWidget, str(REF_DIR / MODEL_FILE))
	qtbot.mouseClick(w._btn_load_model_estimate, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "Model loaded successfully." in out
	assert not w._model.empty

	qtbot.mouseClick(w._btn_estimate, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert f"Backup done at" in out
	assert os.path.isfile(BACKUP_DIR / "astigmatism_3d_calibration.csv")

	shutil.copy2(backup_file, LOC_FILE)
	if os.path.isfile(backup_file): os.remove(backup_file)
	shutil.rmtree(BACKUP_DIR, ignore_errors=True)

	w.close()


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_estimate_backup(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Test basique de lancement de l'estimation."""
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	backup_file = f"{LOC_FILE}.tmp"
	shutil.copy2(LOC_FILE, backup_file)

	# Chargement du fichier de localisation
	fake_qfiledialog(Astigmatism3DWidget, str(LOC_FILE))
	qtbot.mouseClick(w._btn_load_loc_estimate, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "CSV loaded successfully." in out
	assert not w._loc.empty

	# Chargement du fichier model
	fake_qfiledialog(Astigmatism3DWidget, str(REF_DIR / MODEL_FILE))
	qtbot.mouseClick(w._btn_load_model_estimate, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "Model loaded successfully." in out
	assert not w._model.empty

	qtbot.mouseClick(w._btn_estimate, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert f"Backup done at" in out
	assert os.path.isfile(BACKUP_DIR / "astigmatism_3d_calibration.csv")

	qtbot.mouseClick(w._btn_estimate, Qt.MouseButton.LeftButton)  # Test de multiple backup
	out, err = capsys.readouterr()
	assert f"Backup done at" in out
	assert os.path.isfile(BACKUP_DIR / "astigmatism_3d_calibration_1.csv")

	qtbot.mouseClick(w._btn_estimate, Qt.MouseButton.LeftButton)  # Test de multiple backup
	out, err = capsys.readouterr()
	assert f"Backup done at" in out
	assert os.path.isfile(BACKUP_DIR / "astigmatism_3d_calibration_2.csv")

	w._check_b_estimate.setChecked(False)  # On recommence sans le backup
	qtbot.mouseClick(w._btn_estimate, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert f"Localization file with estimation saved successfully." in out

	shutil.copy2(backup_file, LOC_FILE)
	if os.path.isfile(backup_file): os.remove(backup_file)
	shutil.rmtree(BACKUP_DIR, ignore_errors=True)

	w.close()


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_sync_spin(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Test basique de vérification de lien entre les spins pixel size."""
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	init = w._spin_z_compute.value()
	w._spin_z_compute.setValue(init + 1)
	assert w._spin_z_estimate.value() == init + 1, "Mise à jour du spin sur Z invalide"

	init = w._spin_px_compute.value()
	w._spin_px_compute.setValue(init + 0.1)
	assert w._spin_px_estimate.value() == init + 0.1, "Mise à jour du spin sur Pixel Size invalide"

	w.close()


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_download(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Test basique du callback de téléchargement du graphique."""
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	# Chargement du fichier model
	fake_qfiledialog(Astigmatism3DWidget, str(REF_DIR / MODEL_FILE))
	qtbot.mouseClick(w._btn_load_model_estimate, Qt.MouseButton.LeftButton)
	out, err = capsys.readouterr()
	assert "Model loaded successfully." in out
	assert not w._model.empty

	# Simuler un "Cancel" sur le QFileDialog
	fake_qfiledialog(Astigmatism3DWidget, None)
	dl = _FakeDownload("astigmatism.png")
	w._on_download_requested(dl)
	assert dl.canceled

	# Test d'enregistrement de l'image (avec le callback)
	target = Path(REF_DIR / PNG_FILE)
	fake_qfiledialog(Astigmatism3DWidget, str(target))
	dl = _FakeDownload("astigmatism.png")
	w._on_download_requested(dl)

	assert dl.accepted
	assert dl.directory == str(target.parent)
	assert dl.filename == target.name

	w.close()
