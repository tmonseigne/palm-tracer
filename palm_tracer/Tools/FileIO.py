"""
Fichier de fonctions de manipulation de fichiers

Ce module regroupe diverses fonctions pour la gestion et la manipulation de fichiers.
"""

import ctypes
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Literal, Optional

import matplotlib as mpl
import numpy as np
import scipy.io as io
import tifffile as tiff
from PIL import Image

from palm_tracer.Tools import Ui

MAX_UI_8 = np.iinfo(np.uint8).max
MAX_UI_16 = np.iinfo(np.uint16).max
DLL_PATH = Path(__file__).parent.parent / "DLL"


# ==================================================
# region File Management
# ==================================================
##################################################
def add_extension(filename: str, extension: str) -> str:
	"""
	Ajoute l'extension au fichier si ce n'est pas déjà l'extension actuelle

	:param filename: Nom du fichier
	:param extension: Extension finale du fichier
	"""
	if not extension.startswith("."): extension = "." + extension  # S'assurer que l'extension commence par un point
	if not filename.endswith(extension): filename += extension  # .	 Si le fichier n'a pas déjà l'extension, on l'ajoute
	return filename


##################################################
def add_suffix(filename: str, suffix: str) -> str:
	"""
	Ajoute un suffixe à un nom de fichier (gère la possibilité d'une extension ou non au nom de fichier).

	:param filename: Nom de fichier d'origine.
	:param suffix: Suffixe à ajouter.
	:return: Nom de fichier avec l'horodatage ajouté.
	"""
	# Insérer le suffixe avant l'extension du fichier s'il y en a une
	if "." in filename:
		name, ext = filename.rsplit(".", 1)
		return f"{name}{suffix}.{ext}"
	return f"{filename}{suffix}"


##################################################
def get_timestamp_for_files(with_hour: bool = True) -> str:
	"""
	Créé un horodatage au format -AAAAMMJJ_HHMMSS pour un nom de fichier.

	:param with_hour: Ajoute ou non l'heure au timestamp
	:return: Horodatage.
	"""
	if with_hour: return datetime.now().strftime("%Y%m%d_%H%M%S")  # Formater la date et l'heure
	return datetime.now().strftime("%Y%m%d")  # .					 Formater la date


##################################################
def get_last_file(path: str | Path, name: str, sort_mode: Literal["time", "alpha"] = "alpha") -> str:
	"""
	Récupère le dernier fichier (le plus récent) qui contient le paramètre `name` dans son nom dans le chemin `path`.

	:param path: Chemin du dossier où chercher les fichiers.
	:param name: Chaîne à rechercher dans les noms de fichiers.
	:param sort_mode: Mode de tri : "time" : date de modification (par défaut), "alpha" : ordre alphabétique.
	:return: Chemin complet du dernier fichier trouvé ou une chaîne vide si aucun fichier ne correspond.
	"""
	try:
		folder = Path(path)
		if not folder.is_dir(): return ""  # .									   Ce n'est pas un dossier
		files = [p for p in folder.iterdir() if p.is_file() and name in p.name]  # Récupérer tous les fichiers contenant le nom
		if not files: return ""  # .											   Aucun fichier trouvé
		if sort_mode == "time": files.sort(key=lambda p: p.stat().st_mtime)  # .   Trier les fichiers par date de modification décroissante
		else: files.sort(key=lambda p: p.name)  # .								   Trier les fichiers par ordre alphabétique.
		return str(files[-1])  # .												   Retourner le dernier fichier de la liste (le plus récent)
	except Exception as e:
		print(f"Erreur lors de la recherche du fichier : {e}")
		return ""


##################################################
def extract_suffix(filename: str | Path, separator: str = "-") -> str:
	"""
	Récupère le suffixe d'un fichier (partie après le séparateur ou après sa dernière occurence en cas de présence multiple).

	:param filename: Nom du fichier.
	:param separator: Séparateur avant le suffixe
	:return: Suffixe si le séparateur est présent sinon une chaine vide
	"""
	stem = Path(filename).stem
	parts = stem.rsplit(separator, 1)
	return parts[1] if len(parts) == 2 else ""


