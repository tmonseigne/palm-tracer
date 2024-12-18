"""
Ce sous-module gère les groupes de paramètres.

**Composants principaux** :

- `BaseSettingGroup` : Classe principale pour la gestion des groupes.
- `Batch` : Classe regroupant les paramètres du Batch.
- `Calibration` : Classe regroupant les paramètres de la Calibration.
- `Localisation` : Classe regroupant les paramètres de la Localisation.
- `GaussianFit` : Classe regroupant les paramètres du Gaussian Fit.
- `SettingTypes` : Ensemble de classes et d'outils pour créer et manipuler les éléments de l'interface utilisateur, tels que les paramètres ajustables.

**Fonctionnalités principales** :

- Permet un accès direct aux classes principales via `from palm_tracer.Settings.Group import <classe>`.
- Tous les modules peuvent être importés directement via `from palm_tracer.Settings.Group import <module>`.

"""

# Importation explicite des classes pour qu'elles soient accessibles directement
from .BaseSettingGroup import BaseSettingGroup
from .Batch import Batch
from .Calibration import Calibration
from .GaussianFit import GaussianFit
from .Localisation import Localisation

# Définir la liste des symboles exportés
__all__ = ["BaseSettingGroup",
		   "Batch",
		   "Calibration",
		   "Localisation", "GaussianFit"]
