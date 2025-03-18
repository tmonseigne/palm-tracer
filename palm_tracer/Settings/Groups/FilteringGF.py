"""
Fichier contenant la classe :class:`FilteringGF` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de filtrage de l'ajustement gaussien nécessaires à la configuration de PALM Tracer.
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import CheckRangeFloat


##################################################
@dataclass
class FilteringGF(BaseSettingGroup):
	"""
	Classe contenant les paramètres du filtrage pour l'ajustement Gaussien :

	Attributs :
			- **MSE Gaussian (CheckRangeFloat)** : Interval de MSE Gaussian sélectionnés (par défaut : [0.6, 2.0]).
			- **Sigma X (CheckRangeFloat)** : Interval de Sigma X sélectionés (par défaut : [0.0, 2.0]).
			- **Sigma Y (CheckRangeFloat)** : Interval de Sigma Y sélectionés (par défaut : [0.0, 2.0]).
			- **Circularity (CheckRangeFloat)** : Interval de Circularité sélectionés (par défaut : [0.0, 1.0]).
			- **Z (CheckRangeFloat)** : Interval de Z sélectionés (par défaut : [-0.75, 0.75]).
	"""

	label: str = "Gaussian Fit"
	setting_list = {
			"MSE Gaussian": [CheckRangeFloat, ["MSE", [0.6, 2.0], [0.0, 2.0]]],
			"Sigma X":      [CheckRangeFloat, ["Sigma X", [0.0, 2.0], [0.0, 2.0]]],
			"Sigma Y":      [CheckRangeFloat, ["Sigma Y", [0.0, 2.0], [0.0, 2.0]]],
			"Circularity":  [CheckRangeFloat, ["Circularity", [0.0, 1.0], [0.0, 1.0]]],
			"Z":            [CheckRangeFloat, ["Z", [-0.75, 0.75], [-1, 1]]]
			}
