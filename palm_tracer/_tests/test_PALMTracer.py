"""
Teste l'orchestration complète des traitements par la classe :class:`PALMTracer`.

.. note:: Certaines vérifications du journal portent uniquement sur le nombre de lignes, car chaque traitement en produit au moins quinze.
"""

from datetime import datetime, timedelta
from itertools import count
from typing import Literal

import pytest

from palm_tracer._tests.Utils import *
from palm_tracer.Processing import Parsing
from palm_tracer.Settings.Groups.Graph import DATA_SRC
from palm_tracer.Settings.Types import Combo
from palm_tracer.Tools import FileIO


##################################################
@pytest.fixture
def pt():
	"""fixture interne."""
	obj = PALMTracer()
	yield obj
	try: obj._logger.close()
	except Exception: pass


##################################################
@pytest.fixture
def sequential_timestamps(monkeypatch):
	"""Fournit un timestamp croissant par appel pour tester la réutilisation sans attente réelle."""
	start = datetime(2026, 1, 2)
	seconds = count()

	def next_timestamp(with_hour: bool = True) -> str:
		"""
		Avance l'horodatage simulé d'une seconde.

		:param with_hour: Inclut l'heure dans le nom de fichier.
		:return: Horodatage déterministe au format utilisé par le pipeline.
		"""
		current = start + timedelta(seconds=next(seconds))
		return current.strftime("%Y%m%d_%H%M%S" if with_hour else "%Y%m%d")

	monkeypatch.setattr(FileIO, "get_timestamp_for_files", next_timestamp)


##################################################
def check_output(folder: Path, csv: Optional[list[int]] = None, log: Optional[list[int]] = None, json: Optional[list[int]] = None,
				 tif: Optional[list[int]] = None, png: Optional[list[int]] = None, html: Optional[list[int]] = None, clean: bool = True):
	"""Vérifie si la sortie correspond à ce qui est attendu."""
	if not folder.is_dir(): pytest.fail("Dossier invalide.")

	for ext, v in {"csv": csv, "log": log, "json": json, "tif": tif, "png": png, "html": html}.items():
		if v is None: continue
		r = f"*.{ext}"
		files = list(folder.glob(r))
		n = len(files)
		if len(v) == 1:
			if n != v[0]: pytest.fail(f"Il devrait y avoir {v[0]} fichier(s) '{r}', trouvé(s) : {n} ({files}).")
		elif not v[0] <= n <= v[1]: pytest.fail(f"Il devrait y avoir entre {v[0]} et {v[1]} fichiers '{r}', trouvé(s) : {n} ({files}).")

	if clean: shutil.rmtree(folder, ignore_errors=True)


##################################################
def check_capsys(capsys, n_lines: int, steps: list[int]):
	"""
	Vérifie dans le capsys les éléments activé ou non et la correspondance du nombre de lignes.

	:param capsys: Fixture Pytest capturant la sortie standard.
	:param n_lines: Nombre de lignes attendu dans la sortie.
	:param steps: Indices des lignes associées aux différentes étapes du pipeline.
	"""
	lines = get_lines_output(capsys)
	# for i in range(len(lines)): print(f"{i}: {lines[i]}")
	assert len(lines) == n_lines
	step_name = ["Localization", "Beads Extraction", "Tracking", "Blinking Reconnection", "Track Analysis", "Gallery generation",
				 "Graphical visualization", "High-resolution visualization"]
	for i in range(8): assert step_name[i] in lines[steps[i]]


##################################################
def add_fakeprocess(pt: PALMTracer, localisation: bool, tracking: bool):
	"""
	Simule l'exécution d'un process.

	:param pt: Objet de base.
	:param localisation: Défini si une localisation est simulé.
	:param tracking: Défini si un suivi est simulé.
	"""
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
	OUTPUT_FOLDER.mkdir(exist_ok=True, parents=True)
	timestamp = "20260101_000000"
	pt.settings.rois.set_size(256, 128)
	if localisation:
		src = INPUT_DIR / "ref" / "stack-localizations-103.6_True_4_1.0_0.0_7.csv"
		dst = OUTPUT_FOLDER / f"localizations-{timestamp}.csv"
		shutil.copy2(src, dst)
		pt.settings.localization.active = True
	if tracking:
		src = INPUT_DIR / "ref" / "stack-tracking-103.6_True_4_1.0_0.0_7-5.csv"
		dst = OUTPUT_FOLDER / f"tracking-{timestamp}.csv"
		shutil.copy2(src, dst)
		pt.settings.tracking.active = True
	FileIO.save_json(OUTPUT_FOLDER / f"settings-{timestamp}.json", pt.settings.to_compact_dict())


# ==================================================
# region Initialisation
# ==================================================
##################################################
def test_reset_result(pt):
	"""Vérifie le process sans fichiers en entrée."""

	pt.results["loc"] = pd.DataFrame([1, 1])
	pt.results["dft"] = pd.DataFrame([1, 2])
	pt.results["bds"] = pd.DataFrame([1, 3])
	pt.results["blk"] = pd.DataFrame([1, 4])
	pt.results["trc"] = pd.DataFrame([1, 5])
	pt.results["MSD"] = pd.DataFrame([1, 6])
	pt.results["InD"] = pd.DataFrame([1, 7])
	pt.results["Fit"] = pd.DataFrame([1, 8])
	pt.results["f_loc"] = pd.DataFrame([1, 9])
	pt.results["f_blk"] = pd.DataFrame([1, 10])
	pt.results["f_trc"] = pd.DataFrame([1, 11])
	pt.results["f_MSD"] = pd.DataFrame([1, 12])
	pt.results["f_InD"] = pd.DataFrame([1, 13])
	pt.results["f_Fit"] = pd.DataFrame([1, 14])

	pt.results.reset()
	for key in pt.results:
		assert pt.results[key].empty, "Le Dataframe devrait être vide."


##################################################
def test_clean_ui(monkeypatch, pt):
	"""Vérifie la délégation du nettoyage des interfaces."""
	results_names: list[str] = []
	settings_names: list[str] = []
	monkeypatch.setattr(pt.results, "clean_ui", results_names.append)
	monkeypatch.setattr(pt.settings, "clean_ui", settings_names.append)

	pt.clean_ui("viewer")

	assert results_names == ["viewer"]
	assert settings_names == ["viewer"]


# ==================================================
# endregion Initialisation
# ==================================================

# ==================================================
# region Accesseurs
# ==================================================
##################################################
def test_getter_localization(pt):
	"""Vérifie le getter de la localisation."""
	res = pt.results.localizations
	assert res.empty, "Le Dataframe devrait être vide."
	ref1 = pd.DataFrame([1, 2])
	ref2 = pd.DataFrame([3, 4])
	ref3 = pd.DataFrame([5, 6])
	pt.results["f_loc"] = ref1
	res = pt.results.localizations
	assert res.equals(ref1), f"Résultat incorrect.\nAttendu : {ref1}\tObtenu : {res}"
	pt.results["dft"] = ref2
	res = pt.results.localizations
	assert res.equals(ref2), f"Résultat incorrect.\nAttendu : {ref2}\tObtenu : {res}"
	pt.results["f_dft"] = ref3
	res = pt.results.localizations
	assert res.equals(ref3), f"Résultat incorrect.\nAttendu : {ref3}\tObtenu : {res}"
	pt.reset_filtered()
	res = pt.results.localizations
	assert res.equals(ref2), f"Résultat incorrect.\nAttendu : {ref2}\tObtenu : {res}"


##################################################
def test_getter_beads(pt):
	"""Vérifie le getter de la localisation."""
	res = pt.results.beads
	assert res.empty, "Le Dataframe devrait être vide."
	ref1 = pd.DataFrame([1, 2])
	pt.results["bds"] = ref1
	res = pt.results.beads
	assert res.equals(ref1), f"Résultat incorrect.\nAttendu : {ref1}\tObtenu : {res}"


##################################################
def test_getter_tracks(pt):
	"""Vérifie le process sans fichiers en entrée."""
	res = pt.results.tracks
	assert res.empty, "Le Dataframe devrait être vide."
	ref1 = pd.DataFrame([1, 2])
	ref2 = pd.DataFrame([3, 4])
	ref3 = pd.DataFrame([5, 6])
	pt.results["f_trc"] = ref1
	res = pt.results.tracks
	assert res.equals(ref1), f"Résultat incorrect.\nAttendu : {ref1}\tObtenu : {res}"
	pt.results["blk"] = ref2
	res = pt.results.tracks
	assert res.equals(ref2), f"Résultat incorrect.\nAttendu : {ref2}\tObtenu : {res}"
	pt.results["f_blk"] = ref3
	res = pt.results.tracks
	assert res.equals(ref3), f"Résultat incorrect.\nAttendu : {ref3}\tObtenu : {res}"
	pt.reset_filtered()
	res = pt.results.tracks
	assert res.equals(ref2), f"Résultat incorrect.\nAttendu : {ref2}\tObtenu : {res}"


##################################################
def test_getter_track_analysis(pt):
	"""Vérifie le process sans fichiers en entrée."""
	df = pt.results.track_analysis
	assert df["MSD"].empty, "Le Dataframe devrait être vide."
	ref1 = pd.DataFrame([1, 2])
	pt.results["f_MSD"] = ref1
	df = pt.results.track_analysis
	assert df["MSD"].equals(ref1), "Le Dataframe devrait non vide."


##################################################
def test_getter_path(pt):
	"""Vérifie le process sans fichiers en entrée."""
	res = pt.path
	assert res == ""


##################################################
def test_getter_stack(pt):
	"""Vérifie le process sans fichiers en entrée."""
	res = pt.stack
	assert res is None


##################################################
def test_getter_suffix(pt):
	"""Vérifie le process sans fichiers en entrée."""
	res = pt.suffix
	assert res == ""


##################################################
@pytest.mark.parametrize("group_name", [pytest.param("HR", id="hr"), pytest.param("Filters", id="filters")])
def test_save_setting_group_missing_file(monkeypatch, pt, tmp_path, group_name: Literal["HR", "Filters"]):
	"""Ignore un fichier de paramètres supprimé après l'initialisation du traitement."""
	pt._path = str(tmp_path)
	pt._timestamp = "20260101_000000"
	settings_filename = pt._output_name("settings", "json")
	settings_filename.touch()
	settings_filename.unlink()
	monkeypatch.setattr(FileIO, "open_json", lambda _: pytest.fail("Le fichier absent ne doit pas être lu."))
	monkeypatch.setattr(FileIO, "save_json", lambda *_: pytest.fail("Le fichier absent ne doit pas être recréé."))

	pt.save_setting_group(group_name)

	assert not settings_filename.exists()


# ==================================================
# endregion Accesseurs
# ==================================================

# ==================================================
# region Traitements
# ==================================================
##################################################
def test_load_bad_dll(capsys, pt):
	"""Vérifie le process avec tous les éléments à False et aucun fichier chargeable."""
	pt.palm._dll = None
	pt.load("")
	lines = get_lines_output(capsys)
	assert "Process not completed due to missing DLLs." in lines[0]


##################################################
def test_load_nothing(capsys, pt):
	"""Vérifie le chargement avec fichier, mais sans settings."""
	pt.load("bad path")
	lines = get_lines_output(capsys)
	assert "No valid settings file to load." in lines[0]


##################################################
def test_load(capsys, pt):
	"""Vérifie le chargement avec fichier, mais sans settings."""
	clean_output()

	# Process initial
	add_basic_file(pt)
	pt.settings.localization.active = True
	pt.process()
	assert len(pt.results["loc"]) == 455
	check_capsys(capsys, 16, [5, 7, 8, 9, 10, 11, 12, 13])
	# Chargement
	pt.load()

	assert not pt.results["loc"].empty, "Le Dataframe de localization ne devrait pas être vide"
	assert pt.results["f_loc"].empty, "Le Dataframe de localizations filtré devrait être vide."

	lines = get_lines_output(capsys)
	assert len(lines) == 18
	assert "File 'localizations' loaded successfully." in lines[2]
	assert "File 'localizations_filtered' not found." in lines[3]
	assert "File 'localizations_corrected' not found." in lines[4]
	assert "File 'localizations_corrected_filtered' not found." in lines[5]
	assert "File 'beads' not found." in lines[6]
	assert "File 'tracking' not found." in lines[7]
	assert "File 'tracking_filtered' not found." in lines[8]
	assert "File 'tracking_reconnected' not found." in lines[9]
	assert "File 'tracking_reconnected_filtered' not found." in lines[10]
	assert "File 'tracking_MSD' not found." in lines[11]
	assert "File 'tracking_MSD_filtered' not found." in lines[12]
	assert "File 'tracking_InstantD' not found." in lines[13]
	assert "File 'tracking_InstantD_filtered' not found." in lines[14]
	assert "File 'tracking_Fit' not found." in lines[15]
	assert "File 'tracking_Fit_filtered' not found." in lines[16]
	assert "Stack loaded successfully (size: (10, 128, 256))." in lines[17]

	# Un fichier méta + un localization
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1])

	# Simulation d'un chargement déjà en cours
	pt._loading = True
	pt.load()
	lines = get_lines_output(capsys)
	assert len(lines) == 0


