"""
Fichier des tests pour la classe PALMTracer

.. note:: Il est fréquent que la vérificaiton du log ne se fasse qu'au nombre de lignes, car au moins 15 lignes à chaque process.
"""
import shutil
from time import sleep

import pytest

from palm_tracer._tests.Utils import *
from palm_tracer.PALMTracer import FILE_STATUS
from palm_tracer.Tools import FileIO

OUTPUT_FOLDER = INPUT_DIR / "stack_PALM_Tracer"
OUTPUT_FOLDER_2 = INPUT_DIR / "stack_quadrant_PALM_Tracer"


@pytest.fixture
def pt():
	"""fixture interne"""
	obj = PALMTracer()
	yield obj
	try: obj._logger.close()
	except Exception: pass


##################################################
def clean_output():
	"""Vide les dossiers de sorties."""
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
	shutil.rmtree(OUTPUT_FOLDER_2, ignore_errors=True)


##################################################
def check_output(folder: Path, csv: Optional[list[int]] = None, log: Optional[list[int]] = None, json: Optional[list[int]] = None,
				 tif: Optional[list[int]] = None, png: Optional[list[int]] = None, clean: bool = True):
	"""Vérifie si la sortie correspond à ce qui est attendu."""
	if not folder.is_dir(): pytest.fail("Dossier invalide.")

	for ext, v in {"csv": csv, "log": log, "json": json, "tif": tif, "png": png}.items():
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
	Vérifie dans le capsys les éléments activé ou non et la correspondance du nombre de lignes
	:param capsys:
	:param n_lines:
	:param steps:
	"""
	lines = get_lines_output(capsys)
	# for i in range(len(lines)): print(f"{i}: {lines[i]}")
	assert len(lines) == n_lines
	step_name = ["Localization", "Beads Extraction", "Tracking", "Blinking Reconnection", "Tracks Compute", "Gallery generation",
				 "Graphical visualization", "High-resolution visualization"]
	for i in range(8): assert step_name[i] in lines[steps[i]]


##################################################
def add_fakeprocess(pt: PALMTracer, localisation: bool, tracking: bool):
	OUTPUT_FOLDER.mkdir(exist_ok=True, parents=True)
	timestamp = "20260101_000000"
	if localisation:
		src = INPUT_DIR / "ref" / "stack-localizations-103.6_True_4_1.0_0.0_7.csv"
		dst = OUTPUT_FOLDER / f"localizations-{timestamp}.csv"
		shutil.copy2(src, dst)
		pt.settings.localization.active = True
	if tracking:
		src = INPUT_DIR / "ref" / "stack-tracking-103.6_True_4_1.0_0.0_7-5_2_10_0.5.csv"
		dst = OUTPUT_FOLDER / f"tracking-{timestamp}.csv"
		shutil.copy2(src, dst)
		pt.settings.tracking.active = True
	FileIO.save_json(OUTPUT_FOLDER / f"settings-{timestamp}.json", pt.settings.to_compact_dict())


##################################################
def test_reset_result(qtbot, capsys, pt):
	"""Test pour le process sans fichiers en entrée."""

	pt.df["loc"] = pd.DataFrame([1, 1])
	pt.df["dft"] = pd.DataFrame([1, 2])
	pt.df["bds"] = pd.DataFrame([1, 3])
	pt.df["blk"] = pd.DataFrame([1, 4])
	pt.df["trc"] = pd.DataFrame([1, 5])
	pt.df["MSD"] = pd.DataFrame([1, 6])
	pt.df["InD"] = pd.DataFrame([1, 7])
	pt.df["Fit"] = pd.DataFrame([1, 8])
	pt.df["f_loc"] = pd.DataFrame([1, 9])
	pt.df["f_blk"] = pd.DataFrame([1, 10])
	pt.df["f_trc"] = pd.DataFrame([1, 11])
	pt.df["f_MSD"] = pd.DataFrame([1, 12])
	pt.df["f_InD"] = pd.DataFrame([1, 13])
	pt.df["f_Fit"] = pd.DataFrame([1, 14])

	pt.reset_result()
	for key in pt.df:
		assert pt.df[key].empty, "Le Dataframe devrait être vide."


# ==================================================
# region Getter / Setter
# ==================================================
##################################################
def test_getter_localization(qtbot, pt):
	"""Test pour le getter de la localisation."""
	res = pt.localizations
	assert res.empty, "Le Dataframe devrait être vide."
	ref1 = pd.DataFrame([1, 2])
	ref2 = pd.DataFrame([3, 4])
	ref3 = pd.DataFrame([5, 6])
	pt.df["f_loc"] = ref1
	res = pt.localizations
	assert res.equals(ref1), f"Résultat incorrect.\nAttendu : {ref1}\tObtenu : {res}"
	pt.df["dft"] = ref2
	res = pt.localizations
	assert res.equals(ref2), f"Résultat incorrect.\nAttendu : {ref2}\tObtenu : {res}"
	pt.df["f_dft"] = ref3
	res = pt.localizations
	assert res.equals(ref3), f"Résultat incorrect.\nAttendu : {ref3}\tObtenu : {res}"
	pt.reset_filtered()
	res = pt.localizations
	assert res.equals(ref2), f"Résultat incorrect.\nAttendu : {ref2}\tObtenu : {res}"


##################################################
def test_getter_beads(qtbot, pt):
	"""Test pour le getter de la localisation."""
	res = pt.beads
	assert res.empty, "Le Dataframe devrait être vide."
	ref1 = pd.DataFrame([1, 2])
	pt.df["bds"] = ref1
	res = pt.beads
	assert res.equals(ref1), f"Résultat incorrect.\nAttendu : {ref1}\tObtenu : {res}"


##################################################
def test_getter_tracks(qtbot, pt):
	"""Test pour le process sans fichiers en entrée."""
	res = pt.tracks
	assert res.empty, "Le Dataframe devrait être vide."
	ref1 = pd.DataFrame([1, 2])
	ref2 = pd.DataFrame([3, 4])
	ref3 = pd.DataFrame([5, 6])
	pt.df["f_trc"] = ref1
	res = pt.tracks
	assert res.equals(ref1), f"Résultat incorrect.\nAttendu : {ref1}\tObtenu : {res}"
	pt.df["blk"] = ref2
	res = pt.tracks
	assert res.equals(ref2), f"Résultat incorrect.\nAttendu : {ref2}\tObtenu : {res}"
	pt.df["f_blk"] = ref3
	res = pt.tracks
	assert res.equals(ref3), f"Résultat incorrect.\nAttendu : {ref3}\tObtenu : {res}"
	pt.reset_filtered()
	res = pt.tracks
	assert res.equals(ref2), f"Résultat incorrect.\nAttendu : {ref2}\tObtenu : {res}"


##################################################
def test_getter_tracks_compute(qtbot, pt):
	"""Test pour le process sans fichiers en entrée."""
	df = pt.tracks_compute
	assert df["MSD"].empty, "Le Dataframe devrait être vide."
	ref1 = pd.DataFrame([1, 2])
	pt.df["f_MSD"] = ref1
	df = pt.tracks_compute
	assert df["MSD"].equals(ref1), "Le Dataframe devrait non vide."


##################################################
def test_get_status(qtbot, pt):
	# Etat initial
	ref = {"Localization": FILE_STATUS[0], "Beads": FILE_STATUS[0], "Tracking": FILE_STATUS[0],
		   "MSD":          FILE_STATUS[0], "Instant D": FILE_STATUS[0], "Fit": FILE_STATUS[0]}
	res = pt.get_status()
	for key in res: assert res[key] == ref[key], f"Status incorrect.\nAttendu : {ref}\nObtenu : {res}"

	# Intégralité des dataframes remplis
	pt.df["loc"] = pd.DataFrame([1, 1])
	pt.df["dft"] = pd.DataFrame([1, 2])
	pt.df["bds"] = pd.DataFrame([1, 3])
	pt.df["trc"] = pd.DataFrame([1, 4])
	pt.df["blk"] = pd.DataFrame([1, 5])
	pt.df["MSD"] = pd.DataFrame([1, 6])
	pt.df["InD"] = pd.DataFrame([1, 7])
	pt.df["Fit"] = pd.DataFrame([1, 8])
	pt.df["f_loc"] = pd.DataFrame([2, 1])
	pt.df["f_dft"] = pd.DataFrame([2, 2])
	pt.df["f_trc"] = pd.DataFrame([2, 3])
	pt.df["f_blk"] = pd.DataFrame([2, 4])
	pt.df["f_MSD"] = pd.DataFrame([2, 5])
	pt.df["f_InD"] = pd.DataFrame([2, 6])
	pt.df["f_Fit"] = pd.DataFrame([2, 7])
	ref = {"Localization": FILE_STATUS[6], "Beads": FILE_STATUS[1], "Tracking": FILE_STATUS[4],
		   "MSD":          FILE_STATUS[2], "Instant D": FILE_STATUS[2], "Fit": FILE_STATUS[2]}
	res = pt.get_status()
	for key in res: assert res[key] == ref[key], f"Status incorrect.\nAttendu : {ref}\nObtenu : {res}"

	# Suppression des filtres pour les tracks compute, les reconnexions et corrections filtrées
	pt.df["f_dft"] = pd.DataFrame()
	pt.df["f_blk"] = pd.DataFrame()
	pt.df["f_MSD"] = pd.DataFrame()
	pt.df["f_InD"] = pd.DataFrame()
	pt.df["f_Fit"] = pd.DataFrame()
	ref = {"Localization": FILE_STATUS[5], "Beads": FILE_STATUS[1], "Tracking": FILE_STATUS[3],
		   "MSD":          FILE_STATUS[1], "Instant D": FILE_STATUS[1], "Fit": FILE_STATUS[1]}
	res = pt.get_status()
	for key in res: assert res[key] == ref[key], f"Status incorrect.\nAttendu : {ref}\nObtenu : {res}"

	# Suppression des reconnexions et corrections
	pt.df["dft"] = pd.DataFrame()
	pt.df["blk"] = pd.DataFrame()
	ref = {"Localization": FILE_STATUS[2], "Beads": FILE_STATUS[1], "Tracking": FILE_STATUS[2],
		   "MSD":          FILE_STATUS[1], "Instant D": FILE_STATUS[1], "Fit": FILE_STATUS[1]}
	res = pt.get_status()
	for key in res: assert res[key] == ref[key], f"Status incorrect.\nAttendu : {ref}\nObtenu : {res}"

	# Suppression des localisations et suivi filtrés
	pt.df["f_loc"] = pd.DataFrame()
	pt.df["f_trc"] = pd.DataFrame()
	ref = {"Localization": FILE_STATUS[1], "Beads": FILE_STATUS[1], "Tracking": FILE_STATUS[1],
		   "MSD":          FILE_STATUS[1], "Instant D": FILE_STATUS[1], "Fit": FILE_STATUS[1]}
	res = pt.get_status()
	for key in res: assert res[key] == ref[key], f"Status incorrect.\nAttendu : {ref}\nObtenu : {res}"


##################################################
def test_getter_path(qtbot, pt):
	"""Test pour le process sans fichiers en entrée."""
	res = pt.path
	assert res == ""


##################################################
def test_getter_stack(qtbot, pt):
	"""Test pour le process sans fichiers en entrée."""
	res = pt.stack
	assert res is None


##################################################
def test_getter_suffix(qtbot, pt):
	"""Test pour le process sans fichiers en entrée."""
	res = pt.suffix
	assert res == ""


# ==================================================
# endregion Getter / Setter
# ==================================================

# ==================================================
# region Process
# ==================================================
##################################################
def test_load_bad_dll(qtbot, capsys, pt):
	"""Test pour le process avec tous les éléments à False et aucun fichier chargeable."""
	pt.palm._dll = None
	pt.load("")
	lines = get_lines_output(capsys)
	assert "Process not completed due to missing DLLs." in lines[0]


##################################################
def test_load_nothing(qtbot, capsys, pt):
	"""Test pour le chargement avec fichier, mais sans settings."""
	pt.load("bad path")
	lines = get_lines_output(capsys)
	assert "No valid settings file to load." in lines[0]


##################################################
def test_load(qtbot, capsys, pt):
	"""Test pour le chargement avec fichier, mais sans settings."""
	clean_output()

	# Process initial
	add_basic_file(pt)
	pt.settings.localization.active = True
	pt.process()
	assert len(pt.df["loc"]) == 455
	check_capsys(capsys, 16, [5, 7, 8, 9, 10, 11, 12, 13])
	# Chargement
	pt.load()

	assert not pt.df["loc"].empty, "Le Dataframe de localization ne devrait pas être vide"
	assert pt.df["f_loc"].empty, "Le Dataframe de localizations filtré devrait être vide."

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

	# Un fichier meta + un localization
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1])


##################################################
def test_process_no_input(qtbot, capsys, pt):
	"""Test pour le process sans fichiers en entrée."""
	clean_output()
	pt.process()
	assert pt.df["loc"].empty, "Le Dataframe de localization ne devrait pas être vide"
	lines = get_lines_output(capsys)
	assert "No files." in lines[0]


##################################################
def test_process_nothing(qtbot, capsys, pt):
	"""Test pour le process avec tous les éléments à False et aucun fichier chargeable."""
	clean_output()

	add_basic_file(pt)
	pt.process()
	assert pt.df["loc"].empty, "Le Dataframe de localization ne devrait pas être vide"
	check_capsys(capsys, 15, [5, 6, 7, 8, 9, 10, 11, 12])
	check_output(OUTPUT_FOLDER, csv=[1], log=[1], json=[1])

	# Test d'une visualisation sans données.
	pt.settings.gallery.active = True
	pt.settings.visualization_hr.active = True
	pt.settings.visualization_graph.active = True
	pt.process()  # Test d'une visualisation sans données.
	assert pt.df["loc"].empty, "Le Dataframe de localization ne devrait pas être vide"
	check_capsys(capsys, 18, [5, 6, 7, 8, 9, 10, 12, 14])
	check_output(OUTPUT_FOLDER, csv=[1], log=[1], json=[1])

	pt.settings.visualization_hr["Type"].value = 1
	pt.process()
	assert pt.df["loc"].empty, "Le Dataframe de localization devrait être vide"
	check_capsys(capsys, 18, [5, 6, 7, 8, 9, 10, 12, 14])
	check_output(OUTPUT_FOLDER, csv=[1], log=[1], json=[1])

	# Test d'un calcul sur trajectoires sans données.
	pt.settings.gallery.active = False
	pt.settings.visualization_hr.active = False
	pt.settings.visualization_graph.active = False
	pt.settings.tracks_compute.active = True
	pt.process()
	assert pt.df["loc"].empty, "Le Dataframe de localization devrait être vide"
	check_capsys(capsys, 16, [5, 6, 7, 8, 9, 11, 12, 13])
	check_output(OUTPUT_FOLDER, csv=[1], log=[1], json=[1])

	# Test d'un calcul de reconnexion de trajectoires sans données.
	pt.settings.tracks_compute.active = False
	pt.settings.blinking.active = True
	pt.process()
	assert pt.df["loc"].empty, "Le Dataframe de localization devrait être vide"
	check_capsys(capsys, 16, [5, 6, 7, 8, 10, 11, 12, 13])
	check_output(OUTPUT_FOLDER, csv=[1], log=[1], json=[1])

	# Test d'un calcul de trajectoires sans données.
	pt.settings.blinking.active = False
	pt.settings.tracking.active = True
	pt.process()
	assert pt.df["loc"].empty, "Le Dataframe de localization devrait être vide"
	check_capsys(capsys, 16, [5, 6, 7, 9, 10, 11, 12, 13])
	check_output(OUTPUT_FOLDER, csv=[1], log=[1], json=[1])

	# Test d'un calcul de correction de drift sans données.
	pt.settings.tracking.active = False
	pt.settings.beads.active = True
	pt.process()
	assert pt.df["loc"].empty, "Le Dataframe de localization devrait être vide"
	check_capsys(capsys, 16, [5, 6, 8, 9, 10, 11, 12, 13])
	check_output(OUTPUT_FOLDER, csv=[1], log=[1], json=[1])


##################################################
def test_process_bad_dll(qtbot, capsys, pt):
	"""Test pour le process avec tous les éléments à False et aucun fichier chargeable."""
	pt.palm._dll = None
	pt.process()

	lines = get_lines_output(capsys)
	assert "Process not completed due to missing DLLs." in lines[0]


##################################################
def test_process_multiple_stack(qtbot, capsys, pt):
	"""Test pour le process avec plusieurs piles."""
	clean_output()

	add_basic_file(pt, [f"{INPUT_DIR}/stack.tif", f"{INPUT_DIR}/stack_quadrant.tif"])
	pt.settings.batch["Mode"].value = 1
	pt.process()

	check_output(OUTPUT_FOLDER, csv=[1], log=[1], json=[1])
	check_output(OUTPUT_FOLDER_2, csv=[1], log=[1], json=[1])
	# (2*21 lignes dans le cas d'aucun process)
	check_capsys(capsys, 30, [5, 6, 7, 8, 9, 10, 11, 12])


##################################################
def test_process_localization(qtbot, capsys, pt):
	"""Test pour le process de localisation."""
	clean_output()

	add_basic_file(pt)
	pt.settings.localization.active = True
	pt.process()

	assert len(pt.df["loc"]) == 455
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1])
	check_capsys(capsys, 16, [5, 7, 8, 9, 10, 11, 12, 13])


##################################################
def test_process_localization_z(qtbot, capsys, pt):
	"""Test pour le process de localisation."""
	clean_output()

	add_basic_file(pt)
	pt.settings.localization.active = True
	pt.settings.localization["Fit"].value = 1
	s = pt.settings.localization["Gaussian Fit"]
	s["Mode"].value = 2
	s["Z"].value = True
	pt.process()  # Lancement, mais aucun fichier de model.

	assert len(pt.df["loc"]) == 455
	assert np.allclose(pt.df["loc"]["Z"].to_numpy(), 0)
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1])
	check_capsys(capsys, 17, [5, 8, 9, 10, 11, 12, 13, 14])

	s["Model"].value = str(REF_DIR / "astigmatism_3d_model.csv")
	pt.process()  # Lancement

	assert len(pt.df["loc"]) == 455
	assert not np.allclose(pt.df["loc"]["Z"].to_numpy(), 0)
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1])
	check_capsys(capsys, 16, [5, 7, 8, 9, 10, 11, 12, 13])


##################################################
def test_process_localization_spline_bad(qtbot, capsys, pt):
	"""Test pour le process de localisation."""
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
def test_process_localization_spline(qtbot, capsys, pt):
	"""Test pour le process de localisation."""
	clean_output()

	add_basic_file(pt)
	pt.settings.localization.active = True
	pt.settings.localization["Fit"].value = 2
	pt.settings.localization["Spline Fit"]["File"].value = f"{INPUT_DIR}/calibration.mat"
	pt.process()

	assert len(pt.df["loc"]) == 455
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1])
	check_capsys(capsys, 16, [5, 7, 8, 9, 10, 11, 12, 13])


##################################################
def test_process_beads_extraction_no_beads(qtbot, capsys, pt):
	"""Test pour le process de l'extraction des billes."""
	clean_output()

	add_basic_file(pt)
	pt.settings.localization.active = True
	pt.settings.beads.active = True
	pt.process()

	assert len(pt.df["loc"]) == 455
	assert pt.df["bds"].empty
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1])
	check_capsys(capsys, 17, [5, 7, 9, 10, 11, 12, 13, 14])


