"""Teste le widget principal de PALM Tracer."""

import shutil
from pathlib import Path

import pytest
from napari.components import ViewerModel
from qtpy.compat import isalive
from qtpy.QtCore import QCoreApplication, QEvent, QMimeData, QPoint, QPointF, Qt, QUrl
from qtpy.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent, QShowEvent
from qtpy.QtWidgets import QApplication, QDockWidget, QMainWindow, QScrollArea, QTabWidget, QWidget

from palm_tracer._tests.Utils import *
from palm_tracer.UI import PALMTracerWidget
from palm_tracer.UI.PALMTracerWidget import SETTINGS_FILE

SIZE_X, SIZE_Y, INTENSITY, RATIO = 100, 50, 1000, 10
SIZE = int(SIZE_X * np.sqrt(SIZE_Y))
rng = np.random.default_rng(42)  # Générateur propre au jeu de données de ce module.
POINTS = np.stack([rng.uniform(1, SIZE_Y - 1, size=SIZE), rng.uniform(1, SIZE_X - 1, size=SIZE)], axis=1)
OUTPUT_FOLDER = INPUT_DIR / "stack_PALM_Tracer"


##################################################
class DropReceiver(QWidget):
	"""Simule un widget qui ouvrirait normalement les fichiers déposés."""

	def __init__(self, parent=None):
		"""Initialise le compteur d'événements et l'acceptation des dépôts."""
		super().__init__(parent)
		self.received = []
		self.setAcceptDrops(True)

	def dragEnterEvent(self, event):
		"""Accepte le glissement habituel du widget destinataire."""
		self.received.append("enter")
		event.acceptProposedAction()

	def dropEvent(self, event):
		"""Enregistre le dépôt habituel du widget destinataire."""
		self.received.append("drop")
		event.acceptProposedAction()


##################################################
def create_drop_widget(monkeypatch):
	"""Crée un plugin dans un dock sans lecture, prévisualisation ni sauvegarde de paramètres."""
	monkeypatch.setattr(PALMTracerWidget, "_on_startup", lambda self: None)
	monkeypatch.setattr(PALMTracerWidget, "_connect_signal", lambda self: None)
	window = QMainWindow()
	receiver = DropReceiver()
	window.setCentralWidget(receiver)
	dock = QDockWidget(window)
	widget = PALMTracerWidget(ViewerModel())
	# Le modèle connecte lui-même la lecture de profondeur, indépendamment des signaux du widget.
	monkeypatch.setattr(widget.pt.settings.batch, "get_plane_count", lambda: None)
	dock.setWidget(widget)
	window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
	window.show()
	return widget, window, receiver, dock


##################################################
@pytest.fixture
def drop_widget(qtbot, monkeypatch):
	"""Enregistre la fenêtre de dépôt pour son nettoyage automatique par pytest-qt."""
	widgets = create_drop_widget(monkeypatch)
	qtbot.addWidget(widgets[1])
	return widgets


##################################################
def send_file_drop(receiver, mime):
	"""Envoie la séquence Qt d'entrée, de déplacement et de dépôt au destinataire."""
	enter = QDragEnterEvent(QPoint(1, 1), Qt.DropAction.CopyAction, mime, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier)
	move = QDragMoveEvent(QPoint(1, 1), Qt.DropAction.CopyAction, mime, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier)
	drop = QDropEvent(QPointF(1, 1), Qt.DropAction.CopyAction, mime, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier)
	for event in (enter, move, drop): QApplication.sendEvent(receiver, event)
	return enter, move, drop


# ==================================================
# region Initialisation
# ==================================================
##################################################
def test_creation(qtbot):
	"""Vérifie la création du widget."""
	SETTINGS_FILE.unlink(missing_ok=True)  # On supprime le fichier setting
	viewer = ViewerModel()
	w = PALMTracerWidget(viewer)
	qtbot.addWidget(w)


