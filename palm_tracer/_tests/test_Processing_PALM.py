"""Teste l'encapsulation et l'utilisation de la DLL PALM."""

import pytest

from palm_tracer._tests.Utils import *
from palm_tracer.Processing import Palm, Parsing
from palm_tracer.Processing.Parsing import MODEL_ROWS
from palm_tracer.Tools import FileIO


# ==================================================
# region Initialisation
# ==================================================
##################################################
def test_palm_dll_valid():
	"""Vérifie sur la présence d ela DLL PALM."""
	palm = Palm()
	assert palm.is_valid(), "Erreur lors du chargement de la DLL"


# ==================================================
# endregion Initialisation
# ==================================================

# ==================================================
# region Appels de la DLL
# ==================================================
##################################################
def test_palm_cpu_empty_result():
	"""Vérifie sur le lancement de PALM sur une noire."""
	palm = Palm()
	stack = np.zeros((10, 10, 10), dtype=np.uint16)
	res = palm.localization(stack, default_threshold, default_watershed, default_fit, get_fit_params(default_fit))
	assert res.empty


##################################################
@pytest.mark.parametrize("plane", range(10), ids=['plane-1', 'plane-2', 'plane-3', 'plane-4', 'plane-5', 'plane-6', 'plane-7', 'plane-8', 'plane-9', 'plane-10'])
@pytest.mark.parametrize("fit", range(6), ids=['no-fit', 'gaussian-xy', 'gaussian-sigma', 'gaussian-sigma-xy', 'gaussian-theta', 'spline'])
def test_palm_cpu_image(plane, fit):
	"""Vérifie sur le lancement de PALM sur une frame."""
	palm = Palm()
	file = "stack"
	stack = FileIO.open_tif(f"{INPUT_DIR}/{file}.tif")
	suffix = get_loc_suffix(fit)

	localizations = palm.localization(stack[plane], default_threshold, default_watershed, fit, get_fit_params(fit))
	if save_output: localizations.round(6).to_csv(f"{OUTPUT_DIR}/{file}-localizations-{plane}_{suffix}.csv", index=False)

	assert len(localizations) > 0, "Aucune localisation trouvé"

	path = REF_DIR / f"{file}-localizations-{plane}_{suffix}.csv"
	if path.exists() and path.is_file():
		print(f"Comparaison avec : '{path}'")
		ref = pd.read_csv(path)
		assert compare_points(localizations, ref), f"Test invalide pour les paramètres {plane}_{suffix}"


##################################################
@pytest.mark.parametrize("watershed", [True, False], ids=['with-watershed', 'no-watershed'])
@pytest.mark.parametrize("fit", range(6), ids=['no-fit', 'gaussian-xy', 'gaussian-sigma', 'gaussian-sigma-xy', 'gaussian-theta', 'spline'])
def test_palm_cpu_stack(watershed, fit):
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


##################################################
def test_palm_cpu_stack_plane_selection():
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


##################################################
def test_palm_cpu_stack_dll_check_quadrant():
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


##################################################
@pytest.mark.parametrize("i", range(10), ids=['plane-1', 'plane-2', 'plane-3', 'plane-4', 'plane-5', 'plane-6', 'plane-7', 'plane-8', 'plane-9', 'plane-10'])
def test_cpu_auto_threshold(i):
	"""Vérifie l'auto-seuillage avec la DLL CPU."""
	palm = Palm()
	image = FileIO.open_tif(f"{INPUT_DIR}/stack.tif")
	ref = [63.639888, 65.789447, 63.192296, 64.375352, 63.954150,
		   63.400043, 66.521994, 63.373237, 62.515444, 63.866017]
	res = palm.auto_threshold(image[i], get_fit_params(0))
	# print(f"Image {i} : {res:.6f} VS {ref[i]:.6f}")
	assert is_closed(res, ref[i]), f"Le seuil pour l'image {i} vaut {res} au lieu de {ref[i]}"


##################################################
@pytest.mark.parametrize("watershed", [True, False], ids=['with-watershed', 'no-watershed'])
@pytest.mark.parametrize("fit", range(6), ids=['no-fit', 'gaussian-xy', 'gaussian-sigma', 'gaussian-sigma-xy', 'gaussian-theta', 'spline'])
def test_tracking(watershed, fit):
	"""Vérifie le tracking."""
	palm = Palm()
	file = "stack"
	suffix = get_loc_suffix(fit, watershed)
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


