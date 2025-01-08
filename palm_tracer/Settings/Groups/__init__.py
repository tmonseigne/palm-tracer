"""
Ce sous-package gère les groupes de paramètres.

**Composants principaux** :

- `BaseSettingGroup` : Classe principale pour la gestion des groupes.
- `Batch` : Classe regroupant les paramètres du Batch.
- `Calibration` : Classe regroupant les paramètres de la Calibration.
- `Localisation` : Classe regroupant les paramètres de la Localisation.
- `GaussianFit` : Classe regroupant les paramètres du Gaussian Fit.

**Fonctionnalités principales** :

- Permet un accès direct aux classes principales via `from palm_tracer.Settings.Group import <classe>`.

"""

from typing import Any

# Importation explicite des classes pour qu'elles soient accessibles directement
from .BaseSettingGroup import BaseSettingGroup
from .Batch import Batch
from .Calibration import Calibration
from .GaussianFit import GaussianFit
from .Localisation import Localisation


##################################################
def create_group_from_dict(data: dict[str, Any]) -> "BaseSettingGroup":
	"""Créé un setting en fonction d'un dictionnaire en entrée."""
	if not "type" in data: raise ValueError("Le dictionnaire ne contient pas la clé 'type'.")
	if data["type"] == "Batch": return Batch.from_dict(data)
	elif data["type"] == "Calibration": return Calibration.from_dict(data)
	elif data["type"] == "Localisation": return Localisation.from_dict(data)
	elif data["type"] == "GaussianFit": return GaussianFit.from_dict(data)
	raise ValueError("Le dictionnaire ne contient pas un type de paramètre valide.")


# Définir la liste des symboles exportés
__all__ = ["BaseSettingGroup", "create_group_from_dict",
		   "Batch", "Calibration", "Localisation", "GaussianFit"]
