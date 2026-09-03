"""Teste l'ajustement des mélanges gaussiens unidimensionnels."""

import numpy as np
import pytest

from palm_tracer._tests.Utils import rng
from palm_tracer.Processing import GaussianMixture


##################################################
def test_fit_two_components():
	"""Vérifie l'estimation des paramètres d'un mélange de deux gaussiennes."""
	data = np.concatenate((rng.normal(-2.0, 0.5, 3500), rng.normal(3.0, 0.8, 6500)))
	mixture = GaussianMixture.fit(data, n_component=2)

	assert mixture.converged
	assert np.isclose(np.sum(mixture.weights), 1.0)
	assert np.allclose(mixture.weights, [0.35, 0.65], atol=0.02)
	assert np.allclose(mixture.means, [-2.0, 3.0], atol=0.05)
	assert np.allclose(mixture.sigmas, [0.5, 0.8], atol=0.05)


##################################################
def test_fit_is_generic():
	"""Vérifie que l'ajustement accepte plus de deux composantes."""
	data = np.concatenate((rng.normal(-4.0, 0.3, 2000), rng.normal(0.0, 0.5, 3000), rng.normal(5.0, 0.7, 5000)))
	mixture = GaussianMixture.fit(data, n_component=3)

	assert mixture.weights.shape == (3,)
	assert np.all(np.diff(mixture.means) > 0)
	assert np.allclose(mixture.means, [-4.0, 0.0, 5.0], atol=0.08)


##################################################
def test_make_curve():
	"""Vérifie la génération de la courbe de densité du mélange."""
	mixture = GaussianMixture.fit(np.concatenate((rng.normal(-2.0, 0.5, 2000), rng.normal(2.0, 0.5, 2000))))
	x_grid, density = mixture.make_curve([-6.0, 6.0], n_point=1000)

	assert x_grid.shape == density.shape == (1000,)
	assert np.all(density >= 0)
	assert np.isclose(np.trapezoid(density, x_grid), 1.0, atol=1e-3)


##################################################
@pytest.mark.parametrize("data, kwargs", [(np.arange(2), {"n_component": 0}), (np.arange(2), {"max_iter": 0}), (np.arange(2), {"tolerance": 0}),
										  (np.arange(2), {"n_init": 0}), (np.empty(0), {"n_component": 2}), (np.arange(2), {"n_component": 3}),
										  (np.ones(10), {"n_component": 2}), (np.ones(10), {"n_component": 1})])
def test_invalid_fit_parameters(data, kwargs):
	"""Vérifie le rejet des données et paramètres incompatibles avec l'ajustement."""
	with pytest.raises(ValueError): GaussianMixture.fit(data, **kwargs)


##################################################
@pytest.mark.parametrize("limits, n_point", [([-1.0, 1.0], 1), ([0.0], 128), ([np.nan, 1.0], 128), ([1.0, 1.0], 128)])
def test_invalid_curve_parameters(limits, n_point):
	"""Vérifie le rejet des paramètres incompatibles avec la génération d'une courbe."""
	mixture = GaussianMixture(np.ones(1), np.zeros(1), np.ones(1), 0.0, True, 1)

	with pytest.raises(ValueError): mixture.make_curve(limits, n_point)


##################################################
def test_initialize_centers_fallback():
	"""Vérifie le repli sur les quantiles lorsque k-means++ ne dispose plus d'une distance positive."""
	data = np.ones(4)
	centers = GaussianMixture._initialize_centers(data, 2, 1, np.random.default_rng(0))

	assert np.array_equal(centers, np.ones(2))


##################################################
def test_kmeans_iteration_limit(monkeypatch):
	"""Vérifie le retour des paramètres lorsque le k-means atteint sa limite d'itérations."""
	monkeypatch.setattr(np, "allclose", lambda *args, **kwargs: False)
	data = np.array([0.0, 1.0, 9.0, 10.0])
	weights, means, sigmas = GaussianMixture._parameters_from_centers(data, np.array([0.0, 10.0]), 5.0, 1e-6)

	assert np.array_equal(weights, [0.5, 0.5])
	assert np.array_equal(means, [0.5, 9.5])
	assert np.array_equal(sigmas, [0.5, 0.5])


##################################################
def test_em_iteration_limit():
	"""Vérifie l'état retourné lorsqu'EM atteint sa limite d'itérations avant de converger."""
	data = np.concatenate((rng.normal(-1.0, 0.5, 100), rng.normal(1.0, 0.5, 100)))
	mixture = GaussianMixture.fit(data, max_iter=1, n_init=1)

	assert not mixture.converged
	assert mixture.n_iter == 1
