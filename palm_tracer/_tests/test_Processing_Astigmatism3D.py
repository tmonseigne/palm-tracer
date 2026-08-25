"""Teste les fonctions de calibration et d'estimation axiale par astigmatisme 3D."""

from palm_tracer.Processing.Astigmatism3D import *

Z_MAX, N_POINTS, PIXEL_SIZE, SAMPLING = 500, 5000, 160, 1
REF_MODEL = np.array([[300, 450, -0.70, -0.30, 240], [-300, 600, 1.40, 0.04, 240]], dtype=np.float64)
REF_MODEL2 = np.array([[-200, 100, 0, 0, 32], [200, 100, 0, 0, 32]], dtype=np.float64)


##################################################
def get_dataset(model: np.ndarray = REF_MODEL, z_max: float = Z_MAX, n: int = N_POINTS,
				pixel_size: float = PIXEL_SIZE, sampling: float = SAMPLING) -> np.ndarray:
	"""Génère un dataset synthétique (Sx, Sy, Z)."""
	rng = np.random.default_rng(42)

	# Z uniformément réparti entre [-z_max, +z_max]
	z = np.linspace(-z_max, z_max, n, dtype=np.float64)

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


##################################################
def test_get_z_from_planes():
	"""Vérifie le comportement de get_z_from_planes."""
	planes = np.array([0, 1, 2, 3, 4])

	res = z_from_planes(planes, z_min=-10, z_max=10)
	ref = [-10, -5, 0, 5, 10]
	assert np.allclose(res, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	res = z_from_planes(planes, z_min=-10, z_max=0)
	ref = [-10, -7.5, -5, -2.5, 0]
	assert np.allclose(res, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	res = z_from_planes(planes, z_min=0, z_max=10)
	ref = [0, 2.5, 5, 7.5, 10]
	assert np.allclose(res, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	res = z_from_planes(planes, z_min=1, z_max=1)
	ref = np.ones(5)
	assert np.allclose(res, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	res = z_from_planes(np.ones(5), z_min=-10, z_max=10)
	ref = np.zeros(5)
	assert np.allclose(res, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"


##################################################
def test_get_z_from_step():
	"""Vérifie le comportement de get_z_from_step."""
	res = z_from_step(5, 1)
	ref = [-2, -1, 0, 1, 2.]
	assert np.allclose(res, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	res = z_from_step(4, 1)
	ref = [-1.5, -0.5, 0.5, 1.5]
	assert np.allclose(res, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	res = z_from_step(5, 1, False)
	ref = [0, 1, 2, 3, 4.]
	assert np.allclose(res, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"


##################################################
def test_remove_multi_loc():
	"""Vérifie le comportement de remove_multi_loc."""
	columns = ["Plane", "X", "Y", "Sigma X", "Sigma Y", "Z"]
	# DataFrame vide
	data = pd.DataFrame([], columns=columns)
	res = remove_multi_beads(data)
	assert res.empty

	# DataFrame sans la colonne "Plane".
	data = pd.DataFrame([[0, 0, 0, 0, 0]], columns=columns[1:])
	res = remove_multi_beads(data)
	assert np.allclose(res, data, atol=0, rtol=0), f"Résultat incorrect.\nAttendu : {data}\nObtenu : {res}"

	# DataFrame avec déjà un seul point par plan.
	data = pd.DataFrame([[1, 5, 5, 1, 1, 0], [2, 5, 5, 1, 1, 0], [3, 5, 5, 1, 1, 0]], columns=columns)
	res = remove_multi_beads(data)
	assert np.allclose(res, data, atol=0, rtol=0), f"Résultat incorrect.\nAttendu : {data}\nObtenu : {res}"

	# DataFrame dont aucun plan ne contient une seule localisation.
	data = pd.DataFrame([[1, 5, 5, 1, 1, 0], [1, 5, 5, 1, 1, 0], [1, 5, 5, 1, 1, 0]], columns=columns)
	res = remove_multi_beads(data)
	assert np.allclose(res, data, atol=0, rtol=0), f"Résultat incorrect.\nAttendu : {data}\nObtenu : {res}"

	# DataFrame cohérent.
	data = pd.DataFrame([[1, 3, 3, 1, 1, 0], [1, 5, 5, 1, 1, 0], [2, 5, 5, 1, 1, 0]], columns=columns)
	res = remove_multi_beads(data)
	ref = pd.DataFrame([[1, 5, 5, 1, 1, 0], [2, 5, 5, 1, 1, 0]], columns=columns)
	assert np.allclose(res, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	# DataFrame avec une colonne Bead.
	data = pd.DataFrame([[1, 1, 3, 3, 1, 1, 0], [2, 1, 5, 5, 1, 1, 0], [2, 2, 5, 5, 1, 1, 0]], columns=["Bead"] + columns)
	res = remove_multi_beads(data)
	ref = pd.DataFrame([[1, 1, 3, 3, 1, 1, 0]], columns=["Bead"] + columns)
	assert np.allclose(res, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"


##################################################
def test_sigma_model():
	"""Vérifie le comportement de sigma_model."""
	model = np.array([200., 100., 0., 0., 32.], dtype=np.float64)
	z = np.linspace(-200, 200, 11, dtype=np.float64)
	res = sigma_model(model, z, 160, 1)
	ref = [0.82462113, 0.74726167, 0.67052218, 0.59464275, 0.52, 0.4472136, 0.37735925, 0.31240999, 0.25612497, 0.21540659, 0.2]
	assert np.allclose(res, ref), f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"


##################################################
def test_model_validity():
	"""Vérifie le comportement de model_validity."""
	# Vérification des métriques pour le bon modèle.
	# J'ai un bruit de 0.02 donc rmse environ 0.02 et mae légèrement inférieur, R² très proche de 1 (supérieur à 99% de variance expliquée).
	res = model_validity(DATASET, REF_MODEL, PIXEL_SIZE, SAMPLING)
	ref = {'rmse_x': 0.02, 'rmse_y': 0.02, 'rmse_xy': 0.02, 'mae_x': 0.02, 'mae_y': 0.02, 'r2_x': 1, 'r2_y': 1}
	for key in ref: assert np.isclose(res[key], ref[key], atol=0.1), f"Résultat incorrect pour la clé {key}.\nAttendu : {ref}\nObtenu : {res}"

	# Vérification des métriques pour un modèle avec axe inversé, attendu rmse et mae élevé (supérieur à 1) et R2 négatif.
	res = model_validity(DATASET, REF_MODEL[::-1], PIXEL_SIZE, SAMPLING)
	ref = {'rmse_x': 1.21, 'rmse_y': 1.21, 'rmse_xy': 1.21, 'mae_x': 1.06, 'mae_y': 1.06, 'r2_x': -2.87, 'r2_y': -2.21}
	for key in ref: assert np.isclose(res[key], ref[key], atol=0.1), f"Résultat incorrect pour la clé {key}.\nAttendu : {ref}\nObtenu : {res}"

	# Vérification des métriques pour un modèle différent (mais un minimum cohérent avec l'astigmatisme). Attendu : Erreurs encore plus importantes.
	res = model_validity(DATASET, REF_MODEL2, PIXEL_SIZE, SAMPLING)
	ref = {'rmse_x': 1.73, 'rmse_y': 1.73, 'rmse_xy': 1.73, 'mae_x': 1.48, 'mae_y': 1.47, 'r2_x': -6.92, 'r2_y': -5.62}
	for key in ref: assert np.isclose(res[key], ref[key], atol=0.1), f"Résultat incorrect pour la clé {key}.\nAttendu : {ref}\nObtenu : {res}"


##################################################
def test_model_projection_validity():
	"""Vérifie le comportement de model_projection_validity."""
	# Vérification des métriques pour le bon modèle. Le bruit de 0.02 (et son carré) est retrouvé dans les deux derniers éléments du dictionnaire
	res = model_projection_validity(DATASET, REF_MODEL, Z_MAX, PIXEL_SIZE, N_POINTS, SAMPLING)
	print(res)
	ref = {'rmse_z': 5.78, 'mae_z': 4.58, 'p95_abs_z': 11.40, 'bias_z': 0.03, 'std_z': 5.78, 'mean_dist': 0.02, 'p95_dist': 0.04, "slope_mean": 0.004}
	for key in ref: assert np.isclose(res[key], ref[key], atol=0.1), f"Résultat incorrect pour la clé {key}.\nAttendu : {ref}\nObtenu : {res}"

	# Vérification des métriques pour un modèle avec axe inversé,
	# RMSE et MAE attendues élevées (du même ordre de grandeur que Z_MAX), mais distances en pixels faibles : signature d'une inversion du Z.
	# Le biais faible en est une conséquence (les erreurs s'annulent presque du fait que la courbe est PRESQUE symétrique).
	res = model_projection_validity(DATASET, REF_MODEL[::-1], Z_MAX, PIXEL_SIZE, N_POINTS, SAMPLING)
	ref = {'rmse_z': 577.31, 'mae_z': 499.94, 'p95_abs_z': 950, 'bias_z': 7.4, 'std_z': 577.27, 'mean_dist': 0.03, 'p95_dist': 0.1, "slope_mean": 0.004}
	print(res)
	for key in ref: assert np.isclose(res[key], ref[key], atol=0.1), f"Résultat incorrect pour la clé {key}.\nAttendu : {ref}\nObtenu : {res}"

	# Vérification des métriques pour un modèle différent (mais un minimum cohérent avec l'astigmatisme), attendu erreurs importantes partout.
	res = model_projection_validity(DATASET, REF_MODEL2, Z_MAX, PIXEL_SIZE, N_POINTS, SAMPLING)
	ref = {'rmse_z': 763.52, 'mae_z': 749.6, 'p95_abs_z': 975.01, 'bias_z': 20.6, 'std_z': 763.24, 'mean_dist': 1.59, 'p95_dist': 2.27, "slope_mean": 0.0015}
	print(res)
	for key in ref: assert np.isclose(res[key], ref[key], atol=0.1), f"Résultat incorrect pour la clé {key}.\nAttendu : {ref}\nObtenu : {res}"


##################################################
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

	model_no_sign_change = np.array([[0.0, 300.0, 0.0, 0.0, 200.0], [0.0, 300.0, 0.0, 0.0, 250.0]], dtype=np.float64)
	res = find_model_center(model_no_sign_change, Z_MAX, PIXEL_SIZE)
	ref = -0.2442599
	assert np.isclose(res, ref, 1e-6)

	model_easy_0 = np.array([[0.0, 300.0, 0.0, 0.0, 240.0], [0.0, 300.0, 0.0, 0.0, 240.0]], dtype=np.float64)
	res = find_model_center(model_easy_0, 1024, 1)
	ref = -1024
	assert np.isclose(res, ref, 1e-6)

	model_bisection_no_exact_zero = np.array([[-123.41678443, 350.5466747, 0.687, 0.439, 240.456], [210, 350, 0, 0, 240], ], dtype=np.float64)
	res = find_model_center(model_bisection_no_exact_zero, 100, 1)
	ref = 29.2051458
	assert np.isclose(res, ref, 1e-6)
