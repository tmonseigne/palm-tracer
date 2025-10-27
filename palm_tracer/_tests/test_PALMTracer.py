""" Fichier des tests pour la classe PALMTracer """

import os
import shutil
from pathlib import Path
from typing import cast

import pandas as pd
import pytest

from palm_tracer import PALMTracer
from palm_tracer._tests.Utils import is_not_dll_friendly
from palm_tracer.Settings.Groups import FilteringT, TracksCompute
from palm_tracer.Settings.Types import FileList

INPUT_DIR = Path(__file__).parent / "input"
OUTPUT_DIR = Path(__file__).parent / "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_getter_localization(make_napari_viewer):
	"""Test pour le getter de la localisation."""
	pt = PALMTracer()
	df = pt.localizations
	assert df.empty, "Le Dataframe devrait être vide."
	ref1 = pd.DataFrame([1,2])
	pt._df["f_loc"] = ref1
	df = pt.localizations
	assert df.equals(ref1), "Le Dataframe devrait non vide."

##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_getter_tracks(make_napari_viewer):
	"""Test pour le process sans fichiers en entrée."""
	pt = PALMTracer()
	df = pt.tracks
	assert df.empty, "Le Dataframe devrait être vide."
	ref1 = pd.DataFrame([1, 2])
	ref2 = pd.DataFrame([3, 4])
	ref3 = pd.DataFrame([5, 6])
	pt._df["f_trc"] = ref1
	df = pt.tracks
	assert df.equals(ref1), "Le Dataframe devrait non vide."
	pt._df["blk"] = ref2
	df = pt.tracks
	assert df.equals(ref2), "Le Dataframe devrait non vide."
	pt._df["f_blk"] = ref3
	df = pt.tracks
	assert df.equals(ref3), "Le Dataframe devrait non vide."


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_getter_tracks_compute(make_napari_viewer):
	"""Test pour le process sans fichiers en entrée."""
	pt = PALMTracer()
	df = pt.tracks_compute
	assert df["MSD"].empty, "Le Dataframe devrait être vide."
	ref1 = pd.DataFrame([1, 2])
	pt._df["f_trc_MSD"] = ref1
	df = pt.tracks_compute
	assert df["MSD"].equals(ref1), "Le Dataframe devrait non vide."


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_process_no_input(make_napari_viewer):
	"""Test pour le process sans fichiers en entrée."""
	pt = PALMTracer()
	pt.process()
	assert True


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_process_nothing(make_napari_viewer):
	""" Test pour le process avec tout les élément à False et aucun fichier chargeable. """
	pt = PALMTracer()

	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	paths = pt.settings.batch.get_paths()
	for path in paths: shutil.rmtree(path, ignore_errors=True)  # Supprime récursivement le dossier et tout son contenu pour n'avoir rien à charger.
	pt.process()
	# Test d'une visualisation sans données.
	pt.settings.gallery.active = True
	pt.settings.visualization_hr.active = True
	pt.settings.visualization_graph.active = True
	pt.process()	# Test d'une visualisation sans données.
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



