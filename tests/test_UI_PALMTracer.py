"""Teste le widget principal de PALM Tracer."""

from types import SimpleNamespace
from unittest.mock import Mock, PropertyMock

import numpy as np
import pytest
from napari.components import ViewerModel
from qtpy.QtCore import QMimeData, Qt, QUrl
from qtpy.QtWidgets import QDockWidget, QMainWindow, QTabWidget

from palm_tracer.Tools import FileIO
from palm_tracer.UI import PALMTracerWidget
from tests.Utils import *
from tests.Utils import add_basic_file, send_drop_events

SIZE_X, SIZE_Y, INTENSITY, RATIO = 100, 50, 1000, 10
SIZE = int(SIZE_X * np.sqrt(SIZE_Y))
rng = np.random.default_rng(42)  # Générateur propre au jeu de données de ce module.
POINTS = np.stack([rng.uniform(1, SIZE_Y - 1, size=SIZE), rng.uniform(1, SIZE_X - 1, size=SIZE)], axis=1)


# --------------------------------------------------
@pytest.fixture
def callback_widget(qtbot, monkeypatch):
	"""Crée un widget sans chargement initial ni lancement automatique de traitement pendant les tests de callbacks."""
	monkeypatch.setattr(PALMTracerWidget, "_on_startup", lambda self: None)
	monkeypatch.setattr(PALMTracerWidget, "_connect_signal", lambda self: None)
	w = PALMTracerWidget(ViewerModel())
	qtbot.addWidget(w)
	return w


# --------------------------------------------------
@pytest.fixture
def drop_widget(qtbot, monkeypatch):
	"""Crée une fenêtre PALMTracer sans chargement initial ni callbacks de traitement des fichiers."""
	# Ces méthodes sont appelées par le constructeur : les neutraliser avant toute création du widget.
	monkeypatch.setattr(PALMTracerWidget, "_on_startup", lambda self: None)
	monkeypatch.setattr(PALMTracerWidget, "_connect_signal", lambda self: None)
	window = QMainWindow()
	qtbot.addWidget(window)
	receiver = DropReceiver()
	window.setCentralWidget(receiver)
	dock = QDockWidget(window)
	widget = PALMTracerWidget(ViewerModel())
	# Le modèle connecte lui-même la lecture de profondeur, indépendamment des signaux du widget.
	monkeypatch.setattr(widget.pt.settings.batch, "get_plane_count", lambda: None)
	dock.setWidget(widget)
	window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

	window.show()
	return widget, receiver


# ==================================================
# region Initialisation
# ==================================================
def test_creation(qtbot):
	"""Vérifie la création du widget."""
	viewer = ViewerModel()
	w = PALMTracerWidget(viewer)
	qtbot.addWidget(w)


# --------------------------------------------------
def test_filters_button(qtbot, input_stack, output_folder):
	"""Vérifie le comportement du bouton de filtrage."""
	viewer = ViewerModel()
	w = PALMTracerWidget(viewer)

	qtbot.addWidget(w)
	w.show()

	add_basic_file(w.pt, [str(input_stack)])  # .				Ajout d'une entrée
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
	filename = FileIO.get_last_file(output_folder, "localizations_filtered")
	assert filename

	qtbot.mouseClick(ui_buttons["reset"], Qt.MouseButton.LeftButton)
	assert len(w.pt.results["f_loc"]) == 0


# ==================================================
# endregion Initialisation
# ==================================================

# ==================================================
# region Glisser-déposer
# ==================================================
@pytest.mark.parametrize("count", [1, 2], ids=["single-file", "multiple-files"])
def test_drop_adds_files_from_window(drop_widget, tmp_path, count):
	"""Vérifie l'ajout depuis un widget extérieur au plugin et l'interception avant son gestionnaire."""
	widget, receiver = drop_widget
	paths = [tmp_path / name for name in ("z.tif", "a.STK")[:count]]
	for path in paths: path.touch()
	mime = QMimeData()
	mime.setUrls([QUrl.fromLocalFile(str(path)) for path in paths])

	events = send_drop_events(receiver, mime)

	assert all(event.isAccepted() for event in events)
	assert receiver.received == []
	files = widget.pt.settings.batch["Files"]
	assert [Path(p) for p in files.items] == sorted(paths, key=lambda p: str(p).casefold())
	assert files.value == count - 1


