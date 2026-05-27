"""
Fichier contenant la classe :class:`palm_tracer.Settings.Groups.BeadsExtraction` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres permettant l'extraction des billes à partir des localisation nécessaires à la configuration de PALM Tracer.
"""
from __future__ import annotations

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import CheckBox, SpinFloat


##################################################
@dataclass
class BeadsExtraction(BaseSettingGroup):
	"""
	Classe contenant les paramètres de correction du drift.

	Attributs :
		- **Max Distance** (:class:`SpinFloat <palm_tracer.Settings.Types.SpinFloat.SpinFloat>`) :
		  Distance maximale entre deux plans pour une bille (par défaut : `1.0`).
		- **3D** (:class:`CheckBox <palm_tracer.Settings.Types.CheckBox.CheckBox>`) :
		  Utilisation ou non de la coordonnée Z dans les calculs (par défaut : `False`).
	"""

	label: str = "Beads Extraction"
	setting_list = {"Max Distance": [SpinFloat, ["Max Distance (pixel)", "Maximum distance between two planes for a bead.", 1.0, [0.0, 20.0], 0.1, 2]],
					"3D":           [CheckBox, ["3D", "Use the Z-axis during computes.", False]]}


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
