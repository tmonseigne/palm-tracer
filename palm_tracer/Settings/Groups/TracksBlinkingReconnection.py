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

	Attributs :
		- **Mode** (:class:`Combo <palm_tracer.Settings.Types.Combo>`) : Méthode de déplacement du point (par défaut : `Immobile`).
		- **Max Duration** (:class:`SpinInt <palm_tracer.Settings.Types.SpinInt>`) : Durée maximale du scinetillement en nombre de plans (par défaut : `1`).
		- **Max Speed** (:class:`SpinFloat <palm_tracer.Settings.Types.SpinFloat>`) : Vitesse maximale du point en μm/plan (par défaut : `1.0`).
	"""

	label: str = "Blinking Reconnection"
	setting_list = {"Mode":         [Combo, ["Mode", 0, ["Immobile", "Diffuse", "Linear"]]],
					"Max Duration": [SpinInt, ["Max Duration (plane)", 1, [1, 1000], 1]],
					"Max Speed":    [SpinFloat, ["Max Speed (μm/plane)", 1.0, [0.0, 1000.0], 1.0, 2]]}
