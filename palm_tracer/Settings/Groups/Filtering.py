"""
Fichier contenant la classe :class:`Filtering` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de filtrage nécessaires à la configuration de PALM Tracer.

.. todo::
	Vérifier l'ordre de grandeur et le valeurs par défaut des paramètres des filtres
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Groups.FilteringGF import FilteringGF
from palm_tracer.Settings.Groups.FilteringT import FilteringT
from palm_tracer.Settings.Types import CheckRangeInt


##################################################
@dataclass
class Filtering(BaseSettingGroup):
	"""
	Classe contenant les paramètres de filtrage :

	Attributs :
			- **Plane (CheckRangeInt)** : Interval de plans sélectionnés (par défaut : [1,10000]).
			- **Intensity (CheckRangeInt)** : Interval d'intensité sélectionés (par défaut : [1,100000]).
			- **Gaussian Fit** : Paramètres de filtrage du Gaussian Fit.
			- **Tracks** : Paramètres de filtrage du Tracking.
	"""

	label: str = "Filtering"
	setting_list = {
			"Plane":        [CheckRangeInt, ["Plane", [1, 10000], [1, 10000]]],
			"Intensity":    [CheckRangeInt, ["Intensity", [1, 100000], [1, 100000]]],
			"Gaussian Fit": [FilteringGF, []],
			"Tracks":       [FilteringT, []]
			}

	##################################################
	def initialize_ui(self):
		super().initialize_ui()
		self.remove_header()
		self._settings["Gaussian Fit"].always_active()
		self._settings["Tracks"].always_active()
