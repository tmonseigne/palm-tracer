"""Fichier des tests pour l'utilisation des DLL."""
import pytest

from palm_tracer.Processing.Parsing import *


##################################################
def test_get_meta():
	"""Test basique de get_meta."""

	with pytest.raises(ValueError) as exception_info: get_meta([])
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."
	get_meta(np.zeros(shape=(1, N_COL_META)))


##################################################
def test_rearrange_dataframe_columns():
	"""test de la fonction rearrange_dataframe_columns."""
	df = pd.DataFrame({"X": [1, 2, 3], "Y": [4, 5, 6], "Z": [7, 8, 9]})
	res = rearrange_dataframe_columns(df, ["Y"], True)
	assert res.columns.tolist() == ["Y", "X", "Z"], "Erreur dans la fonction rearrange_dataframe_columns."
	res = rearrange_dataframe_columns(res, ["Y"], True)
	assert res.columns.tolist() == ["Y", "X", "Z"], "Erreur dans la fonction rearrange_dataframe_columns."
	res = rearrange_dataframe_columns(df, ["Y"], False)
	assert res.columns.tolist() == ["Y"], "Erreur dans la fonction rearrange_dataframe_columns."
	assert pytest.raises(ValueError, rearrange_dataframe_columns, df, ["Alpha"], True)


##################################################
def test_log10_dataframe():
	"""Test basique de log10_dataframe."""
	data = pd.DataFrame([[0, 0], [1, 1]], columns=["A", "B"])
	res = log10_dataframe(data, ["B"])
	ref = [[0, np.nan], [1, 0]]
	assert np.allclose(res, ref, atol=0, rtol=0, equal_nan=True), f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"


##################################################
def test_degrees_to_radians():
	"""Test basique de degrees_to_radians."""

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
	"""Test basique de radians_to_degrees."""
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
	"""Test basique de wrap_angle."""
	data = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360]
	res = wrap_angle(data, 180, False)
	ref = [0, 30, 45, 60, 90, 120, 135, 150, 0, 30, 45, 60, 90, 120, 135, 150, 0]
	assert np.allclose(res, ref, atol=1e-6, equal_nan=True), f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"

	res = wrap_angle(data, 180, True)
	ref = [0, 30, 45, 60, -90, -60, -45, -30, 0, 30, 45, 60, -90, -60, -45, -30, 0]
	assert np.allclose(res, ref, atol=1e-6, equal_nan=True), f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"


##################################################
def test_manage_theta():
	"""Test basique de manage_theta."""
	data = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi]
	ref = [0, 45, -90, -45, 0]
	res = manage_theta(data)
	assert np.allclose(res, ref, atol=1e-6, equal_nan=True), f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"


##################################################
def test_parse_irregular_array():
	"""Test de la fonction parse_irregular_array."""
	data = np.array([2, 1, 2, 2, 3, 4])
	res = parse_irregular_array(data)
	ref = np.array([[1, 2], [3, 4]])
	assert np.allclose(res, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	data = np.array([[2, 1, 2, 2, 3, 4]])
	assert pytest.raises(ValueError, parse_irregular_array, data)
	data = np.array(["hey", 1, 2, 2, 3, 4])
	assert pytest.raises(ValueError, parse_irregular_array, data)
	data = np.array([2, 1, 2, 2, 3])
	assert pytest.raises(ValueError, parse_irregular_array, data)
	data = np.array([])
	res = parse_irregular_array(data)
	assert res.empty
	data = np.array([0])
	res = parse_irregular_array(data)
	assert res.empty


##################################################
def test_parse_result():
	"""Test basique de parse_result."""
	data = np.arange(20)
	res = parse_result(data, "Localization")
	ref = np.arange(18)
	assert np.allclose(res, ref, atol=0, rtol=0), f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"

	res = parse_result(np.array([]), "Localization")
	assert res.empty, "Le dataframe devrait être vide."

	res = parse_result(data, "Tracking")
	ref = np.arange(16).reshape(2, 8)
	assert np.allclose(res, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	res = parse_result(np.array([]), "Tracking")
	assert res.empty, "Le dataframe devrait être vide."

	data = np.arange(10).reshape((2, 5))
	res = parse_result(data, "Astigmatism 3D Model")
	assert np.allclose(res, data, atol=0, rtol=0), f"Résultat incorrect.\nAttendu : {data}\nObtenu : {res}"

	data = np.array([2, 1, 2, 2, 3, 4])
	res = parse_result(data, "MSD")
	ref = [[1, 2], [3, 4]]
	assert np.allclose(res, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	res = parse_result(data, "Instant Diffusion")
	assert np.allclose(res, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	with pytest.raises(ValueError) as exception_info: parse_result(data, "Fit")
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."

	data = np.array([9, 1, 1, 1, 1, 1, 1, 1, 1, 1])
	res = parse_result(data, "Fit", is_log=True, fit_mode=1)
	ref = [[1, 1, 0, 0, 0, 0, 0, 0, 0]]
	assert np.allclose(res, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	data = np.array([10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
	res = parse_result(data, "Fit", fit_mode=2)
	ref = np.ones(10)
	assert np.allclose(res, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	data = np.array([11, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
	res = parse_result(data, "Fit", fit_mode=3)
	ref = np.ones(11)
	assert np.allclose(res, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	res = parse_result(np.array([]), "Fit")
	assert res.empty, "Le dataframe devrait être vide."

	with pytest.raises(ValueError) as exception_info: parse_result(data, "mon type")
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."


##################################################
def test_parse_localization_for_tracking():
	"""Test de la fonction parse_localization_for_tracking."""
	data = parse_result(np.arange(36), "Localization")
	res = parse_localization_for_tracking(data)
	ref = [0, 4, 5, 6, 15, 16, -1, -1, -1, -1, -1, -1, 18, 22, 23, 24, 33, 34, -1, -1, -1, -1, -1, -1]
	assert np.allclose(res, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"
