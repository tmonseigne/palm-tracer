""" Fichier des tests pour la lecture/écriture des fichiers """

import os
from pathlib import Path

import numpy as np
import pytest

from palm_tracer.Tools import FileIO

OUTPUT_DIR = Path(__file__).parent / "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)

REF_DICT = {"First param": [0, 1, 2],
			"2nd param":   True,
			"3rd param":   "True",
			"élément":     0,
			"Inception":   {"intern": 0}}

# np.random.seed(42) # Possibilité de fixer la graine du random pour avoir un aléatoire "contrôlé".
SIZE = 512  # Taille de l'image de test
NOISE_2D = np.random.rand(SIZE, SIZE) * 255  # Bruit sur une image 2D
REF_BOOLEAN_MASK = NOISE_2D > 128  # Conversion en booléen
GRADIENT = np.linspace(0, 255, SIZE, dtype=np.float32)  # Création du dégradé croissant de 0 à 255
REF_GRADIENT = np.tile(GRADIENT, (SIZE, 1))  # Répète le dégradé sur toutes les lignes
REF_STACK = np.stack((REF_GRADIENT, np.fliplr(REF_GRADIENT)), axis=0)  # Empilement du dégradé et son miroir horizontal


##################################################
def test_save_json():
	""" Test de la fonction save_json. """
	FileIO.save_json(f"{OUTPUT_DIR}/test_save_json.json", REF_DICT)
	assert True


##################################################
def test_open_json():
	""" Test de la fonction open_json. """
	dictionary = FileIO.open_json(f"{OUTPUT_DIR}/test_save_json.json")
	assert dictionary == REF_DICT, "Le dictionnaire devrait correspondre à la référence."


##################################################
def test_open_json_bad_file():
	""" Test de la fonction open_json avec un fichier inexistant. """
	with pytest.raises(OSError) as exception_info:
		dictionary = FileIO.open_json("bad_filename.json")
	assert exception_info.type == OSError, "L'erreur relevé n'est pas correcte."


##################################################
def test_save_tif():
	"""	Test de la fonction save_tif. """
	FileIO.save_tif(REF_STACK, f"{OUTPUT_DIR}/test_save_stack.tif")
	assert True


##################################################
def test_save_tif_2d():
	""" Test de la fonction save_tif avec une image 2D. """
	FileIO.save_tif(REF_GRADIENT, f"{OUTPUT_DIR}/test_save_stack_2D.tif")
	assert True


##################################################
def test_save_tif_bad_stack():
	""" Test de la fonction save_tif avec une image 1D. """
	with pytest.raises(ValueError) as exception_info:
		FileIO.save_tif(REF_GRADIENT[1, :], f"{OUTPUT_DIR}/test_save_stack_1D.tif")
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."


##################################################
def test_open_tif():
	""" Test de la fonction open_tif. """
	stack = FileIO.open_tif(f"{OUTPUT_DIR}/test_save_stack.tif")
	assert np.allclose(REF_STACK, stack, atol=1), "L'échantillon devrait correspondre à la référence avec une tolérance d'erreur."


##################################################
def test_open_tif_bad_file():
	""" Test de la fonction open_tif avec un fichier inexistant. """
	with pytest.raises(OSError) as exception_info:
		stack = FileIO.open_tif("bad_filename.png")
	assert exception_info.type == OSError, "L'erreur relevé n'est pas correcte."
