"""
Fichier contenant la classe `Batch` dérivée de `BaseSettingGroup`, qui regroupe les paramètres de Batch nécessaires
à la configuration de PALM Tracer.

**Attributs de la classe Batch** :

  - **Add File (FileSetting)** : Ajout d'un fichier au Batch.
  - **Files (ComboSetting)** : Liste des fichiers au Batch.
  - **Mode (ComboSetting)** : Méthode d'utilisation du Batch (chaque fichier est traité séparément ou l'ensemble des fichiers correspondent à une seule
  acquisition).
"""

from dataclasses import dataclass
from typing import Any

from palm_tracer.Settings.Group.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.SettingTypes import ComboSetting, FileSetting


##################################################
@dataclass
class Batch(BaseSettingGroup):
	"""
	Classe contenant les informations de calibration :

	Attributs :

		- **Add File (FileSetting)** : Ajout d'un fichier au Batch.
		- **Files (ComboSetting)** : Liste des fichiers au Batch.
		- **Mode (ComboSetting)** : Méthode d'utilisation du Batch
		  (chaque fichier est traité séparément ou l'ensemble des fichiers correspondent à une seule acquisition).
	"""

	##################################################
	def initialize(self):
		""" Initialise le dictionnaire de paramètres. """
		super().initialize()  # Appelle l'initialisation de la classe mère.
		self._settings["Add File"] = FileSetting(label="Add File")
		self._settings["Files"] = ComboSetting(label="Files", choices=[])
		self._settings["Mode"] = ComboSetting(label="Mode", choices=["Each File separately", "All in One"])

	##################################################
	@classmethod
	def from_dict(cls, data: dict[str, Any]) -> "Batch":
		""" Créé une instance de la classe à partir d'un dictionnaire. """
		res = cls()
		res.active = data.get("active", False)
		return res
