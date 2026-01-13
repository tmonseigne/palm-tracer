""" Fichier des tests pour l'astigmatisme 3D, """

from palm_tracer._tests.Utils import *
from palm_tracer.Processing.Astigmatism3D import *

os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)


##################################################
def test_get_z_from_planes():
	"""Test basique pour get_z_from_planes."""
	planes = np.array([0, 1, 2, 3, 4])

	res = get_z_from_planes(planes, z_min=-10, z_max=10)
	ref = [-10, -5, 0, 5, 10]
	assert np.allclose(res, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu: {ref}\nObtenu : {res}"

	res = get_z_from_planes(planes, z_min=-10, z_max=0)
	ref = [-10, -7.5, -5, -2.5, 0]
	assert np.allclose(res, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu: {ref}\nObtenu : {res}"

	res = get_z_from_planes(planes, z_min=0, z_max=10)
	ref = [0, 2.5, 5, 7.5, 10]
	assert np.allclose(res, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu: {ref}\nObtenu : {res}"

	res = get_z_from_planes(planes, z_min=1, z_max=1)
	ref = np.ones(5)
	assert np.allclose(res, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu: {ref}\nObtenu : {res}"

	res = get_z_from_planes(np.ones(5), z_min=-10, z_max=10)
	ref = np.zeros(5)
	assert np.allclose(res, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu: {ref}\nObtenu : {res}"


##################################################
def test_get_z_from_step():
	"""Test basique pour get_z_from_step."""
	res = get_z_from_step(5, 1)
	ref = [-2, -1, 0, 1, 2.]
	assert np.allclose(res, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu: {ref}\nObtenu : {res}"

	res = get_z_from_step(4, 1)
	ref = [-1.5, -0.5, 0.5, 1.5]
	assert np.allclose(res, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu: {ref}\nObtenu : {res}"

	res = get_z_from_step(5, 1, False)
	ref = [0, 1, 2, 3, 4.]
	assert np.allclose(res, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu: {ref}\nObtenu : {res}"


##################################################
def test_sigma_model():
	"""Test basique pour sigma_model."""
	model = np.array([200., 100., 0., 0., 32.], dtype=np.float64)
	z = np.linspace(-200, 200, 11, dtype=np.float64)
	res = sigma_model(model, z, 160, 1)
	ref = [0.82462113, 0.74726167, 0.67052218, 0.59464275, 0.52, 0.4472136, 0.37735925, 0.31240999, 0.25612497, 0.21540659, 0.2]
	assert np.allclose(res, ref), f"Résultat incorrect.\nAttendu: {ref}\nObtenu : {res}"