##################################################
def load_dll(name: str) -> Optional[ctypes.CDLL]:
	"""Charge une DLL, si elle existe."""
	ext = "dll" if sys.platform.startswith("win") else "dylib" if sys.platform == "darwin" else "so"
	path = DLL_PATH / f"PALMTracer_{name}.{ext}"

	try:
		return ctypes.cdll.LoadLibrary(str(path.resolve()))  # Resolve permet d'assurer un chemin absolu et non relatif (pour des DLL ça peut être vital).
	except OSError as e:
		Ui.print_warning(f"Impossible de charger la DLL '{path.name}':\n\t{e}")
		return None


# ==================================================
# endregion File Management
# ==================================================

# ==================================================
# region JSON IO
# ==================================================
##################################################
def save_json(filename: str | Path, data: dict[str, Any]):
	"""
	Enregistre un dictionnaire au format JSON.

	:param filename: Chemin du fichier JSON de sortie.
	:param data: Données à enregistrer.
	"""
	path = Path(filename)
	path.parent.mkdir(parents=True, exist_ok=True)  # Au cas où, création des dossiers et sous-dossiers
	path.write_text(json.dumps(data, indent=4, ensure_ascii=False), encoding="utf-8")


##################################################
def open_json(filename: str | Path) -> dict[str, Any]:
	"""
	Ouvre un fichier JSON et récupère le dictionnaire.

	:param filename: Chemin du fichier JSON d'entrée.
	:return: Dictionnaire contenu dans le JSON.
	"""
	path = Path(filename)
	if not path.is_file(): raise OSError(f"Le fichier '{path}' est introuvable.")
	return json.loads(path.read_text(encoding="utf-8"))


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
	if stack.ndim == 2: stack = stack[np.newaxis, ...]  # .	   Si le tableau est 2D, le transformer en 3D avec une seule frame
	if stack.ndim != 3: raise ValueError("Le tableau doit être 2D (hauteur, largeur) ou 3D (frames, hauteur, largeur).")
	stack = np.clip(stack, 0, MAX_UI_16).astype(np.uint16)  # .S'assure que les valeurs sont bien entre 0 et MAX_UI_16 et de type uint16
	tiff.imwrite(filename, stack, photometric="minisblack")  # Sauvegarde la pile avec tifffile


##################################################
def open_tif(filename: str | Path) -> np.ndarray:
	"""
	Ouvre un fichier TIF en tant que pile 3D (frames x hauteur x largeur).
	Si le fichier contient une seule image 2D, ajoute une dimension pour en faire une pile 3D.

	:param filename: Chemin du fichier TIF à ouvrir.
	:return: Tableau 3D contenant les données TIF.

	.. note::
		Attention les données doivent rester telle quelle pour le transfert à la DLL.
		Aucun cast en float ne doit être fait.
	"""
	path = Path(filename)
	if not path.is_file(): raise OSError(f'Le fichier "{path}" est introuvable.')
	res = tiff.imread(str(path))  # .									 Conserve dtype
	if not res.flags["C_CONTIGUOUS"]: res = np.ascontiguousarray(res)  # Garantit contiguïté sans copie si déjà C-contiguous
	return res


# ==================================================
# endregion TIF IO
# ==================================================

# ==================================================
# region PNG IO
# ==================================================
##################################################
def save_png(image: np.ndarray, filename: str | Path, normalization: bool = True):
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
	im = Image.fromarray(image)  # .			   Passage par Pillow
	im.save(filename)  # .						   Enregistrement


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
def open_calibration_mat(filename: str | Path) -> dict[str, Any]:
	"""
	Charge un fichier de calibration matlab.

	:param filename: Nom du fichier mat en entrée.
	:return: Dictionnaire contennant les éléments utiles
	"""
	path = Path(filename)
	if not path.is_file(): raise OSError(f'Le fichier de calibration "{path}" est introuvable.')

	calibration = io.loadmat(str(path))
	cspline = calibration["SXY"]["cspline"][0, 0]  # .			   Élément cspline
	coeff = cspline["coeff"][0][0][0][0]  # .					   Coefficients de la spline
	if isinstance(coeff, (list, tuple)): coeff = coeff[0]  # .	   Parfois dans un sous-groupe

	return {
			"dz":    cspline["dz"][0][0][0][0],
			"coeff": np.asfortranarray(coeff, dtype=np.float64)  # Passage en column major et en double
			}
