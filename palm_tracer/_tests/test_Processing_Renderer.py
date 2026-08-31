"""Teste la production des rendus haute résolution."""

from palm_tracer._tests.Utils import *
from palm_tracer.Processing import Renderer


##################################################
def test_set_size():
	"""Vérifie le calcul de la taille d'une reconstruction."""
	r = Renderer()
	assert r._w == 1 and r._h == 1 and r._r == 1
	r.set_size(100, 200, 10)
	assert r._w == 1000 and r._h == 2000 and r._r == 10


##################################################
def test_finalize_rendering():
	"""Vérifie la saturation et le repliement cyclique d'un rendu en uint16."""
	img = np.array([[-1, 0, 1.9, 65535, 65536, 65537, 131073]], dtype=np.float64)
	mask = np.ones(img.shape, dtype=bool)
	res = Renderer.finalize_rendering(img, mask)
	ref = np.array([[0, 0, 1, 65535, 65535, 65535, 65535]], dtype=np.uint16)
	np.testing.assert_array_equal(res, ref)

	res = Renderer.finalize_rendering(img, mask, clip=False)
	ref = np.array([[65535, 0, 1, 65535, 0, 1, 1]], dtype=np.uint16)
	np.testing.assert_array_equal(res, ref)
	assert res.dtype == np.uint16
	np.testing.assert_array_equal(img, [[-1, 0, 1.9, 65535, 65536, 65537, 131073]])

	mask = np.zeros(img.shape, dtype=bool)
	res = Renderer.finalize_rendering(img, mask, bg_color=0)
	np.testing.assert_array_equal(res, 0)


##################################################
def test_get_localization_colors():
	# DataFrame vide
	"""Vérifie la génération des couleurs des localisations."""
	loc = pd.DataFrame(columns=["X", "Y", "Intensity"])
	res = Renderer.add_colors_to_localizations(loc, "Intensity")
	assert res.shape == (0, 3)

	# No Column selected
	loc = pd.DataFrame({"X": [1, 2], "Y": [3, 4], "Intensity": [10, 20]})
	res = Renderer.add_colors_to_localizations(loc)
	ref = np.array([[1, 3, 10, 1], [2, 4, 20, 1]], dtype=np.float64)
	np.testing.assert_array_equal(res, ref)

	# Selected columns
	res = Renderer.add_colors_to_localizations(loc, "Intensity")
	ref = np.array([[1, 3, 10, 10], [2, 4, 20, 20]], dtype=np.float64)
	np.testing.assert_array_equal(res, ref)

	# With negatives values
	loc = pd.DataFrame({"X": [1, 2], "Y": [3, 4], "Intensity": [-2, 3]})
	res = Renderer.add_colors_to_localizations(loc, "Intensity")
	ref = np.array([[1, 3, -2, 0], [2, 4, 3, 5]], dtype=np.float64)
	np.testing.assert_array_equal(res, ref)

	# With normalization
	loc = pd.DataFrame({"X": [1, 2], "Y": [3, 4], "Intensity": [2, 4]})
	res = Renderer.add_colors_to_localizations(loc, "Intensity", max_value=100)
	ref = np.array([[1, 3, 2, 50], [2, 4, 4, 100], ], dtype=np.float64)
	np.testing.assert_allclose(res, ref)

	# With 0 in colors
	loc = pd.DataFrame({"X": [1, 2], "Y": [3, 4], "Intensity": [0, 0]})
	res = Renderer.add_colors_to_localizations(loc, "Intensity")
	ref = np.array([[1, 3, 0, 1], [2, 4, 0, 1]], dtype=np.float64)
	np.testing.assert_array_equal(res, ref)


##################################################
def test_get_tracks_colors():
	# DataFrame vide
	"""Vérifie la génération des couleurs des trajectoires."""
	trc = pd.DataFrame(columns=["Track", "Plane", "X", "Y", "Integrated Intensity"])
	res = Renderer.add_colors_to_tracks(trc, "Track Number")
	assert res.shape == (0, 5)

	# No Column selected (and sorting)
	trc = pd.DataFrame({"Track": [2, 1, 1], "Plane": [5, 6, 3], "X": [2, 0, 0], "Y": [2, 1, 0], "Integrated Intensity": [7, 6, 5]})
	res = Renderer.add_colors_to_tracks(trc)
	ref = np.array([[1, 3, 0, 0, 1], [1, 6, 0, 1, 1], [2, 5, 2, 2, 1]], dtype=np.float64)
	np.testing.assert_array_equal(res, ref)

	# Numéro de trajectoire
	trc = pd.DataFrame({"Track": [1, 1, 2], "Plane": [5, 6, 3], "X": [0, 0, 2], "Y": [0, 1, 2], "Integrated Intensity": [7, 3, 5]})
	res = Renderer.add_colors_to_tracks(trc, "Track Number")
	ref = np.array([[1, 5, 0, 0, 1], [1, 6, 0, 1, 1], [2, 3, 2, 2, 2]], dtype=np.float64)
	np.testing.assert_array_equal(res, ref)

	# Plane
	res = Renderer.add_colors_to_tracks(trc, "Plane")
	ref = np.array([[1, 5, 0, 0, 5], [1, 6, 0, 1, 6], [2, 3, 2, 2, 3]], dtype=np.float64)
	np.testing.assert_array_equal(res, ref)

	# Intensity
	res = Renderer.add_colors_to_tracks(trc, "Intensity")
	ref = np.array([[1, 5, 0, 0, 10], [1, 6, 0, 1, 10], [2, 3, 2, 2, 5]], dtype=np.float64)
	np.testing.assert_array_equal(res, ref)

	# Length
	res = Renderer.add_colors_to_tracks(trc, "Length")
	ref = np.array([[1, 5, 0, 0, 1], [1, 6, 0, 1, 1], [2, 3, 2, 2, 0]], dtype=np.float64)
	np.testing.assert_array_equal(res, ref)

	# Duration
	res = Renderer.add_colors_to_tracks(trc, "Duration")
	ref = np.array([[1, 5, 0, 0, 2], [1, 6, 0, 1, 2], [2, 3, 2, 2, 1]], dtype=np.float64)
	np.testing.assert_array_equal(res, ref)

	# Normalization
	res = Renderer.add_colors_to_tracks(trc, "Intensity", max_value=100)
	ref = np.array([[1, 5, 0, 0, 100], [1, 6, 0, 1, 100], [2, 3, 2, 2, 50]], dtype=np.float64)
	np.testing.assert_array_equal(res, ref)

	# Negative and 0
	trc = pd.DataFrame({"Track": [1, 1, 2], "Plane": [5, 6, 3], "X": [0, 0, 2], "Y": [0, 1, 2], "Integrated Intensity": [-1, 0, -1]})
	res = Renderer.add_colors_to_tracks(trc, "Intensity")
	ref = np.array([[1, 5, 0, 0, 1], [1, 6, 0, 1, 1], [2, 3, 2, 2, 1]], dtype=np.float64)
	np.testing.assert_array_equal(res, ref)


