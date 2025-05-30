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
from .Drawing import draw_test_section, get_color_map_by_name
from .FileIO import open_json, open_tif, save_json, save_tif
from .Logger import Logger
from .Monitoring import Monitoring
from .Utils import add_extension, add_suffix, get_last_file, get_timestamp_for_files, print_error, print_success, print_warning

# Définir la liste des symboles exportés
__all__ = ["Drawing", "FileIO", "Logger", "Monitoring", "Utils",
		   "draw_test_section", "get_color_map_by_name",
		   "open_json", "save_json", "open_tif", "save_tif",
		   "add_extension", "add_suffix", "get_timestamp_for_files", "get_last_file", "print_error", "print_success", "print_warning"]
