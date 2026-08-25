"""
Teste l'orchestration complète des traitements par la classe :class:`PALMTracer`.

.. note:: Certaines vérifications du journal portent uniquement sur le nombre de lignes, car chaque traitement en produit au moins quinze.
"""

import shutil
from time import sleep

import pytest

from palm_tracer._tests.Utils import *
from palm_tracer.PALMTracer import FILE_STATUS
from palm_tracer.Processing import Parsing
from palm_tracer.Settings.Types import Combo
from palm_tracer.Tools import FileIO

OUTPUT_FOLDER = INPUT_DIR / "stack_PALM_Tracer"
OUTPUT_FOLDER_2 = INPUT_DIR / "stack_quadrant_PALM_Tracer"


@pytest.fixture
def pt():
	"""fixture interne."""
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


##################################################
def test_reset_result(pt):
	"""Vérifie le process sans fichiers en entrée."""

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
# region Accesseurs
# ==================================================
##################################################
def test_getter_localization(pt):
	"""Vérifie le getter de la localisation."""
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
def test_getter_beads(pt):
	"""Vérifie le getter de la localisation."""
	res = pt.beads
	assert res.empty, "Le Dataframe devrait être vide."
	ref1 = pd.DataFrame([1, 2])
	pt.df["bds"] = ref1
	res = pt.beads
	assert res.equals(ref1), f"Résultat incorrect.\nAttendu : {ref1}\tObtenu : {res}"


##################################################
def test_getter_tracks(pt):
	"""Vérifie le process sans fichiers en entrée."""
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
def test_getter_tracks_compute(pt):
	"""Vérifie le process sans fichiers en entrée."""
	df = pt.tracks_compute
	assert df["MSD"].empty, "Le Dataframe devrait être vide."
	ref1 = pd.DataFrame([1, 2])
	pt.df["f_MSD"] = ref1
	df = pt.tracks_compute
	assert df["MSD"].equals(ref1), "Le Dataframe devrait non vide."


##################################################
def test_get_status(pt):
	# État initial
	"""Vérifie le calcul du statut des tableaux de résultats."""
	ref = {"Localization": FILE_STATUS[0], "Beads": FILE_STATUS[0], "Tracking": FILE_STATUS[0],
		   "MSD":          FILE_STATUS[0], "Instant D": FILE_STATUS[0], "Fit": FILE_STATUS[0]}
	res = pt.get_status()
	for key in res: assert res[key] == ref[key], f"Status incorrect.\nAttendu : {ref}\nObtenu : {res}"

	# Intégralité des DataFrames remplis
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

	# Un fichier méta + un localization
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1])


##################################################
def test_process_no_input(capsys, pt):
	"""Vérifie le process sans fichiers en entrée."""
	clean_output()
	pt.process()
	assert pt.df["loc"].empty, "Le Dataframe de localization ne devrait pas être vide"
	lines = get_lines_output(capsys)
	assert "No files." in lines[0]


##################################################
def test_process_nothing(capsys, pt):
	"""Vérifie le process avec tous les éléments à False et aucun fichier chargeable."""
	clean_output()

	add_basic_file(pt)
	pt.process()
	assert pt.df["loc"].empty, "Le Dataframe de localization devrait être vide"
	check_capsys(capsys, 15, [5, 6, 7, 8, 9, 10, 11, 12])
	check_output(OUTPUT_FOLDER, csv=[1], log=[1], json=[1])

	# Test d'une visualisation sans données.
	pt.settings.gallery.active = True
	pt.settings.hr.active = True
	pt.settings.graph.active = True
	pt.process()  # Test d'une visualisation sans données.
	assert pt.df["loc"].empty, "Le Dataframe de localization devrait être vide"
	check_capsys(capsys, 18, [5, 6, 7, 8, 9, 10, 12, 14])
	check_output(OUTPUT_FOLDER, csv=[1], log=[1], json=[1])

	# Test d'un calcul sur trajectoires sans données.
	pt.settings.gallery.active = False
	pt.settings.graph.active = False
	pt.settings.hr.active = False
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

	assert len(pt.df["loc"]) == 455
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

	assert len(pt.df["loc"]) == 455
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

	assert len(pt.df["loc"]) == 455
	assert pt.df["bds"].empty
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1])
	check_capsys(capsys, 17, [5, 7, 9, 10, 11, 12, 13, 14])


