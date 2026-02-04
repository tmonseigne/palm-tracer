"""Fichier des tests pour la classe PALMTracer"""
import shutil
from typing import cast

import pytest

from palm_tracer import PALMTracer
from palm_tracer._tests.Utils import *
from palm_tracer.Settings.Groups import TracksCompute
from palm_tracer.Settings.Types import FileList
from palm_tracer.Tools import FileIO

OUTPUT_FOLDER = INPUT_DIR / "stack_PALM_tracer"
OUTPUT_FOLDER_2 = INPUT_DIR / "stack_quadrant_PALM_Tracer"


##################################################
def clean_output():
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
	shutil.rmtree(OUTPUT_FOLDER_2, ignore_errors=True)


##################################################
def check_output(folder: Path, csv: Optional[list[int]] = None, log: Optional[list[int]] = None, json: Optional[list[int]] = None,
				 tif: Optional[list[int]] = None, png: Optional[list[int]] = None, clean: bool = True):
	if not folder.is_dir(): pytest.fail("Dossier invalide.")

	for ext, v in {"csv": csv, "log": log, "json": json, "tif": tif, "png": png}.items():
		if v is None: continue
		r = f"*.{ext}"
		n = len(list(folder.glob(r)))
		if len(v) == 1:
			if n != v[0]: pytest.fail(f"Il devrait y avoir {v[0]} fichier(s) '{r}', trouvé(s) : {n}.")
		elif not v[0] <= n <= v[1]: pytest.fail(f"Il devrait y avoir entre {v[0]} et {v[1]} fichiers '{r}', trouvé(s) : {n}.")

	if clean: shutil.rmtree(folder, ignore_errors=True)


##################################################
def test_getter_localization(make_napari_viewer):
	"""Test pour le getter de la localisation."""
	pt = PALMTracer()
	df = pt.localizations
	assert df.empty, "Le Dataframe devrait être vide."
	ref1 = pd.DataFrame([1, 2])
	pt.df["f_loc"] = ref1
	df = pt.localizations
	assert df.equals(ref1), "Le Dataframe devrait non vide."
	pt.reset_filtered()
	df = pt.localizations
	assert df.empty, "Le Dataframe devrait être vide."


##################################################
def test_getter_tracks(make_napari_viewer):
	"""Test pour le process sans fichiers en entrée."""
	pt = PALMTracer()
	df = pt.tracks
	assert df.empty, "Le Dataframe devrait être vide."
	ref1 = pd.DataFrame([1, 2])
	ref2 = pd.DataFrame([3, 4])
	ref3 = pd.DataFrame([5, 6])
	pt.df["f_trc"] = ref1
	df = pt.tracks
	assert df.equals(ref1), "Le Dataframe devrait non vide."
	pt.df["blk"] = ref2
	df = pt.tracks
	assert df.equals(ref2), "Le Dataframe devrait non vide."
	pt.df["f_blk"] = ref3
	df = pt.tracks
	assert df.equals(ref3), "Le Dataframe devrait non vide."
	pt.reset_filtered()
	df = pt.tracks
	assert df.equals(ref2), "Le Dataframe devrait non vide."


##################################################
def test_getter_tracks_compute(make_napari_viewer):
	"""Test pour le process sans fichiers en entrée."""
	pt = PALMTracer()
	df = pt.tracks_compute
	assert df["MSD"].empty, "Le Dataframe devrait être vide."
	ref1 = pd.DataFrame([1, 2])
	pt.df["f_MSD"] = ref1
	df = pt.tracks_compute
	assert df["MSD"].equals(ref1), "Le Dataframe devrait non vide."