##################################################
def test_process_plane_discontinuous(qtbot, capsys, pt):
	"""Test pour le process de l'extraction des billes."""
	clean_output()

	src = INPUT_DIR / "localizations.csv"
	pt.df["loc"] = pd.read_csv(src)
	pt.df["loc"].loc[1, "Plane"] = 5
	pt._beads_extraction()
	assert pt.df["bds"].empty
	lines = get_lines_output(capsys)
	assert "No beads found." in lines[0]


##################################################
def test_process_beads_extraction(qtbot, capsys, pt):
	"""Test pour le process de l'extraction des billes."""
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

	assert len(pt.df["bds"]) == 4  # 2 Billes sur 2 plans
	check_output(OUTPUT_FOLDER, csv=[3], log=[1], json=[1])
	check_capsys(capsys, 17, [5, 7, 9, 10, 11, 12, 13, 14])


##################################################
def test_process_tracking(qtbot, capsys, pt):
	"""Test pour le process de tracking."""
	clean_output()

	add_basic_file(pt)
	add_fakeprocess(pt, True, False)  # Ajout d'un fichier de localisations

	pt.settings.tracking.active = True
	pt.process()

	ref = pt.localizations
	ref = ref[ref["Integrated Intensity"] > 0]  # Suppression des éléments où la colonne "Integrated Intensity" est inférieure à 0 (l'ajustement a échoué).

	assert len(ref) == len(pt.tracks), "Nombre de points différents entre la localization et le tracking."
	check_output(OUTPUT_FOLDER, csv=[3], log=[1], json=[1])
	check_capsys(capsys, 17, [5, 7, 8, 10, 11, 12, 13, 14])


