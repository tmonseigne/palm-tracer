""" Fichier des tests pour le grapher. """
from pathlib import Path

import numpy as np
import pytest

from palm_tracer.Processing import Grapher

OUTPUT_DIR = Path(__file__).parent / "output"
rng = np.random.default_rng(42)  # Initialisation du générateur avec une seed
SIZE = 1000
POINTS = rng.normal(loc=0.0, scale=1.0, size=SIZE).astype(np.float32)
IDX = np.arange(1, SIZE + 1, dtype=POINTS.dtype)


##################################################
def test_get_fig():
	g = Grapher()
	res = g.get_fig("scatter")
	res.write_html(f"{OUTPUT_DIR}/grapher_get_fig_no_data.html", full_html=False)
	res = g.get_fig("scatter", POINTS)
	res.write_html(f"{OUTPUT_DIR}/grapher_get_fig_scat.html", full_html=False)
	res = g.get_fig("histogram", POINTS)
	res.write_html(f"{OUTPUT_DIR}/grapher_get_fig_hist.html", full_html=False)
	res = g.get_fig("", POINTS)
	res.write_html(f"{OUTPUT_DIR}/grapher_get_fig_blank.html", full_html=False)


##################################################
def test_blank():
	g = Grapher()
	res = g.blank("blank")
	res.write_html(f"{OUTPUT_DIR}/grapher_blank.html", full_html=False, include_plotlyjs="cdn")


##################################################
def test_histogram():
	g = Grapher()
	# Entrée Vide
	res = g.histogram(np.empty(0), "Histogram 0")
	res.write_html(f"{OUTPUT_DIR}/grapher_Histogramm_0.html", full_html=False)

	# Entrée 1D sans aucune option à part les Bins fixés
	res = g.histogram(POINTS, "Histogram 1", "", "", False, False, False, False, False, 20)
	res.write_html(f"{OUTPUT_DIR}/grapher_Histogramm_1.html", full_html=False)

	# Entrée 1D avec toutes les options à True
	res = g.histogram(POINTS, "Histogram 2", "", "", True, True, True, True, True)
	res.write_html(f"{OUTPUT_DIR}/grapher_Histogramm_2.html", full_html=False)

	# Entrée 2D
	res = g.histogram(np.stack((IDX, POINTS), axis=0), "Histogram 3", limit=True)
	res.write_html(f"{OUTPUT_DIR}/grapher_Histogramm_3.html", full_html=False)

	# Entrée 2D (transposé)
	res = g.histogram(np.stack((IDX, POINTS), axis=1), "Histogram 4", limit=True)
	res.write_html(f"{OUTPUT_DIR}/grapher_Histogramm_4.html", full_html=False)

	# Entrée 2D mais avec plus de 2 lignes ou colonnes (il compacte tout)
	res = g.histogram(np.zeros((3, 3)), "Histogram 5")
	res.write_html(f"{OUTPUT_DIR}/grapher_Histogramm_5.html", full_html=False)

	# Entrée 3D (il compacte tout)
	res = g.histogram(np.zeros((3, 3, 3)), "Histogram 6")
	res.write_html(f"{OUTPUT_DIR}/grapher_Histogramm_6.html", full_html=False)


##################################################
def test_scatter():
	g = Grapher()
	# Entrée Vide
	res = g.scatter(np.empty(0), "scatter 0")
	res.write_html(f"{OUTPUT_DIR}/grapher_scatter_0.html", full_html=False)

	# Entrée 1D
	res = g.scatter(POINTS, "scatter 1")
	res.write_html(f"{OUTPUT_DIR}/grapher_scatter_1.html", full_html=False)

	# Entrée 2D
	res = g.scatter(np.stack((IDX, POINTS), axis=0), "scatter 2")
	res.write_html(f"{OUTPUT_DIR}/grapher_scatter_2.html", full_html=False)

	# Entrée 2D (transposé) avec limitation
	res = g.scatter(np.stack((IDX, POINTS), axis=1), "scatter 3", limit=True)
	res.write_html(f"{OUTPUT_DIR}/grapher_scatter_3.html", full_html=False)

	# Entrée 2D (transposé) avec affichage des mu et sigma
	res = g.scatter(np.stack((IDX, POINTS), axis=1), "scatter 4", show_sigma=True)
	res.write_html(f"{OUTPUT_DIR}/grapher_scatter_4.html", full_html=False)

	# Entrée 2D mais avec plus de 2 lignes ou colonnes
	with pytest.raises(ValueError) as exception_info: g.scatter(np.zeros((3, 3)), "scatter fail")
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."

	# Entrée 3D
	with pytest.raises(ValueError) as exception_info: g.scatter(np.zeros((3, 3, 3)), "scatter fail")
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."