##################################################
def test_process_no_input(capsys, pt):
	"""Vérifie le process sans fichiers en entrée."""
	clean_output()
	pt.process()
	assert pt.results["loc"].empty, "Le Dataframe de localization ne devrait pas être vide"
	lines = get_lines_output(capsys)
	assert "No files." in lines[0]


##################################################
def test_process_nothing(capsys, pt):
	"""Vérifie le process avec tous les éléments à False et aucun fichier chargeable."""
	clean_output()

	add_basic_file(pt)
	pt.process()
	assert pt.results["loc"].empty, "Le Dataframe de localization devrait être vide"
	check_capsys(capsys, 15, [5, 6, 7, 8, 9, 10, 11, 12])
	check_output(OUTPUT_FOLDER, csv=[1], log=[1], json=[1])

	# Test d'une visualisation sans données.
	pt.settings.gallery.active = True
	pt.settings.hr.active = True
	pt.settings.graph.active = True
	pt.process()  # Test d'une visualisation sans données.
	assert pt.results["loc"].empty, "Le Dataframe de localization devrait être vide"
	check_capsys(capsys, 18, [5, 6, 7, 8, 9, 10, 12, 14])
	check_output(OUTPUT_FOLDER, csv=[1], log=[1], json=[1])

	# Test d'une analyse des trajectoires sans données.
	pt.settings.gallery.active = False
	pt.settings.graph.active = False
	pt.settings.hr.active = False
	pt.settings.track_analysis.active = True
	pt.process()
	assert pt.results["loc"].empty, "Le Dataframe de localization devrait être vide"
	check_capsys(capsys, 16, [5, 6, 7, 8, 9, 11, 12, 13])
	check_output(OUTPUT_FOLDER, csv=[1], log=[1], json=[1])

	# Test d'un calcul de reconnexion de trajectoires sans données.
	pt.settings.track_analysis.active = False
	pt.settings.blinking.active = True
	pt.process()
	assert pt.results["loc"].empty, "Le Dataframe de localization devrait être vide"
	check_capsys(capsys, 16, [5, 6, 7, 8, 10, 11, 12, 13])
	check_output(OUTPUT_FOLDER, csv=[1], log=[1], json=[1])

	# Test d'une analyse des trajectoires sans données.
	pt.settings.blinking.active = False
	pt.settings.tracking.active = True
	pt.process()
	assert pt.results["loc"].empty, "Le Dataframe de localization devrait être vide"
	check_capsys(capsys, 16, [5, 6, 7, 9, 10, 11, 12, 13])
	check_output(OUTPUT_FOLDER, csv=[1], log=[1], json=[1])

	# Test d'un calcul de correction de drift sans données.
	pt.settings.tracking.active = False
	pt.settings.beads.active = True
	pt.process()
	assert pt.results["loc"].empty, "Le Dataframe de localization devrait être vide"
	check_capsys(capsys, 16, [5, 6, 8, 9, 10, 11, 12, 13])
	check_output(OUTPUT_FOLDER, csv=[1], log=[1], json=[1])


##################################################
def test_process_bad_dll(capsys, pt):
	"""Vérifie le process avec tous les éléments à False et aucun fichier chargeable."""
	pt.palm._dll = None
	pt.process()

	lines = get_lines_output(capsys)
	assert "Process not completed due to missing DLLs." in lines[0]


##################################################
def test_process_multiple_stack(capsys, pt):
	"""Vérifie le process avec plusieurs piles."""
	clean_output()

	add_basic_file(pt, [f"{INPUT_DIR}/stack.tif", f"{INPUT_DIR}/stack_quadrant.tif"])
	pt.settings.batch["Mode"].value = 1
	pt.process()

	check_output(OUTPUT_FOLDER, csv=[1], log=[1], json=[1])
	check_output(OUTPUT_FOLDER_2, csv=[1], log=[1], json=[1])
	# (2*21 lignes dans le cas d'aucun process)
	check_capsys(capsys, 30, [5, 6, 7, 8, 9, 10, 11, 12])


##################################################
def test_process_localization(capsys, pt):
	"""Vérifie le process de localisation."""
	clean_output()

	add_basic_file(pt)
	pt.settings.localization.active = True
	pt.process()

	assert len(pt.results["loc"]) == 455
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1])
	check_capsys(capsys, 16, [5, 7, 8, 9, 10, 11, 12, 13])


##################################################
def test_process_localization_z(capsys, pt):
	"""Vérifie le process de localisation."""
	clean_output()

	add_basic_file(pt)
	pt.settings.localization.active = True
	pt.settings.localization["Fit"].value = 1
	s = pt.settings.localization["Gaussian Fit"]
	s["Mode"].value = 2
	s["Z"].value = True
	pt.process()  # Lancement, mais aucun fichier de model.

	assert len(pt.results["loc"]) == 455
	assert np.allclose(pt.results["loc"]["Z"].to_numpy(), 0)
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1])
	check_capsys(capsys, 17, [5, 8, 9, 10, 11, 12, 13, 14])

	s["Model"].value = str(REF_DIR / "astigmatism_3d_model.csv")
	pt.process()  # Lancement

	assert len(pt.results["loc"]) == 455
	assert not np.allclose(pt.results["loc"]["Z"].to_numpy(), 0)
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1])
	check_capsys(capsys, 16, [5, 7, 8, 9, 10, 11, 12, 13])


##################################################
def test_process_localization_spline_bad(capsys, pt):
	"""Vérifie le process de localisation."""
	clean_output()

	add_basic_file(pt)
	pt.settings.localization.active = True
	pt.settings.localization["Fit"].value = 2
	with pytest.raises(OSError) as exception_info: pt.process()
	assert exception_info.type == OSError, "L'erreur relevé n'est pas correcte."

	check_output(OUTPUT_FOLDER, csv=[1], log=[1], json=[1])  # Il va créer le meta mais pas le fichier de localization
	lines = get_lines_output(capsys)
	assert len(lines) == 6  # Arrêt après l'erreur


##################################################
def test_process_localization_spline(capsys, pt):
	"""Vérifie le process de localisation."""
	clean_output()

	add_basic_file(pt)
	pt.settings.localization.active = True
	pt.settings.localization["Fit"].value = 2
	pt.settings.localization["Spline Fit"]["File"].value = f"{INPUT_DIR}/calibration.mat"
	pt.process()

	assert len(pt.results["loc"]) == 455
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1])
	check_capsys(capsys, 16, [5, 7, 8, 9, 10, 11, 12, 13])


##################################################
def test_process_beads_extraction_no_beads(capsys, pt):
	"""Vérifie le process de l'extraction des billes."""
	clean_output()

	add_basic_file(pt)
	pt.settings.localization.active = True
	pt.settings.beads.active = True
	pt.process()

	assert len(pt.results["loc"]) == 455
	assert pt.results["bds"].empty
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1])
	check_capsys(capsys, 17, [5, 7, 9, 10, 11, 12, 13, 14])


##################################################
def test_process_plane_discontinuous(capsys, pt):
	"""Vérifie le process de l'extraction des billes."""
	clean_output()

	src = INPUT_DIR / "localizations.csv"
	pt.results["loc"] = pd.read_csv(src)
	pt.results["loc"].loc[1, "Plane"] = 5
	pt._beads_extraction()
	assert pt.results["bds"].empty
	lines = get_lines_output(capsys)
	assert "No beads found." in lines[0]


##################################################
def test_process_beads_extraction(capsys, pt):
	"""Vérifie le process de l'extraction des billes."""
	clean_output()

	add_basic_file(pt)
	OUTPUT_FOLDER.mkdir(exist_ok=True, parents=True)
	timestamp = FileIO.get_timestamp_for_files()
	src, dst = INPUT_DIR / "localizations.csv", OUTPUT_FOLDER / f"localizations-{timestamp}.csv"
	shutil.copy2(src, dst)
	pt.settings.localization.active = True
	FileIO.save_json(OUTPUT_FOLDER / f"settings-{timestamp}.json", pt.settings.to_compact_dict())

	pt.settings.beads.active = True
	pt.process()

	assert len(pt.results["bds"]) == 4  # 2 Billes sur 2 plans
	check_output(OUTPUT_FOLDER, csv=[3], log=[1], json=[1])
	check_capsys(capsys, 17, [5, 7, 9, 10, 11, 12, 13, 14])


##################################################
def test_process_tracking(capsys, pt):
	"""Vérifie le process de tracking."""
	clean_output()

	add_basic_file(pt)
	add_fakeprocess(pt, True, False)  # Ajout d'un fichier de localisations

	pt.settings.tracking.active = True
	pt.process()

	ref = pt.results.localizations
	ref = ref[ref["Integrated Intensity"] > 0]  # Suppression des éléments où la colonne "Integrated Intensity" est inférieure à 0 (l'ajustement a échoué).

	assert len(ref) == len(pt.results.tracks), "Nombre de points différents entre la localization et le tracking."
	check_output(OUTPUT_FOLDER, csv=[3], log=[1], json=[1])
	check_capsys(capsys, 17, [5, 7, 8, 10, 11, 12, 13, 14])


##################################################
def test_process_tracking_blinking(capsys, pt):
	"""Vérifie le process de tracking."""
	clean_output()

	add_basic_file(pt)
	add_fakeprocess(pt, False, True)  # Ajout d'un fichier de Tracking

	pt.settings.blinking.active = True
	pt.process()

	assert len(pt.results["trc"]) == len(pt.results["blk"]), "Nombre de points différents entre la reconnexion et le tracking."
	check_output(OUTPUT_FOLDER, csv=[3], log=[1], json=[1])
	check_capsys(capsys, 17, [5, 6, 7, 9, 11, 12, 13, 14])


##################################################
def test_process_track_analysis(capsys, pt, sequential_timestamps):
	"""Vérifie le process de tracking."""
	clean_output()

	add_basic_file(pt)
	add_fakeprocess(pt, False, True)  # Ajout d'un fichier de Tracking

	ta = pt.settings.track_analysis
	ta.active = True
	pt.process()

	# Aucun fichier Ajouté juste meta et le tracking copié
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1], clean=False)
	check_capsys(capsys, 17, [5, 6, 7, 9, 10, 12, 13, 14])

	ta["MSD"].value = True
	pt.process()
	assert len(pt.results["MSD"]) == 93  # Toutes les trajectoires sont éligibles au MSD
	assert len(pt.results["Fit"]) == 3  # Seules 3 trajectoires sont éligibles
	# Ajout de fichier MSD (ainsi qu'un fit minimal, un meta, un json et un log)
	check_output(OUTPUT_FOLDER, csv=[4], log=[1], json=[1], clean=False)
	check_capsys(capsys, 19, [5, 6, 7, 9, 10, 14, 15, 16])

	ta["MSD"].value = False
	ta["Instant Diffusion"].value = True
	ta["Fit"].value = 1
	pt.process()
	assert len(pt.results["MSD"]) == 0  # MSD désactivé, il est conservé
	assert len(pt.results["InD"]) == 3  # Seules 3 trajectoires sont éligibles
	assert len(pt.results["Fit"]) == 3  # Seules 3 trajectoires sont éligibles
	check_output(OUTPUT_FOLDER, csv=[6], log=[2], json=[2])  # Il a conservé le msd precedent mais à renommé le meta
	check_capsys(capsys, 18, [5, 6, 7, 9, 10, 13, 14, 15])


##################################################
def test_process_gallery(capsys, pt):
	"""Vérifie le process de visualization HR."""
	clean_output()

	add_basic_file(pt)
	add_fakeprocess(pt, True, False)  # Ajout d'un fichier de localisations

	pt.settings.gallery.active = True
	pt.process()

	# Dimension 270 (30 ROI / lignes(colonnes) * taille de ROI de 9) et 1 frame (30 * 30 = 900 / frame et environ 450 en entrée)
	res, ref = FileIO.open_tif(str(list(OUTPUT_FOLDER.glob("*.tif"))[0])).shape, (1, 270, 270)
	assert res == ref, f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1], tif=[1])
	check_capsys(capsys, 17, [5, 7, 8, 9, 10, 11, 13, 14])


##################################################
def test_process_visualization_graph(capsys, pt):
	"""Vérifie le process de visualization de graph."""
	clean_output()

	add_basic_file(pt)
	add_fakeprocess(pt, True, True)  # Ajout d'un fichier de localisations et de tracking

	pt.settings.graph.active = True
	pt.process()

	check_output(OUTPUT_FOLDER, csv=[3], log=[1], json=[1], html=[1])
	check_capsys(capsys, 18, [5, 7, 8, 10, 11, 12, 13, 15])


