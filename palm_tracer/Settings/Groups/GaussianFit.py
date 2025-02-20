"""
Fichier contenant la classe `GaussianFit` dérivée de `BaseSettingGroup`,
qui regroupe les paramètres d'ajustement gaussien nécessaires à la configuration de PALM Tracer.
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import Combo, SpinFloat


##################################################
@dataclass
class GaussianFit(BaseSettingGroup):
	"""
	Classe contenant les paramètres du Gaussian Fit :

	Attributs :
			- **Mode (Combo)** : Méthode d'ajustement Gaussien (par défaut : Mode X, Y).
						- 0 : Pas d'ajustement Gaussien
						- 1 : Mode X, Y (theta et sigma sont fixes)
						- 2 : Mode X, Y, Sigma (theta est fixe, Sigma Non)
						- 3 : Mode X, Y, SigmaX, SigmaY (theta n'est pas fixe, Sigma Si)
						- 4 : Mode X, Y, SigmaX, SigmaY, Theta (theta et sigma ne sont pas fixes)
			- **Sigma (SpinFloat)** : Paramètre σ pour l'ajustement gaussien (par défaut : 1.0).
			- **Sigma Fixed (CheckBox)** : Indique si le paramètre σ est fixe ou non (par défaut : True).
			- **Theta (SpinFloat)** : Paramètre θ pour l'ajustement gaussien (par défaut : 1.0).
			- **Theta Fixed (CheckBox)** : Indique si le paramètre θ est fixe ou non (par défaut : True).
	"""

	label: str = "Gaussian Fit"
	setting_list = {
			"Mode":  [Combo, ["Mode", 1, ["None", "X, Y", "X, Y, Sigma", "X, Y, SigmaX, SigmaY", "X, Y, SigmaX, SigmaY, Theta"]]],
			"Sigma": [SpinFloat, ["σ", 1.0, 0.0, 10.0, 0.1]],
			"Theta": [SpinFloat, ["θ", 0.0, 0.0, 10.0, 0.1]],
			}
