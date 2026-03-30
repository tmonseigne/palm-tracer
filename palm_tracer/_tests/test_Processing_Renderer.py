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
	res = Renderer.get_localization_colors(loc, "Intensity")
	assert res.shape == (0, 3)

	# No Column selected
	loc = pd.DataFrame({"X": [1, 2], "Y": [3, 4], "Intensity": [10, 20]})
	res = Renderer.get_localization_colors(loc)
	ref = np.array([[1, 3, 1], [2, 4, 1]], dtype=np.float64)
	np.testing.assert_array_equal(res, ref)

	# Selected columns
	res = Renderer.get_localization_colors(loc, "Intensity")
	ref = np.array([[1, 3, 10], [2, 4, 20]], dtype=np.float64)
	np.testing.assert_array_equal(res, ref)

	# With negatives values
	loc = pd.DataFrame({"X": [1, 2], "Y": [3, 4], "Intensity": [-2, 3]})
	res = Renderer.get_localization_colors(loc, "Intensity")
	ref = np.array([[1, 3, 0], [2, 4, 5]], dtype=np.float64)
	np.testing.assert_array_equal(res, ref)

	# With normalization
	loc = pd.DataFrame({"X": [1, 2], "Y": [3, 4], "Intensity": [2, 4]})
	res = Renderer.get_localization_colors(loc, "Intensity", max_value=100)
	ref = np.array([[1, 3, 50], [2, 4, 100], ], dtype=np.float64)
	np.testing.assert_allclose(res, ref)

	# With 0 in colors
	loc = pd.DataFrame({"X": [1, 2], "Y": [3, 4], "Intensity": [0, 0]})
	res = Renderer.get_localization_colors(loc, "Intensity")
	ref = np.array([[1, 3, 1], [2, 4, 1]], dtype=np.float64)
	np.testing.assert_array_equal(res, ref)


##################################################
def test_get_tracks_colors():
	r = Renderer()

	# Empty Dataframe
	trc = pd.DataFrame(columns=["Track", "Plane", "X", "Y", "Integrated Intensity"])
	res = Renderer.get_tracks_colors(trc, "Track Number")
	assert res.shape == (0, 5)

	# No Column selected (and sorting)
	trc = pd.DataFrame({"Track": [2, 1, 1], "Plane": [5, 6, 3], "X": [2, 0, 0], "Y": [2, 1, 0], "Integrated Intensity": [7, 6, 5]})
	res = Renderer.get_tracks_colors(trc)
	ref = np.array([[1, 3, 0, 0, 1], [1, 6, 0, 1, 1], [2, 5, 2, 2, 1]], dtype=np.float64)
	np.testing.assert_array_equal(res, ref)

	# Track number
	trc = pd.DataFrame({"Track": [1, 1, 2], "Plane": [5, 6, 3], "X": [0, 0, 2], "Y": [0, 1, 2], "Integrated Intensity": [7, 3, 5]})
	res = Renderer.get_tracks_colors(trc, "Track Number")
	ref = np.array([[1, 5, 0, 0, 1], [1, 6, 0, 1, 1], [2, 3, 2, 2, 2]], dtype=np.float64)
	np.testing.assert_array_equal(res, ref)

	# Plane
	res = Renderer.get_tracks_colors(trc, "Plane")
	ref = np.array([[1, 5, 0, 0, 5], [1, 6, 0, 1, 6], [2, 3, 2, 2, 3]], dtype=np.float64)
	np.testing.assert_array_equal(res, ref)

	# Intensity
	res = Renderer.get_tracks_colors(trc, "Intensity")
	ref = np.array([[1, 5, 0, 0, 10], [1, 6, 0, 1, 10], [2, 3, 2, 2, 5]], dtype=np.float64)
	np.testing.assert_array_equal(res, ref)

	# Length
	res = Renderer.get_tracks_colors(trc, "Length")
	ref = np.array([[1, 5, 0, 0, 1], [1, 6, 0, 1, 1], [2, 3, 2, 2, 0]], dtype=np.float64)
	np.testing.assert_array_equal(res, ref)

	# Duration
	res = Renderer.get_tracks_colors(trc, "Duration")
	ref = np.array([[1, 5, 0, 0, 2], [1, 6, 0, 1, 2], [2, 3, 2, 2, 1]], dtype=np.float64)
	np.testing.assert_array_equal(res, ref)

	# Normalization
	res = Renderer.get_tracks_colors(trc, "Intensity", max_value=100)
	ref = np.array([[1, 5, 0, 0, 100], [1, 6, 0, 1, 100], [2, 3, 2, 2, 50]], dtype=np.float64)
	np.testing.assert_array_equal(res, ref)

	# Negative and 0
	trc = pd.DataFrame({"Track": [1, 1, 2], "Plane": [5, 6, 3], "X": [0, 0, 2], "Y": [0, 1, 2], "Integrated Intensity": [-1, 0, -1]})
	res = Renderer.get_tracks_colors(trc, "Intensity")
	ref = np.array([[1, 5, 0, 0, 1], [1, 6, 0, 1, 1], [2, 3, 2, 2, 1]], dtype=np.float64)
	np.testing.assert_array_equal(res, ref)


##################################################
def test_draw_line():
	r = Renderer()
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

	# Clip
	loc = np.array([[1, 1, 70000], [1, 1, 1000]], dtype=np.float64)
	res = r.localizations(loc)
	assert res[2, 2] == np.iinfo(np.uint16).max


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
