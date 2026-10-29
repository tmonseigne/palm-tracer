"""Teste les comportements communs aux widgets Qt directement sur leur classe mère."""

from importlib import import_module
from pathlib import Path
from threading import Event, Thread, get_ident
from unittest.mock import Mock
from weakref import ref

import pytest
from qtpy.compat import isalive
from qtpy.QtCore import QCoreApplication, QEvent, QMimeData, QObject, QPoint, QPointF, QSize, Qt, QUrl
from qtpy.QtGui import QContextMenuEvent, QCursor, QDropEvent, QResizeEvent, QShowEvent
from qtpy.QtWidgets import QApplication, QDockWidget, QMainWindow, QVBoxLayout, QWidget

from palm_tracer.UI.BaseWidget import BaseWidget
from tests.Utils import DropReceiver, send_drop_events, send_file_drop, strip_ansi


# --------------------------------------------------
class _RecordingWidget(BaseWidget):
	"""Enregistre les chemins reçus sans effectuer de chargement métier."""

	UI_NAME: str = "Drop test"
	"""Nom utilisé pour vérifier le titre hérité."""

	# --------------------------------------------------
	def __init__(self, parent: QWidget | None = None):
		"""
		Initialise le widget et l'historique des dépôts.

		:param parent: Widget Qt parent éventuel.
		"""
		super().__init__(parent)
		self.received: list[list[Path]] = []

	# --------------------------------------------------
	def _drop_files(self, paths: list[str]):
		"""
		Mémorise les chemins délégués par la classe mère.

		:param paths: Chemins locaux validés par le filtre.
		"""
		self.received.append([Path(path) for path in paths])


# --------------------------------------------------
@pytest.fixture
def context_menu(monkeypatch):
	"""Remplace le menu à sa création afin qu'aucun test n'ouvre de boucle modale Qt."""
	menu = Mock()
	monkeypatch.setattr(import_module(BaseWidget.__module__), "QMenu", Mock(return_value=menu))
	return menu


# --------------------------------------------------
@pytest.fixture
def drop_widget(qtbot, monkeypatch):
	"""Crée une fenêtre et un destinataire enfant sans comportement métier de classe fille."""
	widget = BaseWidget()
	qtbot.addWidget(widget)
	receiver = DropReceiver()
	QVBoxLayout(widget).addWidget(receiver)
	calls = []
	monkeypatch.setattr(widget, "_drop_files", lambda paths: calls.append(paths.copy()))
	widget.show()
	return widget, receiver, calls


# --------------------------------------------------
@pytest.fixture
def notification_panel(qtbot):
	"""Crée un panneau visible afin d'observer ses notifications sans autre interface métier."""
	panel = BaseWidget()
	qtbot.addWidget(panel)
	panel.resize(600, 300)
	panel.show()
	return panel


# ==================================================
# region Fenêtres autonomes
# ==================================================
@pytest.mark.parametrize("dimensions", [(), (640, 480)], ids=["default-size", "custom-size"])
def test_standalone_window_lifetime(qtbot, monkeypatch, dimensions):
	"""Conserve une fenêtre affichée deux fois et libère sa référence commune après fermeture."""
	widget = BaseWidget()
	qtbot.addWidget(widget)
	identity = id(widget)
	reference = ref(widget)
	resize = Mock()
	monkeypatch.setattr(BaseWidget, "resize", resize)
	widget.show_standalone(*dimensions)
	widget.show_standalone(*dimensions)
	assert resize.call_count == 2
	resize.assert_called_with(*(dimensions or (1280, 720)))
	del widget
	window = reference()
	assert window is not None and window.isVisible()
	window.close()
	qtbot.waitUntil(lambda: not isalive(window))
	assert identity not in BaseWidget._standalone_windows


# ==================================================
# endregion Fenêtres autonomes
# ==================================================

