"""
Fichier contenant la classe `Filtering` dérivée de `BaseSettingGroup`,
qui regroupe les paramètres de filtrage du tracking nécessaires à la configuration de PALM Tracer.
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import SpinInt


##################################################
@dataclass
class FilteringT(BaseSettingGroup):
	"""
	Classe contenant les paramètres du filtrage pour le tracking :

	Attributs :
			- **Length (SpinInt)** : Interval de longueur sélectionnés (par défaut : 1-10000).
			- **D Coeff (SpinInt)** : Interval de XXX sélectionés (par défaut : 0-10000).
			- **Instant D (SpinInt)** : Interval de XXX sélectionés (par défaut : 0-10000).
			- **Speed (SpinInt)** : Interval de vitesse sélectionés (par défaut : 0-10000).
			- **Alpha (SpinInt)** : Interval de puissance sélectionés (par défaut : 0-10000).
			- **Confinement (SpinInt)** : Interval de confinement sélectionés (par défaut : 0-10000).
	"""

	label: str = "Tracks"
	setting_list = {
			"Length":      [SpinInt, ["Length", 0, 0, 100, 1]],
			"D Coeff":     [SpinInt, ["D Coeff", 0, 0, 100, 1]],
			"Instant D":   [SpinInt, ["Instant D", 0, 0, 100, 1]],
			"Speed":       [SpinInt, ["Speed (µm/s)", 0, 0, 100, 1]],
			"Alpha":       [SpinInt, ["Alpha (Power)", 0, 0, 100, 1]],
			"Confinement": [SpinInt, ["Confinement (µm)", 0, 0, 100, 1]]
			}
