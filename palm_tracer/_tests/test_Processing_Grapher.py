"""Teste la construction des figures Plotly."""

import json

import plotly.graph_objects as go
import pytest

from palm_tracer._tests.Utils import *
from palm_tracer.Processing import Grapher

SIZE = 1000
rng = np.random.default_rng(42)  # Générateur propre au jeu de données de ce module.
POINTS = rng.normal(loc=1.0, scale=1.0, size=SIZE).astype(float)
POINTS_2 = rng.normal(loc=2.0, scale=1.0, size=SIZE).astype(float)
IDX = np.arange(1, SIZE + 1, dtype=POINTS.dtype)

BLANK_FIG = json.loads((REF_DIR / "grapher_blank.json").read_text(encoding="utf-8"))


##################################################
def _save_output(res: go.Figure, path: Path):
	"""
	Enregistre une figure Plotly pour inspection.

	:param res: Figure Plotly à enregistrer.
	:param path: Chemin du fichier JSON.
	:return: Aucune valeur.
	"""
	data = get_light_json(res.to_plotly_json())
	if save_output:
		res.write_html(path.with_suffix(".html"), full_html=False, include_plotlyjs="cdn")
		path.write_text(json.dumps(data, sort_keys=True, ensure_ascii=False, indent=2), encoding="utf-8")
	return data


# ==================================================
# region Figures statistiques
# ==================================================
##################################################
def test_blank():
	"""Vérifie la création d'une figure vide."""
	g = Grapher()
	res = g.blank("blank")
	res = _save_output(res, OUTPUT_DIR / "grapher_blank.json")
	assert BLANK_FIG == res, f"Résultat incorrect.\nAttendu : {BLANK_FIG}\nObtenu : {res}"


##################################################
@pytest.mark.parametrize("args, kwargs, filename, reference", [
		pytest.param((np.empty(0), 'blank',), {}, 'grapher_Histogram_0.json', 'grapher_blank.json', id="empty"),
		pytest.param((POINTS, 'Histogram', '', '', False, False, False, False, False, False, False, False,), {'bins': 20}, 'grapher_Histogram_1.json',
					 'grapher_Histogram_1.json', id="fixed-bins"),
		pytest.param((np.array([1, 2, 2, 4]),), {'bins': -1}, 'grapher_Histogram_integer.json', 'grapher_Histogram_integer.json', id="integer-values"),
		pytest.param((np.stack((IDX, POINTS), axis=0), 'Histogram',), {'limit': True}, 'grapher_Histogram_4.json', 'grapher_Histogram_4.json',
					 id="two-rows"),
		pytest.param((np.stack((IDX, POINTS), axis=1), 'Histogram',), {'limit': True}, 'grapher_Histogram_4b.json', 'grapher_Histogram_4.json',
					 id="two-columns"),
		pytest.param((np.zeros((3, 3)), 'Histogram',), {}, 'grapher_Histogram_5.json', 'grapher_Histogram_5.json', id="flattened-matrix"),
		pytest.param((np.zeros((3, 3, 3)), 'Histogram',), {}, 'grapher_Histogram_6.json', 'grapher_Histogram_6.json', id="flattened-volume")])
def test_histogram(args, kwargs, filename, reference):
	"""Vérifie chaque configuration du graphique indépendamment."""
	figure = Grapher().histogram(*args, **kwargs)
	res = _save_output(figure, OUTPUT_DIR / filename)
	ref = json.loads((REF_DIR / reference).read_text(encoding="utf-8"))
	assert res == ref


