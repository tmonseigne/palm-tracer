"""Fichier des tests pour le renderer."""
import numpy as np
import pandas as pd

from palm_tracer.Processing import Renderer


##################################################
def test_set_size():
	r = Renderer()
	assert r._width == 1 and r._height == 1 and r._ratio == 1
	r.set_size(100, 200, 10)
	assert r._width == 100 and r._height == 200 and r._ratio == 10


##################################################
def test_get_localization_colors():
	# Empty Dataframe
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
	# Empty Dataframe
	trc = pd.DataFrame(columns=["Track", "Plane", "X", "Y", "Integrated Intensity"])
	res = Renderer.add_colors_to_tracks(trc, "Track Number")
	assert res.shape == (0, 5)

	# No Column selected (and sorting)
	trc = pd.DataFrame({"Track": [2, 1, 1], "Plane": [5, 6, 3], "X": [2, 0, 0], "Y": [2, 1, 0], "Integrated Intensity": [7, 6, 5]})
	res = Renderer.add_colors_to_tracks(trc)
	ref = np.array([[1, 3, 0, 0, 1], [1, 6, 0, 1, 1], [2, 5, 2, 2, 1]], dtype=np.float64)
	np.testing.assert_array_equal(res, ref)

	# Track number
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
def test_draw_line():
	img = np.zeros((5, 5), dtype=np.uint16)

	# Single Point
	Renderer.draw_line(img, 2, 3, 2, 3, np.uint16(123))
	ref = np.zeros((5, 5), dtype=np.uint16)
	ref[3, 2] = 123
	np.testing.assert_array_equal(img, ref)

	# Horizontal line
	img = np.zeros((5, 5), dtype=np.uint16)
	Renderer.draw_line(img, 1, 2, 4, 2, np.uint16(10))
	ref = np.zeros((5, 5), dtype=np.uint16)
	ref[2, 1:5] = 10
	np.testing.assert_array_equal(img, ref)

	# Vertical line
	img = np.zeros((5, 5), dtype=np.uint16)
	Renderer.draw_line(img, 3, 1, 3, 4, np.uint16(20))
	ref = np.zeros((5, 5), dtype=np.uint16)
	ref[1:5, 3] = 20
	np.testing.assert_array_equal(img, ref)

	# Diagonal line
	img = np.zeros((5, 5), dtype=np.uint16)
	Renderer.draw_line(img, 0, 0, 4, 4, np.uint16(7))
	ref = np.zeros((5, 5), dtype=np.uint16)
	np.fill_diagonal(ref, 7)
	np.testing.assert_array_equal(img, ref)

	# Keep Max
	img = np.zeros((5, 5), dtype=np.uint16)
	img[2, 2] = 100
	Renderer.draw_line(img, 2, 2, 4, 2, np.uint16(50))
	assert img[2, 2] == 100 and img[2, 3] == 50 and img[2, 4] == 50

	# Outside points
	img = np.zeros((5, 5), dtype=np.uint16)
	Renderer.draw_line(img, -2, -2, 2, 2, np.uint16(30))
	assert img[0, 0] == 30 and img[1, 1] == 30 and img[2, 2] == 30


##################################################
def test_draw_gaussian():
	r = Renderer()

	img = np.zeros((5, 5), dtype=float)
	x, y, color, sx, sy, theta = 2, 2, 100, 1, 2, 0
	ref = np.array([[0.65321166, 0.95041736, 1.07696397, 0.95041736, 0.65321166],
					[2.92749158, 4.25947511, 4.82661763, 4.25947511, 2.92749158],
					[4.82661763, 7.02268722, 7.95774715, 7.02268722, 4.82661763],
					[2.92749158, 4.25947511, 4.82661763, 4.25947511, 2.92749158],
					[0.65321166, 0.95041736, 1.07696397, 0.95041736, 0.65321166]])

	# Simple anisotrope
	res = r.draw_gaussian_2d(img, x, y, color, sx, sy, theta, 1)
	assert np.allclose(res, ref, atol=1e-6)

	# Simple anisotrope avec cumul
	res = r.draw_gaussian_2d(res, x, y, color, sx, sy, theta, 0)
	assert np.allclose(res, 2 * ref, atol=1e-6)

	# Simple anisotrope avec angle de 90° (transposé du premier test
	img = np.zeros((5, 5), dtype=float)
	res = r.draw_gaussian_2d(img, x, y, color, sx, sy, np.pi / 2, 1)
	assert np.allclose(res, ref.transpose(), atol=1e-6)

	# Hors dimensions
	img = np.zeros((5, 5), dtype=float)
	res = r.draw_gaussian_2d(img, -10, -10, color, sx, sy, theta, 0)
	assert np.allclose(res, 0.0)

	# Sigma négatif
	res = r.draw_gaussian_2d(img, x, y, color, -1, sy, theta, 0)
	assert np.allclose(res, 0.0)


