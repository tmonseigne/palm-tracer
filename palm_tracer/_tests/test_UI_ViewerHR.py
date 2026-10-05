"""Teste le widget Napari de visualisation haute résolution des résultats."""

from copy import deepcopy
from importlib import import_module
from types import SimpleNamespace

import pytest
from napari.components import ViewerModel
from qtpy.QtCore import QCoreApplication, QEvent, QMimeData, QPoint, QPointF, Qt, QUrl
from qtpy.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent
from qtpy.QtWidgets import QApplication, QDockWidget, QMainWindow, QPushButton

from palm_tracer._tests.Utils import *
from palm_tracer.Settings.Types import BaseUIType, ButtonGroup, FileList
from palm_tracer.Tools import FileIO
from palm_tracer.UI import BaseNapariWidget, PALMTracerWidget, ViewerHRWidget

INPUT_FILE = INPUT_DIR / "stack.tif"
OUTPUT_FOLDER = INPUT_DIR / "stack_PALM_Tracer"


##################################################
@pytest.fixture
def stack_drop_widget(qtbot, monkeypatch):
	"""Crée une fenêtre HR et observe le chargement puis l'actualisation sans génération de rendu."""
	window = QMainWindow()
	qtbot.addWidget(window)
	receiver = DropReceiver()
	window.setCentralWidget(receiver)
	dock = QDockWidget(window)
	widget = ViewerHRWidget(ViewerModel(), PALMTracer())
	# Le modèle connecte lui-même la lecture de profondeur, indépendamment des signaux du widget.
	dock.setWidget(widget)
	window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

	calls = []
	files = cast(FileList, widget.pt.settings.batch["Files"])
	monkeypatch.setattr(ViewerHRWidget, "_generate", lambda self: None)
	monkeypatch.setattr(widget.pt, "load", lambda path="": calls.append(("load", Path(path))))
	monkeypatch.setattr(widget, "_actualize", lambda: calls.append(("actualize", Path(files.current_text))))
	window.show()
	return widget, receiver, calls


##################################################
def send_stack_drop(receiver, mime):
	"""Envoie les événements Qt d'entrée, de déplacement et de dépôt d'une pile."""
	enter = QDragEnterEvent(QPoint(1, 1), Qt.DropAction.CopyAction, mime, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier)
	move = QDragMoveEvent(QPoint(1, 1), Qt.DropAction.CopyAction, mime, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier)
	drop = QDropEvent(QPointF(1, 1), Qt.DropAction.CopyAction, mime, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier)
	for event in (enter, move, drop): QApplication.sendEvent(receiver, event)
	return enter, move, drop


##################################################
@pytest.fixture
def generated_widget(qtbot, capsys):
	"""Charge la pile et les résultats de référence pour les scénarios de génération HR."""
	viewer = ViewerModel()
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
	pt = PALMTracer()
	add_basic_file(pt)
	pt.process()  # Process vide pour créer le dossier et les paramètres de base.
	shutil.copy2(INPUT_DIR / "localizations.csv", OUTPUT_FOLDER / f"localizations-{pt._timestamp}.csv")
	shutil.copy2(INPUT_DIR / "tracking.csv", OUTPUT_FOLDER / f"tracking-{pt._timestamp}.csv")
	shutil.copy2(INPUT_DIR / "beads.csv", OUTPUT_FOLDER / f"beads-{pt._timestamp}.csv")
	pt.load()
	pt.results["loc"]["Integrated Intensity"] *= 100
	assert pt.stack is not None
	# En usage normal, cette initialisation est effectuée par le widget principal.
	pt.settings.rois.set_size(pt.stack.shape[-1], pt.stack.shape[-2])
	w = ViewerHRWidget(viewer, pt)
	qtbot.addWidget(w)
	get_lines_output(capsys)
	return viewer, pt, w


##################################################
def flush_qt_delete_events():
	"""Traite les événements Qt de suppression différée."""
	QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
	QCoreApplication.processEvents()


# ==================================================
# region Initialisation
# ==================================================
##################################################
def test_widget_creation(qtbot):
	"""Vérifie la création du widget."""
	viewer = ViewerModel()
	w = ViewerHRWidget(viewer, get_fake_pt())
	qtbot.addWidget(w)


