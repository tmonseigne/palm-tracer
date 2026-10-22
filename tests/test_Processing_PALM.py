"""Teste l'encapsulation et l'utilisation de la DLL PALM."""

from unittest.mock import Mock

import pytest
from scipy.optimize import least_squares

from palm_tracer.Processing import Palm, Parsing
from palm_tracer.Processing.Astigmatism3D import sigma_model
from palm_tracer.Processing.Parsing import MODEL_ROWS
from palm_tracer.Tools import FileIO
from tests.Utils import *


# ==================================================
# region Initialisation
# ==================================================
def test_palm_dll_valid():
	"""Vérifie sur la présence d ela DLL PALM."""
	palm = Palm()
	assert palm.is_valid(), "Erreur lors du chargement de la DLL"


# ==================================================
# endregion Initialisation
# ==================================================

# ==================================================
# region Localisation
# ==================================================
@pytest.mark.parametrize("watershed", [True, False], ids=['with-watershed', 'no-watershed'])
@pytest.mark.parametrize("fit", range(6), ids=['no-fit', 'gaussian-xy', 'gaussian-sigma', 'gaussian-sigma-xy', 'gaussian-theta', 'spline'])
def test_localization(watershed: bool, fit: int):
	"""Vérifie sur le lancement de PALM sur une pile."""
	palm = Palm()
	file = "stack"
	stack = FileIO.open_tif(f"{INPUT_DIR}/{file}.tif")
	suffix = get_loc_suffix(fit, watershed)

	localizations = palm.localization(stack, default_threshold, watershed, fit, get_fit_params(fit))
	if save_output: localizations.round(6).to_csv(f"{OUTPUT_DIR}/{file}-localizations-{suffix}.csv", index=False)

	assert len(localizations) > 0, "Aucune localisation trouvé"

	path = REF_DIR / f"{file}-localizations-{suffix}.csv"
	if path.exists() and path.is_file():
		print(f"Comparaison avec : '{path}'")
		ref = pd.read_csv(path)
		assert compare_points(localizations, ref, 0.001), f"Test invalide pour les paramètres {suffix}"


# --------------------------------------------------
def test_localization_stack_quadrant():
	"""Vérifie sur le lancement de PALM sur une pile."""
	palm = Palm()
	suffix = get_loc_suffix()
	file = "stack_quadrant"
	stack = FileIO.open_tif(f"{INPUT_DIR}/{file}.tif")

	localizations = palm.localization(stack, default_threshold, default_watershed, default_fit, get_fit_params(default_fit))
	if save_output: localizations.round(6).to_csv(f"{OUTPUT_DIR}/{file}-localizations-{suffix}.csv", index=False)

	quadrant = {"Top":    localizations['Plane'].isin([3, 4, 7, 8]),
				"Bottom": localizations['Plane'].isin([1, 2, 5, 6, 9, 10]),
				"Left":   localizations['Plane'].isin([1, 4, 5, 8, 9]),
				"Right":  localizations['Plane'].isin([2, 3, 6, 7, 10])}
	assert (localizations.loc[quadrant["Top"], 'Y'] <= 128).all(), "Des éléments ont été trouvé dans la zone noire en haut de l'image."
	assert (localizations.loc[quadrant["Bottom"], 'Y'] >= 128).all(), "Des éléments ont été trouvé dans la zone noire en bas de l'image."
	assert (localizations.loc[quadrant["Left"], 'X'] <= 128).all(), "Des éléments ont été trouvé dans la zone noire à gauche de l'image."
	assert (localizations.loc[quadrant["Right"], 'X'] >= 128).all(), "Des éléments ont été trouvé dans la zone noire à droite de l'image."

	path = REF_DIR / f"{file}-localizations-{suffix}.csv"
	if path.exists() and path.is_file():
		ref = pd.read_csv(path)
		assert compare_points(localizations, ref), "Test invalide pour la vérification des quadrants."


# --------------------------------------------------
def test_localization_image():
	"""Vérifie la localisation d'une image 2D extraite de la pile."""
	palm = Palm()
	file = "stack"
	stack = FileIO.open_tif(f"{INPUT_DIR}/{file}.tif")
	p = 0
	suffix = get_loc_suffix()

	localizations = palm.localization(stack[p], default_threshold, default_watershed, default_fit, get_fit_params(default_fit))
	if save_output: localizations.round(6).to_csv(f"{OUTPUT_DIR}/{file}-localizations-{p}_{suffix}.csv", index=False)

	assert len(localizations) > 0, "Aucune localisation trouvé"

	path = REF_DIR / f"{file}-localizations-{p}_{suffix}.csv"
	if path.exists() and path.is_file():
		print(f"Comparaison avec : '{path}'")
		ref = pd.read_csv(path)
		assert compare_points(localizations, ref), f"Test invalide pour les paramètres {p}_{suffix}"


