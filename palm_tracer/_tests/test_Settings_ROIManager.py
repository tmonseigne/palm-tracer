"""Tests unitaires de :class:`ROIManager`."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from napari.layers import Shapes

from palm_tracer.Settings import ROI, ROIManager
from palm_tracer.Settings.Types import CheckInt, SpinInt


@pytest.fixture
def manager() -> ROIManager:
	"""Construit un gestionnaire avec une sélection active et un ratio HR de 4."""
	return ROIManager(CheckInt("ROI", "", 1, [1, 1]), SpinInt("Up scaling ratio", "", 4, [1, 256], 2))


# ==================================================
# region Getter/Setter
# ==================================================
##################################################
def test_rois(manager: ROIManager):
	manager.rois = [ROI("rectangle", np.zeros((4, 2)))]
	assert manager.roi_selection.limits == [1, 1]
	manager.rois = [ROI("rectangle", np.zeros((4, 2))), ROI("ellipse", np.ones((4, 2)))]
	assert manager.roi_selection.limits == [1, 2]
	np.testing.assert_allclose(manager.rois[0].data, [[0, 0], [0, 0], [0, 0], [0, 0]])
	np.testing.assert_allclose(manager.rois[1].data, [[1, 1], [1, 1], [1, 1], [1, 1]])


##################################################
def test_set_xy_roi(manager: ROIManager):
	manager.rois = [ROI("ellipse", np.ones((4, 2)))]
	manager.set_xy_roi(10, 20, 30, 40, add=False)

	assert len(manager.rois) == 1
	assert manager.rois[0].type == "rectangle"
	np.testing.assert_allclose(manager.rois[0].data, [[30, 10], [30, 20], [40, 20], [40, 10]])

	manager.set_xy_roi(4.0, 5.0, 6.0, 7.0, add=True)
	assert len(manager.rois) == 2


##################################################
def test_layer(manager: ROIManager):
	assert manager.layer_main is None and manager.layer_hr is None
	manager.layer_main = Shapes()
	manager.layer_hr = Shapes()
	assert isinstance(manager.layer_main, Shapes) and isinstance(manager.layer_hr, Shapes)


# ==================================================
# endregion Getter/Setter
# ==================================================

# ==================================================
# region Synchronization
# ==================================================
##################################################
def test_update_main(manager: ROIManager):
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
	manager.roi_selection.value = 0  # Aucune ROI donc rejet, car hors limite.
	manager.rois = [ROI("rectangle", np.zeros((4, 2)))]  # Ajout d'une forme
	manager.roi_selection.value = 1  # Bonne selection, mais aucun layer.
	manager.layer_main = Shapes()
	manager.roi_selection.value = 1  # Bonne selection, mais aucun layer.
	manager.layer_hr = Shapes()
	manager.roi_selection.value = 1  # Bonne selection, mais aucun layer.


# ==================================================
# endregion Synchronization
# ==================================================

# ==================================================
# region IO
# ==================================================
##################################################
def test_dict(manager: ROIManager):
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
# endregion IO
# ==================================================

# ==================================================
# region Misc
# ==================================================
##################################################
def test_roi_limits(manager: ROIManager):
	manager.set_size(100, 80)
	manager.rois = [ROI("rectangle", np.array([[-5.2, -10.8], [-5.2, 120.4], [90.7, 120.4], [90.7, -10.8]]))]
	manager.roi_selection.value = 0
	assert manager.get_roi_limits() == (0, 100, 0, 80)
	manager.roi_selection.value = 1
	assert manager.get_roi_limits() == (0, 100, 0, 80)


##################################################
def test_hr_box(manager: ROIManager):
	manager.set_size(100, 80)
	manager.rois = [ROI("rectangle", np.array([[-5.2, -10.8], [-5.2, 120.4], [90.7, 120.4], [90.7, -10.8]]))]
	assert manager.hr_box == (0, 1, 0, 1)
	manager.update_hr_box()
	assert manager.hr_box == (0, 100, 0, 80)


##################################################
def test_filtering_dataframe(manager: ROIManager):
	manager.set_size(10, 10)
	df = pd.DataFrame({"X": [1, 2, 3], "Y": [1, 2, 3]})
	res = manager.filtering_dataframe(df)  # ROI sélection non actif
	assert res is df
	manager.roi_selection.active = True
	res = manager.filtering_dataframe(df)  # ROI sélection actif, mais aucune ROI.
	assert res is df
	manager.set_xy_roi(10, 20, 30, 40, add=False)
	res = manager.filtering_dataframe(df)  # La ROI est trop restritive.
	assert res.empty

	manager.set_xy_roi(0, 3, 0, 2, add=False)
	res = manager.filtering_dataframe(df)  # La limite le Y, mais pas le X.
	np.testing.assert_allclose(res.to_numpy(), [[1, 1], [2, 2]])

	manager.rois = [ROI("ellipse", np.array([[1, 1], [1, 3], [3, 3], [3, 1]], dtype=float))]
	res = manager.filtering_dataframe(df)  # Une ellipse est défini par sa bounding box, ici cercle de rayon 1 de centre 2 (donc ne récupère qu'un point)
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
	np.testing.assert_allclose(res.to_numpy(), [[5, 5], [1, 5], [5, 1]])  # enlève en plus les 2 points dans des coins.

# ==================================================
# endregion Misc
# ==================================================
