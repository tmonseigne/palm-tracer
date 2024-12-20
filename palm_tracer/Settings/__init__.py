"""
Ce sous-module gère les paramètres de configuration et l'interface utilisateur de ces paramètres.

**Composants principaux** :

- `Settings` : Classe principale pour la gestion des paramètres.
- `SettingTypes` : Ensemble de classes et d'outils pour créer et manipuler les éléments de l'interface utilisateur, tels que les paramètres ajustables.

**Fonctionnalités principales** :

- Permet un accès direct aux classes principales via `from palm_tracer.Settings import <classe>`.
- Tous les modules peuvent être importés directement via `from palm_tracer.Settings  import <module>`.

"""

# Importation explicite des classes pour qu'elles soient accessibles directement
from .Settings import Settings

# Définir la liste des symboles exportés
__all__ = ["Settings", "Groups", "Types"]
