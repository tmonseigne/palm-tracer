""" Fichier des tests pour les fonctions de visualisation. """
import os
from pathlib import Path

import matplotlib

from palm_tracer.Processing.Visualization import *
from palm_tracer.Tools.FileIO import save_png

matplotlib.use("Agg")  # Désactive le backend interactif

INPUT_DIR = Path(__file__).parent / "input"
OUTPUT_DIR = Path(__file__).parent / "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)

SIZE_X, SIZE_Y, INTENSITY, RATIO = 100, 50, 1000, 10
rng = np.random.default_rng(42)			# Initialisation du générateur avec une seed
SIZE = int(SIZE_X * np.sqrt(SIZE_Y))
POINTS = np.stack([rng.uniform(1, SIZE_X - 1, size=SIZE), rng.uniform(1, SIZE_Y - 1, size=SIZE), rng.uniform(0, INTENSITY, size=SIZE)], axis=1)


##################################################
def test_normalize_data():
	"""Test de la normalisation de données."""
	data = np.array([])  # Cas 0 liste vide
	res = normalize_data(data, scale=1)

	data = np.array([-1, -1, -1])  # Cas 1 colonne uniforme
	res = normalize_data(data, scale=1)
	assert np.array_equal(res, np.array([1, 1, 1])), "Normalisation incorrecte"

	data = np.array([0.1, 0.5, 1.0])  # Cas 2 [0:1]
	res = normalize_data(data, scale=1)
	assert np.array_equal(res, np.array([0.1, 0.5, 1.0])), "Normalisation incorrecte"

	data = np.array([-2, 0, 2])  # Cas 3 [négatif:positif] -> [0:4]
	res = normalize_data(data, scale=4)
	assert np.array_equal(res, np.array([0, 2, 4])), "Normalisation incorrecte"

	data = np.array([-3, 0, 3])  # Cas 3 [négatif:positif] -> [0:8]
	res = normalize_data(data, scale=8)
	assert np.array_equal(res, np.array([1, 4, 7])), "Normalisation incorrecte"

	data = np.array([500, 750, 1000])  # Cas 4 [x:y] -> [0:1024]
	res = normalize_data(data, scale=1024)
	assert np.array_equal(res, np.array([500, 750, 1000])), "Normalisation incorrecte"


##################################################
def test_render_hr_image():
	"""Test de la visualisation de l'image en HR."""
	visualization = render_hr_image(SIZE_X, SIZE_Y, RATIO, POINTS)
	save_png(visualization, f"{OUTPUT_DIR}/test_render_hr_image_normalized.png")
	assert visualization.shape == (SIZE_Y * RATIO, SIZE_X * RATIO)

	visualization = render_hr_image(SIZE_X, SIZE_Y, RATIO, POINTS, False)
	save_png(visualization, f"{OUTPUT_DIR}/test_render_hr_image.png")
	assert visualization.shape == (SIZE_Y * RATIO, SIZE_X * RATIO)


##################################################
def test_render_hr_image_bad_input():
	""" Test de la visualisation de l'image en HR avec une mauvaise entrée. """
	visualization = render_hr_image(SIZE_X, SIZE_Y, 0, POINTS)
	assert visualization.shape == (SIZE_Y, SIZE_X)
	assert np.all(visualization == 0)

	visualization = render_hr_image(0, SIZE_Y, RATIO, POINTS)
	assert visualization.shape == (SIZE_Y * RATIO, 1)
	assert np.all(visualization == 0)

	visualization = render_hr_image(SIZE_X, SIZE_Y, RATIO, np.zeros((2, 2)))
	assert visualization.shape == (SIZE_Y * RATIO, SIZE_X * RATIO)
	assert np.all(visualization == 0)


##################################################
def test_render_roi():
	"""Test de la visualisation de des ROI sur une image."""
	visualization = render_hr_image(SIZE_X, SIZE_Y, RATIO, POINTS)
	roi = render_roi(visualization, POINTS[:, :2] * RATIO, 7, [0, 255, 0])
	save_png(roi, f"{OUTPUT_DIR}/test_render_roi.png")
	assert roi.shape == (SIZE_Y * RATIO, SIZE_X * RATIO, 3)
	roi = render_roi(np.zeros_like(visualization), POINTS * RATIO, 7, [0, 255, 0])
	save_png(roi, f"{OUTPUT_DIR}/test_render_roi_bad_input.png")


