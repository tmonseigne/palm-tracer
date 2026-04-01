"""
Fichier des tests pour la classe PALMTracer

.. note:: Il est fréquent que la vérificaiton du log ne se fasse qu'au nombre de lignes, car au moins 15 lignes à chaque process.
"""
import shutil

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
def check_capsys(capsys, n_lines: int, steps: list[tuple[bool, int]]):
	"""
	Vérifie dans le capsys les éléments activé ou non et la correspondance du nombre de lignes
	:param capsys:
	:param n_lines:
	:param steps:
	"""
	lines = get_lines_output(capsys)
	# for i in range(len(lines)): print(f"{i}: {lines[i]}")
	assert len(lines) == n_lines
	step_name = ["Localization", "Beads Extraction", "Tracking", "Blinking Reconnection", "Tracks Computes",
				 "High-resolution visualization", "Graphical visualization", "Gallery generation"]
	for i in range(8):
		status, line = steps[i]
		status_str = "enabled" if status else "disabled"
		assert re.fullmatch(TS_PATTERN + rf"\s{step_name[i]} {status_str}\.", lines[line])


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
	check_capsys(capsys, 21, [(True, 5), (False, 7), (False, 9), (False, 11), (False, 12), (False, 16), (False, 17), (False, 18)])

	# Chargement
	pt.load()

	assert not pt.df["loc"].empty, "Le Dataframe de localization ne devrait pas être vide"
	assert pt.df["f_loc"].empty, "Le Dataframe de localizations filtré devrait être vide."

	# Un fichier meta + un localization
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1])

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


##################################################
def test_process_no_input(qtbot, capsys, pt):
	"""Test pour le process sans fichiers en entrée."""
	clean_output()
	pt.process()
	lines = get_lines_output(capsys)
	assert "No files." in lines[0]


##################################################
def test_process_nothing(qtbot, capsys, pt):
	"""Test pour le process avec tous les éléments à False et aucun fichier chargeable."""
	clean_output()

	add_basic_file(pt)
	pt.process()
	check_capsys(capsys, 21, [(False, 5), (False, 7), (False, 9), (False, 11), (False, 12), (False, 16), (False, 17), (False, 18)])

	# Test d'une visualisation sans données.
	pt.settings.gallery.active = True
	pt.settings.visualization_hr.active = True
	pt.settings.visualization_graph.active = True
	pt.process()  # Test d'une visualisation sans données.
	check_capsys(capsys, 24, [(False, 5), (False, 7), (False, 9), (False, 11), (False, 12), (True, 16), (True, 18), (True, 20)])

	pt.settings.visualization_hr["Type"].value = 1
	pt.process()
	check_capsys(capsys, 24, [(False, 5), (False, 7), (False, 9), (False, 11), (False, 12), (True, 16), (True, 18), (True, 20)])

	# Test d'un calcul sur trajectoires sans données.
	pt.settings.gallery.active = False
	pt.settings.visualization_hr.active = False
	pt.settings.visualization_graph.active = False
	pt.settings.tracks_compute.active = True
	pt.process()
	check_capsys(capsys, 19, [(False, 5), (False, 7), (False, 9), (False, 11), (True, 12), (False, 14), (False, 15), (False, 16)])

	# Test d'un calcul de reconnexion de trajectoires sans données.
	pt.settings.tracks_compute.active = False
	pt.settings.blinking.active = True
	pt.process()
	check_capsys(capsys, 22, [(False, 5), (False, 7), (False, 9), (True, 11), (False, 13), (False, 17), (False, 18), (False, 19)])

	# Test d'un calcul de trajectoires sans données.
	pt.settings.blinking.active = False
	pt.settings.tracking.active = True
	pt.process()
	check_capsys(capsys, 21, [(False, 5), (False, 7), (True, 9), (False, 11), (False, 12), (False, 16), (False, 17), (False, 18)])

	# Test d'un calcul de correction de drift sans données.
	pt.settings.tracking.active = False
	pt.settings.beads.active = True
	pt.process()
	check_capsys(capsys, 21, [(False, 5), (True, 7), (False, 9), (False, 11), (False, 12), (False, 16), (False, 17), (False, 18)])

	n_process = 7  # Nombre de fois où process a été lancé.
	# suivant le timestamp, il est fort problable que seul le dernier process conserve ses data, mais le hasard du lancement fait que
	# chaque process peut démarrer avec une seconde de décallage et donc un timestamp différent.
	check_output(OUTPUT_FOLDER, csv=[1, n_process], log=[1, n_process], json=[1, n_process])


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
	check_capsys(capsys, 42, [(False, 5), (False, 7), (False, 9), (False, 11), (False, 12), (False, 16), (False, 17), (False, 18)])


