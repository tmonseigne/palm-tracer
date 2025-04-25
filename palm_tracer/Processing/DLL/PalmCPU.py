"""
Fichier contenant une classe pour utiliser la DLL externe CPU_PALM, exécuter les algorithmes de détection de points et les paramètres liés.

.. todo::
	Doit ont garder les identifiants et les plans qui vont de 1 à N au lieu du classique 0 à N-1 ?

.. todo::
	Le processus n'est pas thread sagef avec sa gestion des pointeurs un multithreading est donc incompatible pour le moment.
"""

import ctypes
import math
import sys
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Optional
import time
import numpy as np
import pandas as pd
from palm_tracer.Processing.DLL.Load import load_dll
from palm_tracer.Processing.DLL.Parsing import get_max_points, parse_palm_result


# Fonction pour formater le temps en secondes en HH:MM:SS
##################################################
def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

##################################################
@dataclass
class PalmCPU:
	""" Classe permettant d'utiliser la DLL externe CPU_PALM, exécuter les algorithmes de détection de points et les paramètres liés. """
	_dll: ctypes.CDLL = field(init=False)
	_points: np.ndarray = field(init=False)
	_args: OrderedDict[str, Any] = field(init=False)

	##################################################
	def __post_init__(self):
		"""Méthode appelée automatiquement après l'initialisation du dataclass."""
		self._dll = load_dll("CPU")
		self._points = np.zeros((1,), dtype=np.float64)

		self._args = OrderedDict(
				[("image", None),					# Image
				 ("points", None),					# Liste de points
				 ("n", None),						# Nombre maximum de points théorique
				 ("height", None),					# Hauteur (nombre de lignes)
				 ("width", None),					# Largeur (nombre de colonnes)
				 ("wavelet", ctypes.c_ulong(1)), 	# Wavelet toujours à 1.
				 ("threshold", None),				# Seuil
				 ("watershed", None),				# Activation du Watershed
				 ("vol_min", ctypes.c_double(4)), 	# Vol minimum toujours à 4.
				 ("int_min", ctypes.c_double(0)), 	# Int minimum toujours à 0.
				 ("gauss_fit", None),				# Mode du Gaussian Fit
				 ("sigma_x", None),					# Valeur initiale du Sigma X
				 ("sigma_y", None),					# Valeur initiale du Sigma Y (*2 pour correspondre à métamorph, interet limité)
				 ("theta", None),					# Valeur Initiale du Theta
				 ("roi_size", None)])				# taille de la ROI

	##################################################
	def is_valid(self): return self._dll is not None

	##################################################
	def __init_args(self, height: int, width: int, threshold: float, watershed: bool, gauss_fit: int,
					sigma: float, theta: float, roi_size: int):
		"""
		Initialise les arguments necessaire au lancement de la DLL PALM externe.

		:param height: Hauteur des images.
		:param width: Largeur des images.
		:param threshold: Seuil pour la détection.
		:param watershed: Active ou désactive le mode watershed.
		:param gauss_fit: Mode d'ajustement Gaussien.
		:param sigma: Valeur initiale du sigma pour l'ajustement Gaussien.
		:param theta: Valeur initiale du theta pour l'ajustement Gaussien.
		:param roi_size: Taille de la région d'intérêt (ROI).
		:return: Dictionniare d'arguments pour la DLL (attention l'ordre doit être respecté).
		"""
		# Parsing
		n = get_max_points(height, width)  # Récupération d'un nombre de points maximum théorique
		if n != self._args["n"]: self._points = np.zeros((n,), dtype=np.float64)
		self._args["points"] = self._points.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
		self._args["n"] = ctypes.c_ulong(n)
		self._args["height"] = ctypes.c_ulong(height)
		self._args["width"] = ctypes.c_ulong(width)
		self._args["threshold"] = ctypes.c_double(threshold)
		self._args["watershed"] = ctypes.c_double(0 if watershed else 10)
		self._args["gauss_fit"] = ctypes.c_ushort(gauss_fit)
		self._args["sigma_x"] = ctypes.c_double(sigma)
		self._args["sigma_y"] = ctypes.c_double(sigma * 2)
		self._args["theta"] = ctypes.c_double(theta)
		self._args["roi_size"] = ctypes.c_ushort(roi_size)

	##################################################
	def __updata_args(self, image: np.ndarray):
		"""
		Met à jour les arguments necessaire au lancement de la DLL PALM externe.
		:param image: Image à envoyer
		"""
		self._points.fill(0)  # remise à 0 des points
		# Forcer le type de l'image en np.uint16 et "applati" l'image avant de la passer en pointeur
		self._args["image"] = np.asarray(image, dtype=np.uint16).flatten().ctypes.data_as(ctypes.POINTER(ctypes.c_ushort))

	##################################################
	def __run_image(self, image: np.ndarray, gauss_fit: int, plane: int = 1) -> pd.DataFrame:
		"""
		Exécute un traitement d'image avec une DLL PALM externe pour détecter des points dans une image.

		:param image: Image d'entrée 2D sous forme de tableau numpy d'entier.
		:param gauss_fit: Mode d'ajustement Gaussien.
		:param plane: Numéro du plan dans la pile
		:return: Liste des points détectés sous forme de dataframe contenant toutes les informations reçu de la DLL.
		"""
		self.__updata_args(image)
		self._dll.Process(*self._args.values())
		# self._dll._OpenPALMProcessing(*self._args.values())
		# self._dll._PALMProcessing()
		# self._dll._closePALMProcessing()

		return parse_palm_result(self._points, plane, gauss_fit, True)

	##################################################
	def run(self, stack: np.ndarray, threshold: float, watershed: bool, gauss_fit: int,
			sigma: float, theta: float, roi_size: int, planes: Optional[list[int]] = None) -> pd.DataFrame:
		"""
		Exécute un traitement d'image avec une DLL PALM externe pour détecter des points dans une pile ou une image.

		:param stack: Pile d'images en entrée sous forme de tableau numpy (possibilité d'envoyer une image directement).
		:param threshold: Seuil pour la détection.
		:param watershed: Active ou désactive le mode watershed.
		:param gauss_fit: Mode d'ajustement Gaussien (défini par `get_gaussian_mode`).
		:param sigma: Valeur initiale du sigma pour l'ajustement Gaussien.
		:param theta: Valeur initiale du theta pour l'ajustement Gaussien.
		:param roi_size: Taille de la région d'intérêt (ROI).
		:param planes: Liste des plans à analyser (None pour tous les plans).
		:return: Liste des points détectés sous forme de dataframe contenant toutes les informations reçu de la DLL.
		"""
		height, width = stack.shape[-2:]  # Récupère les deux dernières dimensions
		self.__init_args(height, width, threshold, watershed, gauss_fit, sigma, theta, roi_size)

		if stack.ndim == 2: return self.__run_image(stack, gauss_fit)

		n_planes = stack.shape[0]
		if planes is None: planes = list(range(n_planes))
		else: planes = [p for p in planes if isinstance(p, int) and 0 <= p < n_planes]

		results = []
		# n_planes = len(planes)
		# start_time = time.time()  # Temps de début
		for index, i in enumerate(planes):
			points = self.__run_image(stack[i], gauss_fit, i + 1)
			results.append(points)  # Ajouter à la liste
		# 	if index % 50 == 0 or index == n_planes - 1:
		# 		elapsed_time = time.time() - start_time  # Temps écoulé
		# 		avg_time_per_plane = elapsed_time / (index + 1)  # Temps moyen par plan
		# 		remaining_planes = n_planes - (index + 1)  # Plans restants
		# 		estimated_time_remaining = avg_time_per_plane * remaining_planes  # Temps estimé restant
		# 		# Affichage avec le temps total écoulé et le temps estimé restant
		# 		sys.stdout.write(f"\rRun PALM on Plane {i} ({(index + 1) / n_planes * 100:.0f}%) "
		# 						 f"- Total time elapsed: {format_time(elapsed_time)} "
		# 						 f"- Estimated time remaining: {format_time(estimated_time_remaining)}"
		# 						 f"- Total time to finish: {format_time(elapsed_time + estimated_time_remaining)}")
		# 		sys.stdout.flush()
		# print()  # Ajoute un saut de ligne à la fin pour éviter d'écraser la dernière mise à jour

		# Créer le dataframe final peut-être plus rapide que le mettre à jour à chaque iteration (réallocation des milliers de fois)
		res = pd.concat(results, ignore_index=True)
		res["Id"] = range(1, len(res) + 1)  # Mise à jour de l'ID dans le tableau
		return res

	##################################################
	def auto_threshold(self, image: np.ndarray, roi_size: int = 7, max_iterations: int = 4):
		"""
		Calcule un seuil automatique basé sur la segmentation de l'image.

		:param image: Image 2D sous forme de tableau NumPy.
		:param roi_size: Taille des régions d'intérêt (ROI) utilisées pour la segmentation (par défaut 7).
		:param max_iterations: Nombre d'itérations pour affiner le seuil (par défaut 4).
		:return: Seuil calculé (écart type final).
		"""
		mask = np.zeros_like(image, dtype=bool)  # Creation du masque
		std_dev = float(np.std(image))			 # Calcul initial de l'écart type
		roi_2 = float(roi_size) / 2.0			 # Demi-taille de la zone ROI
		height, width = image.shape				 # Récupération de la taille de l'image

		for _ in range(max_iterations):
			# Lancement d'un PALM et récupération de la liste des points (format (x, y))
			points = self.run(image, std_dev, False, 0, 1, math.pi / 4.0, roi_size)
			# Mise à jour du masque basé sur le résultat du PALM
			# mask.fill(0)
			for x, y in zip(points['X'], points['Y']):
				# Définir les limites de la ROI tout en respectant les bords de l'image
				x_min, x_max = max(0, int(x - roi_2)), min(width, int(x + roi_2))
				y_min, y_max = max(0, int(y - roi_2)), min(height, int(y + roi_2))
				# Mettre à jour le masque pour les pixels dans la ROI
				mask[y_min:y_max, x_min:x_max] = True

			# Calcul de l'écart type pour les pixels hors segmentation
			pixels_outside = image[~mask]
			if len(pixels_outside) > 0: std_dev = np.std(pixels_outside)
			else: break  # pragma: no cover	(ce else est presque impossible à avoir)

		return std_dev

