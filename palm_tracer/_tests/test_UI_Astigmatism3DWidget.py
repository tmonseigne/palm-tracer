"""Fichier des tests pour le widget."""
import shutil

from qtpy.QtCore import Qt

from palm_tracer._tests.Utils import *
from palm_tracer._tests.Utils import _FakeDownload
from palm_tracer.UI.Astigmatism3DWidget import Astigmatism3DWidget  # classe

LOC_FILE = INPUT_DIR / "astigmatism_3d_calibration.csv"
MODEL_FILE = "astigmatism_3d_model.csv"
PNG_FILE = "astigmatism_3d_model.png"
BACKUP_DIR = INPUT_DIR / "backup"


##################################################
def test_widget_creation(qtbot):
	"""Test basique de création du widget."""
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)
	w.close()


##################################################
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
	lines = get_lines_output(capsys)
	assert "No file selected." in lines[0]  # On vérifie juste que le warning attendu est bien passé par print_warning

	# Bad file Input
	fake_qfiledialog(Astigmatism3DWidget, "nofile.csv")
	qtbot.mouseClick(w._btn_load_compute, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Selected file: nofile.csv." in lines[0]
	assert "Unable to read the CSV file" in lines[1]
	assert w._loc.empty

	# Bad Localization Input
	fake_qfiledialog(Astigmatism3DWidget, f"{INPUT_DIR}/tracking.csv")
	qtbot.mouseClick(w._btn_load_compute, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Selected file:" in lines[0]
	assert "The localization file is not in the correct format." in lines[1]
	assert w._loc.empty

	# Simuler un "Cancel" sur le QFileDialog
	fake_qfiledialog(Astigmatism3DWidget, None)
	qtbot.mouseClick(w._btn_load_loc_estimate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "No file selected." in lines[0]  # On vérifie juste que le warning attendu est bien passé par print_warning

	# Bad file Input
	fake_qfiledialog(Astigmatism3DWidget, "nofile.csv")
	qtbot.mouseClick(w._btn_load_loc_estimate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Selected file: nofile.csv." in lines[0]
	assert "Unable to read the CSV file" in lines[1]
	assert w._loc.empty

	# Bad Localization Input
	fake_qfiledialog(Astigmatism3DWidget, f"{INPUT_DIR}/tracking.csv")
	qtbot.mouseClick(w._btn_load_loc_estimate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Selected file:" in lines[0]
	assert "The localization file is not in the correct format." in lines[1]
	assert w._loc.empty

	w.close()


##################################################
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
	lines = get_lines_output(capsys)
	assert "No model file selected." in lines[0]  # On vérifie juste que le warning attendu est bien passé par print_warning

	# Bad Coef Input
	fake_qfiledialog(Astigmatism3DWidget, "nofile.txt")
	qtbot.mouseClick(w._btn_load_model_estimate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Selected file: nofile.txt." in lines[0]
	assert "Unable to read the model file:" in lines[1]
	assert w._model.empty

	# Bad Model Input
	fake_qfiledialog(Astigmatism3DWidget, f"{INPUT_DIR}/tracking.csv")
	qtbot.mouseClick(w._btn_load_model_estimate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Selected file:" in lines[0]
	assert "The model file is not in the correct format. Expected format: two lines of five values (2x5)." in lines[1]
	assert w._model.empty

	w.close()


##################################################
def test_bad_compute(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Test basique de lancement de la calibration sans fichier chargé."""
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	# Compute sans Tif
	qtbot.mouseClick(w._btn_compute, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Can't Compute model without correct file loaded." in lines[0]
	w.close()


##################################################
def test_check_loc(qtbot, capsys):
	"""Test basique de lancement de la calibration sans fichier chargé."""
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	# Chargement du fichier de localisation
	w._loc = pd.read_csv(LOC_FILE)
	w._check_loc()
	lines = get_lines_output(capsys)
	assert "There are 47 planes and 2 beads in file." in lines[0]

	w._loc.drop(columns=["Bead"], inplace=True)
	w._check_loc()
	lines = get_lines_output(capsys)
	assert "There are 47 planes and at least two localizations per plane. The 'Only one bead' option can't be used." in lines[0]

	w._loc = w._loc.iloc[:-10]
	w._check_loc()
	lines = get_lines_output(capsys)
	assert "There are 47 planes and some planes contain multiple localizations. It is recommended to use the 'Only one bead' option." in lines[0]

	w._loc = w._loc.iloc[:-37]
	w._check_loc()
	lines = get_lines_output(capsys)
	assert "There are 47 planes and only one bead." in lines[0]

	w._loc.drop(columns=["Plane"], inplace=True)
	w._check_loc()
	lines = get_lines_output(capsys)
	assert "No 'Plane' Column in file. 'Get Z from plane' and 'Only one bead' options can't be used." in lines[0]

	w._loc = pd.read_csv(LOC_FILE)
	w._loc["Z"] = 0
	w._check_loc()
	lines = get_lines_output(capsys)
	assert "There are 47 planes and 2 beads in file." in lines[0]

	w._loc.drop(columns=["Z"], inplace=True)
	w._check_loc()
	lines = get_lines_output(capsys)
	assert "There are 47 planes and 2 beads in file." in lines[0]
	w.close()


##################################################
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
	lines = get_lines_output(capsys)
	assert "Selected file: " in lines[0]
	assert "CSV loaded successfully with 94 points and 11 columns." in lines[1]
	assert not w._loc.empty

	# Lancement du calcul
	w._spin_px_compute.setValue(0.2)
	qtbot.mouseClick(w._btn_compute, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert len(lines) == 13  # 4 par modèle affiché + ligne finale
	assert "Model saved successfully." in lines[-1]

	ref = pd.read_csv(REF_DIR / f"astigmatism_3d_model_centered.csv", index_col=0)
	assert np.allclose(w._model, ref, atol=0.1, rtol=0), f"Résultat incorrect.\nAttendu : \n\t{ref}\nObtenu : \n\t{w._model}"

	(INPUT_DIR / MODEL_FILE).unlink(missing_ok=True)

	w.close()


##################################################
def test_compute_mean_beads(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Test basique de lancement de la calibration"""
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	# Chargement du fichier de localisation
	fake_qfiledialog(Astigmatism3DWidget, str(LOC_FILE))
	qtbot.mouseClick(w._btn_load_compute, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Selected file: " in lines[0]
	assert "CSV loaded successfully with 94 points and 11 columns." in lines[1]
	assert not w._loc.empty

	w._loc.loc[w._loc["Bead"] == 2, "Z"] *= 3  # la deuxieme bille à une amplitude 3 fois supérieure (pour avoir une moyenne de 2z sur les 2 billes)

	# Lancement du calcul
	w._spin_px_compute.setValue(0.2)
	qtbot.mouseClick(w._btn_compute, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert len(lines) == 13  # 4 par modèle affiché + ligne finale
	assert "Model saved successfully." in lines[-1]

	ref = pd.read_csv(REF_DIR / f"astigmatism_3d_model_centered.csv", index_col=0)
	# Il n'y a que 2 colonnes ou l'amplitude sur Z à eu une influence Z0 et W.
	ref["Z0"] *= 2
	ref["W"] *= 2
	assert np.allclose(w._model, ref, atol=0.1, rtol=0), f"Résultat incorrect.\nAttendu : \n\t{ref}\nObtenu : \n\t{w._model}"

	(INPUT_DIR / MODEL_FILE).unlink(missing_ok=True)

	w.close()


##################################################
def test_compute_remove_bead_col(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Test basique de lancement de la calibration"""
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	# Chargement du fichier de localisation
	fake_qfiledialog(Astigmatism3DWidget, str(LOC_FILE))
	qtbot.mouseClick(w._btn_load_compute, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Selected file: " in lines[0]
	assert "CSV loaded successfully with 94 points and 11 columns." in lines[1]
	assert not w._loc.empty

	w._loc.drop(columns=["Bead"], inplace=True)  # On supprime la colonne Bead

	# Lancement du calcul
	w._spin_px_compute.setValue(0.2)
	qtbot.mouseClick(w._btn_compute, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert len(lines) == 5  # 4 par modèle affiché + ligne finale
	assert "Model saved successfully." in lines[-1]

	ref = pd.read_csv(REF_DIR / f"astigmatism_3d_model_centered.csv", index_col=0)
	assert np.allclose(w._model, ref, atol=0.1, rtol=0), f"Résultat incorrect.\nAttendu : \n\t{ref}\nObtenu : \n\t{w._model}"

	(INPUT_DIR / MODEL_FILE).unlink(missing_ok=True)

	w.close()


##################################################
def test_compute_remove_multi(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Test basique de lancement de la calibration"""
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	# Chargement du fichier de localisation
	fake_qfiledialog(Astigmatism3DWidget, str(LOC_FILE))
	qtbot.mouseClick(w._btn_load_compute, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Selected file: " in lines[0]
	assert "CSV loaded successfully with 94 points and 11 columns." in lines[1]
	assert not w._loc.empty

	# Ajout des colonnes
	w._loc["Plane"] = range(1, len(w._loc) + 1)
	w._loc["X"] = 5
	w._loc["Y"] = 5
	w._loc.loc[4:6, "Plane"] = 3  # même plan pour ceux là
	w._loc.loc[4:6, "X"] = 3  # Mais x différent

	# Lancement du calcul
	w._spin_px_compute.setValue(0.2)
	qtbot.mouseClick(w._check_only_one, Qt.MouseButton.LeftButton)
	qtbot.mouseClick(w._btn_compute, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert len(lines) == 5  # 4 par modèle affiché + ligne finale
	assert "Model saved successfully." in lines[-1]

	(INPUT_DIR / MODEL_FILE).unlink(missing_ok=True)

	w.close()


##################################################
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
	lines = get_lines_output(capsys)
	assert "Selected file: " in lines[0]
	assert "CSV loaded successfully with 94 points and 11 columns." in lines[1]
	assert not w._loc.empty

	# passage de Zmax à 460, coche de get Z from plane et Z flip
	w._spin_px_compute.setValue(0.2)
	w._spin_z_compute.setValue(460)
	w._check_z_from_plane.setChecked(True)
	w._check_z_flip.setChecked(True)

	qtbot.mouseClick(w._btn_compute, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert len(lines) == 13  # 4 par modèle affiché + ligne finale
	assert "Model saved successfully." in lines[-1]

	ref = pd.read_csv(REF_DIR / f"astigmatism_3d_model_centered.csv", index_col=0)
	assert np.allclose(w._model, ref, atol=0.1, rtol=0), f"Résultat incorrect.\nAttendu : \n\t{ref}\nObtenu : \n\t{w._model}"

	(INPUT_DIR / MODEL_FILE).unlink(missing_ok=True)

	# Suppression de la colonne Plane
	w._loc.drop(columns=["Plane"], inplace=True)
	qtbot.mouseClick(w._btn_compute, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "No Plane Column in file. We can't use it to intialize Z." in lines[0]

	# Ajout d'une colonne Plane de 1 à N.
	w._loc["Plane"] = range(1, len(w._loc) + 1)

	w.close()


##################################################
def test_compute_center_z(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Test basique de lancement de la calibration"""
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	# Chargement du fichier de localisation
	fake_qfiledialog(Astigmatism3DWidget, str(LOC_FILE))
	qtbot.mouseClick(w._btn_load_compute, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Selected file: " in lines[0]
	assert "CSV loaded successfully with 94 points and 11 columns." in lines[1]
	assert not w._loc.empty

	# Lancement du calcul
	w._spin_px_compute.setValue(0.2)
	qtbot.mouseClick(w._check_z_center, Qt.MouseButton.LeftButton)
	qtbot.mouseClick(w._btn_compute, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert len(lines) == 13  # 4 par modèle affiché + ligne finale
	assert "Model saved successfully." in lines[-1]

	ref = pd.read_csv(REF_DIR / f"astigmatism_3d_model.csv", index_col=0)
	assert np.allclose(w._model, ref, atol=0.1, rtol=0), f"Résultat incorrect.\nAttendu : \n\t{ref}\nObtenu : \n\t{w._model}"

	(INPUT_DIR / MODEL_FILE).unlink(missing_ok=True)

	w.close()


##################################################
def test_compute_bad_model(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Test basique de lancement de la calibration"""
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	# Chargement du fichier de localisation
	fake_qfiledialog(Astigmatism3DWidget, str(LOC_FILE))
	qtbot.mouseClick(w._btn_load_compute, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Selected file: " in lines[0]
	assert "CSV loaded successfully with 94 points and 11 columns." in lines[1]
	assert not w._loc.empty

	w._loc["Sigma X"] = rng.normal(loc=1.0, scale=1.0, size=len(w._loc))
	w._loc["Sigma Y"] = rng.normal(loc=1.0, scale=1.0, size=len(w._loc))

	# Lancement du calcul
	w._spin_px_compute.setValue(0.2)
	qtbot.mouseClick(w._btn_compute, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert len(lines) == 17  # 4 par modèle affiché + 4 lignes Fail Calibration + ligne finale
	assert "Model saved successfully." in lines[-1]

	(INPUT_DIR / MODEL_FILE).unlink(missing_ok=True)

	w.close()


##################################################
def test_bad_estimate(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Test basique de lancement de l'estimation sans fichier chargé."""
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	# Estimation sans localisation
	qtbot.mouseClick(w._btn_estimate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Can't estimate without correct localization file loaded." in lines[0]

	# Chargement du fichier de localisation
	fake_qfiledialog(Astigmatism3DWidget, str(LOC_FILE))
	qtbot.mouseClick(w._btn_load_loc_estimate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Selected file: " in lines[0]
	assert "CSV loaded successfully with 94 points and 11 columns." in lines[1]
	assert not w._loc.empty

	# Estimation sans model
	qtbot.mouseClick(w._btn_estimate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Can't estimate without correct model file loaded." in lines[0]

	w.close()


##################################################
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
	lines = get_lines_output(capsys)
	assert "Selected file: " in lines[0]
	assert "CSV loaded successfully with 94 points and 11 columns." in lines[1]
	assert not w._loc.empty

	# Chargement du fichier model
	fake_qfiledialog(Astigmatism3DWidget, str(REF_DIR / MODEL_FILE))
	qtbot.mouseClick(w._btn_load_model_estimate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Selected file: " in lines[0]
	assert "Model loaded successfully." in lines[1]
	assert not w._model.empty

	qtbot.mouseClick(w._btn_estimate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert f"Backup done at" in lines[0]
	assert (BACKUP_DIR / "astigmatism_3d_calibration.csv").is_file()

	shutil.copy2(backup_file, LOC_FILE)
	Path(backup_file).unlink(missing_ok=True)
	shutil.rmtree(BACKUP_DIR, ignore_errors=True)

	w.close()


##################################################
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
	lines = get_lines_output(capsys)
	assert "Selected file: " in lines[0]
	assert "CSV loaded successfully with 94 points and 11 columns." in lines[1]
	assert not w._loc.empty

	# Chargement du fichier model
	fake_qfiledialog(Astigmatism3DWidget, str(REF_DIR / MODEL_FILE))
	qtbot.mouseClick(w._btn_load_model_estimate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Selected file: " in lines[0]
	assert "Model loaded successfully." in lines[1]
	assert not w._model.empty

	qtbot.mouseClick(w._btn_estimate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert f"Backup done at" in lines[0]
	assert (BACKUP_DIR / "astigmatism_3d_calibration.csv").is_file()

	qtbot.mouseClick(w._btn_estimate, Qt.MouseButton.LeftButton)  # Test de multiple backup
	lines = get_lines_output(capsys)
	assert f"Backup done at" in lines[0]
	assert (BACKUP_DIR / "astigmatism_3d_calibration_1.csv").is_file()

	qtbot.mouseClick(w._btn_estimate, Qt.MouseButton.LeftButton)  # Test de multiple backup
	lines = get_lines_output(capsys)
	assert f"Backup done at" in lines[0]
	assert (BACKUP_DIR / "astigmatism_3d_calibration_2.csv").is_file()

	w._check_b_estimate.setChecked(False)  # On recommence sans le backup
	qtbot.mouseClick(w._btn_estimate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert f"Localization file with estimation saved successfully." in lines[0]

	shutil.copy2(backup_file, LOC_FILE)
	Path(backup_file).unlink(missing_ok=True)
	shutil.rmtree(BACKUP_DIR, ignore_errors=True)

	w.close()


##################################################
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
	lines = get_lines_output(capsys)
	assert "Selected file: " in lines[0]
	assert "Model loaded successfully." in lines[1]
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
