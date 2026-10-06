"""Teste le widget de visualisation interactive des données PALM."""

import pytest
from qtpy.compat import isalive
from qtpy.QtCore import QCoreApplication, QEvent, QMimeData, QObject, QPoint, QPointF, Qt, QUrl
from qtpy.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent, QShowEvent
from qtpy.QtWidgets import QApplication, QPushButton, QScrollArea

from palm_tracer._tests.Utils import *
from palm_tracer.PALMTracer import PALMTracer
from palm_tracer.Settings.Types import BaseUIType, ButtonGroup, Combo, FileList
from palm_tracer.UI import GraphViewerWidget

OUTPUT_DIR = INPUT_DIR / "stack_PALM_Tracer"
INPUT_FILE = INPUT_DIR / "stack.tif"
SIZE_X, SIZE_Y, INTENSITY, RATIO = 100, 50, 1000, 10
SIZE = int(SIZE_X * np.sqrt(SIZE_Y))
rng = np.random.default_rng(42)  # Générateur propre au jeu de données de ce module.
POINTS = np.stack([rng.uniform(1, SIZE_Y - 1, size=SIZE), rng.uniform(1, SIZE_X - 1, size=SIZE)], axis=1)


##################################################
@pytest.fixture
def stack_drop_widget(qtbot, monkeypatch):
	"""Observe les dépôts dans une fenêtre autonome sans construire de rendu WebEngine."""
	monkeypatch.setattr(GraphViewerWidget, "_make_web_widget", lambda self: DropReceiver(self))
	monkeypatch.setattr(GraphViewerWidget, "_connect_web_widget", lambda self: None)
	monkeypatch.setattr(GraphViewerWidget, "_update_plot", lambda self: None)
	widget = GraphViewerWidget(PALMTracer())
	qtbot.addWidget(widget)
	calls = []
	files = cast(FileList, widget.pt.settings.batch["Files"])
	monkeypatch.setattr(widget.pt, "load", lambda path="": calls.append(("load", Path(path))))
	monkeypatch.setattr(widget, "_update_plot", lambda: calls.append(("plot", Path(files.current_text))))
	widget.show()
	return widget, calls


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
def w() -> GraphViewerWidget:
	"""Instance fraîche de GraphViewerWidget pour chaque test."""
	pt = get_fake_pt()
	w = GraphViewerWidget(pt)
	return w


##################################################
def flush_qt_delete_events():
	"""Traite les événements Qt de suppression différée."""
	QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
	QCoreApplication.processEvents()


# ==================================================
# region Initialisation
# ==================================================
##################################################
def test_widget_creation(w: GraphViewerWidget, qtbot):
	"""Vérifie la création du widget."""
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)
	w.close()


##################################################
def test_results_status_automatic_update(w: GraphViewerWidget, qtbot):
	"""Vérifie que les statuts sont actualisés directement par Results."""
	qtbot.addWidget(w)
	results_ui = w.pt.results.get_ui(w.UI_NAME)

	w.pt.results.reset()
	assert results_ui.labels["Localizations"].text() == "No"

	w.pt.results["loc"] = pd.DataFrame(np.zeros((2, 1)))
	assert results_ui.labels["Localizations"].text() == "Yes (2 localizations)"


##################################################
def test_widget_double_creation(qtbot):
	"""Vérifie Permettant de gérer la création en doublon de la même UI."""

	"""Reproduit le cas où une UI Qt cachée dans un dict survit à la destruction C++."""
	pt = get_fake_pt()

	w = GraphViewerWidget(pt)
	w.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	w.close()
	flush_qt_delete_events()

	# Ici les BaseUI sont encore dans les settings, mais leurs objets Qt internes peuvent être supprimés côté C++.
	w2 = GraphViewerWidget(pt)
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
@pytest.mark.parametrize("scenario", ["hidden", "deleted", "non-widget"], ids=["hidden-window", "deleted-window", "non-widget-receiver"])
def test_stack_drop_ignores_inactive_target(stack_drop_widget, scenario):
	"""Vérifie qu'un événement tardif ou sans destinataire QWidget n'est pas intercepté."""
	widget, calls = stack_drop_widget
	receiver = widget._web
	if scenario == "hidden": widget.hide()
	elif scenario == "deleted":
		window = QWidget()
		window.deleteLater()
		QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
		assert not isalive(window)
		widget._drop_window = window
	else: receiver = QObject(widget)
	mime = QMimeData()
	mime.setUrls([QUrl.fromLocalFile(str(INPUT_FILE))])
	drop = QDropEvent(QPointF(1, 1), Qt.DropAction.CopyAction, mime, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier)

	# Après masquage, le filtre est retiré de l'application : on simule directement un événement tardif.
	assert not widget.eventFilter(receiver, drop)
	assert not drop.isAccepted()
	assert widget.pt.settings.batch["Files"].items == []
	assert calls == []


##################################################
@pytest.mark.parametrize("target", ["window", "button", "scroll", "graph"], ids=["window", "action-button", "scroll-viewport", "graph-area"])
def test_stack_drop_loads_latest_results_and_redraws(stack_drop_widget, target):
	"""Vérifie l'ajout, le chargement du dossier des résultats et le tracé depuis chaque zone."""
	widget, calls = stack_drop_widget
	mime = QMimeData()
	mime.setUrls([QUrl.fromLocalFile(str(INPUT_FILE))])
	targets = {"window": widget, "button": widget._btn_actualize, "scroll": widget.findChild(QScrollArea).viewport(), "graph": widget._web}

	events = send_stack_drop(targets[target], mime)

	assert widget._drop_window is widget
	assert all(event.isAccepted() for event in events)
	assert widget._web.received == []
	assert [Path(path) for path in widget.pt.settings.batch["Files"].items] == [INPUT_FILE]
	assert calls == [("load", OUTPUT_DIR), ("plot", INPUT_FILE)]
	assert all(button.text() != "Add Stack" for button in widget.findChildren(QPushButton))


