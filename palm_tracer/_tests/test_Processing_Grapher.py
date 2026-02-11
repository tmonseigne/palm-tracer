"""Fichier des tests pour le grapher."""
import json

import plotly.graph_objects as go
import pytest

from palm_tracer._tests.Utils import *
from palm_tracer.Processing import Grapher

SIZE = 1000
POINTS = rng.normal(loc=0.0, scale=1.0, size=SIZE).astype(np.float32)
IDX = np.arange(1, SIZE + 1, dtype=POINTS.dtype)

BLANK_FIG = json.loads((REF_DIR / "grapher_blank.json").read_text(encoding="utf-8"))


##################################################
def _save_output(res: go.Figure, path: Path):
	data = get_light_json(res.to_plotly_json())
	if save_output:
		res.write_html(path.with_suffix(".html"), full_html=False, include_plotlyjs="cdn")
		path.write_text(json.dumps(data, sort_keys=True, ensure_ascii=False, indent=2), encoding="utf-8")
	return data


##################################################
def test_get_fig():
	g = Grapher()

	res = g.get_fig("scatter")
	res = _save_output(res, OUTPUT_DIR / "grapher_get_fig_no_data.json")
	ref = json.loads((REF_DIR / "grapher_get_fig_blank.json").read_text(encoding="utf-8"))
	assert ref == res, f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	res = g.get_fig("scatter", POINTS)
	res = _save_output(res, OUTPUT_DIR / "grapher_get_fig_scat.json")
	ref = json.loads((REF_DIR / "grapher_get_fig_scat.json").read_text(encoding="utf-8"))
	assert ref == res, f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	res = g.get_fig("histogram", POINTS)
	res = _save_output(res, OUTPUT_DIR / "grapher_get_fig_hist.json")
	ref = json.loads((REF_DIR / "grapher_get_fig_hist.json").read_text(encoding="utf-8"))
	assert ref == res, f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	res = g.get_fig("", POINTS)
	res = _save_output(res, OUTPUT_DIR / "grapher_get_fig_blank.json")
	ref = json.loads((REF_DIR / "grapher_get_fig_blank.json").read_text(encoding="utf-8"))
	assert ref == res, f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"


##################################################
def test_blank():
	g = Grapher()
	res = g.blank("blank")
	res = _save_output(res, OUTPUT_DIR / "grapher_blank.json")
	assert BLANK_FIG == res, f"Résultat incorrect.\nAttendu : {BLANK_FIG}\nObtenu : {res}"


##################################################
def test_histogram():
	g = Grapher()
	# Entrée Vide
	res = g.histogram(np.empty(0), "blank")
	res = _save_output(res, OUTPUT_DIR / "grapher_Histogramm_0.json")
	assert BLANK_FIG == res, f"Résultat incorrect.\nAttendu : {BLANK_FIG}\nObtenu : {res}"

	# Entrée 1D sans aucune option à part les Bins fixés
	res = g.histogram(POINTS, "Histogram", "", "", False, False, False, False, False, 20)
	res = _save_output(res, OUTPUT_DIR / "grapher_Histogramm_1.json")
	ref = json.loads((REF_DIR / "grapher_Histogramm_1.json").read_text(encoding="utf-8"))
	assert ref == res, f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	# Entrée 1D avec toutes les options à True
	res = g.histogram(POINTS, "Histogram", "", "", True, True, True, True, True)
	res = _save_output(res, OUTPUT_DIR / "grapher_Histogramm_2.json")
	ref = json.loads((REF_DIR / "grapher_Histogramm_2.json").read_text(encoding="utf-8"))
	# Attention, le Calcul du KDE diffère entre les OS...
	if platform.system() == "Windows": assert ref == res, f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	# Entrée 2D
	res = g.histogram(np.stack((IDX, POINTS), axis=0), "Histogram", limit=True)
	res = _save_output(res, OUTPUT_DIR / "grapher_Histogramm_3.json")
	ref = json.loads((REF_DIR / "grapher_Histogramm_3.json").read_text(encoding="utf-8"))
	assert ref == res, f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	# Entrée 2D (transposé identique au précédent)
	res = g.histogram(np.stack((IDX, POINTS), axis=1), "Histogram", limit=True)
	res = _save_output(res, OUTPUT_DIR / "grapher_Histogramm_4.json")
	assert ref == res, f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	# Entrée 2D, mais avec plus de 2 lignes ou colonnes (il compacte tout)
	res = g.histogram(np.zeros((3, 3)), "Histogram")
	res = _save_output(res, OUTPUT_DIR / "grapher_Histogramm_5.json")
	ref = json.loads((REF_DIR / "grapher_Histogramm_5.json").read_text(encoding="utf-8"))
	assert ref == res, f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	# Entrée 3D (il compacte tout)
	res = g.histogram(np.zeros((3, 3, 3)), "Histogram")
	res = _save_output(res, OUTPUT_DIR / "grapher_Histogramm_6.json")
	ref = json.loads((REF_DIR / "grapher_Histogramm_6.json").read_text(encoding="utf-8"))
	assert ref == res, f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"