# ==================================================
# region Threads
# ==================================================
def test_processing_disables_widget_and_ignores_relaunch(qtbot):
	"""Vérifie le calcul hors du thread Qt, le blocage des relances et la finalisation dans le thread graphique."""
	widget = BaseWidget()
	qtbot.addWidget(widget)
	widget.setCursor(Qt.CursorShape.CrossCursor)
	started, release = Event(), Event()
	threads = []
	gui_thread = get_ident()
	duplicate = Mock()

	# --------------------------------------------------
	def compute():
		"""Attend le signal du test pour laisser le temps de tenter une relance concurrente."""
		threads.append(get_ident())
		started.set()
		if not release.wait(timeout=20):
			raise TimeoutError("Le test n'a pas libéré le worker.")

	QApplication.setOverrideCursor(QCursor(Qt.CursorShape.CrossCursor))
	try:
		widget._thread_process(compute, lambda: threads.append(get_ident()))
		try:
			qtbot.waitUntil(started.is_set, timeout=10000)
			assert widget.processing and not widget.isEnabled()
			assert QApplication.overrideCursor().shape() == Qt.CursorShape.WaitCursor
			assert widget.updatesEnabled()
			widget._thread_process(duplicate)
		finally:
			release.set()
			qtbot.waitUntil(lambda: not widget.processing, timeout=10000)

		# Une fin répétée ne doit pas dépiler à nouveau le curseur de l'application.
		widget._process_done()
		assert QApplication.overrideCursor().shape() == Qt.CursorShape.CrossCursor
	finally:
		QApplication.restoreOverrideCursor()

	duplicate.assert_not_called()
	assert len(threads) == 2 and threads[0] != gui_thread and threads[1] == gui_thread
	assert widget.isEnabled() and widget.cursor().shape() == Qt.CursorShape.CrossCursor


# --------------------------------------------------
@pytest.mark.parametrize("stage", ["start", "compute", "finalize"], ids=["start-failure", "compute-failure", "finalization-failure"])
def test_processing_error_restores_widget(qtbot, monkeypatch, stage):
	"""Vérifie la notification d'erreur et la réactivation après échec du lancement, du calcul ou de sa finalisation."""
	widget = BaseWidget()
	qtbot.addWidget(widget)
	widget.setCursor(Qt.CursorShape.CrossCursor)
	error = RuntimeError(f"Failure during {stage}")
	notify = Mock()
	monkeypatch.setattr(widget, "notify_error", notify)
	previous_cursor = QApplication.overrideCursor()
	compute = Mock(side_effect=error if stage == "compute" else None)
	finalize = Mock(side_effect=error if stage == "finalize" else None)
	if stage == "start":
		monkeypatch.setattr(import_module(BaseWidget.__module__), "FunctionWorker", Mock(side_effect=error))

	widget._thread_process(compute, finalize)
	qtbot.waitUntil(lambda: not widget.processing, timeout=10000)

	notify.assert_called_once_with(f"Error in thread: {error}")
	assert widget.isEnabled() and widget.cursor().shape() == Qt.CursorShape.CrossCursor
	current_cursor = QApplication.overrideCursor()
	assert (current_cursor.shape() if current_cursor else None) == (previous_cursor.shape() if previous_cursor else None)
	if stage != "finalize": finalize.assert_not_called()


# --------------------------------------------------
def test_processing_preserves_initial_disabled_state(qtbot):
	"""Vérifie qu'un calcul déclenché par programme ne réactive pas un widget déjà désactivé."""
	widget = BaseWidget()
	qtbot.addWidget(widget)
	widget.setEnabled(False)
	widget._thread_process(lambda: None)
	qtbot.waitUntil(lambda: not widget.processing, timeout=10000)
	assert not widget.isEnabled()


# ==================================================
# endregion Threads
# ==================================================

# ==================================================
# region Notifications
# ==================================================
@pytest.mark.parametrize("level", ["info", "success", "warning", "error"], ids=["information", "success", "warning", "error"])
def test_notification_prints_once_and_displays_level(notification_panel, capsys, level):
	"""Vérifie qu'un appel unique produit le texte console et la notification du niveau demandé."""
	getattr(notification_panel, f"notify_{level}")("Message <b>brut</b>", duration_ms=0)
	notification = notification_panel._notification
	assert notification.isVisible()
	assert notification.property("level") == level
	assert notification._message.text() == "Message <b>brut</b>"
	assert strip_ansi(capsys.readouterr().out).splitlines() == ["Message <b>brut</b>"]