##################################################
def test_process_plane_discontinuous(capsys, pt):
	"""Vérifie le process de l'extraction des billes."""
	clean_output()

	src = INPUT_DIR / "localizations.csv"
	pt.df["loc"] = pd.read_csv(src)
	pt.df["loc"].loc[1, "Plane"] = 5
	pt._beads_extraction()
	assert pt.df["bds"].empty
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

	assert len(pt.df["bds"]) == 4  # 2 Billes sur 2 plans
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

	ref = pt.localizations
	ref = ref[ref["Integrated Intensity"] > 0]  # Suppression des éléments où la colonne "Integrated Intensity" est inférieure à 0 (l'ajustement a échoué).

	assert len(ref) == len(pt.tracks), "Nombre de points différents entre la localization et le tracking."
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

	assert len(pt.df["trc"]) == len(pt.df["blk"]), "Nombre de points différents entre la reconnexion et le tracking."
	check_output(OUTPUT_FOLDER, csv=[3], log=[1], json=[1])
	check_capsys(capsys, 17, [5, 6, 7, 9, 11, 12, 13, 14])


##################################################
def test_process_tracks_compute(capsys, pt):
	"""Vérifie le process de tracking."""
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
	assert len(pt.df["MSD"]) == 93  # Toutes les trajectoires sont éligibles au MSD
	assert len(pt.df["Fit"]) == 3  # Seules 3 trajectoires sont éligibles
	# Ajout de fichier MSD (ainsi qu'un fit minimal, un meta, un json et un log)
	check_output(OUTPUT_FOLDER, csv=[4], log=[1], json=[1], clean=False)
	check_capsys(capsys, 19, [5, 6, 7, 9, 10, 14, 15, 16])

	tc["MSD"].value = False
	tc["Instant Diffusion"].value = True
	tc["Fit"].value = 1
	sleep(1)  # Force un timestamp différent pour le Reuse
	pt.process()
	assert len(pt.df["MSD"]) == 0  # MSD désactivé, il est conservé
	assert len(pt.df["InD"]) == 3  # Seules 3 trajectoires sont éligibles
	assert len(pt.df["Fit"]) == 3  # Seules 3 trajectoires sont éligibles
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


#################################################
def test_process_visualization_hr(capsys, pt):
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
	sleep(1)  # Force un timestamp différent pour le Reuse
	pt.process()

	check_output(OUTPUT_FOLDER, csv=[3], log=[2], json=[2], png=[1], tif=[1], clean=False)
	check_capsys(capsys, 18, [5, 7, 8, 10, 11, 12, 13, 14])

	pt.settings.hr["Dimension"].value = 2  # Génération de la rotation 3D
	sleep(1)  # Force un timestamp différent pour le Reuse
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
	pt.settings.tracks_compute.active = True
	pt.settings.tracks_compute["MSD"].value = True
	pt.settings.tracks_compute["Instant Diffusion"].value = True
	pt.settings.tracks_compute["Fit"].value = 1
	pt.settings.gallery.active = True
	pt.settings.graph.active = True
	pt.settings.hr.active = True
	add_basic_file(pt)
	pt.process()

	check_output(OUTPUT_FOLDER, csv=[7], log=[1], json=[1], tif=[1], png=[1], html=[1])
	check_capsys(capsys, 27, [5, 8, 10, 12, 14, 19, 21, 23])


# ==================================================
# endregion Traitements
# ==================================================

