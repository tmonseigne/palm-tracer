"""
Fichier contenant la classe :class:`FiltersL` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de filtrage de l'ajustement gaussien nécessaires à la configuration de PALM Tracer.
"""
from __future__ import annotations

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import CheckRangeFloat, CheckRangeInt


##################################################
@dataclass
class FiltersL(BaseSettingGroup):
	"""
	Classe contenant les paramètres du filtrage pour la localisation :

	Attributs :
		- **Intensity** (:class:`CheckRangeInt <palm_tracer.Settings.Types.CheckRangeInt.CheckRangeInt>`) :
		  Intervalle d'intensités sélectionnées (par défaut : `[1,10000000]`).
		- **Sigma X** (:class:`CheckRangeFloat <palm_tracer.Settings.Types.CheckRangeFloat.CheckRangeFloat>`) :
		  Intervalle de Sigma X sélectionné (par défaut : `[0.0, 10.0]`).
		- **Sigma Y** (:class:`CheckRangeFloat <palm_tracer.Settings.Types.CheckRangeFloat.CheckRangeFloat>`) :
		  Intervalle de Sigma Y sélectionné (par défaut : `[0.0, 10.0]`).
		- **Circularity** (:class:`CheckRangeFloat <palm_tracer.Settings.Types.CheckRangeFloat.CheckRangeFloat>`) :
		  Intervalle de Circularités sélectionné (par défaut : `[0.0, 1.0]`).
		- **Theta** (:class:`CheckRangeFloat <palm_tracer.Settings.Types.CheckRangeFloat.CheckRangeFloat>`) :
		  Intervalle de Theta sélectionné (par défaut : `[-90, 90]`).
		- **Z** (:class:`CheckRangeFloat <palm_tracer.Settings.Types.CheckRangeFloat.CheckRangeFloat>`) :
		  Intervalle de Z sélectionné (par défaut : `[-2000, 2000]`).
		- **MSE XY** (:class:`CheckRangeFloat <palm_tracer.Settings.Types.CheckRangeFloat.CheckRangeFloat>`) :
		  Intervalle de MSE XY sélectionné (par défaut : `[0.0, 1.0]`).
		- **MSE Z** (:class:`CheckRangeFloat <palm_tracer.Settings.Types.CheckRangeFloat.CheckRangeFloat>`) :
		  Intervalle de MSE Z sélectionné (par défaut : `[0.0, 1.0]`).
	"""

	label: str = "Localization"
	setting_list = {
			"Z":           [CheckRangeInt, ["Z", "", [-2000, 2000], [-2000, 2000]]],
			"Intensity":   [CheckRangeInt, ["Intensity", "", [0, 10000000], [0, 10000000]]],
			"Sigma X":     [CheckRangeFloat, ["Sigma X", "", [0, 10], [0, 10]]],
			"Sigma Y":     [CheckRangeFloat, ["Sigma Y", "", [0, 10], [0, 10]]],
			"Circularity": [CheckRangeFloat, ["Circularity", "", [0, 1], [0, 1]]],
			"Theta":       [CheckRangeFloat, ["Theta", "", [-90, 90], [-90, 90]]],
			"MSE XY":      [CheckRangeFloat, ["MSE XY", "", [0, 1], [0, 1]]],
			"MSE Z":       [CheckRangeFloat, ["MSE Z", "", [0, 1], [0, 1]]]
			}
	mode: int = 1

	##################################################
	def deactivate_filters(self):
		""" Désactive tous les filtres."""
		for key in self.setting_list: self._settings[key].active = False


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # crée et assigne le layout au widget
	group = FiltersL()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