##################################################
def test_process_only_localization(qtbot, capsys, pt):
	"""Test pour le process de localisation."""
	clean_output()

	add_basic_file(pt)
	pt.settings.localization.active = True
	pt.process()

	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1])
	check_capsys(capsys, 21, [(True, 5), (False, 7), (False, 9), (False, 11), (False, 12), (False, 16), (False, 17), (False, 18)])


##################################################
def test_process_only_localization_spline_bad(qtbot, capsys, pt):
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
def test_process_only_localization_spline(qtbot, capsys, pt):
	"""Test pour le process de localisation."""
	clean_output()

	add_basic_file(pt)
	pt.settings.localization.active = True
	pt.settings.localization["Fit"].value = 2
	pt.settings.localization["Spline Fit"]["File"].value = f"{INPUT_DIR}/calibration.mat"
	pt.process()

	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1])
	check_capsys(capsys, 21, [(True, 5), (False, 7), (False, 9), (False, 11), (False, 12), (False, 16), (False, 17), (False, 18)])


##################################################
def test_process_only_beads_extraction_no_beads(qtbot, capsys, pt):
	"""Test pour le process de l'extraction des billes."""
	clean_output()

	OUTPUT_FOLDER.mkdir(exist_ok=True, parents=True)
	src = INPUT_DIR / "ref" / "stack-localizations-103.6_True_4_1.0_0.0_7.csv"
	dst = OUTPUT_FOLDER / f"localizations-{FileIO.get_timestamp_for_files()}.csv"
	shutil.copy2(src, dst)

	add_basic_file(pt)
	pt.settings.beads.active = True
	pt.process()

	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1])
	check_capsys(capsys, 22, [(False, 5), (True, 8), (False, 10), (False, 12), (False, 13), (False, 17), (False, 18), (False, 19)])


##################################################
def test_process_only_beads_extraction(qtbot, capsys, pt):
	"""Test pour le process de l'extraction des billes."""
	clean_output()

	OUTPUT_FOLDER.mkdir(exist_ok=True, parents=True)
	src = INPUT_DIR / "localizations.csv"
	dst = OUTPUT_FOLDER / f"localizations-{FileIO.get_timestamp_for_files()}.csv"
	shutil.copy2(src, dst)

	add_basic_file(pt)
	pt.settings.beads.active = True
	pt.process()

	assert len(pt.df["bds"]) == 4  # 2 Billes sur 2 plans
	check_output(OUTPUT_FOLDER, csv=[3], log=[1], json=[1])
	check_capsys(capsys, 22, [(False, 5), (True, 8), (False, 10), (False, 12), (False, 13), (False, 17), (False, 18), (False, 19)])


##################################################
def test_process_only_tracking(qtbot, capsys, pt):
	"""Test pour le process de tracking."""
	clean_output()

	# Ajout d'un fichier de localisations
	OUTPUT_FOLDER.mkdir(exist_ok=True, parents=True)
	src = INPUT_DIR / "ref" / "stack-localizations-103.6_True_4_1.0_0.0_7.csv"
	dst = OUTPUT_FOLDER / f"localizations-{FileIO.get_timestamp_for_files()}.csv"
	shutil.copy2(src, dst)

	pt.settings.tracking.active = True
	add_basic_file(pt)
	pt.process()
	ref = pt.localizations
	ref = ref[ref["Integrated Intensity"] > 0]  # Suppression des éléments où la colonne "Integrated Intensity" est inférieure à 0 (l'ajustement a échoué).

	assert len(ref) == len(pt.tracks), "Nombre de points différents entre la localization et le tracking."
	check_output(OUTPUT_FOLDER, csv=[3], log=[1], json=[1])
	check_capsys(capsys, 22, [(False, 5), (False, 8), (True, 10), (False, 12), (False, 13), (False, 17), (False, 18), (False, 19)])


