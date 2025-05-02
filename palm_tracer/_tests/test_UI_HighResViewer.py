""" Fichier des tests pour le widget de visualisation. """

import numpy as np
from qtpy.QtCore import QPoint, QSize, Qt
from qtpy.QtGui import QResizeEvent, QWheelEvent

from palm_tracer.UI import HighResViewer

SIZE = 512												# Taille de l'image de test
GRADIENT = np.linspace(0, 255, SIZE, dtype=np.float32)  # Création du dégradé croissant de 0 à 255
REF_GRADIENT = np.tile(GRADIENT, (SIZE, 1))				# Répète le dégradé sur toutes les lignes

# Ajout d'une perturbation (petite sinusoïde)
X, Y = np.meshgrid(np.arange(SIZE), np.arange(SIZE))
PERTURBATION_X = 20 * np.sin(2 * np.pi * X / 32)  # Sinusoïde avec une période de 32 pixels
PERTURBATION_Y = 20 * np.sin(2 * np.pi * Y / 64)  # Sinusoïde avec une période de 64 pixels
PERTURBATION = PERTURBATION_X + PERTURBATION_Y
REF_IMAGE_UINT8 = REF_GRADIENT + PERTURBATION
REF_IMAGE_UINT8 = np.clip(REF_IMAGE_UINT8, 0, 255).astype(np.uint8)
REF_IMAGE_UINT16 = np.clip(REF_IMAGE_UINT8.astype(np.uint16) * 256, 0, 65535)

R = REF_IMAGE_UINT8
G = np.clip(255 - REF_GRADIENT, 0, 255).astype(np.uint8)  # Inversion du gradient pour du contraste
B = np.clip(PERTURBATION + 128, 0, 255).astype(np.uint8)  # Une composante perturbée en bleu
REF_IMAGE_RGB = np.stack([R, G, B], axis=-1)			  # Assemble les trois canaux


##################################################
def test_high_res_view(make_napari_viewer):
	"""Test basique de la classe HighResViewer. """
	view = HighResViewer(REF_IMAGE_UINT16)
	assert True


##################################################
def test_high_res_view_load(make_napari_viewer):
	"""Test basique de la classe HighResViewer. """
	view = HighResViewer(REF_IMAGE_UINT16)
	view.load_image(REF_IMAGE_UINT8)
	view.load_image(REF_IMAGE_RGB)
	assert True


##################################################
def test_high_res_view_check_ratio(make_napari_viewer):
	"""Test de la fonction _check_ratio. """
	view = HighResViewer(REF_IMAGE_UINT16)
	width, height = view._check_ratio(300, 200)
	assert width == 300 and height == 300, "Ratio non respecté."
	width, height = view._check_ratio(200, 300)
	assert width == 300 and height == 300, "Ratio non respecté."
	width, height = view._check_ratio(300, 300)
	assert width == 300 and height == 300, "Ratio non respecté."


##################################################
def test_high_res_view_adjust_window_size(make_napari_viewer):
	"""Test de la fonction _adjust_window_size. """
	view = HighResViewer(REF_IMAGE_UINT16)
	view._adjust_window_size(100, 100)
	assert view.last_size == (400, 400), "Dimensions non respectées."
	view._adjust_window_size(600, 500)
	assert view.last_size == (600, 500), "Dimensions non respectées."
	view._adjust_window_size(500, 600)
	assert view.last_size == (500, 600), "Dimensions non respectées."
	view._adjust_window_size(600, 600)
	assert view.last_size == (600, 600), "Dimensions non respectées."
	view._adjust_window_size(200, 6000)
	assert view.last_size == (400, 2160), "Dimensions non respectées."
	view._adjust_window_size(6000, 200)
	assert view.last_size == (3840, 400), "Dimensions non respectées."
	view._adjust_window_size(6000, 200, True)
	assert view.last_size == (3840, 3840), "Dimensions non respectées."
	assert True


##################################################
def test_high_res_view_wheel(make_napari_viewer):
	"""Test de la fonction check_ratio. """
	view = HighResViewer(REF_IMAGE_UINT16)
	# Taille initiale de la vue
	initial_width = view.view.width()
	initial_height = view.view.height()

	# Fonction pour simuler un événement molette
	def simulate_wheel_event(delta_y):
		wheel_event = QWheelEvent(
				view.view.mapToGlobal(view.view.rect().center()),  # Position globale
				view.view.mapToGlobal(view.view.rect().center()),  # Ancienne position
				QPoint(0, delta_y),  # angleDelta simulé
				QPoint(0, 0),  # pixelDelta (non utilisé ici)
				Qt.MouseButton.NoButton, Qt.KeyboardModifier.NoModifier, Qt.ScrollPhase.ScrollUpdate, False)
		view.wheelEvent(wheel_event)

	# Simulation du zoom avant (molette vers le haut)
	simulate_wheel_event(120)

	# Vérifier que la taille de la vue a augmenté
	assert view.width() > initial_width
	assert view.height() > initial_height

	# Simulation du zoom arrière (molette vers le bas)
	simulate_wheel_event(-120)

	# Vérifier que la taille est revenue à l'originale (ou proche)
	assert abs(view.view.width() - initial_width) < 5
	assert abs(view.view.height() - initial_height) < 5


##################################################
def test_high_res_view_resize(make_napari_viewer):
	"""Test de la fonction check_ratio. """
	view = HighResViewer(REF_IMAGE_UINT16)  # Taille initiale de la fenêtre
	initial_size = view.size()

	# Fonction pour simuler un événement de redimensionnement
	def simulate_resize_event(w, h):
		resize_event = QResizeEvent(QSize(w, h), view.size())
		view.resizeEvent(resize_event)

	# 🔍 Simulation d'un agrandissement de la fenêtre
	new_width, new_height = initial_size.width() + 100, initial_size.height() + 100
	simulate_resize_event(new_width, new_height)
	assert view.width() == new_width and view.height() == new_height

	# 🔍 Simulation d'une réduction de la fenêtre
	new_width, new_height = initial_size.width() - 50, initial_size.height() - 50
	simulate_resize_event(new_width, new_height)
	assert view.width() == new_width and view.height() == new_height

	simulate_resize_event(new_width, new_height)
	assert view.width() == new_width and view.height() == new_height
