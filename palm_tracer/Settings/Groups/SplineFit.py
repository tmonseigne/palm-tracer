"""
Fichier contenant la classe :class:`SplineFit` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres d'ajustement de spline nécessaires à la configuration de PALM Tracer.
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import BrowseFile, Combo


##################################################
@dataclass
class SplineFit(BaseSettingGroup):
	"""
	Classe contenant les paramètres du Spline Fit :

	Attributs :
		- **Sensor** (:class:`Combo <palm_tracer.Settings.Types.Combo>`) : Sélection du type de capteur (par défaut : `EMCCD`).
		- **sCMOS Variance Map** (:class:`BrowseFile <palm_tracer.Settings.Types.BrowseFile>`) : Fichier de calibration du capteur sCMOS.
		- **Calibration File** (:class:`BrowseFile <palm_tracer.Settings.Types.BrowseFile>`) : Fichier de calibration de la PSF (calculé à partir de SMAP.
	"""

	label: str = "Spline Fit"
	setting_list = {
			"Sensor":       [Combo, ["Sensor", "", 0, ["EMCCD", "sCMOS"]]],
			"Variance Map": [BrowseFile, ["sCMOS Variance Map", "", ""]],
			"File":         [BrowseFile, ["Calibration File", "", ""]],
			}