# --------------------------------------------------
def test_drop_rejects_files_during_processing(drop_widget, tmp_path):
	"""Vérifie que le traitement en cours bloque les ajouts au Batch."""
	widget, receiver = drop_widget
	path = tmp_path / "stack.tif"
	path.touch()
	widget._processing = True
	mime = QMimeData()
	mime.setUrls([QUrl.fromLocalFile(str(path))])

	events = send_drop_events(receiver, mime)

	assert not any(event.isAccepted() for event in events)
	assert receiver.received == []
	assert widget.pt.settings.batch["Files"].items == []


# ==================================================
# endregion Glisser-déposer
# ==================================================

# ==================================================
# region Threads
# ==================================================
def test_thread_process(qtbot, input_stack):
	"""Vérifie le clic sur le bouton process."""
	viewer = ViewerModel()
	w = PALMTracerWidget(viewer)
	qtbot.addWidget(w)

	w._thread_process(w._auto_threshold)
	qtbot.waitUntil(lambda: not w._processing, timeout=5000)  # Attente : que le thread soit terminé

	# Ajout d'une entrée
	add_basic_file(w.pt, [str(input_stack)])  # .				Ajout d'une entrée
	qtbot.waitUntil(lambda: not w._processing, timeout=5000)  # Attente : que le thread soit terminé
	w._thread_process(w.pt.process)  # .						Appel de la méthode process
	qtbot.waitUntil(lambda: not w._processing, timeout=5000)  # Attente : que le thread soit terminé
	w._thread_process(w._auto_threshold)  # .					Appel de la méthode auto threshold mais impossible de l'exécuter dans ce contexte.
	qtbot.waitUntil(lambda: not w._processing, timeout=5000)  # Attente : que le thread soit terminé


# ==================================================
# endregion Threads
# ==================================================

# ==================================================
# region Fonctions de rappel des paramètres
# ==================================================
def test_load_setting_restores_values(callback_widget, tmp_path, monkeypatch):
	"""Restaure les paramètres puis désactive les filtres et la prévisualisation avant de synchroniser les ROI."""
	w = callback_widget
	info = Mock()
	monkeypatch.setattr(w, "notify_info", info)
	update_rois = Mock(wraps=w.pt.settings.rois.update_main)
	monkeypatch.setattr(w.pt.settings.rois, "update_main", update_rois)

	# Enregistre une configuration distincte de l'état courant, avec des options à désactiver au chargement.
	w.pt.settings.calibration["Pixel Size"].value = 0.32
	w.pt.settings.localization["Preview"].value = True
	w.pt.settings.filters["Plane"].active = True
	path = tmp_path / "settings.json"
	FileIO.save_json(path, w.pt.settings.to_compact_dict())
	w.pt.settings.calibration["Pixel Size"].value = 0.16

	w._load_setting(path)
	assert w.pt.settings.calibration["Pixel Size"].value == 0.32
	assert not w.pt.settings.localization["Preview"].value
	assert not w.pt.settings.filters["Plane"].active
	update_rois.assert_called_once_with()
	info.assert_called_once_with(f"Loading the setting file '{path}'.")


# --------------------------------------------------
def test_load_setting_invalid_json(callback_widget, tmp_path, monkeypatch):
	"""Signale un fichier JSON invalide sans propager l'erreur au callback Qt."""
	w = callback_widget
	path = tmp_path / "settings.json"
	path.write_text("invalid json", encoding="utf-8")
	warning = Mock()
	monkeypatch.setattr(w, "notify_warning", warning)
	w._load_setting(path)
	warning.assert_called_once()
	assert f"Error loading file '{path}':" in warning.call_args.args[0]


