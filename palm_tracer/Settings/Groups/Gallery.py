"""
Fichier contenant la classe :class:`GaussianFit` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres d'ajustement gaussien nécessaires à la configuration de PALM Tracer.
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import SpinInt


##################################################
@dataclass
class Gallery(BaseSettingGroup):
	"""
	Classe contenant les paramètres de la Gallerie :

	Attributs :
		- **ROI Size** (:class:`SpinInt <palm_tracer.Settings.Types.SpinInt.SpinInt>`) : Taille de la Zone autour des points (par défaut : `9`).
		- **Gallery Size** (:class:`SpinInt <palm_tracer.Settings.Types.SpinInt.SpinInt>`) : Nombre de points par ligne (par défaut : `20`).
	"""

	label: str = "Gallery"
	setting_list = {
			"ROI Size":      [SpinInt, ["ROI Size", "Size of the area around the points.", 9, [3, 31], 2]],
			"ROIs Per Line": [SpinInt, ["ROIs Per Line", "Number of points per line and column.", 30, [1, 500], 1]],
			}