# --------------------------------------------------
@pytest.mark.parametrize("level, duration", [("unknown", 4000), ("info", -1)], ids=["unknown-level", "negative-duration"])
def test_notification_rejects_invalid_options(notification_panel, capsys, level, duration):
	"""Vérifie la validation avant toute écriture console ou création de notification."""
	with pytest.raises(ValueError): notification_panel.notify("Invalide", level, duration)
	assert capsys.readouterr().out == ""


# --------------------------------------------------
def test_notification_is_delivered_from_worker(notification_panel, qtbot):
	"""Vérifie qu'une demande d'un thread Python crée le composant uniquement dans le thread du panneau."""
	worker = Thread(target=notification_panel.notify_warning, args=("Message du worker",), kwargs={"duration_ms": 0})
	worker.start()
	worker.join(timeout=10)
	assert not worker.is_alive()
	qtbot.waitUntil(lambda: notification_panel._notification is not None, timeout=10000)
	notification = notification_panel._notification
	assert notification.thread() is notification_panel.thread()
	assert notification._message.text() == "Message du worker"
	assert notification.isVisible()


# --------------------------------------------------
def test_hidden_panel_only_prints_message(qtbot, capsys):
	"""Conserve le diagnostic console sans créer de notification pour un panneau masqué."""
	panel = BaseWidget()
	qtbot.addWidget(panel)
	panel.notify_error("Panneau masqué")
	assert panel._notification is None
	assert strip_ansi(capsys.readouterr().out).splitlines() == ["Panneau masqué"]


# --------------------------------------------------
def test_hiding_panel_cancels_notification(notification_panel):
	"""Vérifie qu'un panneau masqué puis réaffiché ne montre pas un ancien message."""
	notification_panel.notify_info("Ancien message")
	notification = notification_panel._notification
	notification_panel.hide()
	notification_panel.show()
	assert not notification.isVisible()


# --------------------------------------------------
def test_show_notification_reuses_existing_widget(notification_panel):
	"""Remplace le message dans la notification déjà créée, sans multiplier les composants."""
	notification_panel.notify_info("Premier message", duration_ms=0)
	notification = notification_panel._notification
	notification_panel.notify_error("Message suivant", duration_ms=0)
	assert notification_panel._notification is notification
	assert notification._message.text() == "Message suivant"


# --------------------------------------------------
def test_resize_repositions_notification(notification_panel, monkeypatch):
	"""Délègue le repositionnement au composant lorsqu'un événement de redimensionnement est reçu."""
	notification_panel.notify_info("Message", duration_ms=0)
	reposition = Mock()
	monkeypatch.setattr(notification_panel._notification, "reposition", reposition)
	notification_panel.resizeEvent(QResizeEvent(QSize(400, 200), notification_panel.size()))
	reposition.assert_called_once_with()


# ==================================================
# endregion Notifications
# ==================================================

# ==================================================
# region Menu contextuel
# ==================================================
@pytest.mark.parametrize("host", ["standalone", "embedded", "docked", "floating"],
						 ids=["standalone", "embedded-widget", "docked-panel", "floating-panel"])
def test_always_on_top_targets_only_independent_window(qtbot, host):
	"""Vérifie que seul le widget autonome ou son dock flottant est ciblé, sans remonter à la fenêtre principale."""
	widget = BaseWidget()
	if host == "standalone":
		window, expected = widget, widget
	else:
		window = QMainWindow()
		if host == "embedded":
			window.setCentralWidget(widget)
			expected = None
		else:
			dock = QDockWidget(window)
			dock.setWidget(widget)
			window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
			dock.setFloating(host == "floating")
			expected = dock if host == "floating" else None
	qtbot.addWidget(window)

	assert widget._get_always_on_top_target() is expected


# --------------------------------------------------
@pytest.mark.parametrize("visible", [False, True], ids=["hidden-window", "visible-window"])
def test_always_on_top_preserves_window_state(qtbot, monkeypatch, visible):
	"""Vérifie nos appels de restauration sans solliciter le gestionnaire de fenêtres du système."""
	widget = BaseWidget()
	qtbot.addWidget(widget)
	window = Mock()
	window.windowFlags.return_value = Qt.WindowType.Widget
	window.isVisible.return_value = visible
	monkeypatch.setattr(widget, "_get_always_on_top_target", lambda: window)

	widget._set_always_on_top(True)

	window.setWindowFlag.assert_called_once_with(Qt.WindowType.WindowStaysOnTopHint, True)
	window.setGeometry.assert_called_once_with(window.geometry.return_value)
	if visible: window.show.assert_called_once_with()
	else: window.show.assert_not_called()