# --------------------------------------------------
def test_localization_plane_selection():
	"""Vérifie sur le lancement de PALM sur une pile."""
	palm = Palm()
	file = "stack"
	stack = FileIO.open_tif(f"{INPUT_DIR}/{file}.tif")
	suffix = get_loc_suffix()

	localizations = palm.localization(stack, default_threshold, default_watershed, default_fit, get_fit_params(default_fit), [2, 3, 4, 5, 6])
	if save_output: localizations.round(6).to_csv(f"{OUTPUT_DIR}/{file}-localizations-plane_select-{suffix}.csv", index=False)
	assert len(localizations) > 0, "Aucune localisation trouvé"
	path = REF_DIR / f"{file}-localizations-plane_select-{suffix}.csv"
	if path.exists() and path.is_file():
		print(f"Comparaison avec : '{path}'")
		ref = pd.read_csv(path)
		assert compare_points(localizations, ref, 0.001), f"Test invalide pour les paramètres {suffix}"


# --------------------------------------------------
def test_localization_empty_result():
	"""Vérifie sur le lancement de PALM sur une noire."""
	palm = Palm()
	stack: np.ndarray = np.zeros((10, 10, 10), dtype=np.uint16)
	res = palm.localization(stack, default_threshold, default_watershed, default_fit, get_fit_params(default_fit))
	assert res.empty


# ==================================================
# endregion Localisation
# ==================================================

# ==================================================
# region Ajustement de positions
# ==================================================
@pytest.mark.parametrize("fit", [2, 4], ids=['gaussian-sigma', 'gaussian-theta'])
def test_fitting_matches_localization(fit: int):
	"""Compare la détection suivie d'un fit séparé à la localisation avec fit sur la pile complète."""
	palm = Palm()
	stack = FileIO.open_tif(INPUT_DIR / "stack.tif")
	params = get_fit_params(fit)
	localizations = palm.localization(stack, default_threshold, default_watershed, 0, get_fit_params(0))
	expected = palm.localization(stack, default_threshold, default_watershed, fit, params)
	points = localizations[Parsing.COLS_FOR_FITTING].copy()
	points["Id"] *= 2  # Identifiants non consécutifs pour vérifier leur conservation.
	actual = palm.fitting(stack, points, fit, params)
	np.testing.assert_array_equal(actual["Id"], points["Id"])

	# L'appariement à la localisation avec fit tient compte du tri des positions après ajustement.
	columns = [column for column in expected.columns if column not in ("Id", "Index")]
	assert compare_points(actual, expected, tol=1e-8, compare_cols=columns)


# ==================================================
# endregion Ajustement de positions
# ==================================================

# ==================================================
# region Seuil automatique
# ==================================================
@pytest.mark.parametrize("p", range(10), ids=['plane-1', 'plane-2', 'plane-3', 'plane-4', 'plane-5', 'plane-6', 'plane-7', 'plane-8', 'plane-9', 'plane-10'])
def test_auto_threshold(p: int):
	"""Vérifie l'auto-seuillage avec la DLL CPU."""
	palm = Palm()
	image = FileIO.open_tif(f"{INPUT_DIR}/stack.tif")
	ref = [63.651749, 66.142910, 63.192296, 64.368855, 63.954150,
		   63.400043, 66.521994, 63.373237, 62.613244, 63.866017]
	res = palm.auto_threshold(image[p], get_fit_params(0))
	# print(f"Image {i} : {res:.6f} VS {ref[i]:.6f}")
	assert is_closed(res, ref[p]), f"Le seuil pour l'image {p} vaut {res} au lieu de {ref[p]}"


# ==================================================
# endregion Seuil automatique
# ==================================================

