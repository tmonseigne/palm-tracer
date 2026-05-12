"""
Fichier contenant la classe :class:`VisualizationGraph` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de visualisation de graphique nécessaires à la configuration de PALM Tracer.
"""
from __future__ import annotations

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import Combo

GRAPH_MODE = ["All", "Histogram", "Plane Heat Map", "Plane Violin"]
GRAPH_SOURCE = ["All", "Integrated Intensity", "Sigma X", "Sigma Y", "Circularity", "Theta", "MSE XY", "Z", "MSE Z"]


##################################################
@dataclass
class VisualizationGraph(BaseSettingGroup):
	"""
	Classe contenant les paramètres de Visualization :

	Attributs :
		- **Mode** (:class:`Combo <palm_tracer.Settings.Types.Combo.Combo>`) :
		  Type de graphiques à générer (histogram, heat map, violon) (par défaut : `All`).
		- **Source** (:class:`Combo <palm_tracer.Settings.Types.Combo.Combo>`) : Élément de la localisation à analyser (par défaut : `All`).
	"""

	label: str = "Graph"
	setting_list = {
			"Mode":   [Combo, ["Mode", "", 0, GRAPH_MODE]],
			"Source": [Combo, ["Source", "", 0, GRAPH_SOURCE]]}


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # crée et assigne le layout au widget
	group = VisualizationGraph()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