##################################################
def test_filters_button(qtbot):
	"""Vérifie le comportement du bouton de filtrage."""
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = ViewerModel()
	w = PALMTracerWidget(viewer)

	qtbot.addWidget(w)
	w.show()

	add_basic_file(w.pt)  # .									Ajout d'une entrée
	qtbot.waitUntil(lambda: not w._processing, timeout=5000)  # Attente : que le thread soit terminé

	# Activation d'un process
	w.pt.settings.localization.active = True
	qtbot.mouseClick(w.btn_process, Qt.MouseButton.LeftButton)
	qtbot.waitUntil(lambda: not w._processing, timeout=5000)  # Attente : que le thread soit terminé
	assert len(w.pt.results["loc"]) == 455
	assert len(w.pt.results["f_loc"]) == 0

	qtbot.mouseClick(w.btn_process, Qt.MouseButton.LeftButton)

	f = w.pt.settings.filters
	f.active = True
	ui_buttons = f.buttons[w.UI_NAME]
	print(ui_buttons)
	f["Plane"].active = True
	f["Plane"].max = 5
	print(f)

	tabs = w.findChild(QTabWidget)
	assert tabs is not None
	tabs.setCurrentIndex(2)  # Filtering
	qtbot.waitUntil(lambda: ui_buttons["update"].isVisible() and ui_buttons["update"].isEnabled(), timeout=5000)  # Attente : que l'onglet soit et actif

	qtbot.mouseClick(ui_buttons["update"], Qt.MouseButton.LeftButton)
	assert len(w.pt.results["loc"]) == 455
	assert len(w.pt.results["f_loc"]) == 242

	qtbot.mouseClick(ui_buttons["save"], Qt.MouseButton.LeftButton)
	f = FileIO.get_last_file(OUTPUT_FOLDER, "localizations_filtered")
	assert f

	qtbot.mouseClick(ui_buttons["reset"], Qt.MouseButton.LeftButton)
	assert len(w.pt.results["f_loc"]) == 0


# ==================================================
# endregion Initialisation
# ==================================================

# ==================================================
# region Glisser-déposer
# ==================================================
##################################################
def test_drop_filter_preserves_state_on_repeated_show(drop_widget, tmp_path):
	"""Vérifie qu'un affichage répété conserve le filtre et l'état à restaurer lors du masquage."""
	widget, window, receiver, dock = drop_widget
	dock.hide()
	window.setAcceptDrops(False)
	dock.show()

	QApplication.sendEvent(widget, QShowEvent())
	assert widget._drop_window is window
	path = tmp_path / "stack.tif"
	path.touch()
	mime = QMimeData()
	mime.setUrls([QUrl.fromLocalFile(str(path))])
	events = send_file_drop(receiver, mime)
	assert all(event.isAccepted() for event in events)
	assert receiver.received == []
	assert [Path(item) for item in widget.pt.settings.batch["Files"].items] == [path]

	dock.hide()
	assert not window.acceptDrops()


##################################################
@pytest.mark.parametrize("count", [1, 2], ids=["single-file", "multiple-files"])
@pytest.mark.parametrize("target", ["window", "plugin", "scroll"], ids=["window-content", "plugin-button", "scroll-viewport"])
def test_drop_adds_files_from_window(drop_widget, tmp_path, count, target):
	"""Vérifie l'ajout depuis un widget extérieur au plugin et l'interception avant son gestionnaire."""
	widget, window, receiver, _ = drop_widget
	paths = [tmp_path / name for name in ("z.tif", "a.txt")[:count]]
	for path in paths: path.touch()
	mime = QMimeData()
	mime.setUrls([QUrl.fromLocalFile(str(path)) for path in paths])

	targets = {"window": receiver, "plugin": widget.btn_process, "scroll": widget.findChild(QScrollArea).viewport()}
	events = send_file_drop(targets[target], mime)

	assert widget._drop_window is window
	assert all(event.isAccepted() for event in events)
	assert receiver.received == []
	files = widget.pt.settings.batch["Files"]
	assert [Path(path) for path in files.items] == sorted(paths, key=lambda path: str(path).casefold())
	assert files.value == count - 1