# --------------------------------------------------
def test_on_load_setting(qtbot, capsys, fake_qfiledialog):
	"""Vérifie la remise à zéro des calques."""
	viewer = ViewerModel()
	w = PALMTracerWidget(viewer)
	qtbot.addWidget(w)

	fake_qfiledialog(PALMTracerWidget, None)  # Simuler un "Cancel" sur le QFileDialog
	w._on_load_setting_btn()


# --------------------------------------------------
def test_reset_setting(qtbot):
	"""Vérifie la remise à zéro des calques."""
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

# ==================================================
# region Nettoyage et chargement de la pile
# ==================================================
def test_clean_layer(qtbot):
	"""Vérifie le nettoyage des calques."""
	viewer = ViewerModel()
	w = PALMTracerWidget(viewer)
	qtbot.addWidget(w)

	w._layers["Points Present"].visible = False
	w._clean_layer()
	assert not w._layers["Points Present"].visible
	w._clean_layer(False, False, False)


# --------------------------------------------------
def test_reset_layer(capsys, qtbot, input_stack):
	"""Vérifie la remise à zéro des calques."""
	viewer = ViewerModel()
	w = PALMTracerWidget(viewer)
	qtbot.addWidget(w)

	w._reset_layer()  # .											   Remise à 0 des calques sans fichier dans le batch.
	w._layers["Raw"].visible = False
	add_basic_file(w.pt, [str(input_stack)])  # .					   Ajout d'une entrée
	qtbot.waitUntil(lambda: "Raw" in w.viewer.layers, timeout=5000)  # Attente : qu'il ait mis une image
	assert not w._layers["Raw"].visible
	lines = get_lines_output(capsys)
	assert lines == ["No valid settings file to load.", f"Loaded {input_stack} (10, 128, 256) into Napari viewer."]
	w._reset_layer()  # .											   Remise à 0 des calques sans changement.


# --------------------------------------------------
@pytest.mark.parametrize("stage", ["read", "selection"], ids=["unreadable-stack", "selection-failed"])
def test_reset_layer_error(callback_widget, input_stack, monkeypatch, stage):
	"""Signale une erreur de lecture ou de sélection sans laisser le callback de changement de pile lever une exception."""
	w = callback_widget
	add_basic_file(w.pt, [str(input_stack)])
	error, info = Mock(), Mock()
	monkeypatch.setattr(w, "notify_error", error)
	monkeypatch.setattr(w, "notify_info", info)
	load = Mock()
	monkeypatch.setattr(w.pt, "load", load)

	# La sélection est simulée après les vraies mises à jour de la pile et du calque Raw.
	if stage == "read": monkeypatch.setattr(FileIO, "open_tif", Mock(side_effect=OSError("Unreadable stack")))
	else:
		selection = Mock()
		monkeypatch.setattr(type(selection), "active", PropertyMock(side_effect=RuntimeError("Selection unavailable")), raising=False)
		monkeypatch.setattr(w, "viewer", SimpleNamespace(layers=SimpleNamespace(selection=selection), dims=Mock(), reset_view=Mock()))
	w._reset_layer()

	error.assert_called_once()
	if stage == "read":
		assert error.call_args.args[0] == f"Error loading {input_stack}: Unreadable stack"
		load.assert_not_called()
		info.assert_not_called()
	else:
		assert error.call_args.args[0] == "Error during layer selection: Selection unavailable"
		load.assert_called_once_with(str(input_stack.with_name(f"{input_stack.stem}_PALM_Tracer")))
		info.assert_called_once()
		assert w._current_stack.shape == (10, 128, 256)


# ==================================================
# endregion Nettoyage et chargement de la pile
# ==================================================

# ==================================================
# region Calques de détection
# ==================================================
def test_add_detection_layers(qtbot):
	"""Vérifie Ajout des calques de détection."""
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


