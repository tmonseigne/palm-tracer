"""Teste les groupes de paramètres."""

import copy

import pytest
from qtpy.QtWidgets import QFormLayout

from palm_tracer.Settings import Groups as sg
from palm_tracer.Settings import Types as st
from palm_tracer.Settings.Groups.HRTrackStack import HRTrackStack
from tests.Utils import *


# --------------------------------------------------
def group_base_test(group: sg.BaseSettingGroup, names: list[str],
					first_type: type[st.BaseSettingType], change: Any, default: Any):
	"""
	Tests de base pour un groupe de paramètres.

	:param group: Groupe de paramètres.
	:param names: Nom des paramètres du groupe.
	:param first_type: Type du premier paramètre.
	:param change: Changement du premier paramètre.
	:param default: Valeur par défaut du premier paramètre.
	"""
	# Nom des éléments
	assert names[0] in group, "La clé n'existe pas"
	assert group.settings_names == names, "Les paramètres ne correspondent pas"
	setting = group[names[0]]
	assert isinstance(setting, first_type), "Le paramètre ne correspond pas"
	for key in group: assert key != "", "Une clé est vide"

	# Utilisation du dictionnaire
	group[names[0]].value = change
	assert group[names[0]].value == change, "Valeur défini non valide."
	min_dictionary = copy.deepcopy(group.to_compact_dict())
	group.reset()
	assert group[names[0]].value == default, "Valeur par défaut non valide."
	group.update_from_compact_dict(min_dictionary)
	assert group[names[0]].value == change, "Valeur récupérée du dictionnaire non valide."

	# Interface
	_ = group.get_ui()
	ui = group.get_ui()  # Second appel l'UI existe déjà

	w = QWidget()
	form = QFormLayout(w)  # Crée et affecte la mise en page au widget
	ui.attach_to_form(form)

	# Hide and seek
	group.hide()
	group.show()

	# Activation
	group.active = False
	assert not group.active, "Les paramètres doivent être désactivés."
	group.active = True
	assert group.active, "Les paramètres doivent être activés."
	group.set_active(1)  # Second appel qui ne fait rien

	# Print
	print(group)
	print(group.settings)

	# Signaux
	received: list[Any] = []
	group.connect(lambda v: received.append(v))
	with group.signal_blocked(): pass
	group.disconnect()
	group.clean_ui()


# ==================================================
# region Contrats communs
# ==================================================
@pytest.mark.parametrize("group_type, keys, setting_type, change, default", [
		pytest.param(sg.Calibration, ["Pixel Size", "Exposure", "Intensity"], st.SpinFloat, 0.32, 0.16, id="calibration"),
		pytest.param(sg.GaussianFit, ["Mode", "Sigma", "Theta", "Z", "Z max", "Model", "Default Model"], st.Combo, 2, 0, id="gaussian-fit"),
		pytest.param(sg.SplineFit, ["Sensor", "Variance Map", "File"], st.Combo, 1, 0, id="spline-fit"),
		pytest.param(sg.BeadsExtraction, ["Max Distance"], st.SpinFloat, 2, 1, id="beads"),
		pytest.param(sg.Tracking, ["Max Distance"], st.SpinFloat, 2, 1, id="tracking"),
		pytest.param(sg.BlinkingReconnection, ["Mode", "Max Duration", "Max Distance"], st.Combo, 1, 0, id="blinking"),
		pytest.param(sg.TrackAnalysis, ["MSD", "Instant Diffusion", "Fit Length", "Fit", "3D"], st.CheckBox, True, False, id="track-analysis"),
		pytest.param(sg.Gallery, ["ROI Size", "ROIs Per Line"], st.SpinInt, 11, 9, id="gallery"),
		pytest.param(sg.GraphDisplay, ["Limits", "Sigma", "Gauss", "Gauss Mix", "KDE", "Poiss", "Exp", "Cumul", "Log Scale", "Count", "Bins"],
					 st.CheckBox, False, True, id="graph-display"),
		pytest.param(sg.HRGaussian, ["Intensity", "Fixed Intensity", "Shape", "Size"], st.SpinInt, 10, 100, id="hr-gaussian"),
		pytest.param(sg.HR3D, ["Z Step", "Axis", "Frames"], st.SpinInt, 10, 20, id="hr-3d"),
		pytest.param(HRTrackStack, ["Head", "Width", "Length", "Fade", "Map", "Background", "Upscale"], st.SpinInt, 5, 1, id="hr-track-stack"),
		pytest.param(sg.Visualization3D, ["Point Size", "Pixel Size", "XY Scale", "Z Scale", "Remove Outliers"], st.SpinFloat, 2, 1, id="visualization-3d")])