##################################################
def test_process_visualization_hr(capsys, pt, sequential_timestamps):
	"""Vérifie le process de visualization HR."""
	clean_output()

	add_basic_file(pt)
	add_fakeprocess(pt, True, True)  # Ajout d'un fichier de localisations et de tracking

	pt.settings.hr.active = True
	pt.settings.hr["Crop"].value = False
	pt.process()

	check_output(OUTPUT_FOLDER, csv=[3], log=[1], json=[1], png=[1], clean=False)
	check_capsys(capsys, 18, [5, 7, 8, 10, 11, 12, 13, 14])

	pt.settings.hr["Dimension"].value = 1  # Génération de Z-stack
	pt.process()

	check_output(OUTPUT_FOLDER, csv=[3], log=[2], json=[2], png=[1], tif=[1], clean=False)
	check_capsys(capsys, 18, [5, 7, 8, 10, 11, 12, 13, 14])

	pt.settings.hr["Dimension"].value = 2  # Génération de la rotation 3D
	pt.process()

	check_output(OUTPUT_FOLDER, csv=[3], log=[3], json=[3], png=[1], tif=[2])
	check_capsys(capsys, 18, [5, 7, 8, 10, 11, 12, 13, 14])


##################################################
def test_process_all(capsys, pt):
	"""Vérifie Basique pour le process complet."""
	clean_output()

	pt.settings.localization.active = True
	pt.settings.localization["Fit"].value = 1
	pt.settings.localization["Gaussian Fit"]["Mode"].value = 3
	pt.settings.beads.active = True
	pt.settings.tracking.active = True
	pt.settings.tracking["Max Distance"].value = 4
	pt.settings.blinking.active = True
	pt.settings.blinking["Max Duration"].value = 4
	pt.settings.track_analysis.active = True
	pt.settings.track_analysis["MSD"].value = True
	pt.settings.track_analysis["Instant Diffusion"].value = True
	pt.settings.track_analysis["Fit"].value = 1
	pt.settings.gallery.active = True
	pt.settings.graph.active = True
	pt.settings.hr.active = True
	add_basic_file(pt)
	pt.process()

	check_output(OUTPUT_FOLDER, csv=[7], log=[1], json=[1], tif=[1], png=[1], html=[1])
	check_capsys(capsys, 26, [5, 7, 9, 11, 13, 18, 20, 22])


##################################################
def test_get_astigmatism_model():
	"""Vérifie la récupération du modèle d'astigmatisme."""
	pt = PALMTracer()
	tmp_output = OUTPUT_DIR / "Model"
	shutil.rmtree(tmp_output, ignore_errors=True)
	tmp_output.mkdir(parents=True, exist_ok=True)
	model_file = "astigmatism_3d_model.csv"
	ref = pd.read_csv(REF_DIR / model_file, index_col=0)
	(tmp_output / model_file).unlink(missing_ok=True)
	(tmp_output.parent / model_file).unlink(missing_ok=True)

	pt._path = tmp_output

	model = pt._get_astigmatism_model(Path(""))  # Il ne va pas réussir, il n'a aucun fichier
	assert model.empty

	shutil.copy2(REF_DIR / model_file, tmp_output.parent / model_file)
	model = pt._get_astigmatism_model(Path(""))  # Il va réussir, dans le dernier dossier par défaut
	np.testing.assert_array_almost_equal(model.to_numpy(), ref.to_numpy())

	shutil.copy2(REF_DIR / model_file, tmp_output / model_file)
	model = pt._get_astigmatism_model(Path(""))  # Il va réussir, dans le premier dossier par défaut
	np.testing.assert_array_almost_equal(model.to_numpy(), ref.to_numpy())

	model = pt._get_astigmatism_model(REF_DIR / model_file)  # Il va réussir, dans le chemin donné
	np.testing.assert_array_almost_equal(model.to_numpy(), ref.to_numpy())


# ==================================================
# endregion Traitements
# ==================================================

# ==================================================
# region Filtrage
# ==================================================
##################################################
def test_reset_filtered(capsys, pt):
	"""Vérifie la suppréssion des tableaux filtrés."""

	pt.results["loc"] = pd.DataFrame([1, 1])
	pt.results["dft"] = pd.DataFrame([1, 2])
	pt.results["bds"] = pd.DataFrame([1, 3])
	pt.results["blk"] = pd.DataFrame([1, 4])
	pt.results["trc"] = pd.DataFrame([1, 5])
	pt.results["MSD"] = pd.DataFrame([1, 6])
	pt.results["InD"] = pd.DataFrame([1, 7])
	pt.results["Fit"] = pd.DataFrame([1, 8])
	pt.results["f_loc"] = pd.DataFrame([1, 9])
	pt.results["f_blk"] = pd.DataFrame([1, 10])
	pt.results["f_trc"] = pd.DataFrame([1, 11])
	pt.results["f_MSD"] = pd.DataFrame([1, 12])
	pt.results["f_InD"] = pd.DataFrame([1, 13])
	pt.results["f_Fit"] = pd.DataFrame([1, 14])

	pt.reset_filtered()
	for key in pt.results:
		if key.startswith("f_"): assert pt.results[key].empty, "Le Dataframe devrait être vide."
		else: assert not pt.results[key].empty, "Le Dataframe doit subsister."


##################################################
def test_reset_filtered_saves_only_filters(pt, tmp_path):
	"""Vérifie que Reset cible le traitement chargé et conserve les autres groupes."""
	pt._path = str(tmp_path)
	pt._timestamp = "20260101_000000"
	current = pt._output_name("settings", "json")
	newer = tmp_path / "settings-20260102_000000.json"
	initial = pt.settings.to_compact_dict()
	FileIO.save_json(current, initial)
	FileIO.save_json(newer, initial)

	pt.settings.filters["Plane"].active = True
	pt.settings.hr["Ratio"].value = 8
	pt.reset_filtered()

	assert FileIO.open_json(newer) == initial
	actual = FileIO.open_json(current)
	assert actual["PALM Tracer Settings"]["Filters"] == pt.settings.filters.to_compact_dict()
	assert actual["PALM Tracer Settings"]["HR"] == initial["PALM Tracer Settings"]["HR"]
	assert not pt.settings.filters["Plane"].active


##################################################
def test_update_filtered(capsys, pt):
	"""Vérifie la mise à jour des tableaux filtrés."""
	clean_output()
	pt.update_filtered()  # .			Tout est vide
	pt.settings.filters["Save"].value = True
	pt.update_filtered()  # .			Tout est vide, mais je demande à enregistrer

	add_basic_file(pt)
	add_fakeprocess(pt, True, False)  # Ajout d'un fichier de localisations et de tracking

	pt.process()
	pt.update_filtered()  # .			Maintenant, il va recalculer les filtres (il n'y en aura aucun de toute façon).
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1])  # Il n'a rien enregistré, car les filtres n'ont pas fait de changement.


##################################################
@pytest.mark.parametrize("key, filter_name", [
		pytest.param("loc", "Plane", id="localizations-plane"),
		pytest.param("trc", "Plane", id="tracks-plane"),
		pytest.param("trc", "Track", id="tracks-id")])
def test_update_button_does_not_accumulate_filters(qtbot, pt, key, filter_name):
	"""Vérifie que deux clics sur Update repartent des données originales lorsque le filtre est élargi."""
	filters = pt.settings.filters
	qtbot.addWidget(filters.get_ui("test").widget)
	pt.connect_filters_button("test")
	button = filters.buttons["test"]["update"]
	source = pd.DataFrame({"Plane": [1, 2, 3], "Track": [1, 2, 3], "X": [0.0, 1.0, 2.0], "Y": [0.0, 1.0, 2.0]})
	pt.results[key] = source.copy()
	selected_filter = filters[filter_name] if filter_name == "Plane" else filters.tracking[filter_name]
	selected_filter.active = True

	selected_filter.value = [1, 1] if filter_name == "Plane" else "1"
	button.click()
	pd.testing.assert_frame_equal(pt.results[f"f_{key}"], source.iloc[:1])

	# Le deuxième résultat reste partiel pour ne pas déclencher le repli vers le parent.
	selected_filter.value = [1, 2] if filter_name == "Plane" else "1-2"
	button.click()
	pd.testing.assert_frame_equal(pt.results[f"f_{key}"], source.iloc[:2])
	pd.testing.assert_frame_equal(pt.results[key], source)


##################################################
def test_update_filtered_saves_only_filters(pt, tmp_path):
	"""Vérifie qu'Update enregistre les filtres sans capturer les autres modifications."""
	pt._path = str(tmp_path)
	pt._timestamp = "20260102_000000"
	settings_file = pt._output_name("settings", "json")
	initial = pt.settings.to_compact_dict()
	FileIO.save_json(settings_file, initial)

	pt.settings.filters["Plane"].active = True
	pt.settings.hr["Ratio"].value = 8
	pt.settings.calibration["Pixel Size"].value = 0.32
	pt.update_filtered()

	actual = FileIO.open_json(settings_file)
	assert actual["PALM Tracer Settings"]["Filters"] == pt.settings.filters.to_compact_dict()
	assert actual["PALM Tracer Settings"]["HR"] == initial["PALM Tracer Settings"]["HR"]
	assert actual["PALM Tracer Settings"]["Calibration"] == initial["PALM Tracer Settings"]["Calibration"]


##################################################
def test_save_filtered(capsys, pt):
	"""Vérifie la mise à jour des tableaux filtrés."""
	clean_output()
	pt._path = OUTPUT_DIR
	pt.update_filtered()  # .				Tout est vide
	pt.settings.filters["Save"].value = True
	pt.update_filtered()  # .				Tout est vide, mais je demande à enregistrer

	add_basic_file(pt)
	add_fakeprocess(pt, True, False)  # .	Ajout d'un fichier de localisations et de tracking

	pt.results["loc"] = pd.read_csv(INPUT_DIR / "ref" / "stack-localizations-103.6_True_4_1.0_0.0_7.csv")
	pt.settings.filters["Plane"].active = True
	pt.settings.filters["Plane"].value = [2, 3]
	pt.update_filtered()  # .				Il va recalculer les filtres.
	check_output(OUTPUT_FOLDER, csv=[1])  # Il a enregistré la version filtrée.


##################################################
def test_connect_filters_button(qtbot, capsys, pt):
	"""Vérifie la connexion des boutons de filtrage."""
	pt.settings.get_ui("test")
	pt.connect_filters_button("test")


##################################################
def test_filter_localization(capsys, pt, sequential_timestamps):
	"""Vérifie le filtrage complet lors de l'exécution."""
	clean_output()

	add_basic_file(pt)
	add_fakeprocess(pt, True, False)  # .	Ajout d'un fichier de localisations et de tracking

	f = pt.settings.filters
	fl = f.localization
	f["Plane"].active = True
	f["Plane"].value = [1, 9]  # .			Suppression du dernier plan uniquement 411/451 : 40 suppression(s)
	fl["Intensity"].active = True
	fl["Intensity"].value = [100, 20000]  # 391/411 : 20 suppression(s)
	fl["Sigma X"].active = True
	fl["Sigma X"].value = [0, 10]  # .		Aucune suppression
	fl["Sigma Y"].active = True
	fl["Sigma Y"].value = [0, 10]  # .		Aucune suppression
	fl["Circularity"].active = True  # .	Aucune suppression
	fl["Theta"].active = True
	fl["Theta"].value = [-60, 60]  # .		346/391 : 45 suppression(s)
	fl["Z"].active = True  # .				Aucune suppression
	fl["MSE XY"].active = True
	fl["MSE XY"].value = [0.05, 10]  # .	345/366 : 1 suppression(s)
	pt.process()
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1], clean=False)  # Il n'a pas enregistré le résultat du filtre
	check_capsys(capsys, 17, [5, 8, 9, 10, 11, 12, 13, 14])

	pt.settings.filters["Save"].value = True
	pt.process()  # Second passage avec enregistrement
	check_output(OUTPUT_FOLDER, csv=[3], log=[1], json=[1])
	check_capsys(capsys, 18, [5, 9, 10, 11, 12, 13, 14, 15])


##################################################
def test_filter_track_analysis(capsys, pt, sequential_timestamps):
	"""Vérifie le filtrage complet lors de l'exécution."""
	clean_output()

	add_basic_file(pt)
	add_fakeprocess(pt, False, True)  # Ajout d'un fichier de tracking

	pt.settings.track_analysis.active = True
	pt.settings.track_analysis["MSD"].value = True
	pt.settings.track_analysis["Instant Diffusion"].value = True
	pt.settings.track_analysis["Fit"].value = 1
	pt.settings.track_analysis["Fit Length"].value = 2

	ft = pt.settings.filters.tracking
	ft["Length"].active = True
	ft["Length"].value = [3, 10000]
	ft["Instant D"].active = True
	ft["Instant D"].value = [0.01, 5]
	ft["D Coeff"].active = True
	ft["D Coeff"].value = [1, 5]
	ft["Speed"].active = True
	ft["Speed"].value = [-10, 10]
	ft["Alpha"].active = True
	ft["Confinement"].value = [-10, 10]
	pt.process()

	check_output(OUTPUT_FOLDER, csv=[5], log=[1], json=[1], clean=False)  # Il n'a pas enregistré le résultat du filtre
	check_capsys(capsys, 21, [5, 6, 7, 10, 11, 16, 17, 18])

	pt.settings.filters["Save"].value = True
	pt.process()
	# Vérification manuelle à l'heure actuelle
	assert len(pt.results.tracks) == 26, f"Il reste {len(pt.results.tracks)} points au lieu de 26 sur les trajectoires."
	assert len(pt.results.track_analysis["MSD"]) == 6, f"Il reste {len(pt.results.track_analysis['MSD'])} trajectoires au lieu de 14."

	check_output(OUTPUT_FOLDER, csv=[9], log=[1], json=[1], clean=False)  # Track + 2 analyses de trajectoires, leurs versions filtrées et le meta = 9
	check_capsys(capsys, 26, [5, 6, 7, 11, 12, 21, 22, 23])

	# Filtre massif plus rien à la sortie
	pt.settings.filters["Tracks"]["Length"].value = [42, 10000]
	pt.process()
	assert len(pt.results["f_trc"]) == 0, f"Il reste {len(pt.results.tracks)} points au lieu de 0 sur les trajectoires."
	assert len(pt.results["f_MSD"]) == 0, f"Il reste {len(pt.results.track_analysis['MSD'])} trajectoires au lieu de 0."
	check_output(OUTPUT_FOLDER, csv=[9], log=[2], json=[2])  # Il ne va pas réenregistrer les éléments filtrés
	check_capsys(capsys, 21, [5, 6, 7, 10, 11, 16, 17, 18])


