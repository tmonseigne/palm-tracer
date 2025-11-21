"""
Ce sous-package contient les classes d'interface utilisateur Napari (QT).

**Modules disponibles** :

- PALMTracerWidget : Widget principal de l'application.
- HighResViewer : Widget secondaire pour l'affichage de résultats Haute résolution.

**Fonctionnalités principales** :

- Tous les modules peuvent être importés directement via `from palm_tracer.UI import <module>`.

"""

from .GraphViewerWidget import GraphViewerWidget
from .PALMTracerWidget import PALMTracerWidget
from .Viewer3DWidget import open_viewer3d_from_plugin, Viewer3DWidget

__all__ = ["GraphViewerWidget", "PALMTracerWidget", "Viewer3DWidget", "open_viewer3d_from_plugin"]