##################################################
def test_init_rendering():
	"""Vérifie les valeurs neutres et le masque initial des rendus."""
	for color_mode, init_value in ((0, 0.0), (1, -np.inf), (2, np.inf)):
		img, mask = Renderer.init_rendering(color_mode, 3, 4)

		assert img.shape == (3, 4)
		assert img.dtype == np.float64
		np.testing.assert_array_equal(img, init_value)

		assert mask.shape == img.shape
		assert mask.dtype == bool
		assert not np.any(mask)

	volume, mask = Renderer.init_rendering(0, 3, 4, 2)
	assert volume.shape == (2, 3, 4)
	assert mask.shape == volume.shape
	assert not np.any(mask)


##################################################
def test_prepare_data():
	"""Vérifie la préparation des données de rendu."""
	r = Renderer()
	r.set_size(5, 10, 2)
	loc = np.array([[0, 1, 2, 3, 4, 5, 6],
					[1, 2, 3, 4, 5, 6, 7],
					[10, 10, 4, 5, 6, 7, 8],
					[3, 4, 5, 6, 7, 8, 9],
					[4, 5, 6, 7, 8, 9, 10]], dtype=np.float64)

	# 2D non gaussien
	res = r.prepare_data(loc, False, False)
	ref = np.array([[0, 2, 2, 3, 4, 5, 6],
					[2, 4, 3, 4, 5, 6, 7],
					[6, 8, 5, 6, 7, 8, 9],
					[8, 10, 6, 7, 8, 9, 10]], dtype=np.float64)
	np.testing.assert_array_almost_equal(res, ref)

	# 2D Gaussien
	res = r.prepare_data(loc, False, True)
	ref = np.array([[0, 2, 2, 6, 8, 0.08726646, 6],
					[2, 4, 3, 8, 10, 0.10471976, 7],
					[6, 8, 5, 12, 14, 0.13962634, 9],
					[8, 10, 6, 14, 16, 0.15707963, 10]], dtype=np.float64)
	np.testing.assert_array_almost_equal(res, ref)

	# 3D Non Gaussien
	res = r.prepare_data(loc, True)
	ref = np.array([[0, 2, 2, 3, 4, 5, 6],
					[2, 4, 3, 4, 5, 6, 7],
					[6, 8, 5, 6, 7, 8, 9],
					[8, 10, 6, 7, 8, 9, 10]], dtype=np.float64)
	np.testing.assert_array_almost_equal(res, ref)

	# 3D Gaussien
	res = r.prepare_data(loc, True, True)
	ref = np.array([[0, 2, 2, 3, 8, 10, 0.10471976],
					[2, 4, 3, 4, 10, 12, 0.12217305],
					[6, 8, 5, 6, 14, 16, 0.15707963],
					[8, 10, 6, 7, 16, 18, 0.17453293]], dtype=np.float64)
	np.testing.assert_array_almost_equal(res, ref)