##################################################
def test_layer_styles_follow_shared_configuration(qtbot, monkeypatch, tmp_path):
	"""Vérifie les styles personnalisés à la création, puis lors de la régénération des points HR."""
	styles = deepcopy(BaseNapariWidget.LAYER_ARGS)
	styles["Present"].update(face="blue", color="yellow", size=3.0, border=0.3)
	styles["Filtered"].update(face="magenta", color="orange", size=5.0, border=0.1, edge=2.0)
	monkeypatch.setattr(ViewerHRWidget, "LAYER_ARGS", styles)
	generate = ViewerHRWidget._generate
	monkeypatch.setattr(ViewerHRWidget, "_generate", lambda self: None)
	pt = PALMTracer()
	widget = ViewerHRWidget(ViewerModel(), pt)
	qtbot.addWidget(widget)
	assert widget.pt is pt
	expected = (("Points", "Present", [0, 0, 1, 1], [1, 1, 0, 1]),
				("Points Filtered", "Filtered", [1, 0, 1, 1], [1, 0.6470588, 0, 1]))

	# L'ajout d'un point expose les styles configurés pour les calques initialement vides.
	for name, state, face, border in expected:
		layer = widget._layers[name]
		layer.data = np.array([[0, 1, 1]], dtype=float)
		np.testing.assert_allclose(layer.face_color, [face])
		np.testing.assert_allclose(layer.border_color, [border])
		np.testing.assert_allclose(layer.size, styles[state]["size"])
		np.testing.assert_allclose(layer.border_width, styles[state]["border"])
	roi = widget._layers["ROI Filter"]
	assert roi.current_edge_color == "white"

	pt._path, pt._stack = str(tmp_path), np.zeros((1, 2, 2), dtype=np.uint16)
	pt.settings.hr["Type"].value, pt.settings.hr["Dimension"].value = 0, 0
	monkeypatch.setattr(pt, "hr", lambda: {"visualization": np.ones((2, 2), dtype=np.uint16),
										   "plot_data":     np.array([[0, 0, 0], [0, 1, 1]], dtype=float),
										   "plot_filtered": np.array([[0, 1, 0]], dtype=float)})
	monkeypatch.setattr(pt, "output_viz_name", lambda: tmp_path / "visualization.tif")
	monkeypatch.setattr(pt, "_save_setting_group", lambda group: None)
	monkeypatch.setattr(pt.settings.rois, "update_hr", lambda: None)

	generate(widget)

	for name, state, face, border in expected:
		layer = widget._layers[name]
		count = 2 if state == "Present" else 1
		assert len(layer.data) == count
		np.testing.assert_allclose(layer.face_color, np.tile(face, (count, 1)))
		np.testing.assert_allclose(layer.border_color, np.tile(border, (count, 1)))
		np.testing.assert_allclose(layer.size, styles[state]["size"])
		np.testing.assert_allclose(layer.border_width, styles[state]["border"])
		assert not layer.out_of_slice_display
		assert not layer.editable and layer.locked


##################################################
def test_results_status_automatic_update(qtbot):
	"""Vérifie que les statuts sont actualisés directement par Results."""
	viewer = ViewerModel()
	w = ViewerHRWidget(viewer, get_fake_pt())
	qtbot.addWidget(w)
	results_ui = w.pt.results.get_ui(w.UI_NAME)

	w.pt.results.reset()
	assert results_ui._labels["Beads"].text() == "No"

	w.pt.results["bds"] = pd.DataFrame(np.zeros((2, 1)))
	assert results_ui._labels["Beads"].text() == "Yes (2 localizations)"


##################################################
def test_widget_double_creation(qtbot):
	"""
	Vérifie Permettant de gérer la création en doublon de la même UI.
	Reproduit le cas où une UI Qt cachée dans un dict survit à la destruction C++.
	"""
	viewer = ViewerModel()
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


# ==================================================
# endregion Initialisation
# ==================================================

# ==================================================
# region Glisser-déposer
# ==================================================
##################################################
def test_stack_drop_loads_latest_results_and_actualizes(stack_drop_widget):
	"""Vérifie l'ajout d'une pile, sa sélection, puis le chargement et l'actualisation dans cet ordre."""
	widget, receiver, calls = stack_drop_widget
	mime = QMimeData()
	mime.setUrls([QUrl.fromLocalFile(str(INPUT_FILE))])

	events = send_stack_drop(receiver, mime)

	assert all(event.isAccepted() for event in events)
	assert receiver.received == []
	assert [Path(path) for path in widget.pt.settings.batch["Files"].items] == [INPUT_FILE]
	assert calls == [("load", OUTPUT_FOLDER), ("actualize", INPUT_FILE)]
	assert all(button.text() != "Add Stack" for button in widget.findChildren(QPushButton))


##################################################
@pytest.mark.parametrize("scenario", ["multiple", "mixed"], ids=["multiple-files", "local-and-remote"])
def test_stack_drop_rejects_multiple_urls(stack_drop_widget, scenario):
	"""Vérifie qu'un dépôt refusé ne modifie pas le Batch et ne charge aucun résultat."""
	widget, receiver, calls = stack_drop_widget
	urls = {"multiple": [QUrl.fromLocalFile(str(INPUT_FILE))] * 2,
			"mixed": [QUrl.fromLocalFile(str(INPUT_FILE)), QUrl("https://example.com/stack.tif")]}
	mime = QMimeData()
	mime.setUrls(urls[scenario])

	events = send_stack_drop(receiver, mime)

	assert not any(event.isAccepted() for event in events)
	assert receiver.received == []
	assert widget.pt.settings.batch["Files"].items == []
	assert calls == []


