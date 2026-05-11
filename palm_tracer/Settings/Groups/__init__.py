"""
Ce sous-package gère les groupes de paramètres.

**Fonctionnalités principales** :

- Permet un accès direct aux classes principales via `from palm_tracer.Settings.Group import <classe>`.

"""

from typing import Any

# Importation explicite des classes pour qu'elles soient accessibles directement
from .BaseSettingGroup import BaseSettingGroup
from .Batch import Batch
from .BeadsExtraction import BeadsExtraction
from .BlinkingReconnection import BlinkingReconnection
from .Calibration import Calibration
from .Filters import Filters
from .FiltersL import FiltersL
from .FiltersT import FiltersT
from .Gallery import Gallery
from .GaussianFit import GaussianFit
from .Localization import Localization
from .SplineFit import SplineFit
from .Tracking import Tracking
from .TracksCompute import TracksCompute
from .VisualizationGraph import VisualizationGraph
from .VisualizationHR import VisualizationHR


# Définir la liste des symboles exportés
__all__ = ["BaseSettingGroup",
		   "Batch", "Calibration",
		   "Filters", "FiltersL", "FiltersT",
		   "Localization", "GaussianFit", "SplineFit", "BeadsExtraction",
		   "Tracking", "BlinkingReconnection", "TracksCompute",
		   "Gallery", "VisualizationHR", "VisualizationGraph"]