def test_group_contract(qtbot, group_type, keys, setting_type, change, default):
	"""Vérifie le même contrat de construction, sérialisation et réinitialisation pour chaque groupe."""
	group_base_test(group_type(), keys, setting_type, change, default)


# ==================================================
# endregion Contrats communs
# ==================================================

# ==================================================
# region BaseSettingGroup
# ==================================================
def test_base_group(qtbot):
	"""Vérifie la classe abstraite."""
	group = sg.BaseSettingGroup()
	group.value = None
	assert group.value is None, "Get Value ne doit rien retourné pour la classe mère."

	received: list[Any] = []
	group.connect(lambda v: received.append(v))
	with group.signal_blocked(): pass
	group.disconnect()


# --------------------------------------------------
@pytest.mark.parametrize("setting_type", [
		pytest.param(st.CheckRangeFloat, id="float-range"), pytest.param(st.CheckRangeInt, id="integer-range")])
@pytest.mark.parametrize("active, label", [
		pytest.param(False, "Deactivate", id="inactive"), pytest.param(True, "Activate", id="active")])
def test_base_group_tostring_range(setting_type, active: bool, label: str):
	"""Vérifie la description des plages avec un tuple de classes compatible Python 3.9."""
	group = sg.BaseSettingGroup()
	setting = setting_type("Range")
	setting.active = active
	group._settings["Range"] = setting
	assert f"- Range : {label} {setting.value}\n" in group.tostring()


# ==================================================
# endregion BaseSettingGroup
# ==================================================

# ==================================================
# region Batch
# ==================================================
@pytest.mark.parametrize("suffix, accepted", [
		pytest.param(".tif", True, id="tif"),
		pytest.param(".tiff", True, id="tiff"),
		pytest.param(".STK", True, id="uppercase-stk"),
		pytest.param(".csv", False, id="csv-rejected"),
		pytest.param(".txt", False, id="text-rejected"),
		pytest.param(".tif.csv", False, id="disguised-extension")])
@pytest.mark.parametrize("source", ["dialog", "drop"], ids=["file-dialog", "explicit-paths"])
def test_batch_filters_new_acquisition_files(tmp_path, fake_qfiledialog, suffix, accepted, source):
	"""Vérifie que l'ajout au Batch utilise les mêmes extensions depuis le dialogue et les chemins déposés."""
	batch = sg.Batch()
	files = batch["Files"]
	path = tmp_path / f"acquisition{suffix}"
	path.touch()
	if source == "dialog":
		fake_qfiledialog(st.FileList, str(path))
		files.add_file()
	else: files.add_files([str(path)])
	assert files.items == ([str(path)] if accepted else [])
	assert files.current_text == (str(path) if accepted else "")


# --------------------------------------------------
def test_batch(qtbot):
	"""Vérifie la classe Batch (constructeur, getter, setter)."""
	batch = sg.Batch()
	group_base_test(batch, ["Files", "Mode"], st.FileList, -1, -1)


# --------------------------------------------------
@pytest.mark.parametrize("files, selected, mode, expected", [
		pytest.param([], 0, 0, ["_PALM_Tracer"], id="no-files"),
		pytest.param(["output/File 1.tif", "output/File 2.tif"], 0, 0, ["output/File 1_PALM_Tracer"], id="first-file"),
		pytest.param(["output/File 1.tif", "output/File 2.tif"], 1, 0, ["output/File 2_PALM_Tracer"], id="second-file"),
		pytest.param(["output/File 1.tif", "output/File 2.tif"], 1, 1, ["output/File 1_PALM_Tracer", "output/File 2_PALM_Tracer"], id="all-files"),
		pytest.param(["output/File 1.tif", "output/File 2.tif"], 1, 2, ["output/File 1_PALM_Tracer"], id="merged-files")])
def test_batch_get_path(qtbot, files, selected, mode, expected):
	"""Vérifie les dossiers de sortie pour chaque mode de traitement du lot."""
	batch = sg.Batch()
	if files:
		batch["Files"].items = files.copy()
		batch["Files"].value = selected
	batch["Mode"].value = mode
	paths = batch.get_paths()
	assert len(paths) == len(expected)
	if not files: assert paths[0].endswith(expected[0])
	else: assert paths == [str(Path(path)) for path in expected]


