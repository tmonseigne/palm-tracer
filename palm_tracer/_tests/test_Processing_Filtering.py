"""Teste le filtrage des localisations et des trajectoires."""

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
@pytest.mark.parametrize("method", [
		pytest.param("localization", id="localizations"), pytest.param("tracking", id="tracks"),
		pytest.param("track_analysis", id="track-analysis")])
def test_filter_bad(qtbot, f, method):
	"""Vérifie le retour vide pour chaque type de résultat sans données."""
	if method == "track_analysis":
		res = f.track_analysis(pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame())
		assert all(frame.empty for frame in res)
	else:
		assert getattr(f, method)(pd.DataFrame()).empty


##################################################
def test_localization(qtbot, f):
	"""Vérifie le filtrage complet."""
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
@pytest.mark.parametrize("select_tracks, select_length, active, expected", [
		pytest.param(True, False, True, 66, id="track-ids"),
		pytest.param(False, True, True, 166, id="length"),
		pytest.param(True, True, True, 9, id="track-ids-and-length"),
		pytest.param(True, True, False, 435, id="filters-disabled")])
def test_tracking(qtbot, f, select_tracks, select_length, active, expected):
	"""Vérifie les critères séparés, leur intersection et la désactivation du filtrage."""
	src = pd.read_csv(INPUT_DIR / "ref" / "stack-blinking.csv")
	filters = f.filters
	filters.tracking["Track"].active = select_tracks
	filters.tracking["Track"].value = "1-9;200-250"
	filters.tracking["Length"].active = select_length
	filters.tracking["Length"].value = [3, 10000]
	filters.active = active
	assert len(f.tracking(src)) == expected


##################################################
@pytest.mark.parametrize("plane_active, filters_active, expected_indices", [
		pytest.param(True, True, [1, 2, 4], id="inclusive-planes"),
		pytest.param(False, True, [0, 1, 2, 3, 4], id="plane-disabled"),
		pytest.param(True, False, [0, 1, 2, 3, 4], id="filters-disabled")])
def test_tracking_plane(qtbot, f, plane_active, filters_active, expected_indices):
	"""Vérifie le filtrage des points par plan sans autre critère et la conservation des données originales."""
	src = pd.DataFrame({"Track": [1, 1, 1, 2, 2], "Plane": [1, 2, 3, 4, 2]})
	original = src.copy()
	f.filters["Plane"].active = plane_active
	f.filters["Plane"].value = [2, 3]
	f.filters.active = filters_active

	pd.testing.assert_frame_equal(f.tracking(src), src.iloc[expected_indices])
	pd.testing.assert_frame_equal(src, original)


##################################################
def test_tracking_plane_before_length(qtbot, f):
	"""Vérifie que la longueur est évaluée sur les points des plans retenus."""
	src = pd.DataFrame({"Track": [1, 1, 1, 2, 2], "Plane": [1, 2, 3, 1, 2]})
	f.filters["Plane"].active = True
	f.filters["Plane"].value = [2, 3]
	f.filters.tracking["Length"].active = True
	f.filters.tracking["Length"].value = [2, 2]

	pd.testing.assert_frame_equal(f.tracking(src), src.iloc[[1, 2]])


##################################################
def test_tracking_plane_empty(qtbot, f):
	"""Vérifie qu'un intervalle sans point produit un résultat vide avec les colonnes originales."""
	src = pd.DataFrame({"Track": [1, 1], "Plane": [1, 2]})
	f.filters["Plane"].active = True
	f.filters["Plane"].value = [3, 4]

	pd.testing.assert_frame_equal(f.tracking(src), src.iloc[:0])


##################################################
@pytest.mark.parametrize("roi_active, limits, expected_tracks", [
		pytest.param(True, [0, 0], {1}, id="fully-outside"),
		pytest.param(True, [100, 100], {4}, id="fully-inside"),
		pytest.param(True, [0, 100], {1, 2, 3, 4}, id="any-occupancy"),
		pytest.param(True, [1, 100], {2, 3, 4}, id="positive-occupancy"),
		pytest.param(True, [20, 80], {2, 3}, id="partially-inside"),
		pytest.param(True, [0, 99], {1, 2, 3}, id="not-fully-inside"),
		pytest.param(False, [100, 100], {1, 2, 3, 4}, id="roi-disabled")])
