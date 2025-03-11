"""
Ce sous-package gère les différents types de paramètres.

**Composants principaux** :

- :class:`.BaseSettingTypes` : Classe principale pour la gestion des paramètres ajustables.
- :class:`.BrowseFile` : Classe pour un paramètre spécifique de type recherche de fichier.
- :class:`.CheckBox` : Classe pour un paramètre spécifique de type case à cocher.
- :class:`.CheckRangeFloat` : Classe pour un paramètre spécifique de type interval de nombre réel à activer ou non.
- :class:`.CheckRangeInt` : Classe pour un paramètre spécifique de type interval de nombre entier à activer ou non.
- :class:`.Combo` : Classe pour un paramètre spécifique de type liste déroulante.
- :class:`.FileList` : Classe pour un paramètre spécifique de type liste de fichier.
- :class:`.SpinFloat` : Classe pour un paramètre spécifique de type nombre réel.
- :class:`.SpinInt` : Classe pour un paramètre spécifique de type nombre entier.

**Fonctionnalités principales** :

- Permet un accès direct aux classes principales via `from palm_tracer.Settings.Types import <classe>`.

"""

from typing import Any

# Importation explicite des classes pour qu'elles soient accessibles directement
from .BaseSettingType import BaseSettingType
from .BrowseFile import BrowseFile
from .Button import Button
from .CheckBox import CheckBox
from .CheckRangeFloat import CheckRangeFloat
from .CheckRangeInt import CheckRangeInt
from .Combo import Combo
from .FileList import FileList
from .SignalWrapper import SignalWrapper
from .SpinFloat import SpinFloat
from .SpinInt import SpinInt


def create_setting_from_dict(data: dict[str, Any]) -> "BaseSettingType":
	""" Créé un setting en fonction d'un dictionnaire en entrée. """
	if not "type" in data: raise ValueError("Le dictionnaire ne contient pas la clé 'type'.")
	if data["type"] == "BrowseFile": return BrowseFile.from_dict(data)
	elif data["type"] == "Button": return Button.from_dict(data)
	elif data["type"] == "CheckBox": return CheckBox.from_dict(data)
	elif data["type"] == "Combo": return Combo.from_dict(data)
	elif data["type"] == "FileList": return FileList.from_dict(data)
	elif data["type"] == "SpinFloat": return SpinFloat.from_dict(data)
	elif data["type"] == "SpinInt": return SpinInt.from_dict(data)
	elif data["type"] == "CheckRangeInt": return CheckRangeInt.from_dict(data)
	elif data["type"] == "CheckRangeFloat": return CheckRangeFloat.from_dict(data)
	raise ValueError("Le dictionnaire ne contient pas un type de paramètre valide.")


# Définir la liste des symboles exportés
__all__ = ["BaseSettingType", "create_setting_from_dict", "SignalWrapper",
		   "BrowseFile","Button", "CheckBox", "Combo", "FileList", "SpinFloat", "SpinInt",
		   "CheckRangeFloat", "CheckRangeInt"]