# --------------------------------------------------
@pytest.mark.parametrize("files, mode, expected_count, expected_shape", [
		pytest.param([], 0, 0, None, id="no-stacks"),
		pytest.param(["stack.tif"] * 3, 0, 1, (10, 128, 256), id="selected-stack"),
		pytest.param(["stack.tif"] * 3, 1, 3, (10, 128, 256), id="separate-stacks"),
		pytest.param(["stack.tif"] * 3, 2, 1, (30, 128, 256), id="compatible-merge"),
		pytest.param(["stack.tif", "stack_quadrant.tif", "stack.tif"], 2, 3, (10, 128, 256), id="invalid-dimensions")])
def test_batch_get_stacks(qtbot, files, mode, expected_count, expected_shape):
	"""Vérifie les piles retournées selon le mode et la compatibilité de leurs dimensions."""
	batch = sg.Batch()
	if files: batch["Files"].items = [str(INPUT_DIR / name) for name in files]
	batch["Mode"].value = mode
	stacks = batch.get_stacks()
	assert len(stacks) == expected_count
	# La forme de la première pile suffit à distinguer le mode fusion du mode séparé.
	if stacks: assert stacks[0].shape == expected_shape


# ==================================================
# endregion Batch
# ==================================================

# ==================================================
# region Localization
# ==================================================
def test_localization(qtbot):
	"""Vérifie la classe Localisation (constructeur, getter, setter)."""
	g = sg.Localization()
	group_base_test(g, ["Preview", "Threshold", "Auto Threshold", "ROI Shape", "ROI Size", "Watershed", "Fit", "Gaussian Fit", "Spline Fit"],
					st.CheckBox, True, False)

	assert isinstance(g.gaussian, sg.GaussianFit)
	assert isinstance(g.spline, sg.SplineFit)


# --------------------------------------------------
@pytest.mark.parametrize("with_ui", [False, True], ids=["without-ui", "with-ui"])
@pytest.mark.parametrize("selected, expected_fit, expected_params", [
		pytest.param(0, 0, [7], id="no-fit"),
		pytest.param(1, 1, [7, 1, 2, 0], id="gaussian-fit")])
def test_localization_fit(qtbot, with_ui, selected, expected_fit, expected_params):
	"""Vérifie le numéro et les paramètres du mode d'ajustement sélectionné."""
	loc = sg.Localization()
	if with_ui: loc.get_ui()
	loc["Fit"].value = selected
	assert loc.get_fit() == expected_fit, "Numéro du Fit incorrect"
	np.testing.assert_array_equal(loc.get_fit_params(), np.array(expected_params, dtype=float))


# --------------------------------------------------
@pytest.mark.parametrize("with_ui", [False, True], ids=["without-ui", "with-ui"])
def test_localization_spline_missing_file(qtbot, with_ui):
	"""Identifie le mode spline et refuse ses paramètres si aucun fichier de calibration n'est disponible."""
	loc = sg.Localization()
	if with_ui: loc.get_ui()
	loc["Fit"].value = 2
	assert loc.get_fit() == 5, "Numéro du Fit incorrect"
	with pytest.raises(OSError) as exception_info: loc.get_fit_params()
	assert exception_info.type is OSError, "L'erreur relevé n'est pas correcte."


# ==================================================
# endregion Localization
# ==================================================

# ==================================================
# region GaussianFit
# ==================================================
def test_gaussian_fit_z(qtbot):
	"""Vérifie la classe GaussianFit avec affichage/masquage des éléments."""
	grp = sg.GaussianFit()
	ui_z = grp["Z"].get_ui()
	ui_z_max = grp["Z max"].get_ui()
	assert ui_z.boxes[0].isHidden()
	grp["Mode"].value = 2
	assert not ui_z.boxes[0].isHidden()  # Ne pas utiliser isVisible, car cela demande visible à l'écran et dans les tests unitaires, c'est particulier.
	grp["Z"].value = True
	assert not ui_z_max.boxes[0].isHidden()
	grp["Z"].value = False
	assert ui_z_max.boxes[0].isHidden()
	grp["Z"].value = True
	assert not ui_z_max.boxes[0].isHidden()
	grp["Mode"].value = 0
	assert ui_z.boxes[0].isHidden()
	assert ui_z_max.boxes[0].isHidden()


