"""
Fichier des tests pour la classe PALMTracer

.. note:: Il est fréquent que la vérificaiton du log ne se fasse qu'au nombre de lignes, car au moins 15 lignes à chaque process.
"""
import pytest

from palm_tracer._tests.Utils import *
from palm_tracer.Processing import Filtering
from palm_tracer.Settings import ROIManager
from palm_tracer.Settings.Groups import Filters
from palm_tracer.Settings.Types import CheckInt, SpinInt

OUTPUT_FOLDER = INPUT_DIR / "stack_PALM_Tracer"
OUTPUT_FOLDER_2 = INPUT_DIR / "stack_quadrant_PALM_Tracer"


@pytest.fixture
def f() -> Filtering:
	"""Construit un gestionnaire avec une sélection active et un ratio HR de 4."""
	filters = Filters()
	manager = ROIManager(cast(CheckInt, filters["ROI"]), SpinInt("Up scaling ratio", "", 4, [1, 256], 2))
	manager.set_size(256, 128)
	return Filtering(filters, manager)


##################################################
def test_filter_bad(qtbot, f):
	"""Test pour le filtrage complet."""
	res = f.localization(pd.DataFrame())
	assert res.empty, "Un dataframe vide doit être retourné."
	res = f.tracking(pd.DataFrame())
	assert res.empty, "Un dataframe vide doit être retourné."
	res = f.tracks_compute(pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame())
	for r in res: assert r.empty, "Un dataframe vide doit être retourné."


##################################################
def test_localization(qtbot, f):
	"""Test pour le filtrage complet."""
	src = pd.read_csv(INPUT_DIR / "ref" / "stack-localizations-103.6_True_4_1.0_0.0_7.csv")
	f.filters["Plane"].active = True
	f.filters["Plane"].value = [1, 9]  # .	Suppression du dernier plan uniquement 411/451 : 40 suppression(s)
	fl = f.filters.localization
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
	fl["MSE XY"].value = [0.05, 10]  # .	345/346 : 1 suppression(s)
	# fl["MSE Z"].active = True # .			La colonne est à -1 le filtre est forcément sur un nombre positif donc on passerait à 0 éléments
	f.rois.set_xy_roi(0, 128, 0, 128)  # .	183/345
	f.filters["ROI"].active = True
	f.filters["ROI"].value = 1

	res = f.localization(src)

	ref = [["Plane", 1, 9], ["X", 0, 128], ["Y", 0, 128], ["Integrated Intensity", 100, 20000], ["MSE XY", 0.01, 10],
		   ["Sigma X", 0, 10], ["Sigma Y", 0, 10], ["Theta", -60, 60],
		   ["Circularity", 0, 1], ["Z", -1, 1]]
	for r in ref:
		assert res[r[0]].between(r[1], r[2]).all(), f"Le DataFrame contient des valeurs hors [{r[1]}:{r[2]}] dans la colonne {r[0]}."

	res, ref = len(res), 183
	assert res == ref, f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"

	fl["MSE Z"].active = True  # .			La colonne est à -1 le filtre est forcément sur un nombre positif donc on passerait à 0 éléments
	res = f.localization(src)
	assert res.empty, "Un dataframe vide doit être retourné."

	f.filters.active = False
	res = f.localization(src)
	res, ref = len(res), len(src)
	assert res == ref, f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"


##################################################
def test_tracking(qtbot, f):
	"""Test pour le filtrage des plans."""
	src = pd.read_csv(INPUT_DIR / "ref" / "stack-blinking.csv")
	filters = f.filters
	filters.tracking["Length"].active = True
	filters.tracking["Length"].value = [3, 10000]  # 166/435 : 269 suppression(s)

	res = f.tracking(src)
	res, ref = len(res), 166
	assert res == ref, f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"

	f.filters.active = False
	res = f.tracking(src)
	res, ref = len(res), len(src)
	assert res == ref, f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"


##################################################
def test_tracks_compute(qtbot, f):
	"""Test pour le filtrage des plans."""
	tracks = pd.read_csv(INPUT_DIR / "ref" / "stack-blinking.csv")
	fit = pd.read_csv(INPUT_DIR / "ref" / "stack-blinking-Fit.csv")
	instant_d = pd.read_csv(INPUT_DIR / "ref" / "stack-blinking-InD.csv")
	msd = pd.read_csv(INPUT_DIR / "ref" / "stack-blinking-MSD.csv")

	res = f.tracks_compute(tracks, msd, instant_d, fit)
	ref = [47, 9, 9, 9]  # Même sans filtre, il ne conserve que l'intersection (36, 46, 57, 71, 75, 87, 89, 138, 154).
	for i in range(len(ref)): assert len(res[i]) == ref[i], f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {len(res[i])}"

	ft = f.filters.tracking
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
	res = f.tracks_compute(tracks, msd, instant_d, fit)
	ref = [16, 3, 3, 3]
	for i in range(len(ref)): assert len(res[i]) == ref[i], f"Résultat incorrect pour {i}.\tAttendu : {ref}\tObtenu : {len(res[i])}"

	# Lancement avec des éléments vides
	res = f.tracks_compute(tracks, pd.DataFrame(), instant_d, fit)
	ref = [16, 0, 3, 3]
	for i in range(len(ref)): assert len(res[i]) == ref[i], f"Résultat incorrect pour {i}.\tAttendu : {ref}\tObtenu : {len(res[i])}"

	res = f.tracks_compute(tracks, msd, pd.DataFrame(), fit)
	ref = [16, 3, 0, 3]
	for i in range(len(ref)): assert len(res[i]) == ref[i], f"Résultat incorrect pour {i}.\tAttendu : {ref}\tObtenu : {len(res[i])}"

	res = f.tracks_compute(tracks, msd, instant_d, pd.DataFrame())
	ref = [21, 4, 4, 0]
	for i in range(len(ref)): assert len(res[i]) == ref[i], f"Résultat incorrect pour {i}.\tAttendu : {ref}\tObtenu : {len(res[i])}"

	# Filtres trop restrictifs
	ft["Length"].value = [42, 10000]
	res = f.tracks_compute(tracks, msd, instant_d, fit)
	ref = [0, 0, 0, 0]
	for i in range(len(ref)): assert len(res[i]) == ref[i], f"Résultat incorrect pour {i}.\tAttendu : {ref}\tObtenu : {len(res[i])}"
