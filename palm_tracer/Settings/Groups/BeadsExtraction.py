"""Définit le groupe de paramètres d'extraction des billes."""

from __future__ import annotations

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import CheckBox, SpinFloat


##################################################
@dataclass
class BeadsExtraction(BaseSettingGroup):
	"""
	Regroupe les paramètres d'extraction des billes nécessaires à la correction de dérive.

	Paramètres regroupés :

	- ``Max Distance`` (:class:`~palm_tracer.Settings.Types.SpinFloat.SpinFloat`) : distance maximale entre deux plans pour associer une bille ; valeur
	  par défaut : ``1.0`` pixel.
	- ``3D`` (:class:`~palm_tracer.Settings.Types.CheckBox.CheckBox`) : prend en compte la coordonnée Z ; valeur par défaut : ``False``.
	"""

	label: str = "Beads Extraction"
	"""Libellé du groupe affiché dans l'interface."""
	setting_list = {"Max Distance": [SpinFloat, ["Max Distance (pixel)", "Maximum distance between two planes for a bead.", 1.0, [0.0, 20.0], 0.1, 2]],
					"3D":           [CheckBox, ["3D", "Use the Z-axis during computes.", False]]}
	"""Définition des paramètres du groupe et de leur configuration."""


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # crée et assigne le layout au widget
	group = BeadsExtraction()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
