"""Teste les fonctions de calibration et d'estimation axiale par astigmatisme 3D."""

import pytest

from palm_tracer.Processing.Astigmatism3D import *

Z_MAX, N_POINTS, PIXEL_SIZE, SAMPLING = 500, 5000, 160, 1
REF_MODEL = np.array([[300, 450, -0.70, -0.30, 240], [-300, 600, 1.40, 0.04, 240]], dtype=float)
REF_MODEL2 = np.array([[-200, 100, 0, 0, 32], [200, 100, 0, 0, 32]], dtype=float)
LOC_COLS = ["Plane", "X", "Y", "Sigma X", "Sigma Y", "Z"]


# --------------------------------------------------
def get_dataset(model: np.ndarray = REF_MODEL, z_max: float = Z_MAX, n: int = N_POINTS,
				pixel_size: float = PIXEL_SIZE, sampling: float = SAMPLING) -> np.ndarray:
	"""
	Génère des observations synthétiques (SigmaX, SigmaY, Z) avec un bruit gaussien reproductible sur les sigmas.

	:param model: Modèle d'astigmatisme de forme (2, 5) : paramètres X puis Y, chaque ligne = [Z0, W, C3, C4, A].
	:param z_max: Valeur maximale de Z (le modèle est évalué sur [-z_max, +z_max]).
	:param n: Nombre de positions axiales régulièrement espacées.
	:param pixel_size: Taille du pixel dans les mêmes unités que Z (ex. nm).
	:param sampling: Facteur d'agrandissement appliqué aux sigmas du modèle.
	:return: Tableau (N, 3) des sigmas bruités en pixels et des positions axiales.
	"""
	rng = np.random.default_rng(42)

	# Z uniformément réparti entre [-z_max, +z_max].
	z = np.linspace(-z_max, z_max, n, dtype=float)

	# Sigma modèle
	sx = sigma_model(model[0], z, pixel_size, sampling)
	sy = sigma_model(model[1], z, pixel_size, sampling)

	# Bruit gaussien (en pixels)
	sx += rng.normal(0.0, 0.02, size=n)
	sy += rng.normal(0.0, 0.02, size=n)

	# Dataset final : (Sx, Sy, Z)
	data = np.column_stack((sx, sy, z))
	return data


DATASET = get_dataset()


# ==================================================
# region Préparation des données
# ==================================================
@pytest.mark.parametrize("planes, z_min, z_max, expected", [
		pytest.param(np.arange(5), -10, 10, [-10, -5, 0, 5, 10], id="symmetric-range"),
		pytest.param(np.arange(5), -10, 0, [-10, -7.5, -5, -2.5, 0], id="negative-range"),
		pytest.param(np.arange(5), 0, 10, [0, 2.5, 5, 7.5, 10], id="positive-range"),
		pytest.param(np.arange(5), 1, 1, np.ones(5), id="equal-bounds"),
		pytest.param(np.ones(5), -10, 10, np.zeros(5), id="identical-planes")])
def test_get_z_from_planes(planes, z_min, z_max, expected):
	"""Vérifie la conversion des numéros de plans selon la plage axiale."""
	np.testing.assert_array_equal(z_from_planes(planes, z_min, z_max), expected)


# --------------------------------------------------
@pytest.mark.parametrize("count, centered, expected", [
		pytest.param(5, True, [-2, -1, 0, 1, 2], id="centered-odd-count"),
		pytest.param(4, True, [-1.5, -0.5, 0.5, 1.5], id="centered-even-count"),
		pytest.param(5, False, [0, 1, 2, 3, 4], id="no-centering")])
def test_get_z_from_step(count, centered, expected):
	"""Vérifie les positions axiales pour un pas unitaire."""
	np.testing.assert_array_equal(z_from_step(count, 1, centered), expected)


