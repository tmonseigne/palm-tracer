"""Fichier des tests pour le widget."""
import shutil

import pytest
from qtpy.QtCore import Qt

from palm_tracer._tests.Utils import *
from palm_tracer.UI import ViewerHRWidget

INPUT_FILE = INPUT_DIR / "stack.tif"
OUTPUT_FOLDER = INPUT_DIR / "stack_PALM_Tracer"


##################################################
def get_pt():
	"""Instance basique de PALMTracer pour chaque test."""
	pt = PALMTracer()
	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.update_box([f"{INPUT_DIR / 'stack.tif'}"])
	pt.df["loc"] = pd.read_csv(INPUT_DIR / "localizations.csv")
	pt.df["f_loc"] = pt.df["loc"].copy()
	pt.df["trc"] = pd.read_csv(INPUT_DIR / "tracking.csv")
	pt.df["f_trc"] = pt.df["trc"].copy()
	pt.df["blk"] = pt.df["trc"].copy()
	pt.df["f_blk"] = pt.df["trc"].copy()
	pt.df["MSD"] = pd.read_csv(INPUT_DIR / "tracking_MSD.csv")
	pt.df["InD"] = pd.read_csv(INPUT_DIR / "tracking_InstantD.csv")
	pt.df["Fit"] = pd.read_csv(INPUT_DIR / "tracking_Fit.csv")
	return pt


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_widget_creation(make_napari_viewer, capsys):
	"""Test basique de création du widget."""
	viewer = make_napari_viewer()  # .				Créer un viewer à l'aide de la fixture.
	my_widget = ViewerHRWidget(viewer, get_pt())  # Créer notre widget, en passant par le viewer.

	try: viewer.close()
	except Exception: pass


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_add_stack(make_napari_viewer, qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Test basique du widget."""
	viewer = make_napari_viewer()  # .		  Créer un viewer à l'aide de la fixture.
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
	pt = PALMTracer()
	my_widget = ViewerHRWidget(viewer, pt)  # Créer notre widget, en passant par le viewer.

	fake_qfiledialog(FileList, f"{INPUT_DIR / 'stack.tif'}")
	qtbot.mouseClick(my_widget._btn_add_stack, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "No valid settings file to load." in lines[0]

	try: viewer.close()
	except Exception: pass


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_change_source(make_napari_viewer, qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Test basique du widget."""
	viewer = make_napari_viewer()  # .				Créer un viewer à l'aide de la fixture.
	my_widget = ViewerHRWidget(viewer, get_pt())  # Créer notre widget, en passant par le viewer.

	assert my_widget._cmb_src.items[0] == "Count"

	qtbot.mouseClick(my_widget._btn_src["Tracks"], Qt.MouseButton.LeftButton)
	assert my_widget._cmb_src.items[0] == "Track Number"

	qtbot.mouseClick(my_widget._btn_src["Localization"], Qt.MouseButton.LeftButton)
	assert my_widget._cmb_src.items[0] == "Count"

	try: viewer.close()
	except Exception: pass


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_actualize(make_napari_viewer, qtbot, capsys):
	"""Test basique du widget."""
	viewer = make_napari_viewer()  # .					Créer un viewer à l'aide de la fixture.
	my_widget = ViewerHRWidget(viewer, PALMTracer())  # Créer notre widget, en passant par le viewer.

	qtbot.mouseClick(my_widget._btn_actualize, Qt.MouseButton.LeftButton)

	my_widget._pt._stack = np.zeros((1, 1, 1), dtype=np.uint16)
	qtbot.mouseClick(my_widget._btn_actualize, Qt.MouseButton.LeftButton)

	try: viewer.close()
	except Exception: pass


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_reset_filtered(make_napari_viewer, qtbot, capsys):
	"""Test basique de création du widget."""

	viewer = make_napari_viewer()  # .				Créer un viewer à l'aide de la fixture.
	my_widget = ViewerHRWidget(viewer, get_pt())  # Créer notre widget, en passant par le viewer.

	assert my_widget._status["Localization"].text() == "Yes (Filtered)", "Status Incorrect."
	qtbot.mouseClick(my_widget._filters.buttons["reset"], Qt.MouseButton.LeftButton)
	assert my_widget._status["Localization"].text() == "Yes", "Status Incorrect."

	try: viewer.close()
	except Exception: pass


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_update_filtered(make_napari_viewer, qtbot, capsys):
	"""Test basique de création du widget."""

	viewer = make_napari_viewer()  # .				Créer un viewer à l'aide de la fixture.
	my_widget = ViewerHRWidget(viewer, get_pt())  # Créer notre widget, en passant par le viewer.

	qtbot.mouseClick(my_widget._filters.buttons["reset"], Qt.MouseButton.LeftButton)
	assert my_widget._status["Localization"].text() == "Yes", "Status Incorrect."  # .			On n'a pas de tableaux filtrés

	# Changement des valeurs
	ref = my_widget._filters["Plane"].value
	new_f = [2, 50]
	my_widget._filters["Plane"].value = new_f
	my_widget._filters["Plane"].active = True
	assert my_widget._filters["Plane"].value == new_f, "Filtre incorrect."
	assert my_widget._pt.settings.filtering["Plane"].value == ref, "Filtre incorrect."  # .		Il n'est pas encore à jour.

	qtbot.mouseClick(my_widget._filters.buttons["update"], Qt.MouseButton.LeftButton)

	assert my_widget._pt.settings.filtering["Plane"].value == new_f  # .						Il a été mis à jour
	assert my_widget._status["Localization"].text() == "Yes (Filtered)", "Status Incorrect."  # On a à nouveau un tableau filtré.

	try: viewer.close()
	except Exception: pass


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_save(make_napari_viewer, qtbot, capsys):
	"""Test basique de création du widget."""
	res = OUTPUT_DIR / "HR.png"
	res.unlink(missing_ok=True)  # .				Suppression du fichier de résultat s'il existe.

	viewer = make_napari_viewer()  # .				Créer un viewer à l'aide de la fixture.
	my_widget = ViewerHRWidget(viewer, get_pt())  # Créer notre widget, en passant par le viewer.

	my_widget._filename = ""
	qtbot.mouseClick(my_widget._btn_save, Qt.MouseButton.LeftButton)  # Il ne fait rien si pas de nom de fichier.
	my_widget._filename = str(res.resolve())
	qtbot.mouseClick(my_widget._btn_save, Qt.MouseButton.LeftButton)
	assert res.exists(), "File not saved."

	try: viewer.close()
	except Exception: pass


##################################################
@pytest.mark.skipif(is_headless(), reason="Napari/VisPy/QT causes segfault in headless macOS and Unix.")
def test_generate(make_napari_viewer, qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Test basique de création du widget."""
	viewer = make_napari_viewer()  # .		  Créer un viewer à l'aide de la fixture.
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
	pt = PALMTracer()
	my_widget = ViewerHRWidget(viewer, pt)  # Créer notre widget, en passant par le viewer.

	# palm tracer n'est pas initialisé
	qtbot.mouseClick(my_widget._btn_generate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "WARNING: No stack processed loaded." in lines[0]

	# Chargement d'une pile, mais aucun process
	fake_qfiledialog(FileList, f"{INPUT_DIR / 'stack.tif'}")
	qtbot.mouseClick(my_widget._btn_add_stack, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "No valid settings file to load." in lines[0]

	# Idem aucune pile de chargée (car il n'a pas eu de process précédent)
	qtbot.mouseClick(my_widget._btn_generate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "WARNING: No stack processed loaded." in lines[0]

	# Un process, mais aucun tableau d'exploitable.
	my_widget._pt.process()  # Process Vide pour créer le dossier et un setting de base
	_ = get_lines_output(capsys)
	qtbot.mouseClick(my_widget._btn_generate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "WARNING: No localization file available." in lines[0]

	# Ajout d'un tableau de localisation
	pt.df["loc"] = pd.read_csv(INPUT_DIR / "localizations.csv")
	qtbot.mouseClick(my_widget._btn_generate, Qt.MouseButton.LeftButton)
	layers = my_widget.viewer.layers
	qtbot.waitUntil(lambda: "Localizations" in layers, timeout=5000)  # Attente : Création du calque.
	qtbot.waitUntil(lambda: "Visualization" in layers, timeout=5000)  # Attente : Création du calque.

	# Passage au suivi sans tableau
	qtbot.mouseClick(my_widget._btn_src["Tracks"], Qt.MouseButton.LeftButton)
	qtbot.mouseClick(my_widget._btn_generate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "WARNING: No tracking file available." in lines[-1] # dernière ligne, car il peut y avoir un warning lors de la suppression des calques
	layers = my_widget.viewer.layers
	qtbot.waitUntil(lambda: "Localizations" not in layers, timeout=5000)  # Attente : Suppression du calque.
	# qtbot.waitUntil(lambda: "Visualization" not in layers, timeout=5000)  # Attente : Suppression du calque.

	# Ajout d'un tableau de Suivi
	pt.df["trc"] = pd.read_csv(INPUT_DIR / "tracking.csv")
	qtbot.mouseClick(my_widget._btn_generate, Qt.MouseButton.LeftButton)
	layers = my_widget.viewer.layers
	qtbot.waitUntil(lambda: "Tracks" in layers, timeout=5000)  # .		 Attente : Création du calque.
	qtbot.waitUntil(lambda: "Visualization" in layers, timeout=5000)  # .Attente : Création du calque.

	try: viewer.close()
	except Exception: pass