##################################################
def test_process_tracking_blinking(qtbot, capsys, pt):
	"""Test pour le process de tracking."""
	clean_output()

	add_basic_file(pt)
	add_fakeprocess(pt, False, True)  # Ajout d'un fichier de Tracking

	pt.settings.blinking.active = True
	pt.process()

	assert len(pt.df["trc"]) == len(pt.df["blk"]), "Nombre de points différents entre la reconnexion et le tracking."
	check_output(OUTPUT_FOLDER, csv=[3], log=[1], json=[1])
	check_capsys(capsys, 17, [5, 6, 7, 9, 11, 12, 13, 14])


##################################################
def test_process_tracks_compute(qtbot, capsys, pt):
	"""Test pour le process de tracking."""
	clean_output()

	add_basic_file(pt)
	add_fakeprocess(pt, False, True)  # Ajout d'un fichier de Tracking

	tc = pt.settings.tracks_compute
	tc.active = True
	pt.process()

	# Aucun fichier Ajouté juste meta et le tracking copié
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1], clean=False)
	check_capsys(capsys, 17, [5, 6, 7, 9, 10, 12, 13, 14])

	tc["MSD"].value = True
	sleep(1)  # Force un timestamp différent pour le Reuse
	pt.process()
	assert len(pt.df["MSD"]) == 99  # Toutes les trajectoiers sont éligibles au MSD
	# Ajout de fichier MSD (ainsi qu'un meta, json et log)
	check_output(OUTPUT_FOLDER, csv=[3], log=[1], json=[1], clean=False)
	check_capsys(capsys, 19, [5, 6, 7, 9, 10, 14, 15, 16])

	tc["MSD"].value = False
	tc["Instant Diffusion"].value = True
	tc["Fit"].value = 1
	sleep(1)  # Force un timestamp différent pour le Reuse
	pt.process()
	assert len(pt.df["MSD"]) == 0  # MSD désactivé
	assert len(pt.df["InD"]) == 3  # Seules 3 trajectoires sont éligibles
	assert len(pt.df["Fit"]) == 3  # Seules 3 trajectoires sont éligibles
	check_output(OUTPUT_FOLDER, csv=[5], log=[2], json=[2])  # Il a conservé le msd precedent mais à renommé le meta
	check_capsys(capsys, 21, [5, 6, 7, 9, 10, 16, 17, 18])


