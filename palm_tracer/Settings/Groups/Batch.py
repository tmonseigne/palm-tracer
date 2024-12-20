"""
Fichier contenant la classe `Batch` dérivée de `BaseSettingGroup`, qui regroupe les paramètres de Batch nécessaires
à la configuration de PALM Tracer.

**Attributs de la classe Batch** :

  - **Add File (BrowseFile)** : Ajout d'un fichier au Batch.
  - **Files (Combo)** : Liste des fichiers au Batch.
  - **Mode (Combo)** : Méthode d'utilisation du Batch (chaque fichier est traité séparément ou l'ensemble des fichiers correspondent à une seule
  acquisition).

.. todo::
   Changer le Add File et Files vers un seul setting FileList plus complet

"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import Combo, BrowseFile


##################################################
@dataclass
class Batch(BaseSettingGroup):
	"""
	Classe contenant les informations de calibration :

	Attributs :
			- **Add File (BrowseFile)** : Ajout d'un fichier au Batch.
			- **Files (Combo)** : Liste des fichiers au Batch.
			- **Mode (Combo)** : Méthode d'utilisation du Batch
			  (chaque fichier est traité séparément ou l'ensemble des fichiers correspondent à une seule acquisition).
	"""

	setting_list = {
			"Add File": [BrowseFile, ["Add File", ""]],
			"Files":    [Combo, ["Files", 0, [""]]],
			"Mode":     [Combo, ["Mode", 0, ["Each File separately", "All in One"]]],
			}
