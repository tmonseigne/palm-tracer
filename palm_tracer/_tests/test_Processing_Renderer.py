"""Teste la production des rendus haute résolution."""

import tifffile
from PIL import Image

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
	img = np.array([[-1, 0, 1.9, 65535, 65536, 65537, 131073]], dtype=float)
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
	ref = np.array([[1, 3, 10, 1], [2, 4, 20, 1]], dtype=float)
	np.testing.assert_array_equal(res, ref)

	# Selected columns
	res = Renderer.add_colors_to_localizations(loc, "Intensity")
	ref = np.array([[1, 3, 10, 10], [2, 4, 20, 20]], dtype=float)
	np.testing.assert_array_equal(res, ref)

	# With negatives values
	loc = pd.DataFrame({"X": [1, 2], "Y": [3, 4], "Intensity": [-2, 3]})
	res = Renderer.add_colors_to_localizations(loc, "Intensity")
	ref = np.array([[1, 3, -2, 0], [2, 4, 3, 5]], dtype=float)
	np.testing.assert_array_equal(res, ref)

	# With normalization
	loc = pd.DataFrame({"X": [1, 2], "Y": [3, 4], "Intensity": [2, 4]})
	res = Renderer.add_colors_to_localizations(loc, "Intensity", max_value=100)
	ref = np.array([[1, 3, 2, 50], [2, 4, 4, 100], ], dtype=float)
	np.testing.assert_allclose(res, ref)

	# With 0 in colors
	loc = pd.DataFrame({"X": [1, 2], "Y": [3, 4], "Intensity": [0, 0]})
	res = Renderer.add_colors_to_localizations(loc, "Intensity")
	ref = np.array([[1, 3, 0, 1], [2, 4, 0, 1]], dtype=float)
	np.testing.assert_array_equal(res, ref)


##################################################
def test_get_tracks_colors():
	# DataFrame vide
	"""Vérifie la génération des couleurs des trajectoires."""
	trc = pd.DataFrame(columns=["Track", "Plane", "X", "Y", "Integrated Intensity"])
	res = Renderer.add_colors_to_tracks(trc, "Track ID")
	assert res.shape == (0, 5)

	# No Column selected (and sorting)
	trc = pd.DataFrame({"Track": [2, 1, 1], "Plane": [5, 6, 3], "X": [2, 0, 0], "Y": [2, 1, 0], "Integrated Intensity": [7, 6, 5]})
	res = Renderer.add_colors_to_tracks(trc)
	ref = np.array([[1, 3, 0, 0, 1], [1, 6, 0, 1, 1], [2, 5, 2, 2, 1]], dtype=float)
	np.testing.assert_array_equal(res, ref)

	# Numéro de trajectoire
	trc = pd.DataFrame({"Track": [1, 1, 2], "Plane": [5, 6, 3], "X": [0, 0, 2], "Y": [0, 1, 2], "Integrated Intensity": [7, 3, 5]})
	res = Renderer.add_colors_to_tracks(trc, "Track ID")
	ref = np.array([[1, 5, 0, 0, 1], [1, 6, 0, 1, 1], [2, 3, 2, 2, 2]], dtype=float)
	np.testing.assert_array_equal(res, ref)

	# Numéro de plan
	res = Renderer.add_colors_to_tracks(trc, "Plane Number")
	ref = np.array([[1, 5, 0, 0, 5], [1, 6, 0, 1, 6], [2, 3, 2, 2, 3]], dtype=float)
	np.testing.assert_array_equal(res, ref)

	# Intensité de la trajectoire
	res = Renderer.add_colors_to_tracks(trc, "Track Intensity")
	ref = np.array([[1, 5, 0, 0, 10], [1, 6, 0, 1, 10], [2, 3, 2, 2, 5]], dtype=float)
	np.testing.assert_array_equal(res, ref)

	# Longueur de la trajectoire
	res = Renderer.add_colors_to_tracks(trc, "Track Length")
	ref = np.array([[1, 5, 0, 0, 1], [1, 6, 0, 1, 1], [2, 3, 2, 2, 0]], dtype=float)
	np.testing.assert_array_equal(res, ref)

	# Numéro de plan relatif
	res = Renderer.add_colors_to_tracks(trc, "Relative Plane")
	ref = np.array([[1, 5, 0, 0, 1], [1, 6, 0, 1, 2], [2, 3, 2, 2, 1]], dtype=float)
	np.testing.assert_array_equal(res, ref)

	# Durée totale de la trajectoire
	res = Renderer.add_colors_to_tracks(trc, "Track Duration")
	ref = np.array([[1, 5, 0, 0, 2], [1, 6, 0, 1, 2], [2, 3, 2, 2, 1]], dtype=float)
	np.testing.assert_array_equal(res, ref)

	# Normalization
	res = Renderer.add_colors_to_tracks(trc, "Track Intensity", max_value=100)
	ref = np.array([[1, 5, 0, 0, 100], [1, 6, 0, 1, 100], [2, 3, 2, 2, 50]], dtype=float)
	np.testing.assert_array_equal(res, ref)

	# Negative and 0
	trc = pd.DataFrame({"Track": [1, 1, 2], "Plane": [5, 6, 3], "X": [0, 0, 2], "Y": [0, 1, 2], "Integrated Intensity": [-1, 0, -1]})
	res = Renderer.add_colors_to_tracks(trc, "Track Intensity")
	ref = np.array([[1, 5, 0, 0, 1], [1, 6, 0, 1, 1], [2, 3, 2, 2, 1]], dtype=float)
	np.testing.assert_array_equal(res, ref)


##################################################
def test_init_rendering():
	"""Vérifie les valeurs neutres et le masque initial des rendus."""
	for color_mode, init_value in ((0, 0.0), (1, -np.inf), (2, np.inf)):
		img, mask = Renderer.init_rendering(color_mode, 3, 4)

		assert img.shape == (3, 4)
		assert img.dtype == float
		np.testing.assert_array_equal(img, init_value)

		assert mask.shape == img.shape
		assert mask.dtype == bool
		assert not np.any(mask)

	volume, mask = Renderer.init_rendering(0, 3, 4, 2)
	assert volume.shape == (2, 3, 4)
	assert mask.shape == volume.shape
	assert not np.any(mask)


##################################################
def test_prepare_localizations():
	"""Vérifie la préparation des localisations de rendu."""
	r = Renderer()
	r.set_size(5, 10, 2)

	loc = np.array([[0, 1, 2, 3, 4, 5, 6],
					[1, 2, 3, 4, 5, 6, 7],
					[10, 10, 4, 5, 6, 7, 8],
					[3, 4, 5, 6, 7, 8, 9],
					[4, 5, 6, 7, 8, 9, 10]], dtype=float)

	# L'intensité reste inchangée avec r² / Intensity = 4 / 4 = 1.
	gaussian = {"Shape": 2, "Fixed Intensity": False, "Intensity": 4, }

	# Localisations 2D non gaussiennes.
	res = r.prepare_localizations(loc, False)
	ref = np.array([[0, 2, 2, 3, 4, 5, 6],
					[2, 4, 3, 4, 5, 6, 7],
					[6, 8, 5, 6, 7, 8, 9],
					[8, 10, 6, 7, 8, 9, 10]], dtype=float)
	np.testing.assert_array_almost_equal(res, ref)

	# Localisations 2D gaussiennes.
	res = r.prepare_localizations(loc, False, gaussian)
	ref = np.array([[0, 2, 2, 6, 8, 0.08726646, 6],
					[2, 4, 3, 8, 10, 0.10471976, 7],
					[6, 8, 5, 12, 14, 0.13962634, 9],
					[8, 10, 6, 14, 16, 0.15707963, 10]], dtype=float)
	np.testing.assert_array_almost_equal(res, ref)

	# Localisations 3D non gaussiennes.
	res = r.prepare_localizations(loc, True)
	ref = np.array([[0, 2, 2, 3, 4, 5, 6],
					[2, 4, 3, 4, 5, 6, 7],
					[6, 8, 5, 6, 7, 8, 9],
					[8, 10, 6, 7, 8, 9, 10]], dtype=float)
	np.testing.assert_array_almost_equal(res, ref)

	# Localisations 3D gaussiennes.
	res = r.prepare_localizations(loc, True, gaussian)
	ref = np.array([[0, 2, 2, 3, 8, 10, 0.10471976],
					[2, 4, 3, 4, 10, 12, 0.12217305],
					[6, 8, 5, 6, 14, 16, 0.15707963],
					[8, 10, 6, 7, 16, 18, 0.17453293]], dtype=float)
	np.testing.assert_array_almost_equal(res, ref)


