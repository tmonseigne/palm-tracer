"""Définit le groupe de paramètres des analyses des trajectoires."""

from __future__ import annotations

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import CheckBox, Combo, SpinInt


##################################################
@dataclass
class TrackAnalysis(BaseSettingGroup):
	"""
	Regroupe les paramètres des analyses des trajectoires.

	Paramètres regroupés :

	- ``MSD`` (:class:`~palm_tracer.Settings.Types.CheckBox.CheckBox`) : calcule le déplacement quadratique moyen.
	- ``Instant Diffusion`` (:class:`~palm_tracer.Settings.Types.CheckBox.CheckBox`) : calcule la diffusion instantanée.
	- ``Fit Length`` (:class:`~palm_tracer.Settings.Types.SpinInt.SpinInt`) : longueur initiale de la fenêtre d'ajustement ; valeur par défaut : ``4``.
	- ``Fit`` (:class:`~palm_tracer.Settings.Types.Combo.Combo`) : modèle de mouvement utilisé pour l'ajustement.
	- ``3D`` (:class:`~palm_tracer.Settings.Types.CheckBox.CheckBox`) : prend en compte la coordonnée Z.
	"""

	label: str = "Track Analysis"
	"""Libellé du groupe affiché dans l'interface."""
	setting_list = {"MSD":               [CheckBox, ["MSD", "", False]],
					"Instant Diffusion": [CheckBox, ["Instant Diffusion", "", False]],
					"Fit Length":        [SpinInt, ["Fit Length", "", 4, [2, 1000], 1]],
					"Fit":               [Combo, ["Fit", "Expected tracks movement to fit.", 0, ["None", "Linear", "Power", "Exponential"]]],
					"3D":                [CheckBox, ["3D", "Use the Z-axis during track analysis.", False]]}
	"""Définition des paramètres du groupe et de leur configuration."""


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # Crée et affecte la mise en page au widget
	group = TrackAnalysis()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
