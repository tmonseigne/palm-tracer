"""
Fichier contenant la classe `Localisation` dérivée de `BaseSettingGroup`,
qui regroupe les paramètres de localisation nécessaires à la configuration de PALM Tracer.

.. todo:
	Le gaussian fit doit-être construit dans un widget à part pour complètement le masquer ou non selon le choix du fit (entre gaussien et spline).
	Le changement du combo box doit donc activer/masquer les paramètres correspondants.
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Groups.GaussianFit import GaussianFit
from palm_tracer.Settings.Groups.SplineFit import SplineFit
from palm_tracer.Settings.Types import CheckBox, Combo, SpinFloat, SpinInt


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
			"Preview":      [CheckBox, ["Preview"]],
			"Threshold":    [SpinFloat, ["Threshold", 90.0, 0.0, 1000, 1.0, 2]],
			"ROI Size":     [SpinInt, ["ROI Size", 7, 3, 50, 1]],
			"Watershed":    [CheckBox, ["Watershed", True]],
			"Mode":         [Combo, ["Mode", 0, ["Gaussian Fit", "Spline"]]],
			"Gaussian Fit": [GaussianFit, []],
			"Spline Fit":   [SplineFit, []]
			}

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
