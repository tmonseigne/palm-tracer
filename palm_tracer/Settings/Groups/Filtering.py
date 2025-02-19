"""
Fichier contenant la classe `Filtering` dérivée de `BaseSettingGroup`,
qui regroupe les paramètres de filtrage nécessaires à la configuration de PALM Tracer.
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup


##################################################
@dataclass
class Filtering(BaseSettingGroup):
	"""
	Classe contenant les paramètres du Filtering :

	Attributs :

	"""

	label: str = "Filtering"
	setting_list = { }