##################################################
def test_reset_result(make_napari_viewer):
	"""Test pour le process sans fichiers en entrée."""
	pt = PALMTracer()

	pt.df["loc"] = pd.DataFrame([1, 1])
	pt.df["blk"] = pd.DataFrame([1, 2])
	pt.df["trc"] = pd.DataFrame([1, 3])
	pt.df["MSD"] = pd.DataFrame([1, 4])
	pt.df["InD"] = pd.DataFrame([1, 5])
	pt.df["Fit"] = pd.DataFrame([1, 6])
	pt.df["f_loc"] = pd.DataFrame([1, 7])
	pt.df["f_blk"] = pd.DataFrame([1, 8])
	pt.df["f_trc"] = pd.DataFrame([1, 9])
	pt.df["f_MSD"] = pd.DataFrame([1, 10])
	pt.df["f_InD"] = pd.DataFrame([1, 11])
	pt.df["f_Fit"] = pd.DataFrame([1, 12])

	pt.reset_result()
	for key in pt.df:
		assert pt.df[key].empty, "Le Dataframe devrait être vide."


##################################################
def test_reset_filtered(make_napari_viewer):
	"""Test pour le process sans fichiers en entrée."""
	pt = PALMTracer()

	pt.df["loc"] = pd.DataFrame([1, 1])
	pt.df["blk"] = pd.DataFrame([1, 2])
	pt.df["trc"] = pd.DataFrame([1, 3])
	pt.df["MSD"] = pd.DataFrame([1, 4])
	pt.df["InD"] = pd.DataFrame([1, 5])
	pt.df["Fit"] = pd.DataFrame([1, 6])
	pt.df["f_loc"] = pd.DataFrame([1, 7])
	pt.df["f_blk"] = pd.DataFrame([1, 8])
	pt.df["f_trc"] = pd.DataFrame([1, 9])
	pt.df["f_MSD"] = pd.DataFrame([1, 10])
	pt.df["f_InD"] = pd.DataFrame([1, 11])
	pt.df["f_Fit"] = pd.DataFrame([1, 12])

	pt.reset_filtered()
	for key in pt.df:
		if key.startswith("f_"): assert pt.df[key].empty, "Le Dataframe devrait être vide."
		else: assert not pt.df[key].empty, "Le Dataframe doit subsiter."


##################################################
def test_update_filtered(make_napari_viewer):
	"""Test pour le process sans fichiers en entrée."""
	clean_output()
	pt = PALMTracer()
	pt.update_filtered()  # Tout est vide
	pt.settings.filtering["Save"].set_value(True)
	pt.update_filtered()  # Tout est vide, mais je demande à enregistrer

	pt.settings.localization.active = True
	pt.settings.tracking.active = True
	pt.settings.tracking["Blinking Reconnection"].active = True
	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	pt.process()
	pt.update_filtered()  # Maintenant, il va recalculer les filtres (il n'y en aura aucun de toute façon).

	# Un fichier meta + un localization + un tracking + un reconnecté = 4
	# (1 à 3) * 3 fichiers de tableaux filtrés = entre 7 et 13 csv
	check_output(OUTPUT_FOLDER, csv=[7, 13], log=[1], json=[1])


##################################################
def test_load_bad_dll(make_napari_viewer):
	"""Test pour le process avec tout les élément à False et aucun fichier chargeable."""
	pt = PALMTracer()
	pt.palm._dll = None
	pt.load("")


##################################################
def test_load_nothing(make_napari_viewer):
	"""Test pour le chargement avec fichier mais sans settings."""
	pt = PALMTracer()
	pt.load("bad path")


##################################################
def test_load(make_napari_viewer):
	"""Test pour le chargement avec fichier mais sans settings."""
	clean_output()
	pt = PALMTracer()
	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	pt.settings.localization.active = True
	pt.process()
	pt.load()

	assert not pt.df["loc"].empty, "Le Dataframe de localization ne devrait pas être vide"
	assert pt.df["f_loc"].empty, "Le Dataframe de localizations filtré devrait être vide."

	# Un fichier meta + un localization
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1])


##################################################
def test_process_no_input(make_napari_viewer):
	"""Test pour le process sans fichiers en entrée."""
	clean_output()
	pt = PALMTracer()
	pt.process()


