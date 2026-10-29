"""Teste la récupération et la transmission de l'instance PALMTracer depuis le menu Napari."""

from importlib import import_module
from types import SimpleNamespace
from unittest.mock import Mock

import napari
import pytest
from napari.components import ViewerModel
from qtpy.QtWidgets import QLabel, QMenu, QWidgetAction

from palm_tracer.PALMTracer import PALMTracer
from palm_tracer.UI.BaseWidget import BaseWidget
from palm_tracer.UI.Napari import get_current_palmtracer, install_plugin_menu_sections
from palm_tracer.UI.PALMTracerWidget import PALMTracerWidget


# --------------------------------------------------
def test_plugin_menu_sections_accepts_viewer_without_window():
	"""Accepte un modèle Napari sans tenter d'accéder à une fenêtre ou à son menu Qt."""
	install_plugin_menu_sections(ViewerModel())


# --------------------------------------------------
@pytest.mark.parametrize("rebuild", [False, True], ids=["reopened-menu", "rebuilt-menu"])
def test_plugin_menu_sections_preserve_actions(qtbot, rebuild):
	"""Conserve les actions, leurs connexions et les autres plugins après réouverture ou reconstruction du sous-menu."""
	plugins = QMenu()
	qtbot.addWidget(plugins)
	plain_action = plugins.addAction("Plugin manager")
	other_menu = plugins.addMenu("Other plugin")
	other_menu.setObjectName("napari/plugins/other-plugin")
	other_action = other_menu.addAction("Shared tool")
	# Même un raccourci vers une commande PALMTracer ne doit pas entraîner la décoration d'un autre plugin.
	other_action.setObjectName("palm-tracer.open_alignment")
	viewer = SimpleNamespace(window=SimpleNamespace(plugins_menu=plugins))
	install_plugin_menu_sections(viewer)
	install_plugin_menu_sections(viewer)
	menu = plugins.addMenu("PALM Tracer")
	menu.setObjectName("napari/plugins/palm-tracer")
	commands = [("palm-tracer.make_qwidget", "PALM Tracer"), ("palm-tracer.open_graphviewer", "Graph Viewer"),
				("palm-tracer.open_viewerhr", "HR Viewer"), ("palm-tracer.open_viewer3d", "3D Viewer"),
				("palm-tracer.open_alignment", "Alignment Tool")]
	for command, title in commands:
		action = menu.addAction(title)
		action.setObjectName(command)
	plugins.aboutToShow.emit()
	if rebuild:
		plugins.removeAction(menu.menuAction())
		menu.deleteLater()
		menu = plugins.addMenu("PALM Tracer")
		menu.setObjectName("napari/plugins/palm-tracer")
		for command, title in commands:
			action = menu.addAction(title)
			action.setObjectName(command)
	callback = Mock()
	main_action = next(action for action in menu.actions() if action.objectName() == "palm-tracer.make_qwidget")
	main_action.setCheckable(True)
	main_action.triggered.connect(callback)
	plugins.aboutToShow.emit()
	assert plugins.actions() == [plain_action, other_menu.menuAction(), menu.menuAction()]
	assert other_menu.actions() == [other_action]
	assert [action.text() for action in menu.actions()] == ["Main widget", "PALM Tracer", "Viewers", "Graph Viewer", "HR Viewer", "3D Viewer",
															"Tools", "Alignment Tool"]
	for action in menu.actions():
		if isinstance(action, QWidgetAction):
			assert isinstance(action.defaultWidget(), QLabel) and not action.isEnabled()
	main_action.trigger()
	callback.assert_called_once()


# --------------------------------------------------
@pytest.mark.parametrize("viewer", [None, SimpleNamespace(window=SimpleNamespace(dock_widgets={"Other tool": object()}))],
						 ids=["no-viewer", "no-main-widget"])
def test_current_palmtracer_without_main_widget(monkeypatch, viewer):
	"""Laisse la création d'une instance à la base lorsqu'aucun widget principal n'est disponible."""
	monkeypatch.setattr(napari, "current_viewer", lambda: viewer)
	assert get_current_palmtracer() is None


# --------------------------------------------------
@pytest.mark.parametrize("explicit", [False, True], ids=["active-viewer", "explicit-viewer"])
@pytest.mark.parametrize("script", [False, True], ids=["plugin-main", "script-main"])
def test_current_palmtracer_uses_selected_viewer(monkeypatch, explicit, script):
	"""Retrouve le widget principal importé ou lancé comme script, sans sélectionner une autre session."""
	pt = Mock(spec=PALMTracer)
	main_type = type("PALMTracerWidget", (BaseWidget,), {"__module__": "__main__", "UI_NAME": "PALMTracer"}) if script else PALMTracerWidget
	main = Mock(spec=main_type, pt=pt, UI_NAME="PALMTracer")
	viewer = SimpleNamespace(window=SimpleNamespace(dock_widgets={"Other tool": object(), "Custom main name": main}))
	other = SimpleNamespace(window=SimpleNamespace(dock_widgets={"Another session": Mock(spec=PALMTracerWidget)}))
	monkeypatch.setattr(napari, "current_viewer", lambda: other if explicit else viewer)
	assert get_current_palmtracer(viewer if explicit else None) is pt


# --------------------------------------------------
@pytest.mark.parametrize("module_name, entry, factory, separate_viewer", [
		("AlignmentWidget", "open_alignment", "AlignmentWidget", False),
		("Astigmatism3DWidget", "open_astigmatism3d", "Astigmatism3DWidget", False),
		("FileMigratorWidget", "open_migrator", "FileMigratorWidget", False),
		("GraphViewerWidget", "open_graphviewer", "GraphViewerWidget", False),
		("ViewerHRWidget", "open_viewerhr", "create_viewerhr", True),
		("Viewer3DWidget", "open_viewer3d", "create_viewer3d", True),
		], ids=["alignment", "astigmatism", "migration", "graph-viewer", "hr-viewer", "3d-viewer"])
def test_plugin_entry_point_shares_main_instance(qtbot, monkeypatch, module_name, entry, factory, separate_viewer):
	"""Transmet l'instance avant l'ouverture de l'outil, même si celle-ci change le viewer actif."""
	module = import_module(f"palm_tracer.UI.{module_name}")
	pt = Mock(spec=PALMTracer)
	viewer = SimpleNamespace(window=SimpleNamespace(dock_widgets={"Main": Mock(spec=PALMTracerWidget, pt=pt, UI_NAME="PALMTracer")}))
	monkeypatch.setattr(napari, "current_viewer", lambda: viewer)

	# --------------------------------------------------
	def create(*_args, **_kwargs):
		"""Simule l'ouverture sans créer de visionneuse ou lancer QtWebEngine."""
		monkeypatch.setattr(napari, "current_viewer", lambda: None)
		return Mock()

	constructor = Mock(side_effect=create)
	monkeypatch.setattr(module, factory, constructor)
	stub = getattr(module, entry)()
	if separate_viewer:
		qtbot.addWidget(stub)
		constructor.assert_called_once_with(pt)
	else:
		constructor.assert_called_once_with(palmtracer=pt)