##################################################
def test_draw_line():
	"""Vérifie le tracé d'une ligne et la mise à jour de son masque."""
	# Point unique
	img = np.zeros((5, 5), dtype=np.float64)
	mask = np.zeros(img.shape, dtype=bool)
	Renderer.draw_line(img, mask, 2, 3, 2, 3, 123.0)

	ref = np.zeros((5, 5), dtype=np.float64)
	ref[3, 2] = 123.0
	np.testing.assert_array_equal(img, ref)

	ref_mask = np.zeros((5, 5), dtype=bool)
	ref_mask[3, 2] = True
	np.testing.assert_array_equal(mask, ref_mask)

	# Ligne horizontale
	img.fill(0.0)
	mask.fill(False)
	Renderer.draw_line(img, mask, 1, 2, 4, 2, 10.0)

	ref.fill(0.0)
	ref[2, 1:5] = 10.0
	np.testing.assert_array_equal(img, ref)

	ref_mask.fill(False)
	ref_mask[2, 1:5] = True
	np.testing.assert_array_equal(mask, ref_mask)

	# Ligne verticale
	img.fill(0.0)
	mask.fill(False)
	Renderer.draw_line(img, mask, 3, 1, 3, 4, 20.0)

	ref.fill(0.0)
	ref[1:5, 3] = 20.0
	np.testing.assert_array_equal(img, ref)

	ref_mask.fill(False)
	ref_mask[1:5, 3] = True
	np.testing.assert_array_equal(mask, ref_mask)

	# Ligne diagonale
	img.fill(0.0)
	mask.fill(False)
	Renderer.draw_line(img, mask, 0, 0, 4, 4, 7.0)

	ref.fill(0.0)
	np.fill_diagonal(ref, 7.0)
	np.testing.assert_array_equal(img, ref)
	np.testing.assert_array_equal(mask, np.eye(5, dtype=bool))

	# Ligne partiellement hors de l'image
	img.fill(0.0)
	mask.fill(False)
	Renderer.draw_line(img, mask, -2, -2, 2, 2, 30.0)

	ref.fill(0.0)
	ref[0, 0] = ref[1, 1] = ref[2, 2] = 30.0
	np.testing.assert_array_equal(img, ref)

	ref_mask.fill(False)
	ref_mask[0, 0] = ref_mask[1, 1] = ref_mask[2, 2] = True
	np.testing.assert_array_equal(mask, ref_mask)

	# Ligne entièrement hors de l'image
	img.fill(0.0)
	mask.fill(False)
	Renderer.draw_line(img, mask, -4, -4, -1, -1, 50.0)

	np.testing.assert_array_equal(img, 0.0)
	assert not np.any(mask)

	# Croisement de deux lignes pour les trois modes
	for color_mode, init_value, crossing_value in ((0, 0.0, 30.0), (1, -np.inf, 20.0), (2, np.inf, 10.0)):
		img = np.full((5, 5), init_value, dtype=np.float64)
		mask = np.zeros(img.shape, dtype=bool)

		Renderer.draw_line(img, mask, 0, 2, 4, 2, 10.0, color_mode)
		Renderer.draw_line(img, mask, 2, 0, 2, 4, 20.0, color_mode)

		ref = np.full((5, 5), init_value, dtype=np.float64)
		ref[2, :] = 10.0
		ref[:, 2] = 20.0
		ref[2, 2] = crossing_value
		np.testing.assert_array_equal(img, ref)

		ref_mask = np.zeros((5, 5), dtype=bool)
		ref_mask[2, :] = True
		ref_mask[:, 2] = True
		np.testing.assert_array_equal(mask, ref_mask)


##################################################
def test_draw_gaussian():
	"""Vérifie le rendu gaussien 2D, son masque et ses modes."""
	x, y, color, sx, sy, theta = 2, 2, 100.0, 1.0, 2.0, 0.0
	ref = np.array([[0.65321166, 0.95041736, 1.07696397, 0.95041736, 0.65321166],
					[2.92749158, 4.25947511, 4.82661763, 4.25947511, 2.92749158],
					[4.82661763, 7.02268722, 7.95774715, 7.02268722, 4.82661763],
					[2.92749158, 4.25947511, 4.82661763, 4.25947511, 2.92749158],
					[0.65321166, 0.95041736, 1.07696397, 0.95041736, 0.65321166]])

	# Gaussienne unique avec le mode maximum
	img, mask = Renderer.init_rendering(1, 5, 5)
	res = Renderer.draw_gaussian_2d(img, mask, x, y, color, sx, sy, theta, 1)
	assert res is img
	np.testing.assert_array_almost_equal(res, ref)
	np.testing.assert_array_equal(mask, True)

	# Angle de 90 degrés
	img, mask = Renderer.init_rendering(1, 5, 5)
	Renderer.draw_gaussian_2d(img, mask, x, y, color, sx, sy, np.pi / 2.0, 1)
	np.testing.assert_array_almost_equal(img, ref.transpose())
	np.testing.assert_array_equal(mask, True)

	# Superposition pour les trois modes
	for color_mode, expected in ((0, 1.5 * ref), (1, ref), (2, 0.5 * ref),):
		img, mask = Renderer.init_rendering(color_mode, 5, 5)

		Renderer.draw_gaussian_2d(img, mask, x, y, 100.0, sx, sy, theta, color_mode)
		np.testing.assert_array_equal(mask, True)

		Renderer.draw_gaussian_2d(img, mask, x, y, 50.0, sx, sy, theta, color_mode)
		np.testing.assert_array_almost_equal(img, expected)
		np.testing.assert_array_equal(mask, True)

	# Gaussienne entièrement hors dimensions
	img = np.zeros((5, 5), dtype=np.float64)
	mask = np.zeros(img.shape, dtype=bool)
	Renderer.draw_gaussian_2d(img, mask, -10, -10, color, sx, sy, theta, 0)
	np.testing.assert_array_equal(img, 0.0)
	assert not np.any(mask)

	# Sigma invalide
	img.fill(0.0)
	mask.fill(False)
	Renderer.draw_gaussian_2d(img, mask, x, y, color, -1.0, sy, theta, 0)
	np.testing.assert_array_equal(img, 0.0)
	assert not np.any(mask)


