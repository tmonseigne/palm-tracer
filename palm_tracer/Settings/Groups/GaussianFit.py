"""Définit le groupe de paramètres de l'ajustement gaussien."""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Groups.BaseUIGroup import BaseUIGroup
from palm_tracer.Settings.Types import BrowseFile, CheckBox, Combo, SpinFloat, SpinInt


# --------------------------------------------------
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
	- ``Use default model`` (:class:`~palm_tracer.Settings.Types.CheckBox.CheckBox`) : utilise exclusivement le modèle utilisateur défini par défaut.
	  La sélection du modèle spécifique est grisée et aucun modèle de secours n'est recherché si le fichier par défaut est absent ou invalide.
	"""

	label: str = "Gaussian Fit"
	"""Libellé du groupe affiché dans l'interface."""
	setting_list = {
			"Mode":          [Combo, ["Mode", "Selects the elements to fit.", 0,
									  ["X, Y", "X, Y, Sigma", "X, Y, SigmaX, SigmaY", "X, Y, SigmaX, SigmaY, Theta"]]],
			"Sigma":         [SpinFloat, ["σ", "Initial value of sigma, in acquisition pixels.", 1.0, [0.0, 10.0], 0.1]],
			"Theta":         [SpinFloat, ["θ", "Initial value of theta in degree.", 0.0, [-90, 90], 0.01]],
			"Z":             [CheckBox, ["3D", "Use astigmatism model to compute Z axial position.", False]],
			"Z max":         [SpinInt, ["Z max (nm)", "Maximum absolute value of Z to initialize estimator, in nanometers (nm).", 500, [10, 2000], 10]],
			"Model":         [BrowseFile, ["Specific Model", "Use only if your model isn't in File output folder"], ""],
			"Default Model": [CheckBox, ["Use default model", "Use only the default astigmatism model saved in the user folder.", False]],
			}
	"""Définition des paramètres du groupe et de leur configuration."""
	mode: int = 2
	"""Mode d'affichage du groupe dans l'interface."""

	# --------------------------------------------------
	def initialize(self):
		"""Initialise les connexions entre les paramètres."""
		super().initialize()
		self._settings["Mode"].connect(self.toggle_fit_mode)
		self._settings["Z"].connect(self.toggle_z_estimate)
		self._settings["Default Model"].connect(self.toggle_default_model)

	# --------------------------------------------------
	def get_ui(self, name: str = "default", mode: int = -1) -> BaseUIGroup:
		ui = super().get_ui(name, mode)
		self.toggle_fit_mode(self._settings["Mode"].value)
		self.toggle_z_estimate(self._settings["Z"].value)
		self.toggle_default_model(self._settings["Default Model"].value)
		return ui

	# --------------------------------------------------
	def toggle_fit_mode(self, mode: int):
		"""
		Masque et désactive l'estimation axiale lorsque les deux sigmas ne sont pas ajustés séparément.

		:param mode: Indice du mode d'ajustement gaussien sélectionné.
		"""
		if mode in (0, 1):  # L'estimation de Z nécessite l'ajustement séparé de Sigma X et Sigma Y.
			self._settings["Z"].value = False
			self._settings["Z"].hide()
		else:
			self._settings["Z"].show()

	# --------------------------------------------------
	def toggle_z_estimate(self, mode: bool):
		"""
		Affiche ou masque les paramètres de l'estimation axiale.

		:param mode: Active l'affichage lorsque l'estimation de Z est sélectionnée.
		"""
		if mode:
			self._settings["Z max"].show()
			self._settings["Model"].show()
			self._settings["Default Model"].show()
		else:
			self._settings["Z max"].hide()
			self._settings["Model"].hide()
			self._settings["Default Model"].hide()

	# --------------------------------------------------
	def toggle_default_model(self, active: bool):
		"""
		Grise la sélection du modèle spécifique lorsque le modèle par défaut est demandé.

		:param active: Indique si le modèle par défaut est sélectionné.
		"""
		model = cast(BrowseFile, self._settings["Model"])
		for ui in model.uis.values():
			if ui.label is not None: ui.label.setEnabled(not active)
			for box in ui.boxes: box.setEnabled(not active)


# --------------------------------------------------
if __name__ == "__main__":
	import sys

	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # Crée et affecte la mise en page au widget
	group = GaussianFit()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
