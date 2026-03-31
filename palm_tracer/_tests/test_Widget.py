"""Fichier des tests pour le widget."""

import pytest
from qtpy.QtCore import QEvent, Qt
from qtpy.QtGui import QKeyEvent
from qtpy.QtWidgets import QSpinBox

from palm_tracer._tests.Utils import *
from palm_tracer.Settings.Types import CheckRangeInt
from palm_tracer.UI import PALMTracerWidget, Viewer3DWidget
from palm_tracer.UI.PALMTracerWidget import SETTINGS_FILE

SIZE_X, SIZE_Y, INTENSITY, RATIO = 100, 50, 1000, 10
SIZE = int(SIZE_X * np.sqrt(SIZE_Y))
POINTS = np.stack([rng.uniform(1, SIZE_Y - 1, size=SIZE), rng.uniform(1, SIZE_X - 1, size=SIZE)], axis=1)


##################################################
def test_widget_creation(make_napari_viewer, patched_napari_viewer):
	"""Test basique de création du widget."""
	SETTINGS_FILE.unlink(missing_ok=True)  # On supprime le fichier setting
	viewer = make_napari_viewer()  # .		 Créer un viewer à l'aide de la fixture.
	my_widget = PALMTracerWidget(viewer)  # .Créer notre widget, en passant par le viewer.


##################################################
def test_widget_on_load_setting(make_napari_viewer, patched_napari_viewer, capsys, monkeypatch, fake_qfiledialog):
	"""Test remise à zéro des calques."""
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = make_napari_viewer()
	my_widget = PALMTracerWidget(viewer)

	fake_qfiledialog(PALMTracerWidget, None)  # Simuler un "Cancel" sur le QFileDialog
	my_widget._on_load_setting_btn()
	lines = get_lines_output(capsys)
	assert "WARNING: Error loading file '" in lines[0]


##################################################
def test_widget_reset_setting(make_napari_viewer, patched_napari_viewer):
	"""Test remise à zéro des calques."""
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = make_napari_viewer()
	my_widget = PALMTracerWidget(viewer)

	my_widget._on_reset_setting_btn()


##################################################
def test_widget_reset_layer(make_napari_viewer, patched_napari_viewer, capsys, qtbot):
	"""Test remise à zéro des calques."""
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = make_napari_viewer()
	my_widget = PALMTracerWidget(viewer)

	my_widget._reset_layer()  # .											   Remise à 0 des calques sans fichier dans le batch.
	add_basic_file(my_widget.pt)  # .										   Ajout d'une entrée
	qtbot.waitUntil(lambda: "Raw" in my_widget.viewer.layers, timeout=5000)  # Attente : qu'il ait mis une image
	lines = get_lines_output(capsys)
	assert "INFO: Loaded" in lines[0]
	my_widget._reset_layer()  # .											   Remise à 0 des calques sans changement.


##################################################
def test_widget_get_actual_image(make_napari_viewer, patched_napari_viewer, qtbot):
	"""Test de récupération d'image."""
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = make_napari_viewer()
	my_widget = PALMTracerWidget(viewer)

	add_basic_file(my_widget.pt)  # .															 Ajout d'une entrée
	qtbot.waitUntil(lambda: "Raw" in my_widget.viewer.layers, timeout=5000)  # .				 Attente : qu'il ait mis une image
	assert my_widget._get_actual_image() is not None, "Aucune image récupéré."  # .				 Récupéraiton de l'image
	assert my_widget._get_actual_image(-100) is None, "Une image hors limite a été récupéré."  # Récupération d'une image hors limite
	assert my_widget._get_actual_image(100) is None, "Une image hors limite a été récupéré."  # .Récupération d'une image hors limite