##################################################
def test_draw_gaussian_3d():
	"""Vérifie le rendu gaussien en 3D."""
	x, y, z, color, s = 1.5, 1.5, 1.5, 100, 1
	ref = np.array([[[0.21726327, 0.59058281, 0.59058281],
					 [0.59058281, 1.60537052, 1.60537052],
					 [0.59058281, 1.60537052, 1.60537052]],

					[[0.59058281, 1.60537052, 1.60537052],
					 [1.60537052, 4.36384952, 4.36384952],
					 [1.60537052, 4.36384952, 4.36384952]],

					[[0.59058281, 1.60537052, 1.60537052],
					 [1.60537052, 4.36384952, 4.36384952],
					 [1.60537052, 4.36384952, 4.36384952]]])

	# Gaussienne unique avec le mode maximum
	img, mask = Renderer.init_rendering(1, 3, 3, 3)
	res = Renderer.draw_gaussian_3d(img, mask, x, y, z, color, s, 1)
	assert res is img
	np.testing.assert_array_almost_equal(res, ref)
	np.testing.assert_array_equal(mask, True)

	# Superposition pour les trois modes
	for color_mode, expected in ((0, 1.5 * ref), (1, ref), (2, 0.5 * ref),):
		img, mask = Renderer.init_rendering(color_mode, 3, 3, 3)

		Renderer.draw_gaussian_3d(img, mask, x, y, z, 100.0, s, color_mode)
		np.testing.assert_array_equal(mask, True)

		Renderer.draw_gaussian_3d(img, mask, x, y, z, 50.0, s, color_mode)
		np.testing.assert_array_almost_equal(img, expected)
		np.testing.assert_array_equal(mask, True)

	# Gaussienne entièrement hors dimensions
	img = np.zeros((5, 5, 5), dtype=np.float64)
	mask = np.zeros(img.shape, dtype=bool)
	Renderer.draw_gaussian_3d(img, mask, -10, -10, -10, color, s, 0)
	np.testing.assert_array_equal(img, 0.0)
	assert not np.any(mask)

	# Sigma invalide
	img.fill(0.0)
	mask.fill(False)
	Renderer.draw_gaussian_3d(img, mask, x, y, z, color, -1.0, 0)
	np.testing.assert_array_equal(img, 0.0)
	assert not np.any(mask)


##################################################
def test_localizations():
	"""Vérifie le rendu des localisations."""
	r = Renderer()

	# Not initialized
	loc = np.array([1, 2, 3], dtype=np.float64)
	res = r.localizations(loc)
	assert res.shape == (1, 1) and np.count_nonzero(res) == 0

	# Bad Size
	r.set_size(10, -1, 2)
	res = r.localizations(loc)
	assert res.shape == (1, 20) and np.count_nonzero(res) == 0

	# Invalid Shape
	r.set_size(5, 10, 2)
	res = r.localizations(loc)
	assert res.shape == (20, 10) and np.count_nonzero(res) == 0

	# Points hors limites
	loc = np.array([[10, 2, 5], [2, 10, 6]], dtype=np.float64)
	res = r.localizations(loc)
	assert res.shape == (20, 10) and np.count_nonzero(res) == 0

	# Accumulate
	loc = np.array([[2, 3, 10], [2, 3, 5], [4, 1, 7]], dtype=np.float64)
	res = r.localizations(loc)
	ref = np.zeros((20, 10), dtype=np.uint16)
	ref[6, 4] = 15
	ref[2, 8] = 7
	np.testing.assert_array_equal(res, ref)

	# Max
	loc = np.array([[2, 3, 10], [2, 3, 5], [4, 1, 7]], dtype=np.float64)
	res = r.localizations(loc, 1)
	ref = np.zeros((20, 10), dtype=np.uint16)
	ref[6, 4] = 10
	ref[2, 8] = 7
	np.testing.assert_array_equal(res, ref)

	# Minimum et couleur de fond
	res = r.localizations(loc, color_mode=2, bg_color=42)
	ref = np.full((20, 10), 42, dtype=np.uint16)
	ref[6, 4] = 5
	ref[2, 8] = 7
	np.testing.assert_array_equal(res, ref)

	# Clip
	loc = np.array([[1, 1, 70000], [1, 1, 1000]], dtype=np.float64)
	res = r.localizations(loc)
	assert res[2, 2] == np.iinfo(np.uint16).max