def test_tracking_time_inside_roi(qtbot, f, roi_active, limits, expected_tracks):
	"""Vérifie la sélection par pourcentage dans la ROI et la conservation intégrale des trajectoires retenues."""
	inside = [[5, 5]] * 4
	outside = [[20, 20]] * 4
	coordinates = outside + inside[:1] + outside[:3] + inside[:2] + outside[:2] + inside
	src = pd.DataFrame({"Track": np.repeat([1, 2, 3, 4], 4), "X": [point[0] for point in coordinates], "Y": [point[1] for point in coordinates]})
	f.rois.set_xy_roi(0, 10, 0, 10, add=False)
	f.filters["ROI"].active = roi_active
	f.filters.tracking["Time Inside ROI"].active = True
	f.filters.tracking["Time Inside ROI"].value = limits

	res = f.tracking(src)

	assert set(res["Track"].unique()) == expected_tracks
	pd.testing.assert_frame_equal(res, src[src["Track"].isin(expected_tracks)])


##################################################
@pytest.mark.parametrize("length_active", [
		pytest.param(False, id="no-other-filter"),
		pytest.param(True, id="length-active")])
def test_tracking_ignores_roi_without_percentage(qtbot, f, length_active):
	"""Vérifie que la ROI active ne retire aucun point lorsque le critère de pourcentage est décoché."""
	src = pd.DataFrame({"Track": [1, 1, 2, 2], "X": [5, 20, 20, 30], "Y": [5, 20, 20, 30]})
	f.rois.set_xy_roi(0, 10, 0, 10, add=False)
	f.filters["ROI"].active = True
	f.filters.tracking["Time Inside ROI"].active = False
	f.filters.tracking["Time Inside ROI"].value = [100, 100]
	f.filters.tracking["Length"].active = length_active
	f.filters.tracking["Length"].value = [2, 2]

	pd.testing.assert_frame_equal(f.tracking(src), src)


##################################################
@pytest.mark.parametrize("scenario, expected", [
		pytest.param("intersection", [47, 9, 9, 9], id="intersection-without-criteria"),
		pytest.param("filtered", [16, 3, 3, 3], id="active-criteria"),
		pytest.param("no_msd", [16, 0, 3, 3], id="missing-msd"),
		pytest.param("no_ind", [16, 3, 0, 3], id="missing-instant-diffusion"),
		pytest.param("no_fit", [21, 4, 4, 0], id="missing-fit"),
		pytest.param("restrictive", [0, 0, 0, 0], id="overly-restrictive-length"),
		pytest.param("disjoint", [0, 0, 0, 0], id="no-common-tracks"),
		pytest.param("disabled", [435, 111, 11, 13], id="filters-disabled")])
def test_track_analysis(qtbot, f, scenario, expected):
	"""Vérifie l'intersection des résultats selon les filtres et les données disponibles."""
	tracks = pd.read_csv(INPUT_DIR / "ref" / "stack-blinking.csv")
	fit = pd.read_csv(INPUT_DIR / "ref" / "stack-blinking-Fit.csv")
	instant_d = pd.read_csv(INPUT_DIR / "ref" / "stack-blinking-InD.csv")
	msd = pd.read_csv(INPUT_DIR / "ref" / "stack-blinking-MSD.csv")
	if scenario != "intersection":
		ft = f.filters.tracking
		ft["Length"].active = True
		ft["Length"].value = [42 if scenario == "restrictive" else 3, 10000]
		ft["Instant D"].active = True
		ft["Instant D"].value = [0.01, 5]
		ft["D Coeff"].active = True
		ft["D Coeff"].value = [1, 5]
		ft["Speed"].active = True
		ft["Speed"].value = [-10, 10]
		ft["Alpha"].active = True
		ft["Confinement"].value = [-10, 10]
	if scenario == "no_msd": msd = pd.DataFrame()
	if scenario == "no_ind": instant_d = pd.DataFrame()
	if scenario == "no_fit": fit = pd.DataFrame()
	if scenario in ("disjoint", "disabled"):
		msd.loc[:, "Track"] += 1000
		instant_d.loc[:, "Track"] += 2000
		fit.loc[:, "Track"] += 3000
	f.filters.active = scenario != "disabled"
	res = f.track_analysis(tracks, msd, instant_d, fit)
	assert [len(frame) for frame in res] == expected