##################################################
@pytest.mark.parametrize("scenario", ["directory", "missing", "processing"], ids=["directory", "missing", "processing"])
def test_drop_rejects_unavailable_files(drop_widget, tmp_path, scenario):
	"""Vérifie le refus des dossiers, des fichiers absents et des dépôts pendant un traitement."""
	widget, _, receiver, _ = drop_widget
	path = tmp_path / "stack.tif"
	if scenario == "processing":
		path.touch()
		widget._processing = True
	elif scenario == "directory": path = tmp_path
	mime = QMimeData()
	mime.setUrls([QUrl.fromLocalFile(str(path))])

	events = send_file_drop(receiver, mime)

	assert not any(event.isAccepted() for event in events)
	assert receiver.received == []
	assert widget.pt.settings.batch["Files"].items == []


##################################################
@pytest.mark.parametrize("scenario", ["other-window", "remote-url", "text"], ids=["other-window", "remote-url", "internal-text"])
def test_drop_preserves_unrelated_events(drop_widget, qtbot, tmp_path, scenario):
	"""Vérifie que les autres fenêtres et les glissements sans fichier local gardent leurs événements."""
	widget, _, receiver, _ = drop_widget
	mime = QMimeData()
	if scenario == "other-window":
		receiver = DropReceiver()
		qtbot.addWidget(receiver)
		receiver.show()
		path = tmp_path / "stack.tif"
		path.touch()
		mime.setUrls([QUrl.fromLocalFile(str(path))])
	elif scenario == "remote-url": mime.setUrls([QUrl("https://example.com/stack.tif")])
	else: mime.setText("layer")

	send_file_drop(receiver, mime)

	assert receiver.received == ["enter", "drop"]
	assert widget.pt.settings.batch["Files"].items == []


##################################################
@pytest.mark.parametrize("initial_accepts", [False, True], ids=["drops-disabled", "drops-enabled"])
def test_drop_filter_follows_visibility(drop_widget, tmp_path, initial_accepts):
	"""Vérifie la désactivation au masquage puis la réactivation à l'affichage du même dock."""
	widget, window, receiver, dock = drop_widget
	dock.hide()
	window.setAcceptDrops(initial_accepts)
	dock.show()
	path = tmp_path / "stack.tif"
	path.touch()
	mime = QMimeData()
	mime.setUrls([QUrl.fromLocalFile(str(path))])

	dock.hide()
	assert widget._drop_window is None
	assert window.acceptDrops() == initial_accepts
	send_file_drop(receiver, mime)
	assert receiver.received == ["enter", "drop"]
	assert widget.pt.settings.batch["Files"].items == []

	receiver.received.clear()
	dock.show()
	send_file_drop(receiver, mime)
	assert receiver.received == []
	assert [Path(item) for item in widget.pt.settings.batch["Files"].items] == [path]


##################################################
def test_drop_filter_keeps_window_when_dock_floats(drop_widget, tmp_path):
	"""Vérifie que le détachement du dock conserve l'interception dans la fenêtre d'origine."""
	widget, window, receiver, dock = drop_widget
	dock.setFloating(True)
	path = tmp_path / "stack.tif"
	path.touch()
	mime = QMimeData()
	mime.setUrls([QUrl.fromLocalFile(str(path))])

	send_file_drop(receiver, mime)

	assert widget._drop_window is window
	assert receiver.received == []
	assert [Path(item) for item in widget.pt.settings.batch["Files"].items] == [path]


##################################################
@pytest.mark.parametrize("scenario", ["hide", "drop", "show"], ids=["hide-after-destruction", "drop-after-destruction", "show-after-destruction"])
def test_drop_filter_handles_deleted_window(drop_widget, tmp_path, scenario):
	"""Vérifie les événements tardifs lorsque la référence Python vise une fenêtre Qt déjà détruite."""
	widget, window, receiver, dock = drop_widget
	deleted_window = QMainWindow()
	deleted_window.deleteLater()
	QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
	assert not isalive(deleted_window)
	if scenario == "show": dock.hide()
	widget._drop_window = deleted_window

	if scenario == "hide":
		dock.hide()
		assert widget._drop_window is None
	elif scenario == "drop":
		path = tmp_path / "stack.tif"
		path.touch()
		mime = QMimeData()
		mime.setUrls([QUrl.fromLocalFile(str(path))])
		send_file_drop(receiver, mime)
		assert receiver.received == ["enter", "drop"]
		assert widget.pt.settings.batch["Files"].items == []
	else:
		dock.show()
		assert widget._drop_window is window