##################################################
@pytest.mark.parametrize("mode", [0, 1, 2], ids=["only-one", "each-file", "all-in-one"])
@pytest.mark.parametrize("shared_main", [False, True], ids=["standalone-hr", "shared-main-widget"])
def test_stack_drop_loads_latest_results_from_dropped_stack(stack_drop_widget, tmp_path, monkeypatch, qtbot, mode, shared_main):
	"""Charge réellement les derniers résultats de la pile déposée malgré une autre pile déjà dans le Batch."""
	widget, receiver, calls = stack_drop_widget
	pt = widget.pt
	files = cast(FileList, pt.settings.batch["Files"])
	first_stack, dropped_stack = tmp_path / "first.tif", tmp_path / "dropped.tif"
	for stack in (first_stack, dropped_stack): shutil.copy2(INPUT_FILE, stack)
	first_folder, dropped_folder = tmp_path / "first_PALM_Tracer", tmp_path / "dropped_PALM_Tracer"
	for folder in (first_folder, dropped_folder): folder.mkdir()

	# Les paramètres enregistrés correspondent au traitement individuel de la pile déposée.
	files.items = [str(dropped_stack)]
	pt.settings.batch["Mode"].value = 0
	settings = pt.settings.to_compact_dict()
	older_timestamp, latest_timestamp = "20260101_000000", "20260102_000000"
	FileIO.save_json(first_folder / f"settings-{latest_timestamp}.json", settings)
	pd.DataFrame({"X": [-1.0], "Y": [-1.0]}).to_csv(first_folder / f"localizations-{latest_timestamp}.csv", index=False)
	FileIO.save_json(dropped_folder / f"settings-{older_timestamp}.json", settings)
	pd.DataFrame({"X": [1.0], "Y": [2.0]}).to_csv(dropped_folder / f"localizations-{older_timestamp}.csv", index=False)
	FileIO.save_json(dropped_folder / f"settings-{latest_timestamp}.json", settings)
	expected = pd.DataFrame({"X": [3.0, 4.0], "Y": [5.0, 6.0]})
	expected.to_csv(dropped_folder / f"localizations-{latest_timestamp}.csv", index=False)

	files.items = [str(first_stack)]
	pt.settings.batch["Mode"].value = mode
	# Seule la validation des DLL est neutralisée : load() lit les vrais JSON, CSV et TIFF.
	monkeypatch.setattr(pt, "is_dll_valid", lambda: True)
	load_calls = []

	def load_results(path=""):
		"""Observe les chemins transmis sans remplacer le véritable chargement."""
		load_calls.append(Path(path))
		PALMTracer.load(pt, path)

	monkeypatch.setattr(pt, "load", load_results)
	if shared_main:
		# Le widget principal utilise la même instance et conserve son vrai callback de synchronisation.
		monkeypatch.setattr(import_module(BaseNapariWidget.__module__), "PALMTracer", lambda: pt)
		monkeypatch.setattr(PALMTracerWidget, "_on_startup", lambda self: None)
		monkeypatch.setattr(PALMTracerWidget, "_on_change_setting", lambda self: None)
		monkeypatch.setattr(PALMTracerWidget, "_preview", lambda self: None)
		monkeypatch.setattr(PALMTracerWidget, "_auto_threshold", lambda self: None)
		main = PALMTracerWidget(ViewerModel())
		qtbot.addWidget(main)
	mime = QMimeData()
	mime.setUrls([QUrl.fromLocalFile(str(dropped_stack))])

	send_stack_drop(receiver, mime)

	assert pt.results.results_folder == dropped_folder.resolve()
	assert pt.results.stack_name == dropped_stack.stem
	assert Path(files.current_text) == dropped_stack
	pd.testing.assert_frame_equal(pt.results["loc"], expected)
	np.testing.assert_array_equal(pt.stack, FileIO.open_tif(dropped_stack))
	assert calls == [("actualize", dropped_stack)]
	assert not pt._loading
	assert load_calls and all(path == dropped_folder for path in load_calls)


##################################################
def test_stack_drop_preserves_active_load_context(stack_drop_widget, monkeypatch):
	"""Vérifie qu'un chargement imbriqué ne remplace pas le dossier ni le timestamp actifs."""
	widget, _, calls = stack_drop_widget
	pt = widget.pt
	monkeypatch.setattr(pt, "load", PALMTracer.load.__get__(pt))
	pt._path, pt._timestamp = "active_PALM_Tracer", "20260102_000000"
	pt._loading = True
	try:
		pt.load(str(INPUT_FILE))
		assert pt.path == "active_PALM_Tracer"
		assert pt._timestamp == "20260102_000000"
		assert calls == []
	finally: pt._loading = False


##################################################
def test_stack_drop_releases_load_guard_after_error(stack_drop_widget, monkeypatch):
	"""Vérifie qu'une erreur de lecture n'empêche pas un chargement ultérieur sur la même instance."""
	widget, _, calls = stack_drop_widget
	pt = widget.pt
	monkeypatch.setattr(pt, "load", PALMTracer.load.__get__(pt))

	def fail_load(_path):
		"""Simule une erreur de lecture pendant le chargement protégé."""
		raise OSError("Unreadable settings")

	monkeypatch.setattr(pt, "_load_results", fail_load)
	with pytest.raises(OSError, match="Unreadable settings"):
		widget._add_stack(str(INPUT_FILE))
	assert not pt._loading
	assert calls == []

	loaded_folders = []
	monkeypatch.setattr(pt, "_load_results", loaded_folders.append)
	widget._add_stack(str(INPUT_FILE))
	assert [Path(path) for path in loaded_folders] == [OUTPUT_FOLDER]
	assert calls == [("actualize", INPUT_FILE)]
	assert not pt._loading


# ==================================================
# endregion Glisser-déposer
# ==================================================

# ==================================================
# region Liaison avec PALMTracer
# ==================================================
##################################################
def test_check_beads(qtbot):
	"""Vérifie le widget."""
	viewer = ViewerModel()
	w = ViewerHRWidget(viewer, get_fake_pt())
	qtbot.addWidget(w)

	ui: BaseUIType = w.pt.settings.hr["Remove Beads"].get_ui(w.UI_NAME)
	w._check_beads()  # False
	assert ui.boxes[0].isHidden()
	w.pt.results["bds"] = w.pt.results["loc"].copy()
	w._check_beads()  # True
	assert not ui.boxes[0].isHidden()


