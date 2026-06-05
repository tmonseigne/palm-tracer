"""
Fichier contenant la classe :class:`Visualization3D` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de visualisation3D nécessaires à la configuration de PALM Tracer.
"""
from __future__ import annotations

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import CheckBox, SpinFloat, SpinInt


##################################################
@dataclass
class Visualization3D(BaseSettingGroup):
	"""
	Classe contenant les paramètres de Visualisation 3D :

	Attributs :
		- **Point Size** (:class:`SpinFloat <palm_tracer.Settings.Types.SpinFloat.SpinFloat>`) : Taille des points.
		- **XY Scale** (:class:`SpinFloat <palm_tracer.Settings.Types.SpinFloat.SpinFloat>`) : Échelle sur les axes X et Y.
		- **Z Scale** (:class:`SpinFloat <palm_tracer.Settings.Types.SpinFloat.SpinFloat>`) : Échelle sur l'axe Z.
		- **Remove Outliers** (:class:`CheckBox <palm_tracer.Settings.Types.CheckBox.CheckBox>`) : Supprimme les éléments avec une intensité nulle.
	"""

	label: str = "3D"
	setting_list = {"Point Size":      [SpinFloat, ["Point Size", "", 1, [0.1, 1000], 1, 1]],
					"Pixel Size":      [SpinInt, ["Pixel Size (nm)", "", 160, [1, 1000], 10]],
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
