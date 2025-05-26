"""
Ce sous-package contient les fonctions de traitement pour le projet.

**Modules disponibles** :

- DLL : Fournit des fonctions en lien avec les DLL Palm.
- Threshold : Fournit des fonctions de seuillage automatique.

**Fonctionnalités principales** :

- Tous les modules peuvent être importés directement via `from palm_tracer.Processing import <module>`.

"""

# Exemple d'importation des modules pour un accès direct
from . import Parsing
from .Gallery import make_gallery
from .Palm import Palm
from .Visualization import normalize_data, plot_histogram, plot_plane_heatmap, plot_plane_violin, render_hr_image, render_roi

# Définir la liste des symboles exportés
__all__ = ["Parsing", "Gallery", "Palm", "Visualization",
		   "make_gallery",
		   "normalize_data", "plot_histogram", "plot_plane_heatmap", "plot_plane_violin", "render_hr_image", "render_roi"]