# ==================================================
# endregion Filtrage
# ==================================================

# ==================================================
# region Visualisation
# ==================================================
# region Graph
##################################################
@pytest.mark.parametrize("mode, source_type, source", [
		pytest.param(mode, source_type, source, id=f"{mode_name}-{type_name}-{source}")
		for mode, mode_name in enumerate(("histogram", "scatter", "dual"))
		for source_type, type_name in enumerate(("localizations", "tracks"))
		for source in DATA_SRC["Localization" if source_type == 0 else "Tracking Scatter" if mode == 1 else "Tracking"]
		if mode != 2 or source not in DATA_SRC["No Dual"]])
def test_graph(mode, source_type, source):
	"""Construit une figure pour chaque source A de chaque domaine et mode, avec une source B fixe en Dual."""
	pt = get_fake_pt()
	# Les points et leurs analyses partagent les mêmes identifiants ; toutes les grandeurs d'ajustement sont disponibles.
	pt.results["f_blk"] = pd.DataFrame({"Track": [7, 7, 12, 12], "Plane": [1, 3, 2, 3], "Integrated Intensity": [10, 30, 20, 40]})
	pt.results["MSD"] = pd.DataFrame({"Track": [7, 12], "Step 1": [1.0, 3.0], "Step 2": [2.0, 4.0]})
	pt.results["InD"] = pd.DataFrame({"Track": [7, 12], "Window 1": [1.0, 3.0], "Window 2": [2.0, 4.0]})
	fit_columns = {name: [1.0, 2.0] for name in DATA_SRC["Tracking"] if name not in {"Length", "Length On", "Length Off", "MSD", "Instant D"}}
	pt.results["Fit"] = pd.DataFrame({"Track": [7, 12], **fit_columns})
	s = pt.settings.graph
	s["Mode"].value, s["Type"].value = mode, source_type
	source_a = cast(Combo, s["Source"])
	source_a.value = source_a.items.index(source)
	if mode == 2:
		source_b = cast(Combo, s["Source B"])
		source_b.value = source_b.items.index("X" if source_type == 0 else "Total Intensity")
	figure = pt.graph()
	# Instant D rassemble les fenêtres : une valeur par track en B ne peut pas être associée à ce vecteur.
	if mode == 2 and source_type == 1 and source == "Instant D":
		assert not figure.data
		assert figure.layout.annotations[0].text == "No valid data."
	else:
		assert figure.data
		assert figure.data[0].type == ("histogram", "scatter", "scattergl")[mode]
		assert len(figure.data[0].x) > 0
	assert source in figure.layout.title.text


##################################################
@pytest.mark.parametrize("log_scale", [pytest.param(False, id="linear"), pytest.param(True, id="logarithmic")])
def test_log_data(log_scale):
	"""Vérifie le logarithme et les valeurs non positives sans modifier le tableau reçu."""
	points = np.array([-1.0, 0.0, 0.1, 10.0, np.nan])
	original = points.copy()
	expected = [np.nan, np.nan, -1.0, 1.0, np.nan] if log_scale else points
	np.testing.assert_allclose(PALMTracer._log_data(points, log_scale), expected, equal_nan=True)
	np.testing.assert_array_equal(points, original)


##################################################
@pytest.mark.parametrize("missing_column", [pytest.param(False, id="paired-values"), pytest.param(True, id="missing-source")])
def test_get_graph_data_dual_localizations(pt, missing_column):
	"""Vérifie l'ordre des sources et les métadonnées du Dual des localisations."""
	pt.results["loc"] = pd.DataFrame({"Sigma X": [1.0, 2.0, 3.0], "Sigma Y": [4.0, 5.0, 6.0]})
	if missing_column: pt.results["loc"].drop(columns="Sigma X", inplace=True)
	s = pt.settings.graph
	s["Mode"].value = 2
	s["Source"].value = cast(Combo, s["Source"]).items.index("Sigma X")
	s["Source B"].value = cast(Combo, s["Source B"]).items.index("Sigma Y")
	graph_data = pt._get_graph_data()
	assert graph_data["title"] == "Localizations Sigma X / Sigma Y"
	assert graph_data["xlabel"] == "Sigma X"
	assert graph_data["ylabel"] == "Sigma Y"
	np.testing.assert_array_equal(graph_data["data"], [] if missing_column else [[1, 2, 3], [4, 5, 6]])


##################################################
@pytest.mark.parametrize("source, expected", [
		pytest.param("Length", [[7.0, 10.0], [11.0, 20.0]], id="total-duration"),
		pytest.param("Length On", [[2.5, 10.0], [1.0, 20.0]], id="present-duration"),
		pytest.param("Length Off", [[2.0, 10.0], [4.0, 20.0]], id="absent-duration")])
def test_get_graph_data_dual_tracks(source, expected):
	"""Vérifie la mise en correspondance des données par identifiant de trajectoire."""
	pt = get_fake_pt()
	pt.results["f_blk"] = pd.DataFrame({"Track": [1, 1, 1, 1, 1, 2, 2, 2, 3, 3], "Plane": [1, 2, 5, 6, 7, 10, 12, 20, 4, 5], })
	pt.results["Fit"] = pd.DataFrame({"Track": [2, 1, 4], "MSE(0)": [20.0, 10.0, 40.0]})

	s = pt.settings.graph
	s["Type"].value = 1
	s["Mode"].value = 2
	source_a = cast(Combo, s["Source"])
	source_b = cast(Combo, s["Source B"])
	source_b.value = source_b.items.index("MSE(0)")

	source_a.value = source_a.items.index(source)
	graph_data = pt._get_graph_data()
	assert graph_data["title"] == f"Tracks {source} / MSE(0)"
	assert graph_data["xlabel"] == source
	assert graph_data["ylabel"] == "MSE(0)"
	np.testing.assert_array_equal(graph_data["data"], np.asarray(expected).T)


##################################################
@pytest.mark.parametrize("source_b", [pytest.param("Instant D", id="incompatible-dimensions"), pytest.param("MSE(0)", id="no-common-track")])
def test_get_graph_data_dual_tracks_empty(pt, source_b):
	"""Renvoie des données vides quand les sources ne peuvent pas être associées."""
	pt.results["trc"] = pd.DataFrame({"Track": [1, 1], "Plane": [1, 2]})
	pt.results["Fit"] = pd.DataFrame({"Track": [2], "MSE(0)": [1.0]})
	pt.results["InD"] = pd.DataFrame({"Track": [1], "Window 1": [1.0]})
	s = pt.settings.graph
	s["Type"].value, s["Mode"].value = 1, 2
	s["Source"].value = cast(Combo, s["Source"]).items.index("Length")
	s["Source B"].value = cast(Combo, s["Source B"]).items.index(source_b)
	assert pt._get_graph_data()["data"].size == 0


##################################################
@pytest.mark.parametrize("source_type, mode, method, expected_args", [
		pytest.param(0, 0, "_get_localization_graph_data", ("X", 0, True), id="localizations-histogram"),
		pytest.param(0, 1, "_get_localization_graph_data", ("X", 1, True), id="localizations-scatter"),
		pytest.param(1, 0, "_get_track_graph_data", ("X", True, False), id="tracks-histogram"),
		pytest.param(1, 1, "_get_track_scatter_data", ("X", True), id="tracks-scatter"),
		pytest.param(1, 2, "_get_track_graph_data", ("X", True, True), id="tracks-dual")])
def test_get_graph_data_from_src(pt, monkeypatch, source_type, mode, method, expected_args):
	"""Vérifie uniquement l'aiguillage et la transmission des paramètres, sans refaire les calculs des sources."""
	graph_data = {"data": np.array([1.0]), "title": "Prepared data"}
	calls = []

	def prepare(*args):
		"""Conserve les paramètres reçus et renvoie le dictionnaire préparé."""
		calls.append(args)
		return graph_data

	monkeypatch.setattr(pt, method, prepare)
	pt.settings.graph["Mode"].value = mode
	assert pt._get_graph_data_from_src(source_type, "X", True, mode == 2) is graph_data
	assert calls == [expected_args]


##################################################
@pytest.mark.parametrize("mode", [pytest.param(0, id="histogram"), pytest.param(1, id="scatter"), pytest.param(2, id="dual")])
@pytest.mark.parametrize("log_scale", [pytest.param(False, id="linear"), pytest.param(True, id="logarithmic")])
def test_get_localization_graph_data(pt, mode, log_scale):
	"""Vérifie les valeurs individuelles, les moyennes avant logarithme et les plans vides."""
	pt.results["loc"] = pd.DataFrame({"Plane": [3, 1, 1, 3], "Integrated Intensity": [0.0, 1.0, 9.0, np.inf]})
	graph_data = pt._get_localization_graph_data("Integrated Intensity", mode, log_scale)
	if mode == 1: expected = [[1, 2, 3], [np.log10(5), np.nan, np.nan] if log_scale else [5, np.nan, 0]]
	else: expected = [np.nan, 0, np.log10(9), np.inf] if log_scale else [0, 1, 9, np.inf]
	np.testing.assert_allclose(graph_data["data"], expected, equal_nan=True)
	assert ("fit_limit" in graph_data) == (mode == 0 and not log_scale)
	if "fit_limit" in graph_data: assert graph_data["fit_limit"] == -1.0
	if mode == 1:
		assert graph_data["xlabel"] == "Plane"
		assert graph_data["ylabel"] == "Integrated Intensity"
	assert graph_data["title"] == "Localizations Integrated Intensity" + (" Mean per Plane" if mode == 1 else "")


##################################################
@pytest.mark.parametrize("mode", [pytest.param(0, id="histogram"), pytest.param(1, id="scatter")])
def test_get_localization_graph_data_count(pt, mode):
	"""Vérifie les comptes par plan, y compris zéro sur un plan sans localisation."""
	pt.results["loc"] = pd.DataFrame({"Plane": [3, 1, 1, 3]})
	graph_data = pt._get_localization_graph_data("Count per Plane", mode, False)
	np.testing.assert_array_equal(graph_data["data"], [[1, 2, 3], [2, 0, 2]])
	assert graph_data["title"] == "Localizations Count per Plane"


##################################################
@pytest.mark.parametrize("mode", [pytest.param(0, id="histogram"), pytest.param(1, id="scatter")])
def test_get_localization_graph_data_empty(pt, mode):
	"""Accepte des résultats de localisation vides."""
	graph_data = pt._get_localization_graph_data("X", mode, False)
	assert graph_data["data"].shape == (0,)
	assert graph_data["title"] == "Localizations X"


##################################################
def test_get_localization_graph_data_missing_column(pt):
	"""Renvoie des données vides si la grandeur demandée n'existe pas."""
	pt.results["loc"] = pd.DataFrame({"Plane": [1], "X": [2.0]})
	graph_data = pt._get_localization_graph_data("Unknown", 0, False)
	assert graph_data["data"].shape == (0,)
	assert graph_data["title"] == "Localizations Unknown"


##################################################
@pytest.mark.parametrize("source, key, prefix, xlabel, ylabel", [
		pytest.param("MSD", "MSD", "Step", "Step (planes)", "MSD (μm²)", id="msd"),
		pytest.param("Instant D", "InD", "Window", "Window", "Instant D (μm²/s)", id="instant-diffusion")])