##################################################
def test_add_stack(qtbot, capsys):
	"""Vérifie le chargement d'une pile sans résultat enregistré."""
	viewer = ViewerModel()
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
	pt = PALMTracer()
	w = ViewerHRWidget(viewer, pt)
	qtbot.addWidget(w)

	w._add_stack(str(INPUT_FILE))
	lines = get_lines_output(capsys)
	assert "No valid settings file to load." in lines[0]


##################################################
def test_actualize(qtbot):
	"""Vérifie le widget."""
	viewer = ViewerModel()
	w = ViewerHRWidget(viewer, PALMTracer())
	qtbot.addWidget(w)

	qtbot.mouseClick(w._btn_actualize, Qt.MouseButton.LeftButton)

	w.pt._stack = np.zeros((1, 1, 1), dtype=np.uint16)
	qtbot.mouseClick(w._btn_actualize, Qt.MouseButton.LeftButton)


##################################################
def test_save(qtbot):
	"""Vérifie la création du widget."""
	res_2d, res_3d = OUTPUT_DIR / "HR.png", OUTPUT_DIR / "HR.tif"
	res_2d.unlink(missing_ok=True)  # .				Suppression du fichier de résultat s'il existe.
	res_3d.unlink(missing_ok=True)  # .				Suppression du fichier de résultat s'il existe.

	viewer = ViewerModel()
	w = ViewerHRWidget(viewer, get_fake_pt())
	qtbot.addWidget(w)

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
def test_screenshot(make_napari_viewer, patched_napari_viewer, qtbot, monkeypatch):
	"""Vérifie le bouton de capture et l'appel à l'API du viewer graphique, sans exécuter le rendu OpenGL."""
	res = OUTPUT_DIR / "HR.png"
	res.unlink(missing_ok=True)  # .				Suppression du fichier de résultat s'il existe.
	viewer = make_napari_viewer()  # .			 	Créer un viewer à l'aide de la fixture.

	# --- Mock screenshot ---
	def _fake_screenshot(self, path, canvas_only=True):
		"""Fake screenshot : écrit un faux PNG."""
		Path(path).write_bytes(b"fake png")

	monkeypatch.setattr(type(viewer), "screenshot", _fake_screenshot, raising=True)

	w = ViewerHRWidget(viewer, get_fake_pt())  # .	Créer notre widget, en passant par le viewer.
	qtbot.addWidget(w)

	w._screenshot_filename = ""
	qtbot.mouseClick(w._btn_screenshot, Qt.MouseButton.LeftButton)  # Il ne fait rien si pas de nom de fichier.
	assert not res.exists()

	w._screenshot_filename = str(res.resolve())
	qtbot.mouseClick(w._btn_screenshot, Qt.MouseButton.LeftButton)
	assert res.exists(), "File not saved."
	res.unlink(missing_ok=True)  # .				Suppression du fichier de résultat s'il existe.


##################################################
def test_change_type(qtbot):
	"""Vérifie le widget."""
	viewer = ViewerModel()
	w = ViewerHRWidget(viewer, get_fake_pt())  # Créer notre widget, en passant par le viewer.
	qtbot.addWidget(w)

	ui: BaseUIType = cast(ButtonGroup, w.pt.settings.hr["Type"]).get_ui(w.UI_NAME)
	qtbot.mouseClick(ui.boxes[0], Qt.MouseButton.LeftButton)  # Appuie sur localization
	assert w.pt.settings.hr["Type"].value == 0
	qtbot.mouseClick(ui.boxes[1], Qt.MouseButton.LeftButton)  # Appuie sur Tracks
	assert w.pt.settings.hr["Type"].value == 1


# ==================================================
# endregion Liaison avec PALMTracer
# ==================================================

# ==================================================
# region Dessin
# ==================================================
##################################################
def test_generate_bad(qtbot, capsys):
	"""Vérifie le widget."""
	viewer = ViewerModel()
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
	pt = PALMTracer()
	w = ViewerHRWidget(viewer, pt)  # .				Créer notre widget, en passant par le viewer.
	qtbot.addWidget(w)

	# PALMTracer n'est pas initialisé
	w._generate()
	lines = get_lines_output(capsys)
	assert "WARNING: No stack processed loaded." in lines[0]

	# Chargement d'une pile, mais aucun process
	w._add_stack(str(INPUT_FILE))
	lines = get_lines_output(capsys)
	assert "No valid settings file to load." in lines[0]

	# Idem aucune pile de chargée, car il n'a pas eu de process précédent.
	w._generate()
	lines = get_lines_output(capsys)
	assert "WARNING: No stack processed loaded." in lines[0]

	# Un process, mais aucun tableau d'exploitable.
	w.pt.process()  # Process Vide pour créer le dossier et un paramètre de base
	_ = get_lines_output(capsys)
	w._generate()
	lines = get_lines_output(capsys)
	assert "WARNING: No visualization available." in lines[0]