##################################################
def test_prepare_tracks():
	"""Vérifie les plans, les arrondis, le filtrage et les tranches de trajectoires sans copie."""
	r = Renderer()
	r.set_size(5, 10, 2)
	tracks = np.array([[1, 3, 1.2, 2.6, 10.5], [1, 7, 4.0, 3.0, 20.5],
					   [2, 1, -1.0, 2.0, 30.5], [2, 2, 3.0, 11.0, 40.5],
					   [3, 4, 4.9, 1.0, 50.5], [3, 8, 0.0, 0.0, 60.5],
					   [4, 2, 2.0, 1.0, 70.5], [4, 5, 3.0, 2.0, 80.5]], dtype=float)
	original = tracks.copy()
	track_ids, coords, colors, bounds = r.prepare_tracks(tracks)
	np.testing.assert_array_equal(track_ids, [1, 3, 4])
	np.testing.assert_array_equal(coords, [[3, 2, 5], [7, 8, 6], [8, 0, 0], [2, 4, 2], [5, 6, 4]])
	np.testing.assert_array_equal(colors, [10.5, 20.5, 60.5, 70.5, 80.5])
	np.testing.assert_array_equal(bounds, [0, 2, 3, 5])
	np.testing.assert_array_equal(tracks, original)
	assert track_ids.dtype == int
	assert coords.dtype == int and bounds.dtype == int
	assert np.issubdtype(colors.dtype, float)
	assert np.shares_memory(coords[bounds[0]:bounds[1]], coords)
	assert not np.shares_memory(coords, tracks)
	assert not np.shares_memory(colors, tracks)


##################################################
def test_prepare_tracks_empty():
	"""Vérifie les entrées vides, entièrement filtrées et de forme invalide."""
	r = Renderer()
	r.set_size(5, 10, 2)
	for data in (np.empty((0, 5)), np.array([[1, 3, -1, 0, 10]])):
		track_ids, coords, colors, bounds = r.prepare_tracks(data)
		assert track_ids.shape == (0,) and coords.shape == (0, 3) and colors.shape == (0,)
		np.testing.assert_array_equal(bounds, [0])


##################################################
def test_draw_line():
	"""Vérifie le tracé d'une ligne et la mise à jour de son masque."""
	# Point unique
	img = np.zeros((5, 5), dtype=float)
	mask = np.zeros(img.shape, dtype=bool)
	Renderer.draw_line(img, mask, 2, 3, 2, 3, 123.0)

	ref = np.zeros((5, 5), dtype=float)
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
		img = np.full((5, 5), init_value, dtype=float)
		mask = np.zeros(img.shape, dtype=bool)

		Renderer.draw_line(img, mask, 0, 2, 4, 2, 10.0, color_mode)
		Renderer.draw_line(img, mask, 2, 0, 2, 4, 20.0, color_mode)

		ref = np.full((5, 5), init_value, dtype=float)
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
	img = np.zeros((5, 5), dtype=float)
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
	img = np.zeros((5, 5, 5), dtype=float)
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
	loc = np.array([1, 2, 3], dtype=float)
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
	loc = np.array([[10, 2, 5], [2, 10, 6]], dtype=float)
	res = r.localizations(loc)
	assert res.shape == (20, 10) and np.count_nonzero(res) == 0

	# Accumulate
	loc = np.array([[2, 3, 10], [2, 3, 5], [4, 1, 7]], dtype=float)
	res = r.localizations(loc)
	ref = np.zeros((20, 10), dtype=np.uint16)
	ref[6, 4] = 15
	ref[2, 8] = 7
	np.testing.assert_array_equal(res, ref)

	# Max
	loc = np.array([[2, 3, 10], [2, 3, 5], [4, 1, 7]], dtype=float)
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
	loc = np.array([[1, 1, 70000], [1, 1, 1000]], dtype=float)
	res = r.localizations(loc)
	assert res[2, 2] == np.iinfo(np.uint16).max


##################################################
def test_localizations_gaussian():
	"""Vérifie le rendu gaussien des localisations."""
	r = Renderer()
	r.set_size(5, 5, 1)

	# Bad size
	loc = np.array([[2, 2, 100]], dtype=float)
	gaussian = {"Intensity": 100, "Fixed Intensity": True, "Shape": 0, "Size": 1}
	res = r.localizations(loc, 0, gaussian=gaussian)
	assert res.shape == (5, 5) and np.count_nonzero(res) == 0

	# Fixed Size and intensity
	loc = np.array([[2, 2, 10000, 1, 2, 0]], dtype=float)
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
	loc = np.array([[2, 2, 100, 1, 2, 0], [2, 2, 100, 1, 2, 0]], dtype=float)
	res = r.localizations(loc, 1, gaussian=gaussian)
	np.testing.assert_array_equal(res, ref)

	# Accumulate (on vérifie que les flottants ont bien été pris en compte durant le calcul, ce n'est pas un simple * 2 de la valeur entière finale)
	loc = np.array([[2, 2, 100, 1, 2, 0], [2, 2, 100, 1, 2, 0]], dtype=float)
	res = r.localizations(loc, 0, gaussian=gaussian)
	ref = np.array([[1, 1, 2, 1, 1],
					[5, 8, 9, 8, 5],
					[9, 14, 15, 14, 9],
					[5, 8, 9, 8, 5],
					[1, 1, 2, 1, 1]], dtype=np.uint16)
	np.testing.assert_array_equal(res, ref)

	# Un des points est hors cadre
	loc = np.array([[-1, 2, 100, 1, 2, 0], [2, 2, 100, 1, 2, 0]], dtype=float)
	res = r.localizations(loc, 0, gaussian=gaussian)
	ref = np.array([[0, 0, 1, 0, 0],
					[2, 4, 4, 4, 2],
					[4, 7, 7, 7, 4],
					[2, 4, 4, 4, 2],
					[0, 0, 1, 0, 0]], dtype=np.uint16)
	np.testing.assert_array_equal(res, ref)

	# Dimensions flottantes
	loc = np.array([[1.5, 1.5, 100, 1, 2, 0]], dtype=float)
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
	trc = np.array([1, 2, 3], dtype=float)
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
	trc = np.array([[1, 1, 10, 2, 100], [1, 2, 2, 10, 100], ], dtype=float)
	res = r.tracks(trc)
	assert res.shape == (20, 10) and np.count_nonzero(res) == 0

	# Single point
	trc = np.array([[1, 7, 2, 3, 50], ], dtype=float)
	res = r.tracks(trc)
	ref = np.zeros((20, 10), dtype=np.uint16)
	ref[6, 4] = 50
	np.testing.assert_array_equal(res, ref)

	# Saturation des intensités dans les bornes du type uint16
	trc = np.array([[1, 1, 1, 1, -10], [2, 3, 2, 2, 70000]], dtype=float)
	res = r.tracks(trc)
	assert res[2, 2] == 0
	assert res[4, 4] == np.iinfo(np.uint16).max

	# Croisement de trajectoires pour les trois modes
	trc = np.array([[1, 1, 1, 3, 10], [1, 4, 4, 3, 10], [2, 2, 3, 1, 20], [2, 8, 3, 4, 20]], dtype=float)
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
	loc = np.array([1, 2, 3], dtype=float)
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
	loc = np.array([[10, 2, 0, 5], [2, 10, 0, 6], [-1, 2, 0, 7], [2, -1, 0, 8]], dtype=float)
	res = r.z_stack(loc)
	assert res.shape == (1, 20, 10) and np.count_nonzero(res) == 0

	# Z uniforme à 0 + accumulation
	loc = np.array([[2, 3, 0, 10], [2, 3, 0, 5], [4, 1, 0, 7]], dtype=float)
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
			], dtype=float)

	res = r.z_stack(loc, color_mode=0, z_step=20)
	ref = np.zeros((5, 20, 10), dtype=np.uint16)
	ref[0, 2, 2] = 10
	ref[1, 2, 4] = 20
	ref[2, 2, 6] = 30
	ref[3, 2, 8] = 40
	ref[4, 4, 2] = 50
	np.testing.assert_array_equal(res, ref)

	# Points hors dimensions + points valides
	loc = np.array([[1, 1, 0, 10], [100, 1, 0, 20], [1, 100, 0, 30], [-1, 1, 0, 40], [1, -1, 0, 50]], dtype=float)
	res = r.z_stack(loc, color_mode=0, z_step=20)
	ref = np.zeros((1, 20, 10), dtype=np.uint16)
	ref[0, 2, 2] = 10
	np.testing.assert_array_equal(res, ref)

	# Clip uint16
	loc = np.array([[1, 1, 0, 70000], [1, 1, 0, 1000], ], dtype=float)
	res = r.z_stack(loc, color_mode=0, z_step=20)
	assert res[0, 2, 2] == np.iinfo(np.uint16).max


