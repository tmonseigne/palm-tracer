"""Teste la persistance des dossiers des dialogues Qt."""

import json
from pathlib import Path
from unittest.mock import Mock

import pytest

from palm_tracer.Tools import FileDialog, FileIO


# --------------------------------------------------
@pytest.mark.parametrize("mode", ["single", "multiple", "directory", "save"], ids=["single-file", "multiple-files", "directory", "export"])
def test_dialog_remembers_directory_and_preserves_it_on_cancel(monkeypatch, tmp_path, mode):
	"""Retrouve le dossier sur disque au dialogue suivant, tout en conservant filtres et nom d'export proposé."""
	folder = tmp_path / "selected"
	folder.mkdir()
	filename = str(folder / "data.csv")
	file_filter = "CSV files (*.csv)"
	methods = {"single": "getOpenFileName", "multiple": "getOpenFileNames", "directory": "getExistingDirectory", "save": "getSaveFileName"}
	selected = str(folder) if mode == "directory" else ([filename] if mode == "multiple" else filename, file_filter)
	native_dialog = Mock(return_value=selected)
	monkeypatch.setattr(FileDialog.QFileDialog, methods[mode], native_dialog)

	# --------------------------------------------------
	def select():
		"""Réutilise le même appel avec une sélection validée puis une annulation."""
		if mode == "directory": return FileDialog.open_directory(None, "Select")
		if mode == "save": return FileDialog.save_file(None, "Select", "proposed.csv", file_filter)
		if mode == "multiple": return FileDialog.open_files(None, "Select", file_filter)
		return FileDialog.open_file(None, "Select", file_filter)

	assert select() == selected
	initial_path = Path.home() / "proposed.csv" if mode == "save" else Path.home()
	assert native_dialog.call_args.args[2] == str(initial_path)
	saved = FileIO.USER_UI_STATE_FILE.read_bytes()
	state = json.loads(saved)
	assert state["save" if mode == "save" else "open"] == str(folder.resolve())

	cancelled = "" if mode == "directory" else ([] if mode == "multiple" else "", "")
	native_dialog.return_value = cancelled
	assert select() == cancelled
	expected_path = folder / "proposed.csv" if mode == "save" else folder
	assert native_dialog.call_args.args[2] == str(expected_path)
	assert FileIO.USER_UI_STATE_FILE.read_bytes() == saved


# --------------------------------------------------
def test_open_and_export_directories_are_independent(monkeypatch, tmp_path):
	"""Partage le dossier d'ouverture entre sélections simples et multiples sans le remplacer par celui des exports."""
	inputs, exports = tmp_path / "inputs", tmp_path / "exports"
	inputs.mkdir()
	exports.mkdir()
	monkeypatch.setattr(FileDialog.QFileDialog, "getOpenFileName", Mock(return_value=(str(inputs / "data.csv"), "")))
	monkeypatch.setattr(FileDialog.QFileDialog, "getSaveFileName", Mock(return_value=(str(exports / "graph.png"), "")))
	FileDialog.open_file(None, "Open")
	FileDialog.save_file(None, "Export")
	opening = Mock(return_value=([], ""))
	saving = Mock(return_value=("", ""))
	monkeypatch.setattr(FileDialog.QFileDialog, "getOpenFileNames", opening)
	monkeypatch.setattr(FileDialog.QFileDialog, "getSaveFileName", saving)
	FileDialog.open_files(None, "Open")
	FileDialog.save_file(None, "Export", str(inputs))
	assert opening.call_args.args[2] == str(inputs)
	assert saving.call_args.args[2] == str(exports)


# --------------------------------------------------
@pytest.mark.parametrize("state", ["invalid-json", "wrong-root", "missing-directory"], ids=["invalid-json", "wrong-root", "missing-directory"])
def test_dialog_falls_back_to_home(monkeypatch, tmp_path, state):
	"""Revient au dossier utilisateur lorsque les préférences sont invalides ou désignent un dossier disparu."""
	FileIO.USER_UI_STATE_FILE.parent.mkdir()
	content = {"invalid-json": "{", "wrong-root": "[]", "missing-directory": json.dumps({"open": str(tmp_path / "missing")})}[state]
	FileIO.USER_UI_STATE_FILE.write_text(content, encoding="utf-8")
	dialog = Mock(return_value=("", ""))
	monkeypatch.setattr(FileDialog.QFileDialog, "getOpenFileName", dialog)
	FileDialog.open_file(None, "Open")
	assert dialog.call_args.args[2] == str(Path.home())


# --------------------------------------------------
def test_dialog_returns_selection_when_preferences_cannot_be_saved(monkeypatch, tmp_path):
	"""Conserve la sélection utilisateur lorsque le dossier de configuration ne peut pas être créé."""
	blocked = tmp_path / "blocked"
	blocked.write_text("Not a directory", encoding="utf-8")
	monkeypatch.setattr(FileIO, "USER_UI_STATE_FILE", blocked / "ui_state.json")
	selected = (str(tmp_path / "data.csv"), "CSV files (*.csv)")
	monkeypatch.setattr(FileDialog.QFileDialog, "getOpenFileName", Mock(return_value=selected))
	assert FileDialog.open_file(None, "Open") == selected