# ==================================================
# region Filtrage
# ==================================================
##################################################
def test_reset_filtered(capsys, pt):
	"""Vérifie la suppréssion des tableaux filtrés."""

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
def test_update_filtered(capsys, pt):
	"""Vérifie la mise à jour des tableaux filtrés."""
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
def test_save_filtered(capsys, pt):
	"""Vérifie la mise à jour des tableaux filtrés."""
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
def test_connect_filters_button(qtbot, capsys, pt):
	"""Vérifie la connexion des boutons de filtrage."""
	pt.settings.get_ui("test")
	pt.connect_filters_button("test")


##################################################
def test_filter_localization(capsys, pt):
	"""Vérifie le filtrage complet lors de l'exécution."""
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
def test_filter_tracks_compute(capsys, pt):
	"""Vérifie le filtrage complet lors de l'exécution."""
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
# endregion Filtrage
# ==================================================

# ==================================================
# region Visualisation
# ==================================================
###################################################
def test_graph():
	"""Vérifie différentes récupérations de données."""
	pt = get_fake_pt()

	ref_title: str
	ref_shape: tuple
	ref_data: list[int] | list[list[int]] | list[float] | list[list[float]]

	s = pt.settings.graph
	# Localization Basique
	s["Type"].value = 0
	fig = pt.graph()
	assert fig.data[0].type == "histogram"

	# Localization Count
	s["Source"].value = len(cast(Combo, s["Source"]).items) - 1  # Localisation Count est un affichage Scatter Plot
	fig = pt.graph()
	assert fig.data[0].type == "scatter"

	# Tracking Length Scatter
	s["Type"].value = 1
	s["Source"].value = len(cast(Combo, s["Source"]).items) - 1  # Length Scatter est un affichage Scatter Plot
	fig = pt.graph()
	assert fig.data[0].type == "scatter"

	# Dual
	s["Dual"].value = True
	fig = pt.graph()
	assert fig.data[0].type == "scattergl"


###################################################
def test_get_graph_data():
	"""Vérifie différentes récupérations de données."""
	pt = get_fake_pt()

	ref_title: str
	ref_shape: tuple
	ref_data: list[int] | list[list[int]] | list[float] | list[list[float]]

	s = pt.settings.graph
	s["Type"].value = 0
	# Changement de source
	s["Source"].value = len(cast(Combo, s["Source"]).items) - 1  # Localisation Count est un affichage Scatter Plot

	# Classique
	data, title = pt._get_graph_data()
	ref_title, ref_shape, ref_data = "Localizations Count", (2, 2), [[1, 4], [2, 2]]
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# Double vue
	s["Dual"].value = True
	s["Source"].value = 1
	s["Source B"].value = 2
	data, title = pt._get_graph_data()
	ref_title, ref_shape, ref_data = "Localizations Sigma X / Sigma Y", (6, 2), [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1]]
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"

	# Colonne inexistante
	pt.localizations.drop("Sigma X", inplace=True, axis=1)
	data, title = pt._get_graph_data()
	ref_title, ref_shape, ref_data = "Localizations Sigma X / Sigma Y", (0,), []
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"


