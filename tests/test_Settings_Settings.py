"""Teste l'organisation et la sérialisation des paramètres."""

import copy

import pytest
import tifffile as tiff

from palm_tracer.Settings import Groups as sg
from palm_tracer.Settings import Settings
from palm_tracer.Tools import FileIO
from tests.Utils import *


# ==================================================
# region Initialisation
# ==================================================
def test_settings(qtbot, capsys):
	"""Vérifie la classe (constructeur, getter, setter)."""
	settings = Settings()
	settings.calibration["Pixel Size"].value = 0.32

	dictionary = copy.deepcopy(settings.to_compact_dict())
	settings.reset()
	assert settings.calibration["Pixel Size"].value == 0.16, "Le paramètre n'a pas été remis à sa valeur par défaut."
	settings.update_from_compact_dict(dictionary)
	assert settings.calibration["Pixel Size"].value == 0.32, "Le paramètre n'a pas été correctement enregistré dans le dictionnaire."

	_ = settings.get_ui()
	_ = settings.get_ui()  # Second appel

	print(settings)
	lines = get_lines_output(capsys)
	assert len(lines) == 134


# --------------------------------------------------
@pytest.mark.parametrize("mode, selected, expected", [
		pytest.param(0, 0, 3, id="first-stack"),
		pytest.param(0, 1, 5, id="selected-stack"),
		pytest.param(1, 0, 5, id="separate-files-max"),
		pytest.param(2, 1, 8, id="all-in-one")])
def test_settings_batch_filter_limits(qtbot, tmp_path, mode, selected, expected):
	"""Vérifie les bornes des filtres selon le fichier et le mode du lot."""
	files = [tmp_path / "first.tif", tmp_path / "second.tif"]
	for path, depth in zip(files, (3, 5)):
		tiff.imwrite(path, np.zeros((depth, 4, 4), dtype=np.uint16), photometric="minisblack")

	settings = Settings()
	settings.batch["Files"].items = [str(path) for path in files]
	settings.batch["Files"].value = selected
	settings.batch["Mode"].value = mode
	assert settings.filters["Plane"].limits[1] == expected
	assert settings.filters.tracking["Length"].limits[1] == expected


# --------------------------------------------------
def test_settings_batch_filter_limits_after_list_change(qtbot, tmp_path):
	"""Vérifie le re-calcul quand la liste change sans changer l'index courant."""
	files = [tmp_path / "first.tif", tmp_path / "second.tif"]
	for path, depth in zip(files, (3, 5)):
		tiff.imwrite(path, np.zeros((depth, 4, 4), dtype=np.uint16), photometric="minisblack")

	settings = Settings()
	settings.batch["Files"].items = [str(files[0])]
	settings.batch["Mode"].value = 2
	assert settings.filters["Plane"].limits[1] == 3

	settings.batch["Files"].items = [str(path) for path in files]
	assert settings.filters["Plane"].limits[1] == 8
	assert settings.filters.tracking["Length"].limits[1] == 8

	settings.batch["Files"].clear_files()
	assert settings.filters["Plane"].limits[1] == 100000


# --------------------------------------------------
def test_settings_batch_reuses_tif_metadata(qtbot, tmp_path, monkeypatch):
	"""Vérifie que le changement de mode réutilise les profondeurs déjà lues."""
	files = [tmp_path / "first.tif", tmp_path / "second.tif"]
	for path, depth in zip(files, (3, 5)):
		tiff.imwrite(path, np.zeros((depth, 4, 4), dtype=np.uint16), photometric="minisblack")

	read_shape = FileIO.read_tif_shape
	read_paths = []

	# --------------------------------------------------
	def count_read(p):
		"""Compte les lectures de métadonnées TIFF."""
		read_paths.append(str(p))
		return read_shape(p)

	monkeypatch.setattr(FileIO, "read_tif_shape", count_read)
	settings = Settings()
	settings.batch["Files"].items = [str(path) for path in files]
	settings.batch["Mode"].value = 2
	settings.batch["Mode"].value = 0
	settings.batch["Files"].value = 1
	settings.batch["Mode"].value = 2

	assert read_paths == [str(path) for path in files]
	assert settings.filters["Plane"].limits[1] == 8


# ==================================================
# endregion Initialisation
# ==================================================

# ==================================================
# region Accesseurs
# ==================================================
@pytest.mark.parametrize("attribute, group_type", [
		pytest.param("batch", sg.Batch, id="batch"), pytest.param("calibration", sg.Calibration, id="calibration"),
		pytest.param("localization", sg.Localization, id="localization"), pytest.param("beads", sg.BeadsExtraction, id="beads"),
		pytest.param("tracking", sg.Tracking, id="tracking"), pytest.param("blinking", sg.BlinkingReconnection, id="blinking"),
		pytest.param("track_analysis", sg.TrackAnalysis, id="track-analysis"), pytest.param("gallery", sg.Gallery, id="gallery"),
		pytest.param("graph", sg.Graph, id="graph"), pytest.param("hr", sg.HR, id="high-resolution"), pytest.param("filters", sg.Filters, id="filters")])
def test_settings_group_getter(qtbot, attribute, group_type):
	"""Vérifie que chaque accesseur renvoie le groupe de paramètres attendu."""
	assert isinstance(getattr(Settings(), attribute), group_type), "Récupération du groupe incorrecte."


# ==================================================
# endregion Accesseurs
# ==================================================

# ==================================================
# region Signaux
# ==================================================
def test_settings_signal(qtbot):
	"""Vérifie Connexion d'un slot Python, blocage et émission."""
	settings = Settings()

	received: list[Any] = []
	settings.connect(lambda v: received.append(v))
	with settings.signal_blocked(): pass
	settings.disconnect()

# ==================================================
# endregion Signaux
# ==================================================