# ##################################################
# def run_thread_image(self, image: np.ndarray, threshold: float, watershed: bool, gauss_fit: int,
# 			  sigma: float, theta: float, roi_size: int, plane: int = 1) -> pd.DataFrame:
# 	"""
# 	Exécute un traitement d'image avec une DLL PALM externe pour détecter des points dans une image.
#
# 	:param image: Image d'entrée 2D sous forme de tableau numpy d'entier.
# 	:param threshold: Seuil pour la détection.
# 	:param watershed: Active ou désactive le mode watershed.
# 	:param gauss_fit: Mode d'ajustement Gaussien.
# 	:param sigma: Valeur initiale du sigma pour l'ajustement Gaussien.
# 	:param theta: Valeur initiale du theta pour l'ajustement Gaussien.
# 	:param roi_size: Taille de la région d'intérêt (ROI).
# 	:param plane: Numéro du plan dans la pile
# 	:return: Liste des points détectés sous forme de dataframe contenant toutes les informations reçu de la DLL.
# 	"""
# 	# En multithreading, la dll doit être chargé pour chaque process
# 	dll = load_dll("CPU")
# 	args = self.__get_args(image, threshold, watershed, gauss_fit, sigma, theta, roi_size)
# 	# Running
# 	dll._OpenPALMProcessing(*args.values())
# 	dll._PALMProcessing()
# 	dll._closePALMProcessing()
#
# 	return parse_palm_result(np.ctypeslib.as_array(args["points"], shape=(args["n"].value,)), plane, gauss_fit, True)
#
# ##################################################
# def run_multithread_stack(self, stack: np.ndarray, threshold: float, watershed: bool, gauss_fit: int,
# 			  sigma: float, theta: float, roi_size: int, planes: Optional[list[int]] = None) -> pd.DataFrame:
# 	"""
# 	Exécute un traitement d'image avec une DLL PALM externe pour détecter des points dans une image.
#
# 	:param stack: Pile d'image d'entrée sous forme de tableau numpy.
# 	:param threshold: Seuil pour la détection.
# 	:param watershed: Active ou désactive le mode watershed.
# 	:param gauss_fit: Mode d'ajustement Gaussien (défini par `get_gaussian_mode`).
# 	:param sigma: Valeur initiale du sigma pour l'ajustement Gaussien.
# 	:param theta: Valeur initiale du theta pour l'ajustement Gaussien.
# 	:param roi_size: Taille de la région d'intérêt (ROI).
# 	:param planes: Liste des plans à analyser (None = tous les plans).
# 	:return: Liste des points détectés sous forme de dataframe contenant toutes les informations reçu de la DLL.
# 	"""
# 	n_planes = stack.shape[0]
# 	if planes is None: planes = list(range(n_planes))
# 	else: planes = [p for p in planes if isinstance(p, int) and 0 <= p < n_planes]
#
# 	# Exécution parallèle impossible tant que la DLL ne fonctionne pas en une fonction unique et utilise un objet palm en pointeur
# 	results = []
# 	with ThreadPoolExecutor() as executor:
# 		futures = {executor.submit(self.run_thread_image, stack[i], threshold, watershed, gauss_fit, sigma, theta, roi_size, i + 1): i for i in planes}
# 		for future in futures: results.append(future.result())
#
# 	# Créer le dataframe final peut-être plus rapide que le mettre à jour à chaque iteration (réallocation des milliers de fois)
# 	res = pd.concat(results, ignore_index=True)
# 	res = res.sort_values(by=["Plane", "Index"]).reset_index(drop=True)	# Tri si jamais le multithread à mélangé les sorties
# 	res["Id"] = range(1, len(res) + 1)  # Mise à jour de l'ID dans le tableau
# 	return res
