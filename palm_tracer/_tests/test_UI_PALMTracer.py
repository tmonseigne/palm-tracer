"""Fichier des tests pour le widget."""
import shutil

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QTabWidget

from palm_tracer._tests.Utils import *
from palm_tracer.UI import PALMTracerWidget
from palm_tracer.UI.PALMTracerWidget import SETTINGS_FILE

SIZE_X, SIZE_Y, INTENSITY, RATIO = 100, 50, 1000, 10
SIZE = int(SIZE_X * np.sqrt(SIZE_Y))
POINTS = np.stack([rng.uniform(1, SIZE_Y - 1, size=SIZE), rng.uniform(1, SIZE_X - 1, size=SIZE)], axis=1)
OUTPUT_FOLDER = INPUT_DIR / "stack_PALM_Tracer"


##################################################
def test_creation(make_napari_viewer, patched_napari_viewer):
	"""Test basique de création du widget."""
	SETTINGS_FILE.unlink(missing_ok=True)  # On supprime le fichier setting
	viewer = make_napari_viewer()  # .		 Créer un viewer à l'aide de la fixture.
	_ = PALMTracerWidget(viewer)  # .		 Créer notre widget, en passant par le viewer.


##################################################
def test_on_load_setting(make_napari_viewer, patched_napari_viewer, capsys, monkeypatch, fake_qfiledialog):
	"""Test remise à zéro des calques."""
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = make_napari_viewer()
	w = PALMTracerWidget(viewer)

	fake_qfiledialog(PALMTracerWidget, None)  # Simuler un "Cancel" sur le QFileDialog
	w._on_load_setting_btn()
	lines = get_lines_output(capsys)
	assert "WARNING: Error loading file '" in lines[0]


##################################################
def test_reset_setting(make_napari_viewer, patched_napari_viewer):
	"""Test remise à zéro des calques."""
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = make_napari_viewer()
	w = PALMTracerWidget(viewer)

	w._on_reset_setting_btn()


##################################################
def test_clean_layer(make_napari_viewer, patched_napari_viewer, capsys, qtbot):
	"""Test nettoyage des calques."""
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = make_napari_viewer()
	w = PALMTracerWidget(viewer)

	w._clean_layer()
	w._clean_layer(False, False, False)


##################################################
def test_reset_layer(make_napari_viewer, patched_napari_viewer, capsys, qtbot):
	"""Test remise à zéro des calques."""
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = make_napari_viewer()
	w = PALMTracerWidget(viewer)

	w._reset_layer()  # .											   Remise à 0 des calques sans fichier dans le batch.
	add_basic_file(w.pt)  # .										   Ajout d'une entrée
	qtbot.waitUntil(lambda: "Raw" in w.viewer.layers, timeout=5000)  # Attente : qu'il ait mis une image
	lines = get_lines_output(capsys)
	assert "INFO: Loaded" in lines[0]
	w._reset_layer()  # .											   Remise à 0 des calques sans changement.


##################################################
def test_get_actual_image(make_napari_viewer, patched_napari_viewer, qtbot):
	"""Test de récupération d'image."""
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = make_napari_viewer()
	w = PALMTracerWidget(viewer)

	add_basic_file(w.pt)  # .															 Ajout d'une entrée
	qtbot.waitUntil(lambda: "Raw" in w.viewer.layers, timeout=5000)  # .				 Attente : qu'il ait mis une image
	assert w._get_actual_image() is not None, "Aucune image récupéré."  # .				 Récupéraiton de l'image
	assert w._get_actual_image(-100) is None, "Une image hors limite a été récupéré."  # Récupération d'une image hors limite
	assert w._get_actual_image(100) is None, "Une image hors limite a été récupéré."  # .Récupération d'une image hors limite