###################################################
def test_get_graph_data_from_src():
	"""Vérifie différentes récupérations de données."""
	pt = get_fake_pt()

	ref_title: str
	ref_shape: tuple
	ref_data: list[int] | list[list[int]] | list[float] | list[list[float]]

	# Localizations
	# Colonne inexistante
	data, title = pt._get_graph_data_from_src(0, "no column")
	ref_title, ref_shape, ref_data = "Localizations no column", (0,), []
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# Classique
	data, title = pt._get_graph_data_from_src(0, "X")
	ref_title, ref_shape, ref_data = "Localizations X", (6,), [1, 2, 3, 4, 1, 2]
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# Count
	data, title = pt._get_graph_data_from_src(0, "Localizations Count")
	ref_title, ref_shape, ref_data = "Localizations Count", (2, 2), [[1, 4], [2, 2]]
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# Empty
	for _ in range(4): pt.localizations.drop(pt.localizations.index, inplace=True)
	data, title = pt._get_graph_data_from_src(0, "X")
	ref_title, ref_shape, ref_data = "Localizations X", (0,), []
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"

	# Tracks
	# Colonne inexistante
	data, title = pt._get_graph_data_from_src(1, "no column")
	ref_title, ref_shape, ref_data = "Tracks no column", (0,), []
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# Length Scatter
	data, title = pt._get_graph_data_from_src(1, "Length Scatter")
	ref_title, ref_shape, ref_data = "Tracks Length Scatter", (9, 2), [[1, 99], [2, 2], [3, 2], [4, 2], [5, 2], [6, 2], [7, 2], [8, 2], [9, 2]]
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# Length Hist
	data, title = pt._get_graph_data_from_src(1, "Length")
	ref_title, ref_shape, ref_data = "Tracks Length", (9,), [99, 2, 2, 2, 2, 2, 2, 2, 2]
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# Length On
	data, title = pt._get_graph_data_from_src(1, "Length On")
	ref_title, ref_shape, ref_data = "Tracks Length On", (10,), [1, 1, 2, 2, 2, 2, 2, 2, 2, 2]
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# Length Off
	data, title = pt._get_graph_data_from_src(1, "Length Off")
	ref_title, ref_shape, ref_data = "Tracks Length Off", (1,), [98]
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# Length bad
	data, title = pt._get_graph_data_from_src(1, "Length New")
	ref_title, ref_shape, ref_data = "Tracks Length New", (0,), []
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# MSD
	pt.settings.graph["MSD Step"].value = 5
	data, title = pt._get_graph_data_from_src(1, "MSD")
	ref_title, ref_shape, ref_data = "Tracks MSD Step 5", (1, 2), [[81, 0.14]]
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	pt.settings.graph["MSD Step"].value = 9
	data, title = pt._get_graph_data_from_src(1, "MSD")
	ref_title, ref_shape, ref_data = "Tracks MSD Step 9", (0,), []
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# Instant D
	data, title = pt._get_graph_data_from_src(1, "Instant D")
	ref_title, ref_shape, ref_data = "Tracks Instant D", (27,), [4.51, 1.37, 3.04, 1.13, 1e-06, 1.99, 1e-06, 2.34, 0.81, 4.02, 4.26, 1.31, 6.37, 0.60,
																 2.22, 4.83, 0.27, 0.96, 5.41, 9.19, 0.60, 1.24, 0.54, 2.43, 2.23, 1.61, 3.05, ]
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# Fit
	data, title = pt._get_graph_data_from_src(1, "MSE(0)")
	ref_title, ref_shape, ref_data = "Tracks MSE(0)", (14, 2), [[35, 1], [37, 1], [66, 1], [75, 1], [81, 1], [83, 1], [102, 1], [114, 1],
																[131, 1], [152, 1], [158, 1], [165, 1], [176, 1], [220, 1]]
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	# --- Empty ---
	for _ in range(4): pt.tracks.drop(pt.tracks.index, inplace=True)
	for _ in range(2):
		df = pt.tracks_compute
		for d in df.values(): d.drop(d.index, inplace=True)

	data, title = pt._get_graph_data_from_src(1, "Length")
	ref_title, ref_shape, ref_data = "Tracks Length", (0,), []
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	data, title = pt._get_graph_data_from_src(1, "MSD")
	ref_title, ref_shape, ref_data = "Tracks MSD", (0,), []
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	data, title = pt._get_graph_data_from_src(1, "Instant D")
	ref_title, ref_shape, ref_data = "Tracks Instant D", (0,), []
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)

	data, title = pt._get_graph_data_from_src(1, "MSE(0)")
	ref_title, ref_shape, ref_data = "Tracks MSE(0)", (0,), []
	assert data.shape == ref_shape, f"Dimensions incorrectes.\tAttendu : {ref_shape}\tObtenu : {data.shape}"
	assert title == ref_title, f"Titre Incorrect.\tAttendu : {ref_title}\tObtenu : {title}"
	np.testing.assert_array_equal(data, ref_data)


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


