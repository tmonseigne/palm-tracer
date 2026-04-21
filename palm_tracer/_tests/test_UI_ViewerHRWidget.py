"""Fichier des tests pour le widget."""
import shutil

from qtpy.QtCore import Qt

from palm_tracer._tests.Utils import *
from palm_tracer.Processing import Parsing
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
def test_generate_bad(make_napari_viewer, patched_napari_viewer, qtbot, capsys, monkeypatch, fake_qfiledialog, fake_napari_layers):
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

	# Passage au suivi sans tableau
	qtbot.mouseClick(w._btn_src["Tracks"], Qt.MouseButton.LeftButton)
	qtbot.mouseClick(w._btn_generate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "WARNING: No tracking file available." in lines[-1]  # dernière ligne, car il peut y avoir un warning lors de la suppression des calques


##################################################
def test_generate(make_napari_viewer, patched_napari_viewer, qtbot, capsys, monkeypatch, fake_qfiledialog, fake_napari_layers):
	"""Test basique de création du widget."""
	viewer = make_napari_viewer()  # .		  Créer un viewer à l'aide de la fixture.
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
	pt = PALMTracer()
	add_basic_file(pt)
	pt.process()  # Process Vide pour créer le dossier et un setting de base
	shutil.copy2(INPUT_DIR / "localizations.csv", INPUT_DIR / "stack_PALM_Tracer" / f"localizations-{pt._suffix}.csv")
	shutil.copy2(INPUT_DIR / "tracking.csv", INPUT_DIR / "stack_PALM_Tracer" / f"tracking-{pt._suffix}.csv")
	pt.load()
	pt.df["loc"]["Integrated Intensity"] *= 100
	w = ViewerHRWidget(viewer, pt)  # Créer notre widget, en passant par le viewer.
	fake_napari_layers(viewer)

	w._upscale.value = 1
	w._cmb_src.value = 4
	w._gauss_intensity.value = 1
	upscale = w._upscale.value
	shape = (128 * upscale, 256 * upscale)
	ref = np.zeros(shape)

	# Génération de la localisation
	qtbot.mouseClick(w._btn_generate, Qt.MouseButton.LeftButton)
	ref[2, 1] = 200
	ref[3, 2] = 200
	ref[5, 4] = 100
	assert np.allclose(ref, w.visualization)

	# Génération de la localisation en mode gaussien
	w._gaussian.value = True
	w._color_mode.value = 1
	qtbot.mouseClick(w._btn_generate, Qt.MouseButton.LeftButton)
	ref = np.zeros(shape)
	patch = [[1, 2, 1, 0, 0, 0, 0],
			 [5, 9, 5, 1, 0, 0, 0],
			 [9, 15, 9, 5, 1, 0, 0],
			 [5, 9, 15, 9, 2, 1, 0],
			 [1, 5, 9, 5, 9, 5, 1],
			 [0, 1, 2, 9, 15, 9, 2],
			 [0, 0, 1, 5, 9, 5, 1],
			 [0, 0, 0, 1, 2, 1, 0]]
	ref[0:8, 0:7] += patch
	assert np.allclose(ref, w.visualization)

	# Génération du suivi
	qtbot.mouseClick(w._btn_src["Tracks"], Qt.MouseButton.LeftButton)
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
	w._upscale.value = 2
	upscale = w._upscale.value
	shape = (128 * upscale, 256 * upscale)
	ref = np.zeros(shape)
	assert np.allclose(ref, w.visualization)

	# Sortie avec le fichier de localisation, mais pas de billes.
	pt.df["loc"] = pd.read_csv(INPUT_DIR / "localizations.csv")
	_ = get_lines_output(capsys)  # Nettoyage de la sortie
	qtbot.mouseClick(w._btn_generate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "WARNING: No beads file available to correct drift." in lines[0]  # dernière ligne, car possible warning lors de la suppression des calques

	ref = np.zeros(shape)
	ref[4, 2] = 2
	ref[6, 4] = 2
	ref[8, 6] = 1
	ref[10, 8] = 1
	assert np.allclose(ref, w.visualization)

	# Sortie avec le fichier de localisation et un fichier de billes contenant une valeur abhérrante
	pt.df["bds"] = pd.DataFrame(
			[[1, 1, 1, 1, 2, 3, 1, 1, 1, 0, 1],
			 [1, 2, 2, 2, 3, 4, 1, 1, 1, 0, 1],
			 [1, 3, 3, 50, 3, 4, 1, 1, 1, 0, 1],
			 [1, 4, 4, 4, 3, 4, 1, 1, 1, 0, 1],
			 [1, 5, 5, 5, 3, 4, 1, 1, 1, 0, 1]],
			columns=Parsing.FILES_COLUMNS["Beads"]["columns"])
	pt.df["loc"] = pd.DataFrame(
			[[1, 1, 1, -1, 0, 0, 0, 1, 0, 0, 0, -1, -1, 0, 0, 1, 1, 1],
			 [2, 2, 2, -1, 1, 0, 0, 1, 0, 0, 0, -1, -1, 0, 0, 1, 1, 1],
			 [3, 3, 3, -1, 2, 0, 0, 1, 0, 0, 0, -1, -1, 0, 0, 1, 1, 1],
			 [4, 4, 4, -1, 3, 0, 0, 1, 0, 0, 0, -1, -1, 0, 0, 1, 1, 1],
			 [5, 5, 5, -1, 4, 0, 0, 1, 0, 0, 0, -1, -1, 0, 0, 1, 1, 1]],
			columns=Parsing.FILES_COLUMNS["Localization"]["columns"])

	qtbot.mouseClick(w._btn_generate, Qt.MouseButton.LeftButton)

	ref = np.zeros(shape)
	ref[0, 0] = 5
	assert np.allclose(ref, w.visualization, atol=0)
