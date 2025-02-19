"""
Fichier contenant la classe `Visualization` dérivée de `BaseSettingGroup`,
qui regroupe les paramètres de visualization nécessaires à la configuration de PALM Tracer.
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import Combo, SpinInt


##################################################
@dataclass
class Visualization(BaseSettingGroup):
	"""
	Classe contenant les paramètres de Visualization :
	"""

	label: str = "Visualization"
	setting_list = {"Ratio":  [SpinInt, ["Up scaling ratio", 2, 1, 100, 1]],
					"Source": [Combo, ["Source", 0, ["Integrated Intensity"]]]}
