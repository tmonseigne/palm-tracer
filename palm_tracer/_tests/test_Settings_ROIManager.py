"""Teste la gestion et la synchronisation des zones d'intérêt."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from napari.layers import Shapes

from palm_tracer.Settings import ROI, ROIManager
from palm_tracer.Settings.Types import CheckInt, CheckRangeInt, SpinInt


@pytest.fixture
def manager() -> ROIManager:
	"""Construit un gestionnaire avec une sélection active et un ratio HR de 4."""
	return ROIManager(CheckInt("ROI", "", 1, [1, 1]), SpinInt("Up scaling ratio", "", 4, [1, 256], 2))


# ==================================================
# region Accesseurs
# ==================================================
##################################################
def test_rois(manager: ROIManager):
	"""Vérifie la gestion de la collection de zones d'intérêt."""
	manager.rois = [ROI("rectangle", np.zeros((4, 2)))]
	assert manager.roi_selection.limits == [1, 1]
	manager.rois = [ROI("rectangle", np.zeros((4, 2))), ROI("ellipse", np.ones((4, 2)))]
	assert manager.roi_selection.limits == [1, 2]
	np.testing.assert_allclose(manager.rois[0].data, [[0, 0], [0, 0], [0, 0], [0, 0]])
	np.testing.assert_allclose(manager.rois[1].data, [[1, 1], [1, 1], [1, 1], [1, 1]])


##################################################
def test_set_xy_roi(manager: ROIManager):
	"""Vérifie la définition d'une zone d'intérêt XY."""
	manager.rois = [ROI("ellipse", np.ones((4, 2)))]
	manager.set_xy_roi(10, 20, 30, 40, add=False)

	assert len(manager.rois) == 1
	assert manager.rois[0].type == "rectangle"
	np.testing.assert_allclose(manager.rois[0].data, [[30, 10], [30, 20], [40, 20], [40, 10]])

	manager.set_xy_roi(4.0, 5.0, 6.0, 7.0, add=True)
	assert len(manager.rois) == 2


##################################################
def test_layer(manager: ROIManager):
	"""Vérifie la synchronisation du calque de zones d'intérêt."""
	assert manager.layer_main is None and manager.layer_hr is None
	manager.layer_main = Shapes()
	manager.layer_hr = Shapes()
	assert isinstance(manager.layer_main, Shapes) and isinstance(manager.layer_hr, Shapes)


# ==================================================
# endregion Accesseurs
# ==================================================

# ==================================================
# region Synchronisation
# ==================================================
##################################################
def test_update_main(manager: ROIManager):
	"""Vérifie la mise à jour de la zone d'intérêt principale."""
	manager.update_from_main()  # Aucun layer
	manager.update_main()  # Aucun layer
	manager.layer_main = Shapes()
	manager.update_from_main()  # Aucune forme, mais aucun soucis
	manager.rois = [ROI("rectangle", np.zeros((4, 2)))]  # Ajout d'une forme
	manager.update_main()  # Mise à jour du calque principal.
	np.testing.assert_allclose(manager.layer_main.data, [[[0, 0], [0, 0], [0, 0], [0, 0]]])  # Le callback à appelé update_from_main
	manager.layer_main.selected_data = {0}  # Le callback à appelé on_main_selection_changed


##################################################
def test_update_hr(manager: ROIManager):
	"""Vérifie la mise à jour de la zone d'intérêt haute résolution."""
	manager.update_from_hr()  # Aucun layer
	manager.update_hr()  # Aucun layer
	manager.layer_hr = Shapes()
	manager.update_from_hr()  # Aucune forme, mais aucun soucis
	manager.rois = [ROI("rectangle", np.zeros((4, 2)))]  # Ajout d'une forme
	manager.update_hr()  # Mise à jour du calque HR.
	np.testing.assert_allclose(manager.layer_hr.data, [[[0, 0], [0, 0], [0, 0], [0, 0]]])  # Le callback à appelé update_from_hr
	manager.layer_hr.selected_data = {0}  # Le callback à appelé on_hr_selection_changed


