"""Définit le groupe de paramètres du rendu haute résolution 3D."""

from __future__ import annotations

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import Combo, SpinInt


##################################################
@dataclass
class HR3D(BaseSettingGroup):
	"""
	Regroupe les paramètres des reconstructions haute résolution 3D.

	Paramètres regroupés :

	- ``Z Step`` (:class:`~palm_tracer.Settings.Types.SpinInt.SpinInt`) : distance entre deux plans, dans l'unité de la colonne Z.
	- ``Axis`` (:class:`~palm_tracer.Settings.Types.Combo.Combo`) : axe de rotation de la pile.
	- ``Frames`` (:class:`~palm_tracer.Settings.Types.SpinInt.SpinInt`) : nombre d'images produites pour une rotation complète ; valeur par défaut : ``36``.
	"""

	label: str = "3D"
	"""Libellé du groupe affiché dans l'interface."""
	setting_list = {"Z Step": [SpinInt, ["Z Step", "Distance between two planes (unit same as the Z column, typically in nanometers).",
										 20, [1, 10000], 10]],
					"Axis":   [Combo, ["Axis", "Stack axis rotation.", 1, ["X", "Y", "Z"]]],
					"Frames": [SpinInt, ["Frames", "Sets the number of frames for a full rotation during 3D rotation.", 36, [1, 3600], 10]]
					}
	"""Définition des paramètres du groupe et de leur configuration."""
	mode: int = 2
	"""Mode d'affichage du groupe dans l'interface."""


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # crée et assigne le layout au widget
	group = HR3D()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