###################################################
def test_hr():
	"""Vérifie différentes récupérations de données."""
	pt = get_fake_pt()
	ref_empty = np.zeros((1, 1), dtype=np.uint16)
	ref_viz0 = np.zeros((10, 10), dtype=np.uint16)
	s = pt.settings.hr
	s["Ratio"].value = 2
	s["Remove Beads"].value = False
	s["Drift Correction"].value = False

	# Aucune pile
	viz, plot = pt.hr()
	assert np.allclose(ref_empty, viz) and np.allclose(ref_empty, plot)

	# HR Localisation
	pt._stack = np.zeros((1, 5, 5), dtype=np.uint16)
	pt.settings.rois.set_size(5, 5)
	viz, plot = pt.hr()
	ref_viz = ref_viz0.copy()
	ref_viz[4, 2] = ref_viz[6, 4] = 2
	ref_plot = [[0, 4, 2], [0, 6, 4], [0, 8, 6], [0, 10, 8], [0, 4, 2],
				[0, 6, 4]]  # (8,6) à une intensité de 0 et (10,8) est sur le bord de l'image (donc hors cadre)
	np.testing.assert_array_equal(viz, ref_viz)
	np.testing.assert_array_equal(plot, ref_plot)

	# HR Localisation remove beads
	s["Remove Beads"].value = True
	viz, plot = pt.hr()
	np.testing.assert_array_equal(viz, ref_viz)
	np.testing.assert_array_equal(plot, ref_plot)

	# HR Localisation Drift Correction
	s["Drift Correction"].value = True
	pt.df["bds"] = pd.DataFrame([[1, 1, 1, 1, 2, 3, 1, 1, 1, 0, 1],
								 [1, 2, 2, 2, 3, 4, 1, 1, 1, 0, 1],
								 [1, 3, 3, 50, 3, 4, 1, 1, 1, 0, 1],  # Valeur abhérrante gommée par le smooth
								 [1, 4, 4, 4, 3, 4, 1, 1, 1, 0, 1],
								 [1, 5, 5, 5, 3, 4, 1, 1, 1, 0, 1]],
								columns=Parsing.FILES_COLUMNS["Beads"]["columns"])
	viz, plot = pt.hr()
	ref_viz = ref_viz0.copy()
	ref_viz[4, 0] = ref_viz[6, 4] = 1
	ref_plot = [[0, 6, 4], [0, 8, 6], [0, 10, 8], [0, 4, 0]]
	np.testing.assert_array_equal(viz, ref_viz)
	np.testing.assert_array_equal(plot, ref_plot)
	s["Drift Correction"].value = False

	# HR Localisation DataFrame vide
	for _ in range(4): pt.localizations.drop(pt.localizations.index, inplace=True)
	viz, plot = pt.hr()
	assert np.allclose(ref_empty, viz) and np.allclose(ref_empty, plot)

	# HR Tracking
	s["Type"].value = 1
	viz, plot = pt.hr()
	ref_viz = ref_viz0.copy()
	ref_viz[2, 2] = 8
	ref_viz[2, 8] = 5
	ref_plot = [[1, 1, 2, 2], [1, 99, 2, 2], [3, 3, 2, 8], [3, 4, 2, 8], [4, 3, 2, 10], [4, 4, 2, 10], [5, 5, 2, 8],
				[5, 6, 2, 8], [6, 11, 2, 2], [6, 12, 2, 2], [7, 16, 2, 10], [7, 17, 2, 10], [8, 31, 2, 2], [8, 32, 2, 2]]
	np.testing.assert_array_equal(viz, ref_viz)
	np.testing.assert_array_equal(plot, ref_plot)

	# HR Tracking DataFrame vide
	for _ in range(4): pt.tracks.drop(pt.tracks.index, inplace=True)
	viz, plot = pt.hr()
	assert np.allclose(ref_empty, viz) and np.allclose(ref_empty, plot)


