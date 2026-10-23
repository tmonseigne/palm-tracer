"""Teste la représentation Qt des résultats de PALMTracer."""

import pytest
from qtpy.QtWidgets import QFormLayout, QLabel

from palm_tracer.UI.ResultsUI import _STATUS_TOOLTIPS, ResultsUI


# --------------------------------------------------
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
		assert value is ui.labels[key]
		assert value.text() == ("No" if key == "File" else "0")

	button_item = ui.layout.itemAt(len(_STATUS_TOOLTIPS), QFormLayout.ItemRole.SpanningRole)
	assert button_item.widget() is ui.open_folder_button
	assert ui.open_folder_button.text() == "Open results folder"
	assert not ui.open_folder_button.isEnabled()


# --------------------------------------------------
def test_update_status(qtbot):
	"""Vérifie la mise à jour complète, partielle et avec une clé inconnue."""
	ui = ResultsUI()
	qtbot.addWidget(ui.widget)
	status = {key: (f"Status {index}", f"Tooltip {index}") for index, key in enumerate(_STATUS_TOOLTIPS)}

	ui.update_status(status)
	for key, (expected, tooltip) in status.items():
		assert ui.labels[key].text() == expected
		assert ui.labels[key].toolTip() == tooltip

	ui.update_status({"File": ("stack.tif", "stack.tif"), "Unknown": ("Ignored", "Ignored")})
	assert ui.labels["File"].text() == "stack.tif"
	assert ui.labels["Localizations"].text() == status["Localizations"][0]
	assert "Unknown" not in ui.labels
	assert ui.labels["File"].toolTip() == "stack.tif"


# --------------------------------------------------
@pytest.mark.parametrize("category, expected, tooltip", [
		pytest.param("Localizations", "1\u00a0234", "1\u00a0234 localizations", id="localizations"),
		pytest.param("Beads", "12", "12 beads", id="beads"),
		pytest.param("Tracks", "500/2\u00a0000",
					 "500/2\u00a0000 tracks\n25.00% retained; 75.00% filtered out.", id="filtered-tracks"),
		pytest.param("Tracks Reconnected", "500/2\u00a0000",
					 "500/2\u00a0000 reconnected tracks\n25.00% retained; 75.00% filtered out.", id="filtered-reconnected-tracks"),
		pytest.param("Tracks Reconnected", "12", "12 reconnected tracks", id="reconnected-tracks")])
def test_update_status_counts_and_tooltip(qtbot, category, expected, tooltip):
	"""Vérifie le compteur compact, les détails en infobulle et leur réinitialisation lorsque le résultat est vidé."""
	ui = ResultsUI()
	qtbot.addWidget(ui.widget)
	ui.update_status({category: (expected, tooltip)})
	assert ui.labels[category].text() == expected
	assert ui.labels[category].toolTip() == tooltip
	ui.update_status({category: ("0", "No result")})
	assert ui.labels[category].text() == "0"
	assert ui.labels[category].toolTip() == "No result"


# --------------------------------------------------
@pytest.mark.parametrize("filename", [
		pytest.param("stack.tif", id="tiff-file"),
		pytest.param("stack.ome.tif", id="multiple-suffixes"),
		pytest.param("stack", id="no-extension")])
def test_file_display(qtbot, tmp_path, filename):
	"""Vérifie le nom seul à l'affichage et le chemin complet dans l'infobulle, puis leur réinitialisation."""
	ui = ResultsUI()
	qtbot.addWidget(ui.widget)
	full_path = str(tmp_path / filename)

	ui.update_status({"File": (filename, full_path)})
	assert ui.labels["File"].text() == filename
	assert ui.labels["File"].toolTip() == full_path

	ui.update_status({"File": ("No File", "")})
	assert ui.labels["File"].text() == "No File"
	assert ui.labels["File"].toolTip() == ""


# --------------------------------------------------
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
	assert ui.open_folder_button.isEnabled()
	assert ui.open_folder_button.toolTip() == str(tmp_path)

	path = None
	if path_kind == "existing": path = tmp_path
	elif path_kind == "missing": path = tmp_path / "missing"
	elif path_kind == "file":
		path = tmp_path / "results.txt"
		path.write_text("", encoding="utf-8")

	ui.update_results_folder(path)

	assert ui.open_folder_button.isEnabled() == (path_kind == "existing")
	assert ui.open_folder_button.toolTip() == (str(path) if path is not None else "")