##################################################
def test_process_nothing(make_napari_viewer):
	"""Test pour le process avec tout les élément à False et aucun fichier chargeable."""
	clean_output()
	pt = PALMTracer()

	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	pt.process()
	# Test d'une visualisation sans données.
	pt.settings.gallery.active = True
	pt.settings.visualization_hr.active = True
	pt.settings.visualization_graph.active = True
	pt.process()  # Test d'une visualisation sans données.
	pt.settings.visualization_hr["Type"].set_value(1)
	pt.process()
	# Test d'un calcul sur trajectoires sans données.
	pt.settings.gallery.active = False
	pt.settings.visualization_hr.active = False
	pt.settings.visualization_graph.active = False
	pt.settings.tracks_compute.active = True
	pt.process()
	# Test d'un calcul de trajectoires sans données.
	pt.settings.tracks_compute.active = False
	pt.settings.tracking.active = True
	pt.process()

	n_process = 5  # Nombre de fois ou process à été lancé
	# suivant le timestamp, il est fort problable que seul le dernier process conserve ses data mais le hasard du lancement fait que
	# chaque process peut démarrer avec une seconde de décallage et donc un timestamp différent.
	check_output(OUTPUT_FOLDER, csv=[1, n_process], log=[1, n_process], json=[1, n_process])


##################################################
def test_process_bad_dll(make_napari_viewer):
	"""Test pour le process avec tout les élément à False et aucun fichier chargeable."""
	pt = PALMTracer()
	pt.palm._dll = None
	pt.process()


##################################################
def test_process_multiple_stack(make_napari_viewer):
	"""Test pour le process avec plusieurs piles."""
	clean_output()
	pt = PALMTracer()

	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif", f"{INPUT_DIR}/stack_quadrant.tif"]
	file_list.update_box()
	pt.settings.batch["Mode"].set_value(1)
	pt.process()
	check_output(OUTPUT_FOLDER, csv=[1], log=[1], json=[1])
	check_output(OUTPUT_FOLDER_2, csv=[1], log=[1], json=[1])


##################################################
def test_process_only_localization(make_napari_viewer):
	"""Test pour le process de localisation."""
	clean_output()
	pt = PALMTracer()

	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	pt.settings.localization.active = True
	pt.process()
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1])


##################################################
def test_process_only_localization_spline_bad(make_napari_viewer):
	"""Test pour le process de localisation."""
	clean_output()
	pt = PALMTracer()

	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	pt.settings.localization.active = True
	pt.settings.localization["Fit"].set_value(2)
	with pytest.raises(OSError) as exception_info:
		pt.process()
	assert exception_info.type == OSError, "L'erreur relevé n'est pas correcte."
	check_output(OUTPUT_FOLDER, csv=[1], log=[1], json=[1])  # Il va créer le meta mais pas le fichier de localization


##################################################
def test_process_only_localization_spline(make_napari_viewer):
	"""Test pour le process de localisation."""
	clean_output()
	pt = PALMTracer()

	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	pt.settings.localization.active = True
	pt.settings.localization["Fit"].set_value(2)
	pt.settings.localization["Spline Fit"]["File"].set_value(f"{INPUT_DIR}/calibration.mat")
	pt.process()
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1])


##################################################
def test_process_only_tracking(make_napari_viewer):
	"""Test pour le process de tracking."""
	clean_output()
	pt = PALMTracer()

	# Ajout d'un fichier de localisations
	os.makedirs(OUTPUT_FOLDER, exist_ok=True)
	src = INPUT_DIR / "ref" / "stack-localizations-103.6_True_4_1.0_0.0_7.csv"
	dst = OUTPUT_FOLDER / f"localizations-{FileIO.get_timestamp_for_files()}.csv"
	shutil.copy2(src, dst)

	pt.settings.tracking.active = True
	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	pt.process()
	assert len(pt.localizations) == len(pt.tracks), "Nombre de points différents entre la localization et le tracking."
	check_output(OUTPUT_FOLDER, csv=[3], log=[1], json=[1])


