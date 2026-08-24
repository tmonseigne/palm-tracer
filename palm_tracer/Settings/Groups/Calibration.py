"""Définit le groupe de paramètres de calibration."""

from __future__ import annotations

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import SpinFloat


##################################################
@dataclass
class Calibration(BaseSettingGroup):
	"""
	Regroupe les paramètres de calibration spatiale, temporelle et photométrique.

	Paramètres regroupés :

	- ``Pixel Size`` (:class:`~palm_tracer.Settings.Types.SpinFloat.SpinFloat`) : taille d'un pixel ; valeur par défaut : ``0.160`` µm.
	- ``Exposure`` (:class:`~palm_tracer.Settings.Types.SpinFloat.SpinFloat`) : temps d'exposition par image ; valeur par défaut : ``0.050`` s.
	- ``Intensity`` (:class:`~palm_tracer.Settings.Types.SpinFloat.SpinFloat`) : facteur de conversion photométrique ; valeur par défaut :
	  ``0.0120`` photon/ADU.
	"""

	label: str = "Calibration"
	"""Libellé du groupe affiché dans l'interface."""
	setting_list = {
			"Pixel Size": [SpinFloat, ["Pixel Size (μm)", "", 0.160, [0.001, 1.0], 0.01, 3]],
			"Exposure":   [SpinFloat, ["Exposure Time (s/frame)", "", 0.050, [0.001, 1.0], 0.01, 3]],
			"Intensity":  [SpinFloat, ["Intensity (photon/ADU)", "", 0.0120, [0.0, 1.0], 0.001, 4]]
			}
	"""Définition des paramètres du groupe et de leur configuration."""
	mode: int = 1
	"""Mode d'affichage du groupe dans l'interface."""


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # crée et assigne le layout au widget
	group = Calibration()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
