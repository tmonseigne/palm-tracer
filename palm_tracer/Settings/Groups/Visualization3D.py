"""
Fichier contenant la classe :class:`Visualization3D` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de visualisation3D nécessaires à la configuration de PALM Tracer.
"""
from __future__ import annotations

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import CheckBox, SpinFloat


##################################################
@dataclass
class Visualization3D(BaseSettingGroup):
	"""
	Classe contenant les paramètres de Visualisation 3D :

	Attributs :
		- **Point Size** (:class:`SpinInt <palm_tracer.Settings.Types.SpinFloat.SpinFloat>`) :
		- **XY Scale** (:class:`Combo <palm_tracer.Settings.Types.SpinFloat.SpinFloat>`) :
		- **Z Scale** (:class:`Combo <palm_tracer.Settings.Types.SpinFloat.SpinFloat>`) :
		- **Remove Outliers** (:class:`Combo <palm_tracer.Settings.Types.CheckBox.CheckBox>`) :
	"""

	label: str = "3D"
	setting_list = {"Point Size":      [SpinFloat, ["Point Size", "", 0.5, [0.1, 10], 0.1, 1]],
					"XY Scale":        [SpinFloat, ["XY Scale", "", 1.0, [0.0, 1000], 1.0, 1]],
					"Z Scale":         [SpinFloat, ["Z Scale", "", 1.0, [0.0, 1000], 1.0, 1]],
					"Remove Outliers": [CheckBox, ["Remove Outliers", "", False]]}
	mode: int = 2


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # crée et assigne le layout au widget
	group = Visualization3D()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
