"""
Ce sous-package gère les différents types de paramètres.

**Composants principaux** :

- `BaseSettingTypes` : Classe principale pour la gestion des paramètres ajustables.
- `BrowseFile` : Classe pour un paramètre spécifique de type recherche de fichier.
- `CheckBox` : Classe pour un paramètre spécifique de type case à cocher.
- `Combo` : Classe pour un paramètre spécifique de type liste déroulante.
- `SpinFloat` : Classe pour un paramètre spécifique de type nombre réel.
- `SpinInt` : Classe pour un paramètre spécifique de type nombre entier.

**Fonctionnalités principales** :

- Permet un accès direct aux classes principales via `from palm_tracer.Settings.Types import <classe>`.

"""

from typing import Any

# Importation explicite des classes pour qu'elles soient accessibles directement
from .BaseSettingType import BaseSettingType
from .BrowseFile import BrowseFile
from .CheckBox import CheckBox
from .Combo import Combo
from .SpinFloat import SpinFloat
from .SpinInt import SpinInt


def create_setting_from_dict(data: dict[str, Any]) -> "BaseSettingType":
	""" Créé un setting en fonction d'un dictionnaire en entrée. """
	if not "type" in data: raise ValueError("Le dictionnaire ne contient pas la clé 'type'.")
	if data["type"] == "BrowseFile": return BrowseFile.from_dict(data)
	elif data["type"] == "CheckBox": return CheckBox.from_dict(data)
	elif data["type"] == "Combo": return Combo.from_dict(data)
	elif data["type"] == "SpinFloat": return SpinFloat.from_dict(data)
	elif data["type"] == "SpinInt": return SpinInt.from_dict(data)
	raise ValueError("Le dictionnaire ne contient pas un type de paramètre valide.")


# Définir la liste des symboles exportés
__all__ = ["BaseSettingType", "create_setting_from_dict",
		   "BrowseFile", "CheckBox", "Combo", "SpinFloat", "SpinInt"]
