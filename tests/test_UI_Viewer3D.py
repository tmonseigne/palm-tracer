"""Teste le widget Napari de visualisation 3D des localisations."""

from unittest.mock import Mock

import pytest
from napari.components import ViewerModel

from palm_tracer.UI import Viewer3DWidget
from tests.Utils import *
from tests.Utils import send_file_drop


# --------------------------------------------------
def test_widget_creation(qtbot):
	"""Vérifie la création du widget."""
	viewer = ViewerModel(ndisplay=3)
	w = Viewer3DWidget(viewer)
	qtbot.addWidget(w)


# --------------------------------------------------
def test_viewer3d_drop_loads_localizations(qtbot, tmp_path):
	"""Vérifie le chargement du CSV déposé et l'actualisation du calque 3D."""
	widget = Viewer3DWidget(ViewerModel(ndisplay=3))
	qtbot.addWidget(widget)
	data = pd.DataFrame({"X": [1.0], "Y": [2.0], "Z": [3.0], "Integrated Intensity": [100.0]})
	path = tmp_path / "localizations.CSV"
	data.to_csv(path, index=False)

	widget.show()
	send_file_drop(widget, [path])

	pd.testing.assert_frame_equal(widget.data, data)
	assert widget.layer.data.shape == (1, 3)


# --------------------------------------------------
@pytest.mark.parametrize("error_type", [OSError, ValueError], ids=["read-error", "parse-error"])
def test_load_csv_clears_data_after_read_error(qtbot, tmp_path, monkeypatch, error_type):
	"""Vide les anciennes données et signale l'erreur sans actualiser le calque après une lecture impossible."""
	widget = Viewer3DWidget(ViewerModel(ndisplay=3))
	qtbot.addWidget(widget)
	widget.data = pd.DataFrame({"X": [1.0], "Y": [2.0], "Z": [3.0], "Integrated Intensity": [100.0]})
	notify, update_layer = Mock(), Mock()
	monkeypatch.setattr(widget, "notify_warning", notify)
	monkeypatch.setattr(widget, "update_layer", update_layer)
	monkeypatch.setattr(pd, "read_csv", Mock(side_effect=error_type("CSV unavailable")))

	widget._load_csv(str(tmp_path / "data.csv"))

	assert widget.data.empty
	notify.assert_called_once_with("Unable to read the CSV file: CSV unavailable.")
	update_layer.assert_not_called()


# --------------------------------------------------
def test_viewer3d(qtbot, fake_qfiledialog):
	"""Vérifie la création du widget."""
	# Création du viewer et du widget avec la configuration utilisateur isolée par la fixture commune.
	viewer = ViewerModel(ndisplay=3)
	my_widget = Viewer3DWidget(viewer)
	qtbot.addWidget(my_widget)

	# Annulation et fichiers invalides : aucune donnée ne doit être chargée.
	fake_qfiledialog(Viewer3DWidget, None)  # .			Simuler un "Cancel" sur le QFileDialog
	my_widget.load_csv()
	assert my_widget.data.empty

	fake_qfiledialog(Viewer3DWidget, "file.csv")  # .	Simuler un fichier inexistant
	my_widget.load_csv()
	assert my_widget.data.empty

	fake_qfiledialog(Viewer3DWidget, f"{INPUT_DIR}/bad_localizations.csv")
	my_widget.load_csv()
	assert my_widget.data.empty

	# Chargement valide, puis rechargement avec un calque déjà présent.
	fake_qfiledialog(Viewer3DWidget, f"{INPUT_DIR}/localizations.csv")
	my_widget.load_csv()
	assert my_widget.data.shape == (6, 18)

	my_widget.load_csv()  # .							Pour recommencer avec un calque déjà actif
	assert my_widget.data.shape == (6, 18)

	# Actualisation du calque après filtrage, puis avec un tableau vide.
	my_widget.settings["Remove Outliers"].value = True  # Suppression des outliers
	my_widget.update_layer()

	my_widget.data = pd.DataFrame()
	my_widget.update_layer()  # .						Mise à jour avec un DataFrame vide
