"""Teste le widget de calibration et d'estimation axiale par astigmatisme 3D."""

from unittest.mock import Mock

import numpy as np
import pandas as pd
import pytest
from qtpy.QtCore import Qt

from palm_tracer.Processing.Astigmatism3D import model_projection_validity, model_validity, sigma_model
from palm_tracer.Tools import FileIO
from palm_tracer.UI.Astigmatism3DWidget import Astigmatism3DWidget  # Classe
from tests.Utils import *
from tests.Utils import _FakeDownload

LOC_FILE = INPUT_DIR / "astigmatism_3d_calibration.csv"
MODEL_FILE = "astigmatism_3d_model.csv"
PNG_FILE = "astigmatism_3d_model.png"


# ==================================================
# region Initialisation
# ==================================================
def test_widget_creation(qtbot):
	"""Vérifie la création du widget."""
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	assert not hasattr(w, "_btn_compute")
	assert w._btn_estimate.text() == "Compute Z"
	assert "blank" not in w._sanity[0]
	assert list(w._sanity[0])[-1] == "slope_mean"
	assert list(w._sanity[1])[-1] == "astigmatism"
	assert w._sanity[0]["slope_mean"]["label"].text() == "Slope:"
	assert w._sanity[0]["slope_mean"]["unit"].text() == "px/nm"
	assert w._sanity[1]["astigmatism"]["label"].text() == "Astigmatism:"
	assert w._sanity[1]["astigmatism"]["unit"].text() == "nm"
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)
	w.close()


