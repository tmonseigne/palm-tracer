"""
Fichier contenant la classe `Tracking` dérivée de `BaseSettingGroup`,
qui regroupe les paramètres de tracking nécessaires à la configuration de PALM Tracer.
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup


##################################################
@dataclass
class Tracking(BaseSettingGroup):
	"""
	Classe contenant les paramètres de Tracking :
	"""

	label: str = "Tracking"
	setting_list = { }
