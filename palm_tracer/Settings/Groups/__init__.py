"""
Ce sous-package gère les groupes de paramètres.

**Fonctionnalités principales** :

- Permet un accès direct aux classes principales via `from palm_tracer.Settings.Group import <classe>`.

"""

from typing import Any

# Importation explicite des classes pour qu'elles soient accessibles directement
from .BaseSettingGroup import BaseSettingGroup
from .Batch import Batch
from .BlinkingReconnection import BlinkingReconnection
from .Calibration import Calibration
from .DriftCorrection import DriftCorrection
from .Filtering import Filtering
from .FilteringL import FilteringL
from .FilteringT import FilteringT
from .Gallery import Gallery
from .GaussianFit import GaussianFit
from .Localization import Localization
from .SplineFit import SplineFit
from .Tracking import Tracking
from .TracksCompute import TracksCompute
from .VisualizationGraph import VisualizationGraph
from .VisualizationHR import VisualizationHR


##################################################
def create_group_from_dict(data: dict[str, Any]) -> "BaseSettingGroup":
	"""Créé un setting en fonction d'un dictionnaire en entrée."""
	if not "type" in data: raise ValueError("Le dictionnaire ne contient pas la clé 'type'.")
	if data["type"] == "Batch": return Batch.from_dict(data)
	elif data["type"] == "Calibration": return Calibration.from_dict(data)
	elif data["type"] == "Localization": return Localization.from_dict(data)
	elif data["type"] == "DriftCorrection": return DriftCorrection.from_dict(data)
	elif data["type"] == "GaussianFit": return GaussianFit.from_dict(data)
	elif data["type"] == "SplineFit": return SplineFit.from_dict(data)
	elif data["type"] == "Tracking": return Tracking.from_dict(data)
	elif data["type"] == "BlinkingReconnection": return BlinkingReconnection.from_dict(data)
	elif data["type"] == "TracksCompute": return TracksCompute.from_dict(data)
	elif data["type"] == "Gallery": return Gallery.from_dict(data)
	elif data["type"] == "VisualizationHR": return VisualizationHR.from_dict(data)
	elif data["type"] == "VisualizationGraph": return VisualizationGraph.from_dict(data)
	elif data["type"] == "Filtering": return Filtering.from_dict(data)
	elif data["type"] == "FilteringL": return FilteringL.from_dict(data)
	elif data["type"] == "FilteringT": return FilteringT.from_dict(data)
	raise ValueError("Le dictionnaire ne contient pas un type de paramètre valide.")


# Définir la liste des symboles exportés
__all__ = ["create_group_from_dict",
		   "BaseSettingGroup",
		   "Batch", "Calibration",
		   "Filtering", "FilteringL", "FilteringT",
		   "Localization", "GaussianFit", "SplineFit", "DriftCorrection",
		   "Tracking", "BlinkingReconnection", "TracksCompute",
		   "Gallery", "VisualizationHR", "VisualizationGraph"]