# --------------------------------------------------
@pytest.mark.parametrize("pinned", [False, True], ids=["unchecked", "checked"])
def test_context_menu_configures_always_on_top(qtbot, monkeypatch, context_menu, pinned):
	"""Vérifie l'état transmis à l'action et sa connexion au gestionnaire du panneau."""
	widget = BaseWidget()
	qtbot.addWidget(widget)
	flags = Qt.WindowType.WindowStaysOnTopHint if pinned else Qt.WindowType.Widget
	monkeypatch.setattr(widget, "windowFlags", lambda: flags)
	toggle = Mock()
	monkeypatch.setattr(widget, "_set_always_on_top", toggle)

	widget.contextMenuEvent(QContextMenuEvent(QContextMenuEvent.Reason.Mouse, QPoint(1, 1), QPoint(20, 20)))

	context_menu.addAction.assert_called_once_with("Always on top")
	action = context_menu.addAction.return_value
	action.setChecked.assert_called_once_with(pinned)
	action.setEnabled.assert_called_once_with(True)
	action.toggled.connect.assert_called_once_with(toggle)


# --------------------------------------------------
def test_context_menu_is_disabled_in_docked_panel(qtbot, context_menu):
	"""Vérifie que notre menu désactive l'option dans un panneau intégré à Napari."""
	window = QMainWindow()
	qtbot.addWidget(window)
	dock = QDockWidget(window)
	widget = BaseWidget()
	dock.setWidget(widget)
	window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

	widget.contextMenuEvent(QContextMenuEvent(QContextMenuEvent.Reason.Mouse, QPoint(1, 1), QPoint(20, 20)))

	context_menu.addAction.return_value.setEnabled.assert_called_once_with(False)


# --------------------------------------------------
def test_context_menu_preserves_excluded_view(qtbot, context_menu):
	"""Vérifie qu'un événement remontant d'une vue exclue ne déclenche pas le menu du panneau."""
	widget = BaseWidget()
	qtbot.addWidget(widget)
	view = QWidget(widget)
	view.setGeometry(0, 0, 100, 100)
	widget._context_menu_exclusions.append(view)
	widget.show()
	event = QContextMenuEvent(QContextMenuEvent.Reason.Mouse, QPoint(10, 10), QPoint(20, 20))
	widget.contextMenuEvent(event)
	assert not event.isAccepted()
	context_menu.exec.assert_not_called()


# --------------------------------------------------
@pytest.mark.parametrize("available", [False, True], ids=["no-independent-window", "already-pinned"])
def test_always_on_top_ignores_unnecessary_change(qtbot, monkeypatch, available):
	"""Évite de modifier une fenêtre indisponible ou déjà maintenue au premier plan."""
	widget = BaseWidget()
	qtbot.addWidget(widget)
	window = Mock()
	window.windowFlags.return_value = Qt.WindowType.WindowStaysOnTopHint
	monkeypatch.setattr(widget, "_get_always_on_top_target", lambda: window if available else None)
	widget._set_always_on_top(True)
	window.setWindowFlag.assert_not_called()


# ==================================================
# endregion Menu contextuel
# ==================================================

# ==================================================
# region Glisser-déposer
# ==================================================
@pytest.mark.parametrize("host", ["standalone", "embedded", "docked", "floating"],
						 ids=["standalone", "embedded-window", "docked-panel", "floating-panel"])
@pytest.mark.parametrize("target", ["window", "sibling"], ids=["whole-window", "outside-panel"])
def test_drop_reaches_handler_from_whole_window(qtbot, tmp_path, host, target):
	"""Vérifie la délégation unique sur toute la fenêtre, au-delà du panneau contenant l'outil."""
	widget = _RecordingWidget()
	if host == "standalone":
		window = widget
		QVBoxLayout(window)
	elif host == "embedded":
		window = QWidget()
		QVBoxLayout(window).addWidget(widget)
	else:
		window = QMainWindow()
		dock = QDockWidget(window)
		dock.setWidget(widget)
		window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
	qtbot.addWidget(window)
	receiver = QWidget(window)
	receiver.setAcceptDrops(True)
	if isinstance(window, QMainWindow): window.setCentralWidget(receiver)
	else: window.layout().addWidget(receiver)
	window.show()
	if host == "floating": dock.setFloating(True)
	path = tmp_path / "stack.tif"
	path.touch()

	events, _mime = send_file_drop(window if target == "window" else receiver, [path])

	assert all(event.isAccepted() for event in events)
	assert widget.received == [[path]]


