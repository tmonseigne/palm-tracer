"""Teste le widget Napari de visualisation haute résolution des résultats."""

import shutil

from qtpy.QtCore import QCoreApplication, QEvent, Qt

from palm_tracer._tests.Utils import *
from palm_tracer.Settings.Types import BaseUIType, ButtonGroup
from palm_tracer.UI import ViewerHRWidget

INPUT_FILE = INPUT_DIR / "stack.tif"
OUTPUT_FOLDER = INPUT_DIR / "stack_PALM_Tracer"


##################################################
def flush_qt_delete_events():
	"""Traite les événements Qt de suppression différée."""
	QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
	QCoreApplication.processEvents()


##################################################
def test_widget_creation(make_napari_viewer, patched_napari_viewer):
	"""Vérifie la création du widget."""
	viewer = make_napari_viewer()  # .		Créer un viewer à l'aide de la fixture.
	_ = ViewerHRWidget(viewer, get_fake_pt())  # Créer notre widget, en passant par le viewer.


##################################################
def test_widget_double_creation(make_napari_viewer, patched_napari_viewer, qtbot):
	"""Vérifie Permettant de gérer la création en doublon de la même UI."""

	"""Reproduit le cas où une UI Qt cachée dans un dict survit à la destruction C++."""
	viewer = make_napari_viewer()  # .		Créer un viewer à l'aide de la fixture.
	pt = get_fake_pt()

	w = ViewerHRWidget(viewer, pt)
	w.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	w.close()
	flush_qt_delete_events()

	# Ici les BaseUI sont encore dans les settings, mais leurs objets Qt internes peuvent être supprimés côté C++.
	w2 = ViewerHRWidget(viewer, pt)
	w2.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
	w2.resize(1000, 600)
	w2.show()
	qtbot.waitExposed(w2)
	w2.close()
	flush_qt_delete_events()