##################################################
def test_generate(generated_widget, capsys):
	"""Vérifie le widget."""
	viewer, pt, w = generated_widget

	settings_file = Path(pt.path) / f"settings-{pt.suffix}.json"
	initial = FileIO.open_json(settings_file)
	pt.settings.hr["Background"].value = 10
	pt.settings.gallery.active = True

	w._layers[w.LAYERS_NAME[1]].visible = False  # État initial masqué
	w._generate()
	actual = FileIO.open_json(settings_file)["PALM Tracer Settings"]
	assert actual["HR"] == pt.settings.hr.to_compact_dict()
	assert actual["Gallery"] == initial["PALM Tracer Settings"]["Gallery"]
	assert not w._layers[w.LAYERS_NAME[1]].visible
	assert not w._layers["Tracks"].visible
	w.pt.settings.hr["Type"].value = 1
	w._generate()
	assert not w._layers[w.LAYERS_NAME[1]].visible
	assert not w._layers["Tracks"].visible
	assert viewer.dims.range[0].stop == np.max(w._layers["Tracks"].data[:, 1])
	lines = get_lines_output(capsys)
	assert len(lines) == 0
	w.pt.settings.hr["Dimension"].value = 1
	w._generate()
	lines = get_lines_output(capsys)
	assert len(lines) == 0


##################################################
@pytest.mark.parametrize("dimension", [pytest.param(0, id="2d"), pytest.param(1, id="z-stack")])
@pytest.mark.parametrize("key", [pytest.param("loc", id="raw"), pytest.param("dft", id="corrected")])
@pytest.mark.parametrize("remove_beads", [pytest.param(False, id="keep-beads"), pytest.param(True, id="remove-beads")])
def test_generate_filtered_points(generated_widget, dimension, key, remove_beads):
	"""Les points exclus restent rouges et utilisent le cadre XY et l'origine Z du rendu conservé."""
	_, pt, w = generated_widget
	pt.results.reset_filtered()
	locations = pt.results["loc"].iloc[:4].copy()
	locations.index = [10, 20, 30, 40]
	locations["X"], locations["Y"], locations["Z"] = [20, 22, 21, 100], [30, 32, 31, 100], [4, 8, 6, 10]
	pt.results[key] = locations
	pt.results[f"f_{key}"] = locations.iloc[:2].copy()
	pt.results["bds"] = locations.iloc[3:].copy()
	s = pt.settings.hr
	s["Type"].value, s["Dimension"].value = 0, dimension
	s["Ratio"].value, s["Crop"].value = 2, True
	s["Remove Beads"].value, s["Drift Correction"].value = remove_beads, False
	s.gaussian.active = False
	s.hr_3d["Z Step"].value = 2
	before = locations.copy(deep=True)
	w._generate()
	x0, _, y0, _ = pt.settings.rois.hr_box
	layer = w._layers["Points Filtered"]
	expected_z = 0 if dimension == 0 else 1
	np.testing.assert_allclose(layer.data, [[expected_z, (31 - y0) * 2, (21 - x0) * 2]])
	np.testing.assert_allclose(layer.face_color, [[1, 0, 0, 1]])
	assert not layer.out_of_slice_display
	assert not layer.editable and layer.locked
	pd.testing.assert_frame_equal(pt.results[key], before)

	# La réinitialisation vide le même calque sans recréer l'objet Napari.
	pt.reset_filtered()
	w._generate()
	assert w._layers["Points Filtered"] is layer
	assert layer.data.shape == (0, 3)


##################################################
@pytest.mark.parametrize("mode", [pytest.param("tracking", id="tracking"), pytest.param("rotation", id="rotation")])
def test_generate_clears_filtered_points_in_other_modes(generated_widget, mode):
	"""Une transition vers les trajectoires ou la rotation supprime les points exclus du rendu précédent."""
	_, pt, w = generated_widget
	pt.results.reset_filtered()
	pt.results["f_loc"] = pt.results["loc"].iloc[::2].copy()
	pt.settings.hr["Crop"].value = False
	pt.settings.hr["Remove Beads"].value = pt.settings.hr["Drift Correction"].value = False
	w._generate()
	layer = w._layers["Points Filtered"]
	assert len(layer.data) > 0
	layer.visible = True
	if mode == "tracking": pt.settings.hr["Type"].value = 1
	else:
		pt.settings.hr["Dimension"].value = 2
		pt.settings.hr.hr_3d["Frames"].value = 4
	w._generate()
	assert layer.data.shape == (0, 3)
	if mode == "rotation": assert not layer.visible