@pytest.mark.parametrize("mean", [pytest.param(False, id="per-track"), pytest.param(True, id="mean")])
@pytest.mark.parametrize("log_scale", [pytest.param(False, id="linear"), pytest.param(True, id="logarithmic")])
def test_get_track_scatter_data(pt, source, key, prefix, xlabel, ylabel, mean, log_scale):
	"""Vérifie l'ordre des steps/fenêtres, les absences et la moyenne avant logarithme."""
	third_value = 6.0 if source == "MSD" else 1e-5
	pt.results[key] = pd.DataFrame({"Track":       [12, 7], f"{prefix} 3": [third_value, -1.0], f"{prefix} 1": [0.0, 2.0],
									f"{prefix} 4": [np.inf, np.nan], f"{prefix} 0": [99, 99], "Unrelated": [99, 99]})
	src = source + (" Mean" if mean else "")
	graph_data = pt._get_track_scatter_data(src, log_scale)
	values = np.array([1, np.nan, third_value, np.nan] if mean else [[0, np.nan, third_value, np.nan], [2, np.nan, np.nan, np.nan]])
	if log_scale:
		with np.errstate(divide="ignore", invalid="ignore"): values = np.where(values > 0, np.log10(values), np.nan)
	expected = np.vstack(([1, 2, 3, 4], values)) if mean else np.stack((np.tile([1, 2, 3, 4], (2, 1)), values), axis=1)
	np.testing.assert_allclose(graph_data["data"], expected, equal_nan=True)
	assert graph_data["title"] == f"Tracks {src}"
	assert graph_data["xlabel"] == xlabel
	assert graph_data["ylabel"] == (f"log10({ylabel})" if log_scale else ylabel)
	assert graph_data.get("names") == (None if mean else ["Track 12", "Track 7"])


##################################################
@pytest.mark.parametrize("source, method, expected_args, expected_names, ylabel", [
		pytest.param("Integrated Intensity", "_get_track_intensity_data", (False,), ["Track 12", "Track 7"], "Integrated Intensity", id="intensity"),
		pytest.param("Integrated Intensity Mean", "_get_track_intensity_data", (True,), None, "Integrated Intensity", id="mean-intensity"),
		pytest.param("Track Count", "_get_track_count_data", (), ["In Progress", "Present", "Absent"], "Track Count", id="count")])
@pytest.mark.parametrize("log_scale", [pytest.param(False, id="linear"), pytest.param(True, id="logarithmic")])
def test_get_track_scatter_data_metadata(pt, monkeypatch, source, method, expected_args, expected_names, ylabel, log_scale):
	"""Vérifie les libellés, les noms et la délégation aux calculs d'intensité ou de comptage."""
	pt.results["trc"] = pd.DataFrame({"Track": [12, 7, 12]})
	data = np.array([1.0])
	calls = []

	def prepare(*args):
		"""Conserve les paramètres transmis au calcul des données."""
		calls.append(args)
		return data

	monkeypatch.setattr(pt, method, prepare)
	graph_data = pt._get_track_scatter_data(source, log_scale)
	assert graph_data["data"] is data
	assert calls == [expected_args + (log_scale,)]
	assert graph_data["title"] == f"Tracks {source}"
	assert graph_data["xlabel"] == "Plane"
	assert graph_data["ylabel"] == (f"log10({ylabel})" if log_scale else ylabel)
	assert graph_data.get("names") == expected_names


##################################################
@pytest.mark.parametrize("source", [
		pytest.param("MSD", id="msd"), pytest.param("Instant D Mean", id="mean-diffusion"),
		pytest.param("Integrated Intensity", id="intensity"), pytest.param("Track Count", id="count")])
def test_get_track_scatter_data_empty(pt, source):
	"""Accepte les résultats de tracking ou les analyses absents avec des données vides."""
	graph_data = pt._get_track_scatter_data(source, False)
	assert graph_data["data"].size == 0
	assert graph_data["title"] == f"Tracks {source}"


##################################################
@pytest.mark.parametrize("source, columns", [
		pytest.param("MSD", {"Track": [1], "Unrelated": [2]}, id="missing-step"),
		pytest.param("Instant D", {"Window 1": [2]}, id="missing-track-id"),
		pytest.param("Integrated Intensity", {"Track": [1], "Plane": [1]}, id="missing-intensity"),
		pytest.param("Track Count", {"Track": [1]}, id="missing-plane")])
def test_get_track_scatter_data_missing_columns(pt, source, columns):
	"""Renvoie des données vides si les colonnes nécessaires ne sont pas disponibles."""
	key = "MSD" if source == "MSD" else "InD" if source == "Instant D" else "trc"
	pt.results[key] = pd.DataFrame(columns)
	assert pt._get_track_scatter_data(source, False)["data"].size == 0


##################################################
@pytest.mark.parametrize("source", [pytest.param("Unknown", id="unknown-source"), pytest.param("Track Count Mean", id="unsupported-mean")])
def test_get_track_scatter_data_unknown_source(pt, source):
	"""Renvoie un dictionnaire minimal pour les sources non prises en charge."""
	graph_data = pt._get_track_scatter_data(source, False)
	assert set(graph_data) == {"data", "title"}
	assert graph_data["data"].shape == (0,)
	assert graph_data["title"] == f"Tracks {source}"


##################################################
@pytest.mark.parametrize("source, msd_step, expected_title, expected_data", [
		pytest.param("MSD", 5, "Tracks MSD Step 5", [[81, 0.14]], id="msd-step-5"),
		pytest.param("Instant D", 1, "Tracks Instant D", [4.51, 1.37, 3.04, 1.13, 1e-06, 1.99, 1e-06, 2.34, 0.81, 4.02,
														  4.26, 1.31, 6.37, 0.60, 2.22, 4.83, 0.27, 0.96, 5.41, 9.19, 0.60, 1.24, 0.54, 2.43, 2.23, 1.61,
														  3.05],
					 id="instant-diffusion"),
		pytest.param("MSE(0)", 1, "Tracks MSE(0)", [[35, 1], [37, 1], [66, 1], [75, 1], [81, 1], [83, 1], [102, 1], [114, 1],
													[131, 1], [152, 1], [158, 1], [165, 1], [176, 1], [220, 1]], id="fit-error")])
def test_get_track_graph_data(source, msd_step, expected_title, expected_data):
	"""Vérifie les valeurs des analyses utilisées en histogramme ou en Dual."""
	pt = get_fake_pt()
	pt.settings.graph["MSD Step"].value = msd_step
	graph_data = pt._get_track_graph_data(source, False, False)
	assert graph_data["title"] == expected_title
	np.testing.assert_array_equal(graph_data["data"], expected_data)


##################################################
@pytest.mark.parametrize("source", [pytest.param("MSD", id="msd"), pytest.param("Instant D", id="diffusion"), pytest.param("MSE(0)", id="fit")])
def test_get_track_graph_data_empty(pt, source):
	"""Accepte des analyses de trajectoire vides."""
	graph_data = pt._get_track_graph_data(source, False, False)
	assert graph_data["data"].shape == (0,)
	assert graph_data["title"] == f"Tracks {source}"


##################################################
@pytest.mark.parametrize("source, msd_step, expected_title", [
		pytest.param("MSD", 9, "Tracks MSD Step 9", id="missing-msd-step"),
		pytest.param("Unknown", 1, "Tracks Unknown", id="missing-fit-column")])
def test_get_track_graph_data_missing_column(source, msd_step, expected_title):
	"""Renvoie des données vides si le step ou la colonne d'analyse n'existe pas."""
	pt = get_fake_pt()
	pt.settings.graph["MSD Step"].value = msd_step
	graph_data = pt._get_track_graph_data(source, False, False)
	assert graph_data["data"].shape == (0,)
	assert graph_data["title"] == expected_title


##################################################
@pytest.mark.parametrize("source, expected_limit, expected_bins", [
		pytest.param("Instant D", 1e-5, None, id="instant-diffusion"),
		pytest.param("D(0) (μm²/s)", 1e-5, None, id="diffusion"),
		pytest.param("A (μm²/s)", 1e-5, None, id="diffusion-slope"),
		pytest.param("MSD", -1.0, None, id="msd"),
		pytest.param("Length", None, -1, id="length"),
		pytest.param("MSE(0)", None, None, id="fit-error")])
@pytest.mark.parametrize("mode", [pytest.param(0, id="histogram"), pytest.param(2, id="dual")])
@pytest.mark.parametrize("log_scale", [pytest.param(False, id="linear"), pytest.param(True, id="logarithmic")])
def test_get_track_graph_data_options(pt, source, expected_limit, expected_bins, mode, log_scale):
	"""Vérifie les seuils d'ajustement dans les unités reçues et les classes entières des longueurs."""
	pt.settings.graph["Mode"].value = mode
	graph_data = pt._get_track_graph_data(source, log_scale, mode == 2)
	if mode != 0 or (source == "MSD" and log_scale): expected_limit = None
	elif log_scale and expected_limit is not None: expected_limit = -5.0
	assert graph_data.get("fit_limit") == expected_limit
	assert graph_data.get("bins") == expected_bins


##################################################
@pytest.mark.parametrize("source, expected_data", [
		pytest.param("Length Scatter", [[1, 99], [2, 2], [3, 2], [4, 2], [5, 2], [6, 2], [7, 2], [8, 2], [9, 2]], id="legacy-track-duration-pairs"),
		pytest.param("Length", [99, 2, 2, 2, 2, 2, 2, 2, 2], id="total-duration"),
		pytest.param("Length On", [1, 1, 2, 2, 2, 2, 2, 2, 2, 2], id="present-segments"),
		pytest.param("Length Off", [97], id="absent-segments")])
def test_get_track_length_data(source, expected_data):
	"""Vérifie les durées totales, les segments On/Off et l'ancien format avec identifiants."""
	pt = get_fake_pt()
	np.testing.assert_array_equal(pt._get_track_length_data(source, False), expected_data)


##################################################
def test_get_track_length_data_empty(pt):
	"""Accepte l'absence de trajectoires."""
	assert pt._get_track_length_data("Length", False).shape == (0,)


##################################################
def test_get_track_length_data_unknown_source():
	"""Renvoie des durées vides pour une source de longueur non prise en charge."""
	pt = get_fake_pt()
	assert pt._get_track_length_data("Length New", False).shape == (0,)


##################################################
@pytest.mark.parametrize("with_track_ids, expected_shape", [pytest.param(False, (0,), id="durations"), pytest.param(True, (0, 2), id="track-duration-pairs")])
def test_get_track_length_data_without_absence(pt, with_track_ids, expected_shape):
	"""Ne crée pas de segment absent pour les trajectoires présentes sur tous leurs plans."""
	pt.results["trc"] = pd.DataFrame({"Track": [1, 1, 2, 2], "Plane": [1, 2, 4, 5]})
	assert pt._get_track_length_data("Length Off", with_track_ids).shape == expected_shape


##################################################
@pytest.mark.parametrize("mean", [pytest.param(False, id="per-track"), pytest.param(True, id="mean")])
@pytest.mark.parametrize("log_scale", [pytest.param(False, id="linear"), pytest.param(True, id="logarithmic")])
def test_get_track_intensity_data(pt, mean, log_scale):
	"""Vérifie les doublons moyennés, les échecs exclus et les trous aux plans réels."""
	pt.results["trc"] = pd.DataFrame({"Track":                [12, 7, 7, 7, 12, 7, 12], "Plane": [2, 1, 1, 3, 4, 4, 4],
									  "Integrated Intensity": [20, 10, 30, 0, 40, -1, 60]})
	expected = np.array([[1, 2, 3, 4], [20, 20, 0, 50]] if mean else
						[[[2, np.nan, 4, np.nan], [20, np.nan, 50, np.nan]], [[1, np.nan, 3, 4], [20, np.nan, 0, np.nan]]], dtype=float)
	if log_scale:
		values = expected[1] if mean else expected[:, 1]
		with np.errstate(divide="ignore", invalid="ignore"): values[:] = np.where(values > 0, np.log10(values), np.nan)
	np.testing.assert_allclose(pt._get_track_intensity_data(mean, log_scale), expected, equal_nan=True)


##################################################
@pytest.mark.parametrize("log_scale", [pytest.param(False, id="linear"), pytest.param(True, id="logarithmic")])
def test_get_track_count_data(pt, log_scale):
	"""Compte les tracks présents et absents sans compter deux fois les doublons ni exclure les intensités invalides."""
	pt.results["trc"] = pd.DataFrame({"Track": [7, 7, 7, 12, 12], "Plane": [1, 1, 3, 2, 3], "Integrated Intensity": [-1, -1, np.nan, 0, np.inf]})
	expected = np.array([[[1, 2, 3], [1, 2, 2]], [[1, 2, 3], [1, 1, 2]], [[1, 2, 3], [0, 1, 0]]], dtype=float)
	if log_scale:
		with np.errstate(divide="ignore", invalid="ignore"): expected[:, 1] = np.where(expected[:, 1] > 0, np.log10(expected[:, 1]), np.nan)
	np.testing.assert_allclose(pt._get_track_count_data(log_scale), expected, equal_nan=True)


# endregion Graph


##################################################
@pytest.mark.parametrize("shape", [
		pytest.param(None, id="spots"), pytest.param(0, id="fixed-size"),
		pytest.param(1, id="isotropic"), pytest.param(2, id="anisotropic")])