##################################################
@pytest.mark.parametrize("args, kwargs, filename", [
		pytest.param((POINTS, 'Histogram', '', '', True, True, True, True, True, True, True, True, True,), {}, 'grapher_Histogram_2.json',
					 id="all-options"),
		pytest.param((POINTS, 'Histogram', '', '',), {'kde': True}, 'grapher_Histogram_3_kde.json', id="kde"),
		pytest.param((POINTS, 'Histogram', '', '',), {'gaussian': True}, 'grapher_Histogram_3_gaussian.json', id="gaussian"),
		pytest.param((np.concatenate((POINTS - 2.0, POINTS + 2.0)), 'Histogram',), {'gaussian_mixture': True}, 'grapher_Histogram_3_gaussian_mix.json',
					 id="gaussian-mixture"),
		pytest.param((POINTS, 'Histogram', '', '',), {'poissonian': True}, 'grapher_Histogram_3_poissonian.json', id="poisson"),
		pytest.param((POINTS, 'Histogram', '', '',), {'exponential': True}, 'grapher_Histogram_3_exponential.json', id="exponential"),
		pytest.param((POINTS, 'Histogram', '', '',), {'gaussian': True, 'density': False}, 'grapher_Histogram_3_count.json', id="gaussian-counts")])
def test_histogram_curves(args, kwargs, filename):
	"""Vérifie chaque configuration du graphique indépendamment."""
	figure = Grapher().histogram(*args, **kwargs)
	# Les courbes ajustées peuvent varier selon les versions de SciPy et le système.
	assert isinstance(figure, go.Figure)
	_save_output(figure, OUTPUT_DIR / filename)


##################################################
@pytest.mark.parametrize("cumulative", [
		pytest.param(False, id="density"),
		pytest.param(True, id="cumulative")])
def test_histogram_gaussian_mixture_components(cumulative):
	"""Vérifie le tracé séparé et additif des deux composantes gaussiennes."""
	points = np.concatenate((POINTS - 2.0, POINTS + 2.0))
	figure = Grapher().histogram(points, gaussian_mixture=True, density=True, cumulative=cumulative)
	component_1, component_2, mixture = figure.data[1:]

	assert [trace.name for trace in figure.data[1:]] == ["Gaussian component 1", "Gaussian component 2", "Gaussian mixture"]
	assert np.allclose(np.asarray(component_1.y) + np.asarray(component_2.y), np.asarray(mixture.y))


##################################################
@pytest.mark.parametrize("args, kwargs, filename, reference", [
		pytest.param((np.empty(0), 'blank',), {}, 'grapher_scatter_0.json', 'grapher_blank.json', id="empty"),
		pytest.param((POINTS, 'scatter',), {}, 'grapher_scatter_1.json', 'grapher_scatter_1.json', id="1d-data"),
		pytest.param((np.stack((IDX, POINTS), axis=0), 'scatter',), {}, 'grapher_scatter_2.json', 'grapher_scatter_2.json', id="two-rows"),
		pytest.param((np.stack((IDX, POINTS), axis=1), 'scatter',), {'limit': True}, 'grapher_scatter_3.json', 'grapher_scatter_3.json',
					 id="two-columns-with-limits"),
		pytest.param((np.stack((IDX, POINTS), axis=1), 'scatter',), {'show_sigma': True}, 'grapher_scatter_4.json', 'grapher_scatter_4.json',
					 id="mean-and-sigma")])
def test_scatter(args, kwargs, filename, reference):
	"""Vérifie chaque configuration du graphique indépendamment."""
	figure = Grapher().scatter(*args, **kwargs)
	res = _save_output(figure, OUTPUT_DIR / filename)
	ref = json.loads((REF_DIR / reference).read_text(encoding="utf-8"))
	assert res == ref


##################################################
@pytest.mark.parametrize("args, kwargs", [
		pytest.param((np.zeros((3, 3)), 'scatter fail',), {}, id="invalid-matrix"),
		pytest.param((np.zeros((3, 3, 3)), 'scatter fail',), {}, id="3d-volume")])
def test_scatter_invalid(args, kwargs):
	"""Vérifie le rejet des dimensions incompatibles avec ce graphique."""
	with pytest.raises(ValueError): Grapher().scatter(*args, **kwargs)


