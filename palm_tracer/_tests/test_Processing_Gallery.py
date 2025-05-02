""" Fichier des tests pour la création de galeries. """
import os
from pathlib import Path

import pandas as pd

from palm_tracer.Processing import make_gallery
from palm_tracer.Tools import open_tif, save_tif

INPUT_DIR = Path(__file__).parent / "input"
OUTPUT_DIR = Path(__file__).parent / "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)


##################################################
def test_make_gallery():
	"""Test de la génération de galerie."""
	stack = open_tif(f"{INPUT_DIR}/stack.tif")														# Récupération d'une stack
	localizations = pd.read_csv(f"{INPUT_DIR}/ref/stack-localizations-103.6_True_2_1.0_0.0_7.csv")  # Récupération du fichier de localisation
	gallery = make_gallery(stack, localizations, 11, 10)											# Rendu
	save_tif(gallery, f"{OUTPUT_DIR}/test_gallery.tif")												# Sauvegarde
	assert gallery.shape == (5, 110, 110)