@pytest.mark.parametrize("dimension", [pytest.param(0, id="2d"), pytest.param(1, id="z-stack")])
def test_hr_data_crop(shape, dimension):
	"""Compare le premier crop au rendu complet et vérifie sa désactivation sur le même objet."""
	pt = get_fake_pt()
	pt._stack = np.zeros((1, 100, 100), dtype=np.uint16)
	pt.settings.rois.set_size(100, 100)
	s = pt.settings.hr
	s["Dimension"].value = dimension
	s["Ratio"].value = 2
	s["Remove Beads"].value = False
	s["Drift Correction"].value = False
	s.gaussian.active = shape is not None
	if shape is not None: s.gaussian["Shape"].value = shape
	data = pt.results["loc"].copy()
	data["X"], data["Y"] = 40.25, 50.25
	data["Sigma X"], data["Sigma Y"] = 1.0, 2.0
	pt.results["loc"] = data
	pt.results["f_loc"] = data.copy()
	s["Crop"].value = False
	hr_data = pt.hr()
	full, full_plot = hr_data["visualization"], hr_data["plot_data"]
	s["Crop"].value = True
	hr_data = pt.hr()
	cropped, cropped_plot = hr_data["visualization"], hr_data["plot_data"]
	x0, x1, y0, y1 = pt.settings.rois.hr_box
	assert cropped.size < full.size
	np.testing.assert_array_equal(cropped, full[..., y0 * 2:y1 * 2, x0 * 2:x1 * 2])
	np.testing.assert_allclose(cropped_plot[:, -2:], full_plot[:, -2:] - [y0 * 2, x0 * 2])
	s["Crop"].value = False
	restored = pt.hr()["visualization"]
	np.testing.assert_array_equal(restored, full)
	assert pt.settings.rois.data_box == (-1, -1, -1, -1)


##################################################
@pytest.mark.parametrize("dimension, raw, head, width", [
		pytest.param(0, False, 1, 1, id="tracks-2d"),
		pytest.param(3, False, 1, 1, id="track-stack"),
		pytest.param(3, True, 1, 1, id="raw-background"),
		pytest.param(3, False, 29, 1, id="large-heads"),
		pytest.param(3, False, 1, 30, id="wide-tails"),
		pytest.param(3, True, 29, 30, id="wide-raw")])
@pytest.mark.parametrize("with_roi", [pytest.param(False, id="full-field"), pytest.param(True, id="partial-roi")])
def test_hr_tracks_data_crop(dimension, raw, head, width, with_roi):
	"""Le premier crop conserve les segments et leur empreinte, avec le même décalage pour le raw et les points."""
	pt = PALMTracer()
	pt._stack = np.full((3, 100, 100), 1000, dtype=np.uint16)
	rois = pt.settings.rois
	rois.set_size(100, 100)
	if with_roi:
		rois.set_xy_roi(36, 90, 20, 90)
		rois.roi_selection.active = True
	pt.results["trc"] = pd.DataFrame({"Track": [1, 1, 1], "Plane": [1, 2, 3],
									  "X":     [30, 40, 50], "Y": [35, 45, 40], "Integrated Intensity": [1000] * 3})
	s = pt.settings.hr
	s["Dimension"].value = dimension
	s["Type"].value = 1
	s["Ratio"].value = 2
	s["Scaling"].value = 1000
	s["Remove Beads"].value = False
	s["Drift Correction"].value = False
	s.track_stack["Head"].value = head
	s.track_stack["Width"].value = width
	s.track_stack["Background"].value = raw
	s["Crop"].value = False
	hr_data = pt.hr()
	full, full_plot = hr_data["visualization"], hr_data["plot_data"]
	base_x, _, base_y, _ = rois.hr_box

	s["Crop"].value = True
	hr_data = pt.hr()
	cropped, cropped_plot = hr_data["visualization"], hr_data["plot_data"]
	x0, x1, y0, y1 = rois.hr_box
	y_slice, x_slice = slice((y0 - base_y) * 2, (y1 - base_y) * 2), slice((x0 - base_x) * 2, (x1 - base_x) * 2)
	assert cropped.size < full.size
	assert np.any(cropped)
	if raw: np.testing.assert_array_equal(cropped, full[:, y_slice, x_slice, :])
	else:
		np.testing.assert_array_equal(cropped, full[..., y_slice, x_slice])
		# Reconstituer l'image entière vérifie aussi qu'aucun signal n'a été coupé hors du nouveau cadre.
		reconstructed = np.zeros_like(full)
		reconstructed[..., y_slice, x_slice] = cropped
		np.testing.assert_array_equal(reconstructed, full)
	np.testing.assert_allclose(cropped_plot[:, -2:], full_plot[:, -2:] - [(y0 - base_y) * 2, (x0 - base_x) * 2])
	np.testing.assert_array_equal(cropped_plot[:, :2], full_plot[:, :2])
	if with_roi: assert rois.hr_box[0] == 36

	s["Crop"].value = False
	restored = pt.hr()["visualization"]
	np.testing.assert_array_equal(restored, full)
	assert rois.data_box == (-1, -1, -1, -1)


##################################################
def test_hr():
	"""Vérifie différentes récupérations de données."""
	pt = get_fake_pt()
	ref_empty = np.zeros((1, 1), dtype=np.uint16)
	ref_viz0 = np.zeros((10, 10), dtype=np.uint16)
	s = pt.settings.hr
	s["Ratio"].value = 2
	s["Source"].value = 1
	s["Remove Beads"].value = False
	s["Drift Correction"].value = False

	# Aucune pile
	hr_data = pt.hr()
	viz, plot = hr_data["visualization"], hr_data["plot_data"]
	assert np.allclose(ref_empty, viz) and np.allclose(ref_empty, plot)

	# HR Localisation
	pt._stack = np.zeros((1, 5, 5), dtype=np.uint16)
	pt.settings.rois.set_size(5, 5)
	hr_data = pt.hr()
	viz, plot = hr_data["visualization"], hr_data["plot_data"]
	ref_viz = ref_viz0.copy()
	ref_viz[4, 2] = ref_viz[6, 4] = 2
	ref_plot = [[0, 4, 2], [0, 6, 4], [0, 8, 6], [0, 10, 8], [0, 4, 2],
				[0, 6, 4]]  # (8,6) à une intensité de 0 et (10,8) est sur le bord de l'image (donc hors cadre)
	np.testing.assert_array_equal(viz, ref_viz)
	np.testing.assert_array_equal(plot, ref_plot)

	# Mise à l'échelle de l'intensité des localisations
	s["Scaling"].value = 2
	hr_data = pt.hr()
	viz, scaled_plot = hr_data["visualization"], hr_data["plot_data"]
	np.testing.assert_array_equal(viz, ref_viz * 2)
	np.testing.assert_array_equal(scaled_plot, ref_plot)
	s["Scaling"].value = 1

	# HR Localisation remove beads
	s["Remove Beads"].value = True
	hr_data = pt.hr()
	viz, plot = hr_data["visualization"], hr_data["plot_data"]
	np.testing.assert_array_equal(viz, ref_viz)
	np.testing.assert_array_equal(plot, ref_plot)

	# HR Localisation Drift Correction
	s["Drift Correction"].value = True
	pt.results["bds"] = pd.DataFrame([[1, 1, 1, 1, 2, 3, 1, 1, 1, 0, 1],
									  [1, 2, 2, 2, 3, 4, 1, 1, 1, 0, 1],
									  [1, 3, 3, 50, 3, 4, 1, 1, 1, 0, 1],  # Valeur aberrante gommée par le smooth
									  [1, 4, 4, 4, 3, 4, 1, 1, 1, 0, 1],
									  [1, 5, 5, 5, 3, 4, 1, 1, 1, 0, 1]],
									 columns=Parsing.FILES_COLUMNS["Beads"]["columns"])
	hr_data = pt.hr()
	viz, plot = hr_data["visualization"], hr_data["plot_data"]
	ref_viz = ref_viz0.copy()
	ref_viz[4, 0] = ref_viz[6, 4] = 1
	ref_plot = [[0, 6, 4], [0, 8, 6], [0, 10, 8], [0, 4, 0]]
	np.testing.assert_array_equal(viz, ref_viz)
	np.testing.assert_array_equal(plot, ref_plot)
	s["Drift Correction"].value = False

	# HR Localisation DataFrame vide
	for _ in range(4): pt.results.localizations.drop(pt.results.localizations.index, inplace=True)
	hr_data = pt.hr()
	viz, plot = hr_data["visualization"], hr_data["plot_data"]
	assert np.allclose(ref_empty, viz) and np.allclose(ref_empty, plot)

	# HR Tracking
	s["Type"].value = 1
	hr_data = pt.hr()
	viz, plot = hr_data["visualization"], hr_data["plot_data"]
	ref_viz = ref_viz0.copy()
	ref_viz[2, 2] = 15
	ref_viz[2, 8] = 8
	ref_plot = [[1, 1, 2, 2], [1, 99, 2, 2], [3, 3, 2, 8], [3, 4, 2, 8], [4, 3, 2, 10], [4, 4, 2, 10], [5, 5, 2, 8],
				[5, 6, 2, 8], [6, 11, 2, 2], [6, 12, 2, 2], [7, 16, 2, 10], [7, 17, 2, 10], [8, 31, 2, 2], [8, 32, 2, 2]]
	np.testing.assert_array_equal(viz, ref_viz)
	np.testing.assert_array_equal(plot, ref_plot)

	# Couleur de fond des trajectoires
	s["Background"].value = 42
	hr_data = pt.hr()
	viz, background_plot = hr_data["visualization"], hr_data["plot_data"]
	ref_background = np.full_like(ref_viz, 27525)
	ref_background[2, 2] = 15
	ref_background[2, 8] = 8
	np.testing.assert_array_equal(viz, ref_background)
	np.testing.assert_array_equal(background_plot, ref_plot)
	s["Background"].value = 0

	# Mise à l'échelle de l'intensité des trajectoires
	s["Scaling"].value = 2
	hr_data = pt.hr()
	viz, scaled_plot = hr_data["visualization"], hr_data["plot_data"]
	np.testing.assert_array_equal(viz, ref_viz * 2)
	np.testing.assert_array_equal(scaled_plot, ref_plot)
	s["Scaling"].value = 1

	# HR Tracking DataFrame vide
	for _ in range(4): pt.results.tracks.drop(pt.results.tracks.index, inplace=True)
	hr_data = pt.hr()
	viz, plot = hr_data["visualization"], hr_data["plot_data"]
	assert np.allclose(ref_empty, viz) and np.allclose(ref_empty, plot)


##################################################
@pytest.mark.parametrize("dimension", [pytest.param(0, id="2d"), pytest.param(1, id="z-stack")])
@pytest.mark.parametrize("key", [pytest.param("loc", id="raw"), pytest.param("dft", id="corrected")])
@pytest.mark.parametrize("selection", [pytest.param("subset", id="excluded-points"), pytest.param("all", id="all-kept")])
def test_hr_filtered_plot_data(monkeypatch, dimension, key, selection):
	"""Sépare les points après une préparation commune sans changer l'image ni l'origine Z des points conservés."""
	pt = PALMTracer()
	pt._stack = np.zeros((2, 8, 8), dtype=np.uint16)
	pt.settings.rois.set_size(8, 8)
	locations = pd.DataFrame({"Plane":                [1, 2, 2, 2], "X": [1, 3, 2, 20], "Y": [2, 4, 3, 20], "Z": [4, 8, 2, 0],
							  "Integrated Intensity": [2, 4, -100, 8], "Sigma X": [1.0] * 4, "Sigma Y": [1.0] * 4, "Theta": [0.0] * 4},
							 index=[10, 20, 30, 40])
	kept = locations.iloc[:2].copy() if selection == "subset" else locations.copy()
	pt.results[key], pt.results[f"f_{key}"] = locations.copy(), kept.copy()
	s = pt.settings.hr
	s["Dimension"].value, s["Ratio"].value = dimension, 2
	s["Remove Beads"].value = s["Drift Correction"].value = s["Crop"].value = False
	s.gaussian.active = False
	s.hr_3d["Z Step"].value = 2
	s["Source"].value = 1  # Intensité intégrée.
	prepared_lengths = []
	correct_drift = pt._correct_drift

	def record_preparation(data):
		"""Observe la préparation commune des localisations sans modifier leur traitement."""
		prepared_lengths.append(len(data))
		return correct_drift(data)

	monkeypatch.setattr(pt, "_correct_drift", record_preparation)
	data = pt.hr()
	assert prepared_lengths == [4]
	assert set(data) == {"visualization", "plot_data", "plot_filtered"}
	if selection == "subset":
		np.testing.assert_allclose(data["plot_data"], [[0, 4, 2], [0 if dimension == 0 else 2, 8, 6]])
		np.testing.assert_allclose(data["plot_filtered"], [[0 if dimension == 0 else -1, 6, 4]])
	else: assert data["plot_filtered"].shape == (0, 3)
	pd.testing.assert_frame_equal(pt.results[key], locations)
	pd.testing.assert_frame_equal(pt.results[f"f_{key}"], kept)

	# Le rendu de référence contient directement les points conservés, sans résultat filtré.
	pt.results.reset_filtered()
	pt.results[key] = kept.copy()
	reference = pt.hr()
	assert set(reference) == {"visualization", "plot_data"}
	np.testing.assert_array_equal(data["visualization"], reference["visualization"])
	np.testing.assert_array_equal(data["plot_data"], reference["plot_data"])