##################################################
def test_render_roi_bad_input():
	roi = render_roi(np.zeros((SIZE_Y, SIZE_X)), POINTS * RATIO, 7, [0, 255, 0])
	save_png(roi, f"{OUTPUT_DIR}/test_render_roi_bad_input.png")


##################################################
def test_plot_histogram():
	""" Test de la visualisation du histogramme. """
	datas = rng.normal(loc=10, scale=5, size=(int(SIZE * np.sqrt(SIZE)), 1))
	# Ajouter des aberrations (bruit) aux points
	aberration = rng.uniform(-5, 5, datas.shape)
	datas += aberration

	fig, ax = plt.subplots()
	plot_histogram(ax, datas, "Histogram")
	fig.savefig(f"{OUTPUT_DIR}/test_plot_histogram.png", bbox_inches="tight")
	plt.close(fig)

	fig, ax = plt.subplots()
	plot_histogram(ax, datas, "Histogram", False, False, False)
	fig.savefig(f"{OUTPUT_DIR}/test_plot_histogram_without.png", bbox_inches="tight")
	plt.close(fig)

	fig, ax = plt.subplots()
	plot_histogram(ax, datas, "Histogram", True, True, False)
	fig.savefig(f"{OUTPUT_DIR}/test_plot_histogram_count_kde.png", bbox_inches="tight")
	plt.close(fig)


##################################################
def test_plot_histogram_bad_input():
	""" Test de la visualisation du histogramme avec une mauvaise entrée. """
	fig, ax = plt.subplots()
	plot_histogram(ax, np.zeros((2, 2)), "Histogram")
	fig.savefig(f"{OUTPUT_DIR}/test_plot_histogram_bad_input_constant_datas.png", bbox_inches="tight")
	plt.close(fig)

	fig, ax = plt.subplots()
	plot_histogram(ax, np.zeros((0, 0)), "Histogram")
	fig.savefig(f"{OUTPUT_DIR}/test_plot_histogram_bad_input_no_datas.png", bbox_inches="tight")
	plt.close(fig)


##################################################
def test_plot_violin():
	""" Test de la visualisation des violons. """
	datas = np.hstack((rng.integers(0, 10, size=(100000, 1)), rng.normal(loc=10, scale=5, size=(100000, 1))))
	fig, ax = plt.subplots()
	plot_plane_violin(ax, datas, "Violin")
	fig.savefig(f"{OUTPUT_DIR}/test_plot_violin.png", bbox_inches="tight")
	plt.close(fig)


##################################################
def test_plot_violin_bad_input():
	""" Test de la visualisation des violons avec une mauvaise entrée. """
	fig, ax = plt.subplots()
	plot_plane_violin(ax, np.zeros((0, 0)), "Violin")
	fig.savefig(f"{OUTPUT_DIR}/test_plot_violin_no_datas.png", bbox_inches="tight")
	plt.close(fig)


##################################################
def test_plot_heatmap():
	""" Test de la visualisation des Heat map. """
	datas = np.hstack((rng.integers(0, 1000, size=(100000, 1)), rng.normal(loc=10, scale=5, size=(100000, 1))))
	fig, ax = plt.subplots()
	plot_plane_heatmap(ax, datas, "Heat Map")
	fig.savefig(f"{OUTPUT_DIR}/test_plot_heatmap.png", bbox_inches="tight")
	plt.close(fig)

	fig, ax = plt.subplots()
	plot_plane_heatmap(ax, datas, "Heat Map", "plasma")
	fig.savefig(f"{OUTPUT_DIR}/test_plot_heatmap_plasma.png", bbox_inches="tight")
	plt.close(fig)


##################################################
def test_plot_heatmap_bad_input():
	""" Test de la visualisation des Heat map. """
	fig, ax = plt.subplots()
	plot_plane_heatmap(ax, np.zeros((0, 0)), "Heat Map")
	fig.savefig(f"{OUTPUT_DIR}/test_plot_heatmap_no_datas.png", bbox_inches="tight")
	plt.close(fig)
