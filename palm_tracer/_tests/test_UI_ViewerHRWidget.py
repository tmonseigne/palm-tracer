"""Fichier des tests pour le widget."""
import shutil

from qtpy.QtCore import Qt

from palm_tracer._tests.Utils import *
from palm_tracer.UI import ViewerHRWidget

INPUT_FILE = INPUT_DIR / "stack.tif"
OUTPUT_FOLDER = INPUT_DIR / "stack_PALM_Tracer"


##################################################
def get_pt():
	"""Instance basique de PALMTracer pour chaque test."""
	pt = PALMTracer()
	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.update_box([f"{INPUT_DIR / 'stack.tif'}"])
	pt.df["loc"] = pd.read_csv(INPUT_DIR / "localizations.csv")
	pt.df["f_loc"] = pt.df["loc"].copy()
	pt.df["trc"] = pd.read_csv(INPUT_DIR / "tracking.csv")
	pt.df["f_trc"] = pt.df["trc"].copy()
	pt.df["blk"] = pt.df["trc"].copy()
	pt.df["f_blk"] = pt.df["trc"].copy()
	pt.df["MSD"] = pd.read_csv(INPUT_DIR / "tracking_MSD.csv")
	pt.df["InD"] = pd.read_csv(INPUT_DIR / "tracking_InstantD.csv")
	pt.df["Fit"] = pd.read_csv(INPUT_DIR / "tracking_Fit.csv")
	return pt


##################################################
def test_widget_creation(make_napari_viewer, patched_napari_viewer, capsys):
	"""Test basique de création du widget."""
	viewer = make_napari_viewer()  # .				Créer un viewer à l'aide de la fixture.
	w = ViewerHRWidget(viewer, get_pt())  # Créer notre widget, en passant par le viewer.