##################################################
def test_tracking_empty():
	"""Vérifie les entrées sans localisation exploitable."""
	palm = Palm()
	tracks = palm.tracking(pd.DataFrame(np.zeros((3, Parsing.N_COL_LOC)), columns=Parsing.FILES_COLUMNS["Localization"]["columns"]), max_distance)
	assert tracks.empty

	tracks = palm.tracking(pd.DataFrame(), max_distance)
	assert tracks.empty


##################################################
def test_tracking_discontinuous():
	"""Vérifie sur le tracking avec un fichier qui possède des plans sans localisations."""
	palm = Palm()
	path = INPUT_DIR / f"localizations_discontinuous.csv"
	if path.exists() and path.is_file():
		localizations = pd.read_csv(path)
		tracks = palm.tracking(localizations, max_distance)
		if save_output: tracks.round(6).to_csv(f"{OUTPUT_DIR}/discontinuous-tracking.csv", index=False)


##################################################
@pytest.mark.parametrize("i", range(3), ids=['stationary', 'diffusion', 'linear'])
def test_blinking_reconnection(i):
	"""Vérifie le tracking."""
	palm = Palm()
	file = "tracking"
	path = Path(f"{INPUT_DIR}/{file}.csv")
	if path.exists() and path.is_file():
		t_input = pd.read_csv(path)
		t_output = palm.blinking_reconnection(t_input, 1, i, 4, 2)
		if save_output: t_output.round(6).to_csv(f"{OUTPUT_DIR}/{file}-blinking-{i}.csv", index=False)

		assert len(t_output) > 0, "Aucun Tracking trouvé"

		ref_path = REF_DIR / f"{file}-blinking-{i}.csv"
		if ref_path.exists() and ref_path.is_file():
			print(f"Comparaison avec : '{ref_path}'")
			ref = pd.read_csv(ref_path)
			assert compare_points(t_output, ref, group_cols=["Track", "Plane"]), f"Test invalide pour les paramètres {i}"
	else:
		Ui.print_warning(f"Fichier de Tracking '{path}' indisponible.")


##################################################
def test_blinking_reconnection_empty():
	"""Vérifie le retour vide sans trajectoire."""
	palm = Palm()
	tracks = palm.blinking_reconnection(pd.DataFrame(), 1, 0, 4, 2)
	assert tracks.empty


##################################################
@pytest.mark.parametrize("p", [True, False], ids=['ind-3d-enabled', 'ind-3d-disabled'])
def test_tracks_compute(p):
	"""Vérifie les calculs de trajectoires avec ou sans diffusion instantanée et 3D."""
	palm = Palm()
	file = "tracking2"
	path = Path(f"{INPUT_DIR}/{file}.csv")
	if path.exists() and path.is_file():
		t_input = pd.read_csv(path)
		# Test avec ou sans diffusion instantanée et prise en compte de la 3D.
		t_output = palm.tracks_compute(t_input, True, p, p, 1, 1, 1, np.array([4], dtype=float))
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


##################################################
@pytest.mark.parametrize("mode", range(4), ids=['no-fit', 'linear', 'power', 'exponential'])
def test_tracks_compute_fit_modes(mode):
	"""Vérifie les quatre modes d’ajustement des trajectoires."""
	palm = Palm()
	file = "tracking2"
	path = Path(f"{INPUT_DIR}/{file}.csv")
	if path.exists() and path.is_file():
		t_input = pd.read_csv(path)
		# Test sur différents modes d'ajustement.
		t_output = palm.tracks_compute(t_input, False, False, False, 1, 1, mode, np.array([4], dtype=float))
		for name in ["MSD", "InD", "Fit"]:
			if t_output[name].empty: continue
			if save_output: t_output[name].round(6).to_csv(f"{OUTPUT_DIR}/{file}-{name}-{mode}.csv", index=False)

			ref_path = REF_DIR / f"{file}-{name}-{mode}.csv"
			if ref_path.exists() and ref_path.is_file():
				print(f"Comparaison avec : '{ref_path}'")
				ref = pd.read_csv(ref_path)
				# Comparaison entre le DataFrame t_output[name] et ref avec une tolérance de 1e-5 et ignore les NaN
				np.testing.assert_allclose(t_output[name].to_numpy(float), ref.to_numpy(float), rtol=1e-5, atol=1e-5, equal_nan=True)
	else:
		Ui.print_warning(f"Fichier de Tracking '{path}' indisponible.")


