""" Fichier des tests pour la lecture/écriture des fichiers """

import os
from pathlib import Path

import pytest

from palm_tracer.Tools import FileIO

OUTPUT_DIR = Path(__file__).parent / "Output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)

REF_DICT = {"First param": [0, 1, 2],
			"2nd param":   True,
			"3rd param":   "True",
			"élément":     0,
			"Inception":   {"intern": 0}}


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
