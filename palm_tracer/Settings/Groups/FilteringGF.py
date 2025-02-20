"""
Fichier contenant la classe `FilteringGF` dérivée de `BaseSettingGroup`,
qui regroupe les paramètres de filtrage de l'ajustement gaussien nécessaires à la configuration de PALM Tracer.
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import SpinInt


##################################################
@dataclass
class FilteringGF(BaseSettingGroup):
	"""
	Classe contenant les paramètres du filtrage pour l'ajustement Gaussien :

	Attributs :
			- **Chi² (SpinInt)** : Interval de Chi² sélectionnés (par défaut : 1-10000).
			- **Sigma X (SpinInt)** : Interval de Sigma X sélectionés (par défaut : 0-10000).
			- **Sigma Y (SpinInt)** : Interval de Sigma Y sélectionés (par défaut : 0-10000).
			- **Circularity (SpinInt)** : Interval de Circularité sélectionés (par défaut : 0-10000).
			- **Z (SpinInt)** : Interval de Z sélectionés (par défaut : 0-10000).
	"""

	label: str = "Gaussian Fit"
	setting_list = {
			"Chi²": [SpinInt, ["Chi²", 0, 0, 100, 1]],
			"Sigma X":   [SpinInt, ["Sigma X", 0, 0, 100, 1]],
			"Sigma Y":   [SpinInt, ["Sigma Y", 0, 0, 100, 1]],
			"Circularity":   [SpinInt, ["Circularity", 0, 0, 100, 1]],
			"Z":   [SpinInt, ["Z", 0, 0, 100, 1]]
			}