# --------------------------------------------------
@pytest.mark.parametrize("initial", [False, True], ids=["specific-model", "default-model"])
def test_gaussian_fit_default_model(qtbot, initial):
	"""Vérifie le choix persistant et le grisement des champs dans plusieurs interfaces."""
	grp = sg.GaussianFit()
	grp["Mode"].value = 2
	grp["Z"].value = True
	grp["Default Model"].value = initial
	for name in ("default", "second"): grp.get_ui(name)
	for active in (initial, not initial):
		grp["Default Model"].value = active
		for name in ("default", "second"):
			for box in grp["Model"].get_ui(name).boxes: assert box.isEnabled() == (not active)
		data = grp.to_compact_dict()
		loaded = sg.GaussianFit()
		loaded.update_from_compact_dict(data)
		assert loaded["Default Model"].value == active
	grp["Z"].value = False
	assert grp["Default Model"].get_ui().boxes[0].isHidden()


# ==================================================
# endregion GaussianFit
# ==================================================

# ==================================================
# region Filters, FiltersL et FiltersT
# ==================================================
def test_filters(qtbot):
	"""Vérifie la classe Filters (constructeur, getter, setter)."""
	g = sg.Filters()
	group_base_test(g, ["Save", "Plane", "ROI", "Localization", "Tracks"], st.CheckBox, True, False)
	g.deactivate_filters()
	g.update_limits(None)
	g.update_limits(10)
	assert isinstance(g.localization, sg.FiltersL)
	assert isinstance(g.tracking, sg.FiltersT)
	_ = g.get_ui()
	g.connect_button(lambda: print("Hi"), "default", "0")  # Bouton inexistant
	g.connect_button(lambda: print("Hi"), "new", "0")  # UI inexistante
	g.connect_button(lambda: print("Hi"), "default", "reset")

	g.show_part()
	g.show_part(localization=False, tracking=False)


# --------------------------------------------------
def test_filters_l(qtbot):
	"""Vérifie la classe FiltersL (constructeur, getter, setter)."""
	g = sg.FiltersL()
	group_base_test(g, ["Z", "Intensity", "Sigma X", "Sigma Y", "Circularity", "Theta", "MSE XY", "MSE Z"], st.CheckRangeInt, [2, 9], [-2000, 2000])
	g.deactivate_filters()


# --------------------------------------------------
def test_filters_t(qtbot):
	"""Vérifie la classe FiltersT (constructeur, getter, setter)."""
	g = sg.FiltersT()
	group_base_test(g, ["Track", "Length", "ROI Time", "Instant D", "D Coeff", "Alpha", "Speed", "Confinement"], st.CheckIntSelection, "1;3-4", "")
	g.deactivate_filters()


# ==================================================
# endregion Filters, FiltersL et FiltersT
# ==================================================

# ==================================================
# region Graph
# ==================================================
def test_graph(qtbot):
	"""Vérifie la classe Graph (constructeur, getter, setter)."""
	g = sg.Graph()
	group_base_test(sg.Graph(), ["Mode", "Type", "Source", "Source B", "MSD Step", "Display"], st.ButtonGroup, 1, 0)
	g["Type"].value = 1  # Passage aux Tracks
	g["Source"].value = 3  # Passage au MSD
	g["Mode"].value = 1  # Passage aux Scatter Plot
	g["Mode"].value = 2  # Passage aux nuages de points.

	assert isinstance(g.display, sg.GraphDisplay)


# ==================================================
# endregion Graph
# ==================================================

# ==================================================
# region HR
# ==================================================
def test_hr(qtbot):
	"""Vérifie la classe HR (constructeur, getter, setter)."""
	g = sg.HR()
	g["Type"].value = 1  # Passage aux Tracks
	g["Dimension"].value = 1  # Passage à Z-stack
	g["Dimension"].value = 2  # Passage à 3D Rotation
	g["Dimension"].value = 3  # Passage à Track Stack
	g["Dimension"].reset()
	group_base_test(g, ["Dimension", "Type", "Source", "Scaling", "Color mode", "Background", "Ratio", "Crop", "Remove Beads",
						"Drift Correction", "Smooth Drift", "Gaussian", "3D", "T-Stack"], st.ButtonGroup, 1, 0)
	assert isinstance(g.gaussian, sg.HRGaussian)
	assert isinstance(g.hr_3d, sg.HR3D)
	assert isinstance(g.track_stack, HRTrackStack)

# ==================================================
# endregion HR
# ==================================================
