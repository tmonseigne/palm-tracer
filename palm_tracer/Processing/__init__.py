"""
Ce sous-package contient les fonctions de traitement pour le projet.

**Modules disponibles** :

- DLL : Fournit des fonctions en lien avec les DLL Palm.
- Threshold : Fournit des fonctions de seuillage automatique.

**Fonctionnalités principales** :

- Tous les modules peuvent être importés directement via `from palm_tracer.Processing import <module>`.

"""

# Exemple d'importation des modules pour un accès direct
from .DLL import load_dll, run_palm_image_dll, run_palm_stack_dll, run_tracking_dll
from .Gallery import make_gallery
from .Threshold import auto_threshold, auto_threshold_dll
from .Visualization import normalize_data, plot_histogram, plot_plane_heatmap, plot_plane_violin, render_hr_image, render_roi

# Définir la liste des symboles exportés
__all__ = ["DLL", "Gallery", "Threshold", "Visualization",
		   "load_dll", "run_palm_image_dll", "run_palm_stack_dll", "run_tracking_dll",
		   "make_gallery",
		   "auto_threshold", "auto_threshold_dll",
		   "normalize_data",  "plot_histogram", "plot_plane_heatmap", "plot_plane_violin", "render_hr_image", "render_roi"]
