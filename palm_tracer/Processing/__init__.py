"""
Ce sous-package contient les fonctions de traitement pour le projet.

**Modules disponibles** :

- DLL : Fournit des fonctions en lien avec les DLL Palm.
- Threshold : Fournit des fonctions de seuillage automatique.

**Fonctionnalités principales** :

- Tous les modules peuvent être importés directement via `from palm_tracer.Processing import <module>`.

"""

# Exemple d'importation des modules pour un accès direct
from . import Gallery, Parsing, Visualization
from .Grapher import Grapher
from .Palm import Palm

# Définir la liste des symboles exportés
__all__ = ["Gallery", "Grapher", "Palm", "Parsing", "Visualization"]
