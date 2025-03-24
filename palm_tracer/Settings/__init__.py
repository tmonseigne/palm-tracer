"""
Ce sous-package gère les paramètres de configuration et l'interface utilisateur de ces paramètres.

**Composants principaux** :

- :class:`.Settings` : Classe principale pour la gestion des paramètres.
- `Setting.Groups` : Ensemble de classes et d'outils pour créer et manipuler des ensembles de paramètres.
- `Setting.Types` : Ensemble de classes et d'outils pour créer et manipuler les éléments de l'interface utilisateur, tels que les paramètres ajustables.

**Fonctionnalités principales** :

- Permet un accès direct aux classes principales via `from palm_tracer.Settings import <classe>`.
- Tous les modules peuvent être importés directement via `from palm_tracer.Settings import <module>`.

"""

# Importation explicite des classes pour qu'elles soient accessibles directement
from . import Groups, Types
from .Settings import Settings

# Définir la liste des symboles exportés
__all__ = ["Settings", "Groups", "Types"]