##################################################
def test_drop_filter_handles_parent_destruction(qtbot, monkeypatch):
	"""Vérifie la destruction réelle de la fenêtre et de son plugin sans exception dans la boucle Qt."""
	# Cette fenêtre est détruite explicitement ; pytest-qt ne doit pas tenter de la refermer.
	widget, window, _, _ = create_drop_widget(monkeypatch)
	window.deleteLater()
	QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)

	assert not isalive(window)
	assert not isalive(widget)


# ==================================================
# endregion Glisser-déposer
# ==================================================

# ==================================================
# region Threads
# ==================================================
##################################################
def test_thread_process(qtbot):
	"""Vérifie le clic sur le bouton process."""
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = ViewerModel()
	w = PALMTracerWidget(viewer)
	qtbot.addWidget(w)

	w._thread_process(w._auto_threshold)
	qtbot.waitUntil(lambda: not w._processing, timeout=5000)  # Attente : que le thread soit terminé

	# Appel avec un traitement en cours
	w._processing = True
	w._thread_process(w._auto_threshold)
	w._processing = False

	# Ajout d'une entrée
	add_basic_file(w.pt)  # .									Ajout d'une entrée
	qtbot.waitUntil(lambda: not w._processing, timeout=5000)  # Attente : que le thread soit terminé
	w._thread_process(w.pt.process)  # .						Appel de la méthode process
	qtbot.waitUntil(lambda: not w._processing, timeout=5000)  # Attente : que le thread soit terminé
	w._thread_process(w._auto_threshold)  # .					Appel de la méthode auto threshold mais impossible de l'executer dans ce contexte.
	qtbot.waitUntil(lambda: not w._processing, timeout=5000)  # Attente : que le thread soit terminé


# ==================================================
# endregion Threads
# ==================================================

# ==================================================
# region Fonctions de rappel des paramètres
# ==================================================
##################################################
def test_on_load_setting(qtbot, capsys, fake_qfiledialog):
	"""Vérifie la remise à zéro des calques."""
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = ViewerModel()
	w = PALMTracerWidget(viewer)
	qtbot.addWidget(w)

	fake_qfiledialog(PALMTracerWidget, None)  # Simuler un "Cancel" sur le QFileDialog
	w._on_load_setting_btn()


##################################################
def test_reset_setting(qtbot):
	"""Vérifie la remise à zéro des calques."""
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = ViewerModel()
	w = PALMTracerWidget(viewer)
	qtbot.addWidget(w)

	w._on_reset_setting_btn()


# ==================================================
# endregion Fonctions de rappel des paramètres
# ==================================================

# ==================================================
# region Fonctions de rappel des calques
# ==================================================
##################################################
def test_clean_layer(qtbot):
	"""Vérifie le nettoyage des calques."""
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = ViewerModel()
	w = PALMTracerWidget(viewer)
	qtbot.addWidget(w)

	w._layers["Points Present"].visible = False
	w._clean_layer()
	assert not w._layers["Points Present"].visible
	w._clean_layer(False, False, False)


##################################################
def test_reset_layer(capsys, qtbot):
	"""Vérifie la remise à zéro des calques."""
	clean_output()
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = ViewerModel()
	w = PALMTracerWidget(viewer)
	qtbot.addWidget(w)

	w._reset_layer()  # .											   Remise à 0 des calques sans fichier dans le batch.
	w._layers["Raw"].visible = False
	add_basic_file(w.pt)  # .										   Ajout d'une entrée
	qtbot.waitUntil(lambda: "Raw" in w.viewer.layers, timeout=5000)  # Attente : qu'il ait mis une image
	assert not w._layers["Raw"].visible
	lines = get_lines_output(capsys)
	assert len(lines) == 1
	assert "No valid settings file to load." == lines[0]
	w._reset_layer()  # .											   Remise à 0 des calques sans changement.


