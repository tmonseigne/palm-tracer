"""
Ce sous-package gère les groupes de paramètres.

**Fonctionnalités principales** :

- Permet un accès direct aux classes principales via `from palm_tracer.Settings.Group import <classe>`.

"""

# Importation explicite des classes pour qu'elles soient accessibles directement
from .BaseSettingGroup import BaseSettingGroup
from .BaseUIGroup import BaseUIGroup
from .Batch import Batch
from .BeadsExtraction import BeadsExtraction
from .BlinkingReconnection import BlinkingReconnection
from .Calibration import Calibration
from .Filters import Filters
from .FiltersL import FiltersL
from .FiltersT import FiltersT
from .Gallery import Gallery
from .GaussianFit import GaussianFit
from .Graph import Graph
from .GraphDisplay import GraphDisplay
from .HR import HR
from .HR3D import HR3D
from .HRGaussian import HRGaussian
from .Localization import Localization
from .SplineFit import SplineFit
from .Tracking import Tracking
from .TracksCompute import TracksCompute
from .Visualization3D import Visualization3D

# Définir la liste des symboles exportés
__all__ = ["BaseSettingGroup", "BaseUIGroup",
		   "Batch", "Calibration",
		   "Filters", "FiltersL", "FiltersT",
		   "Localization", "GaussianFit", "SplineFit", "BeadsExtraction",
		   "Tracking", "BlinkingReconnection", "TracksCompute",
		   "Gallery", "Graph", "GraphDisplay", "HR", "HRGaussian", "HR3D", "Visualization3D"]