##################################################
def test_add_stack(make_napari_viewer, patched_napari_viewer, qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Test basique du widget."""
	viewer = make_napari_viewer()  # .		  Créer un viewer à l'aide de la fixture.
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
	pt = PALMTracer()
	w = ViewerHRWidget(viewer, pt)  # Créer notre widget, en passant par le viewer.

	fake_qfiledialog(FileList, f"{INPUT_DIR / 'stack.tif'}")
	qtbot.mouseClick(w._btn_add_stack, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "No valid settings file to load." in lines[0]


##################################################
def test_change_source(make_napari_viewer, patched_napari_viewer, qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Test basique du widget."""
	viewer = make_napari_viewer()  # .				Créer un viewer à l'aide de la fixture.
	w = ViewerHRWidget(viewer, get_pt())  # Créer notre widget, en passant par le viewer.

	assert w._cmb_src.items[0] == "Count"

	qtbot.mouseClick(w._btn_src["Tracks"], Qt.MouseButton.LeftButton)
	assert w._cmb_src.items[0] == "Track Number"

	qtbot.mouseClick(w._btn_src["Localization"], Qt.MouseButton.LeftButton)
	assert w._cmb_src.items[0] == "Count"


##################################################
def test_actualize(make_napari_viewer, patched_napari_viewer, qtbot, capsys):
	"""Test basique du widget."""
	viewer = make_napari_viewer()  # .					Créer un viewer à l'aide de la fixture.
	w = ViewerHRWidget(viewer, PALMTracer())  # Créer notre widget, en passant par le viewer.

	qtbot.mouseClick(w._btn_actualize, Qt.MouseButton.LeftButton)

	w._pt._stack = np.zeros((1, 1, 1), dtype=np.uint16)
	qtbot.mouseClick(w._btn_actualize, Qt.MouseButton.LeftButton)


##################################################
def test_reset_filtered(make_napari_viewer, patched_napari_viewer, qtbot, capsys):
	"""Test basique de création du widget."""

	viewer = make_napari_viewer()  # .				Créer un viewer à l'aide de la fixture.
	w = ViewerHRWidget(viewer, get_pt())  # Créer notre widget, en passant par le viewer.

	assert w._status["Localization"].text() == "Yes (Filtered)", "Status Incorrect."
	qtbot.mouseClick(w._filters.buttons["reset"], Qt.MouseButton.LeftButton)
	assert w._status["Localization"].text() == "Yes", "Status Incorrect."


##################################################
def test_update_filtered(make_napari_viewer, patched_napari_viewer, qtbot, capsys):
	"""Test basique de création du widget."""

	viewer = make_napari_viewer()  # .				Créer un viewer à l'aide de la fixture.
	w = ViewerHRWidget(viewer, get_pt())  # Créer notre widget, en passant par le viewer.

	qtbot.mouseClick(w._filters.buttons["reset"], Qt.MouseButton.LeftButton)
	assert w._status["Localization"].text() == "Yes", "Status Incorrect."  # .			On n'a pas de tableaux filtrés

	# Changement des valeurs
	ref = w._filters["Plane"].value
	new_f = [2, 50]
	w._filters["Plane"].value = new_f
	w._filters["Plane"].active = True
	assert w._filters["Plane"].value == new_f, "Filtre incorrect."
	assert w._pt.settings.filtering["Plane"].value == ref, "Filtre incorrect."  # .		Il n'est pas encore à jour.

	qtbot.mouseClick(w._filters.buttons["update"], Qt.MouseButton.LeftButton)

	assert w._pt.settings.filtering["Plane"].value == new_f  # .						Il a été mis à jour
	assert w._status["Localization"].text() == "Yes (Filtered)", "Status Incorrect."  # On a à nouveau un tableau filtré.


##################################################
def test_save(make_napari_viewer, patched_napari_viewer, qtbot, capsys):
	"""Test basique de création du widget."""
	res = OUTPUT_DIR / "HR.png"
	res.unlink(missing_ok=True)  # .				Suppression du fichier de résultat s'il existe.

	viewer = make_napari_viewer()  # .				Créer un viewer à l'aide de la fixture.
	w = ViewerHRWidget(viewer, get_pt())  # Créer notre widget, en passant par le viewer.

	w._filename = ""
	qtbot.mouseClick(w._btn_save, Qt.MouseButton.LeftButton)  # Il ne fait rien si pas de nom de fichier.
	w._filename = str(res.resolve())
	qtbot.mouseClick(w._btn_save, Qt.MouseButton.LeftButton)
	assert res.exists(), "File not saved."


##################################################
def test_generate(make_napari_viewer, patched_napari_viewer, qtbot, capsys, monkeypatch, fake_qfiledialog, fake_napari_layers):
	"""Test basique de création du widget."""
	viewer = make_napari_viewer()  # .		  Créer un viewer à l'aide de la fixture.
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
	pt = PALMTracer()
	w = ViewerHRWidget(viewer, pt)  # Créer notre widget, en passant par le viewer.

	fake_napari_layers(viewer)

	# palm tracer n'est pas initialisé
	qtbot.mouseClick(w._btn_generate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "WARNING: No stack processed loaded." in lines[0]

	# Chargement d'une pile, mais aucun process
	fake_qfiledialog(FileList, f"{INPUT_DIR / 'stack.tif'}")
	qtbot.mouseClick(w._btn_add_stack, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "No valid settings file to load." in lines[0]

	# Idem aucune pile de chargée (car il n'a pas eu de process précédent)
	qtbot.mouseClick(w._btn_generate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "WARNING: No stack processed loaded." in lines[0]

	# Un process, mais aucun tableau d'exploitable.
	w._pt.process()  # Process Vide pour créer le dossier et un setting de base
	_ = get_lines_output(capsys)
	qtbot.mouseClick(w._btn_generate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "WARNING: No localization file available." in lines[0]

	# Ajout d'un tableau de localisation
	pt.df["loc"] = pd.read_csv(INPUT_DIR / "localizations.csv")
	qtbot.mouseClick(w._btn_generate, Qt.MouseButton.LeftButton)

	# Passage au suivi sans tableau
	qtbot.mouseClick(w._btn_src["Tracks"], Qt.MouseButton.LeftButton)
	qtbot.mouseClick(w._btn_generate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "WARNING: No tracking file available." in lines[-1]  # dernière ligne, car il peut y avoir un warning lors de la suppression des calques

	# Ajout d'un tableau de Suivi
	pt.df["trc"] = pd.read_csv(INPUT_DIR / "tracking.csv")
	qtbot.mouseClick(w._btn_generate, Qt.MouseButton.LeftButton)


##################################################
def test_generate_drift(make_napari_viewer, patched_napari_viewer, qtbot, capsys, monkeypatch, fake_qfiledialog, fake_napari_layers):
	"""Test basique de création du widget."""
	viewer = make_napari_viewer()  # .		  Créer un viewer à l'aide de la fixture.
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
	pt = PALMTracer()
	w = ViewerHRWidget(viewer, pt)  # Créer notre widget, en passant par le viewer.

	fake_napari_layers(viewer)

	# Chargement d'une pile
	fake_qfiledialog(FileList, f"{INPUT_DIR / 'stack.tif'}")
	qtbot.mouseClick(w._btn_add_stack, Qt.MouseButton.LeftButton)
	w._drift.value = True
	w._pt.process()  # Process Vide pour créer le dossier et un setting de base

	# Sans localization la sortie sera entièrement noire.
	qtbot.mouseClick(w._btn_generate, Qt.MouseButton.LeftButton)
	upscale = w.upscale_spin.value
	shape = (128 * upscale, 256 * upscale)
	ref = np.zeros(shape)
	np.allclose(ref, w.visualization)

	# Sortie avec le fichier de localisation, mais pas de billes.
	pt.df["loc"] = pd.read_csv(INPUT_DIR / "localizations.csv")
	_ = get_lines_output(capsys)  # Nettoyage de la sortie
	qtbot.mouseClick(w._btn_generate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "WARNING: No beads file available to correct drift." in lines[0]  # dernière ligne, car il peut y avoir un warning lors de la suppression des calques

	ref = np.zeros(shape)
	ref[4, 2] = 2
	ref[6, 4] = 2
	ref[8, 6] = 1
	ref[10, 8] = 1
	np.allclose(ref, w.visualization)

	# Sortie avec le fichier de localisation et un fichier de billes.
	pt.df["bds"] = pd.read_csv(INPUT_DIR / "beads.csv")
	qtbot.mouseClick(w._btn_generate, Qt.MouseButton.LeftButton)

	ref = np.zeros(shape)
	ref[2, 1] = 1
	ref[4, 2] = 1
	ref[6, 4] = 2
	ref[8, 6] = 1
	ref[10, 8] = 1
	np.allclose(ref, w.visualization)