# --------------------------------------------------
@pytest.mark.parametrize("data, expected", [
		pytest.param(pd.DataFrame([], columns=LOC_COLS), pd.DataFrame([], columns=LOC_COLS), id="empty"),
		pytest.param(pd.DataFrame([[0, 0, 0, 0, 0]], columns=LOC_COLS[1:]), pd.DataFrame([[0, 0, 0, 0, 0]], columns=LOC_COLS[1:]), id="missing-plane-column"),
		pytest.param(pd.DataFrame([[1, 5, 5, 1, 1, 0], [2, 5, 5, 1, 1, 0], [3, 5, 5, 1, 1, 0]], columns=LOC_COLS),
					 pd.DataFrame([[1, 5, 5, 1, 1, 0], [2, 5, 5, 1, 1, 0], [3, 5, 5, 1, 1, 0]], columns=LOC_COLS), id="single-point-per-plane"),
		pytest.param(pd.DataFrame([[1, 5, 5, 1, 1, 0], [1, 5, 5, 1, 1, 0], [1, 5, 5, 1, 1, 0]], columns=LOC_COLS),
					 pd.DataFrame([[1, 5, 5, 1, 1, 0], [1, 5, 5, 1, 1, 0], [1, 5, 5, 1, 1, 0]], columns=LOC_COLS), id="no-single-localization-plane"),
		pytest.param(pd.DataFrame([[1, 3, 3, 1, 1, 0], [1, 5, 5, 1, 1, 0], [2, 5, 5, 1, 1, 0]], columns=LOC_COLS),
					 pd.DataFrame([[1, 5, 5, 1, 1, 0], [2, 5, 5, 1, 1, 0]], columns=LOC_COLS), id="spatial-selection"),
		pytest.param(pd.DataFrame([[1, 1, 3, 3, 1, 1, 0], [2, 1, 5, 5, 1, 1, 0], [2, 2, 5, 5, 1, 1, 0]], columns=["Bead"] + LOC_COLS),
					 pd.DataFrame([[1, 1, 3, 3, 1, 1, 0]], columns=["Bead"] + LOC_COLS), id="bead-column")])
def test_remove_multi_loc(data, expected):
	"""Vérifie la sélection des billes dans chaque configuration de localisation."""
	res = remove_multi_beads(data.copy())
	pd.testing.assert_frame_equal(res, expected)


# ==================================================
# endregion Préparation des données
# ==================================================

# ==================================================
# region Modèle et validation
# ==================================================
def test_sigma_model():
	"""Vérifie le comportement de sigma_model."""
	model = np.array([200., 100., 0., 0., 32.], dtype=float)
	z = np.linspace(-200, 200, 11, dtype=float)
	res = sigma_model(model, z, 160, 1)
	ref = [0.82462113, 0.74726167, 0.67052218, 0.59464275, 0.52, 0.4472136, 0.37735925, 0.31240999, 0.25612497, 0.21540659, 0.2]
	assert np.allclose(res, ref), f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"


# --------------------------------------------------
@pytest.mark.parametrize("model, expected", [
		pytest.param(REF_MODEL, {'rmse_x': 0.02, 'rmse_y': 0.02, 'rmse_xy': 0.02, 'mae_x': 0.02, 'mae_y': 0.02, 'r2_x': 1, 'r2_y': 1}, id="correct-model"),
		pytest.param(REF_MODEL[::-1], {'rmse_x': 1.21, 'rmse_y': 1.21, 'rmse_xy': 1.21, 'mae_x': 1.06, 'mae_y': 1.06, 'r2_x': -2.87, 'r2_y': -2.21},
					 id="reversed-axes"),
		pytest.param(REF_MODEL2, {'rmse_x': 1.73, 'rmse_y': 1.73, 'rmse_xy': 1.73, 'mae_x': 1.48, 'mae_y': 1.47, 'r2_x': -6.92, 'r2_y': -5.62},
					 id="different-model")])
def test_model_validity(model, expected):
	"""Vérifie les métriques pour chaque modèle de calibration indépendamment."""
	res = model_validity(DATASET, model, PIXEL_SIZE, SAMPLING)
	for key, value in expected.items():
		assert np.isclose(res[key], value, atol=0.1), f"Métrique {key} : {res[key]} au lieu de {value}."


# --------------------------------------------------
@pytest.mark.parametrize("model, expected", [
		pytest.param(REF_MODEL, {'rmse_z':     5.78, 'mae_z': 4.58, 'p95_abs_z': 11.40, 'bias_z': 0.03, 'std_z': 5.78, 'mean_dist': 0.02, 'p95_dist': 0.04,
								 "slope_mean": 0.004}, id="correct-model"),
		pytest.param(REF_MODEL[::-1], {'rmse_z':   577.31, 'mae_z': 499.94, 'p95_abs_z': 950, 'bias_z': 7.4, 'std_z': 577.27, 'mean_dist': 0.03,
									   'p95_dist': 0.1, "slope_mean": 0.004}, id="reversed-axes"),
		pytest.param(REF_MODEL2, {'rmse_z':   763.52, 'mae_z': 749.6, 'p95_abs_z': 975.01, 'bias_z': 20.6, 'std_z': 763.24, 'mean_dist': 1.59,
								  'p95_dist': 2.27, "slope_mean": 0.0015}, id="different-model")])