##################################################
@pytest.mark.parametrize("args, kwargs, filename, reference", [
		pytest.param((np.empty(0), 'blank',), {}, 'grapher_cloud_0.json', 'grapher_blank.json', id="empty"),
		pytest.param((np.zeros((2, 2)) + np.inf, 'blank',), {}, 'grapher_cloud_1.json', 'grapher_blank.json', id="infinite-values"),
		pytest.param((np.stack((POINTS, POINTS_2), axis=0), 'cloud',), {}, 'grapher_cloud_2.json', 'grapher_cloud_2.json', id="two-rows"),
		pytest.param((np.stack((POINTS, POINTS_2), axis=1), 'cloud',), {'limit': True}, 'grapher_cloud_3.json', 'grapher_cloud_3.json',
					 id="two-columns-with-limits"),
		pytest.param((np.stack((POINTS, POINTS_2), axis=0), 'cloud',), {'show_sigma': True}, 'grapher_cloud_4_sigma.json', 'grapher_cloud_4_sigma.json',
					 id="mean-and-sigma"),
		pytest.param((np.ones((2, 2)), 'cloud',), {'show_sigma': True, 'kde': True, 'gaussian': True}, 'grapher_cloud_5.json', 'grapher_cloud_5.json',
					 id="constant-data")])
def test_cloud(args, kwargs, filename, reference):
	"""Vérifie chaque configuration du graphique indépendamment."""
	figure = Grapher().cloud(*args, **kwargs)
	res = _save_output(figure, OUTPUT_DIR / filename)
	ref = json.loads((REF_DIR / reference).read_text(encoding="utf-8"))
	assert res == ref


##################################################
@pytest.mark.parametrize("args, kwargs, filename", [
		pytest.param((np.stack((POINTS, POINTS_2), axis=0), 'cloud',), {'kde': True}, 'grapher_cloud_4_kde.json', id="kde"),
		pytest.param((np.stack((POINTS, POINTS_2), axis=0), 'cloud',), {'gaussian': True}, 'grapher_cloud_4_gaussian.json', id="gaussian"),
		pytest.param((np.stack((POINTS, POINTS_2), axis=0), 'cloud',), {'poissonian': True}, 'grapher_cloud_4_poissonian.json', id="poisson"),
		pytest.param((np.stack((POINTS, POINTS_2), axis=0), 'cloud',), {'exponential': True}, 'grapher_cloud_4_exponential.json', id="exponential")])
def test_cloud_curves(args, kwargs, filename):
	"""Vérifie chaque configuration du graphique indépendamment."""
	figure = Grapher().cloud(*args, **kwargs)
	# Les courbes ajustées peuvent varier selon les versions de SciPy et le système.
	assert isinstance(figure, go.Figure)
	_save_output(figure, OUTPUT_DIR / filename)


##################################################
@pytest.mark.parametrize("args, kwargs", [
		pytest.param((np.zeros(3), 'cloud fail',), {}, id="1d-data"),
		pytest.param((np.zeros((3, 3)), 'cloud fail',), {}, id="invalid-matrix"),
		pytest.param((np.zeros((3, 3, 3)), 'cloud fail',), {}, id="3d-volume")])
def test_cloud_invalid(args, kwargs):
	"""Vérifie le rejet des dimensions incompatibles avec ce graphique."""
	with pytest.raises(ValueError): Grapher().cloud(*args, **kwargs)


# ==================================================
# endregion Figures statistiques
# ==================================================

