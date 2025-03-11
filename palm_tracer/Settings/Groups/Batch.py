"""
Fichier contenant la classe :class:`Batch` dérivée de :class:`.BaseSettingGroup`, qui regroupe les paramètres de Batch nécessaires à la configuration de PALM Tracer.
"""

import os
from dataclasses import dataclass
from typing import cast

import numpy as np

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import Combo, FileList
from palm_tracer.Tools import open_tif


##################################################
@dataclass
class Batch(BaseSettingGroup):
	"""
	Classe contenant les informations de batch de fichiers :

	Attributs :
			- **Files (FileList)** : Liste des fichiers au Batch.
			- **Mode (Combo)** : Méthode d'utilisation du Batch
			  (Un seul fichier est traité ou chaque fichier est traité séparément ou l'ensemble des fichiers correspondent à une seule acquisition).
	"""

	label: str = "Batch"
	setting_list = {
			"Files": [FileList, ["Files", 0, []]],
			"Mode":  [Combo, ["Mode", 0, ["Only one", "Each File separately", "All in One"]]],
			}

	##################################################
	def get_paths(self, suffix: str = "_PALM_Tracer") -> list[str]:
		"""
		Génère un chemin basé sur les fichiers du Batch et le mode sélectionné.

		:param suffix: Suffixe à ajouter au nom du dossier créé.
		:return: Chemin complet du dossier généré.
        """
		file_list = cast(FileList, self._settings["Files"])
		mode = self._settings["Mode"].get_value()

		files = file_list.get_list().copy()
		if files:  # Si aucun fichier n'est présent
			if mode == 0: files = [file_list.get_selected()]
			elif mode == 2: files = [file_list.get_list()[0]]
			res = list[str]()
			for file in files:
				base_path, _ = os.path.splitext(file)
				res.append(f"{base_path}{suffix}")
			return res

		return [f"{os.getcwd()}/{suffix}"]  # Retourne le chemin courant si aucun fichiers

	##################################################
	def get_stacks(self) -> list[np.ndarray]:
		"""
		Récupère la liste de piles en fonction des paramètres
		:return: Une liste de pile en fonction du Batch (une seule pile, un ensemble de piles concaténées ou un groupe de pile)
		"""
		res = list[np.ndarray]()
		file_list = cast(FileList, self._settings["Files"])
		files = file_list.get_list()
		mode = self._settings["Mode"].get_value()
		if not files: return res  # Aucun fichier dans le Batch
		if mode == 0:  # Mode Only One
			res.append(open_tif(file_list.get_selected()))
		else:  # Mode fichiers séparés ou concaténés
			for file in files:
				res.append(open_tif(file))
			if mode == 2:  # Mode fichiers Concaténés
				res = [np.concatenate(res, axis=0)]
		return res