##################################################
def test_update_roi_selection(manager: ROIManager):
	# Appel du callback _on_roi_selection_changed
	"""Vérifie la mise à jour de la sélection des zones d'intérêt."""
	manager.roi_selection.value = 0  # Aucune ROI donc rejet, car hors limite.
	manager.rois = [ROI("rectangle", np.zeros((4, 2)))]  # Ajout d'une forme
	manager.roi_selection.value = 1  # Bonne selection, mais aucun layer.
	manager.layer_main = Shapes()
	manager.roi_selection.value = 1  # Bonne selection, mais aucun layer.
	manager.layer_hr = Shapes()
	manager.roi_selection.value = 1  # Bonne selection, mais aucun layer.


# ==================================================
# endregion Synchronisation
# ==================================================

# ==================================================
# region Entrées-sorties
# ==================================================
##################################################
def test_dict(manager: ROIManager):
	"""Vérifie la sérialisation du gestionnaire de zones d'intérêt."""
	manager.rois = [ROI("rectangle", np.zeros((4, 2)))]  # Ajout d'une forme
	res = manager.to_dict_list()
	assert len(res) == 1
	assert res[0]["type"] == "rectangle"
	np.testing.assert_allclose(res[0]["data"], [[0, 0], [0, 0], [0, 0], [0, 0]])
	manager.rois = []
	manager.from_dict_list(res)
	assert len(manager.rois) == 1
	assert manager.rois[0].type == "rectangle"
	np.testing.assert_allclose(manager.rois[0].data, [[0, 0], [0, 0], [0, 0], [0, 0]])


# ==================================================
# endregion Entrées-sorties
# ==================================================

# ==================================================
# region Divers
# ==================================================
##################################################
def test_roi_limits(manager: ROIManager):
	"""Vérifie le calcul des limites des zones d'intérêt."""
	manager.set_size(100, 80)
	manager.rois = [ROI("rectangle", np.array([[-5.2, -10.8], [-5.2, 120.4], [90.7, 120.4], [90.7, -10.8]]))]
	manager.roi_selection.value = 0
	assert manager.get_roi_limits() == (0, 100, 0, 80)
	manager.roi_selection.value = 1
	assert manager.get_roi_limits() == (0, 100, 0, 80)

	manager.set_xy_roi(20, 40, 10, 30, add=False)
	manager.roi_selection.active = True
	assert manager.get_roi_limits() == (20, 40, 10, 30)


##################################################
@pytest.mark.parametrize("limits, expected", [
		pytest.param([0, 0], (0, 100, 0, 80), id="outside"),
		pytest.param([20, 80], (20, 40, 10, 30), id="crossing"),
		pytest.param([0, 99], (20, 40, 10, 30), id="not-fully-inside"),
		pytest.param([100, 100], (20, 40, 10, 30), id="fully-inside")])
def test_hr_limits(manager: ROIManager, limits: list[int], expected: tuple[int, int, int, int]):
	"""Adapte le cadre HR selon la présence possible de points de trajectoire hors de la ROI."""
	manager.set_size(100, 80)
	manager.set_xy_roi(20, 40, 10, 30, add=False)
	manager.roi_selection.active = True
	time_filter = CheckRangeInt("Time Inside ROI", "", limits, [0, 100])
	time_filter.active = True

	assert manager.get_hr_limits(time_filter) == expected
	assert manager.hr_box == expected
	assert manager.get_hr_limits(None) == (20, 40, 10, 30)
	assert manager.hr_box == (20, 40, 10, 30)


##################################################
@pytest.mark.parametrize("gaussian, expected", [
		pytest.param(None, (15, 35, 15, 35), id="spots"),
		pytest.param({"Shape": 0, "Size": 2}, (9, 41, 9, 41), id="fixed-size"),
		pytest.param({"Shape": 1}, (6, 44, 6, 44), id="isotropic"),
		pytest.param({"Shape": 2}, (3, 47, 3, 47), id="anisotropic")])
def test_update_data_box(manager: ROIManager, gaussian, expected):
	"""Vérifie les supports effectifs et la marge convertie en pixels source."""
	manager.set_size(100, 80)
	data = pd.DataFrame({"X": [20, 30], "Y": [20, 30], "Sigma X": [2, 2], "Sigma Y": [4, 4]})
	manager.update_data_box(data, gaussian)
	assert manager.data_box == expected
	assert manager.get_hr_limits() == expected
	assert manager.get_roi_limits() == (0, 100, 0, 80)


