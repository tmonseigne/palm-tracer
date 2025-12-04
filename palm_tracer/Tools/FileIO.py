"""
Fichier de fonctions de manipulation de fichiers

Ce module regroupe diverses fonctions pour la gestion et la manipulation de fichiers.
"""

import json
import os
from typing import Any

import matplotlib as mpl
import numpy as np
import scipy.io as io
import tifffile as tiff
from PIL import Image

MAX_UI_8 = np.iinfo(np.uint8).max
MAX_UI_16 = np.iinfo(np.uint16).max


# ==================================================
# region JSON IO
# ==================================================
##################################################
def save_json(filename: str, data: dict[str, Any]):
	"""
	Enregistre un dictionnaire au format JSON.

	:param filename: Chemin du fichier JSON de sortie.
	:param data: Données à enregistrer.
	"""
	with open(filename, "w", encoding="utf-8") as file: json.dump(data, file, indent=4, ensure_ascii=False)


##################################################
def open_json(filename: str) -> dict[str, Any]:
	"""
	Ouvre un fichier JSON et récupère le dictionnaire.

	:param filename: Chemin du fichier JSON d'entrée.
	:return: Dictionnaire contenu dans le JSON.
	"""
	if not os.path.isfile(filename): raise OSError(f"Le fichier \"{filename}\" est introuvable.")
	with open(filename, "r", encoding="utf-8") as file: return json.load(file)


# ==================================================
# endregion JSON IO
# ==================================================

# ==================================================
# region TIF IO
# ==================================================
##################################################
def save_tif(stack: np.ndarray, filename: str):
	"""
	Sauvegarde un tableau 3D (ou 2D converti en 3D) dans un fichier TIF multi-frame avec tifffile.

	:param stack: Tableau contenant l'image ou les frames
				  - Si 2D (hauteur x largeur), convertit en pile 3D avec une seule frame.
				  - Si 3D (frames x hauteur x largeur), sauvegarde les frames en multi-frame.
	:param filename: Nom du fichier TIF de sortie.
	"""
	if stack.ndim == 2: stack = stack[np.newaxis, ...]		 # Si le tableau est 2D, le transformer en 3D avec une seule frame
	if stack.ndim != 3: raise ValueError("Le tableau doit être 2D (hauteur, largeur) ou 3D (frames, hauteur, largeur).")
	stack = np.clip(stack, 0, MAX_UI_16).astype(np.uint16)	 # S'assure que les valeurs sont bien entre 0 et MAX_UI_16 et de type uint16
	tiff.imwrite(filename, stack, photometric="minisblack")  # Sauvegarde la pile avec tifffile


##################################################
def open_tif(filename: str) -> np.ndarray:
	"""
	Ouvre un fichier TIF en tant que pile 3D (frames x hauteur x largeur).
	Si le fichier contient une seule image 2D, ajoute une dimension pour en faire une pile 3D.

	:param filename: Chemin du fichier TIF à ouvrir.
	:return: Tableau 3D contenant les données TIF.

	.. note::
		Attention les données doivent rester telle quelle pour le transfert à la DLL.
		Aucun cast en float ne doit être fait.
	"""
	if not os.path.isfile(filename): raise OSError(f"Le fichier \"{filename}\" est introuvable.")
	stack = tiff.imread(filename)  # Lecture du fichier avec tifffile
	# return np.asarray(stack, dtype=np.float32)  # Assurer que le type est np.float32
	return stack


# ==================================================
# endregion TIF IO
# ==================================================

# ==================================================
# region PNG IO
# ==================================================
##################################################
def save_png(image: np.ndarray, filename: str, normalization: bool = True):
	"""
	Sauvegarde un tableau 2D dans un fichier PNG avec Pillow.

	:param image: Tableau contenant l'image 2D
	:param filename: Nom du fichier TIF de sortie.
	:param normalization: Normalize l'image avant enregistrement.
	"""
	if not (2 <= image.ndim <= 3): raise ValueError("L'image doit être en 2D (niveaux de gris) ou 3D (RGB).")
	if normalization:
		min_val, max_val = image.min(), image.max()
		if max_val > min_val: image = ((image - min_val) / (max_val - min_val) * 255).astype(np.uint8)
		else: image = np.zeros_like(image, dtype=np.uint8)  # Cas d'une image uniforme

	image = image.clip(0, 255).astype(np.uint8)  # Conversion en entiers 8 bits
	im = Image.fromarray(image)					 # Passage par Pillow
	im.save(filename)							 # Enregistrement


##################################################
def grayscale_to_color(data: np.ndarray, color_map: str = "viridis") -> np.ndarray:
	"""
	Convertie une image 2D Niveau de gris en tableau 3D (pour la couleur RGB) selon la color map. Le format est compatible avec Pillow et Napari.
	Une color Map Napari serait bien en cas de superposition entre un affichage napari et en fond l'image généré.

	:param data: Image 2D (H, W) uint16.
	:param color_map: nom de colormap Matplotlib.
		Privilégier des cartes **perceptuellement uniformes** ('viridis', 'magma', 'plasma', 'inferno', 'cividis', 'turbo').
		(liste des colormaps : https://matplotlib.org/stable/tutorials/colors/colormaps.html).
	:return: Image RGB de forme (H, W, 3) en dtype uint8, compatible Pillow et Napari.
	"""
	# Récupération de la table de correspondance (LUT)
	lut = np.zeros((MAX_UI_16 + 1, 3), dtype=np.uint8)
	# Échantillons continus pour indices 1..65535 inclus
	# t_k = (k-1)/65534 pour k ∈ [1..65535] ; nombre d'échantillons = 65535
	t = np.linspace(0.0, 1.0, MAX_UI_16, dtype=np.float32)

	# Récupère la colormap sous forme d'un callable vectorisé (N,4) RGBA ∈ [0,1]
	cmap = mpl.colormaps.get_cmap(color_map)
	rgba = cmap(t, bytes=False)  # float32 en [0,1], shape (65535,4)
	rgb = rgba[:, :3]

	# Mise à l'échelle -> uint8
	rgb_u8 = np.rint(rgb * MAX_UI_8).astype(np.uint8)  # (65535, 3)

	# Place les couleurs aux indices 1..65535, laisse 0 à (0,0,0)
	lut[1:] = rgb_u8
	return lut[data.astype(np.uint16)]


# ==================================================
# endregion PNG IO
# ==================================================

# ==================================================
# region Matlab File IO
# ==================================================
##################################################
def open_calibration_mat(filename: str) -> dict[str, Any]:
	"""
	Charge un fichier de calibration matlab.

	:param filename: Nom du fichier mat en entrée.
	:return: Dictionnaire contennant les éléments utiles
	"""
	if not os.path.isfile(filename): raise OSError(f"Le fichier de calibration \"{filename}\" est introuvable.")
	calibration = io.loadmat(filename)
	cspline = calibration["SXY"]["cspline"][0, 0]				 # Elements de cspline
	coeff = cspline["coeff"][0][0][0][0]						 # Coefficients de la Spline
	if isinstance(coeff, (list, tuple)): coeff = coeff[0]		 # les coefficients peuvent être dans un sous-groupe
	return {"dz":    cspline["dz"][0][0][0][0],					 # Pas sur Z
			"coeff": np.asfortranarray(coeff, dtype=np.float64)  # Passage en column major et en double
			}

# ==================================================
# region Matlab File IO
# ==================================================