# ==================================================
# region Trajectoires
# ==================================================
def test_tracking():
	"""Vérifie le tracking à partir d'un fichier de localisations de référence."""
	palm = Palm()
	file = "stack"
	suffix = get_loc_suffix()
	suffix_trc = suffix + "-" + get_trc_suffix()

	path = REF_DIR / f"{file}-localizations-{suffix}.csv"
	if path.exists() and path.is_file():
		localizations = pd.read_csv(path)
		tracks = palm.tracking(localizations, max_distance)
		if save_output: tracks.round(6).to_csv(f"{OUTPUT_DIR}/{file}-tracking-{suffix_trc}.csv", index=False)

		assert len(tracks) > 0, "Aucun Tracking trouvé"

		path = REF_DIR / f"{file}-tracking-{suffix_trc}.csv"
		if path.exists() and path.is_file():
			print(f"Comparaison avec : '{path}'")
			ref = pd.read_csv(path)
			assert compare_points(tracks, ref, group_cols=["Track"]), f"Test invalide pour les paramètres {suffix_trc}"
	else:
		Ui.print_warning(f"Fichier de localisations '{path}' indisponible.")


# --------------------------------------------------
@pytest.mark.parametrize("data", [
		pytest.param(pd.DataFrame(np.zeros((3, Parsing.N_COL_LOC)), columns=Parsing.FILES_COLUMNS["Localization"]["columns"]), id="zero-localizations"),
		pytest.param(pd.DataFrame(), id="empty-data")])
def test_tracking_empty(data):
	"""Vérifie le retour vide pour chaque entrée sans localisation exploitable."""
	tracks = Palm().tracking(data, max_distance)
	assert tracks.empty


# --------------------------------------------------
def test_tracking_discontinuous():
	"""Vérifie sur le tracking avec un fichier qui possède des plans sans localisations."""
	palm = Palm()
	path = INPUT_DIR / "localizations_discontinuous.csv"
	if path.exists() and path.is_file():
		localizations = pd.read_csv(path)
		tracks = palm.tracking(localizations, max_distance)
		if save_output: tracks.round(6).to_csv(f"{OUTPUT_DIR}/discontinuous-tracking.csv", index=False)


# --------------------------------------------------
@pytest.mark.parametrize("mode", range(3), ids=['stationary', 'diffusion', 'linear'])
def test_blinking_reconnection(mode: int):
	"""Vérifie la reconnexion et la conversion du nombre de plans manquants en écart entre plans."""
	palm = Palm()
	file = "tracking"
	path = Path(f"{INPUT_DIR}/{file}.csv")
	if path.exists() and path.is_file():
		t_input = pd.read_csv(path)
		t_output = palm.blinking_reconnection(t_input, 1, mode, 3, 2)
		if save_output: t_output.round(6).to_csv(f"{OUTPUT_DIR}/{file}-blinking-{mode}.csv", index=False)

		assert len(t_output) > 0, "Aucun Tracking trouvé"

		ref_path = REF_DIR / f"{file}-blinking-{mode}.csv"
		if ref_path.exists() and ref_path.is_file():
			print(f"Comparaison avec : '{ref_path}'")
			ref = pd.read_csv(ref_path)
			assert compare_points(t_output, ref, group_cols=["Track", "Plane"]), f"Test invalide pour les paramètres {mode}"
	else:
		Ui.print_warning(f"Fichier de Tracking '{path}' indisponible.")


# --------------------------------------------------
def test_blinking_reconnection_empty():
	"""Vérifie le retour vide sans trajectoire."""
	palm = Palm()
	tracks = palm.blinking_reconnection(pd.DataFrame(), 1, 0, 4, 2)
	assert tracks.empty


# --------------------------------------------------
@pytest.mark.parametrize("p", [True, False], ids=['ind-3d-enabled', 'ind-3d-disabled'])
def test_track_analysis(p):
	"""Vérifie les analyses des trajectoires avec ou sans diffusion instantanée et 3D."""
	palm = Palm()
	file = "tracking2"
	path = Path(f"{INPUT_DIR}/{file}.csv")
	if path.exists() and path.is_file():
		t_input = pd.read_csv(path)
		# Test avec ou sans diffusion instantanée et prise en compte de la 3D.
		t_output = palm.track_analysis(t_input, True, p, p, 1, 1, 1, np.array([4], dtype=float))
		for name in ["MSD", "InD", "Fit"]:
			if t_output[name].empty: continue
			if save_output: t_output[name].round(6).to_csv(f"{OUTPUT_DIR}/{file}-{name}-{p}.csv", index=False)

			ref_path = REF_DIR / f"{file}-{name}-{p}.csv"
			if ref_path.exists() and ref_path.is_file():
				print(f"Comparaison avec : '{ref_path}'")
				ref = pd.read_csv(ref_path)
				# Comparaison entre le DataFrame t_output[name] et ref avec une tolérance de 1e-5 et ignore les NaN
				np.testing.assert_allclose(t_output[name].to_numpy(float), ref.to_numpy(float), rtol=1e-5, atol=1e-5, equal_nan=True)
	else:
		Ui.print_warning(f"Fichier de Tracking '{path}' indisponible.")