##################################################
def test_add_stack(make_napari_viewer, patched_napari_viewer, qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Vérifie le widget."""
	viewer = make_napari_viewer()  # .	Créer un viewer à l'aide de la fixture.
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
	pt = PALMTracer()
	w = ViewerHRWidget(viewer, pt)  # Créer notre widget, en passant par le viewer.

	fake_qfiledialog(FileList, f"{INPUT_DIR / 'stack.tif'}")
	qtbot.mouseClick(w._btn_add_stack, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "No valid settings file to load." in lines[0]


##################################################
def test_change_type(make_napari_viewer, patched_napari_viewer, qtbot, capsys):
	"""Vérifie le widget."""
	viewer = make_napari_viewer()  # .			 Créer un viewer à l'aide de la fixture.
	w = ViewerHRWidget(viewer, get_fake_pt())  # Créer notre widget, en passant par le viewer.

	ui: BaseUIType = cast(ButtonGroup, w._pt.settings.hr["Type"]).get_ui(w.UI_NAME)
	qtbot.mouseClick(ui.boxes[0], Qt.MouseButton.LeftButton)  # Appuie sur localization
	assert w._pt.settings.hr["Type"].value == 0
	qtbot.mouseClick(ui.boxes[1], Qt.MouseButton.LeftButton)  # Appuie sur Tracks
	assert w._pt.settings.hr["Type"].value == 1


##################################################
def test_actualize(make_napari_viewer, patched_napari_viewer, qtbot, capsys):
	"""Vérifie le widget."""
	viewer = make_napari_viewer()  # .				Créer un viewer à l'aide de la fixture.
	w = ViewerHRWidget(viewer, PALMTracer())  # .	Créer notre widget, en passant par le viewer.

	qtbot.mouseClick(w._btn_actualize, Qt.MouseButton.LeftButton)

	w._pt._stack = np.zeros((1, 1, 1), dtype=np.uint16)
	qtbot.mouseClick(w._btn_actualize, Qt.MouseButton.LeftButton)


##################################################
def test_save(make_napari_viewer, patched_napari_viewer, qtbot, capsys):
	"""Vérifie la création du widget."""
	res_2d = OUTPUT_DIR / "HR.png"
	res_3d = OUTPUT_DIR / "HR.tif"
	res_2d.unlink(missing_ok=True)  # .				Suppression du fichier de résultat s'il existe.
	res_3d.unlink(missing_ok=True)  # .				Suppression du fichier de résultat s'il existe.

	viewer = make_napari_viewer()  # .				Créer un viewer à l'aide de la fixture.
	w = ViewerHRWidget(viewer, get_fake_pt())  # .	Créer notre widget, en passant par le viewer.

	w._filename = ""
	qtbot.mouseClick(w._btn_save, Qt.MouseButton.LeftButton)  # Il ne fait rien si pas de nom de fichier.

	w._filename = str(res_3d.resolve())
	qtbot.mouseClick(w._btn_save, Qt.MouseButton.LeftButton)
	assert res_3d.exists(), "File not saved."
	res_3d.unlink(missing_ok=True)  # .				Suppression du fichier de résultat s'il existe.

	w.visualization = np.zeros((1, 1), dtype=np.uint16)
	w._filename = str(res_2d.resolve())
	qtbot.mouseClick(w._btn_save, Qt.MouseButton.LeftButton)
	assert res_2d.exists(), "File not saved."
	res_2d.unlink(missing_ok=True)  # .				Suppression du fichier de résultat s'il existe.


##################################################
def test_screenshot(make_napari_viewer, patched_napari_viewer, qtbot, capsys, monkeypatch, fake_qfiledialog, fake_napari_layers):
	"""Vérifie la création du widget."""
	res = OUTPUT_DIR / "HR.png"
	res.unlink(missing_ok=True)  # .				Suppression du fichier de résultat s'il existe.
	viewer = make_napari_viewer()  # .				Créer un viewer à l'aide de la fixture.
	fake_napari_layers(viewer)

	# --- Mock screenshot ---
	def _fake_screenshot(self, path, canvas_only=True):
		"""Fake screenshot : écrit un faux PNG."""
		Path(path).write_bytes(b"fake png")

	monkeypatch.setattr(type(viewer), "screenshot", _fake_screenshot, raising=True)

	w = ViewerHRWidget(viewer, get_fake_pt())  # .	Créer notre widget, en passant par le viewer.

	w._screenshot_filename = ""
	qtbot.mouseClick(w._btn_screenshot, Qt.MouseButton.LeftButton)  # Il ne fait rien si pas de nom de fichier.
	assert not res.exists()

	w._screenshot_filename = str(res.resolve())
	qtbot.mouseClick(w._btn_screenshot, Qt.MouseButton.LeftButton)
	assert res.exists(), "File not saved."
	res.unlink(missing_ok=True)  # .				Suppression du fichier de résultat s'il existe.


##################################################
def test_check_beads(make_napari_viewer, patched_napari_viewer):
	"""Vérifie le widget."""
	viewer = make_napari_viewer()  # .			 	Créer un viewer à l'aide de la fixture.
	w = ViewerHRWidget(viewer, get_fake_pt())  # .	Créer notre widget, en passant par le viewer.

	ui: BaseUIType = w._pt.settings.hr["Remove Beads"].get_ui(w.UI_NAME)
	w._check_beads()  # False
	assert ui.boxes[0].isHidden()
	w._pt.results["bds"] = w._pt.results["loc"].copy()
	w._check_beads()  # True
	assert not ui.boxes[0].isHidden()


##################################################
def test_generate_bad(make_napari_viewer, patched_napari_viewer, qtbot, capsys, monkeypatch, fake_qfiledialog, fake_napari_layers):
	"""Vérifie le widget."""
	viewer = make_napari_viewer()  # .				Créer un viewer à l'aide de la fixture.
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
	pt = PALMTracer()
	w = ViewerHRWidget(viewer, pt)  # .				Créer notre widget, en passant par le viewer.

	fake_napari_layers(viewer)

	# PALMTracer n'est pas initialisé
	w._generate()
	lines = get_lines_output(capsys)
	assert "WARNING: No stack processed loaded." in lines[0]

	# Chargement d'une pile, mais aucun process
	fake_qfiledialog(FileList, f"{INPUT_DIR / 'stack.tif'}")
	qtbot.mouseClick(w._btn_add_stack, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "No valid settings file to load." in lines[0]

	# Idem aucune pile de chargée, car il n'a pas eu de process précédent.
	w._generate()
	lines = get_lines_output(capsys)
	assert "WARNING: No stack processed loaded." in lines[0]

	# Un process, mais aucun tableau d'exploitable.
	w._pt.process()  # Process Vide pour créer le dossier et un paramètre de base
	_ = get_lines_output(capsys)
	w._generate()
	lines = get_lines_output(capsys)
	assert "WARNING: No visualization available." in lines[0]


##################################################
def test_generate(make_napari_viewer, patched_napari_viewer, capsys, monkeypatch, fake_qfiledialog, fake_napari_layers):
	"""Vérifie le widget."""
	viewer = make_napari_viewer()  # Créer un viewer à l'aide de la fixture.
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
	pt = PALMTracer()
	add_basic_file(pt)
	pt.process()  # Process Vide pour créer le dossier et un paramètre de base
	shutil.copy2(INPUT_DIR / "localizations.csv", INPUT_DIR / "stack_PALM_Tracer" / f"localizations-{pt._timestamp}.csv")
	shutil.copy2(INPUT_DIR / "tracking.csv", INPUT_DIR / "stack_PALM_Tracer" / f"tracking-{pt._timestamp}.csv")
	shutil.copy2(INPUT_DIR / "beads.csv", INPUT_DIR / "stack_PALM_Tracer" / f"beads-{pt._timestamp}.csv")
	pt.load()
	pt.results["loc"]["Integrated Intensity"] *= 100
	w = ViewerHRWidget(viewer, pt)  # Créer notre widget, en passant par le viewer.
	fake_napari_layers(viewer)
	_ = get_lines_output(capsys)

	w._generate()
	w._pt.settings.hr["Type"].value = 1
	w._generate()
	lines = get_lines_output(capsys)
	assert len(lines) == 0
	w._pt.settings.hr["Dimension"].value = 1
	w._generate()
	lines = get_lines_output(capsys)
	assert len(lines) == 0
