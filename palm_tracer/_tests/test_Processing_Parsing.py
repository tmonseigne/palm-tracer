"""Teste la conversion et la structuration des résultats des DLL PALM."""

import pytest

from palm_tracer.Processing.Parsing import *


# ==================================================
# region Manipulation de DataFrame
# ==================================================
##################################################
@pytest.mark.parametrize("keep_others, expected", [
		pytest.param(True, ["Y", "X", "Z"], id="other-columns-preserved"),
		pytest.param(False, ["Y"], id="selection-only")])
def test_rearrange_dataframe_columns(keep_others, expected):
	"""Vérifie la sélection, l'ordre des colonnes et l'idempotence du réarrangement."""
	df = pd.DataFrame({"X": [1, 2, 3], "Y": [4, 5, 6], "Z": [7, 8, 9]})
	res = rearrange_dataframe_columns(df, ["Y"], keep_others)
	assert res.columns.tolist() == expected
	assert rearrange_dataframe_columns(res, ["Y"], keep_others).columns.tolist() == expected


##################################################
def test_rearrange_dataframe_columns_missing():
	"""Vérifie le rejet d'une colonne sélectionnée absente."""
	df = pd.DataFrame({"X": [1], "Y": [2], "Z": [3]})
	with pytest.raises(ValueError): rearrange_dataframe_columns(df, ["Alpha"], True)


##################################################
def test_log10_dataframe():
	"""Vérifie log10_DataFrame."""
	data = pd.DataFrame([[0, 0], [1, 1]], columns=["A", "B"])
	res = log10_dataframe(data, ["B"])
	ref = [[0, np.nan], [1, 0]]
	assert np.allclose(res, ref, atol=0, rtol=0, equal_nan=True), f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"


# ==================================================
# endregion Manipulation de DataFrame
# ==================================================

# ==================================================
# region Gestion des angles
# ==================================================
##################################################
def test_degrees_to_radians():
	"""Vérifie degrees_to_radians."""

	data = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360]
	ref = [0, np.pi / 6, np.pi / 4, np.pi / 3, np.pi / 2, 2 * np.pi / 3, 3 * np.pi / 4, 5 * np.pi / 6, np.pi,
		   7 * np.pi / 6, 5 * np.pi / 4, 4 * np.pi / 3, 3 * np.pi / 2, 5 * np.pi / 3, 7 * np.pi / 4, 11 * np.pi / 6, 2 * np.pi]
	res = degrees_to_radians(data)
	assert np.allclose(res, ref, atol=1e-6, equal_nan=True), f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"

	data = [-90, -60, -45, -30, 0, 30, 45, 60, 90]
	ref = [-np.pi / 2, -np.pi / 3, - np.pi / 4, -np.pi / 6, 0, np.pi / 6, np.pi / 4, np.pi / 3, np.pi / 2]
	res = degrees_to_radians(data)
	assert np.allclose(res, ref, atol=1e-6, equal_nan=True), f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"


##################################################
def test_radians_to_degrees():
	"""Vérifie radians_to_degrees."""
	data = [0, np.pi / 6, np.pi / 4, np.pi / 3, np.pi / 2, 2 * np.pi / 3, 3 * np.pi / 4, 5 * np.pi / 6, np.pi,
			7 * np.pi / 6, 5 * np.pi / 4, 4 * np.pi / 3, 3 * np.pi / 2, 5 * np.pi / 3, 7 * np.pi / 4, 11 * np.pi / 6, 2 * np.pi]
	ref = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360]
	res = radians_to_degrees(data)
	assert np.allclose(res, ref, atol=1e-6, equal_nan=True), f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"

	data = [-np.pi / 2, -np.pi / 3, - np.pi / 4, -np.pi / 6, 0, np.pi / 6, np.pi / 4, np.pi / 3, np.pi / 2]
	ref = [-90, -60, -45, -30, 0, 30, 45, 60, 90]
	res = radians_to_degrees(data)
	assert np.allclose(res, ref, atol=1e-6, equal_nan=True), f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"


##################################################
def test_wrap_angle():
	"""Vérifie wrap_angle."""
	data = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360]
	res = wrap_angle(data, 180, False)
	ref = [0, 30, 45, 60, 90, 120, 135, 150, 0, 30, 45, 60, 90, 120, 135, 150, 0]
	assert np.allclose(res, ref, atol=1e-6, equal_nan=True), f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"

	res = wrap_angle(data, 180, True)
	ref = [0, 30, 45, 60, -90, -60, -45, -30, 0, 30, 45, 60, -90, -60, -45, -30, 0]
	assert np.allclose(res, ref, atol=1e-6, equal_nan=True), f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"


