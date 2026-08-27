"""Teste la gestion des résultats de PALMTracer."""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from palm_tracer.Results import Results
from palm_tracer.Tools import FileIO


##################################################
def make_dataframe(row_count: int) -> pd.DataFrame:
	"""
	Construit un DataFrame minimal contenant le nombre de lignes demandé.

	:param row_count: Nombre de lignes à créer.
	:return: DataFrame construit.
	"""
	return pd.DataFrame(np.arange(row_count), columns=["Value"])


##################################################
@pytest.fixture
def results() -> Results:
	"""Retourne un conteneur de résultats vide."""
	return Results()


##################################################
def test_accessors(results, tmp_path):
	"""Vérifie les accès aux résultats et la génération des noms de fichiers."""
	expected_keys = ["loc", "dft", "bds", "trc", "blk", "MSD", "InD", "Fit",
					 "f_loc", "f_dft", "f_trc", "f_blk", "f_MSD", "f_InD", "f_Fit"]

	assert list(results) == expected_keys, "Les clés des résultats ne sont pas valides."

	data = make_dataframe(2)
	results["loc"] = data
	assert results["loc"] is data, "Le DataFrame retourné doit être celui affecté."

	assert results.stack_name == "", "Le nom de pile initial doit être vide."
	results.stack_name = "stack.tif"
	assert results.stack_name == "stack.tif", "Le nom de pile n'a pas été mémorisé."

	expected = tmp_path.resolve() / "localizations-20260827_120000.csv"
	assert results.output_name("localizations", tmp_path, "20260827_120000") == expected
	assert results.output_name_by_key("loc", tmp_path, "20260827_120000") == expected
	assert results.output_name("settings", tmp_path, "20260827_120000", "json") == tmp_path.resolve() / "settings-20260827_120000.json"


##################################################
def test_active_results(results):
	"""Vérifie les priorités de sélection des différentes variantes de résultats."""
	assert results.get_localization_key() == "loc"
	assert results.localizations is results["loc"]
	for key in ("loc", "f_loc", "dft", "f_dft"):
		results._data[key] = make_dataframe(1)
		assert results.get_localization_key() == key, f"La clé de localisation active devrait être '{key}'."
		assert results.localizations is results[key]

	assert results.get_tracks_key() == "trc"
	assert results.tracks is results["trc"]
	for key in ("trc", "f_trc", "blk", "f_blk"):
		results._data[key] = make_dataframe(1)
		assert results.get_tracks_key() == key, f"La clé de trajectoires active devrait être '{key}'."
		assert results.tracks is results[key]

	assert results.get_tracks_compute_key() == ["MSD", "InD", "Fit"]
	results._data["f_MSD"] = make_dataframe(1)
	results._data["f_Fit"] = make_dataframe(1)
	assert results.get_tracks_compute_key() == ["f_MSD", "InD", "f_Fit"]
	assert results.tracks_compute == {
			"MSD": results["f_MSD"],
			"InD": results["InD"],
			"Fit": results["f_Fit"],
			}

	results._data["bds"] = make_dataframe(1)
	assert results.beads is results["bds"]


##################################################
@pytest.mark.parametrize(
		("original_count", "filtered_count", "prefix", "expected"),
		[
				(0, 0, "", "No"),
				(2, 0, "", "Yes (2 tracks)"),
				(2, 2, "", "Yes (2 tracks)"),
				(2, 1, "", "Yes Filtered (1/2 tracks)"),
				(2, 1, "Reconnected", "Yes Reconnected Filtered (1/2 tracks)"),
				],
		)
def test_dataframe_status(original_count, filtered_count, prefix, expected):
	"""Vérifie chaque forme de statut individuel."""
	status = Results.get_df_status(make_dataframe(original_count), make_dataframe(filtered_count), "tracks", prefix)
	assert status == expected, f"Statut incorrect.\nAttendu : {expected}\nObtenu : {status}"


##################################################
def test_status(results):
	"""Vérifie exactement l'ensemble des statuts dans chaque configuration."""
	expected = {
			"File":          "No File",
			"Localizations": "No",
			"Beads":         "No",
			"Tracks":        "No",
			"MSD":           "No",
			"Instant D":     "No",
			"MSD Fit":       "No",
			}
	assert results.get_status() == expected

	results._stack_name = "stack.tif"
	for key in ("loc", "bds", "trc", "blk", "MSD", "InD", "Fit"):
		results._data[key] = make_dataframe(1)
	for key in ("f_loc", "f_trc", "f_blk", "f_MSD", "f_InD", "f_Fit"):
		results._data[key] = make_dataframe(2)

	expected = {
			"File":          "stack.tif",
			"Localizations": "Yes Filtered (2/1 localizations)",
			"Beads":         "Yes (1 localizations)",
			"Tracks":        "Yes Reconnected Filtered (2/1 tracks)",
			"MSD":           "Yes Filtered (2/1 tracks)",
			"Instant D":     "Yes Filtered (2/1 tracks)",
			"MSD Fit":       "Yes Filtered (2/1 tracks)",
			}
	assert results.get_status() == expected

	results._data["f_blk"] = pd.DataFrame()
	expected["Tracks"] = "Yes Reconnected (1 tracks)"
	assert results.get_status() == expected

	for key in ("f_loc", "f_trc", "f_MSD", "f_InD", "f_Fit"):
		results._data[key] = pd.DataFrame()
	results._data["blk"] = pd.DataFrame()
	expected = {
			"File":          "stack.tif",
			"Localizations": "Yes (1 localizations)",
			"Beads":         "Yes (1 localizations)",
			"Tracks":        "Yes (1 tracks)",
			"MSD":           "Yes (1 tracks)",
			"Instant D":     "Yes (1 tracks)",
			"MSD Fit":       "Yes (1 tracks)",
			}
	assert results.get_status() == expected