##################################################
def test_process_only_tracking_blinking(make_napari_viewer):
	"""Test pour le process de tracking."""
	clean_output()
	pt = PALMTracer()

	# Ajout d'un fichier de localisations
	os.makedirs(OUTPUT_FOLDER, exist_ok=True)
	src = INPUT_DIR / "ref" / "stack-localizations-103.6_True_4_1.0_0.0_7.csv"
	dst = OUTPUT_FOLDER / f"localizations-{FileIO.get_timestamp_for_files()}.csv"
	shutil.copy2(src, dst)

	pt.settings.tracking.active = True
	pt.settings.tracking["Blinking Reconnection"].active = True
	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	pt.process()
	assert len(pt.localizations) == len(pt.tracks), "Nombre de points différents entre la localization et le tracking (reconnecté)."
	check_output(OUTPUT_FOLDER, csv=[4], log=[1], json=[1])


##################################################
def test_process_only_tracks_compute(make_napari_viewer):
	"""Test pour le process de tracking."""
	clean_output()
	pt = PALMTracer()

	# Ajout d'un fichier de tracking
	os.makedirs(OUTPUT_FOLDER, exist_ok=True)
	src = INPUT_DIR / "ref" / "stack-tracking-103.6_True_4_1.0_0.0_7-5_2_10_0.5.csv"
	dst = OUTPUT_FOLDER / f"tracking-{FileIO.get_timestamp_for_files()}.csv"
	shutil.copy2(src, dst)

	tc = cast(TracksCompute, pt.settings.tracks_compute)
	tc.active = True
	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()

	pt.process()
	# Aucun fichier Ajouté juste meta et le tracking copié
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1], clean=False)

	tc["MSD"].set_value(True)
	pt.process()
	# Ajout de fichier MSD (et peut être un meta, json et log)
	check_output(OUTPUT_FOLDER, csv=[3, 4], log=[1, 2], json=[1, 2], clean=False)

	tc["MSD"].set_value(False)
	tc["Instant Diffusion"].set_value(True)
	tc["Fit"].set_value(1)
	pt.process()
	# Ajout de fichier 2 ou 3 fichiers csv et 0 ou 1 fichiers meta, json et log
	check_output(OUTPUT_FOLDER, csv=[5, 7], log=[1, 3], json=[1, 3])


##################################################
def test_process_only_visualization_hr(make_napari_viewer):
	"""Test pour le process de visualization HR."""
	clean_output()
	pt = PALMTracer()

	# Ajout des fichiers de localisations et trajectoires
	os.makedirs(OUTPUT_FOLDER, exist_ok=True)
	src = INPUT_DIR / "ref" / "stack-localizations-103.6_True_4_1.0_0.0_7.csv"
	dst = OUTPUT_FOLDER / f"localizations-{FileIO.get_timestamp_for_files()}.csv"
	shutil.copy2(src, dst)
	src = INPUT_DIR / "ref" / "stack-tracking-103.6_True_4_1.0_0.0_7-5_2_10_0.5.csv"
	dst = OUTPUT_FOLDER / f"tracking-{FileIO.get_timestamp_for_files()}.csv"
	shutil.copy2(src, dst)

	pt.settings.visualization_hr.active = True
	pt.settings.visualization_hr["Source L"].set_value(0)
	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	pt.process()
	check_output(OUTPUT_FOLDER, csv=[3], log=[1], json=[1], png=[8], clean=False)

	pt.settings.visualization_hr["Type"].set_value(1)
	pt.settings.visualization_hr["Source T"].set_value(0)
	pt.process()

	# Il a Ajouté un fichier tracking_Fit qu'il a du calculer et un tracking_hr_color, pour les images 8 Sources pour les loc, 5 pour les track
	check_output(OUTPUT_FOLDER, csv=[5, 6], log=[1, 2], json=[1, 2], png=[13])


