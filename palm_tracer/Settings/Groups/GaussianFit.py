"""Définit le groupe de paramètres de l'ajustement gaussien."""

from __future__ import annotations

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Groups.BaseUIGroup import BaseUIGroup
from palm_tracer.Settings.Types import BrowseFile, CheckBox, Combo, SpinFloat, SpinInt


##################################################
@dataclass
class GaussianFit(BaseSettingGroup):
	"""
	Regroupe les paramètres de l'ajustement gaussien des localisations.

	Paramètres regroupés :

	- ``Mode`` (:class:`~palm_tracer.Settings.Types.Combo.Combo`) : paramètres ajustés parmi :math:`X`, :math:`Y`, :math:`\\sigma`, :math:`\\sigma_x`,
	  :math:`\\sigma_y` et :math:`\\theta`.
	- ``Sigma`` (:class:`~palm_tracer.Settings.Types.SpinFloat.SpinFloat`) : valeur initiale de :math:`\\sigma` ; valeur par défaut : ``1.0`` pixel.
	- ``Theta`` (:class:`~palm_tracer.Settings.Types.SpinFloat.SpinFloat`) : valeur initiale de :math:`\\theta` ; valeur par défaut : ``0.0`` degré.
	- ``Z`` (:class:`~palm_tracer.Settings.Types.CheckBox.CheckBox`) : active l'estimation axiale par astigmatisme.
	- ``Z max`` (:class:`~palm_tracer.Settings.Types.SpinInt.SpinInt`) : valeur absolue maximale utilisée pour initialiser l'estimation axiale ; valeur
	  par défaut : ``500`` nm.
	- ``Model`` (:class:`~palm_tracer.Settings.Types.BrowseFile.BrowseFile`) : modèle d'astigmatisme spécifique à utiliser.
	"""

	label: str = "Gaussian Fit"
	"""Libellé du groupe affiché dans l'interface."""
	setting_list = {
			"Mode":  [Combo, ["Mode", "Selects the elements to fit.", 0, ["X, Y", "X, Y, Sigma", "X, Y, SigmaX, SigmaY", "X, Y, SigmaX, SigmaY, Theta"]]],
			"Sigma": [SpinFloat, ["σ", "Initial value of sigma.", 1.0, [0.0, 10.0], 0.1]],
			"Theta": [SpinFloat, ["θ", "Initial value of theta in degree.", 0.0, [-90, 90], 0.01]],
			"Z":     [CheckBox, ["Estimate Z", "Use astigmatism model to estimate Z axial position.", False]],
			"Z max": [SpinInt, ["Z max (nm)", "Maximum absolute value of Z to initialize estimator.", 500, [10, 2000], 10]],
			"Model": [BrowseFile, ["Specific Model", "Use only if your model isn't in File output folder"], ""],
			}
	"""Définition des paramètres du groupe et de leur configuration."""
	mode: int = 2
	"""Mode d'affichage du groupe dans l'interface."""

	##################################################
	def initialize(self):
		"""Initialise les connexions entre les paramètres."""
		super().initialize()
		self._settings["Mode"].connect(self.toggle_fit_mode)
		self._settings["Z"].connect(self.toggle_z_estimate)

	##################################################
	def get_ui(self, name: str = "default", mode: int = -1) -> BaseUIGroup:
		ui = super().get_ui(name, mode)
		self.toggle_fit_mode(self._settings["Mode"].value)
		self.toggle_z_estimate(self._settings["Z"].value)
		return ui

	##################################################
	def toggle_fit_mode(self, mode: int):
		"""Change le mode d'ajustement."""
		if mode in (0, 1):  # On ne peut pas estimer Z Sigma X et Sigma Y.
			self._settings["Z"].value = False
			self._settings["Z"].hide()
		else:
			self._settings["Z"].show()

	##################################################
	def toggle_z_estimate(self, mode: bool):
		"""Change le mode d'ajustement."""
		if mode:
			self._settings["Z max"].show()
			self._settings["Model"].show()
		else:
			self._settings["Z max"].hide()
			self._settings["Model"].hide()


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # crée et assigne le layout au widget
	group = GaussianFit()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