##################################################
@pytest.mark.parametrize("scenario", ["multiple", "mixed", "directory", "missing"], ids=["multiple-files", "local-and-remote", "directory", "missing-file"])
def test_stack_drop_rejects_invalid_batch(stack_drop_widget, tmp_path, scenario):
	"""Vérifie qu'un dépôt refusé ne modifie pas le Batch et ne redessine pas le graphe."""
	widget, calls = stack_drop_widget
	urls = {"multiple":  [QUrl.fromLocalFile(str(INPUT_FILE))] * 2,
			"mixed":     [QUrl.fromLocalFile(str(INPUT_FILE)), QUrl("https://example.com/stack.tif")],
			"directory": [QUrl.fromLocalFile(str(tmp_path))],
			"missing":   [QUrl.fromLocalFile(str(tmp_path / "missing.tif"))]}
	mime = QMimeData()
	mime.setUrls(urls[scenario])

	events = send_stack_drop(widget._web, mime)

	assert not any(event.isAccepted() for event in events)
	assert widget._web.received == []
	assert widget.pt.settings.batch["Files"].items == []
	assert calls == []


##################################################
@pytest.mark.parametrize("scenario", ["other-window", "remote", "text"], ids=["other-window", "remote-url", "internal-text"])
def test_stack_drop_preserves_unrelated_events(stack_drop_widget, qtbot, scenario):
	"""Vérifie que le filtre laisse les autres fenêtres et les glissements sans fichier local inchangés."""
	widget, calls = stack_drop_widget
	receiver = widget._web
	mime = QMimeData()
	if scenario == "other-window":
		receiver = DropReceiver()
		qtbot.addWidget(receiver)
		receiver.show()
		mime.setUrls([QUrl.fromLocalFile(str(INPUT_FILE))])
	elif scenario == "remote": mime.setUrls([QUrl("https://example.com/stack.tif")])
	else: mime.setText("graph")

	send_stack_drop(receiver, mime)

	assert receiver.received == ["enter", "drop"]
	assert widget.pt.settings.batch["Files"].items == []
	assert calls == []


##################################################
@pytest.mark.parametrize("initial_accepts", [False, True], ids=["drops-disabled", "drops-enabled"])
def test_stack_drop_follows_visibility(stack_drop_widget, initial_accepts):
	"""Vérifie la restauration des dépôts et l'installation du filtre après ré-affichage."""
	widget, calls = stack_drop_widget
	widget.hide()
	widget.setAcceptDrops(initial_accepts)
	widget.show()
	QApplication.sendEvent(widget, QShowEvent())
	widget.hide()
	assert widget._drop_window is None
	assert widget.acceptDrops() == initial_accepts
	widget.show()
	mime = QMimeData()
	mime.setUrls([QUrl.fromLocalFile(str(INPUT_FILE))])

	send_stack_drop(widget._web, mime)

	assert widget._web.received == []
	assert calls == [("load", OUTPUT_DIR), ("plot", INPUT_FILE)]


# ==================================================
# endregion Glisser-déposer
# ==================================================

# ==================================================
# region Liaison avec PALMTracer
# ==================================================
##################################################
def test_change_type(w: GraphViewerWidget, qtbot):
	"""Vérifie la création du widget."""
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	ui: BaseUIType = cast(ButtonGroup, w.pt.settings.graph["Type"]).get_ui(w.UI_NAME)
	qtbot.mouseClick(ui.boxes[0], Qt.MouseButton.LeftButton)  # Appuie sur localization
	assert w.pt.settings.graph["Type"].value == 0
	qtbot.mouseClick(ui.boxes[1], Qt.MouseButton.LeftButton)  # Appuie sur Tracks
	assert w.pt.settings.graph["Type"].value == 1

	w.close()


##################################################
@pytest.mark.parametrize("mode", [0, 1, 2], ids=["only-one", "each-file", "all-in-one"])
def test_add_stack_uses_dropped_results_folder(stack_drop_widget, tmp_path, mode):
	"""Vérifie que le chargement utilise la pile ajoutée malgré une autre pile déjà présente."""
	widget, calls = stack_drop_widget
	files = cast(FileList, widget.pt.settings.batch["Files"])
	files.items = [str(tmp_path / "first.tif")]
	widget.pt.settings.batch["Mode"].value = mode

	widget._add_stack(str(INPUT_FILE))

	assert Path(files.current_text) == INPUT_FILE
	assert calls == [("load", OUTPUT_DIR), ("plot", INPUT_FILE)]


##################################################
def test_update_plot_localization(w: GraphViewerWidget, qtbot, capsys):
	"""Vérifie différentes visualizations."""
	qtbot.addWidget(w)
	w.resize(1000, 600)
	w.show()
	qtbot.waitExposed(w)

	s = w.pt.settings.graph
	ui: BaseUIType = cast(ButtonGroup, s["Type"]).get_ui(w.UI_NAME)
	qtbot.mouseClick(ui.boxes[0], Qt.MouseButton.LeftButton)  # Appuie sur localization
	assert w.pt.settings.graph["Type"].value == 0

	# Changement de source
	s["Source"].value = 1  # Changement de graph
	s["Source"].value = len(cast(Combo, s["Source"]).items) - 1  # Localisation Count est un affichage Scatter Plot

	# Dual View
	s["Mode"].value = 2
	s["Source"].value = 1
	s["Source B"].value = 2

	w.close()

# ==================================================
# endregion Liaison avec PALMTracer
# ==================================================