##################################################
def test_generate_preserves_render_limits(generated_widget):
	"""Le vrai rendu recadré et les points affichés utilisent le même cadre, y compris après régénération."""
	viewer, pt, w = generated_widget
	pt.results.reset_filtered()
	pt.results["loc"]["X"], pt.results["loc"]["Y"] = 20.25, 30.25  # Point unique dupliqué
	pt.settings.hr["Ratio"].value = 2
	pt.settings.hr["Crop"].value = True
	pt.settings.hr["Remove Beads"].value = False
	pt.settings.hr["Drift Correction"].value = False
	pt.settings.hr.gaussian.active = False
	w._generate()
	x0, x1, y0, y1 = pt.settings.rois.hr_box
	assert (x0, x1, y0, y1) == (15, 26, 25, 36)  # Taille du padding autour du point unique
	assert w.visualization.shape == ((y1 - y0) * 2, (x1 - x0) * 2)
	np.testing.assert_array_equal(w._layers[w.LAYERS_NAME[0]].data, w.visualization)
	points = w._layers[w.LAYERS_NAME[1]].data
	# Vérification du décallage
	np.testing.assert_allclose(points[:, -2], (pt.results.localizations["Y"] - y0) * 2)
	np.testing.assert_allclose(points[:, -1], (pt.results.localizations["X"] - x0) * 2)

	# La même interface retrouve le champ complet lorsque le cadrage automatique est désactivé.
	pt.settings.hr["Crop"].value = False
	height, width = pt.stack.shape[-2:]
	w._generate()
	assert pt.settings.rois.hr_box == (0, width, 0, height)
	assert w.visualization.shape == (height * 2, width * 2)

	pt.settings.hr["Crop"].value = True
	pt.results["loc"]["X"], pt.results["loc"]["Y"] = 2, 2  # .					Point unique trop proche d'un bord.
	w._generate()
	assert pt.settings.rois.hr_box == (0, 7, 0, 7)  # .							Taille du padding autour du point unique

	pt.results["loc"]["X"], pt.results["loc"]["Y"] = width - 2, height - 2  # .	Point unique trop proche d'un bord.
	w._generate()
	assert pt.settings.rois.hr_box == (width - 7, width, height - 7, height)  # Taille du padding autour du point unique


##################################################
def test_generate_restores_box_without_image(generated_widget, capsys):
	"""Une génération sans résultats conserve l'image, les points et le cadre déjà affichés."""
	viewer, pt, w = generated_widget
	pt.results.reset_filtered()
	pt.results["loc"]["X"], pt.results["loc"]["Y"] = 20.25, 30.25  # Point unique dupliqué
	pt.settings.hr["Ratio"].value = 2
	pt.settings.hr["Crop"].value = True
	pt.settings.hr["Remove Beads"].value = False
	pt.settings.hr["Drift Correction"].value = False
	pt.settings.hr.gaussian.active = False
	w._generate()
	previous_box = w.pt.settings.rois.hr_box
	previous_image = w.visualization
	previous_points = w._layers[w.LAYERS_NAME[1]].data.copy()
	assert previous_box[0] > 0 and previous_box[2] > 0
	w.pt.results.reset()
	get_lines_output(capsys)

	w._generate()
	assert "WARNING: No visualization available." in get_lines_output(capsys)
	assert w.pt.settings.rois.hr_box == previous_box
	assert w.visualization is previous_image
	np.testing.assert_array_equal(w._layers[w.LAYERS_NAME[0]].data, previous_image)
	np.testing.assert_array_equal(w._layers[w.LAYERS_NAME[1]].data, previous_points)