##################################################
def test_scatter():
	g = Grapher()
	# Entrée Vide
	res = g.scatter(np.empty(0), "blank")
	res = _save_output(res, OUTPUT_DIR / "grapher_scatter_0.json")
	assert BLANK_FIG == res, f"Résultat incorrect.\nAttendu : {BLANK_FIG}\nObtenu : {res}"

	# Entrée 1D
	res = g.scatter(POINTS, "scatter")
	res = _save_output(res, OUTPUT_DIR / "grapher_scatter_1.json")
	ref = json.loads((REF_DIR / "grapher_scatter_1.json").read_text(encoding="utf-8"))
	assert ref == res, f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	# Entrée 2D
	res = g.scatter(np.stack((IDX, POINTS), axis=0), "scatter")
	res = _save_output(res, OUTPUT_DIR / "grapher_scatter_2.json")
	ref = json.loads((REF_DIR / "grapher_scatter_2.json").read_text(encoding="utf-8"))
	assert ref == res, f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	# Entrée 2D (transposé) avec limitation
	res = g.scatter(np.stack((IDX, POINTS), axis=1), "scatter", limit=True)
	res = _save_output(res, OUTPUT_DIR / "grapher_scatter_3.json")
	ref = json.loads((REF_DIR / "grapher_scatter_3.json").read_text(encoding="utf-8"))
	assert ref == res, f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	# Entrée 2D (transposé) avec affichage des mu et sigma
	res = g.scatter(np.stack((IDX, POINTS), axis=1), "scatter", show_sigma=True)
	res = _save_output(res, OUTPUT_DIR / "grapher_scatter_4.json")
	ref = json.loads((REF_DIR / "grapher_scatter_4.json").read_text(encoding="utf-8"))
	assert ref == res, f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	# Entrée 2D, mais avec plus de 2 lignes ou colonnes
	with pytest.raises(ValueError) as exception_info: g.scatter(np.zeros((3, 3)), "scatter fail")
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."

	# Entrée 3D
	with pytest.raises(ValueError) as exception_info: g.scatter(np.zeros((3, 3, 3)), "scatter fail")
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."


##################################################
def test_astigmatism3d_curve():
	g = Grapher()
	# Entrée invalide
	with pytest.raises(ValueError) as exception_info: g.astigmatism3d_curve(np.zeros((3, 3)), "blank")
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."

	# Entrée valide
	model = np.array([[-100, 100, 0, 0, 30], [100, 100, 0, 0, 30]], dtype=np.float64)
	res = g.astigmatism3d_curve(model, "Astigmatism 3D", pixel_size=100, z_max=100, n_points=100)
	res = _save_output(res, OUTPUT_DIR / "grapher_astigmatism3d.json")
	ref = json.loads((REF_DIR / "grapher_astigmatism3d.json").read_text(encoding="utf-8"))
	assert ref == res, f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"