##################################################
def test_process_only_visualization_graph(make_napari_viewer):
	"""Test pour le process de visualization de graph."""
	clean_output()
	pt = PALMTracer()

	# Ajout des fichiers de localisation et tracking
	os.makedirs(OUTPUT_FOLDER, exist_ok=True)
	src = INPUT_DIR / "ref" / "stack-localizations-103.6_True_4_1.0_0.0_7.csv"
	dst = OUTPUT_FOLDER / f"localizations-{FileIO.get_timestamp_for_files()}.csv"
	shutil.copy2(src, dst)
	src = INPUT_DIR / "ref" / "stack-tracking-103.6_True_4_1.0_0.0_7-5_2_10_0.5.csv"
	dst = OUTPUT_FOLDER / f"tracking-{FileIO.get_timestamp_for_files()}.csv"
	shutil.copy2(src, dst)

	pt.settings.visualization_graph.active = True
	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	pt.process()
	check_output(OUTPUT_FOLDER, csv=[3], log=[1], json=[1], png=[18])


##################################################
def test_process_only_gallery(make_napari_viewer):
	"""Test pour le process de visualization HR."""
	clean_output()
	pt = PALMTracer()

	# Ajout du fichier de localisation
	os.makedirs(OUTPUT_FOLDER, exist_ok=True)
	src = INPUT_DIR / "ref" / "stack-localizations-103.6_True_4_1.0_0.0_7.csv"
	dst = OUTPUT_FOLDER / f"localizations-{FileIO.get_timestamp_for_files()}.csv"
	shutil.copy2(src, dst)

	pt.settings.gallery.active = True
	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	pt.process()

	# dimension 270 (30 ROI / lignes(colonnes) * taille de ROI de 9) et 1 frame (30 * 30 = 900 / frame et environ 450 en entrée)
	res, ref = FileIO.open_tif(str(list(OUTPUT_FOLDER.glob("*.tif"))[0])).shape, (1, 270, 270)
	assert res == ref, f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1], tif=[1])


##################################################
def test_process_all(make_napari_viewer):
	"""Test Basique pour le process complet."""
	clean_output()
	pt = PALMTracer()

	pt.settings.localization.active = True
	pt.settings.localization["Fit"].set_value(1)
	pt.settings.localization["Gaussian Fit"]["Mode"].set_value(3)
	pt.settings.tracking.active = True
	pt.settings.tracking["Blinking Reconnection"].active = True
	pt.settings.tracks_compute.active = True
	pt.settings.tracks_compute["MSD"].set_value(True)
	pt.settings.tracks_compute["Instant Diffusion"].set_value(True)
	pt.settings.tracks_compute["Fit"].set_value(1)
	pt.settings.gallery.active = True
	pt.settings.visualization_hr.active = True
	pt.settings.visualization_graph.active = True
	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	pt.process()

	check_output(OUTPUT_FOLDER, csv=[7], log=[1], json=[1], tif=[1], png=[19])


##################################################
def test_process_filter_plan(make_napari_viewer):
	"""Test pour le filtrage des plans lors de l'exécution."""
	clean_output()
	pt = PALMTracer()

	# Ajout du fichier de localisation
	os.makedirs(OUTPUT_FOLDER, exist_ok=True)
	src = INPUT_DIR / "ref" / "stack-localizations-103.6_True_4_1.0_0.0_7.csv"
	dst = OUTPUT_FOLDER / f"localizations-{FileIO.get_timestamp_for_files()}.csv"
	shutil.copy2(src, dst)

	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	pt.settings.filtering["Plane"].active = True
	pt.settings.filtering["Plane"].set_value([2, 3])
	pt.process()

	assert pt.localizations["Plane"].isin([2, 3]).all(), "Le DataFrame contient des valeurs hors [2, 3] dans la colonne Plane."
	res, ref = pt.localizations.shape, (95, 18)
	assert res == ref, f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"
	# création des 3 fichiers normaux (meta, settings, log) aucun changement pour le fichier loc pas d'enregistrement des données filtrées
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1])