##################################################
def test_manage_theta():
	"""Vérifie manage_theta."""
	data = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi]
	ref = [0, 45, -90, -45, 0]
	res = manage_theta(data)
	assert np.allclose(res, ref, atol=1e-6, equal_nan=True), f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"


# ==================================================
# endregion Gestion des angles
# ==================================================

# ==================================================
# region Analyse
# ==================================================
##################################################
def test_get_meta():
	"""Vérifie la lecture de métadonnées de dimensions valides."""
	get_meta(np.zeros(shape=(1, N_COL_META)))


##################################################
def test_get_meta_invalid():
	"""Vérifie le rejet de métadonnées vides."""
	with pytest.raises(ValueError): get_meta([])


##################################################
def test_parse_irregular_array():
	"""Vérifie la reconstruction d'un tableau avec longueurs de lignes intégrées."""
	res = parse_irregular_array(np.array([2, 1, 2, 2, 3, 4]))
	np.testing.assert_array_equal(res, [[1, 2], [3, 4]])


##################################################
@pytest.mark.parametrize("data", [
		pytest.param(np.array([[2, 1, 2, 2, 3, 4]]), id="2d-array"),
		pytest.param(np.array(["hey", 1, 2, 2, 3, 4]), id="non-numeric-data"),
		pytest.param(np.array([2, 1, 2, 2, 3]), id="truncated-row")])
def test_parse_irregular_array_invalid(data):
	"""Vérifie chaque forme de tableau irrégulier invalide."""
	with pytest.raises(ValueError): parse_irregular_array(data)


##################################################
@pytest.mark.parametrize("data", [
		pytest.param(np.array([]), id="empty-array"), pytest.param(np.array([0]), id="empty-row")])
def test_parse_irregular_array_empty(data):
	"""Vérifie les entrées sans valeur à reconstruire."""
	assert parse_irregular_array(data).empty


##################################################
@pytest.mark.parametrize("data, result_type, fit_mode, expected", [
		pytest.param(np.arange(20), "Localization",  0, np.arange(18), id="localizations"),
		pytest.param(np.arange(20), "Tracking", 0, np.arange(16).reshape(2, 8), id="tracks"),
		pytest.param(np.arange(10).reshape(2, 5), "Astigmatism 3D Model", 0, np.arange(10).reshape(2, 5), id="astigmatism-model"),
		pytest.param(np.array([2, 1, 2, 2, 3, 4]), "MSD", 0, [[1, 2], [3, 4]], id="msd"),
		pytest.param(np.array([2, 1, 2, 2, 3, 4]), "Instant Diffusion", 0, [[1, 2], [3, 4]], id="instant-diffusion"),
		pytest.param(np.array([9] + [1] * 9), "Fit", 1, np.ones(9), id="linear-fit"),
		pytest.param(np.array([10] + [1] * 10), "Fit", 2, np.ones(10), id="power-fit"),
		pytest.param(np.array([11] + [1] * 11), "Fit", 3, np.ones(11), id="exponential-fit")])
def test_parse_result(data, result_type, fit_mode, expected):
	"""Vérifie la conversion de chaque format de résultat valide."""
	res = parse_result(data, result_type, fit_mode=fit_mode)
	assert np.allclose(res, expected, atol=0, rtol=0)


##################################################
@pytest.mark.parametrize("result_type", [
		pytest.param("Localization", id="localizations"), pytest.param("Tracking", id="tracks"), pytest.param("Fit", id="fit")])
def test_parse_result_empty(result_type):
	"""Vérifie la conversion des résultats vides."""
	assert parse_result(np.array([]), result_type).empty


##################################################
@pytest.mark.parametrize("data, result_type", [
		pytest.param(np.array([2, 1, 2, 2, 3, 4]), "Fit", id="invalid-fit"),
		pytest.param(np.array([11] + [1] * 11), "mon type", id="unknown-type")])
def test_parse_result_invalid(data, result_type):
	"""Vérifie les formats de résultats incompatibles ou inconnus."""
	with pytest.raises(ValueError): parse_result(data, result_type)

# ==================================================
# endregion Analyse
# ==================================================
