"""
Ce sous-package contient les classes d'interface utilisateur Napari (QT).

**Modules disponibles** :

- PALMTracerWidget : Widget principal de l'application.
- HighResViewer : Widget secondaire pour l'affichage de résultats Haute résolution.

**Fonctionnalités principales** :

- Tous les modules peuvent être importés directement via `from palm_tracer.UI import <module>`.

"""

from .PALMTracerWidget import PALMTracerWidget

__all__ = ["PALMTracerWidget"]