##################################################
def test_process_filter_all_localization(make_napari_viewer):
	"""Test pour le filtrage complet lors de l'exécution."""
	clean_output()
	pt = PALMTracer()

	# Ajout du fichier de localisation
	os.makedirs(OUTPUT_FOLDER, exist_ok=True)
	src = INPUT_DIR / "ref" / "stack-localizations-103.6_True_4_1.0_0.0_7.csv"
	dst = OUTPUT_FOLDER / f"localizations-{FileIO.get_timestamp_for_files()}.csv"
	shutil.copy2(src, dst)

	# Ajout du fichier
	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()

	pt.settings.filtering["Plane"].active = True
	pt.settings.filtering["Plane"].set_value([1, 9])  # Suppression du dernier plan uniquement 411/451 : 40 suppression(s)
	pt.settings.filtering["Localization"]["Intensity"].active = True
	pt.settings.filtering["Localization"]["Intensity"].set_value([100, 20000])  # 391/411 : 20 suppression(s)
	pt.settings.filtering["Localization"]["Sigma X"].active = True
	pt.settings.filtering["Localization"]["Sigma X"].set_value([0, 10])  # Aucune suppression
	pt.settings.filtering["Localization"]["Sigma Y"].active = True
	pt.settings.filtering["Localization"]["Sigma Y"].set_value([0, 10])  # Aucune suppression
	pt.settings.filtering["Localization"]["Circularity"].active = True  # Aucune suppression
	pt.settings.filtering["Localization"]["Theta"].active = True
	pt.settings.filtering["Localization"]["Theta"].set_value([-5, 5])  # 366/391 : 25 suppression(s)
	pt.settings.filtering["Localization"]["Z"].active = True  # Aucune suppression
	pt.settings.filtering["Localization"]["MSE XY"].active = True
	pt.settings.filtering["Localization"]["MSE XY"].set_value([0.01, 10])  # 365/366 : 1 suppression(s)
	# pt.settings.filtering["Localization"]["MSE Z"].active = True # La colonne est à -1 le filtre est forcément sur un nombre positif
	# pt.settings.filtering["Localization"]["MSE Z"].set_value([0, 10])
	pt.process()
	pt.settings.filtering["Save"].set_value(True)
	pt.process()  # Second passage avec enregistrement

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
def test_process_filter_all_tracking(make_napari_viewer):
	"""Test pour le filtrage complet lors de l'exécution."""
	clean_output()
	pt = PALMTracer()

	# Ajout du fichier de trajectoires
	os.makedirs(OUTPUT_FOLDER, exist_ok=True)
	src = INPUT_DIR / "ref" / "stack-tracking-103.6_True_4_1.0_0.0_7-5_2_10_0.5.csv"
	dst = OUTPUT_FOLDER / f"tracking-{FileIO.get_timestamp_for_files()}.csv"
	shutil.copy2(src, dst)

	# Ajout du fichier
	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()

	pt.process()
	res, ref = len(pt.tracks), 222
	assert res == ref, f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"
	check_output(OUTPUT_FOLDER, csv=[2], log=[1], json=[1], clean=False)

	pt.settings.filtering["Tracks"]["Length"].active = True
	pt.settings.filtering["Tracks"]["Length"].set_value([3, 10000])  # 52/222 : 170 suppression(s)
	pt.settings.filtering["Save"].set_value(True)
	pt.process()

	res, ref = len(pt.tracks), 52
	assert res == ref, f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"
	check_output(OUTPUT_FOLDER, csv=[3, 4], log=[1, 2], json=[1, 2])