##################################################
def test_localizations_gaussian():
	"""Vérifie le rendu gaussien des localisations."""
	r = Renderer()
	r.set_size(5, 5, 1)

	# Bad size
	loc = np.array([[2, 2, 100]], dtype=np.float64)
	gaussian = {"Intensity": 100, "Fixed Intensity": True, "Shape": 0, "Size": 1}
	res = r.localizations(loc, 0, gaussian=gaussian)
	assert res.shape == (5, 5) and np.count_nonzero(res) == 0

	# Fixed Size and intensity
	loc = np.array([[2, 2, 10000, 1, 2, 0]], dtype=np.float64)
	res = r.localizations(loc, 0, gaussian=gaussian)
	ref = np.array([[0, 1, 2, 1, 0],
					[1, 5, 9, 5, 1],
					[2, 9, 15, 9, 2],
					[1, 5, 9, 5, 1],
					[0, 1, 2, 1, 0]], dtype=np.uint16)
	np.testing.assert_array_equal(res, ref)

	# Fixed Size and not intensity
	gaussian["Fixed Intensity"] = False
	res = r.localizations(loc, 0, gaussian=gaussian)
	np.testing.assert_array_equal(res, ref)

	# Isotrope (Sigma = 1.5 car moyenne des deux)
	gaussian["Fixed Intensity"] = True
	gaussian["Shape"] = 1
	res = r.localizations(loc, 0, gaussian=gaussian)
	ref = np.array([[1, 2, 2, 2, 1],
					[2, 4, 5, 4, 2],
					[2, 5, 7, 5, 2],
					[2, 4, 5, 4, 2],
					[1, 2, 2, 2, 1]], dtype=np.uint16)
	np.testing.assert_array_equal(res, ref)

	# Anisotrope
	gaussian["Shape"] = 2
	res = r.localizations(loc, 0, gaussian=gaussian)
	ref = np.array([[0, 0, 1, 0, 0],
					[2, 4, 4, 4, 2],
					[4, 7, 7, 7, 4],
					[2, 4, 4, 4, 2],
					[0, 0, 1, 0, 0]], dtype=np.uint16)
	np.testing.assert_array_equal(res, ref)

	# Max, résultat identique, car 2 points confondus.
	loc = np.array([[2, 2, 100, 1, 2, 0], [2, 2, 100, 1, 2, 0]], dtype=np.float64)
	res = r.localizations(loc, 1, gaussian=gaussian)
	np.testing.assert_array_equal(res, ref)

	# Accumulate (on vérifie que les flottants ont bien été pris en compte durant le calcul, ce n'est pas un simple * 2 de la valeur entière finale)
	loc = np.array([[2, 2, 100, 1, 2, 0], [2, 2, 100, 1, 2, 0]], dtype=np.float64)
	res = r.localizations(loc, 0, gaussian=gaussian)
	ref = np.array([[1, 1, 2, 1, 1],
					[5, 8, 9, 8, 5],
					[9, 14, 15, 14, 9],
					[5, 8, 9, 8, 5],
					[1, 1, 2, 1, 1]], dtype=np.uint16)
	np.testing.assert_array_equal(res, ref)

	# Un des points est hors cadre
	loc = np.array([[-1, 2, 100, 1, 2, 0], [2, 2, 100, 1, 2, 0]], dtype=np.float64)
	res = r.localizations(loc, 0, gaussian=gaussian)
	ref = np.array([[0, 0, 1, 0, 0],
					[2, 4, 4, 4, 2],
					[4, 7, 7, 7, 4],
					[2, 4, 4, 4, 2],
					[0, 0, 1, 0, 0]], dtype=np.uint16)
	np.testing.assert_array_equal(res, ref)

	# Dimensions flottantes
	loc = np.array([[1.5, 1.5, 100, 1, 2, 0]], dtype=np.float64)
	res = r.localizations(loc, 0, gaussian=gaussian)
	ref = np.array([[1, 2, 2, 1, 1],
					[5, 6, 6, 5, 3],
					[5, 6, 6, 5, 3],
					[1, 2, 2, 1, 1],
					[0, 0, 0, 0, 0]], dtype=np.uint16)
	np.testing.assert_array_equal(res, ref)

	# L'upscale ne doit pas influencer l'intensité maximale
	r.set_size(5, 5, 10)
	res = r.localizations(loc, 0, gaussian=gaussian)
	ref_max = res.max()
	r.set_size(5, 5, 20)
	res = r.localizations(loc, 0, gaussian=gaussian)
	assert ref_max == res.max()


##################################################
def test_tracks():
	"""Vérifie le rendu des trajectoires."""
	r = Renderer()

	# Not initialized
	trc = np.array([1, 2, 3], dtype=np.float64)
	res = r.tracks(trc)
	assert res.shape == (1, 1) and np.count_nonzero(res) == 0

	# Bad Size
	r.set_size(10, -1, 2)
	res = r.tracks(trc)
	assert res.shape == (1, 20) and np.count_nonzero(res) == 0

	# Invalid Shape
	r.set_size(5, 10, 2)
	res = r.tracks(trc)
	assert res.shape == (20, 10) and np.count_nonzero(res) == 0

	# Points hors limites
	trc = np.array([[1, 10, 2, 100], [1, 2, 10, 100], ], dtype=np.float64)
	res = r.tracks(trc)
	assert res.shape == (20, 10) and np.count_nonzero(res) == 0

	# Single point
	trc = np.array([[1, 2, 3, 50], ], dtype=np.float64)
	res = r.tracks(trc)
	ref = np.zeros((20, 10), dtype=np.uint16)
	ref[6, 4] = 50
	np.testing.assert_array_equal(res, ref)

	# Saturation des intensités dans les bornes du type uint16
	trc = np.array([[1, 1, 1, -10], [2, 2, 2, 70000]], dtype=np.float64)
	res = r.tracks(trc)
	assert res[2, 2] == 0
	assert res[4, 4] == np.iinfo(np.uint16).max

	# Croisement de trajectoires pour les trois modes
	trc = np.array([[1, 1, 3, 10], [1, 4, 3, 10], [2, 3, 1, 20], [2, 3, 4, 20]], dtype=np.float64)
	for color_mode, crossing_value in ((0, 30), (1, 20), (2, 10)):
		res = r.tracks(trc, color_mode=color_mode, bg_color=42)
		ref = np.full((20, 10), 42, dtype=np.uint16)
		ref[6, 2:9] = 10
		ref[2:9, 6] = 20
		ref[6, 6] = crossing_value
		np.testing.assert_array_equal(res, ref)