def test_model_projection_validity(model, expected):
	"""Vérifie les métriques pour chaque modèle de calibration indépendamment."""
	res = model_projection_validity(DATASET, model, Z_MAX, PIXEL_SIZE, N_POINTS, SAMPLING)
	for key, value in expected.items():
		assert np.isclose(res[key], value, atol=0.1), f"Métrique {key} : {res[key]} au lieu de {value}."


# --------------------------------------------------
@pytest.mark.parametrize("model, expected_distance", [
		pytest.param(np.array([[-50, 100, 0, 0, 30], [50, 100, 0, 0, 30]], dtype=float), 100, id="separated-minima"),
		pytest.param(np.array([[50, 100, 0, 0, 30], [-50, 100, 0, 0, 30]], dtype=float), 100, id="reversed-axes"),
		pytest.param(np.array([[0, 100, 0, 0, 30], [0, 150, 0, 0, 40]], dtype=float), 0, id="coincident-minima"),
		pytest.param(np.array([[-300, 100, 0, 0, 30], [300, 100, 0, 0, 30]], dtype=float), 400, id="minima-at-domain-edges"),
		pytest.param(np.array([[0, 100, 3, 2, 30], [0, 100, 0, 0, 30]], dtype=float),
					 100 * (9 + np.sqrt(17)) / 16, id="asymmetric-model")])
@pytest.mark.parametrize("pixel_size", [80, 160], ids=["small-pixels", "large-pixels"])
def test_model_projection_astigmatism(model, expected_distance, pixel_size):
	"""Vérifie la distance axiale entre les minima, y compris lorsqu'ils diffèrent des paramètres Z0."""
	z_max, n_curve = 200, 401
	z = np.array([-100, 0, 100], dtype=float)
	points = np.column_stack((sigma_model(model[0], z, pixel_size), sigma_model(model[1], z, pixel_size), z))

	metrics = model_projection_validity(points, model, z_max, pixel_size, n_curve)

	# Chaque minimum est localisé à un demi-pas près : l'erreur sur leur distance peut atteindre un pas.
	z_step = 2 * z_max / (n_curve - 1)
	assert np.isclose(metrics["astigmatism"], expected_distance, atol=z_step, rtol=0)
	assert metrics["astigmatism"] >= 0


# ==================================================
# endregion Modèle et validation
# ==================================================

# ==================================================
# region Recherche du centre
# ==================================================
def test_find_model_center():
	"""Vérifie le comportement de find_model_center."""
	res = find_model_center(REF_MODEL, Z_MAX, PIXEL_SIZE)
	ref = 21.3895675
	assert np.isclose(res, ref, 1e-6)
	model = REF_MODEL.copy()
	model[0, 0] -= res
	model[1, 0] -= res
	res = find_model_center(model, Z_MAX, PIXEL_SIZE)
	assert np.isclose(res, 0, 1e-6)

	model_no_sign_change = np.array([[0.0, 300.0, 0.0, 0.0, 200.0], [0.0, 300.0, 0.0, 0.0, 250.0]], dtype=float)
	res = find_model_center(model_no_sign_change, Z_MAX, PIXEL_SIZE)
	ref = -0.2442599
	assert np.isclose(res, ref, 1e-6)

	model_easy_0 = np.array([[0.0, 300.0, 0.0, 0.0, 240.0], [0.0, 300.0, 0.0, 0.0, 240.0]], dtype=float)
	res = find_model_center(model_easy_0, 1024, 1)
	ref = -1024
	assert np.isclose(res, ref, 1e-6)

	model_bisection_no_exact_zero = np.array([[-123.41678443, 350.5466747, 0.687, 0.439, 240.456], [210, 350, 0, 0, 240], ], dtype=float)
	res = find_model_center(model_bisection_no_exact_zero, 100, 1)
	ref = 29.2051458
	assert np.isclose(res, ref, 1e-6)

# ==================================================
# endregion Recherche du centre
# ==================================================
