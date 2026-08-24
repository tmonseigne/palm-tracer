"""Définit le groupe de paramètres de suivi des particules."""

from __future__ import annotations

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import SpinFloat


##################################################
@dataclass
class Tracking(BaseSettingGroup):
	"""Regroupe les paramètres de suivi des particules.

	Paramètres regroupés :

	- ``Max Distance`` (:class:`~palm_tracer.Settings.Types.SpinFloat.SpinFloat`) : distance maximale entre deux plans pour associer un point ; valeur
	  par défaut : ``1.0`` pixel.
	"""

	label: str = "Tracking"
	setting_list = {"Max Distance": [SpinFloat, ["Max Distance (px)", "Maximum distance between two planes for a point.", 1.0, [0.0, 20.0], 1.0, 2]]}


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # crée et assigne le layout au widget
	group = Tracking()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