# --------------------------------------------------
@pytest.mark.parametrize("mode", range(4), ids=['no-fit', 'linear', 'power', 'exponential'])
def test_track_analysis_fit_modes(mode: int):
	"""Vérifie les quatre modes d’ajustement des trajectoires."""
	palm = Palm()
	file = "tracking2"
	path = Path(f"{INPUT_DIR}/{file}.csv")
	if path.exists() and path.is_file():
		t_input = pd.read_csv(path)
		# Test sur différents modes d'ajustement.
		t_output = palm.track_analysis(t_input, False, False, False, 1, 1, mode, np.array([4], dtype=float))
		for name in ["MSD", "InD", "Fit"]:
			if t_output[name].empty: continue
			if save_output: t_output[name].round(6).to_csv(f"{OUTPUT_DIR}/{file}-{name}-{mode}.csv", index=False)

			ref_path = REF_DIR / f"{file}-{name}-{mode}.csv"
			if ref_path.exists() and ref_path.is_file():
				print(f"Comparaison avec : '{ref_path}'")
				ref = pd.read_csv(ref_path)
				# Sans plateau observé, les paramètres exponentiels sont sensibles aux variations numériques entre plateformes.
				# La tolérance relative de ce mode est alignée sur les tests C++ ; les autres modes restent à 1e-5.
				rtol = 1e-3 if mode == 3 else 1e-5
				np.testing.assert_allclose(t_output[name].to_numpy(float), ref.to_numpy(float), rtol=rtol, atol=1e-5, equal_nan=True)
	else:
		Ui.print_warning(f"Fichier de Tracking '{path}' indisponible.")


# --------------------------------------------------
@pytest.mark.parametrize("mode", [1, 2, 3], ids=['linear', 'power', 'exponential'])
def test_track_analysis_recovers_synthetic_model(mode: int):
	"""Retrouve les paramètres connus d'un MSD synthétique via l'analyse complète d'une trajectoire."""
	lags = np.arange(1, 9, dtype=float)
	if mode == 1:
		expected_msd = 2 * lags + 3
		columns, expected_params = ["A (μm²/s)", "B (μm²)"], [0.5, 3]
	elif mode == 2:
		expected_msd = 2 * lags ** 1.3
		columns, expected_params = ["Alpha", "B (μm²)"], [1.3, 2]
	else:
		expected_msd = 20 * (1 - np.exp(-lags / 3))
		# Le décalage temporel et l'ordonnée initiale ne sont pas identifiables séparément.
		columns, expected_params = ["A (μm²)", "B (s)"], [20, 3]

	def msd_residual(coordinates):
		"""Construit les positions à partir du MSD cible, indépendamment du moteur de fit testé."""
		points = np.vstack(([0.0, 0.0], coordinates.reshape(-1, 2)))
		return np.array([np.mean(np.sum((points[k:] - points[:-k]) ** 2, axis=1)) for k in range(1, len(points))]) - expected_msd

	# L'API prend des positions : synthétiser une trajectoire dont le MSD suit exactement le modèle choisi.
	rng = np.random.default_rng(42)
	initial = np.cumsum(rng.normal(size=(len(lags), 2)) * 2, axis=0)
	simulation = least_squares(msd_residual, initial.ravel(), ftol=1e-12, xtol=1e-12, gtol=1e-12, max_nfev=1000)
	np.testing.assert_allclose(msd_residual(simulation.x), 0, atol=1e-6)
	positions = np.vstack(([0.0, 0.0], simulation.x.reshape(-1, 2)))
	planes = np.arange(1, len(positions) + 1)
	tracks = pd.DataFrame({"Track": 1, "Plane": planes, "Id": planes, "X": positions[:, 0], "Y": positions[:, 1],
						   "Z":     0.0, "Integrated Intensity": 100.0, "Surface": 1})

	result = Palm().track_analysis(tracks, True, False, False, 1, 1, mode, np.array([4], dtype=float))
	np.testing.assert_allclose(result["MSD"].iloc[0, 1:].to_numpy(float), expected_msd, atol=1e-6)
	assert len(result["Fit"]) == 1
	fit = result["Fit"].iloc[0]
	np.testing.assert_allclose(fit[columns].to_numpy(float), expected_params, rtol=1e-2, atol=1e-2)
	# La colonne historique « MSE » contient le coefficient R².
	assert fit["MSE"] == pytest.approx(1, abs=1e-5)


