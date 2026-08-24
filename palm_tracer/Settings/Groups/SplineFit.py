"""Définit le groupe de paramètres de l'ajustement par spline."""

from __future__ import annotations

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import BrowseFile, Combo


##################################################
@dataclass
class SplineFit(BaseSettingGroup):
	"""
	Regroupe les paramètres de l'ajustement par spline.

	Paramètres regroupés :

	- ``Sensor`` (:class:`~palm_tracer.Settings.Types.Combo.Combo`) : type de capteur, ``EMCCD`` ou ``sCMOS``.
	- ``Variance Map`` (:class:`~palm_tracer.Settings.Types.BrowseFile.BrowseFile`) : carte de variance du capteur sCMOS.
	- ``File`` (:class:`~palm_tracer.Settings.Types.BrowseFile.BrowseFile`) : fichier de calibration de la fonction d'étalement du point.
	"""

	label: str = "Spline Fit"
	"""Libellé du groupe affiché dans l'interface."""
	setting_list = {
			"Sensor":       [Combo, ["Sensor", "", 0, ["EMCCD", "sCMOS"]]],
			"Variance Map": [BrowseFile, ["sCMOS Variance Map", "", ""]],
			"File":         [BrowseFile, ["Calibration File", "", ""]],
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
	group = SplineFit()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