##################################################
def test_process_only_tracking_blinking(qtbot, capsys, pt):
	"""Test pour le process de tracking."""
	clean_output()

	# Ajout d'un fichier de localisations
	OUTPUT_FOLDER.mkdir(exist_ok=True, parents=True)
	src = INPUT_DIR / "ref" / "stack-tracking-103.6_True_4_1.0_0.0_7-5_2_10_0.5.csv"
	dst = OUTPUT_FOLDER / f"tracking-{FileIO.get_timestamp_for_files()}.csv"
	shutil.copy2(src, dst)

	pt.settings.blinking.active = True
	add_basic_file(pt)
	pt.process()

	check_output(OUTPUT_FOLDER, csv=[3], log=[1], json=[1])
	check_capsys(capsys, 23, [(False, 5), (False, 7), (False, 9), (True, 12), (False, 14), (False, 18), (False, 19), (False, 20)])


##################################################
def test_process_only_tracks_compute(qtbot, capsys, pt):
	"""Test pour le process de tracking."""
	clean_output()

	# Ajout d'un fichier de tracking
	OUTPUT_FOLDER.mkdir(exist_ok=True, parents=True)
	src = INPUT_DIR / "ref" / "stack-tracking-103.6_True_4_1.0_0.0_7-5_2_10_0.5.csv"
	dst = OUTPUT_FOLDER / f"tracking-{FileIO.get_timestamp_for_files()}.csv"
	shutil.copy2(src, dst)

	tc = pt.settings.tracks_compute
	tc.active = True
	add_basic_file(pt)

	pt.process()
	# Aucun fichier Ajouté juste meta et le tracking copié
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1], clean=False)
	check_capsys(capsys, 20, [(False, 5), (False, 7), (False, 9), (False, 12), (True, 13), (False, 15), (False, 16), (False, 17)])

	tc["MSD"].value = True
	pt.process()
	# Ajout de fichier MSD (et peut être un meta, json et log)
	check_output(OUTPUT_FOLDER, csv=[3, 4], log=[1, 2], json=[1, 2], clean=False)
	check_capsys(capsys, 22, [(False, 5), (False, 7), (False, 9), (False, 12), (True, 13), (False, 17), (False, 18), (False, 19)])

	tc["MSD"].value = False
	tc["Instant Diffusion"].value = True
	tc["Fit"].value = 1
	pt.process()
	# Ajout de fichier 2 ou 3 fichiers csv et 0 ou 1 fichiers meta, json et log
	check_output(OUTPUT_FOLDER, csv=[5, 7], log=[1, 3], json=[1, 3])
	check_capsys(capsys, 24, [(False, 5), (False, 7), (False, 9), (False, 12), (True, 13), (False, 19), (False, 20), (False, 21)])