##################################################
@pytest.mark.parametrize("data", [
		pytest.param(None, id="disabled"),
		pytest.param(pd.DataFrame(), id="empty-data"),
		pytest.param(pd.DataFrame({"X": [np.nan], "Y": [2]}), id="nonfinite-data"),
		pytest.param(pd.DataFrame({"X": [2]}), id="missing-column")])
def test_update_data_box_reset(manager: ROIManager, data):
	"""Une entrée inexploitable efface le cadre de la génération précédente."""
	manager.set_size(100, 80)
	manager.data_box = (10, 20, 10, 20)
	manager.update_data_box(data)
	assert manager.data_box == (-1, -1, -1, -1)


##################################################
@pytest.mark.parametrize("sigmas, gaussian", [
		pytest.param({"Sigma Y": [1.0]}, {"Shape": 1}, id="missing-sigma-x"),
		pytest.param({"Sigma X": [1.0]}, {"Shape": 2}, id="missing-sigma-y"),
		pytest.param({"Sigma X": [np.nan], "Sigma Y": [1.0]}, {"Shape": 1}, id="nan-sigma"),
		pytest.param({"Sigma X": [1.0], "Sigma Y": [np.inf]}, {"Shape": 2}, id="infinite-sigma"),
		pytest.param({}, {"Shape": 0, "Size": np.nan}, id="nan-size"),
		pytest.param({}, {"Shape": 0, "Size": np.inf}, id="infinite-size"),
		pytest.param({}, {"Shape": 0, "Size": 0.0}, id="zero-size"),
		pytest.param({}, {"Shape": 0, "Size": -1.0}, id="negative-size"),
		pytest.param({"Sigma X": [0.0], "Sigma Y": [0.0]}, {"Shape": 1}, id="zero-mean-sigma"),
		pytest.param({"Sigma X": [-2.0], "Sigma Y": [-1.0]}, {"Shape": 2}, id="negative-max-sigma")])
def test_update_data_box_invalid_gaussian(manager: ROIManager, sigmas, gaussian):
	"""Des paramètres gaussiens invalides effacent le cadre précédent sans modifier la ROI utilisateur."""
	manager.set_size(100, 80)
	manager.set_xy_roi(10, 50, 10, 50)
	manager.roi_selection.active = True
	data = pd.DataFrame({"X": [20.0], "Y": [30.0], **sigmas})
	manager.update_data_box(data)
	assert manager.data_box != (-1, -1, -1, -1)

	manager.update_data_box(data, gaussian)
	assert manager.data_box == (-1, -1, -1, -1)
	assert manager.get_roi_limits() == (10, 50, 10, 50)
	assert manager.get_hr_limits() == (10, 50, 10, 50)


##################################################
@pytest.mark.parametrize("data_box, expected", [
		pytest.param((0, 25, 0, 20), (20, 25, 10, 20), id="image-edge"),
		pytest.param((60, 70, 60, 70), (20, 40, 10, 30), id="disjoint")])
def test_hr_data_intersection(manager: ROIManager, data_box, expected):
	"""Accepte les bords nuls et conserve un domaine valide si les cadres sont disjoints."""
	manager.set_size(100, 80)
	manager.set_xy_roi(20, 40, 10, 30)
	manager.roi_selection.active = True
	manager.data_box = data_box
	assert manager.get_hr_limits() == expected
	assert manager.hr_box == expected


##################################################
def test_data_box_intersection_and_reset(manager: ROIManager):
	"""Le cadrage HR ne filtre pas les données et disparaît au changement de pile."""
	manager.set_size(100, 80)
	manager.set_xy_roi(20, 40, 10, 30)
	manager.roi_selection.active = True
	manager.data_box = (25, 50, 0, 25)
	assert manager.get_hr_limits() == (25, 40, 10, 25)
	data = pd.DataFrame({"X": [21, 30], "Y": [20, 20]})
	assert len(manager.filtering_dataframe(data)) == 2
	manager.update_data_box(None)
	assert manager.hr_box == (25, 40, 10, 25)
	assert manager.get_hr_limits() == (20, 40, 10, 30)
	assert manager.hr_box == (20, 40, 10, 30)
	manager.data_box = (25, 50, 0, 25)
	manager.set_size(50, 40)
	assert manager.data_box == (-1, -1, -1, -1)