###################################################
def test_hr_filter():
	"""Vérifie différentes récupérations de données."""
	pt = get_fake_pt()
	s = pt.settings.hr
	s["Ratio"].value = 2
	s["Remove Beads"].value = False
	s["Drift Correction"].value = False

	# Filtre sur X
	pt._stack = np.zeros((1, 5, 5), dtype=np.uint16)
	pt.settings.rois.set_size(5, 5)
	sf = pt.settings.filters
	sf["ROI"].active = True
	pt.settings.rois.set_xy_roi(2, 5, 0, 5, False)
	viz, plot = pt.hr()
	ref_viz = np.zeros((10, 6), dtype=np.uint16)
	ref_viz[6, 0] = 2  # Précédemment [4, 2], [6, 4] mais avec le filtre sur X à 2 le premier devient hors filtre (-2 × facteur d'agrandissement de 2 = -4)
	ref_plot = [[0, 6, 0], [0, 8, 2], [0, 10, 4], [0, 6, 0]]
	np.testing.assert_array_equal(viz, ref_viz)
	np.testing.assert_array_equal(plot, ref_plot)

	# Filtre sur Y
	pt.settings.rois.set_xy_roi(2, 5, 2, 5, False)
	viz, plot = pt.hr()
	ref_viz = np.zeros((6, 6), dtype=np.uint16)
	ref_viz[2, 0] = 2
	ref_plot = [[0, 2, 0], [0, 4, 2], [0, 6, 4], [0, 2, 0]]
	np.testing.assert_array_equal(viz, ref_viz)
	np.testing.assert_array_equal(plot, ref_plot)

	# Tracking Filtré
	s["Type"].value = 1
	pt.settings.rois.set_xy_roi(1, 4, 1, 2, False)
	viz, plot = pt.hr()
	ref_viz = np.zeros((2, 6), dtype=np.uint16)
	ref_viz[0, 0] = 8
	ref_plot = [[1, 1, 0, 0], [1, 99, 0, 0], [3, 3, 0, 6], [3, 4, 0, 6], [5, 5, 0, 6], [5, 6, 0, 6],
				[6, 11, 0, 0], [6, 12, 0, 0], [8, 31, 0, 0], [8, 32, 0, 0]]
	np.testing.assert_array_equal(viz, ref_viz)
	np.testing.assert_array_equal(plot, ref_plot)


###################################################
def test_hr_z_stack():
	"""Vérifie différentes récupérations de données."""
	pt = get_fake_pt()
	s = pt.settings.hr
	s["Dimension"].value = 1
	s["Ratio"].value = 2
	s["Remove Beads"].value = False
	s["Drift Correction"].value = False
	# HR Localisation
	pt._stack = np.zeros((1, 5, 5), dtype=np.uint16)
	pt.settings.rois.set_size(5, 5)
	viz, plot = pt.hr()
	ref_viz = np.zeros((1, 10, 10), dtype=np.uint16)
	ref_viz[0, 4, 2] = ref_viz[0, 6, 4] = 2
	ref_plot = [[0, 4, 2], [2, 6, 4], [4, 8, 6], [6, 10, 8], [0, 4, 2], [2, 6, 4]]
	np.testing.assert_array_equal(viz, ref_viz)
	np.testing.assert_array_equal(plot, ref_plot)


