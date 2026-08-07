"""
Fichier contenant la classe :class:`Graph` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de visualisation de graphique nécessaires à la configuration de PALM Tracer.
"""
from __future__ import annotations

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import CheckBox


##################################################
@dataclass
class GraphDisplay(BaseSettingGroup):
	"""
	Classe contenant les paramètres de Visualisation :

	Attributs :
		- **Limits** (:class:`CheckBox <palm_tracer.Settings.Types.CheckBox.CheckBox>`) : Limite les données à ±3σ autour de la moyenne (règle des 3 sigmas).
		- **Sigma** (:class:`CheckBox <palm_tracer.Settings.Types.CheckBox.CheckBox>`) :
		  Trace des lignes pointillées à des distances de 1, 2 et 3 sigmas de la moyenne.
		- **Gauss** (:class:`CheckBox <palm_tracer.Settings.Types.CheckBox.CheckBox>`) :
		  Affiche la courbe gaussienne associée à la moyenne et à l'écart-type des données. .
		- **KDE** (:class:`CheckBox <palm_tracer.Settings.Types.CheckBox.CheckBox>`) :
		  Affiche l'estimation de densité par noyau (la courbe la plus proche de l'histogramme) associée aux données.
		- **Cumul** (:class:`CheckBox <palm_tracer.Settings.Types.CheckBox.CheckBox>`) : Affiche un histogramme cumulatif à la place d'un histogramme simple.
		- **Log Scale** (:class:`CheckBox <palm_tracer.Settings.Types.CheckBox.CheckBox>`) : Applique une échelle logarithmique aux données.
	"""

	label: str = "Display"
	setting_list = {
			"Limits":    [CheckBox, ["Apply Limits", "Limits data to ±3σ around the mean (3-sigma rule).", True]],
			"Sigma":     [CheckBox, ["Show σ", "Plots dotted lines at distances of 1, 2, and 3 sigma from the mean."]],
			"Gauss":     [CheckBox, ["Show Gaussian", "Displays the Gaussian curve associated with the mean and standard deviation of the data."]],
			"KDE":       [CheckBox, ["Show KDE", "Displays the kernel density estimation (the curve closest to the histogram) associated with the data."]],
			"Cumul":     [CheckBox, ["Cumulative Histogram", "Show cumulative histogram instead of simple histogram."]],
			"Log Scale": [CheckBox, ["Log Scale", "Apply a logarithmic scale to the data."]],
			# "Count":   [CheckBox, ["Count", "The data on Y is expressed in terms of count (instead of density."]]}
			}
	mode: int = 1


##################################################


if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # crée et assigne le layout au widget
	group = GraphDisplay()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
