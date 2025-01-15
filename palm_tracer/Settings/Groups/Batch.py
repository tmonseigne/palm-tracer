"""
Fichier contenant la classe `Batch` dérivée de `BaseSettingGroup`, qui regroupe les paramètres de Batch nécessaires à la configuration de PALM Tracer.
"""

import os
from dataclasses import dataclass
from typing import cast

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import Combo, FileList


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
	def get_path(self, suffix: str = "_PALM_Tracer") -> str:
		"""
		Génère un chemin basé sur les fichiers du Batch et le mode sélectionné.

		:param suffix: Suffixe à ajouter au nom du dossier créé.
		:return: Chemin complet du dossier généré.
        """

		file_list = cast(FileList, self._settings["Files"])
		# Si aucun fichier n'est présent
		if not file_list.get_list(): return f"{os.getcwd()}/{suffix}"  # Retourne le chemin courant

		# Si Mode "Only one". Utiliser le fichier sélectionné dans FileList.
		if self._settings["Mode"].get_value() == 0: file = file_list.get_selected()
		# Sinon. Utiliser le premier fichier de la liste.
		else: file = file_list.get_list()[0]

		if file:
			base_path, _ = os.path.splitext(file)
			return f"{base_path}{suffix}"
		# if not file est impossible, mais au cas où.
		return f"{os.getcwd()}/{suffix}" # pragma: no cover