##################################################
def test_z_stack_gaussian():
	"""Vérifie le rendu gaussien d'une pile Z."""
	r = Renderer()
	r.set_size(5, 5, 1)

	# Bad size
	loc = np.array([[2, 2, 0, 100, 1]], dtype=float)
	gaussian = {"Intensity": 100, "Fixed Intensity": True, "Shape": 0, "Size": 1}
	res = r.z_stack(loc, 0, 20, gaussian=gaussian)
	assert res.shape == (1, 5, 5) and np.count_nonzero(res) == 0

	# Fixed Size and intensity
	loc = np.array([[2, 2, 0, 10000, 1, 2, 0]], dtype=float)
	res = r.z_stack(loc, 0, 20, gaussian=gaussian)
	ref = np.array([[[0, 0, 0, 0, 0],
					 [0, 2, 3, 2, 0],
					 [0, 3, 6, 3, 0],
					 [0, 2, 3, 2, 0],
					 [0, 0, 0, 0, 0]]], dtype=np.uint16)
	np.testing.assert_array_equal(res, ref)

	# 2 point in nearly same Z
	loc = np.array([[1, 1, 0, 10000, 1, 2, 0], [3, 3, 9, 10000, 1, 2, 0]], dtype=float)
	res = r.z_stack(loc, 0, 20, gaussian=gaussian)
	ref = np.array([[[2, 3, 2, 0, 0],
					 [3, 6, 4, 1, 0],
					 [2, 4, 4, 4, 2],
					 [0, 1, 4, 5, 3],
					 [0, 0, 2, 3, 2]]], dtype=np.uint16)
	np.testing.assert_array_equal(res, ref)

	# 2 point in nearly same Z and Max color mode
	loc = np.array([[1, 1, 0, 10000, 1, 2, 0], [3, 3, 9, 10000, 1, 2, 0]], dtype=float)
	res = r.z_stack(loc, 1, 20, gaussian=gaussian)
	ref = np.array([[[2, 3, 2, 0, 0],
					 [3, 6, 3, 0, 0],
					 [2, 3, 2, 3, 2],
					 [0, 0, 3, 5, 3],
					 [0, 0, 2, 3, 2]]], dtype=np.uint16)
	np.testing.assert_array_equal(res, ref)

	# 2 point in different Z (and spaced)
	loc = np.array([[1, 1, 0, 10000, 1, 2, 0], [3, 3, 60, 10000, 1, 2, 0]], dtype=float)
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
	loc = np.array([1, 2, 3], dtype=float)
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
	loc = np.array([[10, 2, 0, 5], [2, 10, 0, 6], [-1, 2, 0, 7], [2, -1, 0, 8]], dtype=float)
	res = r.rotation_3d(loc)
	assert res.shape == (1, 10, 10) and np.count_nonzero(res) == 0

	# Z uniforme à 0.
	loc = np.array([[2, 3, 0, 10], [2, 3, 0, 5], [3, 2, 0, 7]], dtype=float)

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
	loc = np.array([[2, 3, -20, 10], [2, 3, -20, 5], [3, 2, 20, 7]], dtype=float)
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
	loc = np.array([[0, 0, 0, 1000, 1, 1, 0]], dtype=float)
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
	loc = np.array([[0, 0, 0, 1000, 1, 1]], dtype=float)
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


##################################################
def test_upscale_raw():
	"""Vérifie les blocs dupliqués, l'indépendance des plans et la conservation de l'entrée."""
	r = Renderer()
	r.set_size(3, 2, 2)
	raw = np.arange(12, dtype=np.uint16).reshape(2, 2, 3)
	original = raw.copy()
	res = r._upscale_raw(raw, 0)
	ref = np.array([[0, 0, 1, 1, 2, 2], [0, 0, 1, 1, 2, 2], [3, 3, 4, 4, 5, 5], [3, 3, 4, 4, 5, 5]])
	np.testing.assert_array_equal(res, np.stack((ref, ref + 6)))
	assert res.dtype == float
	assert not np.shares_memory(res, raw)
	np.testing.assert_array_equal(raw, original)
	# Une vue non contiguë doit également être acceptée.
	np.testing.assert_array_equal(r._upscale_raw(raw[:, :, ::-1], 0), res[:, :, ::-1])


##################################################
def test_upscale_raw_lanczos():
	"""Vérifie les plans constants, les valeurs intermédiaires et l'absence de mélange entre plans."""
	r = Renderer()
	r.set_size(3, 2, 3)
	raw = np.array([[[0, 1000, 0], [0, 1000, 0]], [[1234, 1234, 1234], [1234, 1234, 1234]]], dtype=np.uint16)
	original = raw.copy()
	res = r._upscale_raw(raw, 1)
	assert res.shape == (2, 6, 9)
	assert res.dtype == float
	assert np.isfinite(res).all()
	np.testing.assert_allclose(res[1], 1234)
	np.testing.assert_allclose(res[0], res[0, :, ::-1], atol=1e-5)
	assert np.any((res[0] > 0) & (res[0] < 1000))
	assert not np.shares_memory(res, raw)
	np.testing.assert_array_equal(raw, original)


##################################################
def test_upscale_raw_edge_cases():
	"""Vérifie le ratio un, les volumes vides, les dimensions incompatibles et les paramètres invalides."""
	r = Renderer()
	for mode in (0, 1):
		r.set_size(3, 2, 1)
		raw = np.arange(6, dtype=float).reshape(1, 2, 3) + 0.123456789
		res = r._upscale_raw(raw, mode)
		np.testing.assert_array_equal(res, raw)
		assert not np.shares_memory(res, raw)
		r.set_size(3, 2, 2)
		assert r._upscale_raw(np.empty((0, 2, 3)), mode).shape == (0, 4, 6)
		res = r._upscale_raw(np.ones((2, 1, 3)), mode)
		assert res.shape == (2, 4, 6)
		np.testing.assert_array_equal(res, 0)


