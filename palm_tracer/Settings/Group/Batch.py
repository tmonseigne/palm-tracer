"""
Fichier contenant la classe `Batch` dérivée de `BaseSettingGroup`, qui regroupe les paramètres de Batch nécessaires
à la configuration de PALM Tracer.

**Attributs de la classe Batch** :

  - **Add File (FileSetting)** : Ajout d'un fichier au Batch.
  - **Files (ComboSetting)** : Liste des fichiers au Batch.
  - **Mode (ComboSetting)** : Méthode d'utilisation du Batch (chaque fichier est traité séparément ou l'ensemble des fichiers correspondent à une seule
  acquisition).

.. todo::
   Changer le Add File et Files vers un seul setting FileList plus complet

"""

from dataclasses import dataclass

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
	setting_list = {
			"Add File": [FileSetting, ["Add File"]],
			"Files":    [ComboSetting, ["Files", [""]]],
			"Mode":     [ComboSetting, ["Mode", ["Each File separately", "All in One"]]]
			}