##################################################
def test_process_only_visualization_hr(qtbot, capsys, pt):
	"""Test pour le process de visualization HR."""
	clean_output()

	# Ajout des fichiers de localisations et trajectoires
	OUTPUT_FOLDER.mkdir(exist_ok=True, parents=True)
	src = INPUT_DIR / "ref" / "stack-localizations-103.6_True_4_1.0_0.0_7.csv"
	dst = OUTPUT_FOLDER / f"localizations-{FileIO.get_timestamp_for_files()}.csv"
	shutil.copy2(src, dst)
	src = INPUT_DIR / "ref" / "stack-tracking-103.6_True_4_1.0_0.0_7-5_2_10_0.5.csv"
	dst = OUTPUT_FOLDER / f"tracking-{FileIO.get_timestamp_for_files()}.csv"
	shutil.copy2(src, dst)

	pt.settings.visualization_hr.active = True
	pt.settings.visualization_hr["Source L"].value = 0
	add_basic_file(pt)
	pt.process()

	check_output(OUTPUT_FOLDER, csv=[3], log=[1], json=[1], png=[8], clean=False)
	check_capsys(capsys, 31, [(False, 5), (False, 8), (False, 10), (False, 13), (False, 14), (True, 18), (False, 27), (False, 28)])

	pt.settings.visualization_hr["Type"].value = 1
	pt.settings.visualization_hr["Source T"].value = 0
	pt.process()

	# Il a Ajouté un fichier tracking_Fit qu'il a dû calculer et un tracking_hr_color, pour les images 8 Sources pour les loc, 5 pour les trajectoires.
	check_output(OUTPUT_FOLDER, csv=[5, 6], log=[1, 2], json=[1, 2], png=[13])
	check_capsys(capsys, 33, [(False, 5), (False, 8), (False, 10), (False, 13), (False, 14), (True, 18), (False, 29), (False, 30)])


##################################################
def test_process_only_visualization_graph(qtbot, capsys, pt):
	"""Test pour le process de visualization de graph."""
	clean_output()

	# Ajout des fichiers de localisation et tracking
	OUTPUT_FOLDER.mkdir(exist_ok=True, parents=True)
	src = INPUT_DIR / "ref" / "stack-localizations-103.6_True_4_1.0_0.0_7.csv"
	dst = OUTPUT_FOLDER / f"localizations-{FileIO.get_timestamp_for_files()}.csv"
	shutil.copy2(src, dst)
	src = INPUT_DIR / "ref" / "stack-tracking-103.6_True_4_1.0_0.0_7-5_2_10_0.5.csv"
	dst = OUTPUT_FOLDER / f"tracking-{FileIO.get_timestamp_for_files()}.csv"
	shutil.copy2(src, dst)

	pt.settings.visualization_graph.active = True
	add_basic_file(pt)
	pt.process()

	check_output(OUTPUT_FOLDER, csv=[3], log=[1], json=[1], png=[18])
	check_capsys(capsys, 43, [(False, 5), (False, 8), (False, 10), (False, 13), (False, 14), (False, 18), (True, 19), (False, 40)])


##################################################
def test_process_only_gallery(qtbot, capsys, pt):
	"""Test pour le process de visualization HR."""
	clean_output()

	# Ajout du fichier de localisation
	OUTPUT_FOLDER.mkdir(exist_ok=True, parents=True)
	src = INPUT_DIR / "ref" / "stack-localizations-103.6_True_4_1.0_0.0_7.csv"
	dst = OUTPUT_FOLDER / f"localizations-{FileIO.get_timestamp_for_files()}.csv"
	shutil.copy2(src, dst)

	pt.settings.gallery.active = True
	add_basic_file(pt)
	pt.process()

	# dimension 270 (30 ROI / lignes(colonnes) * taille de ROI de 9) et 1 frame (30 * 30 = 900 / frame et environ 450 en entrée)
	res, ref = FileIO.open_tif(str(list(OUTPUT_FOLDER.glob("*.tif"))[0])).shape, (1, 270, 270)
	assert res == ref, f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1], tif=[1])
	check_capsys(capsys, 23, [(False, 5), (False, 8), (False, 10), (False, 12), (False, 13), (False, 17), (False, 18), (True, 19)])


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
	check_capsys(capsys, 48, [(True, 5), (True, 7), (True, 9), (True, 11), (True, 13), (True, 21), (True, 23), (True, 44)])


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
	pt.settings.filtering["Save"].value = True
	pt.update_filtered()  # Tout est vide, mais je demande à enregistrer

	OUTPUT_FOLDER.mkdir(exist_ok=True, parents=True)
	src = INPUT_DIR / "ref" / "stack-localizations-103.6_True_4_1.0_0.0_7.csv"
	dst = OUTPUT_FOLDER / f"localizations-{FileIO.get_timestamp_for_files()}.csv"
	shutil.copy2(src, dst)

	add_basic_file(pt)
	pt.process()
	pt.update_filtered()  # Maintenant, il va recalculer les filtres (il n'y en aura aucun de toute façon).
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1])  # Il n'a rien enregistré, car les filtres n'ont pas fait de changement.