# --------------------------------------------------
@pytest.mark.parametrize("selection, is_msd, fit_length", [
		pytest.param("all", False, 4, id="diffusion-without-msd"),
		pytest.param("first", True, 18, id="single-observation"),
		pytest.param("empty", True, 18, id="no-observations")])
def test_track_analysis_small_inputs(selection, is_msd, fit_length):
	"""Vérifie les calculs désactivés et les entrées trop petites pour une trajectoire."""
	palm = Palm()
	path = INPUT_DIR / "tracking2.csv"
	if path.exists() and path.is_file():
		tracks = pd.read_csv(path)
		if selection == "first": tracks = tracks.iloc[[0]].copy()
		if selection == "empty": tracks = pd.DataFrame()
		palm.track_analysis(tracks, is_msd, True, False, 1, 1, 1, np.array([fit_length], dtype=float))
	else:
		Ui.print_warning(f"Fichier de Tracking '{path}' indisponible.")


# --------------------------------------------------
@pytest.mark.parametrize("ids, planes, fit_length, mode, sizes", [
		pytest.param([1, 1], [1, 100], 4, 1, (102, 1, 11), id="long-blinking"),
		pytest.param([1, 1, 1, 2, 2], [8000, 8001, 8009, 15000, 15009], 1, 2, (23, 8, 23), id="separate-tracks"),
		pytest.param([1], [16000], 4, 3, (1, 1, 13), id="single-point")])
def test_track_analysis_buffer_sizes(monkeypatch, ids, planes, fit_length, mode, sizes):
	"""Vérifie les allocations sans appeler la DLL, notamment quand le blinking dépasse l'ancienne marge."""
	columns = Parsing.FILES_COLUMNS["Tracking"]["columns"]
	tracks = pd.DataFrame(np.ones((len(ids), len(columns))), columns=columns)
	tracks["Track"], tracks["Plane"] = ids, planes
	palm = Palm.__new__(Palm)
	palm._dll = Mock()
	parser = Mock(return_value=pd.DataFrame())
	monkeypatch.setattr(Parsing, "parse_result", parser)

	palm.track_analysis(tracks, True, True, False, 1, 1, mode, np.array([fit_length], dtype=float))

	palm._dll.TrackAnalysis.assert_called_once()
	assert tuple(call.args[0].size for call in parser.call_args_list) == sizes


# ==================================================
# endregion Trajectoires
# ==================================================

# ==================================================
# region Alignement et ondelettes
# ==================================================
@pytest.mark.parametrize("mode, upscale, filename", [
		pytest.param("copy", 1, "stack-aligned-copy.tif", id="identity"),
		pytest.param("upsample", 2, "stack-aligned-upsampling.tif", id="upsampling"),
		pytest.param("transpose", 1, "stack-aligned-transpose.tif", id="transposition")])
def test_align(mode, upscale, filename):
	"""Vérifie indépendamment chaque mode d'alignement en conservant ses sorties pour inspection."""
	palm = Palm()
	stack = FileIO.open_tif(f"{INPUT_DIR}/stack.tif")
	z, h, w = stack.shape
	factors: np.ndarray = np.zeros((2, 10), dtype=float)
	if mode == "transpose":
		factors[0, 8] = factors[1, 7] = 1.0
	else:
		factors[0, 7] = factors[1, 8] = 1.0

	aligned = palm.align(stack, factors, upscale)
	if save_output: FileIO.save_tif(aligned, OUTPUT_DIR / filename)
	if mode == "copy":
		assert aligned.shape == stack.shape, "Mode Copie : les dimensions doivent être identiques"
		assert np.allclose(aligned, stack, atol=0, rtol=0), "Mode Copie : le résultat doit être IDENTIQUE au stack d'origine."
	elif mode == "upsample":
		assert aligned.shape == (z, 2 * h, 2 * w), "Mode Upscale : pour un stack 3D seule X et Y doivent être doublées."
		# Référence par répétition des pixels, avec le même padding exclu que dans le scénario initial.
		ref = np.repeat(np.repeat(stack, 2, axis=-2), 2, axis=-1)
		assert np.allclose(aligned[..., :-1, :-1], ref[..., :-1, :-1], atol=0, rtol=0), (
				"Mode Upscale : le résultat doit être IDENTIQUE au stack d'origine.")
	else:
		assert aligned.shape == stack.shape, "Mode Transpose : les dimensions doivent être identiques malgré la transposition."


