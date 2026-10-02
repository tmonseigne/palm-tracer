"""Teste le widget Napari de visualisation haute résolution des résultats."""

import shutil
from types import SimpleNamespace

import pytest
from napari.components import ViewerModel
from qtpy.QtCore import QCoreApplication, QEvent, Qt

from palm_tracer._tests.Utils import *
from palm_tracer.Settings.Types import BaseUIType, ButtonGroup
from palm_tracer.Tools import FileIO
from palm_tracer.UI import ViewerHRWidget

INPUT_FILE = INPUT_DIR / "stack.tif"
OUTPUT_FOLDER = INPUT_DIR / "stack_PALM_Tracer"


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
def test_results_status_automatic_update(qtbot):
	"""Vérifie que les statuts sont actualisés directement par Results."""
	viewer = ViewerModel()
	w = ViewerHRWidget(viewer, get_fake_pt())
	qtbot.addWidget(w)
	results_ui = w._pt.results.get_ui(w.UI_NAME)

	w._pt.results.reset()
	assert results_ui._labels["Beads"].text() == "No"

	w._pt.results["bds"] = pd.DataFrame(np.zeros((2, 1)))
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
# region Liaison avec PALMTracer
# ==================================================
##################################################
def test_check_beads(qtbot):
	"""Vérifie le widget."""
	viewer = ViewerModel()
	w = ViewerHRWidget(viewer, get_fake_pt())
	qtbot.addWidget(w)

	ui: BaseUIType = w._pt.settings.hr["Remove Beads"].get_ui(w.UI_NAME)
	w._check_beads()  # False
	assert ui.boxes[0].isHidden()
	w._pt.results["bds"] = w._pt.results["loc"].copy()
	w._check_beads()  # True
	assert not ui.boxes[0].isHidden()


##################################################
def test_add_stack(qtbot, capsys, fake_qfiledialog):
	"""Vérifie le widget."""
	viewer = ViewerModel()
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
	pt = PALMTracer()
	w = ViewerHRWidget(viewer, pt)
	qtbot.addWidget(w)

	fake_qfiledialog(FileList, f"{INPUT_DIR / 'stack.tif'}")
	qtbot.mouseClick(w._btn_add_stack, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "No valid settings file to load." in lines[0]


##################################################
def test_actualize(qtbot):
	"""Vérifie le widget."""
	viewer = ViewerModel()
	w = ViewerHRWidget(viewer, PALMTracer())
	qtbot.addWidget(w)

	qtbot.mouseClick(w._btn_actualize, Qt.MouseButton.LeftButton)

	w._pt._stack = np.zeros((1, 1, 1), dtype=np.uint16)
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

	ui: BaseUIType = cast(ButtonGroup, w._pt.settings.hr["Type"]).get_ui(w.UI_NAME)
	qtbot.mouseClick(ui.boxes[0], Qt.MouseButton.LeftButton)  # Appuie sur localization
	assert w._pt.settings.hr["Type"].value == 0
	qtbot.mouseClick(ui.boxes[1], Qt.MouseButton.LeftButton)  # Appuie sur Tracks
	assert w._pt.settings.hr["Type"].value == 1


# ==================================================
# endregion Liaison avec PALMTracer
# ==================================================

# ==================================================
# region Dessin
# ==================================================
##################################################
def test_generate_bad(qtbot, capsys, fake_qfiledialog):
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
	fake_qfiledialog(FileList, f"{INPUT_DIR / 'stack.tif'}")
	qtbot.mouseClick(w._btn_add_stack, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "No valid settings file to load." in lines[0]

	# Idem aucune pile de chargée, car il n'a pas eu de process précédent.
	w._generate()
	lines = get_lines_output(capsys)
	assert "WARNING: No stack processed loaded." in lines[0]

	# Un process, mais aucun tableau d'exploitable.
	w._pt.process()  # Process Vide pour créer le dossier et un paramètre de base
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
	w._pt.settings.hr["Type"].value = 1
	w._generate()
	assert not w._layers[w.LAYERS_NAME[1]].visible
	assert not w._layers["Tracks"].visible
	assert viewer.dims.range[0].stop == np.max(w._layers["Tracks"].data[:, 1])
	lines = get_lines_output(capsys)
	assert len(lines) == 0
	w._pt.settings.hr["Dimension"].value = 1
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
	previous_box = w._pt.settings.rois.hr_box
	previous_image = w.visualization
	previous_points = w._layers[w.LAYERS_NAME[1]].data.copy()
	assert previous_box[0] > 0 and previous_box[2] > 0
	w._pt.results.reset()
	get_lines_output(capsys)

	w._generate()
	assert "WARNING: No visualization available." in get_lines_output(capsys)
	assert w._pt.settings.rois.hr_box == previous_box
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
	state = SimpleNamespace(viewer=viewer, LAYERS_NAME=ViewerHRWidget.LAYERS_NAME, _layers={"Visualization": layer})
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
