"""
Fichier contenant la classe :class:`VisualizationHR` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de visualisation haute résolution nécessaires à la configuration de PALM Tracer.
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import Combo, SpinInt

HR_SOURCE = ["All", "Integrated Intensity", "Sigma X", "Sigma Y", "Theta"]

##################################################
@dataclass
class VisualizationHR(BaseSettingGroup):
	"""
	Classe contenant les paramètres de Visualization :
	"""

	label: str = "High Resolution"
	setting_list = {"Ratio":  [SpinInt, ["Up scaling ratio", 2, 1, 100, 1]],
					"Source": [Combo, ["Source", 0, HR_SOURCE]]}