##################################################
def test_reset(results):
	"""Vérifie les réinitialisations partielles et complète des résultats."""
	for key in results:
		results._data[key] = make_dataframe(1)

	results.reset_filtered()
	for key in results:
		if key.startswith("f_"):
			assert results[key].empty, f"Le résultat filtré '{key}' devrait être vide."
		else:
			assert not results[key].empty, f"Le résultat original '{key}' devrait être conservé."

	results.reset()
	assert all(results[key].empty for key in results), "Tous les résultats devraient être vides."


##################################################
def test_load(results, tmp_path, monkeypatch, capsys):
	"""Vérifie le chargement d'un fichier, une absence et une erreur de lecture."""
	timestamp = "20260827_120000"
	results.KEYS_TO_FILE = {"loc": "localizations", "bds": "beads", "trc": "tracking"}
	localizations = make_dataframe(2)
	localizations.to_csv(results.output_name_by_key("loc", tmp_path, timestamp), index=False)
	make_dataframe(1).to_csv(results.output_name_by_key("bds", tmp_path, timestamp), index=False)

	real_read_csv = pd.read_csv

	def fake_read_csv(path, *args, **kwargs):
		"""Simule une erreur limitée au fichier de billes."""
		if Path(path).name.startswith("beads-"):
			raise ValueError("invalid beads file")
		return real_read_csv(path, *args, **kwargs)

	monkeypatch.setattr(pd, "read_csv", fake_read_csv)
	results._data["Fit"] = make_dataframe(1)
	results.load("stack.tif", tmp_path, timestamp)

	assert results.stack_name == "stack.tif"
	assert_frame_equal(results["loc"], localizations)
	assert results["bds"].empty
	assert results["trc"].empty
	assert results["Fit"].empty, "Le chargement doit commencer par réinitialiser les anciens résultats."

	output = capsys.readouterr().out
	assert f"Loading files from the '{str(tmp_path.resolve())}' folder with the timestamp {timestamp}." in output
	assert "File 'localizations' loaded successfully." in output
	assert "Error loading file 'beads': invalid beads file" in output
	assert "File 'tracking' not found." in output


##################################################
def test_save(results, tmp_path, monkeypatch):
	"""Vérifie l'enregistrement individuel et celui des résultats filtrés utiles."""
	timestamp = "20260827_120000"
	results._data["loc"] = make_dataframe(3)
	results.save("loc", tmp_path, timestamp)
	filename = results.output_name_by_key("loc", tmp_path, timestamp)
	assert filename.is_file()
	assert_frame_equal(pd.read_csv(filename), results["loc"])

	results._data["f_loc"] = make_dataframe(2)
	results._data["trc"] = make_dataframe(1)
	results._data["f_trc"] = make_dataframe(1)
	results.save_filtered(tmp_path, timestamp)
	assert results.output_name_by_key("f_loc", tmp_path, timestamp).is_file()
	assert not results.output_name_by_key("f_trc", tmp_path, timestamp).exists()

	automatic_timestamp = "20260827_130000"
	monkeypatch.setattr(FileIO, "get_timestamp_for_files", lambda: automatic_timestamp)
	results.save_filtered(tmp_path)
	assert results.output_name_by_key("f_loc", tmp_path, automatic_timestamp).is_file()


##################################################
def test_interfaces(results, qtbot):
	"""Vérifie la création, la réutilisation et la synchronisation des interfaces."""
	first_ui = results.get_ui("first", margin=7)
	second_ui = results.get_ui("second")
	qtbot.addWidget(first_ui.widget)
	qtbot.addWidget(second_ui.widget)

	assert results.get_ui("first") is first_ui, "Une interface existante doit être réutilisée."
	assert first_ui.margin == 7

	results.stack_name = "stack.tif"
	results["loc"] = make_dataframe(2)
	for ui in (first_ui, second_ui):
		assert ui._labels["File"].text() == "stack.tif"
		assert ui._labels["Localizations"].text() == "Yes (2 localizations)"

	results.clean_ui("first")
	results.clean_ui("unknown")
	replacement_ui = results.get_ui("first")
	qtbot.addWidget(replacement_ui.widget)
	assert replacement_ui is not first_ui, "Une interface nettoyée doit être recréée."
