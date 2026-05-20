"""Fichier des tests pour le grapher."""
import json
import platform

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
	res = _save_output(res, OUTPUT_DIR / "grapher_Histogram_0.json")
	assert BLANK_FIG == res, f"Résultat incorrect.\nAttendu : {BLANK_FIG}\nObtenu : {res}"

	# Entrée 1D sans aucune option à part les Bins fixés
	res = g.histogram(POINTS, "Histogram", "", "", False, False, False, False, False, bins=20)
	res = _save_output(res, OUTPUT_DIR / "grapher_Histogram_1.json")
	ref = json.loads((REF_DIR / "grapher_Histogram_1.json").read_text(encoding="utf-8"))
	assert ref == res, f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	# Entrée 1D avec toutes les options à True
	res = g.histogram(POINTS, "Histogram", "", "", True, True, True, True, True, True)
	res = _save_output(res, OUTPUT_DIR / "grapher_Histogram_2.json")
	ref = json.loads((REF_DIR / "grapher_Histogram_2.json").read_text(encoding="utf-8"))
	# Attention, le Calcul du KDE diffère entre les OS...
	if platform.system() == "Windows": assert ref == res, f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	# Entrée 1D avec gaussienne densité et non cumulatif
	res = g.histogram(POINTS, "Histogram", "", "", gaussian=True)
	res = _save_output(res, OUTPUT_DIR / "grapher_Histogram_3.json")
	# ref = json.loads((REF_DIR / "grapher_Histogram_3.json").read_text(encoding="utf-8"))
	# assert ref == res, f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	# Entrée 2D
	res = g.histogram(np.stack((IDX, POINTS), axis=0), "Histogram", limit=True)
	res = _save_output(res, OUTPUT_DIR / "grapher_Histogram_4.json")
	ref = json.loads((REF_DIR / "grapher_Histogram_4.json").read_text(encoding="utf-8"))
	assert ref == res, f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	# Entrée 2D (transposé identique au précédent)
	res = g.histogram(np.stack((IDX, POINTS), axis=1), "Histogram", limit=True)
	res = _save_output(res, OUTPUT_DIR / "grapher_Histogram_4b.json")
	assert ref == res, f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	# Entrée 2D, mais avec plus de 2 lignes ou colonnes (il compacte tout)
	res = g.histogram(np.zeros((3, 3)), "Histogram")
	res = _save_output(res, OUTPUT_DIR / "grapher_Histogram_5.json")
	ref = json.loads((REF_DIR / "grapher_Histogram_5.json").read_text(encoding="utf-8"))
	assert ref == res, f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	# Entrée 3D (il compacte tout)
	res = g.histogram(np.zeros((3, 3, 3)), "Histogram")
	res = _save_output(res, OUTPUT_DIR / "grapher_Histogram_6.json")
	ref = json.loads((REF_DIR / "grapher_Histogram_6.json").read_text(encoding="utf-8"))
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
def test_cloud():
	g = Grapher()
	# Entrée Vide
	res = g.cloud(np.empty(0), "blank")
	res = _save_output(res, OUTPUT_DIR / "grapher_cloud_0.json")
	assert BLANK_FIG == res, f"Résultat incorrect.\nAttendu : {BLANK_FIG}\nObtenu : {res}"

	res = g.cloud(np.zeros((2, 2)) + np.inf, "blank")
	res = _save_output(res, OUTPUT_DIR / "grapher_cloud_1.json")
	assert BLANK_FIG == res, f"Résultat incorrect.\nAttendu : {BLANK_FIG}\nObtenu : {res}"

	# Entrée 2D
	res = g.cloud(np.stack((IDX, POINTS), axis=0), "cloud")
	res = _save_output(res, OUTPUT_DIR / "grapher_cloud_2.json")
	ref = json.loads((REF_DIR / "grapher_cloud_2.json").read_text(encoding="utf-8"))
	assert ref == res, f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	# Entrée 2D (transposé) avec limitation
	res = g.cloud(np.stack((IDX, POINTS), axis=1), "cloud", limit=True)
	res = _save_output(res, OUTPUT_DIR / "grapher_cloud_3.json")
	ref = json.loads((REF_DIR / "grapher_cloud_3.json").read_text(encoding="utf-8"))
	assert ref == res, f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	# Entrée 2D (transposé) avec affichage des mu et sigma
	res = g.cloud(np.stack((IDX, POINTS), axis=1), "cloud", show_sigma=True, kde=True, gaussian=True)
	res = _save_output(res, OUTPUT_DIR / "grapher_cloud_4.json")
	# Map complexe et suivant la version de python et l'OS les résultats peuvent légèrement différer
	# ref = json.loads((REF_DIR / "grapher_cloud_4.json").read_text(encoding="utf-8"))
	# assert ref == res, f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	# Entrée 2D avec des données constantes
	res = g.cloud(np.ones((2, 2)), "cloud", show_sigma=True, kde=True, gaussian=True)
	res = _save_output(res, OUTPUT_DIR / "grapher_cloud_5.json")
	ref = json.loads((REF_DIR / "grapher_cloud_5.json").read_text(encoding="utf-8"))
	assert ref == res, f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	# Entrée 1D
	with pytest.raises(ValueError) as exception_info: g.cloud(np.zeros(3), "cloud fail")
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."

	# Entrée 2D, mais avec plus de 2 lignes ou colonnes
	with pytest.raises(ValueError) as exception_info: g.cloud(np.zeros((3, 3)), "cloud fail")
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."

	# Entrée 3D
	with pytest.raises(ValueError) as exception_info: g.cloud(np.zeros((3, 3, 3)), "cloud fail")
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."


