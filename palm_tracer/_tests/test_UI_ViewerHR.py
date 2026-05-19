"""Fichier des tests pour le widget."""
import shutil

from qtpy.QtCore import Qt

from palm_tracer._tests.Utils import *
from palm_tracer.Processing import Parsing
from palm_tracer.UI import ViewerHRWidget

INPUT_FILE = INPUT_DIR / "stack.tif"
OUTPUT_FOLDER = INPUT_DIR / "stack_PALM_Tracer"


##################################################
def test_widget_creation(make_napari_viewer, patched_napari_viewer, capsys):
	"""Test basique de création du widget."""
	viewer = make_napari_viewer()  # .		Créer un viewer à l'aide de la fixture.
	w = ViewerHRWidget(viewer, get_fake_pt())  # Créer notre widget, en passant par le viewer.


##################################################
def test_add_stack(make_napari_viewer, patched_napari_viewer, qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Test basique du widget."""
	viewer = make_napari_viewer()  # .Créer un viewer à l'aide de la fixture.
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
	pt = PALMTracer()
	w = ViewerHRWidget(viewer, pt)  # Créer notre widget, en passant par le viewer.

	fake_qfiledialog(FileList, f"{INPUT_DIR / 'stack.tif'}")
	qtbot.mouseClick(w._btn_add_stack, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "No valid settings file to load." in lines[0]


##################################################
def test_change_source(make_napari_viewer, patched_napari_viewer, qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Test basique du widget."""
	viewer = make_napari_viewer()  # .		Créer un viewer à l'aide de la fixture.
	w = ViewerHRWidget(viewer, get_fake_pt())  # Créer notre widget, en passant par le viewer.

	assert w._cmb_src.items[0] == "Count"

	qtbot.mouseClick(w._btn_src["Tracks"], Qt.MouseButton.LeftButton)
	assert w._cmb_src.items[0] == "Track Number"

	qtbot.mouseClick(w._btn_src["Localization"], Qt.MouseButton.LeftButton)
	assert w._cmb_src.items[0] == "Count"


##################################################
def test_actualize(make_napari_viewer, patched_napari_viewer, qtbot, capsys):
	"""Test basique du widget."""
	viewer = make_napari_viewer()  # .			Créer un viewer à l'aide de la fixture.
	w = ViewerHRWidget(viewer, PALMTracer())  # Créer notre widget, en passant par le viewer.

	qtbot.mouseClick(w._btn_actualize, Qt.MouseButton.LeftButton)

	w._pt._stack = np.zeros((1, 1, 1), dtype=np.uint16)
	qtbot.mouseClick(w._btn_actualize, Qt.MouseButton.LeftButton)


##################################################
def test_reset_filtered(make_napari_viewer, patched_napari_viewer, qtbot, capsys):
	"""Test basique de création du widget."""

	viewer = make_napari_viewer()  # .		Créer un viewer à l'aide de la fixture.
	w = ViewerHRWidget(viewer, get_fake_pt())  # Créer notre widget, en passant par le viewer.

	assert w._status["Localization"].text() == "Yes (Filtered)", "Status Incorrect."
	qtbot.mouseClick(w._filters.buttons["reset"], Qt.MouseButton.LeftButton)
	assert w._status["Localization"].text() == "Yes", "Status Incorrect."


##################################################
def test_update_filtered(make_napari_viewer, patched_napari_viewer, qtbot, capsys):
	"""Test basique de création du widget."""

	viewer = make_napari_viewer()  # .		Créer un viewer à l'aide de la fixture.
	w = ViewerHRWidget(viewer, get_fake_pt())  # Créer notre widget, en passant par le viewer.

	qtbot.mouseClick(w._filters.buttons["reset"], Qt.MouseButton.LeftButton)
	assert w._status["Localization"].text() == "Yes", "Status Incorrect."  # .			On n'a pas de tableaux filtrés

	# Changement des valeurs
	ref = w._filters["Plane"].value
	new_f = [2, 50]
	w._filters["Plane"].value = new_f
	w._filters["Plane"].active = True
	assert w._filters["Plane"].value == new_f, "Filtre incorrect."
	assert w._pt.settings.filters["Plane"].value == ref, "Filtre incorrect."  # .		Il n'est pas encore à jour.

	qtbot.mouseClick(w._filters.buttons["update"], Qt.MouseButton.LeftButton)

	assert w._pt.settings.filters["Plane"].value == new_f  # .						Il a été mis à jour
	assert w._status["Localization"].text() == "Yes (Filtered)", "Status Incorrect."  # On a à nouveau un tableau filtré.


##################################################
def test_save(make_napari_viewer, patched_napari_viewer, qtbot, capsys):
	"""Test basique de création du widget."""
	res = OUTPUT_DIR / "HR.png"
	res.unlink(missing_ok=True)  # .		Suppression du fichier de résultat s'il existe.

	viewer = make_napari_viewer()  # .		Créer un viewer à l'aide de la fixture.
	w = ViewerHRWidget(viewer, get_fake_pt())  # Créer notre widget, en passant par le viewer.

	w._filename = ""
	qtbot.mouseClick(w._btn_save, Qt.MouseButton.LeftButton)  # Il ne fait rien si pas de nom de fichier.
	w._filename = str(res.resolve())
	qtbot.mouseClick(w._btn_save, Qt.MouseButton.LeftButton)
	assert res.exists(), "File not saved."
	res.unlink(missing_ok=True)  # .		Suppression du fichier de résultat s'il existe.


##################################################
def test_screenshot(make_napari_viewer, patched_napari_viewer, qtbot, capsys, monkeypatch, fake_qfiledialog, fake_napari_layers):
	"""Test basique de création du widget."""
	res = OUTPUT_DIR / "HR.png"
	res.unlink(missing_ok=True)  # .				Suppression du fichier de résultat s'il existe.
	viewer = make_napari_viewer()  # .				Créer un viewer à l'aide de la fixture.
	fake_napari_layers(viewer)

	# --- Mock screenshot ---
	def _fake_screenshot(self, path, canvas_only=True):
		"""Fake screenshot : écrit un faux PNG."""
		Path(path).write_bytes(b"fake png")

	monkeypatch.setattr(type(viewer), "screenshot", _fake_screenshot, raising=True)

	w = ViewerHRWidget(viewer, get_fake_pt())  # Créer notre widget, en passant par le viewer.

	w._screenshot_filename = ""
	qtbot.mouseClick(w._btn_screenshot, Qt.MouseButton.LeftButton)  # Il ne fait rien si pas de nom de fichier.
	assert not res.exists()

	w._screenshot_filename = str(res.resolve())
	qtbot.mouseClick(w._btn_screenshot, Qt.MouseButton.LeftButton)
	assert res.exists(), "File not saved."
	res.unlink(missing_ok=True)  # .				Suppression du fichier de résultat s'il existe.


##################################################
def test_crop(make_napari_viewer, patched_napari_viewer):
	"""Test basique de création du widget."""
	res = OUTPUT_DIR / "HR.png"
	res.unlink(missing_ok=True)  # .		Suppression du fichier de résultat s'il existe.

	viewer = make_napari_viewer()  # .		Créer un viewer à l'aide de la fixture.
	w = ViewerHRWidget(viewer, get_fake_pt())  # Créer notre widget, en passant par le viewer.

	res = w._crop()  # .					Crop à True, image noire
	assert res == np.zeros((1, 1), dtype=np.uint16)

	w.visualization = np.zeros((10, 10), dtype=np.uint16)
	w.visualization[2:4, 6:] = 1
	ref = w.visualization[:-1, 1:].copy()  # Le crop avec une marge de 5 va très peu recadrer
	assert np.allclose(w._crop(), ref)  # .	Crop à True, avec un carré à 1 et une marge (par défaut) de 5
	assert np.allclose(w._crop(0), 1)  # .	Crop à True, avec aucune marge

	w._chk_crop.value = False
	w._crop()  # .							Crop à False


##################################################
def test_generate_bad(make_napari_viewer, patched_napari_viewer, qtbot, capsys, monkeypatch, fake_qfiledialog, fake_napari_layers):
	"""Test basique de création du widget."""
	viewer = make_napari_viewer()  # .Créer un viewer à l'aide de la fixture.
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
	pt = PALMTracer()
	w = ViewerHRWidget(viewer, pt)  # Créer notre widget, en passant par le viewer.

	fake_napari_layers(viewer)

	# palm tracer n'est pas initialisé
	qtbot.mouseClick(w._btn_generate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "WARNING: No stack processed loaded." in lines[0]

	# Chargement d'une pile, mais aucun process
	fake_qfiledialog(FileList, f"{INPUT_DIR / 'stack.tif'}")
	qtbot.mouseClick(w._btn_add_stack, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "No valid settings file to load." in lines[0]

	# Idem aucune pile de chargée (car il n'a pas eu de process précédent)
	qtbot.mouseClick(w._btn_generate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "WARNING: No stack processed loaded." in lines[0]

	# Un process, mais aucun tableau d'exploitable.
	w._pt.process()  # Process Vide pour créer le dossier et un setting de base
	_ = get_lines_output(capsys)
	qtbot.mouseClick(w._btn_generate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "WARNING: No localization file available." in lines[0]

	# Passage au suivi sans tableau
	qtbot.mouseClick(w._btn_src["Tracks"], Qt.MouseButton.LeftButton)
	qtbot.mouseClick(w._btn_generate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "WARNING: No tracking file available." in lines[-1]  # dernière ligne, car il peut y avoir un warning lors de la suppression des calques


##################################################
def test_generate(make_napari_viewer, patched_napari_viewer, qtbot, capsys, monkeypatch, fake_qfiledialog, fake_napari_layers):
	"""Test basique de création du widget."""
	viewer = make_napari_viewer()  # Créer un viewer à l'aide de la fixture.
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
	pt = PALMTracer()
	add_basic_file(pt)
	pt.process()  # Process Vide pour créer le dossier et un setting de base
	shutil.copy2(INPUT_DIR / "localizations.csv", INPUT_DIR / "stack_PALM_Tracer" / f"localizations-{pt._timestamp}.csv")
	shutil.copy2(INPUT_DIR / "tracking.csv", INPUT_DIR / "stack_PALM_Tracer" / f"tracking-{pt._timestamp}.csv")
	shutil.copy2(INPUT_DIR / "beads.csv", INPUT_DIR / "stack_PALM_Tracer" / f"beads-{pt._timestamp}.csv")
	pt.load()
	pt.df["loc"]["Integrated Intensity"] *= 100
	w = ViewerHRWidget(viewer, pt)  # Créer notre widget, en passant par le viewer.
	fake_napari_layers(viewer)

	w._spn_upscale.value = 1
	w._cmb_src.value = 4
	w._spn_gauss_intensity.value = 1
	upscale = w._spn_upscale.value
	shape = (128 * upscale, 256 * upscale)
	ref = np.zeros(shape)

	# Génération de la localisation
	w._chk_beads_remove.value = False
	qtbot.mouseClick(w._btn_generate, Qt.MouseButton.LeftButton)
	ref[2, 1] = 200
	ref[3, 2] = 200
	ref[5, 4] = 100
	assert np.allclose(ref, w.visualization)

	# Suppression de billes
	w._chk_beads_remove.value = True
	qtbot.mouseClick(w._btn_generate, Qt.MouseButton.LeftButton)
	ref = np.zeros(shape)
	ref[2, 1] = ref[3, 2] = ref[5, 4] = 100  # Il supprime 2 localisations donc plus qu'une sur les supperpositions
	assert np.allclose(ref, w.visualization)

	# Génération de la localisation en mode gaussien
	w._chk_gaussian.value = True
	w._cmb_color_mode.value = 1
	qtbot.mouseClick(w._btn_generate, Qt.MouseButton.LeftButton)
	ref = np.zeros(shape)
	patch = [[1, 2, 1, 0, 0, 0, 0],
			 [5, 9, 5, 1, 0, 0, 0],
			 [9, 15, 9, 5, 1, 0, 0],
			 [5, 9, 15, 9, 2, 1, 0],
			 [1, 5, 9, 5, 9, 5, 1],
			 [0, 1, 2, 9, 15, 9, 2],
			 [0, 0, 1, 5, 9, 5, 1],
			 [0, 0, 0, 1, 2, 1, 0]]
	ref[0:8, 0:7] += patch
	assert np.allclose(ref, w.visualization)

	# Génération du suivi
	qtbot.mouseClick(w._btn_src["Tracks"], Qt.MouseButton.LeftButton)
	qtbot.mouseClick(w._btn_generate, Qt.MouseButton.LeftButton)


##################################################
def test_generate_drift(make_napari_viewer, patched_napari_viewer, qtbot, capsys, monkeypatch, fake_qfiledialog, fake_napari_layers):
	"""Test basique de création du widget."""
	viewer = make_napari_viewer()  # .Créer un viewer à l'aide de la fixture.
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
	pt = PALMTracer()
	w = ViewerHRWidget(viewer, pt)  # Créer notre widget, en passant par le viewer.

	fake_napari_layers(viewer)

	# Chargement d'une pile
	fake_qfiledialog(FileList, f"{INPUT_DIR / 'stack.tif'}")
	qtbot.mouseClick(w._btn_add_stack, Qt.MouseButton.LeftButton)
	w._chk_drift_correction.value = True
	w._pt.process()  # Process Vide pour créer le dossier et un setting de base

	# Sans localization la sortie sera entièrement noire.
	qtbot.mouseClick(w._btn_generate, Qt.MouseButton.LeftButton)
	w._spn_upscale.value = 2
	upscale = w._spn_upscale.value
	shape = (128 * upscale, 256 * upscale)
	ref = np.zeros(shape)
	assert np.allclose(ref, w.visualization)

	# Sortie avec le fichier de localisation, mais pas de billes.
	pt.df["loc"] = pd.read_csv(INPUT_DIR / "localizations.csv")
	_ = get_lines_output(capsys)  # Nettoyage de la sortie
	qtbot.mouseClick(w._btn_generate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "WARNING: No beads file available to correct drift." in lines[0]  # dernière ligne, car possible warning lors de la suppression des calques

	ref = np.zeros(shape)
	ref[4, 2] = 2
	ref[6, 4] = 2
	ref[8, 6] = 1
	ref[10, 8] = 1
	assert np.allclose(ref, w.visualization)

	# Sortie avec le fichier de localisation et un fichier de billes contenant une valeur abhérrante
	pt.df["bds"] = pd.DataFrame(
			[[1, 1, 1, 1, 2, 3, 1, 1, 1, 0, 1],
			 [1, 2, 2, 2, 3, 4, 1, 1, 1, 0, 1],
			 [1, 3, 3, 50, 3, 4, 1, 1, 1, 0, 1],
			 [1, 4, 4, 4, 3, 4, 1, 1, 1, 0, 1],
			 [1, 5, 5, 5, 3, 4, 1, 1, 1, 0, 1]],
			columns=Parsing.FILES_COLUMNS["Beads"]["columns"])
	pt.df["loc"] = pd.DataFrame(
			[[1, 1, 1, -1, 0, 0, 0, 1, 0, 0, 0, -1, -1, 0, 0, 1, 1, 1],
			 [2, 2, 2, -1, 1, 0, 0, 1, 0, 0, 0, -1, -1, 0, 0, 1, 1, 1],
			 [3, 3, 3, -1, 2, 0, 0, 1, 0, 0, 0, -1, -1, 0, 0, 1, 1, 1],
			 [4, 4, 4, -1, 3, 0, 0, 1, 0, 0, 0, -1, -1, 0, 0, 1, 1, 1],
			 [5, 5, 5, -1, 4, 0, 0, 1, 0, 0, 0, -1, -1, 0, 0, 1, 1, 1]],
			columns=Parsing.FILES_COLUMNS["Localization"]["columns"])

	qtbot.mouseClick(w._btn_generate, Qt.MouseButton.LeftButton)

	ref = np.zeros(shape)
	ref[0, 0] = 5
	assert np.allclose(ref, w.visualization, atol=0)


##################################################
def test_generate_stress(make_napari_viewer, patched_napari_viewer, qtbot, capsys, monkeypatch, fake_qfiledialog, fake_napari_layers):
	"""Test basique de création du widget."""
	viewer = make_napari_viewer()  # .Créer un viewer à l'aide de la fixture.
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
	pt = PALMTracer()
	w = ViewerHRWidget(viewer, pt)  # Créer notre widget, en passant par le viewer.

	fake_napari_layers(viewer)
	n_p, n_x, n_y = 8, 8, 4

	# Chargement d'une pile
	fake_qfiledialog(FileList, f"{INPUT_DIR / 'stack.tif'}")
	qtbot.mouseClick(w._btn_add_stack, Qt.MouseButton.LeftButton)
	w._pt.process()  # Process Vide pour créer le dossier et un setting de base
	w._pt._stack = np.zeros((n_p, n_y, n_x))
	w._spn_upscale.value = 2
	upscale = w._spn_upscale.value
	shape = (n_y * upscale, n_x * upscale)

	# Bille qui part en diagonale du haut à droite vers le bas à gauche
	bead_x, bead_y = np.linspace(n_x - 0.5, 0, n_p, dtype=np.float32), np.linspace(0, n_y - 0.5, n_p, dtype=np.float32)

	beads = pd.DataFrame({"Bead":  np.ones(n_p, dtype=np.int32),
						  "Plane": np.arange(1, n_p + 1, dtype=np.int32),
						  "X":     bead_x,
						  "Y":     bead_y,
						  "Z":     np.zeros(n_p, dtype=np.float32)})

	loc = pd.DataFrame({"Plane":                np.arange(1, n_p + 1, dtype=np.int32),
						"X":                    np.full(n_p, n_x / 2.0, dtype=np.float32),
						"Y":                    np.full(n_p, n_y / 2.0, dtype=np.float32),
						"Z":                    np.zeros(n_p, dtype=np.float32),
						"Integrated Intensity": np.full(n_p, 1, dtype=np.float32),
						"Sigma X":              np.ones(n_p, dtype=np.float32),
						"Sigma Y":              np.ones(n_p, dtype=np.float32),
						"Theta":                np.zeros(n_p, dtype=np.float32)})

	w._pt.df["bds"], w._pt.df["loc"] = beads.copy(), loc.copy()

	# Génération fixe (n_beads fois sur la position centrale)
	w._generate()
	ref = np.zeros(shape)
	ref[n_y, n_x] = n_p
	assert np.allclose(ref, w.visualization)

	# Génération fixe de la bille (n_beads fois sur la position [1, 1] * upscale)
	w._pt.df["loc"].loc[:, ["X", "Y"]] = w._pt.df["bds"].loc[:, ["X", "Y"]].to_numpy()
	w._chk_beads_remove.value = False
	w._generate()
	ref = np.zeros(shape)
	ref[0, 15] = ref[1, 13] = ref[2, 11] = ref[3, 9] = ref[4, 6] = ref[5, 4] = ref[6, 2] = ref[7, 0] = 1
	assert np.allclose(ref, w.visualization)

	# Génération Drift corrigé des mêmes données que la bille, donc le premier point sera compté 8 fois.
	w._chk_drift_correction.value = True
	w._generate()
	ref = np.zeros(shape)
	ref[np.round(bead_y[0] * upscale).astype(int), np.round(bead_x[0] * upscale).astype(int)] = n_p
	assert np.allclose(ref, w.visualization)

	# Génération Drift corrigé, mais la localisation était fixe
	# (donc elle va bouger vers le haut à droite, elle remonte la diagonale et une partie sera hors champs (départ au centre)
	w._pt.df["bds"], w._pt.df["loc"] = beads.copy(), loc.copy()
	w._generate()
	ref = np.zeros(shape)
	ref[4, 8] = ref[3, 10] = ref[2, 12] = ref[1, 14] = 1  # les autres points hors champs continues (0,16) (-1, 18)...
	assert np.allclose(ref, w.visualization)

	# Seconde bille qui descend comme la précédente, mais ne va pas vers la gauche donc la pente initiale sera divisé par 2.
	beads2 = pd.DataFrame({"Bead":  np.full(n_p, 2, dtype=np.int32),
						   "Plane": np.arange(1, n_p + 1, dtype=np.int32),
						   "X":     np.zeros_like(bead_x, dtype=np.float32),
						   "Y":     bead_y,
						   "Z":     np.zeros(n_p, dtype=np.float32)})

	w._pt.df["bds"] = pd.concat([beads, beads2], ignore_index=True)
	w._generate()
	ref = np.zeros(shape)
	ref[4, 8] = ref[3, 9] = ref[2, 10] = ref[1, 11] = ref[0, 12] = 1  # les autres points hors champs continues (-1,13) (-2, 14)...
	assert np.allclose(ref, w.visualization)

	# On ajoute nos 2 billes à la localisation et on enlève le drift, tout doit être affiché
	w._chk_drift_correction.value = False
	size = 3 * n_p
	loc2 = pd.DataFrame({"Plane":                np.tile(np.arange(1, n_p + 1, dtype=np.int32), 3),
						 "X":                    np.full(size, n_x / 2.0, dtype=np.float32),
						 "Y":                    np.full(size, n_y / 2.0, dtype=np.float32),
						 "Z":                    np.zeros(size, dtype=np.float32),
						 "Integrated Intensity": np.full(size, 1, dtype=np.float32),
						 "Sigma X":              np.ones(size, dtype=np.float32),
						 "Sigma Y":              np.ones(size, dtype=np.float32),
						 "Theta":                np.zeros(size, dtype=np.float32)})
	loc2.loc[n_p:, ["X", "Y"]] = w._pt.df["bds"].loc[:, ["X", "Y"]].to_numpy()

	w._pt.df["loc"] = loc2.copy()
	w._generate()
	ref = np.zeros(shape)
	ref[0, 15] = ref[1, 13] = ref[2, 11] = ref[3, 9] = ref[4, 6] = ref[5, 4] = ref[6, 2] = ref[7, 0] = 1  # Bille originale
	ref[n_y, n_x] += n_p  # Localization statique
	ref[:, 0] += 1  # Bille Verticale
	assert np.allclose(ref, w.visualization)

	# On supprime nos 2 billes (mais on va conserver notre localisation
	w._chk_beads_remove.value = True
	w._generate()
	ref = np.zeros(shape)
	ref[n_y, n_x] += n_p  # Localization statique
	assert np.allclose(ref, w.visualization)

	# Bille Random....
	w._chk_beads_remove.value = False
	w._chk_drift_correction.value = True
	w._pt.df["bds"], w._pt.df["loc"] = beads.copy(), loc.copy()
	w._pt.df["bds"]["X"] = np.array([5.095, 3.755, 5.434, 4.789, 2.376, 5.902, 5.044, 5.144], dtype=np.float32)  # Random autour du centre
	w._pt.df["bds"]["Y"] = np.array([1.256, 1.900, 1.741, 2.853, 2.287, 2.645, 1.886, 1.454], dtype=np.float32)  # Random autour du centre
	w._generate()
	ref = np.zeros(shape)
	# Position au centre puis résultat du random dans tous les sens ATTENTION LE DRIFT EST LISSÉ.
	ref[4, 8] = ref[3, 9] = ref[2, 11] = ref[2, 13] = ref[2, 14] = ref[3, 15] = 1
	assert np.allclose(ref, w.visualization)

	# Correction sur la position de la bille avec lissage...
	w._pt.df["loc"].loc[:, ["X", "Y"]] = w._pt.df["bds"].loc[:, ["X", "Y"]].to_numpy()
	w._generate()
	ref = np.zeros(shape)
	# Position de la bille random corrigé ATTENTION LE DRIFT EST LISSÉ, ce n'est donc pas un point unique.
	ref[3, 9] = ref[3, 10] = ref[2, 11] = ref[2, 14] = ref[3, 14] = 1
	assert np.allclose(ref, w.visualization)

	# Correction sur la position de la bille sans lissage...
	w._chk_drift_smooth.value = False
	w._generate()
	ref = np.zeros(shape)
	# Position de la bille random corrigé et non lissé.
	ref[3, 10] = n_p
	assert np.allclose(ref, w.visualization)