##################################################
def test_z_stack():
	"""Vérifie le rendu d'une pile Z."""
	r = Renderer()

	# Not initialized
	loc = np.array([1, 2, 3], dtype=np.float64)
	res = r.z_stack(loc)
	assert res.shape == (1, 1, 1) and np.count_nonzero(res) == 0

	# Bad Size
	r.set_size(10, -1, 2)
	res = r.z_stack(loc)
	assert res.shape == (1, 1, 20) and np.count_nonzero(res) == 0

	# Invalid Shape
	r.set_size(5, 10, 2)
	res = r.z_stack(loc)
	assert res.shape == (1, 20, 10) and np.count_nonzero(res) == 0

	# Points hors limites
	loc = np.array([[10, 2, 0, 5], [2, 10, 0, 6], [-1, 2, 0, 7], [2, -1, 0, 8]], dtype=np.float64)
	res = r.z_stack(loc)
	assert res.shape == (1, 20, 10) and np.count_nonzero(res) == 0

	# Z uniforme à 0 + accumulation
	loc = np.array([[2, 3, 0, 10], [2, 3, 0, 5], [4, 1, 0, 7]], dtype=np.float64)
	res = r.z_stack(loc, color_mode=0, z_step=20)
	ref = np.zeros((1, 20, 10), dtype=np.uint16)
	ref[0, 6, 4] = 15
	ref[0, 2, 8] = 7
	np.testing.assert_array_equal(res, ref)

	# Z uniforme à 0 + max
	res = r.z_stack(loc, color_mode=1, z_step=20)
	ref = np.zeros((1, 20, 10), dtype=np.uint16)
	ref[0, 6, 4] = 10
	ref[0, 2, 8] = 7
	np.testing.assert_array_equal(res, ref)

	# Z uniforme à 0 + minimum et couleur de fond
	res = r.z_stack(loc, color_mode=2, z_step=20, bg_color=42)
	ref = np.full((1, 20, 10), 42, dtype=np.uint16)
	ref[0, 6, 4] = 5
	ref[0, 2, 8] = 7
	np.testing.assert_array_equal(res, ref)

	# Z dans [-40 ; +40]
	loc = np.array([
			[1, 1, -40, 10],  # Plan 0
			[2, 1, -20, 20],  # Plan 1
			[3, 1, +00, 30],  # Plan 2
			[4, 1, +20, 40],  # Plan 3
			[1, 2, +40, 50],  # Plan 4
			], dtype=np.float64)

	res = r.z_stack(loc, color_mode=0, z_step=20)
	ref = np.zeros((5, 20, 10), dtype=np.uint16)
	ref[0, 2, 2] = 10
	ref[1, 2, 4] = 20
	ref[2, 2, 6] = 30
	ref[3, 2, 8] = 40
	ref[4, 4, 2] = 50
	np.testing.assert_array_equal(res, ref)

	# Points hors dimensions + points valides
	loc = np.array([[1, 1, 0, 10], [100, 1, 0, 20], [1, 100, 0, 30], [-1, 1, 0, 40], [1, -1, 0, 50]], dtype=np.float64)
	res = r.z_stack(loc, color_mode=0, z_step=20)
	ref = np.zeros((1, 20, 10), dtype=np.uint16)
	ref[0, 2, 2] = 10
	np.testing.assert_array_equal(res, ref)

	# Clip uint16
	loc = np.array([[1, 1, 0, 70000], [1, 1, 0, 1000], ], dtype=np.float64)
	res = r.z_stack(loc, color_mode=0, z_step=20)
	assert res[0, 2, 2] == np.iinfo(np.uint16).max


