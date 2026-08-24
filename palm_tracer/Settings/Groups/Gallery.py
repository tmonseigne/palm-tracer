"""Définit le groupe de paramètres de construction des galeries."""

from __future__ import annotations

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import SpinInt


##################################################
@dataclass
class Gallery(BaseSettingGroup):
	"""
	Regroupe les paramètres de construction des galeries d'images.

	Paramètres regroupés :

	- ``ROI Size`` (:class:`~palm_tracer.Settings.Types.SpinInt.SpinInt`) : côté de la zone extraite autour de chaque point ; valeur par défaut : ``9`` pixels.
	- ``ROIs Per Line`` (:class:`~palm_tracer.Settings.Types.SpinInt.SpinInt`) : nombre de zones par ligne et par colonne ; valeur par défaut : ``30``.
	"""

	label: str = "Gallery"
	"""Libellé du groupe affiché dans l'interface."""
	setting_list = {
			"ROI Size":      [SpinInt, ["ROI Size", "Size of the area around the points.", 9, [3, 31], 2]],
			"ROIs Per Line": [SpinInt, ["ROIs Per Line", "Number of points per line and column.", 30, [1, 500], 1]],
			}
	"""Définition des paramètres du groupe et de leur configuration."""


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # crée et assigne le layout au widget
	group = Gallery()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