##################################################
def test_process_gallery(qtbot, capsys, pt):
	"""Test pour le process de visualization HR."""
	clean_output()

	add_basic_file(pt)
	add_fakeprocess(pt, True, False)  # Ajout d'un fichier de localisations

	pt.settings.gallery.active = True
	pt.process()

	# dimension 270 (30 ROI / lignes(colonnes) * taille de ROI de 9) et 1 frame (30 * 30 = 900 / frame et environ 450 en entrée)
	res, ref = FileIO.open_tif(str(list(OUTPUT_FOLDER.glob("*.tif"))[0])).shape, (1, 270, 270)
	assert res == ref, f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1], tif=[1])
	check_capsys(capsys, 17, [5, 7, 8, 9, 10, 11, 13, 14])


##################################################
def test_process_visualization_graph(qtbot, capsys, pt):
	"""Test pour le process de visualization de graph."""
	clean_output()

	add_basic_file(pt)
	add_fakeprocess(pt, True, True)  # Ajout d'un fichier de localisations et de tracking

	pt.settings.visualization_graph.active = True
	pt.process()

	check_output(OUTPUT_FOLDER, csv=[3], log=[1], json=[1], png=[18])
	check_capsys(capsys, 37, [5, 7, 8, 10, 11, 12, 13, 34])


