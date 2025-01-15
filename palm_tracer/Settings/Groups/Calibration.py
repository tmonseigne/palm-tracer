"""
Fichier contenant la classe `Calibration` dérivée de `BaseSettingGroup`,
qui regroupe les paramètres de calibration nécessaires à la configuration de PALM Tracer.
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import SpinFloat, SpinInt


##################################################
@dataclass
class Calibration(BaseSettingGroup):
	"""
	Classe contenant les informations de calibration :

	Attributs :
			- **Pixel Size (SpinInt)** : Taille d'un pixel en nanomètres (par défaut : 160).
			- **Exposure (SpinInt)** : Temps d'exposition en millisecondes par image (par défaut : 50).
			- **Intensity (SpinFloat)** : Intensité lumineuse en photons par Unités analogique-numériques (ADU) (par défaut : 0.0120).
	"""

	label: str = "Calibration"
	setting_list = {
			"Pixel Size": [SpinInt, ["Pixel Size (nm)", 160, 1, 500, 10]],
			"Exposure":   [SpinInt, ["Exposure Time (ms/frame)", 50, 1, 1000, 10]],
			"Intensity":  [SpinFloat, ["Intensity (photon/ADU", 0.0120, 0.0, 1.0, 0.001, 4]],
			}
