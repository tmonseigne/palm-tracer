""" Fichier des tests pour le logger """

import os
from palm_tracer.Tools import Logger
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)


##################################################
def test_logger():
	"""Test du logger."""
	logger = Logger()
	logger.open(f"{OUTPUT_DIR}/test_logger.log")
	logger.add("First message")
	logger.add("")
	logger.add("after blank")
	logger.close()


##################################################
def test_logger_bad_use():
	"""Test d'une mauvaise utilisation du Logger."""
	logger = Logger()
	logger.close()
	logger.add("Message without logger open")
