""" Fichier des tests pour le logger. """
from palm_tracer._tests.Utils import *
from palm_tracer.Tools import Logger

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