##################################################
def test_add_detection_layers(qtbot):
	"""Vérifie Ajout des calques de détection."""
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = ViewerModel()
	w = PALMTracerWidget(viewer)
	qtbot.addWidget(w)
	layers = w.viewer.layers

	w.pt.settings.localization["Preview"].value = True
	qtbot.waitUntil(lambda: w.pt.settings.localization["Preview"].value, timeout=5000)
	qtbot.waitUntil(lambda: not w._processing, timeout=5000)
	w.pt.settings.localization["ROI Shape"].value = 0
	qtbot.waitUntil(lambda: w.pt.settings.localization["ROI Shape"].value == 0, timeout=5000)
	qtbot.waitUntil(lambda: not w._processing, timeout=5000)

	# Ajout avec des tableaux normaux.
	w._layers["Points Present"].visible = False
	w._layers["ROI Present"].visible = False
	w._preview_locs = {"Past": POINTS, "Present": POINTS, "Future": POINTS, "Filtered": POINTS}
	w._add_preview_layers()
	qtbot.waitUntil(lambda: "Points Present" in layers, timeout=5000)
	assert len(w._layers["Points Past"].data) == 707
	assert not w._layers["Points Present"].visible
	assert not w._layers["ROI Present"].visible
	# Ajout avec des calques existants et un futur vide.
	w._preview_locs = {"Past": POINTS, "Present": POINTS, "Future": np.empty(0), "Filtered": np.empty(0)}
	w._add_preview_layers()
	assert len(w._layers["Points Future"].data) == 0

	# Ajout avec un tableau vide et rien en passé et future.
	w._preview_locs = {"Past": np.zeros((2, 0)), "Present": POINTS, "Future": np.empty(0), "Filtered": np.empty(0)}
	w._add_preview_layers()
	assert len(w._layers["Points Past"].data) == 0

	w.pt.settings.localization["ROI Shape"].value = 1
	qtbot.waitUntil(lambda: w.pt.settings.localization["ROI Shape"].value == 1, timeout=5000)
	qtbot.waitUntil(lambda: not w._processing, timeout=5000)
	w._preview_locs = {"Past": POINTS, "Present": POINTS, "Future": POINTS}
	w._add_preview_layers()
	assert len(w._layers["Points Future"].data) == 707


##################################################
def test_get_actual_image(qtbot):
	"""Vérifie la récupération d'image."""
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = ViewerModel()
	w = PALMTracerWidget(viewer)
	qtbot.addWidget(w)

	add_basic_file(w.pt)  # .															 Ajout d'une entrée
	qtbot.waitUntil(lambda: "Raw" in w.viewer.layers, timeout=5000)  # .				 Attente : qu'il ait mis une image
	assert w._get_actual_image() is not None, "Aucune image récupéré."  # .				 Récupéraiton de l'image
	assert w._get_actual_image(-100) is None, "Une image hors limite a été récupéré."  # Récupération d'une image hors limite
	assert w._get_actual_image(100) is None, "Une image hors limite a été récupéré."  # .Récupération d'une image hors limite