##################################################
def test_generate_render_and_roi_transitions(qtbot):
	"""
	Enchaîne tous les rendus sur les mêmes viewers pour détecter une dérive du repère des ROI.

	Les boucles constituent un seul scénario de transitions : les objets, calques et ROI sont réutilisés jusqu'au retour au cadre initial.
	Les deux ViewerModel utilisent les vrais calques et événements Napari sans canvas OpenGL ; seul le widget HR nécessite Qt.
	La ROI vide conserve sa taille ; le track stack sans dessin retourne actuellement un volume gris, même si le fond raw est demandé.
	"""
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
	pt = PALMTracer()
	add_basic_file(pt)
	pt.process()  # Initialise le dossier et les paramètres associés à la pile de référence.
	pt.load()
	assert pt.stack is not None
	# Remplace l'initialisation des dimensions normalement effectuée par le widget principal.
	pt.settings.rois.set_size(pt.stack.shape[-1], pt.stack.shape[-2])
	pt.results.reset()
	localizations = pd.DataFrame({"X":                    [20, 24, 28, 40, 44, 48], "Y": [30, 32, 34, 50, 52, 54],
								  "Z":                    [0, 1, 2, 0, 1, 2], "Plane": [1, 2, 3, 1, 2, 3],
								  "Integrated Intensity": [1000] * 6, "Sigma X": [1.0] * 6,
								  "Sigma Y":              [1.0] * 6, "Theta": [0.0] * 6})
	tracks = localizations.copy()
	tracks["Track"] = [1, 1, 1, 2, 2, 2]
	pt.results["loc"], pt.results["trc"] = localizations.copy(), tracks.copy()
	s = pt.settings.hr
	s["Ratio"].value = 2
	s["Crop"].value = True
	s["Background"].value = 0
	s["Scaling"].value = 1000
	s["Remove Beads"].value = False
	s["Drift Correction"].value = False
	s.gaussian["Shape"].value = 0
	s.gaussian["Size"].value = 1
	s.gaussian["Fixed Intensity"].value = True
	s.gaussian["Intensity"].value = 1000
	s.hr_3d["Frames"].value = 4
	s.hr_3d["Z Step"].value = 1
	s.track_stack["Head"].value = 1
	s.track_stack["Width"].value = 1
	pt.settings.calibration["Pixel Size"].value = 0.001

	# Deux vrais calques de ROI pour vérifier les transformations dans les deux sens.
	main_viewer = ViewerModel()
	rois = pt.settings.rois
	rois.set_xy_roi(22, 70, 28, 80, add=False)
	rois.set_xy_roi(90, 110, 90, 110)
	canonical_rois = [roi.data.copy() for roi in rois.rois]
	rois.layer_main = main_viewer.add_shapes([], name="ROI Filter", shape_type="rectangle")
	rois.roi_selection.active = False
	viewer = ViewerModel()
	w = ViewerHRWidget(viewer, pt)
	qtbot.addWidget(w)
	initial_tracks_layer = w._layers["Tracks"]
	full_box = (0, pt.stack.shape[-1], 0, pt.stack.shape[-2])

	# L'ordre fait notamment passer du gris au RGB, puis revenir aux localisations après les trajectoires.
	modes = [("2d-spots", 0, 0, False, False), ("2d-gaussian", 0, 0, True, False),
			 ("z-spots", 1, 0, False, False), ("z-gaussian", 1, 0, True, False),
			 ("rotation-spots", 2, 0, False, False), ("rotation-gaussian", 2, 0, True, False),
			 ("tracks", 0, 1, False, False), ("track-stack", 3, 1, False, False),
			 ("track-stack-raw", 3, 1, False, True), ("return-z", 1, 0, False, False),
			 ("return-tracks", 0, 1, False, False), ("return-rotation", 2, 0, False, False), ("return-2d", 0, 0, False, False)]
	for name, dimension, track_mode, gaussian, raw in modes:
		s["Dimension"].value = dimension
		# Le retour depuis les tracks vérifie aussi un pas Z manuel différent du pas automatique.
		s.hr_3d["Z Step"].value = 2 if name == "return-z" else 1
		s["Type"].value = track_mode
		s["Source"].value = 0
		s.gaussian.active = gaussian
		s.track_stack["Background"].value = raw
		initial_render = None
		for stage in ("auto", "mixed-roi", "empty-roi", "shifted-data", "return-auto"):
			context = f"{name}/{stage}"
			shift_x, shift_y = (8, 4) if stage == "shifted-data" else (0, 0)
			for key, source in (("loc", localizations), ("trc", tracks)):
				data = source.copy()
				data["X"] += shift_x
				data["Y"] += shift_y
				pt.results[key] = data
			rois.roi_selection.value = 2 if stage == "empty-roi" else 1
			rois.roi_selection.active = stage in ("mixed-roi", "empty-roi")
			if track_mode: initial_tracks_layer.visible = True
			if track_mode: w._layers[w.LAYERS_NAME[1]].visible = True
			w._generate()
			assert w._layers["ROI Filter"].visible == (dimension != 2), context
			assert w._layers["Tracks"] is initial_tracks_layer, context
			assert viewer.layers["Tracks"] is initial_tracks_layer, context
			if track_mode: assert initial_tracks_layer.visible, context

			# Bornes de référence explicites : marge actuelle de cinq pixels source, plus trois sigmas en gaussien.
			auto_box = (12, 56, 22, 62) if gaussian else (15, 53, 25, 59)
			if dimension == 2:
				expected_box = full_box
				assert rois.data_box == (-1, -1, -1, -1), context
			else:
				expected_box = (auto_box[0] + shift_x, auto_box[1] + shift_x, auto_box[2] + shift_y, auto_box[3] + shift_y)
				assert rois.data_box == expected_box, context
			if stage == "mixed-roi":
				expected_box = (22, 70, 28, 80) if dimension == 2 else (22, auto_box[1], 28, auto_box[3])
			elif stage == "empty-roi": expected_box = (90, 110, 90, 110)
			assert rois.hr_box == expected_box, context
			x0, x1, y0, y1 = expected_box
			image = w.visualization
			is_rgb = bool(raw and stage != "empty-roi")
			image_layer = w._layers[w.LAYERS_NAME[0]]
			assert viewer.layers[0] is image_layer, context
			assert len(viewer.layers) == len(w.LAYERS_NAME), context
			assert image_layer.rgb == is_rgb, context
			np.testing.assert_array_equal(image_layer.data, image, err_msg=context)
			spatial_shape = image.shape[-3:-1] if is_rgb else image.shape[-2:]
			if dimension == 2 and stage != "empty-roi":
				assert image.shape[0] == 4, context
				# Le canevas tourné est recadré sans modifier le repère source conservé dans hr_box.
				cx, cy = ((x1 - x0) * 2 - 1) / 2, ((y1 - y0) * 2 - 1) / 2
				diameter = int(np.ceil(2 * np.sqrt(cx * cx + cy * cy + 1))) + 3
				assert 0 < spatial_shape[0] < diameter and 0 < spatial_shape[1] < diameter, context
			else: assert spatial_shape == ((y1 - y0) * 2, (x1 - x0) * 2), context
			assert bool(np.any(image)) == (stage != "empty-roi"), context
			if stage == "empty-roi" and dimension != 0: assert image.shape[0] == 1, context
			if is_rgb:
				assert image.shape == (3, (y1 - y0) * 2, (x1 - x0) * 2, 3), context
				# Ce coin est hors des trajectoires : sa valeur doit provenir du bon pixel de l'acquisition.
				background = pt.stack[:3, y0:y1, x0:x1].astype(float)
				low, high = background.min(), background.max()
				offset, span = (low, high - low) if high > low else (0.0, 65535.0)
				expected_corner = round((background[0, 0, 0] - offset) * 255 / span)
				np.testing.assert_array_equal(image[0, 0, 0], [expected_corner] * 3, err_msg=context)
			# Le crop à l'export reste distinct du cadre affiché et ne doit pas modifier sa synchronisation.
			cropped = pt.crop(image)
			assert cropped.size <= image.size, context
			assert rois.hr_box == expected_box, context
			if stage == "empty-roi": assert cropped.size == 1, context

			# Le calque de points/trajectoires conserve le même décalage XY que les limites source.
			source = pt.results.tracks if track_mode else pt.results.localizations
			inside = source["X"].between(x0, x1) & source["Y"].between(y0, y1)
			expected_xy = (source.loc[inside, ["Y", "X"]].to_numpy() - [y0, x0]) * 2
			plot = w._layers["Tracks" if track_mode else "Points"].data
			if dimension == 2:
				assert plot.shape == (0, 3), context
				assert not w._layers[w.LAYERS_NAME[1]].visible, context
			elif track_mode and expected_xy.shape[0] == 0:
				# Le point fictif garde le calque utilisateur en place sans transmettre un tableau vide à Napari.
				np.testing.assert_array_equal(plot, np.zeros((1, 4)), err_msg=context)
			else: np.testing.assert_allclose(plot[:, -2:], expected_xy, err_msg=context)
			if not track_mode:
				np.testing.assert_array_equal(initial_tracks_layer.data, np.zeros((1, 4)), err_msg=context)
				assert not initial_tracks_layer.visible, context
			if dimension == 1 and len(plot):
				z = source.loc[inside, "Z"].to_numpy()
				z_step = s.hr_3d["Z Step"].value or pt._get_uniform_z_step()
				np.testing.assert_array_equal(plot[:, 0], np.floor((z - z.min()) / z_step), err_msg=context)
				assert not w._layers[w.LAYERS_NAME[1]].out_of_slice_display, context
			if track_mode:
				points_layer = w._layers[w.LAYERS_NAME[1]]
				assert points_layer.visible and not points_layer.out_of_slice_display, context
				if expected_xy.shape[0] == 0:
					assert points_layer.data.shape == (0, 3), context
				else:
					np.testing.assert_array_equal(points_layer.data, plot[:, 1:], err_msg=context)
					planes = source.loc[inside, "Plane"].to_numpy()
					if dimension == 3: planes = planes - source["Plane"].min()
					np.testing.assert_array_equal(points_layer.data[:, 0], planes, err_msg=context)
					np.testing.assert_array_equal(points_layer.face_color, np.tile([0, 1, 0, 1], (len(plot), 1)), err_msg=context)

			# Aucun appel à get_hr_limits ici : les assertions ne doivent pas réparer le cadre testé.
			for index, canonical in enumerate(canonical_rois):
				np.testing.assert_allclose(rois.rois[index].data, canonical, err_msg=context)
				np.testing.assert_allclose(rois.layer_main.data[index], canonical, err_msg=context)
				np.testing.assert_allclose(rois.layer_hr.data[index], (canonical - [y0, x0]) * 2, err_msg=context)
			# Aller-retour via les callbacks réels, sans changer les sommets ni leur repère attendu.
			rois.update_from_hr()
			rois.update_from_main()
			for index, canonical in enumerate(canonical_rois):
				np.testing.assert_allclose(rois.rois[index].data, canonical, err_msg=context)
				np.testing.assert_allclose(rois.layer_main.data[index], canonical, err_msg=context)
				np.testing.assert_allclose(rois.layer_hr.data[index], (canonical - [y0, x0]) * 2, err_msg=context)
			if stage == "auto": initial_render = image.copy()
			elif stage == "return-auto": np.testing.assert_array_equal(image, initial_render, err_msg=context)


