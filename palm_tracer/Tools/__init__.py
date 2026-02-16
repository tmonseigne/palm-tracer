"""
Ce sous-package contient des outils utilitaires pour le projet SampleMaker.

**Modules disponibles** :

- Drawing : Fournit des fonctions de dessin génériques.
- Monitoring : Fournit un module de surveillance des ressources système pendant l'exécution de tests.
- Utils : Fournit des fonctions d'assistance génériques.

**Fonctionnalités principales** :

- Tous les modules peuvent être importés directement via `from palm_tracer.Tools import <module>`.

"""

# Exemple d'importation des modules pour un accès direct
from .FileMigrator import FileMigrator
from .Logger import Logger
from .Monitoring import Monitoring

# Définir la liste des symboles exportés
__all__ = ["FileIO", "Ui", "FileMigrator", "Logger", "Monitoring"]
