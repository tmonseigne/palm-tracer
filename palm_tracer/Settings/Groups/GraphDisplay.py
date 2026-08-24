"""Définit le groupe de paramètres d'affichage des graphiques."""

from __future__ import annotations

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import CheckBox, SpinInt


##################################################
@dataclass
class GraphDisplay(BaseSettingGroup):
	"""Regroupe les options de rendu statistique des graphiques.

	Paramètres regroupés :

	- ``Limits`` (:class:`~palm_tracer.Settings.Types.CheckBox.CheckBox`) : limite l'affichage à l'intervalle :math:`[\\mu-3\\sigma,\\mu+3\\sigma]`.
	- ``Sigma`` (:class:`~palm_tracer.Settings.Types.CheckBox.CheckBox`) : affiche les repères à un, deux et trois écarts-types de la moyenne.
	- ``Gauss``, ``Poiss`` et ``Exp`` (:class:`~palm_tracer.Settings.Types.CheckBox.CheckBox`) : superposent respectivement les modèles gaussien,
	  poissonnien et exponentiel.
	- ``KDE`` (:class:`~palm_tracer.Settings.Types.CheckBox.CheckBox`) : affiche l'estimation de densité par noyau.
	- ``Cumul`` (:class:`~palm_tracer.Settings.Types.CheckBox.CheckBox`) : produit un histogramme cumulatif.
	- ``Log Scale`` (:class:`~palm_tracer.Settings.Types.CheckBox.CheckBox`) : utilise une échelle logarithmique.
	- ``Count`` (:class:`~palm_tracer.Settings.Types.CheckBox.CheckBox`) : exprime l'axe Y en effectifs plutôt qu'en densité.
	- ``Bins`` (:class:`~palm_tracer.Settings.Types.SpinInt.SpinInt`) : nombre de classes de l'histogramme ; ``0`` active le choix automatique.
	"""

	label: str = "Display"
	setting_list = {
			"Limits":    [CheckBox, ["Apply Limits", "Limits data to ±3σ around the mean (3-sigma rule).", True]],
			"Sigma":     [CheckBox, ["Show σ", "Plots dotted lines at distances of 1, 2, and 3 sigma from the mean."]],
			"Gauss":     [CheckBox, ["Show Gaussian", "Displays the Gaussian curve associated with the mean and standard deviation of the data."]],
			"KDE":       [CheckBox, ["Show KDE", "Displays the kernel density estimation (the curve closest to the histogram) associated with the data."]],
			"Poiss":     [CheckBox, ["Show Poisson", "Displays the Poissonnian curve associated with the mean of the data."]],
			"Exp":       [CheckBox, ["Show Exponential", "Displays the Exponential inverse curve associated with the mean of the data."]],
			"Cumul":     [CheckBox, ["Cumulative Histogram", "Show cumulative histogram instead of simple histogram."]],
			"Log Scale": [CheckBox, ["Log Scale", "Apply a logarithmic scale to the data."]],
			"Count":     [CheckBox, ["Count", "The data on Y is expressed in terms of count (instead of density."]],
			"Bins":      [SpinInt, ["Bins", "The number of bins along the histogram (0 for auto).", 0, [0, 1000]]]
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