##################################################
def test_localizations():
	r = Renderer()

	# Not initialized
	loc = np.array([1, 2, 3], dtype=np.float64)
	res = r.localizations(loc)
	assert res.shape == (1, 1)

	# Bad Size
	r.set_size(10, -1, 2)
	res = r.localizations(loc)
	assert res.shape == (1, 20)

	# Invalid Shape
	r.set_size(5, 10, 2)
	res = r.localizations(loc)
	assert res.shape == (20, 10) and np.count_nonzero(res) == 0

	# Points outside
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

	# Clip
	loc = np.array([[1, 1, 70000], [1, 1, 1000]], dtype=np.float64)
	res = r.localizations(loc)
	assert res[2, 2] == np.iinfo(np.uint16).max


##################################################
def test_localizations_gaussian():
	r = Renderer()
	r.set_size(5, 5, 1)

	# Bad size
	loc = np.array([[2, 2, 100]], dtype=np.float64)
	gaussian = {
			"Intensity":       100,
			"Fixed Intensity": True,
			"Shape":           0,
			"Size":            1
			}
	res = r.localizations(loc, 0, gaussian)
	assert res.shape == (5, 5) and np.count_nonzero(res) == 0

	# Fixed Size and intensity
	loc = np.array([[2, 2, 10000, 1, 2, 0]], dtype=np.float64)
	res = r.localizations(loc, 0, gaussian)
	ref = np.array([[0, 1, 2, 1, 0],
					[1, 5, 9, 5, 1],
					[2, 9, 15, 9, 2],
					[1, 5, 9, 5, 1],
					[0, 1, 2, 1, 0]], dtype=np.uint16)
	np.allclose(res, ref)

	# Fixed Size and not intensity
	gaussian["Fixed Intensity"] = False
	res = r.localizations(loc, 0, gaussian)
	np.allclose(res, ref)

	# Isotrope (Sigma = 1.5 car moyenne des deux)
	gaussian["Fixed Intensity"] = True
	gaussian["Shape"] = 1
	res = r.localizations(loc, 0, gaussian)
	ref = np.array([[1, 2, 2, 2, 1],
					[2, 4, 5, 4, 2],
					[2, 5, 7, 5, 2],
					[2, 4, 5, 4, 2],
					[1, 2, 2, 2, 1]], dtype=np.uint16)
	np.allclose(res, ref)

	# Anisotrope
	gaussian["Shape"] = 2
	res = r.localizations(loc, 0, gaussian)
	ref = np.array([[0, 0, 1, 0, 0],
					[2, 4, 4, 4, 2],
					[4, 7, 7, 7, 4],
					[2, 4, 4, 4, 2],
					[0, 0, 1, 0, 0]], dtype=np.uint16)
	np.allclose(res, ref)

	# Max, résultat identique, car 2 points confondus.
	loc = np.array([[2, 2, 100, 1, 2, 0], [2, 2, 100, 1, 2, 0]], dtype=np.float64)
	res = r.localizations(loc, 1, gaussian)
	np.allclose(res, ref)

	# Accumulate (on vérifie que les flottants ont bien été pris en compte durant le calcul, ce n'est pas un simple * 2 de la valeur entière finale)
	loc = np.array([[2, 2, 100, 1, 2, 0], [2, 2, 100, 1, 2, 0]], dtype=np.float64)
	res = r.localizations(loc, 0, gaussian)
	ref = np.array([[1, 1, 2, 1, 1],
					[5, 8, 9, 8, 5],
					[9, 14, 15, 14, 9],
					[5, 8, 9, 8, 5],
					[1, 1, 2, 1, 1]], dtype=np.uint16)
	np.allclose(res, ref)


##################################################
def test_tracks():
	r = Renderer()

	# Not initialized
	trc = np.array([1, 2, 3], dtype=np.float64)
	res = r.tracks(trc)
	assert res.shape == (1, 1)

	# Bad Size
	r.set_size(10, -1, 2)
	res = r.tracks(trc)
	assert res.shape == (1, 20)

	# Invalid Shape
	r.set_size(5, 10, 2)
	res = r.tracks(trc)
	assert res.shape == (20, 10) and np.count_nonzero(res) == 0

	# Points outside
	trc = np.array([[1, 10, 2, 100], [1, 2, 10, 100], ], dtype=np.float64)
	res = r.tracks(trc)
	assert res.shape == (20, 10) and np.count_nonzero(res) == 0

	# Single point
	trc = np.array([[1, 2, 3, 50], ], dtype=np.float64)
	res = r.tracks(trc)
	ref = np.zeros((20, 10), dtype=np.uint16)
	ref[6, 4] = 50
	np.testing.assert_array_equal(res, ref)

	# Two crossed track the lowest (horizontal) is cut by the highest (vertical)
	trc = np.array([[1, 1, 3, 10], [1, 4, 3, 10], [2, 3, 1, 20], [2, 3, 4, 20], ], dtype=np.float64)
	res = r.tracks(trc)
	ref = np.zeros((20, 10), dtype=np.uint16)
	ref[6, 2:6] = 10
	ref[6, 7:9] = 10
	ref[2:9, 6] = 20
	np.testing.assert_array_equal(res, ref)
