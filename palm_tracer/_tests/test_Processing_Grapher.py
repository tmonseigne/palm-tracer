""" Fichier des tests pour le grapher. """
from pathlib import Path

import numpy as np
import pytest

from palm_tracer.Processing import Grapher

OUTPUT_DIR = Path(__file__).parent / "output"
rng = np.random.default_rng(42)  # Initialisation du générateur avec une seed
SIZE = 1000
POINTS = rng.normal(loc=0.0, scale=1.0, size=SIZE).astype(np.float32)


##################################################
def test_grapher_blank():
	g = Grapher()
	res = g.blank("blank")
	res.write_html(f"{OUTPUT_DIR}/grapher_blank.html", full_html=False)
	assert True


##################################################
def test_grapher_histogram():
	g = Grapher()
	res = g.histogram(np.empty(0), "Histogram 0")
	res.write_html(f"{OUTPUT_DIR}/grapher_Histogramm_0.html", full_html=False)
	res = g.histogram(POINTS, "Histogram 1", False, False, False, False, False, 20)
	res.write_html(f"{OUTPUT_DIR}/grapher_Histogramm_1.html", full_html=False)
	res = g.histogram(POINTS, "Histogram 2", True, True, True, True, True)
	res.write_html(f"{OUTPUT_DIR}/grapher_Histogramm_2.html", full_html=False)
	assert True


##################################################
def test_grapher_scatter():
	g = Grapher()
	res = g.scatter(np.empty(0), "scatter 0")
	res.write_html(f"{OUTPUT_DIR}/grapher_scatter_0.html", full_html=False)
	res = g.scatter(POINTS, "scatter 1")
	res.write_html(f"{OUTPUT_DIR}/grapher_scatter_1.html", full_html=False)

	idx = np.arange(1, SIZE + 1, dtype=POINTS.dtype)
	res = g.scatter(np.stack((idx, POINTS), axis=0), "scatter 2")
	res.write_html(f"{OUTPUT_DIR}/grapher_scatter_2.html", full_html=False)
	res = g.scatter(np.stack((idx, POINTS), axis=1), "scatter 3", True)
	res.write_html(f"{OUTPUT_DIR}/grapher_scatter_3.html", full_html=False)

	with pytest.raises(ValueError) as exception_info:
		g.scatter(np.zeros((3, 3)), "scatter fail")
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."

	with pytest.raises(ValueError) as exception_info:
		g.scatter(np.zeros((3, 3, 3)), "scatter fail")
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."

	assert True