##################################################
def test_process_visualization_hr(qtbot, capsys, pt):
	"""Test pour le process de visualization HR."""
	clean_output()

	add_basic_file(pt)
	add_fakeprocess(pt, True, True)  # Ajout d'un fichier de localisations et de tracking

	pt.settings.visualization_hr.active = True
	pt.settings.visualization_hr["Source L"].value = 0
	pt.process()

	check_output(OUTPUT_FOLDER, csv=[3], log=[1], json=[1], png=[8], clean=False)
	check_capsys(capsys, 25, [5, 7, 8, 10, 11, 12, 13, 14])

	pt.settings.visualization_hr["Type"].value = 1
	pt.settings.visualization_hr["Source T"].value = 0
	sleep(1)  # Force un timestamp différent pour le Reuse
	pt.process()

	# Il a ajouté un fichier tracking_Fit qu'il a dû calculer et un tracking_hr_color, pour les images 8 Sources pour les loc, 5 pour les trajectoires.
	check_output(OUTPUT_FOLDER, csv=[5], log=[2], json=[2], png=[13])
	check_capsys(capsys, 27, [5, 7, 8, 10, 11, 12, 13, 14])


##################################################
def test_process_all(qtbot, capsys, pt):
	"""Test Basique pour le process complet."""
	clean_output()

	pt.settings.localization.active = True
	pt.settings.localization["Fit"].value = 1
	pt.settings.localization["Gaussian Fit"]["Mode"].value = 3
	pt.settings.beads.active = True
	pt.settings.tracking.active = True
	pt.settings.blinking.active = True
	pt.settings.tracks_compute.active = True
	pt.settings.tracks_compute["MSD"].value = True
	pt.settings.tracks_compute["Instant Diffusion"].value = True
	pt.settings.tracks_compute["Fit"].value = 1
	pt.settings.gallery.active = True
	pt.settings.visualization_hr.active = True
	pt.settings.visualization_graph.active = True
	add_basic_file(pt)
	pt.process()

	check_output(OUTPUT_FOLDER, csv=[7], log=[1], json=[1], tif=[1], png=[19])
	check_capsys(capsys, 49, [5, 8, 10, 12, 14, 22, 24, 45])


