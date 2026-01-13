""" Fichier des tests pour l'utilisation de la DLL CPU. """
import pytest

from palm_tracer._tests.Utils import *
from palm_tracer.Processing import Palm
from palm_tracer.Tools import open_tif, save_tif

os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_palm_cpu_image():
	""" Test sur le lancement de PALM sur une frame. """
	palm = Palm()
	file = "stack"
	stack = open_tif(f"{INPUT_DIR}/{file}.tif")
	for plane in range(stack.shape[0]):
		for fit in range(6):
			suffix = get_loc_suffix(fit)

			localizations = palm.localization(stack[plane], default_threshold, default_watershed, fit, get_fit_params(fit))
			if save_output: localizations.round(6).to_csv(f"{OUTPUT_DIR}/{file}-localizations-{plane}_{suffix}.csv", index=False)

			assert len(localizations) > 0, "Aucune localisation trouvé"

			path = Path(f"{INPUT_DIR}/ref/{file}-localizations-{plane}_{suffix}.csv")
			if path.exists() and path.is_file():
				print(f"Comparaison avec : '{path}'")
				ref = pd.read_csv(path)
				assert compare_points(localizations, ref), f"Test invalide pour les paramètres {plane}_{suffix}"


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_palm_cpu_stack():
	""" Test sur le lancement de PALM sur une pile. """
	palm = Palm()
	file = "stack"
	stack = open_tif(f"{INPUT_DIR}/{file}.tif")
	for watershed in [True, False]:
		for fit in range(6):
			suffix = get_loc_suffix(fit, watershed)

			localizations = palm.localization(stack, default_threshold, watershed, fit, get_fit_params(fit))
			if save_output: localizations.round(6).to_csv(f"{OUTPUT_DIR}/{file}-localizations-{suffix}.csv", index=False)

			assert len(localizations) > 0, "Aucune localisation trouvé"

			path = Path(f"{INPUT_DIR}/ref/{file}-localizations-{suffix}.csv")
			if path.exists() and path.is_file():
				print(f"Comparaison avec : '{path}'")
				ref = pd.read_csv(path)
				assert compare_points(localizations, ref, 0.001), f"Test invalide pour les paramètres {suffix}"


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_palm_cpu_stack_plane_selection():
	""" Test sur le lancement de PALM sur une pile. """
	palm = Palm()
	file = "stack"
	stack = open_tif(f"{INPUT_DIR}/{file}.tif")
	suffix = get_loc_suffix()

	localizations = palm.localization(stack, default_threshold, default_watershed, default_fit, get_fit_params(default_fit), [2, 3, 4, 5, 6])
	if save_output: localizations.round(6).to_csv(f"{OUTPUT_DIR}/{file}-localizations-plane_select-{suffix}.csv", index=False)
	assert len(localizations) > 0, "Aucune localisation trouvé"
	path = Path(f"{INPUT_DIR}/ref/{file}-localizations-plane_select-{suffix}.csv")
	if path.exists() and path.is_file():
		print(f"Comparaison avec : '{path}'")
		ref = pd.read_csv(path)
		assert compare_points(localizations, ref, 0.001), f"Test invalide pour les paramètres {suffix}"


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_palm_cpu_stack_dll_check_quadrant():
	"""	Test sur le lancement de PALM sur une pile. """
	palm = Palm()
	suffix = get_loc_suffix()
	file = "stack_quadrant"
	stack = open_tif(f"{INPUT_DIR}/{file}.tif")

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

	path = Path(f"{INPUT_DIR}/ref/{file}-localizations-{suffix}.csv")
	if path.exists() and path.is_file():
		ref = pd.read_csv(path)
		assert compare_points(localizations, ref), "Test invalide pour la vérification des quadrants."


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_cpu_auto_threshold():
	""" Test basique sur l'auto-seuillage avec la DLL CPU. """
	palm = Palm()
	image = open_tif(f"{INPUT_DIR}/stack.tif")
	ref = [63.639888, 65.789447, 63.192296, 64.375352, 63.954150,
		   63.400043, 66.521994, 63.373237, 62.515444, 63.866017]
	for i in range(image.shape[0]):
		res = palm.auto_threshold(image[i], get_fit_params(0))
		# print(f"Image {i} : {res:.6f} VS {ref[i]:.6f}")
		assert is_closed(res, ref[i]), f"Le seuil pour l'image {i} vaut {res} au lieu de {ref[i]}"


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_tracking():
	"""Test basique sur le tracking."""
	palm = Palm()
	file = "stack"
	for watershed in [True, False]:
		for fit in range(6):
			suffix = get_loc_suffix(fit, watershed)
			suffix_trc = suffix + "-" + get_trc_suffix()

			path = Path(f"{INPUT_DIR}/ref/{file}-localizations-{suffix}.csv")
			if path.exists() and path.is_file():
				localizations = pd.read_csv(path)
				tracks = palm.tracking(localizations, max_distance, min_life, decrease, cost_birth)
				if save_output: tracks.round(6).to_csv(f"{OUTPUT_DIR}/{file}-tracking-{suffix_trc}.csv", index=False)

				assert len(tracks) > 0, "Aucun Tracking trouvé"

				path = Path(f"{INPUT_DIR}/ref/{file}-tracking-{suffix_trc}.csv")
				if path.exists() and path.is_file():
					print(f"Comparaison avec : '{path}'")
					ref = pd.read_csv(path)
					assert compare_points(tracks, ref, group_cols=["Track"]), f"Test invalide pour les paramètres {suffix_trc}"
			else:
				print_warning(f"Fichier de localisations '{path}' indisponible.")

	tracks = palm.tracking(pd.DataFrame(), max_distance, min_life, decrease, cost_birth)
	assert tracks.empty


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_blinking_reconnection():
	"""Test basique sur le tracking."""
	palm = Palm()
	file = "tracking"
	path = Path(f"{INPUT_DIR}/{file}.csv")
	if path.exists() and path.is_file():
		t_input = pd.read_csv(path)
		for i in range(3):
			t_output = palm.blinking_reconnection(t_input, 1, i, 4, 2)
			if save_output: t_output.round(6).to_csv(f"{OUTPUT_DIR}/{file}-blinking-{i}.csv", index=False)

			assert len(t_output) > 0, "Aucun Tracking trouvé"

			ref_path = Path(f"{INPUT_DIR}/ref/{file}-blinking-{i}.csv")
			if ref_path.exists() and ref_path.is_file():
				print(f"Comparaison avec : '{ref_path}'")
				ref = pd.read_csv(ref_path)
				assert compare_points(t_output, ref, group_cols=["Track", "Plane"]), f"Test invalide pour les paramètres {i}"
	else:
		print_warning(f"Fichier de Tracking '{path}' indisponible.")

	tracks = palm.blinking_reconnection(pd.DataFrame(), 1, 0, 4, 2)
	assert tracks.empty


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_tracks_compute():
	"""Test basique sur le tracking."""
	palm = Palm()
	file = "tracking2"
	path = Path(f"{INPUT_DIR}/{file}.csv")
	if path.exists() and path.is_file():
		t_input = pd.read_csv(path)
		# Test avec ou sans les mise à jour de log et la 3D
		for p in [True, False]:
			t_output = palm.tracks_compute(t_input, True, p, p, p, 1, 1, 1, np.array([4], dtype=np.float64))
			for name in ["MSD", "InD", "Fit"]:
				if t_output[name].empty: continue
				if save_output: t_output[name].round(6).to_csv(f"{OUTPUT_DIR}/{file}-{name}-{p}.csv", index=False)

				ref_path = Path(f"{INPUT_DIR}/ref/{file}-{name}-{p}.csv")
				if ref_path.exists() and ref_path.is_file():
					print(f"Comparaison avec : '{ref_path}'")
					ref = pd.read_csv(ref_path)
					# comparaison entre le dataframe t_output[name] et ref avec une toelrance de 1e-5 et ignore les Nan
					np.testing.assert_allclose(t_output[name].to_numpy(float), ref.to_numpy(float), rtol=1e-5, atol=1e-5, equal_nan=True)

		# Test sur différents mode de fit
		for mode in range(4):
			t_output = palm.tracks_compute(t_input, False, False, False, False, 1, 1, mode, np.array([4], dtype=np.float64))
			for name in ["MSD", "InD", "Fit"]:
				if t_output[name].empty: continue
				if save_output: t_output[name].round(6).to_csv(f"{OUTPUT_DIR}/{file}-{name}-{mode}.csv", index=False)

				ref_path = Path(f"{INPUT_DIR}/ref/{file}-{name}-{mode}.csv")
				if ref_path.exists() and ref_path.is_file():
					print(f"Comparaison avec : '{ref_path}'")
					ref = pd.read_csv(ref_path)
					# comparaison entre le dataframe t_output[name] et ref avec une toelrance de 1e-5 et ignore les Nan
					np.testing.assert_allclose(t_output[name].to_numpy(float), ref.to_numpy(float), rtol=1e-5, atol=1e-5, equal_nan=True)

		# Dernier True/False pour la couverture de code
		palm.tracks_compute(t_input, False, True, False, False, 1, 1, 1, np.array([4], dtype=np.float64))
		df = t_input.iloc[[0]].copy()  # note les double crochets → DataFrame, pas Series
		palm.tracks_compute(df, True, True, False, False, 1, 1, 1, np.array([18], dtype=np.float64))
		palm.tracks_compute(pd.DataFrame(), True, True, False, False, 1, 1, 1, np.array([18], dtype=np.float64))
	else:
		print_warning(f"Fichier de Tracking '{path}' indisponible.")


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_align():
	"""Test basique pour l'alignement."""
	palm = Palm()

	# --- Lecture stack ---
	file = "stack"
	stack = open_tif(f"{INPUT_DIR}/{file}.tif")
	z, h, w = stack.shape

	# --- Facteurs de test (identité) ---
	factors = np.zeros((2, 10), dtype=np.float64)
	factors[0, 7] = 1.0
	factors[1, 8] = 1.0

	aligned = palm.align(stack, factors, 1)
	if save_output: save_tif(aligned, f"{OUTPUT_DIR}/{file}-aligned-copy.tif")
	assert aligned.shape == stack.shape, "Mode Copie : les dimensions doivent être identiques"
	assert np.allclose(aligned, stack, atol=0, rtol=0), "Mode Copie : le résultat doit être IDENTIQUE au stack d'origine."

	aligned = palm.align(stack, factors, 2)
	if save_output: save_tif(aligned, f"{OUTPUT_DIR}/{file}-aligned-upsampling.tif")
	assert aligned.shape == (z, 2 * h, 2 * w), "Mode Upscale : pour un stack 3D seule X et Y doivent être doublées."

	def up2_nn(arr): return np.repeat(np.repeat(arr, 2, axis=-2), 2, axis=-1)

	ref = np.stack([up2_nn(stack[z]) for z in range(stack.shape[0])], axis=0)
	assert np.allclose(aligned[..., :-1, :-1], ref[..., :-1, :-1], atol=0, rtol=0), "Mode Upscale : le résultat doit être IDENTIQUE au stack d'origine."
	# On supprime la derniere ligne et colonne car 0 padding en cas de débord dans l'algo original.

	# --- Facteurs de test (transposition) ---
	factors = np.zeros((2, 10), dtype=np.float64)
	factors[0][8] = 1.0
	factors[1][7] = 1.0

	aligned = palm.align(stack, factors, 1)
	if save_output: save_tif(aligned, f"{OUTPUT_DIR}/{file}-aligned-transpose.tif")
	assert aligned.shape == stack.shape, "Mode Transpose : les dimensions doivent être identiques malgrè la transposition."


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_wavelett():
	"""Test basique pour récupérer un plan d'ondelette."""
	palm = Palm()

	# --- Lecture stack ---
	file = "stack"
	stack = open_tif(f"{INPUT_DIR}/{file}.tif")

	for i in range(5):
		wavelett = palm.wavelett(stack, i)
		if save_output: save_tif(wavelett, f"{OUTPUT_DIR}/{file}-wavelett-{i}.tif")
		assert wavelett.shape == stack.shape, "Les dimensions doivent être identiques"


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
@pytest.mark.xfail(reason="Calcul incorrect, en attente de correctif très certainement les sigma sont dans une unité intermédiaire sur le fichier en entrée.")
def test_astigmatism_3d_calibration():
	"""Test basique pour la calibration de l'astigatisme 3D."""
	palm = Palm()

	# --- Lecture d'un fichier de localisation ---
	localizations = pd.read_csv(f"{INPUT_DIR}/astigmatism_3d_calibration.csv")
	res = palm.astigmatism_3d_calibration(localizations.to_numpy(dtype=float, copy=True), 108)
	ref = pd.read_csv(Path(f"{INPUT_DIR}/ref/astigmatism_3d_model.csv"), index_col=0)
	assert np.allclose(res, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu: \n\t{ref}\nObtenu : \n\t{res}"


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
@pytest.mark.xfail(reason="Calcul incorrect, en attente de correctif très certainement les sigma sont dans une unité intermédiaire sur le fichier en entrée.")
def test_astigmatism_3d_estimation():
	"""Test basique pour l'estimation de l'astigmatisme 3D."""
	palm = Palm()

	# --- Lecture des fichiers ---
	localizations = pd.read_csv(f"{INPUT_DIR}/astigmatism_3d_calibration.csv")
	model = pd.read_csv(Path(f"{INPUT_DIR}/ref/astigmatism_3d_model.csv"), index_col=0)
	res = palm.astigmatism_3d_estimation(localizations.to_numpy(dtype=float, copy=True)[:,:-1], 108,model.to_numpy(),50)
	ref = localizations["Z"].to_numpy()
	assert np.allclose(res, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu: {ref}\nObtenu : {res}"
