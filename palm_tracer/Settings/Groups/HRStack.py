"""
Fichier contenant la classe :class:`HRStack` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de visualisation haute résolution sous forme de pile nécessaires à la configuration de PALM Tracer.
"""
from __future__ import annotations

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import SpinInt


##################################################
@dataclass
class HRStack(BaseSettingGroup):
	"""
	Classe contenant les paramètres de Visualisation haute résolution :

	Attributs :
		- **Z Step** (:class:`SpinInt <palm_tracer.Settings.Types.SpinInt.SpinInt>`) :
		  Distance entre deux plans (unité identique à la colonne Z généralement en nanomètres).
	"""

	label: str = "Z Stack"
	setting_list = {"Z Step": [SpinInt, ["Z Step", "Distance between two planes (unit same as the Z column, typically in nanometers).",
										 20, [1, 10000], 10]],
					}
	mode: int = 2


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # crée et assigne le layout au widget
	group = HRStack()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
