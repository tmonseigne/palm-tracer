"""
Fichier contenant la classe :class:`VisualizationGraph` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de visualisation de graphique nécessaires à la configuration de PALM Tracer.
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import Combo

GRAPH_MODE = ["All", "Histogram", "Plane Heat Map","Plane Violin"]
GRAPH_SOURCE = ["All", "Integrated Intensity", "Sigma X", "Sigma Y", "Circularity", "Theta", "MSE Gaussian", "Z", "MSE Z"]

##################################################
@dataclass
class VisualizationGraph(BaseSettingGroup):
	"""
	Classe contenant les paramètres de Visualization :
	"""

	label: str = "Graph"
	setting_list = {
			"Mode": [Combo, ["Mode", 0, GRAPH_MODE]],
			"Source": [Combo, ["Source", 0, GRAPH_SOURCE]]}