# --------------------------------------------------
@pytest.mark.parametrize("initial_accepts", [False, True], ids=["drops-disabled", "drops-enabled"])
def test_drop_filter_restores_window_after_hiding(qtbot, tmp_path, initial_accepts):
	"""Vérifie la restauration de l'acceptation initiale et la réinstallation après réaffichage."""
	widget = _RecordingWidget()
	qtbot.addWidget(widget)
	widget.setAcceptDrops(initial_accepts)
	widget.show()
	assert widget.acceptDrops()
	QApplication.sendEvent(widget, QShowEvent())
	widget.hide()
	assert widget.acceptDrops() == initial_accepts
	widget.show()
	path = tmp_path / "stack.tif"
	path.touch()
	send_file_drop(widget, [path])
	assert widget.received == [[path]]


# --------------------------------------------------
def test_drop_requires_specialized_handler(qtbot, tmp_path):
	"""Vérifie que la base reste instanciable et impose une action seulement lors de son appel."""
	widget = BaseWidget()
	qtbot.addWidget(widget)
	path = tmp_path / "stack.tif"
	with pytest.raises(NotImplementedError, match="traitement des fichiers"):
		widget._drop_files([str(path)])


# --------------------------------------------------
@pytest.mark.parametrize("scenario, accepted", [
		pytest.param("tiff", True, id="tiff-stack"),
		pytest.param("stk", True, id="uppercase-stk"),
		pytest.param("unsupported", False, id="unsupported-extension"),
		pytest.param("directory", False, id="directory-disabled"),
		pytest.param("allowed-directory", True, id="directory-enabled"),
		pytest.param("mixed-invalid", False, id="mixed-invalid-batch")])
def test_drop_filters_paths_before_dispatch(qtbot, tmp_path, scenario, accepted):
	"""Vérifie le filtrage des extensions, des dossiers et des lots contenant un chemin invalide."""
	widget = _RecordingWidget()
	qtbot.addWidget(widget)
	widget.DROP_EXTENSIONS = (".tif", ".tiff", ".stk")
	widget.DROP_DIRECTORIES = scenario == "allowed-directory"
	widget.show()
	path = tmp_path / {"tiff": "stack.tiff", "stk": "stack.STK", "unsupported": "data.csv"}.get(scenario, "stack.tif")
	path.touch()
	paths = [tmp_path] if "directory" in scenario else [path]
	if scenario == "mixed-invalid": paths.append(tmp_path / "missing.tif")

	events, _mime = send_file_drop(widget, paths)

	assert all(event.isAccepted() == accepted for event in events)
	assert widget.received == ([paths] if accepted else [])


# --------------------------------------------------
@pytest.mark.parametrize("target", ["window", "child"], ids=["root-window", "child-widget"])
@pytest.mark.parametrize("scenario", ["single", "single-only", "multiple", "mixed"],
						 ids=["single-file", "single-file-only", "multiple-files", "local-and-remote"])
def test_drop_delivers_local_files_once(drop_widget, tmp_path, monkeypatch, target, scenario):
	"""Vérifie l'acceptation du glissement et la délégation des seuls chemins locaux au dépôt."""
	widget, receiver, calls = drop_widget
	first, second = tmp_path / "first.tif", tmp_path / "second.tif"
	for path in (first, second): path.touch()
	monkeypatch.setattr(widget, "DROP_MULTIPLE", scenario != "single-only")
	urls = [QUrl.fromLocalFile(str(first))]
	if scenario == "multiple": urls.append(QUrl.fromLocalFile(str(second)))
	elif scenario == "mixed": urls.append(QUrl("https://example.com/stack.tif"))
	mime = QMimeData()
	mime.setUrls(urls)

	events = send_drop_events(widget if target == "window" else receiver, mime)

	assert all(event.isAccepted() for event in events)
	assert all(event.dropAction() == Qt.DropAction.CopyAction for event in events)
	assert [[Path(path) for path in paths] for paths in calls] == [[first, second] if scenario == "multiple" else [first]]
	assert receiver.received == []


