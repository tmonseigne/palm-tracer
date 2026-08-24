"""Teste le widget Napari de visualisation 3D des localisations."""

from palm_tracer._tests.Utils import *
from palm_tracer.UI import Viewer3DWidget
from palm_tracer.UI.PALMTracerWidget import SETTINGS_FILE

INPUT_FILE = INPUT_DIR / "stack.tif"
OUTPUT_FOLDER = INPUT_DIR / "stack_PALM_Tracer"


##################################################
def test_widget_creation(make_napari_viewer, patched_napari_viewer, capsys):
	"""Vérifie la création du widget."""
	viewer = make_napari_viewer()  # Créer un viewer à l'aide de la fixture.
	_ = Viewer3DWidget(viewer)  # .	 Créer notre widget, en passant par le viewer.


##################################################
def test_viewer3d(make_napari_viewer, patched_napari_viewer, qtbot, monkeypatch, fake_qfiledialog):
	"""Vérifie la création du widget."""
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = make_napari_viewer()
	my_widget = Viewer3DWidget(viewer)

	fake_qfiledialog(Viewer3DWidget, None)  # .			Simuler un "Cancel" sur le QFileDialog
	my_widget.load_csv()
	assert my_widget.data.empty

	fake_qfiledialog(Viewer3DWidget, "file.csv")  # .	Simuler un fichier inexistant
	my_widget.load_csv()
	assert my_widget.data.empty

	fake_qfiledialog(Viewer3DWidget, f"{INPUT_DIR}/bad_localizations.csv")
	my_widget.load_csv()
	assert my_widget.data.empty

	fake_qfiledialog(Viewer3DWidget, f"{INPUT_DIR}/localizations.csv")
	my_widget.load_csv()
	assert my_widget.data.shape == (6, 18)

	my_widget.load_csv()  # .							Pour recommencer avec un calque déjà actif
	assert my_widget.data.shape == (6, 18)

	my_widget.settings["Remove Outliers"].value = True  # Suppression des outliers
	my_widget.update_layer()

	my_widget.data = pd.DataFrame()
	my_widget.update_layer()  # .						Mise à jour avec un dataframe vide