##################################################
def test_process_filter_all_tracks_compute(make_napari_viewer):
	"""Test pour le filtrage complet lors de l'exécution."""
	clean_output()
	pt = PALMTracer()

	pt.settings.localization.active = True
	pt.settings.localization["Gaussian Fit"]["Mode"].set_value(1)
	pt.settings.tracking.active = True
	pt.settings.tracking["Blinking Reconnection"].active = True

	# Ajout du fichier
	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()

	pt.settings.tracks_compute.active = True
	pt.settings.tracks_compute["MSD"].set_value(True)
	pt.settings.tracks_compute["Instant Diffusion"].set_value(True)
	pt.settings.tracks_compute["Fit"].set_value(1)
	pt.settings.tracks_compute["Fit Length"].set_value(2)

	pt.settings.filtering["Tracks"]["Length"].active = True
	pt.settings.filtering["Tracks"]["Length"].set_value([3, 10000])
	pt.settings.filtering["Tracks"]["Instant D"].active = True
	pt.settings.filtering["Tracks"]["Instant D"].set_value([0.01, 5])
	pt.settings.filtering["Tracks"]["D Coeff"].active = True
	pt.settings.filtering["Tracks"]["D Coeff"].set_value([1, 5])
	pt.settings.filtering["Tracks"]["Speed"].active = True
	pt.settings.filtering["Tracks"]["Speed"].set_value([-10, 10])
	pt.settings.filtering["Tracks"]["Alpha"].active = True
	pt.settings.filtering["Tracks"]["Confinement"].set_value([-10, 10])
	pt.process()
	pt.settings.filtering["Save"].set_value(True)
	pt.process()

	# Vérification manuelle à l'heure actuelle
	assert len(pt.tracks) == 55, f"Il reste {len(pt.tracks)} points au lieu de 55 sur les trajectoires."
	assert len(pt.tracks_compute["MSD"]) == 14, f"Il reste {len(pt.tracks_compute['MSD'])} trajectoires au lieu de 14."
	# Filtre massif plus rien à la sortie
	pt.settings.filtering["Tracks"]["Length"].set_value([42, 10000])
	pt.process()
	assert len(pt.df["f_trc"]) == 0, f"Il reste {len(pt.tracks)} points au lieu de 0 sur les trajectoires."
	assert len(pt.df["f_MSD"]) == 0, f"Il reste {len(pt.tracks_compute['MSD'])} trajectoires au lieu de 0."


##################################################
def test_process_filter_outside(make_napari_viewer):
	"""Test pour le filtrage hors exécution."""
	clean_output()
	pt = PALMTracer()
	pt.settings.filtering["Tracks"]["Instant D"].active = True
	assert pt.filter_localizations(pt.localizations).empty
	assert pt.filter_tracks(pt.tracks).empty
	res = pt.filter_tracks_compute(pt.tracks, pt.df["MSD"], pt.df["InD"], pt.df["Fit"])
	for r in res: assert r.empty
	res = pt.filter_tracks_compute(pd.DataFrame(data=[1], columns=["Track"]), pd.DataFrame(data=[2], columns=["Track"]),
								   pd.DataFrame(data=[3], columns=["Track"]), pd.DataFrame(data=[4], columns=["Track"]))

	o_trc, o_msd, o_ind, o_fit = res
	assert len(o_trc) == 1  # Il a conservé son unique track même si elle n'est pas présente ailleurs. ce comportement est sensé être impossible à avoir.
	assert o_msd.empty
	assert o_ind.empty
	assert o_fit.empty


##################################################
def test_add_color(make_napari_viewer):
	pt = PALMTracer()
	file = "tracking2"
	path = Path(f"{INPUT_DIR}/{file}.csv")
	df = pd.read_csv(path)

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
	pt.settings.tracks_compute["Fit Length"].set_value(2)

	ref = [1, 1, 1, 65535, 65535, 65535]
	res = pt.add_color_to_tracks(df, "Total Intensity")  # fit Compute
	assert (res["Color"].tolist() == ref)

	res = pt.add_color_to_tracks(df, "Total Intensity")  # fit Compute already compute
	assert (res["Color"].tolist() == ref)
