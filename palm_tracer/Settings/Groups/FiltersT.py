"""
Fichier contenant la classe :class:`Filters` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de filtrage du tracking nécessaires à la configuration de PALM Tracer.

.. todo:: Vérifier l'ordre de grandeur et les valeurs par défaut des paramètres des filtres. Dynamiquement, changer le max de la longueur
"""
from __future__ import annotations

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import CheckIntSelection, CheckRangeFloat, CheckRangeInt


##################################################
@dataclass
class FiltersT(BaseSettingGroup):
	"""
	Classe contenant les paramètres du filtrage pour le tracking :

	Attributs :
		- **Track** (:class:`CheckIntSelection <palm_tracer.Settings.Types.CheckIntSelection.CheckIntSelection>`) :
		  Sélectionne les Track IDs à conserver. Utilisez - pour définir un intervalle et ; pour séparer plusieurs valeurs ou intervalles.
		  Exemple : 1-10;15;20-25.
		- **Length** (:class:`CheckRangeInt <palm_tracer.Settings.Types.CheckRangeInt.CheckRangeInt>`) :
		  Intervalle de longueur sélectionné (par défaut : `[1, 10000]`).
		- **Instant D** (:class:`CheckRangeFloat <palm_tracer.Settings.Types.CheckRangeFloat.CheckRangeFloat>`) :
		  Intervalle de diffusion instantanée sélectionné (par défaut : `[-5, 5]`).
		- **D Coeff** (:class:`CheckRangeFloat <palm_tracer.Settings.Types.CheckRangeFloat.CheckRangeFloat>`) :
		  Intervalle de direction sélectionné (par défaut : `[-5, 5]`).
		- **Alpha** (:class:`CheckRangeFloat <palm_tracer.Settings.Types.CheckRangeFloat.CheckRangeFloat>`) :
		  Intervalle de puissance sélectionné (par défaut : `[-10, 10]`).
		- **Speed** (:class:`CheckRangeFloat <palm_tracer.Settings.Types.CheckRangeFloat.CheckRangeFloat>`) :
		  Intervalle de vitesse sélectionné (par défaut : `[0, 1]`).
		- **Confinement** (:class:`CheckRangeFloat <palm_tracer.Settings.Types.CheckRangeFloat.CheckRangeFloat>`) :
		  Intervalle de confinement sélectionné (par défaut : `[-10, 10]`).
	"""

	label: str = "Tracks"
	setting_list = {
			"Track":       [CheckIntSelection, ["Track ID", "Select the Track IDs to keep. Use - to specify a range and ; "
															"to separate multiple values or ranges. Example: 1-10;15;20-25."]],
			"Length":      [CheckRangeInt, ["Length", "", [1, 10000], [1, 100000]]],
			"Instant D":   [CheckRangeFloat, ["Instant D", "", [-5, 5], [-10, 10]]],
			"D Coeff":     [CheckRangeFloat, ["D Coeff (μm²/s)", "", [-5, 5], [-10, 10]]],
			"Alpha":       [CheckRangeFloat, ["Alpha (Power)", "", [-10, 10], [-100, 100]]],
			"Speed":       [CheckRangeFloat, ["Speed (µm/s)", "", [0, 1], [0, 100]]],
			"Confinement": [CheckRangeFloat, ["Confinement (µm)", "", [-10, 10], [-100, 100]]]
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
	group = FiltersT()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
