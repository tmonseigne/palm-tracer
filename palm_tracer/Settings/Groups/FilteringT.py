"""
Fichier contenant la classe :class:`Filtering` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de filtrage du tracking nécessaires à la configuration de PALM Tracer.

.. todo::
	Vérifier l'ordre de grandeur et les valeurs par défaut des paramètres des filtres
	dynamiquement, changer le max de la longueur
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
			- **D Coeff (CheckRangeFloat)** : Interval de XXX sélectionés (par défaut : 0-10000).
			- **Instant D (CheckRangeFloat)** : Interval de XXX sélectionés (par défaut : 0-10000).
			- **Speed (CheckRangeFloat)** : Interval de vitesse sélectionés (par défaut : 0-10000).
			- **Alpha (CheckRangeFloat)** : Interval de puissance sélectionés (par défaut : 0-10000).
			- **Confinement (CheckRangeFloat)** : Interval de confinement sélectionés (par défaut : 0-10000).
	"""

	label: str = "Tracks"
	setting_list = {
			"Length":      [CheckRangeInt, ["Length", [1, 10000], [1, 100000]]],
			"Instant D":   [CheckRangeFloat, ["Instant D", [-5, 5], [-10, 10]]],
			"D Coeff":     [CheckRangeFloat, ["D Coeff (μm²/s)", [-5, 5], [-10, 10]]],
			"Alpha":       [CheckRangeFloat, ["Alpha (Power)", [-10, 10], [-100, 100]]],
			"Speed":       [CheckRangeFloat, ["Speed (µm/s)", [0, 1], [0, 100]]],
			"Confinement": [CheckRangeFloat, ["Confinement (µm)", [-10, 10], [-100, 100]]]
			}
