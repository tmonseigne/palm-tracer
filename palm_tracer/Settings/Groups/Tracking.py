"""
Fichier contenant la classe :class:`palm_tracer.Settings.Groups.Tracking` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de tracking nécessaires à la configuration de PALM Tracer.
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Groups.TracksBlinkingReconnection import TracksBlinkingReconnection
from palm_tracer.Settings.Types import SpinFloat


##################################################
@dataclass
class Tracking(BaseSettingGroup):
	"""
	Classe contenant les paramètres de Tracking :

	Attributs :
		- **Max Distance** (:class:`SpinFloat <palm_tracer.Settings.Types.SpinFloat>`) : Distance maximale en pixel entre deux plans (par défaut : `1.0`).
		- **Blinking Reconnection** (:class:`TracksBlinkingReconnection`) : Paramètres de reconnexion en cas de scintillement.
	"""

	label: str = "Tracking"
	setting_list = {"Max Distance":          [SpinFloat, ["Max Distance (px)", 1.0, [0.0, 20.0], 1.0, 2]],
					#"Min Length": [SpinInt, ["Min Length", 1, 1, 10, 1]],
					#"Decrease":              [SpinFloat, ["Decrease", 10.0, [1.0, 20.0], 1.0, 2]],
					#"Cost Birth":            [SpinFloat, ["Cost Birth", 0.5, [0.0, 1000.0], 1.0, 2]],
					"Blinking Reconnection": [TracksBlinkingReconnection, []]}
	_inner_groups = ["Blinking Reconnection"]
