"""
Ce sous-package contient les classes d'interface utilisateur Napari (QT).

**Modules disponibles** :

- PALMTracerWidget : Widget principal de l'application.
- HighResViewer : Widget secondaire pour l'affichage de résultats Haute résolution.

**Fonctionnalités principales** :

- Tous les modules peuvent être importés directement via `from palm_tracer.UI import <module>`.

"""

from . import Utils
from .AlignmentWidget import AlignmentWidget, open_alignment
from .Astigmatism3DWidget import Astigmatism3DWidget, open_astigmatism3d
from .GraphViewerWidget import GraphViewerWidget
from .PALMTracerWidget import PALMTracerWidget
from .Viewer3DWidget import open_viewer3d, Viewer3DWidget
from .ViewerHRWidget import open_viewerhr, ViewerHRWidget

__all__ = ["GraphViewerWidget", "PALMTracerWidget", "Viewer3DWidget", "ViewerHRWidget", "AlignmentWidget", "Astigmatism3DWidget",
		   "Utils", "open_viewer3d", "open_viewerhr", "open_alignment", "open_astigmatism3d"]