##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_process_bad_dll(make_napari_viewer):
	""" Test pour le process avec tout les élément à False et aucun fichier chargeable. """
	pt = PALMTracer()
	pt.palm._dll = None
	pt.process()


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_process_multiple_stack(make_napari_viewer):
	""" Test pour le process avec plusieurs piles. """
	pt = PALMTracer()

	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif", f"{INPUT_DIR}/stack_quadrant.tif"]
	file_list.update_box()
	pt.settings.batch["Mode"].set_value(1)
	pt.process()


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_process_only_localization(make_napari_viewer):
	""" Test pour le process de localisation. """
	pt = PALMTracer()

	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	pt.settings.localization.active = True
	pt.process()
	assert True


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_process_only_localization_spline_bad(make_napari_viewer):
	""" Test pour le process de localisation. """
	pt = PALMTracer()

	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	pt.settings.localization.active = True
	pt.settings.localization["Fit"].set_value(2)
	with pytest.raises(OSError) as exception_info:
		pt.process()
	assert exception_info.type == OSError, "L'erreur relevé n'est pas correcte."


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_process_only_localization_spline(make_napari_viewer):
	""" Test pour le process de localisation. """
	pt = PALMTracer()

	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	pt.settings.localization.active = True
	pt.settings.localization["Fit"].set_value(2)
	pt.settings.localization["Spline Fit"]["File"].set_value(f"{INPUT_DIR}/calibration.mat")
	pt.process()
	assert True


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_process_only_tracking(make_napari_viewer):
	""" Test pour le process de tracking. """
	pt = PALMTracer()

	pt.settings.tracking.active = True
	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	pt.process()
	assert True


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_process_only_tracking_blinking(make_napari_viewer):
	""" Test pour le process de tracking. """
	pt = PALMTracer()

	pt.settings.tracking.active = True
	pt.settings.tracking["Blinking Reconnection"].active = True
	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	pt.process()
	assert True


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_process_only_tracks_compute(make_napari_viewer):
	""" Test pour le process de tracking. """
	pt = PALMTracer()

	tc = cast(TracksCompute, pt.settings.tracks_compute)
	tc.active = True
	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()

	pt.process()

	tc["MSD"].set_value(True)
	pt.process()

	tc["MSD"].set_value(False)
	tc["Instant Diffusion"].set_value(True)
	tc["Fit"].set_value(1)
	pt.process()

	# Supprime récursivement le dossier et tout son contenu pour n'avoir rien à charger.
	paths = pt.settings.batch.get_paths()
	for path in paths: shutil.rmtree(path, ignore_errors=True)
	pt.process()

	# restauration des fichiers
	pt.settings.localization.active = True
	pt.settings.tracking.active = True
	pt.settings.tracking["Blinking Reconnection"].active = True
	pt.process()

	assert True


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_process_only_visualization_hr(make_napari_viewer):
	""" Test pour le process de visualization HR. """
	pt = PALMTracer()

	pt.settings.visualization_hr.active = True
	pt.settings.visualization_hr["Source L"].set_value(0)
	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	pt.process()
	pt.settings.visualization_hr["Type"].set_value(1)
	pt.settings.visualization_hr["Source T"].set_value(0)
	pt.process()

	assert True


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_process_only_visualization_graph(make_napari_viewer):
	""" Test pour le process de visualization HR. """
	pt = PALMTracer()

	pt.settings.visualization_graph.active = True
	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	pt.process()
	assert True


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_process_only_gallery(make_napari_viewer):
	""" Test pour le process de visualization HR. """
	pt = PALMTracer()

	pt.settings.gallery.active = True
	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	pt.process()
	assert True


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_process_all(make_napari_viewer):
	""" Test Basique pour le process complet. """
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
	assert True


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_process_filter_plan(make_napari_viewer):
	""" Test pour le filtrage des plans lors de l'exécution. """
	pt = PALMTracer()

	pt.settings.localization.active = True
	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	pt.settings.filtering["Plane"].active = True
	pt.settings.filtering["Plane"].set_value([2, 3])
	pt.process()
	assert pt.localizations["Plane"].isin([2, 3]).all(), "Le DataFrame contient des valeurs hors [2, 3] dans la colonne Plane."
	assert True


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_process_filter_all_localization(make_napari_viewer):
	""" Test pour le filtrage complet lors de l'exécution. """
	pt = PALMTracer()

	pt.settings.localization.active = True
	# Ajout du fichier
	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()
	# Passage en Guassian Fit ou les Sigma et Theta sont calculés
	pt.settings.localization["Gaussian Fit"]["Mode"].set_value(4)

	pt.settings.filtering["Plane"].active = True
	pt.settings.filtering["Plane"].set_value([1, 9])  # Suppression du dernier plan uniquement
	pt.settings.filtering["Intensity"].active = True
	pt.settings.filtering["Intensity"].set_value([100, 20000])
	pt.settings.filtering["Gaussian Fit"]["MSE"].active = True
	pt.settings.filtering["Gaussian Fit"]["MSE"].set_value([0.01, 10])
	pt.settings.filtering["Gaussian Fit"]["Sigma X"].active = True
	pt.settings.filtering["Gaussian Fit"]["Sigma X"].set_value([0, 10])
	pt.settings.filtering["Gaussian Fit"]["Sigma Y"].active = True
	pt.settings.filtering["Gaussian Fit"]["Sigma Y"].set_value([0, 10])
	pt.settings.filtering["Gaussian Fit"]["Theta"].active = True
	pt.settings.filtering["Gaussian Fit"]["Theta"].set_value([-5, 10])
	pt.settings.filtering["Gaussian Fit"]["Circularity"].active = True
	pt.settings.filtering["Gaussian Fit"]["Z"].active = True
	pt.process()
	pt.settings.filtering["Save"].set_value(True)
	pt.process()

	# Le filtrage ne modifie plus le dataframe original qui garde constamment son statut "complet".
	loc = pt.filter_localizations(pt.localizations)
	ref = [["Plane", 1, 9], ["Integrated Intensity", 100, 20000], ["MSE XY", 0.01, 10],
		   ["Sigma X", 0, 10], ["Sigma Y", 0, 10], ["Theta", -5, 10],
		   ["Circularity", 0, 1], ["Z", -1, 1]]
	for r in ref:
		assert loc[r[0]].between(r[1], r[2]).all(), f"Le DataFrame contient des valeurs hors [{r[1]}:{r[2]}] dans la colonne {r[0]}."


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_process_filter_all_tracking(make_napari_viewer):
	""" Test pour le filtrage complet lors de l'exécution. """
	pt = PALMTracer()

	pt.settings.localization.active = True
	pt.settings.localization["Gaussian Fit"]["Mode"].set_value(1)
	pt.settings.tracking.active = True
	pt.settings.tracking["Blinking Reconnection"].active = True
	pt.settings.tracks_compute.active = True
	pt.settings.tracks_compute["MSD"].set_value(True)
	pt.settings.tracks_compute["Instant Diffusion"].set_value(True)
	pt.settings.tracks_compute["Fit"].set_value(1)
	# Ajout du fichier
	file_list = cast(FileList, pt.settings.batch["Files"])
	file_list.items = [f"{INPUT_DIR}/stack.tif"]
	file_list.update_box()

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
	assert len(pt.tracks) == 143, f"Il reste {len(pt.tracks)} points au lieu de 143 sur les trajectoires."
	assert len(pt.tracks_compute["MSD"]) == 5, f"Il reste {len(pt.tracks_compute['MSD'])} trajectoires au lieu de 5."
	# Filtre massif plus rien à la sortie
	pt.settings.filtering["Tracks"]["Length"].set_value([42, 10000])
	pt.process()

##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_process_filter_outside(make_napari_viewer):
	""" Test pour le filtrage hors exécution. """
	pt = PALMTracer()
	pt.settings.filtering["Tracks"]["Instant D"].active = True
	pt.filter_localizations(pt.localizations)
	pt.filter_tracks(pt.tracks)
	pt.filter_tracks_compute(pt.tracks, pt._df["trc_MSD"], pt._df["trc_InstantD"], pt._df["trc_Fit"])
	pt.filter_tracks_compute(pd.DataFrame(data=[1],columns=["Track"]), pd.DataFrame(data=[2],columns=["Track"]),
							 pd.DataFrame(data=[3],columns=["Track"]),pd.DataFrame(data=[4],columns=["Track"]))
