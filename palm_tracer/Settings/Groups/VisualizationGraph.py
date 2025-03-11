"""
Fichier contenant la classe :class:`VisualizationGraph` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de visualisation de graphique nécessaires à la configuration de PALM Tracer.
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import Combo

GRAPH_SOURCE = ["Integrated Intensity", "Sigma X", "Sigma Y", "Theta"]

##################################################
@dataclass
class VisualizationGraph(BaseSettingGroup):
	"""
	Classe contenant les paramètres de Visualization :
	"""

	label: str = "Graph"
	setting_list = {
			"Mode": [Combo, ["Mode", 0, ["Histogram", "Plane Heat Map","Plane Violin"]]],
			"Source": [Combo, ["Source", 0, GRAPH_SOURCE]]}
