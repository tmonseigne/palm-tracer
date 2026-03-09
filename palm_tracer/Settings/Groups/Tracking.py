"""
Fichier contenant la classe :class:`palm_tracer.Settings.Groups.Tracking` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de tracking nécessaires à la configuration de PALM Tracer.
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import SpinFloat


##################################################
@dataclass
class Tracking(BaseSettingGroup):
	"""
	Classe contenant les paramètres de Tracking :

	Attributs :
		- **Max Distance** (:class:`SpinFloat <palm_tracer.Settings.Types.SpinFloat.SpinFloat>`) :
		  Distance maximale en pixel entre deux plans (par défaut : `1.0`).
	"""

	label: str = "Tracking"
	setting_list = {"Max Distance": [SpinFloat, ["Max Distance (px)", "Maximum distance between two planes for a point.", 1.0, [0.0, 20.0], 1.0, 2]]}