##################################################
def test_save_filtered(qtbot, capsys, pt):
	"""Test pour la mise à jour des tableaux filtrés."""
	clean_output()
	pt._path = OUTPUT_DIR
	pt.update_filtered()  # Tout est vide
	pt.settings.filtering["Save"].value = True
	pt.update_filtered()  # Tout est vide, mais je demande à enregistrer

	OUTPUT_FOLDER.mkdir(exist_ok=True, parents=True)
	src = INPUT_DIR / "ref" / "stack-localizations-103.6_True_4_1.0_0.0_7.csv"
	dst = OUTPUT_FOLDER / f"localizations-{FileIO.get_timestamp_for_files()}.csv"
	shutil.copy2(src, dst)

	add_basic_file(pt)
	pt.df["loc"] = pd.read_csv(INPUT_DIR / "ref" / "stack-localizations-103.6_True_4_1.0_0.0_7.csv")
	pt.settings.filtering["Plane"].active = True
	pt.settings.filtering["Plane"].value = [2, 3]
	pt.update_filtered()  # Il va recalculer les filtres.
	check_output(OUTPUT_FOLDER, csv=[1])  # Il a enregistré la version filtrée.


##################################################
def test_filter_plan(qtbot, capsys, pt):
	"""Test pour le filtrage des plans lors de l'exécution."""
	clean_output()

	# Ajout du fichier de localisation
	OUTPUT_FOLDER.mkdir(exist_ok=True, parents=True)
	src = INPUT_DIR / "ref" / "stack-localizations-103.6_True_4_1.0_0.0_7.csv"
	dst = OUTPUT_FOLDER / f"localizations-{FileIO.get_timestamp_for_files()}.csv"
	shutil.copy2(src, dst)

	add_basic_file(pt)
	pt.settings.filtering["Plane"].active = True
	pt.settings.filtering["Plane"].value = [2, 3]
	pt.process()

	assert pt.localizations["Plane"].isin([2, 3]).all(), "Le DataFrame contient des valeurs hors [2, 3] dans la colonne Plane."
	res, ref = pt.localizations.shape, (95, 18)
	assert res == ref, f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"
	# création des 3 fichiers normaux (meta, settings, log) aucun changement pour le fichier loc pas d'enregistrement des données filtrées
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1])
	check_capsys(capsys, 23, [(False, 5), (False, 9), (False, 11), (False, 13), (False, 14), (False, 18), (False, 19), (False, 20)])


