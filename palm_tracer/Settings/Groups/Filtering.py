"""
Fichier contenant la classe :class:`Filtering` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de filtrage nécessaires à la configuration de PALM Tracer.

.. todo::
	Vérifier l'ordre de grandeur et le valeurs par défaut des paramètres des filtres
	Borne plane filter a gérer dynamiquement
	intensité c'est intensité intégré de la localisation donc potentiellement beaucouppppppp
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Groups.FilteringL import FilteringL
from palm_tracer.Settings.Groups.FilteringT import FilteringT
from palm_tracer.Settings.Types import CheckBox, CheckRangeInt


##################################################
@dataclass
class Filtering(BaseSettingGroup):
	"""
	Classe contenant les paramètres de filtrage :

	Attributs :
		- **Save** (:class:`CheckBox <palm_tracer.Settings.Types.CheckBox>`) :
		  Sauvegarde les éléments une fois filtrés (dans un fichiers séparé du fichier non filtré)  (par défaut : `False`).
		- **Plane** (:class:`CheckRangeInt <palm_tracer.Settings.Types.CheckRangeInt>`) : Interval de plans sélectionnés (par défaut : `[1,10000]`).
		- **Localization** (:class:`FilteringL`) : Paramètres de filtrage de la Localisation.
		- **Tracks** (:class:`FilteringT`) : Paramètres de filtrage du Tracking.
	"""

	label: str = "Filtering"
	setting_list = {
			"Save":         [CheckBox, ["Save filtered", "", False]],
			"Plane":        [CheckRangeInt, ["Plane", "", [1, 100000], [1, 100000]]],
			"Localization": [FilteringL, []],
			"Tracks":       [FilteringT, []]
			}
	_inner_groups = ["Localization", "Tracks"]

	##################################################
	def initialize_ui(self):
		super().initialize_ui()
		self.remove_header()
		self._settings["Localization"].always_active()
		self._settings["Tracks"].always_active()

	##################################################
	def deactivate_filters(self):
		self._settings["Save"].set_value(False)
		self._settings["Plane"].active = False
		fl = self._settings["Localization"]
		if isinstance(fl, FilteringL): fl.deactivate_filters()
		ft = self._settings["Tracks"]
		if isinstance(ft, FilteringT): ft.deactivate_filters()
