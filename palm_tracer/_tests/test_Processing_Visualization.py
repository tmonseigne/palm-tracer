""" Fichier des tests pour l'utilisation des DLL """
import os
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from palm_tracer.Processing import hr_visualization, plot_histogram, plot_plane_heatmap, plot_plane_violin
from palm_tracer.Tools.FileIO import save_png

matplotlib.use("Agg")  # Désactive le backend interactif

INPUT_DIR = Path(__file__).parent / "input"
OUTPUT_DIR = Path(__file__).parent / "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)

SIZE, RATIO = 100, 10
rng = np.random.default_rng(42)  # Initialisation du générateur avec une seed
POINTS = rng.uniform(1, SIZE - 1, size=(int(SIZE * np.sqrt(SIZE)), 3))


##################################################
def test_hr_visualization():
	"""Test de la visualisation de l'image en HR."""
	visualization = hr_visualization(SIZE, SIZE, RATIO, POINTS)
	save_png(visualization, f"{OUTPUT_DIR}/test_hr_visualization_normalized.png")
	assert visualization.shape == (SIZE * RATIO, SIZE * RATIO)

	visualization = hr_visualization(SIZE, SIZE, RATIO, POINTS, False)
	save_png(visualization, f"{OUTPUT_DIR}/test_hr_visualization.png")
	assert visualization.shape == (SIZE * RATIO, SIZE * RATIO)


##################################################
def test_hr_visualization_bad_input():
	""" Test de la visualisation de l'image en HR avec une mauvaise entrée. """
	visualization = hr_visualization(SIZE, SIZE, 1, POINTS)
	assert visualization.shape == (SIZE, SIZE)
	assert np.all(visualization == 0)

	visualization = hr_visualization(0, SIZE, RATIO, POINTS)
	assert visualization.shape == (1, SIZE * RATIO)
	assert np.all(visualization == 0)

	visualization = hr_visualization(SIZE, SIZE, RATIO, np.zeros((2, 2)))
	assert visualization.shape == (SIZE * RATIO, SIZE * RATIO)
	assert np.all(visualization == 0)


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