##################################################
@pytest.mark.parametrize("selection, is_msd, fit_length", [
		pytest.param("all", False, 4, id="diffusion-without-msd"),
		pytest.param("first", True, 18, id="single-observation"),
		pytest.param("empty", True, 18, id="no-observations")])
def test_tracks_compute_small_inputs(selection, is_msd, fit_length):
	"""Vérifie les calculs désactivés et les entrées trop petites pour une trajectoire."""
	palm = Palm()
	path = INPUT_DIR / "tracking2.csv"
	if path.exists() and path.is_file():
		tracks = pd.read_csv(path)
		if selection == "first": tracks = tracks.iloc[[0]].copy()
		if selection == "empty": tracks = pd.DataFrame()
		palm.tracks_compute(tracks, is_msd, True, False, 1, 1, 1, np.array([fit_length], dtype=float))
	else:
		Ui.print_warning(f"Fichier de Tracking '{path}' indisponible.")


##################################################
def test_align():
	"""Vérifie le comportement de l'alignement."""
	palm = Palm()

	# --- Lecture stack ---
	file = "stack"
	stack = FileIO.open_tif(f"{INPUT_DIR}/{file}.tif")
	z, h, w = stack.shape

	# --- Facteurs de test (identité) ---
	factors = np.zeros((2, 10), dtype=float)
	factors[0, 7] = 1.0
	factors[1, 8] = 1.0

	aligned = palm.align(stack, factors, 1)
	if save_output: FileIO.save_tif(aligned, f"{OUTPUT_DIR}/{file}-aligned-copy.tif")
	assert aligned.shape == stack.shape, "Mode Copie : les dimensions doivent être identiques"
	assert np.allclose(aligned, stack, atol=0, rtol=0), "Mode Copie : le résultat doit être IDENTIQUE au stack d'origine."

	aligned = palm.align(stack, factors, 2)
	if save_output: FileIO.save_tif(aligned, f"{OUTPUT_DIR}/{file}-aligned-upsampling.tif")
	assert aligned.shape == (z, 2 * h, 2 * w), "Mode Upscale : pour un stack 3D seule X et Y doivent être doublées."

	def up2_nn(arr): return np.repeat(np.repeat(arr, 2, axis=-2), 2, axis=-1)

	ref = np.stack([up2_nn(stack[z]) for z in range(stack.shape[0])], axis=0)
	assert np.allclose(aligned[..., :-1, :-1], ref[..., :-1, :-1], atol=0, rtol=0), "Mode Upscale : le résultat doit être IDENTIQUE au stack d'origine."
	# On supprime la derniere ligne et colonne car 0 padding en cas de débord dans l'algo original.

	# --- Facteurs de test (transposition) ---
	factors = np.zeros((2, 10), dtype=float)
	factors[0][8] = 1.0
	factors[1][7] = 1.0

	aligned = palm.align(stack, factors, 1)
	if save_output: FileIO.save_tif(aligned, f"{OUTPUT_DIR}/{file}-aligned-transpose.tif")
	assert aligned.shape == stack.shape, "Mode Transpose : les dimensions doivent être identiques malgrè la transposition."


##################################################
@pytest.mark.parametrize("i", range(5), ids=['level-0', 'level-1', 'level-2', 'level-3', 'level-4'])
def test_wavelett(i):
	"""Vérifie le comportement de récupérer un plan d'ondelette."""
	palm = Palm()

	# --- Lecture stack ---
	file = "stack"
	stack = FileIO.open_tif(f"{INPUT_DIR}/{file}.tif")

	wavelett = palm.wavelett(stack, i)
	if save_output: FileIO.save_tif(wavelett, f"{OUTPUT_DIR}/{file}-wavelett-{i}.tif")
	assert wavelett.shape == stack.shape, "Les dimensions doivent être identiques"


##################################################
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


##################################################
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

	# Vérification de l'erreur maximale en pixel²
	assert np.max(res[:, 1]) < 0.15, f"Résultat incorrect.\tAttendu : 0.15\tObtenu : {np.max(res[:, 1])}"

# ==================================================
# endregion Appels de la DLL
# ==================================================
