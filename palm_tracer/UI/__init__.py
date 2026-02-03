"""
Ce sous-package contient les classes d'interface utilisateur Napari (QT).

**Modules disponibles** :

- PALMTracerWidget : Widget principal de l'application.
- HighResViewer : Widget secondaire pour l'affichage de résultats Haute résolution.

**Fonctionnalités principales** :

- Tous les modules peuvent être importés directement via `from palm_tracer.UI import <module>`.

"""

from .AlignmentWidget import AlignmentWidget
from .Astigmatism3DWidget import Astigmatism3DWidget
from .BaseStandAloneWidget import BaseStandAloneWidget
from .FileMigratorWidget import FileMigratorWidget
from .GraphViewerWidget import GraphViewerWidget
from .PALMTracerWidget import PALMTracerWidget
from .Viewer3DWidget import Viewer3DWidget
from .ViewerHRWidget import ViewerHRWidget

__all__ = ["PALMTracerWidget", "Viewer3DWidget", "ViewerHRWidget", "BaseStandAloneWidget",
		   "AlignmentWidget", "Astigmatism3DWidget", "FileMigratorWidget", "GraphViewerWidget"]
