"""
Fichier contenant la classe :class:`Localisation` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de localisation nécessaires à la configuration de PALM Tracer.
"""

from dataclasses import dataclass

import numpy as np

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Groups.GaussianFit import GaussianFit
from palm_tracer.Settings.Groups.SplineFit import SplineFit
from palm_tracer.Settings.Types import Button, CheckBox, Combo, SpinFloat, SpinInt
from palm_tracer.Tools.FileIO import open_calibration_mat


##################################################
@dataclass
class Localization(BaseSettingGroup):
	"""
	Classe contenant les paramètres de Localisation :

	Attributs :
		- **Preview** (:class:`CheckBox <palm_tracer.Settings.Types.CheckBox.CheckBox>`) : Activation de l'aperçu ou non (par défaut : `False`).
		- **Threshold** (:class:`SpinFloat <palm_tracer.Settings.Types.SpinFloat.SpinFloat>`) :
		  Seuil de détection de la localisation en intensité (par défaut : `90`).
		- **Auto Threshold** (:class:`Button <palm_tracer.Settings.Types.Button.Button>`) : Bouton pour calculer le seuil automatiquement.
		- **ROI Shape** (:class:`Combo <palm_tracer.Settings.Types.Combo.Combo>`) : Forme de la zone autour de la localisation (par défaut : `Circle`).
		- **ROI Size** (:class:`SpinInt <palm_tracer.Settings.Types.SpinInt.SpinInt>`) : Taille de la zone autour de la localisation (par défaut : `7`).
		- **Watershed** (:class:`CheckBox <palm_tracer.Settings.Types.CheckBox.CheckBox>`) :
		  Activation ou désactivation du mode Watershed (par défaut : `True`).
		- **Fit** (:class:`Combo <palm_tracer.Settings.Types.Combo.Combo>`) : Mode de calcul d'ajustement pour la localisation (par défaut : `Nothing`).
		- **Gaussian Fit** (:class:`GaussianFit <palm_tracer.Settings.Groups.GaussianFit.GaussianFit>`) : Paramètres du Gaussian Fit.
		- **Spline Fit** (:class:`SplineFit <palm_tracer.Settings.Groups.SplineFit.SplineFit>`) : Paramètres du Spline Fit.
	"""

	label: str = "Localization"
	setting_list = {
			"Preview":        [CheckBox, ["Preview", "", False]],
			"Threshold":      [SpinFloat, ["Threshold", "", 90.0, [0.0, 1000], 1.0, 2]],
			"Auto Threshold": [Button, ["Auto Threshold", ""]],
			"ROI Shape":      [Combo, ["ROI Shape", "", 0, ["Circle", "Square"]]],
			"ROI Size":       [SpinInt, ["ROI Size", "", 7, [3, 50], 1]],
			"Watershed":      [CheckBox, ["Watershed", "", True]],
			"Fit":            [Combo, ["Fit", "", 0, ["Nothing", "Gaussian Fit", "Spline"]]],
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
		self._settings["Fit"].connect(self.toggle_fit_mode)

	##################################################
	def toggle_fit_mode(self, mode):
		"""Change le mode d'ajustement."""
		if mode == 0:
			self._settings["Gaussian Fit"].hide()
			self._settings["Spline Fit"].hide()
		elif mode == 1:
			self._settings["Gaussian Fit"].show()
			self._settings["Spline Fit"].hide()
		else:
			self._settings["Gaussian Fit"].hide()
			self._settings["Spline Fit"].show()

	##################################################
	def get_fit(self) -> int:
		"""Récupère le paramètre indiquant le mode d'ajustement."""
		s = self.settings
		mode = s["Fit"]
		gaussian_mode = s["Gaussian Fit Mode"]
		# spline_sensor = s["Spline Fit Sensor"]
		if mode == 0: return 0  # .					Aucun ajustement
		elif mode == 1: return 1 + gaussian_mode  # Ajustement Gaussien
		else: return 5  # + spline_sensor 		  # Ajustement Spline

	##################################################
	def get_fit_params(self) -> np.ndarray:
		"""Récupère les paramètres pour l'ajustement."""
		s = self.settings
		if s["Fit"] == 0: return np.array([s["ROI Size"]], dtype=np.float64)
		if s["Fit"] != 2: return np.array([s["ROI Size"], s["Gaussian Fit Sigma"], 2 * s["Gaussian Fit Sigma"], s["Gaussian Fit Theta"]], dtype=np.float64)
		# Load Mat File
		try:
			calib = open_calibration_mat(s["Spline Fit File"])
			sx, sy, sz = calib["coeff"].shape[:3]
			return np.concatenate([np.array([s["ROI Size"], sx, sy, sz, calib["dz"]], dtype=np.float64), calib["coeff"].flatten()])
		except Exception: raise