##################################################
@pytest.mark.parametrize("filtered", [pytest.param(False, id="unfiltered"), pytest.param(True, id="filtered")])
def test_hr_localization_z_source(pt, filtered):
	"""Le rendu Z normalise les points conservés sur uint16 sans inclure les points exclus dans les extrema."""
	pt._stack = np.zeros((1, 8, 8), dtype=np.uint16)
	pt.settings.rois.set_size(8, 8)
	locations = pd.DataFrame({"Plane":   [1] * 4, "X": [1.0, 2.0, 3.0, 4.0], "Y": [1.0] * 4,
							  "Z":       [-200.0, 0.0, 200.0, -10000.0], "Integrated Intensity": [100.0] * 4,
							  "Sigma X": [1.0] * 4, "Sigma Y": [1.0] * 4, "Theta": [0.0] * 4})
	pt.results["loc"] = locations.copy() if filtered else locations.iloc[:3].copy()
	if filtered: pt.results["f_loc"] = locations.iloc[:3].copy()
	before = pt.results["loc"].copy(deep=True)
	s = pt.settings.hr
	s["Ratio"].value = 1
	s["Remove Beads"].value = s["Drift Correction"].value = s["Crop"].value = False
	s.gaussian.active = False
	source = s["Source"]
	assert isinstance(source, Combo)
	source.value = source.items.index("Z")

	data = pt.hr()

	np.testing.assert_array_equal(data["visualization"][1, 1:4], [0, 32767, 65535])
	assert data["visualization"][1, 4] == 0
	np.testing.assert_array_equal(data["plot_data"], [[0, 1, 1], [0, 1, 2], [0, 1, 3]])
	if filtered: np.testing.assert_array_equal(data["plot_filtered"], [[0, 1, 4]])
	else: assert "plot_filtered" not in data
	pd.testing.assert_frame_equal(pt.results["loc"], before)


##################################################
@pytest.mark.parametrize("key", [pytest.param("loc", id="raw"), pytest.param("dft", id="corrected")])
def test_hr_filtered_points_all_removed_as_beads(pt, key):
	"""Une sélection composée uniquement de billes ne produit aucun rendu HR."""
	pt._stack = np.zeros((1, 8, 8), dtype=np.uint16)
	pt.settings.rois.set_size(8, 8)
	locations = pd.DataFrame({"Id":                   [1, 2], "Plane": [1, 1], "X": [2.0, 4.0], "Y": [2.0, 4.0], "Z": [0.0, 0.0],
							  "Integrated Intensity": [100.0, 200.0], "Sigma X": [1.0, 1.0], "Sigma Y": [1.0, 1.0], "Theta": [0.0, 0.0]})
	pt.results[key] = locations.copy()
	pt.results[f"f_{key}"] = locations.iloc[:1].copy()
	pt.results["bds"] = locations.iloc[:1].copy()

	s = pt.settings.hr
	s["Remove Beads"].value = True
	s["Drift Correction"].value = s["Crop"].value = False

	data = pt.hr()

	np.testing.assert_array_equal(data["visualization"], np.zeros((1, 1), dtype=np.uint16))
	assert data["plot_filtered"].shape == (0, 3)
	np.testing.assert_array_equal(data["plot_data"], np.zeros((1, 1)))


##################################################
def test_hr_filter():
	"""Vérifie différentes récupérations de données."""
	pt = get_fake_pt()
	s = pt.settings.hr
	s["Ratio"].value = 2
	s["Source"].value = 1
	s["Remove Beads"].value = False
	s["Drift Correction"].value = False

	# Filtre sur X
	pt._stack = np.zeros((1, 5, 5), dtype=np.uint16)
	pt.settings.rois.set_size(5, 5)
	sf = pt.settings.filters
	sf["ROI"].active = True
	pt.settings.rois.set_xy_roi(2, 5, 0, 5, False)
	hr_data = pt.hr()
	viz, plot = hr_data["visualization"], hr_data["plot_data"]
	ref_viz = np.zeros((10, 6), dtype=np.uint16)
	ref_viz[6, 0] = 2  # Précédemment [4, 2], [6, 4] mais avec le filtre sur X à 2 le premier devient hors filtre (-2 × facteur d'agrandissement de 2 = -4).
	ref_plot = [[0, 6, 0], [0, 8, 2], [0, 10, 4], [0, 6, 0]]
	np.testing.assert_array_equal(viz, ref_viz)
	np.testing.assert_array_equal(plot, ref_plot)

	# Filtre sur Y
	pt.settings.rois.set_xy_roi(2, 5, 2, 5, False)
	hr_data = pt.hr()
	viz, plot = hr_data["visualization"], hr_data["plot_data"]
	ref_viz = np.zeros((6, 6), dtype=np.uint16)
	ref_viz[2, 0] = 2
	ref_plot = [[0, 2, 0], [0, 4, 2], [0, 6, 4], [0, 2, 0]]
	np.testing.assert_array_equal(viz, ref_viz)
	np.testing.assert_array_equal(plot, ref_plot)

	# Tracking Filtré
	s["Type"].value = 1
	pt.settings.rois.set_xy_roi(1, 4, 1, 2, False)
	hr_data = pt.hr()
	viz, plot = hr_data["visualization"], hr_data["plot_data"]
	ref_viz = np.zeros((2, 6), dtype=np.uint16)
	ref_viz[0, 0] = 15
	ref_plot = [[1, 1, 0, 0], [1, 99, 0, 0], [3, 3, 0, 6], [3, 4, 0, 6], [5, 5, 0, 6], [5, 6, 0, 6],
				[6, 11, 0, 0], [6, 12, 0, 0], [8, 31, 0, 0], [8, 32, 0, 0]]
	np.testing.assert_array_equal(viz, ref_viz)
	np.testing.assert_array_equal(plot, ref_plot)


##################################################
def test_hr_track_crossing_roi():
	"""Trace depuis le bord de la ROI un segment dont le premier point est extérieur."""
	pt = PALMTracer()
	pt._stack = np.zeros((2, 5, 5), dtype=np.uint16)
	pt.settings.rois.set_size(5, 5)
	pt.settings.rois.set_xy_roi(1, 4, 0, 5, add=False)
	pt.settings.filters["ROI"].active = True
	pt.results["trc"] = pd.DataFrame([[1, 1, 0, 2, 100], [1, 2, 2, 2, 100]], columns=["Track", "Plane", "X", "Y", "Integrated Intensity"])
	s = pt.settings.hr
	s["Type"].value = 1
	s["Ratio"].value = 1
	s["Drift Correction"].value = False

	hr_data = pt.hr()
	viz, plot = hr_data["visualization"], hr_data["plot_data"]

	ref = np.zeros((5, 3), dtype=np.uint16)
	ref[2, 0:2] = 1
	np.testing.assert_array_equal(viz, ref)
	np.testing.assert_array_equal(plot, [[1, 2, 2, 1]])


##################################################
def test_hr_empty_roi_3d():
	"""Génère un volume vide aux dimensions de la ROI lorsqu'elle ne contient aucune localisation."""
	pt = get_fake_pt()
	pt._stack = np.zeros((1, 5, 5), dtype=np.uint16)
	pt.settings.rois.set_size(5, 5)
	pt.settings.rois.set_xy_roi(0, 1, 0, 1, add=False)
	pt.settings.filters["ROI"].active = True
	s = pt.settings.hr
	s["Dimension"].value = 1
	s["Ratio"].value = 2
	s["Remove Beads"].value = False
	s["Drift Correction"].value = False

	hr_data = pt.hr()
	viz, plot = hr_data["visualization"], hr_data["plot_data"]

	assert viz.shape == (1, 2, 2)
	assert plot.shape == (0, 3)
	assert not np.any(viz)


##################################################
def test_hr_z_stack():
	"""Vérifie que les points vectoriels utilisent le même pas Z que le rendu."""
	pt = get_fake_pt()
	s = pt.settings.hr
	s["Dimension"].value = 1
	s.hr_3d["Z Step"].value = 1
	s["Ratio"].value = 2
	s["Source"].value = 1
	s["Remove Beads"].value = False
	s["Drift Correction"].value = False
	# HR Localisation
	pt._stack = np.zeros((1, 5, 5), dtype=np.uint16)
	pt.settings.rois.set_size(5, 5)
	hr_data = pt.hr()
	viz, plot = hr_data["visualization"], hr_data["plot_data"]
	# Les Z de 3 à 6 nm deviennent les plans 0 à 3 avec un pas de 1 nm.
	# Le point du plan 3 est hors image en Y ; le plan 2 est conservé, mais son intensité est nulle.
	ref_viz = np.zeros((3, 10, 10), dtype=np.uint16)
	ref_viz[0, 4, 2] = ref_viz[1, 6, 4] = 2
	ref_plot = [[0, 4, 2], [1, 6, 4], [2, 8, 6], [3, 10, 8], [0, 4, 2], [1, 6, 4]]
	np.testing.assert_array_equal(viz, ref_viz)
	np.testing.assert_array_equal(plot, ref_plot)


##################################################
def test_hr_rotation():
	"""Vérifie différentes récupérations de données."""
	pt = get_fake_pt()
	s = pt.settings.hr
	s["Dimension"].value = 2
	s.hr_3d["Frames"].value = 2
	s["Ratio"].value = 2
	s["Source"].value = 1
	s["Remove Beads"].value = False
	s["Drift Correction"].value = False
	# HR Localisation
	pt._stack = np.zeros((1, 5, 5), dtype=np.uint16)
	pt.settings.rois.set_size(5, 5)
	hr_data = pt.hr()
	viz, plot = hr_data["visualization"], hr_data["plot_data"]
	ref_viz = np.zeros((2, 17, 17), dtype=np.uint16)
	ref_viz[0, 8, 6] = ref_viz[0, 10, 8] = ref_viz[1, 8, 10] = ref_viz[1, 10, 8] = 2
	ref_plot = [[0, 4, 2], [2, 6, 4], [4, 8, 6], [6, 10, 8], [0, 4, 2], [2, 6, 4]]
	np.testing.assert_array_equal(viz, ref_viz)
	np.testing.assert_array_equal(plot, ref_plot)


