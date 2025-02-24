"""
Fichier contenant la classe `VisualizationGraph` dérivée de `BaseSettingGroup`,
qui regroupe les paramètres de visualisation de graphique nécessaires à la configuration de PALM Tracer.
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import Combo


##################################################
@dataclass
class VisualizationGraph(BaseSettingGroup):
	"""
	Classe contenant les paramètres de Visualization :
	"""

	label: str = "Graph"
	setting_list = {"Source": [Combo, ["Source", 0, ["Sigma X", "Sigma Y"]]]}
