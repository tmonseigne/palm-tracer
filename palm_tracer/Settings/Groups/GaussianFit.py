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
	Classe contenant les paramètres du Gaussian Fit :

	Attributs :

		- **Mode** (:class:`Combo <palm_tracer.Settings.Types.Combo.Combo>`) : Méthode d'ajustement gaussien (par défaut : `Mode X, Y`).

			- `0` : `Mode X, Y` (theta et sigma sont fixes)
			- `1` : `Mode X, Y, Sigma` (theta est fixe, Sigma Non)
			- `2` : `Mode X, Y, SigmaX, SigmaY` (theta n'est pas fixe, Sigma Si)
			- `3` : `Mode X, Y, SigmaX, SigmaY, Theta` (theta et sigma ne sont pas fixes)

		- **Sigma** (:class:`SpinFloat <palm_tracer.Settings.Types.SpinFloat.SpinFloat>`) : Paramètre σ pour l'ajustement gaussien (par défaut : `1.0`).
		- **Theta** (:class:`SpinFloat <palm_tracer.Settings.Types.SpinFloat.SpinFloat>`) : Paramètre θ pour l'ajustement gaussien (par défaut : `0.0`).
		- **Z** (:class:`CheckBox <palm_tracer.Settings.Types.CheckBox.CheckBox>`) : Utilise le modèle d'astigmatisme pour estimer la position axiale Z.
	"""

	label: str = "Gaussian Fit"
	setting_list = {
			"Mode":  [Combo, ["Mode", "Selects the elements to fit.", 0, ["X, Y", "X, Y, Sigma", "X, Y, SigmaX, SigmaY", "X, Y, SigmaX, SigmaY, Theta"]]],
			"Sigma": [SpinFloat, ["σ", "Initial value of sigma.", 1.0, [0.0, 10.0], 0.1]],
			"Theta": [SpinFloat, ["θ", "Initial value of theta in degree.", 0.0, [-90, 90], 0.01]],
			"Z":     [CheckBox, ["Estimate Z", "Use astigmatism model to estimate Z axial position.", False]],
			"Z max": [SpinInt, ["Z max (nm)", "Maximum absolute value of Z to initialize estimator.", 500, [10, 2000], 10]],
			"Model": [BrowseFile, ["Specific Model", "Use only if your model isn't in File output folder"], ""],
			}
	mode: int = 2

	##################################################
	def initialize(self):
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