##################################################
def test_hr_stress():
	"""Vérifie génération HR plus complexe."""
	pt = PALMTracer()
	pt.settings.rois.set_size(8, 8)
	n_p, n_x, n_y = 8, 8, 4  # Dimensions de la pile
	pt._stack = np.zeros((n_p, n_y, n_x), dtype=np.uint16)
	pt.settings.rois.set_size(8, 4)
	ref_viz0 = np.zeros((n_y * 2, n_x * 2), dtype=np.uint16)

	s = pt.settings.hr
	s["Ratio"].value = 2
	s["Source"].value = 1
	s["Remove Beads"].value = False
	s["Drift Correction"].value = False

	# Bille qui part en diagonale du haut à droite vers le bas à gauche
	bead_x, bead_y = np.linspace(n_x - 0.5, 0, n_p, dtype=float), np.linspace(0, n_y - 0.5, n_p, dtype=float)

	beads = pd.DataFrame({"Bead":  np.ones(n_p, dtype=int),
						  "Plane": np.arange(1, n_p + 1, dtype=int),
						  "X":     bead_x,
						  "Y":     bead_y,
						  "Z":     np.zeros(n_p, dtype=float)})

	# Localisation au centre
	loc = pd.DataFrame({"Plane":                np.arange(1, n_p + 1, dtype=int),
						"X":                    np.full(n_p, n_x / 2.0, dtype=float),
						"Y":                    np.full(n_p, n_y / 2.0, dtype=float),
						"Z":                    np.zeros(n_p, dtype=float),
						"Integrated Intensity": np.full(n_p, 1, dtype=float),
						"Sigma X":              np.ones(n_p, dtype=float),
						"Sigma Y":              np.ones(n_p, dtype=float),
						"Theta":                np.zeros(n_p, dtype=float)})

	pt.results["bds"], pt.results["loc"] = beads.copy(), loc.copy()

	# Génération fixe (n_beads fois sur la position centrale)
	viz = pt.hr()["visualization"]
	ref = ref_viz0.copy()
	ref[n_y, n_x] = n_p
	np.testing.assert_array_equal(viz, ref)

	# Génération fixe de la bille (n_beads fois sur la position [1, 1] * upscale)
	pt.results["loc"].loc[:, ["X", "Y"]] = pt.results["bds"].loc[:, ["X", "Y"]].to_numpy()
	viz = pt.hr()["visualization"]
	ref = ref_viz0.copy()
	ref[0, 15] = ref[1, 13] = ref[2, 11] = ref[3, 9] = ref[4, 6] = ref[5, 4] = ref[6, 2] = ref[7, 0] = 1
	np.testing.assert_array_equal(viz, ref)

	# Génération Drift corrigé des mêmes données que la bille, donc le premier point sera compté 8 fois.
	s["Drift Correction"].value = True
	viz = pt.hr()["visualization"]
	ref = ref_viz0.copy()
	ref[np.round(bead_y[0] * 2).astype(int), np.round(bead_x[0] * 2).astype(int)] = n_p
	np.testing.assert_array_equal(viz, ref)

	# Génération Drift corrigé, mais la localisation était fixe
	# (donc elle va bouger vers le haut à droite, elle remonte la diagonale et une partie sera hors champs (départ au centre)
	pt.results["bds"], pt.results["loc"] = beads.copy(), loc.copy()
	viz = pt.hr()["visualization"]
	ref = ref_viz0.copy()
	ref[4, 8] = ref[3, 10] = ref[2, 12] = ref[1, 14] = 1  # Les autres points hors champ continuent (0,16) (-1, 18)...
	np.testing.assert_array_equal(viz, ref)

	# Seconde bille qui descend comme la précédente, mais ne va pas vers la gauche donc la pente initiale sera divisé par 2.
	beads2 = pd.DataFrame({"Bead":  np.full(n_p, 2, dtype=int),
						   "Plane": np.arange(1, n_p + 1, dtype=int),
						   "X":     np.zeros_like(bead_x, dtype=float),
						   "Y":     bead_y,
						   "Z":     np.zeros(n_p, dtype=float)})

	pt.results["bds"] = pd.concat([beads, beads2], ignore_index=True)
	viz = pt.hr()["visualization"]
	ref = ref_viz0.copy()
	ref[4, 8] = ref[3, 9] = ref[2, 10] = ref[1, 11] = ref[0, 12] = 1  # Les autres points hors champ continuent (-1,13) (-2, 14)...
	np.testing.assert_array_equal(viz, ref)

	# On ajoute nos 2 billes à la localisation et on enlève le drift, tout doit être affiché
	s["Drift Correction"].value = False
	size = 3 * n_p
	loc2 = pd.DataFrame({"Plane":                np.tile(np.arange(1, n_p + 1, dtype=int), 3),
						 "X":                    np.full(size, n_x / 2.0, dtype=float),
						 "Y":                    np.full(size, n_y / 2.0, dtype=float),
						 "Z":                    np.zeros(size, dtype=float),
						 "Integrated Intensity": np.full(size, 1, dtype=float),
						 "Sigma X":              np.ones(size, dtype=float),
						 "Sigma Y":              np.ones(size, dtype=float),
						 "Theta":                np.zeros(size, dtype=float)})
	loc2.loc[n_p:, ["X", "Y"]] = pt.results["bds"].loc[:, ["X", "Y"]].to_numpy()

	pt.results["loc"] = loc2.copy()
	viz = pt.hr()["visualization"]
	ref = ref_viz0.copy()
	ref[0, 15] = ref[1, 13] = ref[2, 11] = ref[3, 9] = ref[4, 6] = ref[5, 4] = ref[6, 2] = ref[7, 0] = 1  # Bille originale
	ref[n_y, n_x] += n_p  # Localization statique
	ref[:, 0] += 1  # Bille Verticale
	np.testing.assert_array_equal(viz, ref)

	# On supprime nos 2 billes (mais on va conserver notre localisation
	s["Remove Beads"].value = True
	viz = pt.hr()["visualization"]
	ref = ref_viz0.copy()
	ref[n_y, n_x] += n_p  # Localization statique
	np.testing.assert_array_equal(viz, ref)

	# Bille avec une trajectoire aléatoire.
	s["Remove Beads"].value = False
	s["Drift Correction"].value = True
	pt.results["bds"], pt.results["loc"] = beads.copy(), loc.copy()
	pt.results["bds"]["X"] = np.array([5.095, 3.755, 5.434, 4.789, 2.376, 5.902, 5.044, 5.144], dtype=float)  # Aléatoire autour du centre.
	pt.results["bds"]["Y"] = np.array([1.256, 1.900, 1.741, 2.853, 2.287, 2.645, 1.886, 1.454], dtype=float)  # Aléatoire autour du centre.
	viz = pt.hr()["visualization"]
	ref = ref_viz0.copy()
	# Position au centre puis résultat du random dans tous les sens ATTENTION LE DRIFT EST LISSÉ.
	ref[4, 8] = ref[3, 9] = ref[2, 11] = ref[2, 13] = ref[2, 14] = ref[3, 15] = 1
	np.testing.assert_array_equal(viz, ref)

	# Correction sur la position de la bille avec lissage...
	pt.results["loc"].loc[:, ["X", "Y"]] = pt.results["bds"].loc[:, ["X", "Y"]].to_numpy()
	viz = pt.hr()["visualization"]
	ref = ref_viz0.copy()
	# Position corrigée de la bille aléatoire. Le drift est lissé, il ne s'agit donc pas d'un point unique.
	ref[3, 9] = ref[3, 10] = ref[2, 11] = ref[2, 14] = ref[3, 14] = 1
	np.testing.assert_array_equal(viz, ref)

	# Correction sur la position de la bille sans lissage...
	s["Smooth Drift"].value = False
	viz = pt.hr()["visualization"]
	ref = ref_viz0.copy()
	# Position de la bille random corrigé et non lissé.
	ref[3, 10] = n_p
	np.testing.assert_array_equal(viz, ref)


##################################################
@pytest.mark.parametrize("background", [False, True], ids=["no-background", "with-background"])
@pytest.mark.parametrize("color_mode", [0, 1, 2], ids=["addition", "maximum", "minimum"])
def test_hr_track_stack(monkeypatch, background, color_mode):
	"""Vérifie les options, la ROI et l'alignement temporel du rendu animé avec ou sans fond brut."""
	pt = PALMTracer()
	pt._stack = np.full((8, 8, 9), 25700, dtype=np.uint16)
	pt.settings.rois.set_size(9, 8)
	monkeypatch.setattr(pt.settings.rois, "get_roi_limits", lambda: (2, 7, 1, 6))
	pt.results["trc"] = pd.DataFrame([[1, 1, 6.9, 2, 100], [1, 3, 3, 2, 100], [1, 5, 4, 3, 100]], columns=["Track", "Plane", "X", "Y", "Integrated Intensity"])
	original = pt.results.tracks.copy(deep=True)
	s = pt.settings.hr
	s["Dimension"].value = 3
	assert s["Type"].value == 1  # .		Vérification, Avec track stack la type est forcément Tracks
	for key, value in {"Ratio": 2, "Color mode": color_mode, "Background": 20, "Scaling": 2, "Drift Correction": False}.items(): s[key].value = value
	options = s["T-Stack"]
	for key, value in {"Head": 3, "Width": 2, "Length": 2, "Fade": 1, "Map": 1, "Background": background, "Upscale": 1}.items(): options[key].value = value

	hr_data = pt.hr()
	viz, plot = hr_data["visualization"], hr_data["plot_data"]
	assert viz.shape == ((5, 10, 10, 3) if background else (5, 10, 10))
	assert viz.dtype == (np.uint8 if background else np.uint16)
	np.testing.assert_array_equal(plot, [[1, 0, 2, 9.8], [1, 2, 2, 2], [1, 4, 4, 4]])
	# Compare le pipeline à un rendu direct des coordonnées et options attendues.
	reference = pt._renderer.track_stack(np.array([[1, 1, 4.9, 1, 2], [1, 3, 1, 1, 2], [1, 5, 2, 2, 2]], dtype=float),
										 color_mode, 13107, 3, 2, 2, 1, pt._stack[:, 1:6, 2:7] if background else None, 1, "magma")
	np.testing.assert_array_equal(viz, reference)
	if background: np.testing.assert_array_equal(viz[:, 9, 9], np.full((5, 3), 100, dtype=np.uint8))
	else: np.testing.assert_array_equal(viz[:, 9, 9], [13107] * 5)
	pd.testing.assert_frame_equal(pt.results.tracks, original)
	assert pt.output_viz_name().suffix == ".tif"
	assert "visualization_track_stack_tracks" in pt.output_viz_name().name


##################################################
@pytest.mark.parametrize("crop, expected_box, expected_shape", [
		pytest.param(False, (0, 5, 0, 5), (1, 5, 5), id="full-field"),
		pytest.param(True, (1, 5, 1, 5), (1, 4, 4), id="auto-crop")])
def test_hr_track_stack_empty_roi(crop, expected_box, expected_shape):
	"""Vérifie une animation sans trajectoire conservée dans la ROI."""
	pt = PALMTracer()
	pt._stack = np.zeros((3, 5, 5), dtype=np.uint16)
	pt.settings.rois.set_size(5, 5)
	pt.results["trc"] = pd.DataFrame([[1, 2, 6, 6, 100]], columns=["Track", "Plane", "X", "Y", "Integrated Intensity"])
	pt.settings.hr["Dimension"].value = 3
	pt.settings.hr["Ratio"].value = 1
	pt.settings.hr["Crop"].value = crop
	hr_data = pt.hr()
	viz, plot = hr_data["visualization"], hr_data["plot_data"]
	assert pt.settings.rois.hr_box == expected_box
	assert viz.shape == expected_shape
	assert plot.shape == (0, 4)
	assert not np.any(viz)


##################################################
@pytest.mark.parametrize("raw_background, background_color, expected_shape", [
		pytest.param(False, 20, (2, 3, 3), id="uniform-background"),
		pytest.param(True, 0, (2, 3, 3, 3), id="raw-background"),
		pytest.param(False, 0, (2, 1, 2), id="black-background")])
def test_hr_track_stack_crop_background(raw_background, background_color, expected_shape):
	"""Caractérise l'autocrop d'un track stack déjà recadré sur une ROI, selon son fond."""
	pt = PALMTracer()
	pt._stack = np.full((2, 5, 5), 25700, dtype=np.uint16)
	pt.settings.rois.set_size(5, 5)
	pt.settings.rois.set_xy_roi(1, 4, 1, 4, add=False)
	pt.settings.filters["ROI"].active = True
	pt.results["trc"] = pd.DataFrame([[1, 1, 1, 2, 100], [1, 2, 2, 2, 100]],
									 columns=["Track", "Plane", "X", "Y", "Integrated Intensity"])
	s = pt.settings.hr
	s["Dimension"].value = 3
	s["Ratio"].value = 1
	s["Background"].value = background_color
	s["Drift Correction"].value = False
	s.track_stack["Head"].value = 1
	s.track_stack["Width"].value = 1
	s.track_stack["Length"].value = -1
	s.track_stack["Background"].value = raw_background

	viz = pt.hr()["visualization"]
	cropped = pt.crop(viz, margin=0)

	assert viz.shape == ((2, 3, 3, 3) if raw_background else (2, 3, 3))
	assert cropped.shape == expected_shape


##################################################
def test_hr_track_stack_dimension_switch(qtbot):
	"""Vérifie le type sélectionné et la réactivation des localisations en quittant le mode animé."""
	pt = PALMTracer()
	s = pt.settings.hr
	ui = s.get_ui()
	qtbot.addWidget(ui.widget)
	s["Dimension"].value = 3
	assert s["Type"].value == 1
	assert cast(Combo, s["Source"]).current_text == "Track ID"
	assert not s["Type"]._uis["default"].boxes[0].isEnabled()
	for dimension in [0, 1, 2]:
		s["Dimension"].value = dimension
		assert s["Type"]._uis["default"].boxes[0].isEnabled()
		if dimension != 0: assert s["Type"].value == 0
		s["Dimension"].value = 3


##################################################
def test_crop():
	"""Vérifie la création du widget."""

	pt = get_fake_pt()
	img = np.zeros((1, 1), dtype=np.uint16)
	res = pt.crop(img)  # .										Crop à True, image noire
	assert np.allclose(img, res)  # .							Crop à True, avec un carré à 1 et une marge (par défaut) de 5

	img = np.zeros((10, 10), dtype=np.uint16)
	img[2:4, 6:] = 1  # Carré de 1.
	ref = img[:-1, 1:].copy()  # .								Le crop avec une marge de 5 va très peu recadrer
	assert np.allclose(pt.crop(img), ref)  # .					Crop à True, avec un carré à 1 et une marge (par défaut) de 5
	assert np.allclose(pt.crop(img, 0), np.ones((2, 4)))  # .	Crop à True, avec aucune marge donc uniquement les points à 1

	vol = np.zeros((10, 10, 10), dtype=np.uint16)
	vol[0, 2:4, 6:] = 1
	assert np.allclose(pt.crop(vol, 0), np.ones((1, 2, 4)))  # .Crop à True, avec aucune marge donc uniquement les points à 1

	pt.settings.hr["Crop"].value = False
	assert np.allclose(pt.crop(img), img)  # .					Crop à False, aucun changement dans l'image


##################################################
def test_crop_track_stack_rgb():
	"""Préserve les trois canaux RGB, même si un seul canal est non nul ou si le volume est noir."""
	pt = PALMTracer()
	img = np.zeros((3, 10, 10, 3), dtype=np.uint8)
	img[1, 2:4, 6:8, 0] = 255
	cropped = pt.crop(img, margin=0)
	assert cropped.shape == (1, 2, 2, 3)
	np.testing.assert_array_equal(cropped, img[1:2, 2:4, 6:8])
	assert pt.crop(np.zeros_like(img)).shape == (1, 1, 1, 3)

# ==================================================
# endregion Visualisation
# ==================================================
