"""
Fichier contenant la classe `SplineFit` dérivée de `BaseSettingGroup`,
qui regroupe les paramètres d'ajustement de spline nécessaires à la configuration de PALM Tracer.
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import SpinFloat


##################################################
@dataclass
class SplineFit(BaseSettingGroup):
	"""
	Classe contenant les paramètres du Spline Fit :

	Attributs :

	"""

	label: str = "Spline Fit"
	setting_list = {
			"Peak":    [SpinFloat, ["Peak", 1.0, 0.0, 10.0, 0.1]],
			"Cut-Off": [SpinFloat, ["Cut-Off", 1.0, 0.0, 10.0, 0.1]],
			}
