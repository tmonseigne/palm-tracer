"""
Fichier contenant la classe :class:`palm_tracer.Settings.Groups.TrackingBlinkingReconnection` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de reconnexion de trajectoires en cas de scintillement nécessaires à la configuration de PALM Tracer.
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import Combo, SpinFloat, SpinInt


##################################################
@dataclass
class TracksBlinkingReconnection(BaseSettingGroup):
	"""
	Classe contenant les paramètres de reconnexion de trajectoires en cas de scintillement
	Par principe on pourrait mettre le minimum de la Distance maximale à 2.
	Mais, si on veut reconnecter sur 2 frames consécutives avec des distances plus longues que la sélection d'origine, c'est possible.
	"""

	label: str = "Blinking Reconnection"
	setting_list = {"Mode": [Combo, ["Mode", 0, ["Immobile", "Diffuse", "Linear"]]],
					"Max Distance": [SpinInt, ["Max Distance", 1, 1, 1000, 1]],
					"Max Speed":     [SpinFloat, ["Max Speed", 1, 0.0, 1000.0, 1.0, 2]]}
