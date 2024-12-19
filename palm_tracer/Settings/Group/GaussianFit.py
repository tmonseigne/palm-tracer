"""
Fichier contenant la classe `GaussianFit` dérivée de `BaseSettingGroup`, qui regroupe les paramètres de calibration nécessaires
à la configuration de PALM Tracer.

**Attributs de la classe GaussianFit** :

- **Sigma (FloatSetting)** : Paramètre σ pour l'ajustement gaussien.
  - Plage : [0.0, 10]
  - Pas : 0.1
  - Précision : 2
  - Valeur par défaut : 1.0

- **Sigma Fixed (CheckSetting)** : Indique si le paramètre σ est fixe ou non.
  - Valeur par défaut : True

- **Theta (FloatSetting)** : Paramètre θ pour l'ajustement gaussien.
  - Plage : [0.0, 10]
  - Pas : 0.1
  - Précision : 2
  - Valeur par défaut : 1.0

- **Theta Fixed (CheckSetting)** : Indique si le paramètre θ est fixe ou non.
  - Valeur par défaut : True

"""

from dataclasses import dataclass

from palm_tracer.Settings.Group.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.SettingTypes import CheckSetting, FloatSetting
from typing import Any, Union


##################################################
@dataclass
class GaussianFit(BaseSettingGroup):
	"""
	Classe contenant les paramètres du Gaussian Fit :

	Attributs :
		- **Sigma (FloatSetting)** : Paramètre σ pour l'ajustement gaussien (par défaut : 1.0).
		- **Sigma Fixed (CheckSetting)** : Indique si le paramètre σ est fixe ou non (par défaut : True).
		- **Theta (FloatSetting)** : Paramètre θ pour l'ajustement gaussien (par défaut : 1.0).
		- **Theta Fixed (CheckSetting)** : Indique si le paramètre θ est fixe ou non (par défaut : True).
	"""
	##################################################
	def initialize(self):
		""" Initialise le dictionnaire de paramètres. """
		super().initialize()  # Appelle l'initialisation de la classe mère.
		self._settings["Sigma"] = FloatSetting(label="σ", min=0.0, max=10, step=0.1, default=1.0)
		self._settings["Sigma Fixed"] = CheckSetting(label="Fixed", default=True)
		self._settings["Theta"] = FloatSetting(label="θ", min=0.0, max=10, step=0.1, default=1.0)
		self._settings["Theta Fixed"] = CheckSetting(label="Fixed", default=True)

	##################################################
	@classmethod
	def from_dict(cls, data: dict[str, Any]) -> "GaussianFit":
		""" Créé une instance de la classe à partir d'un dictionnaire. """
		res = cls()
		res.active = data.get("active", False)
		return res
