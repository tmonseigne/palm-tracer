"""
Fichier contenant la classe `GaussianFit` dérivée de `BaseSettingGroup`,
qui regroupe les paramètres de calibration nécessaires à la configuration de PALM Tracer.
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import CheckBox, SpinFloat


##################################################
@dataclass
class GaussianFit(BaseSettingGroup):
	"""
	Classe contenant les paramètres du Gaussian Fit :

	Attributs :
			- **Sigma (SpinFloat)** : Paramètre σ pour l'ajustement gaussien (par défaut : 1.0).
			- **Sigma Fixed (CheckBox)** : Indique si le paramètre σ est fixe ou non (par défaut : True).
			- **Theta (SpinFloat)** : Paramètre θ pour l'ajustement gaussien (par défaut : 1.0).
			- **Theta Fixed (CheckBox)** : Indique si le paramètre θ est fixe ou non (par défaut : True).
	"""

	label: str = "Gaussian Fit"
	setting_list = {
			"Sigma":       [SpinFloat, ["σ", 1.0, 0.0, 10.0, 0.1]],
			"Sigma Fixed": [CheckBox, ["Fixed", False]],
			"Theta":       [SpinFloat, ["θ", 1.0, 0.0, 10.0, 0.1]],
			"Theta Fixed": [CheckBox, ["Fixed", False]],
			}
