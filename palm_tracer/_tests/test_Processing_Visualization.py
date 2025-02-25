""" Fichier des tests pour l'utilisation des DLL """
import os
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from palm_tracer.Processing import hr_visualization, plot_histogram
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
	save_png(visualization, f"{OUTPUT_DIR}/test_hr_visualization.png")
	assert visualization.shape == (SIZE * RATIO, SIZE * RATIO)


##################################################
def test_hr_visualization_bad_input():
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
	datas = rng.normal(loc=10, scale=5, size=(int(SIZE * np.sqrt(SIZE)), 1))
	# Ajouter des aberrations (bruit) aux points
	aberration = rng.uniform(-5, 5, datas.shape)
	datas += aberration

	fig, ax = plt.subplots()
	plot_histogram(ax, datas, "Histogram")
	fig.savefig(f"{OUTPUT_DIR}/test_plot_histogram.png", bbox_inches="tight")
	plt.close(fig)

	fig, ax = plt.subplots()
	plot_histogram(ax, datas, "Histogram", False, False)
	fig.savefig(f"{OUTPUT_DIR}/test_plot_histogram_without.png", bbox_inches="tight")
	plt.close(fig)
