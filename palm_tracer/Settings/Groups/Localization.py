"""Définit le groupe de paramètres de localisation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import cast

import numpy as np

from palm_tracer.Processing.Parsing import degrees_to_radians
from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Groups.BaseUIGroup import BaseUIGroup
from palm_tracer.Settings.Groups.GaussianFit import GaussianFit
from palm_tracer.Settings.Groups.SplineFit import SplineFit
from palm_tracer.Settings.Types import BaseSettingType, Button, CheckBox, Combo, SpinFloat, SpinInt
from palm_tracer.Tools.FileIO import open_calibration_mat


# --------------------------------------------------
@dataclass
class Localization(BaseSettingGroup):
	"""
	Regroupe les paramètres de détection et d'ajustement des localisations.

	Paramètres regroupés :

	- ``Preview`` (:class:`~palm_tracer.Settings.Types.CheckBox.CheckBox`) : active la prévisualisation ; valeur par défaut : ``False``.
	- ``Threshold`` (:class:`~palm_tracer.Settings.Types.SpinFloat.SpinFloat`) : seuil d'intensité de la détection ; valeur par défaut : ``90.0``.
	- ``Auto Threshold`` (:class:`~palm_tracer.Settings.Types.Button.Button`) : calcule automatiquement le seuil.
	- ``ROI Shape`` (:class:`~palm_tracer.Settings.Types.Combo.Combo`) : forme du contour dans l'aperçu, circulaire par défaut ou carrée.
	- ``ROI Radius`` (:class:`~palm_tracer.Settings.Types.SpinInt.SpinInt`) : nombre de pixels de chaque côté du centre ; valeur par défaut : ``3``.
	- ``Watershed`` (:class:`~palm_tracer.Settings.Types.CheckBox.CheckBox`) : sépare les points voisins ; valeur par défaut : ``True``.
	- ``Fit`` (:class:`~palm_tracer.Settings.Types.Combo.Combo`) : sélectionne l'absence d'ajustement, l'ajustement gaussien ou l'ajustement par spline.
	- ``Gaussian Fit`` (:class:`~palm_tracer.Settings.Groups.GaussianFit.GaussianFit`) : paramètres de l'ajustement gaussien.
	- ``Spline Fit`` (:class:`~palm_tracer.Settings.Groups.SplineFit.SplineFit`) : paramètres de l'ajustement par spline.
	"""

	label: str = "Localization"
	"""Libellé du groupe affiché dans l'interface."""
	_settings: dict[str, BaseSettingGroup | BaseSettingType] = field(init=False, default_factory=lambda: {
			"Preview":        CheckBox("Preview", "Preview localizations on the current plane using the current detection and fitting parameters.", False),
			"Threshold":      SpinFloat("Threshold", "Detection threshold on wavelet coefficients, in image intensity units (ADU).",
										90.0, [1.0, 10000.0], 5.0, 2),
			"Auto Threshold": Button("Auto Threshold", "Estimate the detection threshold automatically from the current plane."),
			"ROI Shape":      Combo("ROI Shape", "Shape of the ROI outline in the preview.", 0, ["Circle", "Square"]),
			"ROI Radius":     SpinInt("ROI Radius", "Number of pixels on each side of the center pixel. A radius of 3 gives a 7 × 7 pixel fitting window.",
									  3, [1, 24], 1),
			"Watershed":      CheckBox("Watershed", "Use Watershed algorithm to separate nearby points.", True),
			"Fit":            Combo("Fit", "Fitting method used to refine detected localizations; 'Nothing' disables fitting.",
									0, ["Nothing", "Gaussian Fit"]),
			"Gaussian Fit":   GaussianFit(),
			"Spline Fit":     SplineFit()
			})
	"""Paramètres du groupe, créés indépendamment pour chaque instance."""

	# --------------------------------------------------
	@property
	def gaussian(self) -> GaussianFit:
		"""Paramètres de l'ajustement gaussien."""
		return cast(GaussianFit, self._settings["Gaussian Fit"])

	# --------------------------------------------------
	@property
	def spline(self) -> SplineFit:
		"""Paramètres de l'ajustement par spline."""
		return cast(SplineFit, self._settings["Spline Fit"])

	# --------------------------------------------------
	@property
	def roi_width(self) -> int:
		"""Largeur en pixels de la fenêtre carrée, pixel central compris."""
		return 1 + 2 * self._settings["ROI Radius"].value

	# --------------------------------------------------
	def initialize(self):
		"""Initialise les connexions entre les paramètres."""
		super().initialize()
		self._settings["Fit"].connect(self.toggle_fit_mode)

	# --------------------------------------------------
	def get_ui(self, name: str = "default", mode: int = -1) -> BaseUIGroup:
		ui = super().get_ui(name, mode)
		self.toggle_fit_mode(self._settings["Fit"].value)
		return ui

	# --------------------------------------------------
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

	# --------------------------------------------------
	def get_fit(self) -> int:
		"""Récupère le paramètre indiquant le mode d'ajustement."""
		s = self.settings
		mode = s["Fit"]
		gaussian_mode = s["Gaussian Fit Mode"]
		# spline_sensor = s["Spline Fit Sensor"]
		if mode == 0: return 0  # .					Aucun ajustement
		elif mode == 1: return 1 + gaussian_mode  # Ajustement Gaussien
		else: return 5  # + spline_sensor 		  # Ajustement Spline

	# --------------------------------------------------
	def get_fit_params(self) -> np.ndarray:
		"""Récupère les paramètres pour l'ajustement."""
		s = self.settings
		width = self.roi_width
		# Sans ajustement.
		if s["Fit"] == 0: return np.array([width], dtype=float)
		# Ajustement gaussien
		if s["Fit"] == 1:
			return np.array([width, s["Gaussian Fit Sigma"], 2 * s["Gaussian Fit Sigma"],
							 degrees_to_radians(s["Gaussian Fit Theta"])], dtype=float)
		# Ajustement par spline à partir de la calibration MAT.
		calib = open_calibration_mat(s["Spline Fit File"])
		sx, sy, sz = calib["coeff"].shape[:3]
		return np.concatenate([np.array([width, sx, sy, sz, calib["dz"]], dtype=float), calib["coeff"].flatten()])


# --------------------------------------------------
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
