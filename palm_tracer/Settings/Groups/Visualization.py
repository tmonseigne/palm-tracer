"""
Fichier contenant la classe `Visualization` dérivée de `BaseSettingGroup`,
qui regroupe les paramètres de visualization nécessaires à la configuration de PALM Tracer.
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup


##################################################
@dataclass
class Visualization(BaseSettingGroup):
	"""
	Classe contenant les paramètres de Visualization :
	"""

	label: str = "Visualization"
	setting_list = { }
