""" Fichier des tests pour la création de galeries. """
from palm_tracer._tests.Utils import *
from palm_tracer.Processing import Gallery
from palm_tracer.Tools import FileIO


##################################################
def test_make_gallery():
	"""Test de la génération de galerie."""
	stack = FileIO.open_tif(f"{INPUT_DIR}/stack.tif")										 # Récupération d'une stack
	localizations = pd.read_csv(REF_DIR / "stack-localizations-103.6_True_2_1.0_0.0_7.csv")  # Récupération du fichier de localisation
	gallery = Gallery.make_gallery(stack, localizations, 11, 10)							 # Rendu
	FileIO.save_tif(gallery, f"{OUTPUT_DIR}/test_gallery.tif")								 # Sauvegarde
	assert gallery.shape == (5, 110, 110)													 # Vérificaiton sur la taille de la gallerie