##################################################
def test_z_stack_gaussian():
	"""Vérifie le rendu gaussien d'une pile Z."""
	r = Renderer()
	r.set_size(5, 5, 1)

	# Bad size
	loc = np.array([[2, 2, 0, 100, 1]], dtype=np.float64)
	gaussian = {"Intensity": 100, "Fixed Intensity": True, "Shape": 0, "Size": 1}
	res = r.z_stack(loc, 0, 20, gaussian=gaussian)
	assert res.shape == (1, 5, 5) and np.count_nonzero(res) == 0

	# Fixed Size and intensity
	loc = np.array([[2, 2, 0, 10000, 1, 2, 0]], dtype=np.float64)
	res = r.z_stack(loc, 0, 20, gaussian=gaussian)
	ref = np.array([[[0, 0, 0, 0, 0],
					 [0, 2, 3, 2, 0],
					 [0, 3, 6, 3, 0],
					 [0, 2, 3, 2, 0],
					 [0, 0, 0, 0, 0]]], dtype=np.uint16)
	np.testing.assert_array_equal(res, ref)

	# 2 point in nearly same Z
	loc = np.array([[1, 1, 0, 10000, 1, 2, 0], [3, 3, 9, 10000, 1, 2, 0]], dtype=np.float64)
	res = r.z_stack(loc, 0, 20, gaussian=gaussian)
	ref = np.array([[[2, 3, 2, 0, 0],
					 [3, 6, 4, 1, 0],
					 [2, 4, 4, 4, 2],
					 [0, 1, 4, 5, 3],
					 [0, 0, 2, 3, 2]]], dtype=np.uint16)
	np.testing.assert_array_equal(res, ref)

	# 2 point in nearly same Z and Max color mode
	loc = np.array([[1, 1, 0, 10000, 1, 2, 0], [3, 3, 9, 10000, 1, 2, 0]], dtype=np.float64)
	res = r.z_stack(loc, 1, 20, gaussian=gaussian)
	ref = np.array([[[2, 3, 2, 0, 0],
					 [3, 6, 3, 0, 0],
					 [2, 3, 2, 3, 2],
					 [0, 0, 3, 5, 3],
					 [0, 0, 2, 3, 2]]], dtype=np.uint16)
	np.testing.assert_array_equal(res, ref)

	# 2 point in different Z (and spaced)
	loc = np.array([[1, 1, 0, 10000, 1, 2, 0], [3, 3, 60, 10000, 1, 2, 0]], dtype=np.float64)
	res = r.z_stack(loc, 0, 20, gaussian=gaussian)
	patch_low = np.array([[1, 2, 1],
						  [2, 3, 2],
						  [1, 2, 1]], dtype=np.uint16)

	patch_high = np.array([[2, 3, 2],
						   [3, 6, 3],
						   [2, 3, 2]], dtype=np.uint16)
	ref = np.zeros((4, 5, 5), dtype=np.uint16)

	# Point 1 : centré en (y=1, x=1), déborde sur les plans 0 et 1.
	ref[0, 0:3, 0:3] += patch_high
	ref[1, 0:3, 0:3] += patch_low

	# Point 2 : centré en (y=3, x=3), déborde sur les plans 2 et 3.
	ref[2, 2:5, 2:5] += patch_low
	ref[3, 2:5, 2:5] += patch_high
	np.testing.assert_array_equal(res, ref)

	# L'upscale ne doit pas influencer l'intensité maximale
	r.set_size(5, 5, 10)
	res = r.z_stack(loc, 0, 20, gaussian=gaussian)
	ref_max = res.max()
	r.set_size(5, 5, 20)
	res = r.z_stack(loc, 0, 20, gaussian=gaussian)
	assert ref_max == res.max()


##################################################
def test_rotation():
	"""Vérifie le rendu d'une rotation 3D."""
	r = Renderer()

	# Not initialized
	loc = np.array([1, 2, 3], dtype=np.float64)
	res = r.rotation_3d(loc)
	assert res.shape == (1, 1, 1) and np.count_nonzero(res) == 0

	# Bad Size
	r.set_size(10, -1, 2)
	res = r.rotation_3d(loc)
	assert res.shape == (1, 1, 20) and np.count_nonzero(res) == 0

	# Invalid Shape
	r.set_size(5, 5, 2)
	res = r.rotation_3d(loc)
	assert res.shape == (1, 10, 10) and np.count_nonzero(res) == 0

	# Points hors limites
	loc = np.array([[10, 2, 0, 5], [2, 10, 0, 6], [-1, 2, 0, 7], [2, -1, 0, 8]], dtype=np.float64)
	res = r.rotation_3d(loc)
	assert res.shape == (1, 10, 10) and np.count_nonzero(res) == 0

	# Z uniforme à 0.
	loc = np.array([[2, 3, 0, 10], [2, 3, 0, 5], [3, 2, 0, 7]], dtype=np.float64)

	# Z uniforme à 0 + accumulation rotation sur X, X ne change pas, mais Y s'inverse autour de l'axe central (7.5)
	res = r.rotation_3d(loc, color_mode=0, z_step=20, frames=2, axis=0)
	ref = np.zeros((2, 16, 16), dtype=np.uint16)
	ref[0, 9, 7], ref[0, 7, 9] = 15, 7  # 0°
	ref[1, 6, 7], ref[1, 8, 9] = 15, 7  # 180°
	np.testing.assert_array_equal(res, ref)

	# Z uniforme à 0 + accumulation rotation sur Y, Y ne change pas, mais X s'inverse autour de l'axe central (7.5)
	res = r.rotation_3d(loc, color_mode=0, z_step=20, frames=2, axis=1)
	ref = np.zeros((2, 16, 16), dtype=np.uint16)
	ref[0, 9, 7], ref[0, 7, 9] = 15, 7  # 0°
	ref[1, 9, 8], ref[1, 7, 6] = 15, 7  # 180°
	np.testing.assert_array_equal(res, ref)

	# Z uniforme à 0 + max rotation sur Z, Z ne change pas, mais X et Y se transposent s'inverse autour de l'axe central (7.5, 7.5)
	res = r.rotation_3d(loc, color_mode=1, z_step=20, frames=2, axis=2)
	ref = np.zeros((2, 16, 16), dtype=np.uint16)
	ref[0, 9, 7], ref[0, 7, 9] = 10, 7  # 0°
	ref[1, 6, 8], ref[1, 8, 6] = 10, 7  # 180°
	np.testing.assert_array_equal(res, ref)

	# Minimum avec une couleur de fond non nulle
	res = r.rotation_3d(loc, color_mode=2, z_step=20, frames=2, axis=2, bg_color=42)
	ref = np.full((2, 16, 16), 42, dtype=np.uint16)
	ref[0, 9, 7], ref[0, 7, 9] = 5, 7
	ref[1, 6, 8], ref[1, 8, 6] = 5, 7
	np.testing.assert_array_equal(res, ref)

	# Z non uniforme [-20 ; +20], aucun changement pour 0 et 180° masi ajout de 90 et 270 Y inchangé, mais X autour du centre évolue
	# Attention, l'arrondi python dans le cas de X.5 va arrondir au nombre pair le plus proche
	# Cela donne l'impression de l'axe central à 7 sur les angles 90 et 270.
	# np.round([6.5, 7.5, 8.5, 9.5]) = array([ 6.,  8.,  8., 10.])
	loc = np.array([[2, 3, -20, 10], [2, 3, -20, 5], [3, 2, 20, 7]], dtype=np.float64)
	res = r.rotation_3d(loc, color_mode=0, z_step=20, frames=4, axis=1)
	ref = np.zeros((4, 16, 16), dtype=np.uint16)
	ref[0, 9, 7], ref[0, 7, 9] = 15, 7  # 0°
	ref[2, 9, 8], ref[2, 7, 6] = 15, 7  # 180°
	ref[1, 9, 6], ref[1, 7, 8] = 15, 7  # 90°
	ref[3, 9, 8], ref[3, 7, 6] = 15, 7  # 270°
	np.testing.assert_array_equal(res, ref)


