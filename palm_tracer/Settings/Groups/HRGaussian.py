"""Définit le groupe de paramètres du rendu gaussien haute résolution."""

from __future__ import annotations

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import CheckBox, Combo, SpinFloat, SpinInt


##################################################
@dataclass
class HRGaussian(BaseSettingGroup):
	"""
	Regroupe les paramètres du rendu gaussien haute résolution.

	Paramètres regroupés :

	- ``Intensity`` (:class:`~palm_tracer.Settings.Types.SpinInt.SpinInt`) : intensité intégrée fixe ou diviseur appliqué à la source sélectionnée.
	- ``Fixed Intensity`` (:class:`~palm_tracer.Settings.Types.CheckBox.CheckBox`) : impose la même intensité à chaque localisation.
	- ``Shape`` (:class:`~palm_tracer.Settings.Types.Combo.Combo`) : choisit une distribution isotrope, anisotrope ou de taille fixe.
	- ``Size`` (:class:`~palm_tracer.Settings.Types.SpinFloat.SpinFloat`) : écart-type utilisé lorsque la taille est fixe.
	"""

	label: str = "Gaussian Mode"
	"""Libellé du groupe affiché dans l'interface."""
	setting_list = {"Intensity":       [SpinInt, ["Intensity", "Integrated intensity of the Gaussian curve if 'Fixed Intensity' is selected; otherwise, "
															   "the ratio by which the value selected in the source will be divided.", 100, [1, 100000], 10]],
					"Fixed Intensity": [CheckBox, ["Fixed Intensity", "Ensures that each point has the same intensity."]],
					"Shape":           [Combo, ["Shape", "Defines the shape of the Gaussian distribution (Isotropic, Anisotropic, or Fixed Size, "
														 "so that each point has the same isotropic shape).", 0, ["Fixed Size", "Isotrope", "Anisotrope"]]],
					"Size":            [SpinFloat, ["Size", "The standard deviation of the Gaussian distribution if \"Fixed Size\" is selected.",
													1, [0, 50], 0.01, 3]],
					}
	"""Définition des paramètres du groupe et de leur configuration."""


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # Crée et affecte la mise en page au widget
	group = HRGaussian()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