##################################################
def test_widget_add_detection_layers(make_napari_viewer, patched_napari_viewer, qtbot):
	"""Test Ajout des calques de détection."""
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = make_napari_viewer()
	my_widget = PALMTracerWidget(viewer)
	layers = my_widget.viewer.layers

	my_widget.pt.settings.localization["Preview"].value = True
	qtbot.waitUntil(lambda: my_widget.pt.settings.localization["Preview"].value, timeout=5000)
	qtbot.waitUntil(lambda: not my_widget._processing, timeout=5000)
	my_widget.pt.settings.localization["ROI Shape"].value = 0
	qtbot.waitUntil(lambda: my_widget.pt.settings.localization["ROI Shape"].value == 0, timeout=5000)
	qtbot.waitUntil(lambda: not my_widget._processing, timeout=5000)

	# Ajout avec des tableaux normaux.
	my_widget._preview_locs = {"Past": POINTS, "Present": POINTS, "Future": POINTS}
	my_widget._add_preview_layers()
	qtbot.waitUntil(lambda: "Points Present" in layers, timeout=5000)

	# Ajout avec des calques existants et un futur vide.
	my_widget._preview_locs = {"Past": POINTS, "Present": POINTS, "Future": None}
	my_widget._add_preview_layers()
	qtbot.waitUntil(lambda: "Points Future" not in layers, timeout=5000)

	# Ajout avec un tableau vide et rien en passé et future.
	my_widget._preview_locs = {"Past": np.zeros((2, 0)), "Present": POINTS, "Future": None}
	my_widget._add_preview_layers()
	qtbot.waitUntil(lambda: "Points Past" not in layers, timeout=5000)

	my_widget.pt.settings.localization["ROI Shape"].value = 1
	qtbot.waitUntil(lambda: my_widget.pt.settings.localization["ROI Shape"].value == 1, timeout=5000)
	qtbot.waitUntil(lambda: not my_widget._processing, timeout=5000)
	my_widget._preview_locs = {"Past": POINTS, "Present": POINTS, "Future": POINTS}
	my_widget._add_preview_layers()
	qtbot.waitUntil(lambda: "Points Future" in layers, timeout=5000)


##################################################
def test_widget_preview(make_napari_viewer, patched_napari_viewer, capsys, qtbot):
	"""Test click sur le bouton preview."""
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = make_napari_viewer()
	my_widget = PALMTracerWidget(viewer)

	setting = my_widget.pt.settings.localization
	layers = my_widget.viewer.layers
	with setting.signal_blocked():  # L'éxecution ne devra pas être dans un sub-process pour vérifier la couverture (sans partir sur des configs complexes).
		my_widget._preview()  # .										Passage si preview à False
		setting["Preview"].value = True
		qtbot.waitUntil(lambda: setting["Preview"].value, timeout=5000)
		my_widget._preview()  # .										Passage par le point get_actual_image = None pour le temps présent.

	# Ajout d'une entrée
	add_basic_file(my_widget.pt)  # .									Ajout d'une entrée.
	qtbot.waitUntil(lambda: "Raw" in layers, timeout=5000)  # .			Attente : qu'il ait mis une image.
	qtbot.waitUntil(lambda: not my_widget._processing, timeout=5000)  # Attente : le flag doit passer à False.

	with setting.signal_blocked():
		setting["Preview"].value = True  # .							Le flag se remet à False à chaque changement de fichiers
		qtbot.waitUntil(lambda: setting["Preview"].value, timeout=5000)
		my_widget._preview()  # .										Preview simple
		lines = get_lines_output(capsys)
		assert "Preview of 142 detected points (46 on the current frame, 48 on the previous frame, 48 on the next frame)." in lines[-1]


##################################################
def test_widget_roi_filter_layer(make_napari_viewer, patched_napari_viewer, qtbot):
	"""Test click sur le bouton preview."""
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = make_napari_viewer()
	my_widget = PALMTracerWidget(viewer)

	filter_x = cast(CheckRangeInt, my_widget.pt.settings.filtering["Localization"]["X"])
	filter_y = cast(CheckRangeInt, my_widget.pt.settings.filtering["Localization"]["Y"])
	layers = my_widget.viewer.layers
	l_name = "ROI Filter"

	my_widget._add_roi_filter_layer()  # .							Lancement sans aucune entrée.
	# Ajout d'une entrée
	add_basic_file(my_widget.pt)  # .								Ajout d'une entrée.
	qtbot.waitUntil(lambda: "Raw" in layers, timeout=5000)  # .		Attente : qu'il ait mis une image.

	filter_x.active = True  # .										On active le filtre sur X.
	qtbot.waitUntil(lambda: l_name in layers, timeout=5000)  # .	Attente : qu'il ait mis une image.

	filter_y.active = True  # .										On active le filtre sur Y (l'image existe déjà).
	qtbot.waitUntil(lambda: l_name in layers, timeout=5000)  # .	Attente : qu'il ait mis une image.

	filter_x.box[0].setValue(filter_x.box[1].value())  # .			Cas dégénéré, min et max sont égaux.
	qtbot.waitUntil(lambda: l_name not in layers, timeout=5000)  # .Attente : Il supprime le calque en cas dégénéré.

	filter_x.active = False  # .									On désactive le filtre sur X (l'image est recréé).
	qtbot.waitUntil(lambda: l_name in layers, timeout=5000)  # .	Attente : qu'il ait mis une image à nouveau.

	filter_y.active = False  # .									On désactive le filtre sur Y (l'image est à nouveau supprimé).
	qtbot.waitUntil(lambda: l_name not in layers, timeout=5000)  # .Attente : Il supprime le calque.