##################################################
def test_add_detection_layers(make_napari_viewer, patched_napari_viewer, qtbot):
	"""Test Ajout des calques de détection."""
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = make_napari_viewer()
	w = PALMTracerWidget(viewer)
	layers = w.viewer.layers

	w.pt.settings.localization["Preview"].value = True
	qtbot.waitUntil(lambda: w.pt.settings.localization["Preview"].value, timeout=5000)
	qtbot.waitUntil(lambda: not w._processing, timeout=5000)
	w.pt.settings.localization["ROI Shape"].value = 0
	qtbot.waitUntil(lambda: w.pt.settings.localization["ROI Shape"].value == 0, timeout=5000)
	qtbot.waitUntil(lambda: not w._processing, timeout=5000)

	# Ajout avec des tableaux normaux.
	w._preview_locs = {"Past": POINTS, "Present": POINTS, "Future": POINTS, "Filtered": POINTS}
	w._add_preview_layers()
	qtbot.waitUntil(lambda: "Points Present" in layers, timeout=5000)
	assert len(w._layers["Points Past"].data) == 707
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
def test_preview(make_napari_viewer, patched_napari_viewer, capsys, qtbot):
	"""Test click sur le bouton preview."""
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = make_napari_viewer()
	w = PALMTracerWidget(viewer)

	setting = w.pt.settings.localization
	layers = w.viewer.layers
	with setting.signal_blocked():  # L'éxecution ne devra pas être dans un sub-process pour vérifier la couverture (sans partir sur des configs complexes).
		w._preview()  # .										Passage si preview à False
		setting["Preview"].value = True
		qtbot.waitUntil(lambda: setting["Preview"].value, timeout=5000)
		w._preview()  # .										Passage par le point get_actual_image = None pour le temps présent.

	# Ajout d'une entrée
	add_basic_file(w.pt)  # .									Ajout d'une entrée.
	qtbot.waitUntil(lambda: "Raw" in layers, timeout=5000)  # . Attente : qu'il ait mis une image.
	qtbot.waitUntil(lambda: not w._processing, timeout=5000)  # Attente : le flag doit passer à False.

	with setting.signal_blocked():
		setting["Preview"].value = True  # .					Le flag se remet à False à chaque changement de fichiers
		qtbot.waitUntil(lambda: setting["Preview"].value, timeout=5000)
		w._preview()  # .										Preview simple
		lines = get_lines_output(capsys)
		assert "Preview of plane 4 : 142 detected points (46 on the current frame, 48 on the previous frame, 48 on the next frame)." in lines[-1]


##################################################
def test_auto_threshold(make_napari_viewer, patched_napari_viewer, capsys, qtbot):
	"""Test click sur le bouton auto_threshold."""
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = make_napari_viewer()
	w = PALMTracerWidget(viewer)

	w._auto_threshold()  # .										   Appel de la méthode auto_threshold sans fichier dans le batch.

	# Ajout d'une entrée
	add_basic_file(w.pt)  # .										   Ajout d'une entrée
	qtbot.waitUntil(lambda: "Raw" in w.viewer.layers, timeout=5000)  # Attente : qu'il ait mis une image
	w._auto_threshold()  # .										   Appel de la méthode auto_threshold.

	lines = get_lines_output(capsys)
	assert "Auto Threshold: 63.95" in lines[-1]


##################################################
def test_thread_process(make_napari_viewer, patched_napari_viewer, qtbot):
	"""Test click sur le bouton process."""
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = make_napari_viewer()
	w = PALMTracerWidget(viewer)

	w._thread_process(w._auto_threshold)
	qtbot.waitUntil(lambda: not w._processing, timeout=5000)  # Attente : que le thread soit terminé

	# appel avec un process en cours
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


##################################################
def test_filters_button(make_napari_viewer, patched_napari_viewer, qtbot):
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = make_napari_viewer()
	w = PALMTracerWidget(viewer)

	qtbot.addWidget(w)
	w.show()

	add_basic_file(w.pt)  # .										   Ajout d'une entrée
	qtbot.waitUntil(lambda: not w._processing, timeout=5000)  # Attente : que le thread soit terminé

	# Activation d'un process
	w.pt.settings.localization.active = True
	qtbot.mouseClick(w.btn_process, Qt.MouseButton.LeftButton)
	qtbot.waitUntil(lambda: not w._processing, timeout=5000)  # Attente : que le thread soit terminé
	assert len(w.pt.df["loc"]) == 455
	assert len(w.pt.df["f_loc"]) == 0

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
	assert len(w.pt.df["loc"]) == 455
	assert len(w.pt.df["f_loc"]) == 242

	qtbot.mouseClick(ui_buttons["save"], Qt.MouseButton.LeftButton)
	f = FileIO.get_last_file(OUTPUT_FOLDER, "localizations_filtered")
	assert f

	qtbot.mouseClick(ui_buttons["reset"], Qt.MouseButton.LeftButton)
	assert len(w.pt.df["f_loc"]) == 0
