"""
Fichier contenant la classe :class:`FilteringL` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de filtrage de l'ajustement gaussien nécessaires à la configuration de PALM Tracer.
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import CheckRangeFloat


##################################################
@dataclass
class FilteringL(BaseSettingGroup):
	"""
	Classe contenant les paramètres du filtrage pour la localisation :

	Attributs :
		- **MSE** (:class:`CheckRangeFloat <palm_tracer.Settings.Types.CheckRangeFloat>`) : Interval de MSE XY sélectionnés (par défaut : `[0.0, 1.0]`).
		- **Sigma X** (:class:`CheckRangeFloat <palm_tracer.Settings.Types.CheckRangeFloat>`) : Interval de Sigma X sélectionnés (par défaut : `[0.0, 10.0]`).
		- **Sigma Y** (:class:`CheckRangeFloat <palm_tracer.Settings.Types.CheckRangeFloat>`) : Interval de Sigma Y sélectionnés (par défaut : `[0.0, 10.0]`).
		- **Theta** (:class:`CheckRangeFloat <palm_tracer.Settings.Types.CheckRangeFloat>`) : Interval de Theta sélectionnés (par défaut : `[-180, 180]`).
		- **Circularity** (:class:`CheckRangeFloat <palm_tracer.Settings.Types.CheckRangeFloat>`) : Interval de Circularité sélectionnés (par défaut : `[0.0, 1.0]`).
		- **Z** (:class:`CheckRangeFloat <palm_tracer.Settings.Types.CheckRangeFloat>`) : Interval de Z sélectionnés (par défaut : `[-5, 5]`).
	"""

	label: str = "Gaussian Fit"
	setting_list = {
			"MSE":         [CheckRangeFloat, ["MSE", [0, 1], [0, 1]]],
			"Sigma X":     [CheckRangeFloat, ["Sigma X", [0, 10], [0, 10]]],
			"Sigma Y":     [CheckRangeFloat, ["Sigma Y", [0, 10], [0, 10]]],
			"Theta":       [CheckRangeFloat, ["Theta", [-180, 180], [-180, 180]]],
			"Circularity": [CheckRangeFloat, ["Circularity", [0, 1], [0, 1]]],
			"Z":           [CheckRangeFloat, ["Z", [-5, 5], [-5, 5]]]
			}