##################################################
def test_widget_auto_threshold(make_napari_viewer, patched_napari_viewer, capsys, qtbot):
	"""Test click sur le bouton auto_threshold."""
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = make_napari_viewer()
	my_widget = PALMTracerWidget(viewer)

	my_widget._auto_threshold()  # .										   Appel de la méthode auto_threshold sans fichier dans le batch.

	# Ajout d'une entrée
	add_basic_file(my_widget.pt)  # .										   Ajout d'une entrée
	qtbot.waitUntil(lambda: "Raw" in my_widget.viewer.layers, timeout=5000)  # Attente : qu'il ait mis une image
	my_widget._auto_threshold()  # .										   Appel de la méthode auto_threshold.

	lines = get_lines_output(capsys)
	assert "Auto Threshold: 63.95" in lines[-1]


##################################################
def test_widget_thread_process(make_napari_viewer, patched_napari_viewer, qtbot):
	"""Test click sur le bouton process."""
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = make_napari_viewer()
	my_widget = PALMTracerWidget(viewer)

	my_widget._thread_process(my_widget._auto_threshold)
	qtbot.waitUntil(lambda: not my_widget._processing, timeout=5000)  # Attente : que le thread soit terminé

	# appel avec un process en cours
	my_widget._processing = True
	my_widget._thread_process(my_widget._auto_threshold)
	my_widget._processing = False

	# Ajout d'une entrée
	add_basic_file(my_widget.pt)  # .									Ajout d'une entrée
	qtbot.waitUntil(lambda: not my_widget._processing, timeout=5000)  # Attente : que le thread soit terminé
	my_widget._thread_process(my_widget.pt.process)  # .				Appel de la méthode process
	qtbot.waitUntil(lambda: not my_widget._processing, timeout=5000)  # Attente : que le thread soit terminé
	my_widget._thread_process(my_widget._auto_threshold)  # .			Appel de la méthode auto threshold mais impossible de l'executer dans ce contexte.
	qtbot.waitUntil(lambda: not my_widget._processing, timeout=5000)  # Attente : que le thread soit terminé


##################################################
def test_widget_keyblocker(make_napari_viewer, patched_napari_viewer, qtbot):
	viewer = make_napari_viewer()
	my_widget = PALMTracerWidget(viewer)

	qtbot.addWidget(my_widget)
	my_widget.show()

	spin = QSpinBox(my_widget)
	qtbot.addWidget(spin)
	spin.show()
	spin.setFocus()
	event = QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_Backspace, Qt.KeyboardModifier.NoModifier)
	my_widget.key_blocker.eventFilter(viewer.window.qt_viewer, event)


##################################################
def test_viewer3d(make_napari_viewer, patched_napari_viewer, qtbot, monkeypatch, fake_qfiledialog):
	"""Test basique de création du widget."""
	SETTINGS_FILE.unlink(missing_ok=True)
	viewer = make_napari_viewer()
	my_widget = Viewer3DWidget(viewer)

	fake_qfiledialog(Viewer3DWidget, None)  # .										 Simuler un "Cancel" sur le QFileDialog
	my_widget.load_csv()
	qtbot.waitUntil(lambda: not my_widget.points_layer, timeout=5000)  # .			 Attente : que le thread soit terminé

	fake_qfiledialog(Viewer3DWidget, "file.csv")  # .								 Simuler un fichier inexistant
	my_widget.load_csv()
	qtbot.waitUntil(lambda: not my_widget.points_layer, timeout=5000)  # .			 Attente : que le thread soit terminé

	fake_qfiledialog(Viewer3DWidget, f"{INPUT_DIR}/bad_localizations.csv")
	my_widget.load_csv()
	qtbot.waitUntil(lambda: not my_widget.points_layer, timeout=5000)  # .			 Attente : que le thread soit terminé

	fake_qfiledialog(Viewer3DWidget, f"{INPUT_DIR}/localizations.csv")
	my_widget.load_csv()
	qtbot.waitUntil(lambda: my_widget.points_layer is not None, timeout=5000)  # .	 Attente : que le thread soit terminé
	qtbot.waitUntil(lambda: "Points 3D" in my_widget.viewer.layers, timeout=5000)  # Attente : qu'il ait mis une image

	my_widget.load_csv()  # .														 Pour recommencer avec un calque déjà actif
	qtbot.waitUntil(lambda: my_widget.points_layer is not None, timeout=5000)  # .	 Attente : que le thread soit terminé
	qtbot.waitUntil(lambda: "Points 3D" in my_widget.viewer.layers, timeout=5000)  # Attente : qu'il ait mis une image

	my_widget.outliers.value = True  # .											 Suppression des outliers
	my_widget.update_layer()

	my_widget.data = pd.DataFrame()
	my_widget.update_layer()  # .													 Mise à jour avec un dataframe vide
