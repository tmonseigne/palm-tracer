"""
Fichier contenant la classe :class:`Filtering` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de filtrage du tracking nécessaires à la configuration de PALM Tracer.
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import CheckRangeFloat, CheckRangeInt


##################################################
@dataclass
class FilteringT(BaseSettingGroup):
	"""
	Classe contenant les paramètres du filtrage pour le tracking :

	Attributs :
			- **Length (CheckRangeInt)** : Interval de longueur sélectionnés (par défaut : [1, 10000]).
			- **D Coeff (CheckRangeInt)** : Interval de XXX sélectionés (par défaut : 0-10000).
			- **Instant D (CheckRangeInt)** : Interval de XXX sélectionés (par défaut : 0-10000).
			- **Speed (CheckRangeFloat)** : Interval de vitesse sélectionés (par défaut : 0-10000).
			- **Alpha (CheckRangeFloat)** : Interval de puissance sélectionés (par défaut : 0-10000).
			- **Confinement (CheckRangeFloat)** : Interval de confinement sélectionés (par défaut : 0-10000).
	"""

	label: str = "Tracks"
	setting_list = {
			"Length":      [CheckRangeInt, ["Length", [1, 10000], [1, 10000]]],
			"D Coeff":     [CheckRangeInt, ["D Coeff", [-5, 5], [-5, 5]]],
			"Instant D":   [CheckRangeInt, ["Instant D", [-5, 5], [-5, 5]]],
			"Speed":       [CheckRangeFloat, ["Speed (µm/s)", [0, 1], [0, 10]]],
			"Alpha":       [CheckRangeFloat, ["Alpha (Power)", [-10, 10], [-10, 10]]],
			"Confinement": [CheckRangeFloat, ["Confinement (µm)", [-10, 10], [-10, 10]]]
			}
