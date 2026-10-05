"""Teste les références partagées et les gardes Qt de la base des widgets Napari."""

from importlib import import_module
from pathlib import Path

import pytest
from napari.components import ViewerModel
from qtpy.compat import isalive
from qtpy.QtCore import QCoreApplication, QEvent, QMimeData, QObject, QPoint, QPointF, Qt, QUrl
from qtpy.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent, QShowEvent
from qtpy.QtWidgets import QApplication, QDockWidget, QMainWindow, QVBoxLayout, QWidget

from palm_tracer.PALMTracer import PALMTracer
from palm_tracer.UI import BaseNapariWidget


##################################################
class _DropReceiver(QWidget):
	"""Enregistre les événements que le filtre laisse au destinataire habituel."""

	def __init__(self):
		"""Initialise l'acceptation des dépôts et leur historique."""
		super().__init__()
		self.received = []
		self.setAcceptDrops(True)

	def dragEnterEvent(self, event):
		"""Accepte le glissement non intercepté."""
		self.received.append("enter")
		event.acceptProposedAction()

	def dropEvent(self, event):
		"""Enregistre le dépôt non intercepté."""
		self.received.append("drop")
		event.acceptProposedAction()


##################################################
@pytest.fixture
def drop_widget(qtbot, monkeypatch):
	"""Crée une fenêtre et un destinataire enfant sans comportement métier de classe fille."""
	widget = BaseNapariWidget(ViewerModel())
	qtbot.addWidget(widget)
	receiver = _DropReceiver()
	QVBoxLayout(widget).addWidget(receiver)
	calls = []
	monkeypatch.setattr(widget, "_drop_files", lambda paths: calls.append(paths.copy()))
	widget.show()
	return widget, receiver, calls


##################################################
def send_file_drop(receiver, mime):
	"""Envoie la séquence Qt complète d'entrée, de déplacement et de dépôt."""
	enter = QDragEnterEvent(QPoint(1, 1), Qt.DropAction.CopyAction, mime, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier)
	move = QDragMoveEvent(QPoint(1, 1), Qt.DropAction.CopyAction, mime, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier)
	drop = QDropEvent(QPointF(1, 1), Qt.DropAction.CopyAction, mime, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier)
	for event in (enter, move, drop): QApplication.sendEvent(receiver, event)
	return enter, move, drop


##################################################
class _DummyLayer:
	"""Simule un calque et mémorise sa visibilité lors des affectations."""

	def __init__(self, visible: bool, invalid_property: str = ""):
		"""
		Initialise le calque avec l'état demandé.

		:param visible: Visibilité initiale du calque.
		:param invalid_property: Nom de la propriété dont l'affectation doit échouer.
		"""
		object.__setattr__(self, "visible", visible)
		object.__setattr__(self, "data", "old-data")
		object.__setattr__(self, "invalid_property", invalid_property)
		object.__setattr__(self, "updates_visibility", [])

	def __setattr__(self, name, value):
		"""Mémorise la visibilité courante ou refuse la propriété utilisée pour simuler une erreur."""
		if name == self.invalid_property: raise ValueError("Invalid property")
		if name != "visible": self.updates_visibility.append(self.visible)
		object.__setattr__(self, name, value)


# ==================================================
# region Initialisation
# ==================================================
##################################################
@pytest.mark.parametrize("shared", [False, True], ids=["new-instance", "shared-instance"])
def test_initialization_preserves_references(qtbot, monkeypatch, shared):
	"""Vérifie l'identité des références et l'absence de création supplémentaire en mode partagé."""
	viewer, pt = ViewerModel(), PALMTracer()
	created = []

	def create_palmtracer():
		"""Observe la création de l'instance par défaut."""
		created.append(pt)
		return pt

	monkeypatch.setattr(import_module(BaseNapariWidget.__module__), "PALMTracer", create_palmtracer)
	widget = BaseNapariWidget(viewer, pt if shared else None)
	qtbot.addWidget(widget)

	assert widget.viewer is viewer
	assert widget.pt is pt
	assert len(created) == (0 if shared else 1)


# ==================================================
# endregion Initialisation
# ==================================================

