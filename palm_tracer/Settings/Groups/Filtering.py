"""
Fichier contenant la classe `Filtering` dérivée de `BaseSettingGroup`,
qui regroupe les paramètres de filtrage nécessaires à la configuration de PALM Tracer.

.. todo:: checked range setting pour les filtres
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Groups.FilteringGF import FilteringGF
from palm_tracer.Settings.Groups.FilteringT import FilteringT
from palm_tracer.Settings.Types import SpinInt


##################################################
@dataclass
class Filtering(BaseSettingGroup):
	"""
	Classe contenant les paramètres de filtrage :

	Attributs :
			- **Plane (SpinInt)** : Interval de plans sélectionnés (par défaut : 1-10000).
			- **Intensity (SpinInt)** : Interval d'intensité sélectionés (par défaut : 0-10000).
			- **Gaussian Fit** : Paramètres de filtrage du Gaussian Fit.
			- **Tracks** : Paramètres de filtrage du Tracking.
	"""

	label: str = "Filtering"
	setting_list = {
			"Plane":        [SpinInt, ["Plane", 1, 1, 10000, 1]],
			"Intensity":    [SpinInt, ["Intensity", 0, 0, 10000, 1]],
			"Gaussian Fit": [FilteringGF, []],
			"Tracks":       [FilteringT, []]
			}

	##################################################
	def initialize_ui(self):
		super().initialize_ui()
		self.remove_header()
		self._settings["Gaussian Fit"].always_active()
		self._settings["Tracks"].always_active()