##################################################
def test_rotation_gaussian():
	"""Vérifie le rendu gaussien d'une rotation 3D."""
	r = Renderer()
	r.set_size(3, 3, 2)
	loc = np.array([[0, 0, 0, 1000, 1, 1, 0]], dtype=np.float64)
	gaussian = {"Intensity": 100, "Fixed Intensity": True, "Shape": 0, "Size": 1}
	res = r.rotation_3d(loc, color_mode=0, z_step=20, frames=2, axis=1, gaussian=gaussian)
	ref = np.zeros((2, 11, 11), dtype=np.uint16)
	patch = np.array([[3, 5, 7, 7, 5, 3, 1, 0],
					  [5, 9, 11, 11, 9, 5, 2, 0],
					  [7, 11, 14, 14, 11, 7, 3, 1],
					  [7, 11, 14, 14, 11, 7, 3, 1],
					  [5, 9, 11, 11, 9, 5, 2, 0],
					  [3, 5, 7, 7, 5, 3, 1, 0],
					  [1, 2, 3, 3, 2, 1, 0, 0],
					  [0, 0, 1, 1, 0, 0, 0, 0]], dtype=np.uint16)
	ref[0, 0:8, 0:8] = patch
	ref[1, 0:8, 3:11] = np.fliplr(patch)
	np.testing.assert_array_equal(res, ref)

	# L'upscale ne doit pas influencer l'intensité maximale
	r.set_size(3, 3, 10)
	res = r.rotation_3d(loc, color_mode=0, z_step=20, frames=1, axis=1, gaussian=gaussian)
	ref_max = res.max()
	r.set_size(3, 3, 20)
	res = r.rotation_3d(loc, color_mode=0, z_step=20, frames=1, axis=1, gaussian=gaussian)
	assert ref_max == res.max()

	# Bad size
	r.set_size(3, 3, 2)
	loc = np.array([[0, 0, 0, 1000, 1, 1]], dtype=np.float64)
	res = r.rotation_3d(loc, color_mode=0, z_step=20, frames=2, axis=1, gaussian=gaussian)
	assert res.shape == (1, 6, 6) and np.count_nonzero(res) == 0


##################################################
def test_renderer_atom():
	"""Vérifie le rendu d'une localisation isolée."""
	r = Renderer()
	r.set_size(700, 500, 2)
	loc = pd.read_csv(INPUT_DIR / "atoms_sphere_motion.csv").to_numpy()
	loc[:, 0] += 3.5  # Les positions vont de -3 à +3
	loc[:, 1] += 2.5  # Les positions vont de -2 à +2
	loc[:, 0:3] *= 100  # Passsage en gros à des pixel
	loc = np.hstack((loc, np.zeros((loc.shape[0], 3))))  # Ajout de SigmaX,SigmaY et Theta
	loc[:, 4] = 1  # Sigma X
	loc[:, 5] = 2  # Sigma Y
	gaussian = {"Intensity": 1000, "Fixed Intensity": True, "Shape": 2, "Size": 1}

	loc_2d = np.delete(loc, 2, axis=1)
	res = r.localizations(loc_2d)
	assert np.count_nonzero(res) != 0
	FileIO.save_png(res, OUTPUT_DIR / "atoms_sphere_motion_loc.png")

	res = r.localizations(loc_2d, gaussian=gaussian)
	assert np.count_nonzero(res) != 0
	FileIO.save_png(res, OUTPUT_DIR / "atoms_sphere_motion_loc_gaussian.png")

	res = r.z_stack(loc)
	assert np.count_nonzero(res) != 0
	FileIO.save_tif(res, OUTPUT_DIR / "atoms_sphere_motion_Zstack.tif")

	res = r.z_stack(loc, gaussian=gaussian)
	assert np.count_nonzero(res) != 0
	FileIO.save_tif(res, OUTPUT_DIR / "atoms_sphere_motion_Zstack_gaussian.tif")

	res = r.rotation_3d(loc, z_step=1)
	assert np.count_nonzero(res) != 0
	FileIO.save_tif(res, OUTPUT_DIR / "atoms_sphere_motion_3D.tif")

	res = r.rotation_3d(loc, z_step=1, gaussian=gaussian)
	assert np.count_nonzero(res) != 0
	FileIO.save_tif(res, OUTPUT_DIR / "atoms_sphere_motion_3D_gaussian.tif")