##################################################
def test_hr_box(manager: ROIManager):
	"""Vérifie le calcul de la boîte haute résolution."""
	manager.set_size(100, 80)
	manager.rois = [ROI("rectangle", np.array([[-5.2, -10.8], [-5.2, 120.4], [90.7, 120.4], [90.7, -10.8]]))]
	assert manager.hr_box == (0, 1, 0, 1)
	assert manager.get_hr_limits() == (0, 100, 0, 80)
	assert manager.hr_box == (0, 100, 0, 80)


##################################################
def test_filtering_dataframe(manager: ROIManager):
	"""Vérifie le filtrage spatial d'un DataFrame."""
	manager.set_size(10, 10)
	df = pd.DataFrame({"X": [1, 2, 3], "Y": [1, 2, 3]})
	res = manager.filtering_dataframe(df)  # ROI sélection non actif
	assert res is df
	manager.roi_selection.active = True
	res = manager.filtering_dataframe(df)  # ROI sélection actif, mais aucune ROI.
	assert res is df
	manager.set_xy_roi(10, 20, 30, 40, add=False)
	res = manager.filtering_dataframe(df)  # La ROI est trop restrictive.
	assert res.empty

	manager.set_xy_roi(0, 3, 0, 2, add=False)
	res = manager.filtering_dataframe(df)  # La limite le Y, mais pas le X.
	np.testing.assert_allclose(res.to_numpy(), [[1, 1], [2, 2]])

	manager.rois = [ROI("ellipse", np.array([[1, 1], [1, 3], [3, 3], [3, 1]], dtype=float))]
	res = manager.filtering_dataframe(df)  # Une ellipse est défini par sa bounding box, ici cercle de rayon 1 de centre 2 (donc ne récupère qu'un point).
	np.testing.assert_allclose(res.to_numpy(), [[2, 2]])

	manager.rois = [ROI("ellipse", np.array([[1, 1], [1, 1], [1, 1], [1, 1]], dtype=float))]
	res = manager.filtering_dataframe(df)  # Une ellipse de rayon 0
	assert res.empty

	manager.rois = [ROI("line", np.array([[1, 1], [1, 2], [2, 2], [2, 1]], dtype=float))]
	res = manager.filtering_dataframe(df)  # Type non conforme, mais il a fait la bounding box
	np.testing.assert_allclose(res.to_numpy(), [[1, 1], [2, 2]])


##################################################
def test_filtering_dataframe_concave_cross(manager: ROIManager):
	"""Vérifie le filtrage exact d'une ROI concave en forme de croix."""
	manager.set_size(10, 10)
	manager.roi_selection.active = True

	# Polygone concave en forme de croix. Les coordonnées Napari sont données dans l'ordre (Y, X).
	cross = np.array([[0, 4], [0, 6], [4, 6], [4, 10], [6, 10], [6, 6], [10, 6], [10, 4], [6, 4], [6, 0], [4, 0], [4, 4]], dtype=float)
	manager.rois = [ROI("polygon", cross)]
	dataframe = pd.DataFrame({"X": [5, 1, 5, 1, 9, 11], "Y": [5, 5, 1, 1, 9, 5]})

	res = manager.filtering_dataframe(dataframe, strict=False)
	np.testing.assert_allclose(res.to_numpy(), [[5, 5], [1, 5], [5, 1], [1, 1], [9, 9]])  # Uniquement le dernier qui est en dehors de la bounding box.
	res = manager.filtering_dataframe(dataframe, strict=True)
	np.testing.assert_allclose(res.to_numpy(), [[5, 5], [1, 5], [5, 1]])  # Enlève en plus les 2 points dans des coins.

# ==================================================
# endregion Divers
# ==================================================
