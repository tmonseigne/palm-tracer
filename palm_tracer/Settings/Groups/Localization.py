"""
Fichier contenant la classe :class:`Localisation` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de localisation nécessaires à la configuration de PALM Tracer.
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Groups.GaussianFit import GaussianFit
from palm_tracer.Settings.Groups.SplineFit import SplineFit
from palm_tracer.Settings.Types import Button, CheckBox, Combo, SpinFloat, SpinInt


##################################################
@dataclass
class Localization(BaseSettingGroup):
	"""
	Classe contenant les paramètres de Localisation :

	Attributs :
			- **Preview (CheckBox)** : Activation de la preview ou non (par défaut : False).
			- **Threshold (SpinFloat)** : Seuil de détection de la localisation en intensité (par défaut : 90).
			- **Watershed (CheckBox)** : Activation ou désactivation du mode Watershed (par défaut : True).
			- **Mode (Combo)** : Mode de calcul pour la localisation (par défaut : Gaussian Fit).
			- **ROI Size (SpinInt)** : Taille du carré autour de la localisation (par défaut : 7).
			- **Gaussian Fit (GaussianFit)** : Paramètres du Gaussian Fit.
	"""

	label: str = "Localization"
	setting_list = {
			"Preview":        [CheckBox, ["Preview", False]],
			"Threshold":      [SpinFloat, ["Threshold", 90.0, 0.0, 1000, 1.0, 2]],
			"Auto Threshold": [Button, ["Auto Threshold"]],
			"ROI Shape":       [Combo, ["ROI Shape", 0, ["Circle", "Square"]]],
			"ROI Size":       [SpinInt, ["ROI Size", 7, 3, 50, 1]],
			"Watershed":      [CheckBox, ["Watershed", True]],
			"Mode":           [Combo, ["Mode", 0, ["Gaussian Fit", "Spline"]]],
			"Gaussian Fit":   [GaussianFit, []],
			"Spline Fit":     [SplineFit, []]
			}
	_inner_groups = ["Gaussian Fit", "Spline Fit"]

	##################################################
	def initialize_ui(self):
		super().initialize_ui()
		self._settings["Gaussian Fit"].remove_header()
		self._settings["Spline Fit"].remove_header()
		self._settings["Spline Fit"].hide()
		self._settings["Mode"].connect(self.toggle_fit_mode)

	##################################################
	def toggle_fit_mode(self, mode):
		if mode == 0:
			self._settings["Gaussian Fit"].show()
			self._settings["Spline Fit"].hide()
		else:
			self._settings["Spline Fit"].show()
			self._settings["Gaussian Fit"].hide()