# --------------------------------------------------
@pytest.mark.parametrize("level", range(5), ids=['level-0', 'level-1', 'level-2', 'level-3', 'level-4'])
def test_wavelet(level: int):
	"""Vérifie le comportement de récupérer un plan d'ondelette."""
	palm = Palm()

	# --- Lecture stack ---
	file = "stack"
	stack = FileIO.open_tif(f"{INPUT_DIR}/{file}.tif")

	wavelet = palm.wavelet(stack, level)
	if save_output: FileIO.save_tif(wavelet, f"{OUTPUT_DIR}/{file}-wavelet-{level}.tif")
	assert wavelet.shape == stack.shape, "Les dimensions doivent être identiques"


# ==================================================
# endregion Alignement et ondelettes
# ==================================================

# ==================================================
# region Astigmatisme 3D
# ==================================================
@pytest.mark.parametrize("center, filename", [
		pytest.param(False, "astigmatism_3d_model.csv", id="no-centering"),
		pytest.param(True, "astigmatism_3d_model_centered.csv", id="centered-model")])
def test_astigmatism_3d_calibration(center, filename):
	"""Vérifie la calibration avec ou sans recentrage du modèle."""
	palm = Palm()
	localizations = pd.read_csv(INPUT_DIR / "astigmatism_3d_calibration.csv")
	points = localizations.loc[:, ["Sigma X", "Sigma Y", "Z"]].to_numpy(dtype=float, copy=True)
	res = palm.astigmatism_3d_calibration(points, 200, center)
	if save_output: res.round(6).to_csv(OUTPUT_DIR / filename, index=MODEL_ROWS)
	ref = pd.read_csv(REF_DIR / filename, index_col=0)
	np.testing.assert_allclose(res, ref, atol=0.1, rtol=0)


# --------------------------------------------------
def test_astigmatism_3d_estimation():
	"""Vérifie le comportement de l'estimation de l'astigmatisme 3D."""
	palm = Palm()

	# --- Lecture des fichiers ---
	localizations = pd.read_csv(INPUT_DIR / "astigmatism_3d_calibration.csv")
	localizations = localizations[localizations["Bead"] == localizations.loc[0, "Bead"]]
	points = localizations.loc[:, ["Sigma X", "Sigma Y", "Z"]].to_numpy(dtype=float, copy=True)
	model = pd.read_csv(REF_DIR / "astigmatism_3d_model.csv", index_col=0)
	res = palm.astigmatism_3d_estimation(points[:, :-1], 200, model.to_numpy(), 460)
	ref = localizations["Z"].to_numpy()

	# Vérification que Z est trié en ordre décroissant
	assert np.all(res[:-1, 0] >= res[1:, 0]), "Le fichier contient les éléments Z en ordre décroissant, le résultat doit donc être dans le même ordre."

	# Vérification très permissive (arrondi et estimateurs sont les fautifs)
	assert np.allclose(res[:, 0], ref, atol=40, rtol=0), f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res[:, 0]}"

	# Le score est calculé sur les sigmas prédits au Z effectivement retenu, sans normalisation par la pile.
	predicted = np.column_stack([sigma_model(axis, res[:, 0], 200) for axis in model.to_numpy()])
	relative_error = (points[:, :-1] - predicted) / predicted
	expected_score = 1 / (1 + np.mean(relative_error * relative_error, axis=1) / 0.2 ** 2)
	np.testing.assert_allclose(res[:, 1], expected_score, atol=1e-12, rtol=1e-12)
	assert np.all((res[:, 1] >= 0) & (res[:, 1] <= 1))

# ==================================================
# endregion Astigmatisme 3D
# ==================================================


# ==================================================
# endregion Appels de la DLL
# ==================================================
