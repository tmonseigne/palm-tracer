"""
Ce sous-package gère les différents types de paramètres.

**Composants principaux** :

- :class:`.BaseSettingTypes` : Classe principale pour la gestion des paramètres ajustables.
- :class:`.BrowseFile` : Classe pour un paramètre spécifique de type recherche de fichier.
- :class:`.CheckBox` : Classe pour un paramètre spécifique de type case à cocher.
- :class:`.CheckRangeFloat` : Classe pour un paramètre spécifique de type intervalle de nombre réel à activer ou non.
- :class:`.CheckRangeInt` : Classe pour un paramètre spécifique de type intervalle de nombre entier à activer ou non.
- :class:`.Combo` : Classe pour un paramètre spécifique de type liste déroulante.
- :class:`.FileList` : Classe pour un paramètre spécifique de type liste de fichier.
- :class:`.SpinFloat` : Classe pour un paramètre spécifique de type nombre réel.
- :class:`.SpinInt` : Classe pour un paramètre spécifique de type nombre entier.

**Fonctionnalités principales** :

- Permet un accès direct aux classes principales via `from palm_tracer.Settings.Types import <classe>`.

"""
# Importation explicite des classes pour qu'elles soient accessibles directement
from .BaseSettingType import BaseSettingType
from .BaseUIType import BaseUIType
from .BrowseFile import BrowseFile
from .Button import Button
from .ButtonGroup import ButtonGroup
from .CheckBox import CheckBox
from .CheckRangeFloat import CheckRangeFloat
from .CheckRangeInt import CheckRangeInt
from .Combo import Combo
from .FileList import FileList
from .SignalWrapper import SignalWrapper
from .SpinFloat import SpinFloat
from .SpinInt import SpinInt

# Définir la liste des symboles exportés
__all__ = ["BaseSettingType", "BaseUIType", "SignalWrapper",
		   "BrowseFile", "Button", "ButtonGroup", "CheckBox", "Combo", "FileList", "SpinFloat", "SpinInt",
		   "CheckRangeFloat", "CheckRangeInt"]