# ==================================================
# region Glisser-déposer
# ==================================================
##################################################
@pytest.mark.parametrize("floating", [False, True], ids=["docked", "floating"])
def test_drop_target_preserves_root_window(qtbot, floating):
	"""Vérifie que la fenêtre Napari reste la cible lorsque le dock est détaché."""
	window = QMainWindow()
	qtbot.addWidget(window)
	dock = QDockWidget(window)
	widget = BaseNapariWidget(ViewerModel())
	dock.setWidget(widget)
	window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
	window.show()
	dock.setFloating(floating)

	assert widget._get_drop_target() is window
	assert widget._drop_window is window


##################################################
@pytest.mark.parametrize("initial_accepts", [False, True], ids=["drops-disabled", "drops-enabled"])
def test_drop_filter_follows_visibility(drop_widget, initial_accepts):
	"""Vérifie qu'un affichage répété conserve l'état à restaurer après masquage."""
	widget, _, calls = drop_widget
	widget.hide()
	widget.setAcceptDrops(initial_accepts)
	widget.show()
	QApplication.sendEvent(widget, QShowEvent())
	assert widget._drop_window is widget
	assert widget.acceptDrops()
	widget.hide()
	assert widget._drop_window is None
	assert widget.acceptDrops() == initial_accepts
	widget.show()
	assert widget._drop_window is widget
	assert calls == []


##################################################
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

	events = send_file_drop(widget if target == "window" else receiver, mime)

	assert all(event.isAccepted() for event in events)
	assert all(event.dropAction() == Qt.DropAction.CopyAction for event in events)
	assert [[Path(path) for path in paths] for paths in calls] == [[first, second] if scenario == "multiple" else [first]]
	assert receiver.received == []


##################################################
@pytest.mark.parametrize("scenario", ["multiple", "mixed", "directory", "missing", "blocked"],
						 ids=["multiple-files", "local-and-remote", "directory", "missing-file", "blocked-widget"])
def test_drop_rejects_invalid_files(drop_widget, tmp_path, monkeypatch, scenario):
	"""Vérifie les contraintes sur le nombre de fichiers, leur existence et l'état du widget."""
	widget, receiver, calls = drop_widget
	path = tmp_path / "stack.tif"
	path.touch()
	monkeypatch.setattr(widget, "DROP_MULTIPLE", False)
	urls = {"multiple":  [QUrl.fromLocalFile(str(path))] * 2,
			"mixed":     [QUrl.fromLocalFile(str(path)), QUrl("https://example.com/stack.tif")],
			"directory": [QUrl.fromLocalFile(str(tmp_path))],
			"missing":   [QUrl.fromLocalFile(str(tmp_path / "missing.tif"))],
			"blocked":   [QUrl.fromLocalFile(str(path))]}
	if scenario == "blocked": monkeypatch.setattr(widget, "_can_drop_files", lambda paths: False)
	mime = QMimeData()
	mime.setUrls(urls[scenario])

	events = send_file_drop(receiver, mime)

	assert not any(event.isAccepted() for event in events)
	assert calls == []
	assert receiver.received == []


##################################################
@pytest.mark.parametrize("scenario", ["other-window", "remote", "text"], ids=["other-window", "remote-url", "internal-text"])
def test_drop_preserves_unrelated_events(drop_widget, qtbot, tmp_path, scenario):
	"""Vérifie que les autres fenêtres et les glissements sans fichier local suivent leur traitement habituel."""
	_, receiver, calls = drop_widget
	mime = QMimeData()
	if scenario == "other-window":
		receiver = _DropReceiver()
		qtbot.addWidget(receiver)
		receiver.show()
		path = tmp_path / "stack.tif"
		path.touch()
		mime.setUrls([QUrl.fromLocalFile(str(path))])
	elif scenario == "remote": mime.setUrls([QUrl("https://example.com/stack.tif")])
	else: mime.setText("layer")

	send_file_drop(receiver, mime)

	assert receiver.received == ["enter", "drop"]
	assert calls == []