##################################################
def test_upscale_raw_2d():
	"""Vérifie qu'une image 2D produit un volume à un plan dans les deux modes."""
	r = Renderer()
	raw = np.array([[0, 1000, 2000], [3000, 4000, 5000]], dtype=np.uint16)
	original = raw.copy()
	for ratio in (1, 2):
		r.set_size(3, 2, ratio)
		for mode in (0, 1):
			res = r._upscale_raw(raw, mode)
			assert res.shape == (1, 2 * ratio, 3 * ratio)
			assert res.dtype == float
			np.testing.assert_array_equal(res, r._upscale_raw(raw[None, :, :], mode))
			assert not np.shares_memory(res, raw)
			np.testing.assert_array_equal(raw, original)


##################################################
def test_draw_line_width():
	"""Vérifie les largeurs paires et impaires, les points, les bords et l'absence de cumul interne."""
	for width, first, last in ((1, 3, 4), (2, 3, 5), (3, 2, 5), (4, 2, 6)):
		for mode in (0, 1, 2):
			img, mask = Renderer.init_rendering(mode, 8, 8)
			Renderer.draw_line(img, mask, 2, 3, 5, 3, 10, mode, width=width)
			ref_mask = np.zeros((8, 8), dtype=bool)
			ref_mask[first:last, 2 - (width - 1) // 2:6 + width // 2] = True
			np.testing.assert_array_equal(mask, ref_mask)
			np.testing.assert_array_equal(img[mask], 10)
		# Un point isolé produit une empreinte carrée.
		img, mask = Renderer.init_rendering(0, 8, 8)
		Renderer.draw_line(img, mask, 3, 3, 3, 3, 10, width=width)
		ref = np.zeros((8, 8))
		ref[first:last, first:last] = 10
		np.testing.assert_array_equal(img, ref)

	# Une ligne dont le centre est hors de l'image peut encore toucher le bord.
	img, mask = Renderer.init_rendering(0, 5, 5)
	Renderer.draw_line(img, mask, -1, 0, -1, 4, 10, width=3)
	ref = np.zeros((5, 5))
	ref[:, 0] = 10
	np.testing.assert_array_equal(img, ref)
	np.testing.assert_array_equal(mask, ref > 0)


##################################################
def test_draw_line_width_orientations():
	"""Vérifie les diagonales, les pentes variées et le sens du tracé avec une référence par empreintes."""
	for x1, y1 in ((7, 7), (7, 4), (4, 7), (1, 7), (7, 1), (3, 7), (7, 3)):
		for reverse in (False, True):
			x0, y0, xe, ye = (x1, y1, 3, 3) if reverse else (3, 3, x1, y1)
			thin, thin_mask = Renderer.init_rendering(0, 10, 10)
			Renderer.draw_line(thin, thin_mask, x0, y0, xe, ye, 1)
			for width in (2, 3, 4):
				ref_mask = np.zeros((10, 10), dtype=bool)
				for y, x in np.argwhere(thin_mask):
					ref_mask[max(0, y - (width - 1) // 2):min(10, y + width // 2 + 1), max(0, x - (width - 1) // 2):min(10, x + width // 2 + 1)] = True
				img = np.full((10, 10), 20.0)
				mask = np.zeros((10, 10), dtype=bool)
				Renderer.draw_line(img, mask, x0, y0, xe, ye, 100, 1, width, 0.25)
				ref = np.full((10, 10), 20.0)
				ref[ref_mask] = 40.0
				np.testing.assert_array_equal(img, ref)
				np.testing.assert_array_equal(mask, ref_mask)


##################################################
def test_draw_line_alpha():
	"""Vérifie la transparence sur fond non nul pour les trois modes et les fonds d'initialisation infinis."""
	for width in (1, 3):
		for mode, color, expected in ((0, 100, 45), (1, 100, 40), (1, 10, 20), (2, 100, 20), (2, 4, 16)):
			img = np.full((7, 7), 20.0)
			mask = np.zeros((7, 7), dtype=bool)
			Renderer.draw_line(img, mask, 1, 3, 5, 3, color, mode, width, 0.25)
			assert mask.any()
			np.testing.assert_array_equal(img[mask], expected)
			np.testing.assert_array_equal(img[~mask], 20)
		for mode in (0, 1, 2):
			img, mask = Renderer.init_rendering(mode, 7, 7)
			original = img.copy()
			Renderer.draw_line(img, mask, 1, 3, 5, 3, 100, mode, width, 0)
			np.testing.assert_array_equal(img, original)
			assert not mask.any()
			Renderer.draw_line(img, mask, 1, 3, 5, 3, 100, mode, width, 0.25)
			np.testing.assert_array_equal(img[mask], 25)
			np.testing.assert_array_equal(img[~mask], original[~mask])


##################################################
def test_draw_line_clamped_parameters():
	"""Vérifie le bornage de la largeur et de l'opacité, sans exception ni contamination par NaN."""
	for width in (-5, 0, 1):
		for alpha, expected_alpha in ((-0.1, 0), (0.25, 0.25), (1.1, 1)):
			img, mask = Renderer.init_rendering(0, 5, 5)
			Renderer.draw_line(img, mask, 0, 0, 4, 4, 100, width=width, alpha=alpha)
			ref = np.eye(5) * (100 * expected_alpha)
			np.testing.assert_array_equal(img, ref)
			np.testing.assert_array_equal(mask, ref > 0)


##################################################
def test_draw_line_width_finalize():
	"""Vérifie que la finalisation conserve toute l'épaisseur grâce au masque de contribution."""
	for mode in (0, 1, 2):
		for width in (2, 3, 4):
			img, mask = Renderer.init_rendering(mode, 9, 9)
			Renderer.draw_line(img, mask, 2, 4, 6, 4, 100, mode, width, 0.5)
			res = Renderer.finalize_rendering(img, mask, bg_color=7)
			ref = np.full((9, 9), 7, dtype=np.uint16)
			ref[4 - (width - 1) // 2:5 + width // 2, 2 - (width - 1) // 2:7 + width // 2] = 50
			np.testing.assert_array_equal(res, ref)
			np.testing.assert_array_equal(mask, ref == 50)


##################################################
def test_line_spans():
	"""Vérifie directement les bornes inclusives/exclusives des lignes fines, épaisses et des points."""
	cases = [((1, 2, 4, 2, 1), 2, [1], [5]),
			 ((3, 1, 3, 4, 1), 1, [3, 3, 3, 3], [4, 4, 4, 4]),
			 ((0, 0, 4, 4, 1), 0, [0, 1, 2, 3, 4], [1, 2, 3, 4, 5]),
			 ((4, 0, 0, 4, 1), 0, [4, 3, 2, 1, 0], [5, 4, 3, 2, 1]),
			 ((2, 3, 5, 3, 3), 2, [1, 1, 1], [7, 7, 7]),
			 ((2, 3, 5, 3, 2), 3, [2, 2], [7, 7]),
			 ((3, 3, 3, 3, 3), 2, [2, 2, 2], [5, 5, 5]),
			 ((3, 3, 3, 3, 4), 2, [2, 2, 2, 2], [6, 6, 6, 6]), ]
	for args, expected_y, expected_left, expected_right in cases:
		for reverse in (False, True):
			x0, y0, x1, y1, width = args
			if reverse: x0, y0, x1, y1 = x1, y1, x0, y0
			y_min, left, right = Renderer._line_spans((8, 8), x0, y0, x1, y1, width)
			assert y_min == expected_y
			np.testing.assert_array_equal(left, expected_left)
			np.testing.assert_array_equal(right, expected_right)
			assert left.dtype == int and right.dtype == int


##################################################
def test_line_spans_clipping():
	"""Vérifie les empreintes hors cadre, les lignes vides et le bornage des largeurs."""
	for shape, points, width in (((0, 5), (0, 0, 4, 4), 3), ((5, 0), (0, 0, 4, 4), 3),
								 ((5, 5), (-4, -4, -2, -2), 1), ((5, 5), (6, 0, 6, 4), 1),
								 ((5, 5), (-3, 1, 1, -3), 1)):
		y_min, left, right = Renderer._line_spans(shape, *points, width)
		assert y_min == 0 and left.shape == (0,) and right.shape == (0,)
		assert left.dtype == int and right.dtype == int

	# Le centre de la ligne est hors cadre, mais son épaisseur touche la première colonne.
	y_min, left, right = Renderer._line_spans((5, 5), -1, -3, -1, 7, 3)
	assert y_min == 0
	np.testing.assert_array_equal(left, [0] * 5)
	np.testing.assert_array_equal(right, [1] * 5)

	# Certaines lignes de la boîte englobante restent vides : elles ne doivent pas remplir l'image.
	y_min, left, right = Renderer._line_spans((5, 5), -4, 0, 0, 4)
	assert y_min == 0
	assert np.all(left[:4] >= right[:4])
	assert left[4] == 0 and right[4] == 1

	for width in (-2, 0, 1):
		y_min, left, right = Renderer._line_spans((5, 5), -2, 2, 7, 2, width)
		assert y_min == 2
		np.testing.assert_array_equal(left, [0])
		np.testing.assert_array_equal(right, [5])


##################################################
def test_line_spans_orientations():
	"""Compare les empreintes à des points de référence explicites dans les huit octants."""
	# Segment de référence (0, 0) → (4, 2), avec les décisions d'arrondi de Bresenham.
	points = np.array([[0, 0], [1, 1], [2, 1], [3, 2], [4, 2]])
	for swap_axes in (False, True):
		for sign_x, sign_y in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
			coords = points[:, ::-1] if swap_axes else points
			coords = coords * [sign_x, sign_y] + [5, 5]
			for width in (1, 2, 3, 4):
				ref = np.zeros((11, 11), dtype=bool)
				for x, y in coords:
					ref[max(0, y - (width - 1) // 2):min(11, y + width // 2 + 1), max(0, x - (width - 1) // 2):min(11, x + width // 2 + 1)] = True
				y_min, left, right = Renderer._line_spans(ref.shape, *coords[0], *coords[-1], width)
				res = np.zeros_like(ref)
				for row, (start, end) in enumerate(zip(left, right)):
					res[y_min + row, start:end] = True
				np.testing.assert_array_equal(res, ref)


##################################################
def test_draw_line_thick_empty_rows():
	"""Vérifie que des intervalles vides ne modifient ni l'image ni le masque lors du dessin épais."""
	img = np.full((5, 5), 20.0)
	mask = np.zeros((5, 5), dtype=bool)
	Renderer.draw_line(img, mask, -5, 0, -1, 4, 100, 1, 3, 0.25)
	ref_mask = np.zeros((5, 5), dtype=bool)
	ref_mask[3:, 0] = True
	ref = np.full((5, 5), 20.0)
	ref[ref_mask] = 40
	np.testing.assert_array_equal(img, ref)
	np.testing.assert_array_equal(mask, ref_mask)


##################################################
def test_draw_track_blinks():
	"""Vérifie les apparitions aux plans 12/20, l'historique illimité et la conservation des entrées."""
	track = np.array([[10, 0, 1], [12, 2, 1], [20, 4, 1]])
	colors = np.array([5.0, 10.0, 30.0])
	original = track.copy()
	img = np.zeros((22, 3, 5))
	alpha = np.zeros_like(img)
	Renderer.draw_track(img, alpha, track, colors)
	ref = np.zeros_like(img)
	ref[12:, 1, :3] = 10
	ref[20:, 1, 2:] += 30
	np.testing.assert_array_equal(img, ref)
	np.testing.assert_array_equal(alpha, ref > 0)
	np.testing.assert_array_equal(track, original)
	np.testing.assert_array_equal(colors, [5, 10, 30])


##################################################
def test_draw_track_empty_rows():
	"""Vérifie que les lignes vides d'une empreinte partiellement hors cadre sont ignorées."""
	img = np.zeros((3, 5, 5))
	alpha = np.zeros_like(img)
	track = np.array([[0, -5, 0], [1, -1, 4]])

	Renderer.draw_track(img, alpha, track, np.array([0, 100]), tail_width=3, tail_length=1, fade_type=1)

	ref = np.zeros_like(img)
	ref[1:, 3:, 0] = 100
	np.testing.assert_array_equal(img, ref)

	ref_alpha = np.zeros_like(alpha)
	ref_alpha[1, 3:, 0] = 1
	ref_alpha[2, 3:, 0] = 0.5
	np.testing.assert_array_equal(alpha, ref_alpha)


##################################################
def test_draw_track_short_fade_long_blink():
	"""Vérifie le fade uniforme d'un segment qui apparaît après huit plans sans observation."""
	track = np.array([[12, 0, 1], [20, 4, 1]])
	img = np.zeros((24, 3, 5))
	alpha = np.zeros_like(img)
	Renderer.draw_track(img, alpha, track, np.array([5, 90]), tail_length=2, fade_type=1)
	ref_alpha = np.zeros_like(alpha)
	# Tout le segment apparaît opaque, puis vieillit uniquement depuis son arrivée au plan 20.
	ref_alpha[20, 1, :] = 1
	ref_alpha[21, 1, :] = 2 / 3
	ref_alpha[22, 1, :] = 1 / 3
	np.testing.assert_allclose(alpha, ref_alpha)
	np.testing.assert_array_equal(img, np.where(ref_alpha > 0, 90, 0))


##################################################
def test_draw_track_hard_cutoff():
	"""Vérifie la limite d'âge inclusive et les plans sans nouvelle observation, sans fade."""
	track = np.array([[0, 0, 0], [4, 4, 0]])
	img = np.zeros((8, 1, 5))
	alpha = np.zeros_like(img)
	Renderer.draw_track(img, alpha, track, np.array([1, 50]), tail_length=2)
	ref = np.zeros_like(img)
	ref[4:7, 0, :] = 1
	np.testing.assert_array_equal(alpha, ref)
	np.testing.assert_array_equal(img, ref * 50)


##################################################
def test_draw_track_overlap():
	"""Vérifie la combinaison indépendante des intensités et le maximum des opacités."""
	for mode, initial, expected in ((0, 0, 120), (1, -np.inf, 100), (2, np.inf, 20)):
		img = np.full((5, 5, 5), initial, dtype=float)
		alpha = np.zeros_like(img)
		# Au plan 3, l'horizontale a un âge de 1 ; la verticale vient d'apparaître et impose alpha = 1.
		Renderer.draw_track(img, alpha, np.array([[0, 0, 2], [2, 4, 2]]), np.array([0, 100]), tail_length=3, fade_type=1, color_mode=mode)
		Renderer.draw_track(img, alpha, np.array([[1, 2, 0], [3, 2, 4]]), np.array([0, 20]), tail_length=3, fade_type=1, color_mode=mode)
		assert img[3, 2, 2] == expected
		assert alpha[3, 2, 2] == 1
		assert alpha[4, 2, 2] == 0.75
		assert img[0, 0, 0] == initial and alpha[0, 0, 0] == 0


##################################################
def test_draw_track_thickness():
	"""Vérifie l'opacité uniforme sur toute l'épaisseur et l'absence de cumul interne."""
	track = np.array([[0, 2, 3], [2, 4, 3]])
	for mode, initial in ((0, 0), (1, -np.inf), (2, np.inf)):
		img = np.full((5, 7, 7), initial, dtype=float)
		alpha = np.zeros_like(img)
		Renderer.draw_track(img, alpha, track, np.array([0, 80]), tail_width=3, tail_length=2, fade_type=1, color_mode=mode)
		ref = np.zeros_like(alpha)
		ref[2, 2:5, 1:6] = 1
		ref[3, 2:5, 1:6] = 2 / 3
		ref[4, 2:5, 1:6] = 1 / 3
		np.testing.assert_allclose(alpha, ref)
		np.testing.assert_array_equal(img, np.where(ref > 0, 80, initial))


##################################################
def test_draw_track_stationary_and_clipping():
	"""Vérifie un déplacement nul au bord, les segments hors cadre et les bornes temporelles du volume."""
	img = np.zeros((5, 3, 3))
	alpha = np.zeros_like(img)
	Renderer.draw_track(img, alpha, np.array([[0, 0, 0], [2, 0, 0]]), np.array([0, 10]), tail_width=3, tail_length=1, fade_type=1)
	ref = np.zeros_like(alpha)
	ref[2, :2, :2] = 1
	ref[3, :2, :2] = 0.5
	np.testing.assert_array_equal(alpha, ref)
	np.testing.assert_array_equal(img, np.where(ref > 0, 10, 0))

	for track in (np.empty((0, 3), dtype=int), np.array([[0, 1, 1]]), np.array([[5, 0, 0], [6, 1, 1]]),
				  np.array([[-5, 0, 0], [-4, 1, 1]]), np.array([[0, -5, -5], [1, -4, -4]])):
		img.fill(0)
		alpha.fill(0)
		Renderer.draw_track(img, alpha, track, np.ones(len(track)), tail_length=1)
		np.testing.assert_array_equal(img, 0)
		np.testing.assert_array_equal(alpha, 0)

	# Une queue désactivée ne dessine pas les têtes ; leur passe reste séparée.
	Renderer.draw_track(img, alpha, np.array([[0, 0, 0], [1, 2, 2]]), np.array([1, 2]), tail_length=0)
	np.testing.assert_array_equal(img, 0)
	np.testing.assert_array_equal(alpha, 0)


##################################################
def test_draw_track_alpha_independent_of_geometry():
	"""Vérifie que seul le plan d'arrivée détermine l'alpha, quels que soient le départ et la longueur spatiale."""
	for departure in (0, 9):
		for endpoint in ((1, 1), (8, 1), (8, 8)):
			track = np.array([[departure, 1, 1], [10, *endpoint]])
			img = np.zeros((14, 10, 10))
			alpha = np.zeros_like(img)
			Renderer.draw_track(img, alpha, track, np.array([1, 50]), tail_length=2, fade_type=1)
			mask = img[10] > 0
			assert mask.any()
			for plane, expected in ((10, 1), (11, 2 / 3), (12, 1 / 3)):
				np.testing.assert_allclose(alpha[plane, mask], expected)
				np.testing.assert_array_equal(alpha[plane, ~mask], 0)
			np.testing.assert_array_equal(alpha[:10], 0)
			np.testing.assert_array_equal(alpha[13:], 0)


##################################################
def test_draw_track_heads_planes():
	"""Vérifie les plans observés uniquement, le diamètre minimal et la conservation des entrées."""
	track = np.array([[1, 2, 1], [4, 3, 2]])
	colors = np.array([20.0, 70.0])
	original = track.copy()
	for size in (-2, 0, 1):
		img = np.zeros((6, 4, 5))
		alpha = np.zeros_like(img)
		Renderer.draw_track_heads(img, alpha, track, colors, size)
		ref = np.zeros_like(img)
		ref[1, 1, 2], ref[4, 2, 3] = colors
		np.testing.assert_array_equal(img, ref)
		np.testing.assert_array_equal(alpha, ref > 0)
	np.testing.assert_array_equal(track, original)
	np.testing.assert_array_equal(colors, [20, 70])


##################################################
def test_draw_track_heads_circles():
	"""Vérifie les contours de diamètres pairs et impairs et les pixels minimaux du diamètre deux."""
	for size, pattern in ((2, [[1, 1], [1, 1]]),
						  (4, [[0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 1], [0, 1, 1, 0]]),
						  (5, [[0, 1, 1, 1, 0], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [0, 1, 1, 1, 0]])):
		img = np.zeros((3, 9, 9))
		alpha = np.zeros_like(img)
		Renderer.draw_track_heads(img, alpha, np.array([[1, 4, 4]]), np.array([80]), size)
		ref = np.zeros_like(img)
		start = 4 - (size - 1) // 2
		ref[1, start:start + size, start:start + size] = pattern
		np.testing.assert_array_equal(alpha, ref)
		np.testing.assert_array_equal(img, ref * 80)


##################################################
def test_draw_track_heads_clipping():
	"""Vérifie le recadrage des cercles aux bords sans déplacer leur centre et les entrées hors volume."""
	img = np.zeros((2, 3, 3))
	alpha = np.zeros_like(img)
	Renderer.draw_track_heads(img, alpha, np.array([[0, 0, 0], [1, 2, 2]]), np.array([10, 20]), 4)
	ref = np.zeros_like(img)
	ref[0] = [[0, 0, 10], [0, 0, 10], [10, 10, 0]]
	ref[1] = [[0, 0, 0], [0, 0, 20], [0, 20, 0]]
	np.testing.assert_array_equal(img, ref)
	np.testing.assert_array_equal(alpha, ref > 0)
	for track in (np.empty((0, 3), dtype=int), np.array([[-1, 1, 1], [2, 1, 1], [0, -9, -9], [0, 9, 9]])):
		Renderer.draw_track_heads(img, alpha, track, np.ones(len(track)), 4)
		np.testing.assert_array_equal(img, ref)
		np.testing.assert_array_equal(alpha, ref > 0)


##################################################
def test_draw_track_heads_priority():
	"""Vérifie la priorité opaque des têtes sur une queue et la priorité de la dernière tête dessinée."""
	img = np.zeros((5, 5, 5))
	alpha = np.zeros_like(img)
	Renderer.draw_track(img, alpha, np.array([[0, 0, 2], [1, 4, 2]]), np.array([0, 100]), tail_length=3, fade_type=1)
	original_img, original_alpha = img.copy(), alpha.copy()
	Renderer.draw_track_heads(img, alpha, np.array([[2, 2, 2], [2, 2, 2]]), np.array([20, 0]))
	original_img[2, 2, 2] = 0  # Une intensité nulle reste une tête opaque ; elle ne doit pas devenir transparente.
	original_alpha[2, 2, 2] = 1
	np.testing.assert_array_equal(img, original_img)
	np.testing.assert_array_equal(alpha, original_alpha)


##################################################
def test_draw_track_heads_preserve_interior():
	"""Vérifie que le contour laisse les intensités et les opacités existantes intactes à l'intérieur."""
	img = np.full((3, 7, 7), 40.0)
	alpha = np.full_like(img, 0.25)
	Renderer.draw_track_heads(img, alpha, np.array([[1, 3, 3]]), np.array([90]), 5)
	contour = np.array([[0, 1, 1, 1, 0], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [0, 1, 1, 1, 0]], dtype=bool)
	mask = np.zeros(img.shape, dtype=bool)
	mask[1, 1:6, 1:6] = contour
	np.testing.assert_array_equal(img, np.where(mask, 90, 40))
	np.testing.assert_array_equal(alpha, np.where(mask, 1, 0.25))


##################################################
def test_finalize_track_stack():
	"""Vérifie le mélange unique avec le fond, la saturation après mélange et la troncature."""
	img = np.array([[[100, 100, 100, 1.9, -100, 70000, 70000]]], dtype=float)
	alpha = np.array([[[0, 0.25, 1, 1, 1, 1, 0.5]]], dtype=float)
	original_alpha = alpha.copy()
	res = Renderer.finalize_track_stack(img, alpha, bg_color=20)
	np.testing.assert_array_equal(res, [[[20, 40, 100, 1, 0, 65535, 35010]]])
	np.testing.assert_array_equal(img, [[[20, 40, 100, 1.9, 0, 65535, 35010]]])
	np.testing.assert_array_equal(alpha, original_alpha)
	assert res.dtype == np.uint16 and res.shape == img.shape
	assert not np.shares_memory(res, img)


##################################################
def test_finalize_track_stack_empty_background():
	"""Vérifie les fonds sans contribution et l'absence de calcul invalide avec les infinis d'initialisation."""
	for initial in (0, -np.inf, np.inf):
		for background, expected in ((0, 0), (42, 42), (-10, 0), (70000, 65535)):
			img = np.full((2, 3, 4), initial, dtype=float)
			alpha = np.zeros_like(img)
			with np.errstate(all='raise'):
				res = Renderer.finalize_track_stack(img, alpha, background)
			np.testing.assert_array_equal(res, np.full(img.shape, expected, dtype=np.uint16))
			np.testing.assert_array_equal(alpha, 0)
	for shape in ((0, 3, 4), (2, 0, 4), (2, 3, 0)):
		res = Renderer.finalize_track_stack(np.empty(shape), np.empty(shape))
		assert res.shape == shape and res.dtype == np.uint16


##################################################
def test_finalize_track_stack_strided():
	"""Vérifie la finalisation d'une vue non contiguë sans modifier les pixels voisins ni l'alpha."""
	base = np.full((2, 3, 8), 100.0)
	view = base[:, :, ::2]
	alpha = np.full(view.shape, 0.5)
	res = Renderer.finalize_track_stack(view, alpha, 20)
	np.testing.assert_array_equal(res, np.full(view.shape, 60, dtype=np.uint16))
	np.testing.assert_array_equal(base[:, :, ::2], 60)
	np.testing.assert_array_equal(base[:, :, 1::2], 100)
	np.testing.assert_array_equal(alpha, 0.5)


##################################################
def test_finalize_track_stack_drawing():
	"""Vérifie le fade d'une queue sur fond non nul et la tête opaque sur son seul plan, pour les trois modes."""
	for mode, initial in ((0, 0), (1, -np.inf), (2, np.inf)):
		img = np.full((5, 3, 5), initial, dtype=float)
		alpha = np.zeros_like(img)
		track = np.array([[0, 1, 1], [1, 3, 1]])
		colors = np.array([40, 100])
		Renderer.draw_track(img, alpha, track, colors, tail_length=1, fade_type=1, color_mode=mode)
		Renderer.draw_track_heads(img, alpha, track, colors)
		with np.errstate(all='raise'):
			res = Renderer.finalize_track_stack(img, alpha, 20)
		ref = np.full(img.shape, 20, dtype=np.uint16)
		ref[0, 1, 1] = 40
		ref[1, 1, 1:4] = 100
		ref[2, 1, 1:4] = 60
		np.testing.assert_array_equal(res, ref)


##################################################
def test_finalize_track_stack_remainder():
	"""Vérifie le modulo après mélange, les valeurs négatives, les tours multiples et la troncature."""
	img = np.array([[[-1, -1.5, 65536, 65537, 131073, 70000, -np.inf, np.inf]]], dtype=float)
	alpha = np.array([[[1, 1, 1, 1, 1, 0.5, 0, 0]]], dtype=float)
	original_alpha = alpha.copy()
	with np.errstate(all='raise'):
		res = Renderer.finalize_track_stack(img, alpha, bg_color=20, clip=False)
	np.testing.assert_array_equal(res, [[[65535, 65534, 0, 1, 1, 35010, 20, 20]]])
	np.testing.assert_array_equal(img, [[[65535, 65534.5, 0, 1, 1, 35010, 20, 20]]])
	np.testing.assert_array_equal(alpha, original_alpha)
	assert res.dtype == np.uint16
	# Le fond est également replié lorsque l'alpha est nul.
	for background, expected in ((-1, 65535), (65536, 0), (131073, 1)):
		res = Renderer.finalize_track_stack(np.full((1, 1, 1), np.inf), np.zeros((1, 1, 1)), background, clip=False)
		np.testing.assert_array_equal(res, [[[expected]]])


##################################################
def test_track_stack_timeline():
	"""Vérifie le recadrage temporel, les blinks, le fade et les têtes sur leurs seuls plans."""
	r = Renderer()
	r.set_size(5, 3, 1)
	track = np.array([[1, 10, 0, 1, 40], [1, 12, 2, 1, 100], [1, 16, 4, 1, 80]], dtype=float)
	original = track.copy()
	res = r.track_stack(track, bg_color=20, tail_length=1, fade_type=1)
	ref = np.full((7, 3, 5), 20, dtype=np.uint16)
	ref[0, 1, 0] = 40
	ref[2, 1, :3] = 100
	ref[3, 1, :3] = 60
	ref[6, 1, 2:] = 80
	np.testing.assert_array_equal(res, ref)
	np.testing.assert_array_equal(track, original)
	assert res.dtype == np.uint16


##################################################
def test_track_stack_empty_and_scale():
	"""Vérifie les sorties anticipées 3D et la mise à l'échelle des coordonnées."""
	r = Renderer()
	r.set_size(3, 2, 2)
	for data in (np.empty((0, 5)), np.zeros(5), np.zeros((1, 4)), np.array([[1, 4, -5, -5, 20]])):
		res = r.track_stack(data, bg_color=17)
		np.testing.assert_array_equal(res, np.full((1, 4, 6), 17, dtype=np.uint16))
	res = r.track_stack(np.array([[1, 50, 1, 1, 90]]), bg_color=17, tail_length=0)
	ref = np.full((1, 4, 6), 17, dtype=np.uint16)
	ref[0, 2, 2] = 90
	np.testing.assert_array_equal(res, ref)
	r.set_size(0, -1, 1)
	np.testing.assert_array_equal(r.track_stack(np.empty((0, 5)), bg_color=17), [[[17]]])


##################################################
def test_track_stack_priority_and_modes():
	"""Vérifie les croisements, les queues illimitées et la priorité globale des têtes."""
	r = Renderer()
	r.set_size(5, 5, 1)
	tracks = np.array([[1, 10, 0, 2, 10], [1, 11, 4, 2, 10], [2, 10, 2, 0, 20], [2, 11, 2, 4, 20],
					   [3, 12, 0, 0, 5]], dtype=float)
	for mode, expected in ((0, 30), (1, 20), (2, 10)):
		res = r.track_stack(tracks, color_mode=mode, bg_color=7)
		assert res.shape == (3, 5, 5)
		assert res[0, 2, 2] == 7
		assert res[1, 2, 2] == expected and res[2, 2, 2] == expected
	# La tête de la première trajectoire doit rester visible même si la queue suivante la traverse.
	tracks = np.array([[1, 11, 2, 2, 3], [2, 10, 0, 2, 100], [2, 11, 4, 2, 100]], dtype=float)
	res = r.track_stack(tracks, color_mode=1, bg_color=7)
	assert res[1, 2, 2] == 3 and res[1, 2, 1] == 100


##################################################
def test_finalize_track_stack_rgb():
	"""Vérifie la colormap, le gris, les alphas nul/partiel/opaque et la conservation des entrées."""
	img = np.array([[[np.inf, 65535, 65535, 0]]])
	alpha = np.array([[[0, 0.5, 1, 1]]])
	raw = np.full(img.shape, 2570.0)
	for cmap in ("viridis", "magma"):
		with np.errstate(all='raise'):
			res = Renderer.finalize_track_stack_rgb(img, alpha, raw, cmap)
		color = FileIO.grayscale_to_color(np.array([[65535]], dtype=np.uint16), cmap)[0, 0]
		np.testing.assert_array_equal(res[0, 0, 0], [10, 10, 10])
		np.testing.assert_array_equal(res[0, 0, 1], np.rint(5 + 0.5 * color))
		np.testing.assert_array_equal(res[0, 0, 2], color)
		np.testing.assert_array_equal(res[0, 0, 3], [0, 0, 0])
		assert res.dtype == np.uint8 and res.shape == (1, 1, 4, 3)
	np.testing.assert_array_equal(img, [[[np.inf, 65535, 65535, 0]]])
	np.testing.assert_array_equal(alpha, [[[0, 0.5, 1, 1]]])
	np.testing.assert_array_equal(raw, 2570)
	with np.testing.assert_raises(ValueError): Renderer.finalize_track_stack_rgb(img, alpha, raw[:, :, :2])


##################################################
def test_track_stack_raw():
	"""Vérifie la sélection des plans 1-based, l'upscale et les têtes identiques quel que soit color_mode."""
	r = Renderer()
	r.set_size(3, 2, 2)
	raw = np.stack([np.full((2, 3), value, dtype=np.uint16) for value in (257, 2570, 5140, 7710, 65535)])
	original = raw.copy()
	tracks = np.array([[1, 2, 0, 0, 65535], [1, 4, 1, 0, 65535]], dtype=float)
	for upscale in (0, 1):
		ref = r.track_stack(tracks, raw=raw, tail_length=0, upscale_type=upscale)
		assert ref.shape == (3, 4, 6, 3) and ref.dtype == np.uint8
		np.testing.assert_array_equal(ref[:, 3, 5], [[10] * 3, [20] * 3, [30] * 3])
		color = FileIO.grayscale_to_color(np.array([[65535]], dtype=np.uint16))[0, 0]
		np.testing.assert_array_equal(ref[0, 0, 0], color)
		np.testing.assert_array_equal(ref[2, 0, 2], color)
		for mode in (1, 2):
			np.testing.assert_array_equal(r.track_stack(tracks, color_mode=mode, raw=raw, tail_length=0, upscale_type=upscale), ref)
	np.testing.assert_array_equal(raw, original)
	with np.testing.assert_raises(ValueError): r.track_stack(tracks, raw=raw[:2])


##################################################
def test_track_stack_raw_empty_and_2d():
	"""Vérifie le retour scalaire sans observation et le rendu RGB sur fond 2D avec une observation."""
	r = Renderer()
	r.set_size(2, 2, 1)
	res = r.track_stack(np.empty((0, 5)), raw=np.zeros((1, 2, 2)), bg_color=2570)
	np.testing.assert_array_equal(res, np.full((1, 2, 2), 2570, dtype=np.uint16))
	res = r.track_stack(np.array([[1, 1, 0, 0, 65535]]), raw=np.full((2, 2), 5140))
	assert res.shape == (1, 2, 2, 3)
	np.testing.assert_array_equal(res[0, 1, 1], [20, 20, 20])


##################################################
def test_track_stack_raw_fade_and_overlap():
	"""Vérifie le fade sur raw et la colormap après addition, maximum ou minimum aux croisements."""
	r = Renderer()
	r.set_size(5, 5, 1)
	tracks = np.array([[1, 1, 0, 2, 30000], [1, 2, 4, 2, 30000], [2, 1, 2, 0, 10000], [2, 2, 2, 4, 10000], [3, 3, 0, 0, 1]], dtype=float)
	raw = np.full((3, 5, 5), 5140, dtype=np.uint16)
	for mode, intensity in ((0, 40000), (1, 30000), (2, 10000)):
		color = FileIO.grayscale_to_color(np.array([[intensity]], dtype=np.uint16))[0, 0]
		res = r.track_stack(tracks, raw=raw, color_mode=mode, tail_length=1, fade_type=1)
		np.testing.assert_array_equal(res[1, 2, 2], color)
		np.testing.assert_array_equal(res[2, 2, 2], np.rint(10 + 0.5 * color))
		np.testing.assert_array_equal(res[:, 4, 4], [[20] * 3] * 3)


##################################################
def test_renderer_track_stack_spiral():
	"""Exporte une spirale animée pour vérifier visuellement la queue, le fade, la tête et le fond gris foncé."""
	r = Renderer()
	size = 256
	n_points = 72
	r.set_size(size, size, 2)
	theta = np.linspace(0, 4 * np.pi, n_points)
	radius = np.linspace(size // 16, size // 2.5, n_points)
	track = np.column_stack((np.ones(n_points), np.arange(10, 10 + n_points),
							 size // 2 + radius * np.cos(theta), size // 2 + radius * np.sin(theta), np.full(n_points, 58000)))
	res = r.track_stack(track, color_mode=1, bg_color=8000, head_size=15, tail_width=2, tail_length=9, fade_type=1)
	assert res.shape == (n_points, size * 2, size * 2) and res.dtype == np.uint16
	assert np.all(res[:, 0, 0] == 8000)
	assert np.any((res[-1] > 8000) & (res[-1] < 58000))
	assert np.max(res[-1]) == 58000
	FileIO.save_tif(res, OUTPUT_DIR / "track_stack_spiral.tif")
	# Échelle fixe sur toute l'animation pour préserver visuellement les intensités du fond et du fade.
	frames = [Image.fromarray((plane / 257).astype(np.uint8)) for plane in res]
	frames[0].save(OUTPUT_DIR / "track_stack_spiral.gif", save_all=True, append_images=frames[1:], duration=80, loop=0, optimize=False)


##################################################
def test_renderer_track_stack_spiral_raw():
	"""Exporte une spirale rouge avec fade sur un léger dégradé gris mouvant pour vérification visuelle."""
	r = Renderer()
	size = 256
	r.set_size(size, size, 2)
	n_points = 72
	theta = np.linspace(0, 4 * np.pi, n_points)
	radius = np.linspace(size // 16, size // 2.5, n_points)
	# La LUT réserve zéro au noir ; son indice un correspond au début de HSV, donc au rouge pur.
	track = np.column_stack((np.ones(n_points), np.arange(10, 10 + n_points),
							 size // 2 + radius * np.cos(theta), size // 2 + radius * np.sin(theta), np.ones(n_points)))
	x = np.linspace(0, 1, size)[None, :]
	y = np.linspace(0, 1, size)[:, None]
	# Le raw commence au plan d'acquisition un, tandis que la trajectoire commence au plan dix.
	raw = np.empty((n_points + 9, size, size), dtype=np.uint16)
	for plane in range(len(raw)):
		phase = 2 * np.pi * (plane - 9) / n_points
		raw[plane] = np.rint(9500 + 2500 * np.sin(2 * np.pi * x - phase) + 1500 * y).astype(np.uint16)
	res = r.track_stack(track, color_mode=1, raw=raw, color_map="hsv", head_size=15, tail_width=2, tail_length=9, fade_type=1)
	assert res.shape == (n_points, size * 2, size * 2, 3) and res.dtype == np.uint8
	background = np.rint(raw[9:, 0, 0] / 257.0).astype(np.uint8)
	np.testing.assert_array_equal(res[:, 0, 0], np.repeat(background[:, None], 3, axis=1))
	assert np.ptp(background) > 0  # Le fond doit effectivement évoluer pendant l'animation.
	assert np.any(np.all(res[-1] == [255, 0, 0], axis=-1))
	assert np.any((res[-1, :, :, 0] > res[-1, :, :, 1]) & (res[-1, :, :, 1] > 0))  # Mélange rouge/gris dû au fade.
	# Exporter la séquence RGB avec la même fonction que les volumes scalaires.
	path = OUTPUT_DIR / "track_stack_spiral_raw.tif"
	FileIO.save_tif(res, path)
	np.testing.assert_array_equal(tifffile.imread(path), res)
	frames = [Image.fromarray(plane) for plane in res]
	frames[0].save(OUTPUT_DIR / "track_stack_spiral_raw.gif", save_all=True, append_images=frames[1:], duration=80, loop=0, optimize=False)