##################################################
def test_rotation_preserves_hidden_roi(generated_widget):
	"""Conserve une ROI déjà masquée après plusieurs générations en rotation puis un retour en 2D."""
	_, _, w = generated_widget
	roi_layer = w._layers["ROI Filter"]
	roi_layer.visible = False
	w._hr_settings["Dimension"].value = 2
	w._hr_settings.hr_3d["Frames"].value = 4
	w._generate()
	assert not roi_layer.visible
	w._generate()
	assert not roi_layer.visible
	w._hr_settings["Dimension"].value = 0
	w._generate()
	assert not roi_layer.visible
	assert w._roi_visibility_before_rotation is None


##################################################
def test_visualization_layer_rgb_transitions():
	"""Vérifie les axes des rendus 2D et 3D lors des transitions, sans fenêtre ni OpenGL."""
	viewer = ViewerModel()
	layer = viewer.add_image(np.zeros((1, 1), dtype=np.uint16), name="Visualization")
	viewer.add_points(np.empty((0, 3)), name="Points")
	state = SimpleNamespace(viewer=viewer, LAYERS_NAME=ViewerHRWidget.LAYERS_NAME, _layers={"Visualization": layer},
							update_layer=BaseNapariWidget.update_layer)
	for shape in [(2, 5, 7, 3), (3, 5, 7, 3), (2, 5, 7), (5, 7), (2, 5, 7, 3)]:
		state.visualization = np.zeros(shape, dtype=np.uint8)
		ViewerHRWidget._update_visualization_layer(state)
		layer = state._layers["Visualization"]
		assert layer.rgb == (len(shape) == 4)
		assert layer.ndim == len(shape) - int(layer.rgb)
		assert viewer.dims.ndim == 3
		assert viewer.layers[0] is layer
		assert len(viewer.layers) == 2
		assert not layer.editable and layer.locked
		np.testing.assert_array_equal(layer.data, state.visualization)
		viewer.dims.ndisplay = 3
		assert layer.ndim == len(shape) - int(layer.rgb)

# ==================================================
# endregion Dessin
# ==================================================