###################################################
def test_hr_rotation():
	"""Vérifie différentes récupérations de données."""
	pt = get_fake_pt()
	s = pt.settings.hr
	s["Dimension"].value = 2
	s.hr_3d["Frames"].value = 2
	s["Ratio"].value = 2
	s["Remove Beads"].value = False
	s["Drift Correction"].value = False
	# HR Localisation
	pt._stack = np.zeros((1, 5, 5), dtype=np.uint16)
	pt.settings.rois.set_size(5, 5)
	viz, plot = pt.hr()
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
	s["Remove Beads"].value = False
	s["Drift Correction"].value = False

	# Bille qui part en diagonale du haut à droite vers le bas à gauche
	bead_x, bead_y = np.linspace(n_x - 0.5, 0, n_p, dtype=np.float32), np.linspace(0, n_y - 0.5, n_p, dtype=np.float32)

	beads = pd.DataFrame({"Bead":  np.ones(n_p, dtype=np.int32),
						  "Plane": np.arange(1, n_p + 1, dtype=np.int32),
						  "X":     bead_x,
						  "Y":     bead_y,
						  "Z":     np.zeros(n_p, dtype=np.float32)})

	# Loclaisation au centre
	loc = pd.DataFrame({"Plane":                np.arange(1, n_p + 1, dtype=np.int32),
						"X":                    np.full(n_p, n_x / 2.0, dtype=np.float32),
						"Y":                    np.full(n_p, n_y / 2.0, dtype=np.float32),
						"Z":                    np.zeros(n_p, dtype=np.float32),
						"Integrated Intensity": np.full(n_p, 1, dtype=np.float32),
						"Sigma X":              np.ones(n_p, dtype=np.float32),
						"Sigma Y":              np.ones(n_p, dtype=np.float32),
						"Theta":                np.zeros(n_p, dtype=np.float32)})

	pt.df["bds"], pt.df["loc"] = beads.copy(), loc.copy()

	# Génération fixe (n_beads fois sur la position centrale)
	viz, _ = pt.hr()
	ref = ref_viz0.copy()
	ref[n_y, n_x] = n_p
	np.testing.assert_array_equal(viz, ref)

	# Génération fixe de la bille (n_beads fois sur la position [1, 1] * upscale)
	pt.df["loc"].loc[:, ["X", "Y"]] = pt.df["bds"].loc[:, ["X", "Y"]].to_numpy()
	viz, _ = pt.hr()
	ref = ref_viz0.copy()
	ref[0, 15] = ref[1, 13] = ref[2, 11] = ref[3, 9] = ref[4, 6] = ref[5, 4] = ref[6, 2] = ref[7, 0] = 1
	np.testing.assert_array_equal(viz, ref)

	# Génération Drift corrigé des mêmes données que la bille, donc le premier point sera compté 8 fois.
	s["Drift Correction"].value = True
	viz, _ = pt.hr()
	ref = ref_viz0.copy()
	ref[np.round(bead_y[0] * 2).astype(int), np.round(bead_x[0] * 2).astype(int)] = n_p
	np.testing.assert_array_equal(viz, ref)

	# Génération Drift corrigé, mais la localisation était fixe
	# (donc elle va bouger vers le haut à droite, elle remonte la diagonale et une partie sera hors champs (départ au centre)
	pt.df["bds"], pt.df["loc"] = beads.copy(), loc.copy()
	viz, _ = pt.hr()
	ref = ref_viz0.copy()
	ref[4, 8] = ref[3, 10] = ref[2, 12] = ref[1, 14] = 1  # Les autres points hors champ continuent (0,16) (-1, 18)...
	np.testing.assert_array_equal(viz, ref)

	# Seconde bille qui descend comme la précédente, mais ne va pas vers la gauche donc la pente initiale sera divisé par 2.
	beads2 = pd.DataFrame({"Bead":  np.full(n_p, 2, dtype=np.int32),
						   "Plane": np.arange(1, n_p + 1, dtype=np.int32),
						   "X":     np.zeros_like(bead_x, dtype=np.float32),
						   "Y":     bead_y,
						   "Z":     np.zeros(n_p, dtype=np.float32)})

	pt.df["bds"] = pd.concat([beads, beads2], ignore_index=True)
	viz, _ = pt.hr()
	ref = ref_viz0.copy()
	ref[4, 8] = ref[3, 9] = ref[2, 10] = ref[1, 11] = ref[0, 12] = 1  # Les autres points hors champ continuent (-1,13) (-2, 14)...
	np.testing.assert_array_equal(viz, ref)

	# On ajoute nos 2 billes à la localisation et on enlève le drift, tout doit être affiché
	s["Drift Correction"].value = False
	size = 3 * n_p
	loc2 = pd.DataFrame({"Plane":                np.tile(np.arange(1, n_p + 1, dtype=np.int32), 3),
						 "X":                    np.full(size, n_x / 2.0, dtype=np.float32),
						 "Y":                    np.full(size, n_y / 2.0, dtype=np.float32),
						 "Z":                    np.zeros(size, dtype=np.float32),
						 "Integrated Intensity": np.full(size, 1, dtype=np.float32),
						 "Sigma X":              np.ones(size, dtype=np.float32),
						 "Sigma Y":              np.ones(size, dtype=np.float32),
						 "Theta":                np.zeros(size, dtype=np.float32)})
	loc2.loc[n_p:, ["X", "Y"]] = pt.df["bds"].loc[:, ["X", "Y"]].to_numpy()

	pt.df["loc"] = loc2.copy()
	viz, _ = pt.hr()
	ref = ref_viz0.copy()
	ref[0, 15] = ref[1, 13] = ref[2, 11] = ref[3, 9] = ref[4, 6] = ref[5, 4] = ref[6, 2] = ref[7, 0] = 1  # Bille originale
	ref[n_y, n_x] += n_p  # Localization statique
	ref[:, 0] += 1  # Bille Verticale
	np.testing.assert_array_equal(viz, ref)

	# On supprime nos 2 billes (mais on va conserver notre localisation
	s["Remove Beads"].value = True
	viz, _ = pt.hr()
	ref = ref_viz0.copy()
	ref[n_y, n_x] += n_p  # Localization statique
	np.testing.assert_array_equal(viz, ref)

	# Bille Random....
	s["Remove Beads"].value = False
	s["Drift Correction"].value = True
	pt.df["bds"], pt.df["loc"] = beads.copy(), loc.copy()
	pt.df["bds"]["X"] = np.array([5.095, 3.755, 5.434, 4.789, 2.376, 5.902, 5.044, 5.144], dtype=np.float32)  # Random autour du centre
	pt.df["bds"]["Y"] = np.array([1.256, 1.900, 1.741, 2.853, 2.287, 2.645, 1.886, 1.454], dtype=np.float32)  # Random autour du centre
	viz, _ = pt.hr()
	ref = ref_viz0.copy()
	# Position au centre puis résultat du random dans tous les sens ATTENTION LE DRIFT EST LISSÉ.
	ref[4, 8] = ref[3, 9] = ref[2, 11] = ref[2, 13] = ref[2, 14] = ref[3, 15] = 1
	np.testing.assert_array_equal(viz, ref)

	# Correction sur la position de la bille avec lissage...
	pt.df["loc"].loc[:, ["X", "Y"]] = pt.df["bds"].loc[:, ["X", "Y"]].to_numpy()
	viz, _ = pt.hr()
	ref = ref_viz0.copy()
	# Position de la bille random corrigé ATTENTION LE DRIFT EST LISSÉ, ce n'est donc pas un point unique.
	ref[3, 9] = ref[3, 10] = ref[2, 11] = ref[2, 14] = ref[3, 14] = 1
	np.testing.assert_array_equal(viz, ref)

	# Correction sur la position de la bille sans lissage...
	s["Smooth Drift"].value = False
	viz, _ = pt.hr()
	ref = ref_viz0.copy()
	# Position de la bille random corrigé et non lissé.
	ref[3, 10] = n_p
	np.testing.assert_array_equal(viz, ref)


# ==================================================
# endregion Visualisation
# ==================================================

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

	model = pt._get_astigmatism_model(Path(""))  # Il ne va pas reussir, il n'a aucun fichier
	assert model.empty

	shutil.copy2(REF_DIR / model_file, tmp_output.parent / model_file)
	model = pt._get_astigmatism_model(Path(""))  # Il va reussir, dans le dernier dossier par défaut
	np.testing.assert_array_almost_equal(model.to_numpy(), ref.to_numpy())

	shutil.copy2(REF_DIR / model_file, tmp_output / model_file)
	model = pt._get_astigmatism_model(Path(""))  # Il va reussir, dans le premier dossier par défaut
	np.testing.assert_array_almost_equal(model.to_numpy(), ref.to_numpy())

	model = pt._get_astigmatism_model(REF_DIR / model_file)  # Il va reussir, dans le chemin donné
	np.testing.assert_array_almost_equal(model.to_numpy(), ref.to_numpy())