# --------------------------------------------------
@pytest.mark.parametrize("scenario", ["multiple", "mixed", "directory", "missing"],
						 ids=["multiple-files", "local-and-remote", "directory", "missing-file"])
def test_drop_rejects_invalid_files(drop_widget, tmp_path, monkeypatch, scenario):
	"""Vérifie les contraintes sur le nombre de fichiers et leur existence."""
	widget, receiver, calls = drop_widget
	path = tmp_path / "stack.tif"
	path.touch()
	monkeypatch.setattr(widget, "DROP_MULTIPLE", False)
	urls = {"multiple":  [QUrl.fromLocalFile(str(path))] * 2,
			"mixed":     [QUrl.fromLocalFile(str(path)), QUrl("https://example.com/stack.tif")],
			"directory": [QUrl.fromLocalFile(str(tmp_path))],
			"missing":   [QUrl.fromLocalFile(str(tmp_path / "missing.tif"))]}
	mime = QMimeData()
	mime.setUrls(urls[scenario])

	events = send_drop_events(receiver, mime)

	assert not any(event.isAccepted() for event in events)
	assert calls == []
	assert receiver.received == []


# --------------------------------------------------
@pytest.mark.parametrize("scenario", ["other-window", "remote", "text"], ids=["other-window", "remote-url", "internal-text"])
def test_drop_preserves_unrelated_events(drop_widget, qtbot, tmp_path, scenario):
	"""Vérifie que les autres fenêtres et les glissements sans fichier local suivent leur traitement habituel."""
	_, receiver, calls = drop_widget
	mime = QMimeData()
	if scenario == "other-window":
		receiver = DropReceiver()
		qtbot.addWidget(receiver)
		receiver.show()
		path = tmp_path / "stack.tif"
		path.touch()
		mime.setUrls([QUrl.fromLocalFile(str(path))])
	elif scenario == "remote": mime.setUrls([QUrl("https://example.com/stack.tif")])
	else: mime.setText("layer")

	send_drop_events(receiver, mime)

	assert receiver.received == ["enter", "drop"]
	assert calls == []


# --------------------------------------------------
@pytest.mark.parametrize("scenario", ["hidden", "deleted", "non-widget"], ids=["hidden-window", "deleted-window", "non-widget-receiver"])
def test_drop_ignores_inactive_target(qtbot, tmp_path, monkeypatch, scenario):
	"""Vérifie les événements tardifs et les destinataires dépourvus d'interface QWidget."""
	widget = BaseWidget()
	qtbot.addWidget(widget)
	widget.show()
	receiver = widget
	if scenario == "hidden": widget.hide()
	elif scenario == "deleted":
		window = QWidget()
		window.deleteLater()
		QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
		widget._drop_window = window
	else: receiver = QObject(widget)
	path = tmp_path / "stack.tif"
	path.touch()
	mime = QMimeData()
	mime.setUrls([QUrl.fromLocalFile(str(path))])
	drop = QDropEvent(QPointF(1, 1), Qt.DropAction.CopyAction, mime, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier)
	calls: list[list[str]] = []
	monkeypatch.setattr(widget, "_drop_files", calls.append)

	# Le filtre a déjà été retiré après masquage ; on simule directement l'événement tardif.
	assert not widget.eventFilter(receiver, drop)
	assert not drop.isAccepted()
	assert calls == []


# --------------------------------------------------
@pytest.mark.parametrize("scenario", ["hide", "show"], ids=["hide-after-destruction", "show-after-destruction"])
def test_drop_filter_handles_deleted_window(drop_widget, scenario):
	"""Vérifie le masquage et le ré-affichage après destruction de la fenêtre mémorisée."""
	widget, _, calls = drop_widget
	window = QWidget()
	window.deleteLater()
	QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
	if scenario == "show": widget.hide()
	widget._drop_window = window

	if scenario == "hide":
		widget.hide()
		assert widget._drop_window is None
	else:
		widget.show()
		assert widget._drop_window is widget
	assert calls == []

# ==================================================
# endregion Glisser-déposer
# ==================================================
