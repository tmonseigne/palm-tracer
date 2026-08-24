"""Définit le groupe de paramètres de calibration."""

from __future__ import annotations

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import SpinFloat


##################################################
@dataclass
class Calibration(BaseSettingGroup):
	"""
	Classe contenant les informations de calibration :

	Attributs :
		- **Pixel Size** (:class:`SpinFloat <palm_tracer.Settings.Types.SpinFloat.SpinFloat>`) : Taille d'un pixel en micromètre (par défaut : `0.160`).
		- **Exposure** (:class:`SpinFloat <palm_tracer.Settings.Types.SpinFloat.SpinFloat>`) : Temps d'exposition en secondes par image (par défaut : `0.050`).
		- **Intensity** (:class:`SpinFloat <palm_tracer.Settings.Types.SpinFloat.SpinFloat>`) :
		  Intensité lumineuse en photons par Unités analogique-numérique (ADU) (par défaut : `0.0120`).
	"""

	label: str = "Calibration"
	setting_list = {
			"Pixel Size": [SpinFloat, ["Pixel Size (μm)", "", 0.160, [0.001, 1.0], 0.01, 3]],
			"Exposure":   [SpinFloat, ["Exposure Time (s/frame)", "", 0.050, [0.001, 1.0], 0.01, 3]],
			"Intensity":  [SpinFloat, ["Intensity (photon/ADU)", "", 0.0120, [0.0, 1.0], 0.001, 4]]
			}
	mode: int = 1


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
