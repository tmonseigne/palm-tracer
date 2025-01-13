""" Fichier des tests pour le widget """

import numpy as np

from palm_tracer import PALMTracerWidget


##################################################
def test_widget_creation(make_napari_viewer, capsys):
	"""Test basique de création du widget."""
	viewer = make_napari_viewer()					# Créer un viewer à l'aide de la fixture.
	viewer.add_image(np.random.random((256, 256)))  # Ajouter une image
	my_widget = PALMTracerWidget(viewer)			# Créer notre widget, en passant par le viewer.
	assert True


##################################################
def test_widget_process(make_napari_viewer, capsys):
	"""Test click sur le bouton."""
	viewer = make_napari_viewer()					# Créer un viewer à l'aide de la fixture.
	viewer.add_image(np.random.random((256, 256)))  # Ajouter une image
	my_widget = PALMTracerWidget(viewer)			# Créer notre widget, en passant par le viewer.
	my_widget.process()							# Appel de la méthode process
	# captured = capsys.readouterr() # Lire la sortie capturée
	assert True