# ==================================================
# endregion Process
# ==================================================

# ==================================================
# region Filtering
# ==================================================
##################################################
def test_reset_filtered(qtbot, capsys, pt):
	"""Test pour la suppréssion des tableaux filtrés."""

	pt.df["loc"] = pd.DataFrame([1, 1])
	pt.df["dft"] = pd.DataFrame([1, 2])
	pt.df["bds"] = pd.DataFrame([1, 3])
	pt.df["blk"] = pd.DataFrame([1, 4])
	pt.df["trc"] = pd.DataFrame([1, 5])
	pt.df["MSD"] = pd.DataFrame([1, 6])
	pt.df["InD"] = pd.DataFrame([1, 7])
	pt.df["Fit"] = pd.DataFrame([1, 8])
	pt.df["f_loc"] = pd.DataFrame([1, 9])
	pt.df["f_blk"] = pd.DataFrame([1, 10])
	pt.df["f_trc"] = pd.DataFrame([1, 11])
	pt.df["f_MSD"] = pd.DataFrame([1, 12])
	pt.df["f_InD"] = pd.DataFrame([1, 13])
	pt.df["f_Fit"] = pd.DataFrame([1, 14])

	pt.reset_filtered()
	for key in pt.df:
		if key.startswith("f_"): assert pt.df[key].empty, "Le Dataframe devrait être vide."
		else: assert not pt.df[key].empty, "Le Dataframe doit subsiter."