##################################################
def test_astigmatism3d():
	g = Grapher()
	# Entrée invalide
	with pytest.raises(ValueError) as exception_info: g.astigmatism3d(np.zeros((3, 3)), "blank")
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."

	# Entrée valide
	model = np.array([[-100, 100, 0, 0, 30], [100, 100, 0, 0, 30]], dtype=np.float64)
	data = np.array([[0, 0, 0]], dtype=np.float64)

	# Courbe simple
	res = g.astigmatism3d(model, None, "Astigmatism 3D", pixel_size=100, z_max=100, mode="curve", n_points=100)
	res = _save_output(res, OUTPUT_DIR / "grapher_astigmatism3d_curve.json")
	ref = json.loads((REF_DIR / "grapher_astigmatism3d_curve.json").read_text(encoding="utf-8"))
	assert ref == res, f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	# Courbe Cross sans data
	res = g.astigmatism3d(model, None, "Astigmatism 3D", pixel_size=100, z_max=100, mode="cross", n_points=100)
	res = _save_output(res, OUTPUT_DIR / "grapher_astigmatism3d_cross_1.json")
	ref = json.loads((REF_DIR / "grapher_astigmatism3d_cross_1.json").read_text(encoding="utf-8"))
	# Courbe Cross avec data
	res = g.astigmatism3d(model, data, "Astigmatism 3D", pixel_size=100, z_max=100, mode="cross", n_points=100)
	res = _save_output(res, OUTPUT_DIR / "grapher_astigmatism3d_cross_2.json")
	ref = json.loads((REF_DIR / "grapher_astigmatism3d_cross_2.json").read_text(encoding="utf-8"))
	# Courbe Slope sans data
	res = g.astigmatism3d(model, None, "Astigmatism 3D", pixel_size=100, z_max=100, mode="slope", n_points=100)
	res = _save_output(res, OUTPUT_DIR / "grapher_astigmatism3d_slope_1.json")
	ref = json.loads((REF_DIR / "grapher_astigmatism3d_slope_1.json").read_text(encoding="utf-8"))
	# Courbe Slope avec data
	res = g.astigmatism3d(model, data, "Astigmatism 3D", pixel_size=100, z_max=100, mode="slope", n_points=100)
	res = _save_output(res, OUTPUT_DIR / "grapher_astigmatism3d_slope_2.json")
	ref = json.loads((REF_DIR / "grapher_astigmatism3d_slope_2.json").read_text(encoding="utf-8"))

	# Courbe un mauvais mode (mais l'IDE averti qu'il y a un problème)
	res = g.astigmatism3d(model, data, "Astigmatism 3D", pixel_size=100, z_max=100, mode="any", n_points=100)
	res = _save_output(res, OUTPUT_DIR / "grapher_astigmatism3d_bad.json")
	ref = json.loads((REF_DIR / "grapher_astigmatism3d_bad.json").read_text(encoding="utf-8"))
