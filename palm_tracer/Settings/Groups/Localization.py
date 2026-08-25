"""Définit le groupe de paramètres de localisation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast

import numpy as np

from palm_tracer.Processing.Parsing import degrees_to_radians
from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Groups.BaseUIGroup import BaseUIGroup
from palm_tracer.Settings.Groups.GaussianFit import GaussianFit
from palm_tracer.Settings.Groups.SplineFit import SplineFit
from palm_tracer.Settings.Types import Button, CheckBox, Combo, SpinFloat, SpinInt
from palm_tracer.Tools.FileIO import open_calibration_mat


##################################################
@dataclass
class Localization(BaseSettingGroup):
	"""
	Regroupe les paramètres de détection et d'ajustement des localisations.

	Paramètres regroupés :

	- ``Preview`` (:class:`~palm_tracer.Settings.Types.CheckBox.CheckBox`) : active la prévisualisation ; valeur par défaut : ``False``.
	- ``Threshold`` (:class:`~palm_tracer.Settings.Types.SpinFloat.SpinFloat`) : seuil d'intensité de la détection ; valeur par défaut : ``90.0``.
	- ``Auto Threshold`` (:class:`~palm_tracer.Settings.Types.Button.Button`) : calcule automatiquement le seuil.
	- ``ROI Shape`` (:class:`~palm_tracer.Settings.Types.Combo.Combo`) : forme circulaire ou carrée de la zone d'ajustement.
	- ``ROI Size`` (:class:`~palm_tracer.Settings.Types.SpinInt.SpinInt`) : taille de la zone d'ajustement ; valeur par défaut : ``7`` pixels.
	- ``Watershed`` (:class:`~palm_tracer.Settings.Types.CheckBox.CheckBox`) : sépare les points voisins ; valeur par défaut : ``True``.
	- ``Fit`` (:class:`~palm_tracer.Settings.Types.Combo.Combo`) : sélectionne l'absence d'ajustement, l'ajustement gaussien ou l'ajustement par spline.
	- ``Gaussian Fit`` (:class:`~palm_tracer.Settings.Groups.GaussianFit.GaussianFit`) : paramètres de l'ajustement gaussien.
	- ``Spline Fit`` (:class:`~palm_tracer.Settings.Groups.SplineFit.SplineFit`) : paramètres de l'ajustement par spline.
	"""

	label: str = "Localization"
	"""Libellé du groupe affiché dans l'interface."""
	setting_list = {
			"Preview":        [CheckBox, ["Preview", "", False]],
			"Threshold":      [SpinFloat, ["Threshold", "", 90.0, [1.0, 10000.0], 5.0, 2]],
			"Auto Threshold": [Button, ["Auto Threshold", ""]],
			"ROI Shape":      [Combo, ["ROI Shape", "", 0, ["Circle", "Square"]]],
			"ROI Size":       [SpinInt, ["ROI Size", "", 7, [3, 50], 1]],
			"Watershed":      [CheckBox, ["Watershed", "Use Watershed algorithm to separate nearby points.", True]],
			"Fit":            [Combo, ["Fit", "", 0, ["Nothing", "Gaussian Fit", "Spline"]]],
			"Gaussian Fit":   [GaussianFit, []],
			"Spline Fit":     [SplineFit, []]
			}
	"""Définition des paramètres du groupe et de leur configuration."""

	##################################################
	@property
	def gaussian(self) -> GaussianFit:
		"""Groupe de paramètres liés aux filtres sur la localization (:class:`~palm_tracer.Settings.Groups.FiltersL.FiltersL`)."""
		return cast(GaussianFit, self._settings["Gaussian Fit"])

	##################################################
	@property
	def spline(self) -> SplineFit:
		"""Groupe de paramètres liés aux filtres sur la localization (:class:`~palm_tracer.Settings.Groups.FiltersL.FiltersL`)."""
		return cast(SplineFit, self._settings["Spline Fit"])

	##################################################
	def initialize(self):
		"""Initialise les connexions entre les paramètres."""
		super().initialize()
		self._settings["Fit"].connect(self.toggle_fit_mode)

	##################################################
	def get_ui(self, name: str = "default", mode: int = -1) -> BaseUIGroup:
		ui = super().get_ui(name, mode)
		self.toggle_fit_mode(self._settings["Fit"].value)
		return ui

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
		# No fit
		if s["Fit"] == 0: return np.array([s["ROI Size"]], dtype=np.float64)
		# Ajustement gaussien
		if s["Fit"] == 1:
			return np.array([s["ROI Size"], s["Gaussian Fit Sigma"], 2 * s["Gaussian Fit Sigma"],
							 degrees_to_radians(s["Gaussian Fit Theta"])], dtype=np.float64)
		# Ajustement par spline
		# Chargement du fichier MAT
		try:
			calib = open_calibration_mat(s["Spline Fit File"])
			sx, sy, sz = calib["coeff"].shape[:3]
			return np.concatenate([np.array([s["ROI Size"], sx, sy, sz, calib["dz"]], dtype=np.float64), calib["coeff"].flatten()])
		except Exception: raise


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # Crée et affecte la mise en page au widget
	group = Localization()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