##################################################
def test_update_filtered(qtbot, capsys, pt):
	"""Test pour la mise à jour des tableaux filtrés."""
	clean_output()
	pt.update_filtered()  # Tout est vide
	pt.settings.filters["Save"].value = True
	pt.update_filtered()  # Tout est vide, mais je demande à enregistrer

	add_basic_file(pt)
	add_fakeprocess(pt, True, False)  # Ajout d'un fichier de localisations et de tracking

	pt.process()
	pt.update_filtered()  # Maintenant, il va recalculer les filtres (il n'y en aura aucun de toute façon).
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1])  # Il n'a rien enregistré, car les filtres n'ont pas fait de changement.


##################################################
def test_save_filtered(qtbot, capsys, pt):
	"""Test pour la mise à jour des tableaux filtrés."""
	clean_output()
	pt._path = OUTPUT_DIR
	pt.update_filtered()  # Tout est vide
	pt.settings.filters["Save"].value = True
	pt.update_filtered()  # Tout est vide, mais je demande à enregistrer

	add_basic_file(pt)
	add_fakeprocess(pt, True, False)  # Ajout d'un fichier de localisations et de tracking

	pt.df["loc"] = pd.read_csv(INPUT_DIR / "ref" / "stack-localizations-103.6_True_4_1.0_0.0_7.csv")
	pt.settings.filters["Plane"].active = True
	pt.settings.filters["Plane"].value = [2, 3]
	pt.update_filtered()  # Il va recalculer les filtres.
	check_output(OUTPUT_FOLDER, csv=[1])  # Il a enregistré la version filtrée.


##################################################
def test_filter_localization(qtbot, capsys, pt):
	"""Test pour le filtrage complet lors de l'exécution."""
	clean_output()

	add_basic_file(pt)
	add_fakeprocess(pt, True, False)  # Ajout d'un fichier de localisations et de tracking

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
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1], clean=False)  # Il n'a pas enregistré le resultat du filtre
	check_capsys(capsys, 17, [5, 8, 9, 10, 11, 12, 13, 14])

	pt.settings.filters["Save"].value = True
	sleep(1)  # Force un timestamp différent pour le Reuse
	pt.process()  # Second passage avec enregistrement
	check_output(OUTPUT_FOLDER, csv=[3], log=[1], json=[1])
	check_capsys(capsys, 18, [5, 9, 10, 11, 12, 13, 14, 15])


