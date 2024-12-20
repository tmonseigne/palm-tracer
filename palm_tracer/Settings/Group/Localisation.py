"""
Fichier contenant la classe `Localisation` dérivée de `BaseSettingGroup`, qui regroupe les paramètres de calibration nécessaires
à la configuration de PALM Tracer.

**Attributs de la classe Localisation** :

- **Preview (CheckSetting)** : Activation ou désactivation de la preview.
  - Valeur par défaut : False

- **Threshold (FloatSetting)** : Seuil de détection de la localisation en intensité.
  - Plage : [0.0, 1000]
  - Pas : 1
  - Précision : 2
  - Valeur par défaut : 90

- **ROI Size (IntSetting)** : Taille du carré autour de la localisation.
  - Plage : [1, 50] pixels
  - Pas : 1
  - Valeur par défaut : 7 pixels

- **Watershed (CheckSetting)** : Activation ou désactivation du mode Watershed.
  - Valeur par défaut : False

- **Mode (ComboSetting)** : Mode de calcul pour la localisation.
  - Choix : Gaussian Fit, Spline
  - Valeur par défaut : Gaussian Fit

- **Gaussian Fit (GaussianFit)** : Paramètres du Gaussian Fit.

"""

from dataclasses import dataclass, field
from typing import Any

from palm_tracer.Settings.Group.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Group.GaussianFit import GaussianFit
from palm_tracer.Settings.SettingTypes import CheckSetting, ComboSetting, FloatSetting, IntSetting


##################################################
@dataclass
class Localisation(BaseSettingGroup):
	"""
	Classe contenant les paramètres de Localisation :

	Attributs :

		- **Preview (CheckSetting)** : Activation de la preview ou non (par défaut : False).
		- **Threshold (FloatSetting)** : Seuil de détection de la localisation en intensité (par défaut : 90).
		- **Watershed (CheckSetting)** : Activation ou désactivation du mode Watershed (par défaut : True).
		- **Mode (ComboSetting)** : Mode de calcul pour la localisation (par défaut : Gaussian Fit).
		- **ROI Size (IntSetting)** : Taille du carré autour de la localisation (par défaut : 7).
		- **Gaussian Fit (GaussianFit)** : Paramètres du Gaussian Fit.
	"""
	setting_list: dict[str, list[Any]] = field(init=False, default_factory=lambda:
	{
			"Preview":      [CheckSetting, ["Preview"]],
			"Threshold":    [FloatSetting, ["Threshold", 90.0, 0.0, 1000, 1.0, 2]],
			"ROI Size":     [IntSetting, ["ROI Size", 7, 3, 50, 1]],
			"Watershed":    [CheckSetting, ["Watershed", True]],
			"Mode":         [ComboSetting, ["Mode", ["Gaussian Fit", "Spline"]]],
			"Gaussian Fit": [GaussianFit, []]
			})
