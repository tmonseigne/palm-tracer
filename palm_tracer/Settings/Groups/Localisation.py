"""
Fichier contenant la classe `Localisation` dérivée de `BaseSettingGroup`,
qui regroupe les paramètres de calibration nécessaires à la configuration de PALM Tracer.
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Groups.GaussianFit import GaussianFit
from palm_tracer.Settings.Types import CheckBox, Combo, SpinFloat, SpinInt


##################################################
@dataclass
class Localisation(BaseSettingGroup):
	"""
	Classe contenant les paramètres de Localisation :

	Attributs :
			- **Preview (CheckBox)** : Activation de la preview ou non (par défaut : False).
			- **Threshold (SpinFloat)** : Seuil de détection de la localisation en intensité (par défaut : 90).
			- **Watershed (CheckBox)** : Activation ou désactivation du mode Watershed (par défaut : True).
			- **Mode (Combo)** : Mode de calcul pour la localisation (par défaut : Gaussian Fit).
			- **ROI Size (SpinInt)** : Taille du carré autour de la localisation (par défaut : 7).
			- **Gaussian Fit (GaussianFit)** : Paramètres du Gaussian Fit.
	"""

	label: str = "Localisation"
	setting_list = {
			"Preview":      [CheckBox, ["Preview"]],
			"Threshold":    [SpinFloat, ["Threshold", 90.0, 0.0, 1000, 1.0, 2]],
			"ROI Size":     [SpinInt, ["ROI Size", 7, 3, 50, 1]],
			"Watershed":    [CheckBox, ["Watershed", True]],
			"Mode":         [Combo, ["Mode", 0, ["Gaussian Fit", "Spline"]]],
			"Gaussian Fit": [GaussianFit, []],
			}
