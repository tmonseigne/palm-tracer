"""Définit le groupe de paramètres du rendu haute résolution 3D."""

from __future__ import annotations

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import Combo, SpinInt


##################################################
@dataclass
class HR3D(BaseSettingGroup):
	"""
	Classe contenant les paramètres de Visualisation haute résolution pour la 3D :

	Attributs :
		- **Z Step** (:class:`SpinInt <palm_tracer.Settings.Types.SpinInt.SpinInt>`) :
		  Distance entre deux plans (unité identique à la colonne Z généralement en nanomètres).
		- **Axis** (:class:`Combo <palm_tracer.Settings.Types.Combo.Combo>`) : Axe de rotation de la pile.
		- **N Plane** (:class:`SpinInt <palm_tracer.Settings.Types.SpinInt.SpinInt>`) : Définit le nombre de plans pour un tour complet lors de la Rotation 3D.
	"""

	label: str = "3D"
	setting_list = {"Z Step": [SpinInt, ["Z Step", "Distance between two planes (unit same as the Z column, typically in nanometers).",
										 20, [1, 10000], 10]],
					"Axis":   [Combo, ["Axis", "Stack axis rotation.", 1, ["X", "Y", "Z"]]],
					"Frames": [SpinInt, ["Frames", "Sets the number of frames for a full rotation during 3D rotation.", 36, [1, 3600], 10]]
					}
	mode: int = 2


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