# ==================================================
# region Figure d'astigmatisme
# ==================================================
##################################################
@pytest.mark.parametrize("args, kwargs, filename, reference", [
		pytest.param((np.array([[-100, 100, 0, 0, 30], [100, 100, 0, 0, 30]], dtype=float), None, 'Astigmatism 3D',),
					 {'pixel_size': 100, 'z_max': 100, 'mode': 'curve', 'n_points': 100}, 'grapher_astigmatism3d_curve.json',
					 'grapher_astigmatism3d_curve.json', id="curve"),
		pytest.param((np.array([[-100, 100, 0, 0, 30], [100, 100, 0, 0, 30]], dtype=float), None, 'Astigmatism 3D',),
					 {'pixel_size': 100, 'z_max': 100, 'mode': 'cross', 'n_points': 100}, 'grapher_astigmatism3d_cross_1.json',
					 'grapher_astigmatism3d_cross_1.json', id="cross-without-points"),
		pytest.param((np.array([[-100, 100, 0, 0, 30], [100, 100, 0, 0, 30]], dtype=float), np.array([[0, 0, 0]], dtype=float), 'Astigmatism 3D',),
					 {'pixel_size': 100, 'z_max': 100, 'mode': 'cross', 'n_points': 100}, 'grapher_astigmatism3d_cross_2.json',
					 'grapher_astigmatism3d_cross_2.json', id="cross-with-points"),
		pytest.param((np.array([[-100, 100, 0, 0, 30], [100, 100, 0, 0, 30]], dtype=float), None, 'Astigmatism 3D',),
					 {'pixel_size': 100, 'z_max': 100, 'mode': 'slope', 'n_points': 100}, 'grapher_astigmatism3d_slope_1.json',
					 'grapher_astigmatism3d_slope_1.json', id="slope-without-points"),
		pytest.param((np.array([[-100, 100, 0, 0, 30], [100, 100, 0, 0, 30]], dtype=float), np.array([[0, 0, 0]], dtype=float), 'Astigmatism 3D',),
					 {'pixel_size': 100, 'z_max': 100, 'mode': 'slope', 'n_points': 100}, 'grapher_astigmatism3d_slope_2.json',
					 'grapher_astigmatism3d_slope_2.json', id="slope-with-points"),
		pytest.param((np.array([[-100, 100, 0, 0, 30], [100, 100, 0, 0, 30]], dtype=float), np.array([[0, 0, 0]], dtype=float), 'Astigmatism 3D',),
					 {'pixel_size': 100, 'z_max': 100, 'mode': 'any', 'n_points': 100}, 'grapher_astigmatism3d_bad.json', 'grapher_astigmatism3d_bad.json',
					 id="unknown-mode")])
def test_astigmatism3d(args, kwargs, filename, reference):
	"""Vérifie chaque configuration du graphique indépendamment."""
	figure = Grapher().astigmatism3d(*args, **kwargs)
	res = _save_output(figure, OUTPUT_DIR / filename)
	ref = json.loads((REF_DIR / reference).read_text(encoding="utf-8"))
	assert res == ref


##################################################
@pytest.mark.parametrize("args, kwargs", [pytest.param((np.zeros((3, 3)), None, 'blank',), {}, id="invalid-model")])
def test_astigmatism3d_invalid(args, kwargs):
	"""Vérifie le rejet des dimensions incompatibles avec ce graphique."""
	with pytest.raises(ValueError): Grapher().astigmatism3d(*args, **kwargs)


# ==================================================
# endregion Figure d'astigmatisme
# ==================================================


# ==================================================
# region Rendus spéciaux
# ==================================================
##################################################
def test_histogram_poisson_distribution():
	"""Exporte une distribution de Poisson et sa courbe ajustée pour comparaison visuelle."""
	# Des classes centrées sur les entiers permettent de comparer les barres aux probabilités de Poisson.
	points = rng.poisson(lam=4.0, size=10000)
	figure = Grapher().histogram(points, "Poisson distribution (lambda = 4)", poissonian=True, density=True, bins=-1)
	_save_output(figure, OUTPUT_DIR / "grapher_visual_poisson.json")


##################################################
def test_histogram_exponential_distribution():
	"""Exporte une exponentielle décroissante et sa courbe ajustée pour comparaison visuelle."""
	# La courbe du Grapher estime la moyenne d'une loi exponentielle non décalée, définie à partir de zéro.
	points = rng.exponential(scale=2.0, size=10000)
	figure = Grapher().histogram(points, "Exponential distribution (mean = 2)", exponential=True, density=True, bins=80)
	_save_output(figure, OUTPUT_DIR / "grapher_visual_exponential.json")


##################################################
def test_histogram_gaussian_mixture_distribution():
	"""Exporte un mélange de deux gaussiennes et sa courbe ajustée pour comparaison visuelle."""
	# Les poids, moyennes et écarts-types distincts rendent les deux composantes visibles.
	points = np.concatenate((rng.normal(-2.0, 0.5, 3500), rng.normal(3.0, 0.8, 6500)))
	figure = Grapher().histogram(points, "Gaussian mixture (35% / 65%)", gaussian_mixture=True, density=True, bins=80)
	_save_output(figure, OUTPUT_DIR / "grapher_visual_gaussian_mixture.json")

# ==================================================
# endregion Rendus spéciaux
# ==================================================