##################################################
def test_filter_tracks_compute(qtbot, capsys, pt):
	"""Test pour le filtrage complet lors de l'exécution."""
	clean_output()

	add_basic_file(pt)
	add_fakeprocess(pt, False, True)  # Ajout d'un fichier de tracking

	pt.settings.tracks_compute.active = True
	pt.settings.tracks_compute["MSD"].value = True
	pt.settings.tracks_compute["Instant Diffusion"].value = True
	pt.settings.tracks_compute["Fit"].value = 1
	pt.settings.tracks_compute["Fit Length"].value = 2

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

	check_output(OUTPUT_FOLDER, csv=[5], log=[1], json=[1], clean=False)  # Il n'a pas enregistré le resultat du filtre
	check_capsys(capsys, 21, [5, 6, 7, 10, 11, 16, 17, 18])

	pt.settings.filters["Save"].value = True
	sleep(1)  # Force un timestamp différent pour le Reuse
	pt.process()
	# Vérification manuelle à l'heure actuelle
	assert len(pt.tracks) == 26, f"Il reste {len(pt.tracks)} points au lieu de 26 sur les trajectoires."
	assert len(pt.tracks_compute["MSD"]) == 6, f"Il reste {len(pt.tracks_compute['MSD'])} trajectoires au lieu de 14."

	check_output(OUTPUT_FOLDER, csv=[9], log=[1], json=[1], clean=False)  # Track + 2 tracks computes, leurs versions filtrées et le meta = 9
	check_capsys(capsys, 26, [5, 6, 7, 11, 12, 21, 22, 23])

	# Filtre massif plus rien à la sortie
	pt.settings.filters["Tracks"]["Length"].value = [42, 10000]
	sleep(1)  # Force un timestamp différent pour le Reuse
	pt.process()
	assert len(pt.df["f_trc"]) == 0, f"Il reste {len(pt.tracks)} points au lieu de 0 sur les trajectoires."
	assert len(pt.df["f_MSD"]) == 0, f"Il reste {len(pt.tracks_compute['MSD'])} trajectoires au lieu de 0."
	check_output(OUTPUT_FOLDER, csv=[9], log=[2], json=[2])  # Il ne va pas réenregistrer les éléments filtrés
	check_capsys(capsys, 21, [5, 6, 7, 10, 11, 16, 17, 18])


# ==================================================
# endregion Filtering
# ==================================================

##################################################
def test_add_color(qtbot, capsys, pt):
	file = "tracking2"
	path = Path(f"{INPUT_DIR}/{file}.csv")
	df = pd.read_csv(path)
	pt._path = OUTPUT_DIR

	ref = [1, 1, 1, 1, 1, 1]
	res = pt.add_color_to_tracks(df, "Track Number")  # Premier exemple basique
	assert (res["Color"].tolist() == ref)
	res = pt.add_color_to_tracks(df, "Length")  # Exemple basique avec erreur de calcul
	assert (res["Color"].tolist() == ref)

	pt.df["trc"] = df
	ref = [32767, 32767, 32767, 32767, 32767, 32767]
	res = pt.add_color_to_tracks(df, "Length")  # fit Compute but equality
	assert (res["Color"].tolist() == ref)

	# Changement des valeurs pour permettre le calcul
	pt.reset_result()
	df.loc[df.index[-3:], "Track"] = 2
	pt.df["trc"] = df
	pt.settings.tracks_compute["Fit Length"].value = 2

	ref = [1, 1, 1, 65535, 65535, 65535]
	res = pt.add_color_to_tracks(df, "Total Intensity")  # fit Compute
	assert (res["Color"].tolist() == ref)

	res = pt.add_color_to_tracks(df, "Total Intensity")  # fit Compute already compute
	assert (res["Color"].tolist() == ref)

	lines = get_lines_output(capsys)
	assert len(lines) == 16  # Beaucoup de warnings dû à l'ajout dans un logger non ouvert


##################################################
def test_get_astigmatism_model(qtbot, capsys, pt):
	tmp_output = OUTPUT_DIR / "Model"
	shutil.rmtree(tmp_output, ignore_errors=True)
	tmp_output.mkdir(parents=True, exist_ok=True)
	model_file = "astigmatism_3d_model.csv"
	ref = pd.read_csv(REF_DIR / model_file, index_col=0)
	(tmp_output / model_file).unlink(missing_ok=True)
	(tmp_output.parent / model_file).unlink(missing_ok=True)

	pt._path = tmp_output

	model = pt._get_astigmatism_model(Path(""))  # Il ne va pas reussir, il n'a aucun fichier
	assert model.empty

	shutil.copy2(REF_DIR / model_file, tmp_output.parent / model_file)
	model = pt._get_astigmatism_model(Path(""))  # Il va reussir, dnas le dernier dossier par défaut
	assert np.allclose(model.to_numpy(), ref.to_numpy(), atol=1e-6)

	shutil.copy2(REF_DIR / model_file, tmp_output / model_file)
	model = pt._get_astigmatism_model(Path(""))  # Il va reussir, dnas le premier dossier par défaut
	assert np.allclose(model.to_numpy(), ref.to_numpy(), atol=1e-6)

	model = pt._get_astigmatism_model(REF_DIR / model_file)  # Il va reussir, dans le chemin donné
	assert np.allclose(model.to_numpy(), ref.to_numpy(), atol=1e-6)