##################################################
def test_filter_all_localization(qtbot, capsys, pt):
	"""Test pour le filtrage complet lors de l'exécution."""
	clean_output()

	# Ajout du fichier de localisation
	OUTPUT_FOLDER.mkdir(exist_ok=True, parents=True)
	src = INPUT_DIR / "ref" / "stack-localizations-103.6_True_4_1.0_0.0_7.csv"
	dst = OUTPUT_FOLDER / f"localizations-{FileIO.get_timestamp_for_files()}.csv"
	shutil.copy2(src, dst)

	# Ajout du fichier
	add_basic_file(pt)

	pt.settings.filtering["Plane"].active = True
	pt.settings.filtering["Plane"].value = [1, 9]  # Suppression du dernier plan uniquement 411/451 : 40 suppression(s)
	pt.settings.filtering["Localization"]["Intensity"].active = True
	pt.settings.filtering["Localization"]["Intensity"].value = [100, 20000]  # 391/411 : 20 suppression(s)
	pt.settings.filtering["Localization"]["Sigma X"].active = True
	pt.settings.filtering["Localization"]["Sigma X"].value = [0, 10]  # Aucune suppression
	pt.settings.filtering["Localization"]["Sigma Y"].active = True
	pt.settings.filtering["Localization"]["Sigma Y"].value = [0, 10]  # Aucune suppression
	pt.settings.filtering["Localization"]["Circularity"].active = True  # Aucune suppression
	pt.settings.filtering["Localization"]["Theta"].active = True
	pt.settings.filtering["Localization"]["Theta"].value = [-5, 5]  # 366/391 : 25 suppression(s)
	pt.settings.filtering["Localization"]["Z"].active = True  # Aucune suppression
	pt.settings.filtering["Localization"]["MSE XY"].active = True
	pt.settings.filtering["Localization"]["MSE XY"].value = [0.01, 10]  # 365/366 : 1 suppression(s)
	# pt.settings.filtering["Localization"]["MSE Z"].active = True # La colonne est à -1 le filtre est forcément sur un nombre positif
	# pt.settings.filtering["Localization"]["MSE Z"].value = [0, 10]
	pt.process()
	check_capsys(capsys, 23, [(False, 5), (False, 9), (False, 11), (False, 13), (False, 14), (False, 18), (False, 19), (False, 20)])

	pt.settings.filtering["Save"].value = True
	pt.process()  # Second passage avec enregistrement
	check_capsys(capsys, 24, [(False, 5), (False, 10), (False, 12), (False, 14), (False, 15), (False, 19), (False, 20), (False, 21)])

	# Le filtrage ne modifie plus le dataframe original qui garde constamment son statut "complet".
	loc = pt.localizations
	ref = [["Plane", 1, 9], ["Integrated Intensity", 100, 20000], ["MSE XY", 0.01, 10],
		   ["Sigma X", 0, 10], ["Sigma Y", 0, 10], ["Theta", -5, 5],
		   ["Circularity", 0, 1], ["Z", -1, 1]]
	for r in ref:
		assert loc[r[0]].between(r[1], r[2]).all(), f"Le DataFrame contient des valeurs hors [{r[1]}:{r[2]}] dans la colonne {r[0]}."

	res, ref = len(loc), 365
	assert res == ref, f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"

	# La colonne est à -1 le filtre est forcément sur un nombre positif donc il va vider le dataframe
	pt.settings.filtering["Localization"]["MSE Z"].active = True

	res = pt.filter_localizations(pt.localizations)
	assert res.empty, "Un dataframe vide doit être retourné."
	res = pt.filter_localizations(pd.DataFrame())
	assert res.empty, "Un dataframe vide doit être retourné."
	check_output(OUTPUT_FOLDER, csv=[3, 4], log=[1, 2], json=[1, 2])


##################################################
def test_filter_all_tracking(qtbot, capsys, pt):
	"""Test pour le filtrage complet lors de l'exécution."""
	clean_output()

	# Ajout du fichier de trajectoires
	OUTPUT_FOLDER.mkdir(exist_ok=True, parents=True)
	src = INPUT_DIR / "ref" / "stack-tracking-103.6_True_4_1.0_0.0_7-5_2_10_0.5.csv"
	dst = OUTPUT_FOLDER / f"tracking-{FileIO.get_timestamp_for_files()}.csv"
	shutil.copy2(src, dst)

	# Ajout du fichier
	add_basic_file(pt)

	pt.process()
	res, ref = len(pt.tracks), 222
	assert res == ref, f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1], clean=False)
	check_capsys(capsys, 22, [(False, 5), (False, 7), (False, 9), (False, 12), (False, 13), (False, 17), (False, 18), (False, 19)])

	pt.settings.filtering["Tracks"]["Length"].active = True
	pt.settings.filtering["Tracks"]["Length"].value = [3, 10000]  # 52/222 : 170 suppression(s)
	pt.settings.filtering["Save"].value = True
	pt.process()

	res, ref = len(pt.tracks), 52
	assert res == ref, f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"
	check_output(OUTPUT_FOLDER, csv=[3, 4], log=[1, 2], json=[1, 2])
	check_capsys(capsys, 24, [(False, 5), (False, 7), (False, 9), (False, 14), (False, 15), (False, 19), (False, 20), (False, 21)])