##################################################
def test_preview(capsys, qtbot):
	"""Vérifie le clic sur le bouton preview."""
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = ViewerModel()
	w = PALMTracerWidget(viewer)
	qtbot.addWidget(w)

	setting = w.pt.settings.localization
	layers = w.viewer.layers
	with setting.signal_blocked():  # L'éxecution ne devra pas être dans un sub-process pour vérifier la couverture (sans partir sur des configs complexes).
		w._preview()  # .										Passage si preview à False
		setting["Preview"].value = True
		qtbot.waitUntil(lambda: setting["Preview"].value, timeout=5000)
		w._preview()  # .										Passage par le point get_actual_image = None pour le temps présent.

	# Ajout d'une entrée
	add_basic_file(w.pt)  # .									Ajout d'une entrée.
	qtbot.waitUntil(lambda: "Raw" in layers, timeout=5000)  # .	Attente : qu'il ait mis une image.
	qtbot.waitUntil(lambda: not w._processing, timeout=5000)  # Attente : le flag doit passer à False.

	with setting.signal_blocked():
		setting["Preview"].value = True  # .					Le flag se remet à False à chaque changement de fichiers
		qtbot.waitUntil(lambda: setting["Preview"].value, timeout=5000)
		w._preview()  # .										Preview simple
		lines = get_lines_output(capsys)
		assert "Preview of plane 4 : 142 detected points (46 on the current frame, 48 on the previous frame, 48 on the next frame)." in lines[-1]

		setting["Fit"].value = 1
		setting["Gaussian Fit"]["Mode"].value = 3
		w._preview()
		lines = get_lines_output(capsys)
		assert lines[-4].startswith("Preview of plane 4 :")
		assert lines[-3].startswith("Sigma X mean:")
		assert "Sigma X median (robust):" in lines[-3]
		assert lines[-2].startswith("Sigma Y mean:")
		assert "Sigma Y median (robust):" in lines[-2]
		assert lines[-1].startswith("Theta mean:")
		assert "Theta median (robust):" in lines[-1]
		assert "Concentration R:" in lines[-1]

		setting["Gaussian Fit"]["Mode"].value = 0
		w._preview()
		lines = get_lines_output(capsys)
		assert lines[-1].startswith("Preview of plane 4 :")

		setting["Threshold"].value = 1000  # Plus aucune détection
		w._preview()
		lines = get_lines_output(capsys)
		assert lines[-1].startswith("Preview of plane 4 :")

		setting["Preview"].value = False
		w._preview()

	assert all(points.size == 0 for points in w._preview_locs.values())
	assert all(len(w._layers[name].data) == 0 for name in w.LAYERS_NAME[1:6])


##################################################
def test_preview_plane_filter_uses_stack_plane(qtbot):
	"""Vérifie que le filtre utilise les numéros réels des plans prévisualisés."""
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = ViewerModel()
	w = PALMTracerWidget(viewer)
	qtbot.addWidget(w)

	add_basic_file(w.pt)
	qtbot.waitUntil(lambda: "Raw" in viewer.layers, timeout=5000)
	qtbot.waitUntil(lambda: not w._processing, timeout=5000)
	viewer.dims.set_current_step(0, 4)  # Le cinquième plan a pour indice 4 dans Napari.

	setting = w.pt.settings.localization
	filters = w.pt.settings.filters
	with setting.signal_blocked(), filters.signal_blocked():
		setting["Preview"].value = True
		filters["Plane"].active = True
		filters["Plane"].value = [5, 5]
		w._preview()
		assert len(w._preview_locs["Present"]) > 0
		assert len(w._preview_locs["Filtered"]) == 0
		assert len(w._preview_locs["Past"]) == 0
		assert len(w._preview_locs["Future"]) == 0

		filters["Plane"].value = [4, 6]
		w._preview()
		assert len(w._preview_locs["Present"]) > 0
		assert len(w._preview_locs["Filtered"]) == 0
		assert len(w._preview_locs["Past"]) > 0
		assert len(w._preview_locs["Future"]) > 0


##################################################
def test_auto_threshold(capsys, qtbot):
	"""Vérifie le clic sur le bouton auto_threshold."""
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = ViewerModel()
	w = PALMTracerWidget(viewer)
	qtbot.addWidget(w)

	w._auto_threshold()  # .										   Appel de la méthode auto_threshold sans fichier dans le batch.

	# Ajout d'une entrée
	add_basic_file(w.pt)  # .										   Ajout d'une entrée
	qtbot.waitUntil(lambda: "Raw" in w.viewer.layers, timeout=5000)  # Attente : qu'il ait mis une image
	w._auto_threshold()  # .										   Appel de la méthode auto_threshold.

	lines = get_lines_output(capsys)
	assert "Auto Threshold: 63.95" in lines[-1]

# ==================================================
# endregion Fonctions de rappel des calques
# ==================================================
