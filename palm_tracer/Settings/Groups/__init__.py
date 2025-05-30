"""
Ce sous-package gère les groupes de paramètres.

**Fonctionnalités principales** :

- Permet un accès direct aux classes principales via `from palm_tracer.Settings.Group import <classe>`.

"""

from typing import Any

# Importation explicite des classes pour qu'elles soient accessibles directement
from .BaseSettingGroup import BaseSettingGroup
from .Batch import Batch
from .Calibration import Calibration
from .Filtering import Filtering
from .FilteringGF import FilteringGF
from .FilteringT import FilteringT
from .Gallery import Gallery
from .GaussianFit import GaussianFit
from .Localization import Localization
from .SplineFit import SplineFit
from .Tracking import Tracking
from .VisualizationGraph import VisualizationGraph
from .VisualizationHR import VisualizationHR


##################################################
def create_group_from_dict(data: dict[str, Any]) -> "BaseSettingGroup":
	"""Créé un setting en fonction d'un dictionnaire en entrée."""
	if not "type" in data: raise ValueError("Le dictionnaire ne contient pas la clé 'type'.")
	if data["type"] == "Batch": return Batch.from_dict(data)
	elif data["type"] == "Calibration": return Calibration.from_dict(data)
	elif data["type"] == "Localization": return Localization.from_dict(data)
	elif data["type"] == "GaussianFit": return GaussianFit.from_dict(data)
	elif data["type"] == "SplineFit": return SplineFit.from_dict(data)
	elif data["type"] == "Tracking": return Tracking.from_dict(data)
	elif data["type"] == "Gallery": return Gallery.from_dict(data)
	elif data["type"] == "VisualizationHR": return VisualizationHR.from_dict(data)
	elif data["type"] == "VisualizationGraph": return VisualizationGraph.from_dict(data)
	elif data["type"] == "Filtering": return Filtering.from_dict(data)
	elif data["type"] == "FilteringGF": return FilteringGF.from_dict(data)
	elif data["type"] == "FilteringT": return FilteringT.from_dict(data)
	raise ValueError("Le dictionnaire ne contient pas un type de paramètre valide.")


# Définir la liste des symboles exportés
__all__ = ["create_group_from_dict",
		   "BaseSettingGroup",
		   "Batch", "Calibration",
		   "Filtering", "FilteringGF", "FilteringT",
		   "Localization", "GaussianFit", "SplineFit", "Tracking",
		   "Gallery", "VisualizationHR", "VisualizationGraph"]