# --------------------------------------------------
def test_sync_spin(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Vérifie la synchronisation des tailles de pixel et des limites axiales entre les deux onglets."""
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


# ==================================================
# endregion Initialisation
# ==================================================

# ==================================================
# region Interface utilisateur
# ==================================================
@pytest.mark.parametrize("z_max", [100, 250], ids=["small-range", "large-range"])
def test_sanity_check_filters_z_limits(qtbot, z_max):
	"""Vérifie les scores affichés avec les vrais calculs après exclusion des points aux bornes ou au-delà."""
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w._spin_z_compute.setValue(z_max)
	model = np.array([[-50, 100, 0, 0, 30], [50, 100, 0, 0, 30]], dtype=float)
	pixel_size = 160
	z = np.array([-0.999999, -0.5, 0, 0.5, 0.999999]) * z_max
	valid_points = np.column_stack((sigma_model(model[0], z, pixel_size), sigma_model(model[1], z, pixel_size), z))
	points = np.vstack(([[100, 200, -2 * z_max], [100, 200, -z_max]], valid_points, [[100, 200, z_max], [100, 200, 2 * z_max]]))
	original = points.copy()
	expected_sigma = model_validity(valid_points, model, pixel_size, 1)
	expected_projection = model_projection_validity(valid_points, model, z_max, pixel_size)

	w._update_sanity_values(points, model, pixel_size)

	np.testing.assert_array_equal(points, original)
	for key, value in expected_sigma.items():
		expected_text = f"{100 * value:0.2f}" if "r2" in key else f"{value:0.4f}"
		assert w._sanity[0][key]["value"].text() == expected_text
	for key, value in expected_projection.items():
		column = 0 if key == "slope_mean" else 1
		assert w._sanity[column][key]["value"].text() == f"{value:0.4f}"
	assert w._sanity[0]["r2_x"]["value"].text() == "100.00"
	assert w._sanity[0]["r2_y"]["value"].text() == "100.00"
	w.close()


# --------------------------------------------------
@pytest.mark.parametrize("points", [
		pytest.param(np.empty((0, 3)), id="empty-data"),
		pytest.param(np.array([[1, 2, -101], [1, 2, -100], [1, 2, 100], [1, 2, 101]], dtype=float), id="all-excluded")])
def test_sanity_check_without_valid_points(qtbot, points):
	"""Vérifie la remise à zéro de l'affichage quand aucun point n'est utilisable."""
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w._spin_z_compute.setValue(100)
	for column in w._sanity:
		for metric in column.values():
			metric["value"].setText("123.45")

	model = np.array([[-50, 100, 0, 0, 30], [50, 100, 0, 0, 30]], dtype=float)
	w._update_sanity_values(points, model, 160)

	for column in w._sanity:
		for metric in column.values():
			assert metric["value"].text().strip() == "--"
	w.close()


# --------------------------------------------------
@pytest.mark.parametrize("mode, expected", [
		pytest.param(0, "cross", id="cross-section"),
		pytest.param(1, "slope", id="slope"),
		pytest.param(2, "curve", id="sigma-curves")])
def test_update_plot_modes(qtbot, monkeypatch, mode, expected):
	"""Transmet le mode sélectionné et les paramètres physiques au générateur de figure."""
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	# Observe un seul rafraîchissement explicite, sans rendu Web ni calcul de calibration.
	figure = w._grapher.blank()
	plot = Mock(return_value=figure)
	update_web = Mock()
	monkeypatch.setattr(w._grapher, "astigmatism3d", plot)
	monkeypatch.setattr(w, "_update_web_widget", update_web)
	w._model = pd.DataFrame(np.array([[-50, 100, 0, 0, 30], [50, 100, 0, 0, 30]], dtype=float))
	w._loc = pd.DataFrame()
	# Le sélecteur est contrôlé sans déclencher son callback avant la vérification.
	monkeypatch.setattr(w._btg_type_compute, "checkedId", lambda: mode)
	w._update_plot()
	plot.assert_called_once()
	args, kwargs = plot.call_args
	np.testing.assert_array_equal(args[0], w._model.to_numpy())
	assert args[1] is None
	assert kwargs == {"title": w.GRAPH_TITLE, "pixel_size": w._spin_px_compute.value() * 1000, "z_max": w._spin_z_estimate.value(), "mode": expected}
	assert w._fig is figure
	update_web.assert_called_once_with()


# ==================================================
# endregion Interface utilisateur
# ==================================================

# ==================================================
# region Fonctions de rappel
# ==================================================

# ==================================================
# region Chargement des données et modèles
# ==================================================
def test_check_loc(qtbot, capsys):
	"""Vérifie l'adaptation des options aux colonnes, plans et billes présents dans les localisations."""
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

	w._loc = w._loc.drop(columns=["Bead"])
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

	w._loc = w._loc.drop(columns=["Plane"])
	w._check_loc()
	lines = get_lines_output(capsys)
	assert "No 'Plane' Column in file. 'Get Z from plane' and 'Only one bead' options can't be used." in lines[0]

	w._loc = pd.read_csv(LOC_FILE)
	w._loc["Z"] = 0
	w._check_loc()
	lines = get_lines_output(capsys)
	assert "There are 47 planes and 2 beads in file." in lines[0]

	w._loc = w._loc.drop(columns=["Z"])
	w._check_loc()
	lines = get_lines_output(capsys)
	assert "There are 47 planes and 2 beads in file." in lines[0]
	w.close()


# --------------------------------------------------
@pytest.mark.parametrize("button", ["_btn_load_compute", "_btn_load_loc_estimate"], ids=["calibration-tab", "estimation-tab"])
def test_bad_load_loc(qtbot, capsys, monkeypatch, fake_qfiledialog, button):
	"""Vérifie la gestion des erreurs avec la boîte de dialogue d'ouverture de fichier."""
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	# Simuler un "Cancel" sur le QFileDialog
	fake_qfiledialog(Astigmatism3DWidget, None)
	qtbot.mouseClick(getattr(w, button), Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "No file selected." in lines[0]  # On vérifie juste que le warning attendu est bien passé par print_warning

	# Bad file Input
	fake_qfiledialog(Astigmatism3DWidget, "nofile.csv")
	qtbot.mouseClick(getattr(w, button), Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Selected file: nofile.csv." in lines[0]
	assert "Unable to read the CSV file" in lines[1]
	assert w._loc.empty

	# Bad Localization Input
	fake_qfiledialog(Astigmatism3DWidget, f"{INPUT_DIR}/tracking.csv")
	qtbot.mouseClick(getattr(w, button), Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Selected file:" in lines[0]
	assert "The localization file is not in the correct format." in lines[1]
	assert w._loc.empty

	w.close()


# --------------------------------------------------
def test_estimation_load_does_not_calibrate(qtbot, capsys, fake_qfiledialog, tmp_path):
	"""Vérifie que le chargement destiné à Compute Z et ses paramètres ne recalibrent pas le modèle fourni."""
	localization_file = tmp_path / LOC_FILE.name
	shutil.copy2(LOC_FILE, localization_file)
	original_file = localization_file.read_bytes()
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	fake_qfiledialog(Astigmatism3DWidget, str(localization_file))
	qtbot.mouseClick(w._btn_load_loc_estimate, Qt.MouseButton.LeftButton)
	assert w._model.empty
	assert w._calibration_z is None
	fake_qfiledialog(Astigmatism3DWidget, str(REF_DIR / MODEL_FILE))
	qtbot.mouseClick(w._btn_load_model_estimate, Qt.MouseButton.LeftButton)
	model = w._model.copy()
	capsys.readouterr()

	w._spin_px_estimate.setValue(0.2)
	w._spin_z_estimate.setValue(450)

	pd.testing.assert_frame_equal(w._model, model)
	assert not (tmp_path / MODEL_FILE).exists()
	assert localization_file.read_bytes() == original_file
	assert get_lines_output(capsys) == []
	w.close()


# --------------------------------------------------
def test_bad_load_model(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Vérifie la gestion des erreurs avec la boîte de dialogue d'ouverture de fichier."""
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

	# Bad Coeffs Input
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


# ==================================================
# endregion Chargement des données et modèles
# ==================================================

# ==================================================
# region Calibration
# ==================================================
def test_compute_without_calibration_data(qtbot, capsys):
	"""Vérifie que les paramètres restent modifiables sans déclencher de calibration avant le chargement."""
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w._spin_px_compute.setValue(0.2)
	w._spin_z_compute.setValue(450)
	w._check_z_flip.setChecked(True)
	assert w._model.empty
	assert w._calibration_z is None
	assert get_lines_output(capsys) == []
	w.close()


# --------------------------------------------------
@pytest.mark.parametrize("scenario, reference, scale, bead_count", [
		pytest.param("original", "astigmatism_3d_model_centered.csv", 1, 2, id="original-z"),
		pytest.param("mean-beads", "astigmatism_3d_model_centered.csv", 2, 2, id="mean-beads"),
		pytest.param("single-bead", "astigmatism_3d_model_centered.csv", 1, 1, id="single-bead"),
		pytest.param("plane-z", "astigmatism_3d_model_centered.csv", 1, 2, id="plane-z-flipped"),
		pytest.param("uncentered", "astigmatism_3d_model.csv", 1, 2, id="uncentered")])
def test_compute_on_localization_load(qtbot, capsys, fake_qfiledialog, tmp_path, user_model_path, scenario, reference, scale, bead_count):
	"""Vérifie la calibration immédiate au chargement, ses résultats et le CSV effectivement sauvegardé."""
	# Préparation des localisations du scénario dans un fichier temporaire.
	data = pd.read_csv(LOC_FILE)
	if scenario == "mean-beads":
		data.loc[data["Bead"] == 2, "Z"] *= 3
	elif scenario == "single-bead":
		data = data.drop(columns=["Bead"])
	localization_file = tmp_path / LOC_FILE.name
	data.to_csv(localization_file, index=False)
	original_file = localization_file.read_bytes()
	# Configuration des options de calibration avant de charger les localisations.
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w._spin_px_compute.setValue(0.2)
	w._check_z_from_plane.setChecked(scenario == "plane-z")
	w._check_z_flip.setChecked(scenario == "plane-z")
	w._check_z_center.setChecked(scenario != "uncentered")
	capsys.readouterr()

	# Le chargement doit déclencher immédiatement le calcul et la sauvegarde du modèle.
	fake_qfiledialog(Astigmatism3DWidget, str(localization_file))
	qtbot.mouseClick(w._btn_load_compute, Qt.MouseButton.LeftButton)

	lines = get_lines_output(capsys)
	assert "Selected file:" in lines[0]
	assert "CSV loaded successfully" in lines[1]
	assert sum("Model for bead " in line for line in lines) == bead_count
	assert sum("Model saved successfully." in line for line in lines) == 1
	ref = pd.read_csv(REF_DIR / reference, index_col=0)
	ref[["Z0", "W"]] *= scale
	assert np.allclose(w._model, ref, atol=0.1, rtol=0)
	# Vérification des deux sauvegardes du modèle et de la préservation du fichier d'entrée.
	saved_model = pd.read_csv(tmp_path / MODEL_FILE, index_col=0)
	pd.testing.assert_frame_equal(saved_model, w._model)
	pd.testing.assert_frame_equal(pd.read_csv(user_model_path, index_col=0), w._model)
	np.testing.assert_array_equal(w._calibration_z, data["Z"].to_numpy())
	assert localization_file.read_bytes() == original_file
	w.close()


# --------------------------------------------------
@pytest.mark.parametrize("attribute, value", [
		pytest.param("_spin_px_compute", 0.21, id="pixel-size"),
		pytest.param("_spin_z_compute", 450, id="z-limit"),
		pytest.param("_spin_z_interval", 25, id="plane-interval"),
		pytest.param("_check_z_from_plane", False, id="z-from-plane"),
		pytest.param("_check_z_center", False, id="center-z"),
		pytest.param("_check_z_flip", True, id="flip-z"),
		pytest.param("_check_only_one", True, id="one-bead"),
		pytest.param("_spin_px_estimate", 0.21, id="synced-pixel-size"),
		pytest.param("_spin_z_estimate", 450, id="synced-z-limit")])
def test_compute_on_parameter_change(qtbot, capsys, fake_qfiledialog, tmp_path, attribute, value):
	"""Vérifie un unique recalcul complet pour chaque paramètre, y compris les paramètres synchronisés."""
	localization_file = tmp_path / LOC_FILE.name
	shutil.copy2(LOC_FILE, localization_file)
	original_file = localization_file.read_bytes()
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w._spin_px_compute.setValue(0.2)
	fake_qfiledialog(Astigmatism3DWidget, str(localization_file))
	qtbot.mouseClick(w._btn_load_compute, Qt.MouseButton.LeftButton)
	capsys.readouterr()

	control = getattr(w, attribute)
	if isinstance(value, bool):
		control.setChecked(value)
	else:
		control.setValue(value)

	lines = get_lines_output(capsys)
	assert sum("Model saved successfully." in line for line in lines) == 1
	pd.testing.assert_frame_equal(pd.read_csv(tmp_path / MODEL_FILE, index_col=0), w._model)
	assert w._spin_px_compute.value() == w._spin_px_estimate.value()
	assert w._spin_z_compute.value() == w._spin_z_estimate.value()
	assert localization_file.read_bytes() == original_file
	w.close()


# --------------------------------------------------
def test_compute_reuses_original_z(qtbot, fake_qfiledialog, tmp_path, user_model_path):
	"""Vérifie que les changements successifs ne réutilisent ni les Z estimés ni une inversion précédente."""
	localization_file = tmp_path / LOC_FILE.name
	shutil.copy2(LOC_FILE, localization_file)
	original_z = pd.read_csv(localization_file)["Z"].to_numpy()
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w._spin_px_compute.setValue(0.2)
	w._check_z_from_plane.setChecked(False)
	fake_qfiledialog(Astigmatism3DWidget, str(localization_file))
	qtbot.mouseClick(w._btn_load_compute, Qt.MouseButton.LeftButton)
	original_model = w._model.copy()

	w._check_z_flip.setChecked(True)
	assert not np.allclose(w._model, original_model)
	pd.testing.assert_frame_equal(pd.read_csv(user_model_path, index_col=0), w._model)
	w._spin_px_compute.setValue(0.21)
	w._spin_px_compute.setValue(0.2)
	w._check_z_flip.setChecked(False)

	np.testing.assert_array_equal(w._calibration_z, original_z)
	pd.testing.assert_frame_equal(w._model, original_model)
	pd.testing.assert_frame_equal(pd.read_csv(tmp_path / MODEL_FILE, index_col=0), original_model)
	pd.testing.assert_frame_equal(pd.read_csv(user_model_path, index_col=0), original_model)
	w.close()


# --------------------------------------------------
def test_compute_user_backup_unavailable(qtbot, capsys, tmp_path, user_model_path):
	"""Vérifie la propagation de l'erreur de sauvegarde utilisateur après l'écriture locale, sans faux message de succès."""
	user_model_path.parent.write_text("blocked", encoding="utf-8")  # Un fichier empêche la création du dossier de sauvegarde.
	localization_file = tmp_path / LOC_FILE.name
	shutil.copy2(LOC_FILE, localization_file)
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w._loc_filename = localization_file
	w._loc = pd.read_csv(localization_file)
	w._calibration_z = w._loc["Z"].to_numpy(dtype=float, copy=True)
	previous_figure = w._fig
	capsys.readouterr()

	with pytest.raises(FileExistsError):
		w._on_compute()

	lines = get_lines_output(capsys)
	assert not any("Model saved successfully." in line for line in lines)
	pd.testing.assert_frame_equal(pd.read_csv(tmp_path / MODEL_FILE, index_col=0), w._model)
	assert w._fig is previous_figure
	assert user_model_path.parent.read_text(encoding="utf-8") == "blocked"
	w.close()


# --------------------------------------------------
def test_compute_remove_multi(qtbot, capsys, fake_qfiledialog, tmp_path):
	"""Vérifie la calibration automatique après désambiguïsation de plusieurs localisations sur un même plan."""
	data = pd.read_csv(LOC_FILE)
	data["Plane"] = range(1, len(data) + 1)
	data["X"], data["Y"] = 5, 5
	data.loc[4:6, "Plane"] = 3
	data.loc[4:6, "X"] = 3
	localization_file = tmp_path / LOC_FILE.name
	data.to_csv(localization_file, index=False)
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w._spin_px_compute.setValue(0.2)
	w._check_z_from_plane.setChecked(False)
	w._check_only_one.setChecked(True)
	capsys.readouterr()

	fake_qfiledialog(Astigmatism3DWidget, str(localization_file))
	qtbot.mouseClick(w._btn_load_compute, Qt.MouseButton.LeftButton)

	lines = get_lines_output(capsys)
	assert sum("Model for bead " in line for line in lines) == 1
	assert sum("Model saved successfully." in line for line in lines) == 1
	pd.testing.assert_frame_equal(pd.read_csv(tmp_path / MODEL_FILE, index_col=0), w._model)
	w.close()


# --------------------------------------------------
def test_compute_missing_plane(qtbot, capsys, fake_qfiledialog, tmp_path):
	"""Vérifie que l'absence de plans désactive les options concernées avant l'unique calibration automatique."""
	localization_file = tmp_path / LOC_FILE.name
	pd.read_csv(LOC_FILE).drop(columns=["Plane"]).to_csv(localization_file, index=False)
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w._spin_px_compute.setValue(0.2)
	capsys.readouterr()

	fake_qfiledialog(Astigmatism3DWidget, str(localization_file))
	qtbot.mouseClick(w._btn_load_compute, Qt.MouseButton.LeftButton)

	lines = get_lines_output(capsys)
	assert not w._check_z_from_plane.isChecked()
	assert not w._check_z_from_plane.isEnabled()
	assert not w._check_only_one.isEnabled()
	assert sum("Model saved successfully." in line for line in lines) == 1
	assert "No 'Plane' Column in file." in lines[2]
	w.close()


# --------------------------------------------------
def test_compute_missing_plane_with_option_enabled(qtbot, capsys, fake_qfiledialog, tmp_path, user_model_path):
	"""Vérifie l'arrêt du recalcul si la colonne Plane disparaît alors que son utilisation reste sélectionnée."""
	localization_file = tmp_path / LOC_FILE.name
	shutil.copy2(LOC_FILE, localization_file)
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	fake_qfiledialog(Astigmatism3DWidget, str(localization_file))
	qtbot.mouseClick(w._btn_load_compute, Qt.MouseButton.LeftButton)
	assert w._check_z_from_plane.isChecked()
	previous_model = w._model.copy()
	local_model = tmp_path / MODEL_FILE
	previous_local_file = local_model.read_bytes()
	previous_user_file = user_model_path.read_bytes()
	w._loc = w._loc.drop(columns=["Plane"])
	capsys.readouterr()

	w._spin_z_interval.setValue(w._spin_z_interval.value() + 1)

	assert get_lines_output(capsys) == ["No Plane Column in file. We can't use it to initialize Z."]
	pd.testing.assert_frame_equal(w._model, previous_model)
	assert local_model.read_bytes() == previous_local_file
	assert user_model_path.read_bytes() == previous_user_file
	w.close()


# --------------------------------------------------
def test_compute_bad_model(qtbot, capsys, fake_qfiledialog, tmp_path, user_model_path, monkeypatch):
	"""Vérifie l'avertissement et la sauvegarde lorsque la calibration renvoie les paramètres initiaux."""
	data = pd.read_csv(LOC_FILE)
	localization_file = tmp_path / LOC_FILE.name
	data.to_csv(localization_file, index=False)
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w._spin_px_compute.setValue(0.2)
	w._check_z_from_plane.setChecked(False)
	w._check_z_center.setChecked(False)
	# Des sigmas aléatoires ne garantissent pas l'échec du solveur : imposer ici son résultat
	# pour tester le comportement de l'interface, indépendamment de sa convergence numérique.
	initial_width = (data["Z"].max() - data["Z"].min()) / 4
	initial_model = pd.DataFrame([[-100.0, initial_width, 0.0, 0.0, 200.0],
								  [100.0, initial_width, 0.0, 0.0, 200.0]],
								 columns=["Z0", "W", "C3", "C4", "A"], index=["X", "Y"])
	calibration = Mock(side_effect=lambda *_args: initial_model.copy())
	monkeypatch.setattr(w._palm, "astigmatism_3d_calibration", calibration)
	# Le rendu Web dispose de ses propres tests ; ce scénario cible les avertissements et les sauvegardes.
	monkeypatch.setattr(w, "_update_web_widget", Mock())
	capsys.readouterr()

	fake_qfiledialog(Astigmatism3DWidget, str(localization_file))
	qtbot.mouseClick(w._btn_load_compute, Qt.MouseButton.LeftButton)

	lines = get_lines_output(capsys)
	assert calibration.call_count == data["Bead"].nunique()
	for axis in ("X", "Y"):
		assert sum(f"Model Calibration keep initial state on axis {axis}." in line for line in lines) == calibration.call_count
	assert sum("Model saved successfully." in line for line in lines) == 1
	pd.testing.assert_frame_equal(w._model, initial_model)
	pd.testing.assert_frame_equal(pd.read_csv(tmp_path / MODEL_FILE, index_col=0), initial_model)
	pd.testing.assert_frame_equal(pd.read_csv(user_model_path, index_col=0), initial_model)
	w.close()


# ==================================================
# endregion Calibration
# ==================================================

# ==================================================
# region Modèle par défaut
# ==================================================
def test_set_default_model_without_model(qtbot, capsys):
	"""Permet d'activer la sauvegarde par défaut avant de calculer un modèle."""
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w._check_set_default_model.setChecked(True)
	assert not FileIO.DEFAULT_ASTIGMATISM_MODEL.exists()
	assert get_lines_output(capsys) == []
	w.close()


# --------------------------------------------------
@pytest.mark.parametrize("enable_before_load", [False, True], ids=["enable-after-model", "enable-before-model"])
def test_set_default_model(qtbot, tmp_path, fake_qfiledialog, enable_before_load):
	"""Vérifie la sauvegarde automatique du modèle par défaut et son arrêt lorsque l'option est décochée."""
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	assert not hasattr(w, "_btn_set_default_model")
	assert not w._check_set_default_model.isChecked()
	w._check_set_default_model.setChecked(enable_before_load)
	localization_file = tmp_path / LOC_FILE.name
	shutil.copyfile(LOC_FILE, localization_file)
	fake_qfiledialog(Astigmatism3DWidget, str(localization_file))
	qtbot.mouseClick(w._btn_load_compute, Qt.MouseButton.LeftButton)
	if not enable_before_load:
		assert not FileIO.DEFAULT_ASTIGMATISM_MODEL.exists()
		w._check_set_default_model.setChecked(True)
	pd.testing.assert_frame_equal(pd.read_csv(FileIO.DEFAULT_ASTIGMATISM_MODEL, index_col=0), w._model)
	w._spin_z_interval.setValue(w._spin_z_interval.value() + 10)
	pd.testing.assert_frame_equal(pd.read_csv(FileIO.DEFAULT_ASTIGMATISM_MODEL, index_col=0), w._model)
	previous = FileIO.DEFAULT_ASTIGMATISM_MODEL.read_bytes()
	w._check_set_default_model.setChecked(False)
	w._spin_z_interval.setValue(w._spin_z_interval.value() + 10)
	assert FileIO.DEFAULT_ASTIGMATISM_MODEL.read_bytes() == previous
	pd.testing.assert_frame_equal(pd.read_csv(FileIO.USER_ASTIGMATISM_MODEL, index_col=0), w._model)
	w.close()


# --------------------------------------------------
@pytest.mark.parametrize("content", [
		pytest.param("valid", id="valid-default"),
		pytest.param(None, id="missing-default"),
		pytest.param(",Z0,W\nX,1,2\n", id="invalid-default"),
		pytest.param('"unterminated quote\n', id="unreadable-default")])
def test_estimate_default_model(qtbot, tmp_path, content):
	"""Vérifie les vrais calculs avec le modèle par défaut et l'absence de repli sur le modèle déjà chargé."""
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w._loc_filename = tmp_path / LOC_FILE.name
	shutil.copyfile(LOC_FILE, w._loc_filename)
	original = w._loc_filename.read_bytes()
	w._loc = pd.read_csv(w._loc_filename)
	w._model = pd.read_csv(REF_DIR / MODEL_FILE, index_col=0)
	default = w._model.copy()
	default.iloc[:, 0] += 100
	FileIO.USER_ASTIGMATISM_MODEL.parent.mkdir(parents=True)
	w._model.to_csv(FileIO.USER_ASTIGMATISM_MODEL)
	if content == "valid": default.to_csv(FileIO.DEFAULT_ASTIGMATISM_MODEL)
	elif content is not None: FileIO.DEFAULT_ASTIGMATISM_MODEL.write_text(content, encoding="utf-8")
	w._check_b_estimate.setChecked(False)
	w._check_default_model.setChecked(True)
	assert not w._btn_load_model_estimate.isEnabled()
	assert not w._lbl_model_estimate.isEnabled()
	if content == "valid":
		points = w._loc.loc[:, ["Sigma X", "Sigma Y"]].to_numpy(dtype=float, copy=True)
		expected = w._palm.astigmatism_3d_estimation(points, w._spin_px_estimate.value() * 1000, default.to_numpy(), w._spin_z_estimate.value())
	else: assert w._get_estimation_model().empty
	w._on_estimate()
	if content == "valid":
		actual = pd.read_csv(w._loc_filename)[["Z", "MSE Z"]].to_numpy()
		np.testing.assert_allclose(actual, expected)
	else: assert w._loc_filename.read_bytes() == original
	w._check_default_model.setChecked(False)
	assert w._btn_load_model_estimate.isEnabled()
	assert w._lbl_model_estimate.isEnabled()
	pd.testing.assert_frame_equal(w._get_estimation_model(), w._model)
	w.close()


# ==================================================
# endregion Modèle par défaut
# ==================================================

# ==================================================
# region Estimation axiale
# ==================================================
def test_bad_estimate(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Vérifie le lancement de l'estimation sans fichier chargé."""
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


# --------------------------------------------------
def test_estimate(qtbot, capsys, monkeypatch, fake_qfiledialog, tmp_path):
	"""Vérifie le lancement de l'estimation."""
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	localization_file = tmp_path / LOC_FILE.name
	shutil.copy2(LOC_FILE, localization_file)
	backup_dir = tmp_path / "backup"

	# Chargement du fichier de localisation
	fake_qfiledialog(Astigmatism3DWidget, str(localization_file))
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
	assert "Backup done at" in lines[0]
	assert (backup_dir / "astigmatism_3d_calibration.csv").is_file()

	w.close()


# --------------------------------------------------
def test_estimate_backup(qtbot, capsys, monkeypatch, fake_qfiledialog, tmp_path):
	"""Vérifie le lancement de l'estimation."""
	w = Astigmatism3DWidget()
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	localization_file = tmp_path / LOC_FILE.name
	shutil.copy2(LOC_FILE, localization_file)
	backup_dir = tmp_path / "backup"

	# Chargement du fichier de localisation
	fake_qfiledialog(Astigmatism3DWidget, str(localization_file))
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
	assert "Backup done at" in lines[0]
	assert (backup_dir / "astigmatism_3d_calibration.csv").is_file()

	qtbot.mouseClick(w._btn_estimate, Qt.MouseButton.LeftButton)  # Test de multiple backup
	lines = get_lines_output(capsys)
	assert "Backup done at" in lines[0]
	assert (backup_dir / "astigmatism_3d_calibration_1.csv").is_file()

	qtbot.mouseClick(w._btn_estimate, Qt.MouseButton.LeftButton)  # Test de multiple backup
	lines = get_lines_output(capsys)
	assert "Backup done at" in lines[0]
	assert (backup_dir / "astigmatism_3d_calibration_2.csv").is_file()

	w._check_b_estimate.setChecked(False)  # On recommence sans le backup
	qtbot.mouseClick(w._btn_estimate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Localization file with estimation saved successfully." in lines[0]

	w.close()


# ==================================================
# endregion Estimation axiale
# ==================================================


# ==================================================
# endregion Fonctions de rappel
# ==================================================

# ==================================================
# region Export Plotly hérité
# ==================================================
def test_download(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Vérifie le callback de téléchargement du graphique."""
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

# ==================================================
# endregion Export Plotly hérité
# ==================================================
