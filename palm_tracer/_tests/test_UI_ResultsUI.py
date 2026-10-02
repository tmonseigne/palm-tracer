"""Teste la représentation Qt des résultats de PALMTracer."""

import pytest
from qtpy.QtWidgets import QFormLayout, QLabel

from palm_tracer.UI.ResultsUI import _STATUS_TOOLTIPS, ResultsUI


##################################################
def test_creation(qtbot):
	"""Vérifie la construction du groupe et de chacune de ses lignes."""
	ui = ResultsUI(title="Test Results", space=7, margin=9)
	qtbot.addWidget(ui.widget)

	assert ui.widget.title() == "Test Results"
	assert ui.layout.rowCount() == len(_STATUS_TOOLTIPS) + 1
	assert ui.layout.spacing() == 7
	margins = ui.layout.contentsMargins()
	assert (margins.left(), margins.top(), margins.right(), margins.bottom()) == (9, 9, 9, 9)

	for row, (key, tooltip) in enumerate(_STATUS_TOOLTIPS.items()):
		label_item = ui.layout.itemAt(row, QFormLayout.ItemRole.LabelRole)
		field_item = ui.layout.itemAt(row, QFormLayout.ItemRole.FieldRole)
		label = label_item.widget()
		field_layout = field_item.layout()
		value = field_layout.itemAt(0).widget()

		assert isinstance(label, QLabel)
		assert label.text() == f"{key}: "
		assert label.toolTip() == tooltip
		assert value is ui._labels[key]
		assert value.text() == "No"

	button_item = ui.layout.itemAt(len(_STATUS_TOOLTIPS), QFormLayout.ItemRole.SpanningRole)
	assert button_item.widget() is ui._open_folder_button
	assert ui._open_folder_button.text() == "Open results folder"
	assert not ui._open_folder_button.isEnabled()


##################################################
def test_update_status(qtbot):
	"""Vérifie la mise à jour complète, partielle et avec une clé inconnue."""
	ui = ResultsUI()
	qtbot.addWidget(ui.widget)
	status = {key: f"Status {index}" for index, key in enumerate(_STATUS_TOOLTIPS)}

	ui.update_status(status)
	for key, expected in status.items():
		assert ui._labels[key].text() == expected

	ui.update_status({"File": "stack.tif", "Unknown": "Ignored"})
	assert ui._labels["File"].text() == "stack.tif"
	assert ui._labels["Localizations"].text() == status["Localizations"]
	assert "Unknown" not in ui._labels
	assert ui._labels["File"].toolTip() == "stack.tif"


##################################################
@pytest.mark.parametrize("filename", [
		pytest.param("stack.tif", id="tiff-file"),
		pytest.param("stack.ome.tif", id="multiple-suffixes"),
		pytest.param("stack", id="no-extension")])
def test_file_display(qtbot, tmp_path, filename):
	"""Vérifie le nom seul à l'affichage et le chemin complet dans l'infobulle, puis leur réinitialisation."""
	ui = ResultsUI()
	qtbot.addWidget(ui.widget)
	full_path = str(tmp_path / filename)

	ui.update_status({"File": full_path})
	assert ui._labels["File"].text() == filename
	assert ui._labels["File"].toolTip() == full_path

	ui.update_status({"File": "No File"})
	assert ui._labels["File"].text() == "No File"
	assert ui._labels["File"].toolTip() == ""


##################################################
@pytest.mark.parametrize("path_kind", [
		pytest.param("existing", id="existing-folder"),
		pytest.param("missing", id="missing-folder"),
		pytest.param("file", id="file-instead-of-folder"),
		pytest.param("unset", id="unset-folder")])
def test_update_results_folder(qtbot, tmp_path, path_kind):
	"""Vérifie la disponibilité et l'infobulle du bouton, y compris après un dossier valide."""
	ui = ResultsUI()
	qtbot.addWidget(ui.widget)
	ui.update_results_folder(tmp_path)
	assert ui._open_folder_button.isEnabled()
	assert ui._open_folder_button.toolTip() == str(tmp_path)

	path = None
	if path_kind == "existing": path = tmp_path
	elif path_kind == "missing": path = tmp_path / "missing"
	elif path_kind == "file":
		path = tmp_path / "results.txt"
		path.write_text("", encoding="utf-8")

	ui.update_results_folder(path)

	assert ui._open_folder_button.isEnabled() == (path_kind == "existing")
	assert ui._open_folder_button.toolTip() == (str(path) if path is not None else "")
