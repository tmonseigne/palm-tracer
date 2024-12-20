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

from dataclasses import dataclass, field
from typing import Any

from palm_tracer.Settings.Group.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.SettingTypes import CheckSetting, FloatSetting


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
	setting_list: dict[str, list[Any]] = field(init=False, default_factory=lambda:
	{
			"Sigma":       [FloatSetting, ["σ", 1.0, 0.0, 10.0, 0.1]],
			"Sigma Fixed": [CheckSetting, ["Fixed", False]],
			"Theta":       [FloatSetting, ["θ", 1.0, 0.0, 10.0, 0.1]],
			"Theta Fixed": [CheckSetting, ["Fixed", False]]
			})