# ==================================================
# endregion Calques de détection
# ==================================================

# ==================================================
# region Prévisualisation et seuil automatique
# ==================================================
def test_get_actual_image(qtbot, input_stack):
	"""Vérifie la récupération d'image."""
	viewer = ViewerModel()
	w = PALMTracerWidget(viewer)
	qtbot.addWidget(w)

	add_basic_file(w.pt, [str(input_stack)])  # .										 Ajout d'une entrée
	qtbot.waitUntil(lambda: "Raw" in w.viewer.layers, timeout=5000)  # .				 Attente : qu'il ait mis une image
	assert w._get_actual_image() is not None, "Aucune image récupéré."  # .				 Récupération de l'image
	assert w._get_actual_image(-100) is None, "Une image hors limite a été récupéré."  # Récupération d'une image hors limite
	assert w._get_actual_image(100) is None, "Une image hors limite a été récupéré."  # .Récupération d'une image hors limite


# --------------------------------------------------
def test_preview(capsys, qtbot, input_stack):
	"""Vérifie le clic sur le bouton preview."""
	viewer = ViewerModel()
	w = PALMTracerWidget(viewer)
	qtbot.addWidget(w)

	setting = w.pt.settings.localization
	layers = w.viewer.layers
	with setting.signal_blocked():  # L'exécution ne devra pas être dans un sub-process pour vérifier la couverture (sans partir sur des configs complexes).
		w._preview()  # .										Passage si preview à False
		setting["Preview"].value = True
		qtbot.waitUntil(lambda: setting["Preview"].value, timeout=5000)
		w._preview()  # .										Passage par le point get_actual_image = None pour le temps présent.

	# Ajout d'une entrée
	add_basic_file(w.pt, [str(input_stack)])  # .				Ajout d'une entrée.
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


# --------------------------------------------------
def test_preview_fit_error(callback_widget, monkeypatch):
	"""Propage une configuration d'ajustement invalide avant tout calcul de localisation."""
	w = callback_widget
	w.pt.settings.localization["Preview"].value = True
	# Fournit une image valide pour atteindre la lecture des paramètres d'ajustement.
	monkeypatch.setattr(w, "_get_actual_image", lambda offset=0: np.zeros((1, 4, 4), dtype=np.uint16))
	monkeypatch.setattr(w.pt.settings.localization, "get_fit", Mock(side_effect=ValueError("Invalid fit")))
	localize = Mock()
	monkeypatch.setattr(w.pt.palm, "localization", localize)
	with pytest.raises(ValueError, match="Invalid fit"): w._preview()
	localize.assert_not_called()


# --------------------------------------------------
def test_preview_plane_filter_uses_stack_plane(qtbot, input_stack):
	"""Vérifie que le filtre utilise les numéros réels des plans prévisualisés."""
	viewer = ViewerModel()
	w = PALMTracerWidget(viewer)
	qtbot.addWidget(w)

	add_basic_file(w.pt, [str(input_stack)])
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


# --------------------------------------------------
def test_auto_threshold(capsys, qtbot, input_stack):
	"""Vérifie le clic sur le bouton auto_threshold."""
	viewer = ViewerModel()
	w = PALMTracerWidget(viewer)
	qtbot.addWidget(w)

	w._auto_threshold()  # .										   Appel de la méthode auto_threshold sans fichier dans le batch.

	# Ajout d'une entrée
	add_basic_file(w.pt, [str(input_stack)])  # .					   Ajout d'une entrée
	qtbot.waitUntil(lambda: "Raw" in w.viewer.layers, timeout=5000)  # Attente : qu'il ait mis une image
	w._auto_threshold()  # .										   Appel de la méthode auto_threshold.

	lines = get_lines_output(capsys)
	assert "Auto Threshold: 63.95" in lines[-1]

# ==================================================
# endregion Prévisualisation et seuil automatique
# ==================================================

# ==================================================
# endregion Fonctions de rappel des calques
# ==================================================
