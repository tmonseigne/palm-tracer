"""Teste la représentation Qt des résultats de PALMTracer."""

from qtpy.QtWidgets import QFormLayout, QLabel

from palm_tracer.UI.ResultsUI import _STATUS_TOOLTIPS, ResultsUI


##################################################
def test_creation(qtbot):
	"""Vérifie la construction du groupe et de chacune de ses lignes."""
	ui = ResultsUI(title="Test Results", space=7, margin=9)
	qtbot.addWidget(ui.widget)

	assert ui.widget.title() == "Test Results"
	assert ui.layout.rowCount() == len(_STATUS_TOOLTIPS)
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
