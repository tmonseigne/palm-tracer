""" Fichier des tests pour l'utilisation des DLL """
import os
from pathlib import Path

import numpy as np
import pandas as pd

from palm_tracer.Processing import make_gallery
from palm_tracer.Tools import save_tif, open_tif

INPUT_DIR = Path(__file__).parent / "input"
OUTPUT_DIR = Path(__file__).parent / "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)

SIZE_X, SIZE_Y, INTENSITY, RATIO = 100, 50, 1000, 10
rng = np.random.default_rng(42)  # Initialisation du générateur avec une seed
SIZE = int(SIZE_X * np.sqrt(SIZE_Y))
POINTS = np.stack([rng.uniform(1, SIZE_X - 1, size=SIZE), rng.uniform(1, SIZE_Y - 1, size=SIZE), rng.uniform(0, INTENSITY, size=SIZE)], axis=1)


##################################################
def test_make_gallery():
	"""Test de la génération de galerie."""
	stack = open_tif(f"{INPUT_DIR}/stack.tif")														# Récupération d'une stack
	localizations = pd.read_csv(f"{INPUT_DIR}/ref/stack-localizations-103.6_True_2_1.0_0.0_7.csv")	# Récupération du fichier de localisation
	gallery = make_gallery(stack, localizations, 11, 10)											# Rendu
	save_tif(gallery, f"{OUTPUT_DIR}/test_gallery.tif")												# Sauvegarde
	assert gallery.shape == (5, 110, 110)