##################################################
@pytest.mark.parametrize("scenario", ["hidden", "deleted", "non-widget"], ids=["hidden-window", "deleted-window", "non-widget-receiver"])
def test_drop_ignores_inactive_target(qtbot, tmp_path, monkeypatch, scenario):
	"""Vérifie les événements tardifs et les destinataires dépourvus d'interface QWidget."""
	widget = BaseNapariWidget(ViewerModel())
	qtbot.addWidget(widget)
	widget.show()
	receiver = widget
	if scenario == "hidden": widget.hide()
	elif scenario == "deleted":
		window = QWidget()
		window.deleteLater()
		QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
		assert not isalive(window)
		widget._drop_window = window
	else: receiver = QObject(widget)
	path = tmp_path / "stack.tif"
	path.touch()
	mime = QMimeData()
	mime.setUrls([QUrl.fromLocalFile(str(path))])
	drop = QDropEvent(QPointF(1, 1), Qt.DropAction.CopyAction, mime, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier)
	calls = []
	monkeypatch.setattr(widget, "_drop_files", calls.append)

	# Le filtre a déjà été retiré après masquage ; on simule directement l'événement tardif.
	assert not widget.eventFilter(receiver, drop)
	assert not drop.isAccepted()
	assert calls == []


##################################################
@pytest.mark.parametrize("scenario", ["hide", "show"], ids=["hide-after-destruction", "show-after-destruction"])
def test_drop_filter_handles_deleted_window(drop_widget, scenario):
	"""Vérifie le masquage et le ré-affichage après destruction de la fenêtre mémorisée."""
	widget, _, calls = drop_widget
	window = QWidget()
	window.deleteLater()
	QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
	assert not isalive(window)
	if scenario == "show": widget.hide()
	widget._drop_window = window

	if scenario == "hide":
		widget.hide()
		assert widget._drop_window is None
	else:
		widget.show()
		assert widget._drop_window is widget
	assert calls == []


##################################################
def test_drop_filter_handles_parent_destruction(qtbot):
	"""Vérifie la destruction réelle du parent et de son plugin sans exception dans la boucle Qt."""
	# Ce parent est détruit explicitement ; pytest-qt ne doit pas tenter de le refermer.
	window = QMainWindow()
	dock = QDockWidget(window)
	widget = BaseNapariWidget(ViewerModel())
	dock.setWidget(widget)
	window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
	window.show()
	window.deleteLater()
	QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)

	assert not isalive(window)
	assert not isalive(widget)


##################################################
def test_drop_requires_specialized_handler(qtbot, tmp_path):
	"""Vérifie qu'une classe fille incomplète ne perd pas silencieusement les fichiers déposés."""
	widget = BaseNapariWidget(ViewerModel())
	qtbot.addWidget(widget)
	with pytest.raises(NotImplementedError, match="traitement des fichiers"):
		widget._drop_files([str(tmp_path / "stack.tif")])


# ==================================================
# endregion Glisser-déposer
# ==================================================

# ==================================================
# region Calques
# ==================================================
##################################################
@pytest.mark.parametrize("initial_visibility, visible, expected_visibility", [
		pytest.param(False, None, False, id="preserve-hidden"),
		pytest.param(True, None, True, id="preserve-visible"),
		pytest.param(False, True, True, id="force-visible"),
		pytest.param(True, False, False, id="force-hidden")])
def test_update_layer(initial_visibility, visible, expected_visibility):
	"""Vérifie la mise à jour du calque et les différentes politiques de visibilité."""
	layer = _DummyLayer(initial_visibility)
	BaseNapariWidget.update_layer(layer, "new-data", visible, face_color="lime", blending="translucent")

	assert layer.data == "new-data"
	assert layer.face_color == "lime"
	assert layer.blending == "translucent"
	assert layer.updates_visibility == [True, True, True]
	assert layer.visible is expected_visibility


##################################################
def test_update_layer_restores_visibility_on_error():
	"""Vérifie la restauration de la visibilité lorsqu'une propriété ne peut pas être affectée."""
	layer = _DummyLayer(False, "invalid")
	with pytest.raises(ValueError, match="Invalid property"): BaseNapariWidget.update_layer(layer, "new-data", invalid=True)
	assert layer.visible is False

# ==================================================
# endregion Calques
# ==================================================