##################################################
def test_filter_all_tracks_compute(qtbot, capsys, pt):
	"""Test pour le filtrage complet lors de l'exécution."""
	clean_output()

	# Ajout du fichier de trajectoires
	OUTPUT_FOLDER.mkdir(exist_ok=True, parents=True)
	src = INPUT_DIR / "ref" / "stack-tracking-103.6_True_4_1.0_0.0_7-5_2_10_0.5.csv"
	dst = OUTPUT_FOLDER / f"tracking-{FileIO.get_timestamp_for_files()}.csv"
	shutil.copy2(src, dst)

	# Ajout du fichier
	add_basic_file(pt)

	pt.settings.tracks_compute.active = True
	pt.settings.tracks_compute["MSD"].value = True
	pt.settings.tracks_compute["Instant Diffusion"].value = True
	pt.settings.tracks_compute["Fit"].value = 1
	pt.settings.tracks_compute["Fit Length"].value = 2

	pt.settings.filtering["Tracks"]["Length"].active = True
	pt.settings.filtering["Tracks"]["Length"].value = [3, 10000]
	pt.settings.filtering["Tracks"]["Instant D"].active = True
	pt.settings.filtering["Tracks"]["Instant D"].value = [0.01, 5]
	pt.settings.filtering["Tracks"]["D Coeff"].active = True
	pt.settings.filtering["Tracks"]["D Coeff"].value = [1, 5]
	pt.settings.filtering["Tracks"]["Speed"].active = True
	pt.settings.filtering["Tracks"]["Speed"].value = [-10, 10]
	pt.settings.filtering["Tracks"]["Alpha"].active = True
	pt.settings.filtering["Tracks"]["Confinement"].value = [-10, 10]
	pt.process()

	check_capsys(capsys, 24, [(False, 5), (False, 7), (False, 9), (False, 13), (True, 14), (False, 19), (False, 20), (False, 21)])

	pt.settings.filtering["Save"].value = True
	pt.process()
	check_capsys(capsys, 29, [(False, 5), (False, 7), (False, 9), (False, 14), (True, 15), (False, 24), (False, 25), (False, 26)])

	# Vérification manuelle à l'heure actuelle
	assert len(pt.tracks) == 26, f"Il reste {len(pt.tracks)} points au lieu de 26 sur les trajectoires."
	assert len(pt.tracks_compute["MSD"]) == 6, f"Il reste {len(pt.tracks_compute['MSD'])} trajectoires au lieu de 14."
	# Filtre massif plus rien à la sortie
	pt.settings.filtering["Tracks"]["Length"].value = [42, 10000]
	pt.process()
	assert len(pt.df["f_trc"]) == 0, f"Il reste {len(pt.tracks)} points au lieu de 0 sur les trajectoires."
	assert len(pt.df["f_MSD"]) == 0, f"Il reste {len(pt.tracks_compute['MSD'])} trajectoires au lieu de 0."
	check_capsys(capsys, 26, [(False, 5), (False, 7), (False, 9), (False, 13), (True, 14), (False, 21), (False, 22), (False, 23)])


##################################################
def test_filter_outside(qtbot, capsys, pt):
	"""Test pour le filtrage hors exécution."""
	clean_output()
	pt.settings.filtering["Tracks"]["Instant D"].active = True
	assert pt.filter_localizations(pt.localizations).empty
	assert pt.filter_tracks(pt.tracks).empty
	res = pt.filter_tracks_compute(pt.tracks, pt.df["MSD"], pt.df["InD"], pt.df["Fit"])
	for r in res: assert r.empty
	res = pt.filter_tracks_compute(pd.DataFrame(data=[1], columns=["Track"]), pd.DataFrame(data=[2], columns=["Track"]),
								   pd.DataFrame(data=[3], columns=["Track"]), pd.DataFrame(data=[4], columns=["Track"]))

	o_trc, o_msd, o_ind, o_fit = res
	assert len(o_trc) == 1  # Il a conservé son unique track même si elle n'est pas présente ailleurs. Ce comportement est censé être impossible à avoir.
	assert o_msd.empty
	assert o_ind.empty
	assert o_fit.empty


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
