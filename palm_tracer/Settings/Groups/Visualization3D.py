"""Définit le groupe de paramètres de visualisation 3D."""

from __future__ import annotations

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import CheckBox, SpinFloat, SpinInt


##################################################
@dataclass
class Visualization3D(BaseSettingGroup):
	"""
	Regroupe les paramètres de la visualisation 3D.

	Paramètres regroupés :

	- ``Point Size`` (:class:`~palm_tracer.Settings.Types.SpinFloat.SpinFloat`) : taille des points.
	- ``Pixel Size`` (:class:`~palm_tracer.Settings.Types.SpinInt.SpinInt`) : taille physique d'un pixel ; valeur par défaut : ``160`` nm.
	- ``XY Scale`` (:class:`~palm_tracer.Settings.Types.SpinFloat.SpinFloat`) : facteur d'échelle des axes X et Y.
	- ``Z Scale`` (:class:`~palm_tracer.Settings.Types.SpinFloat.SpinFloat`) : facteur d'échelle de l'axe Z.
	- ``Remove Outliers`` (:class:`~palm_tracer.Settings.Types.CheckBox.CheckBox`) : exclut les localisations dont l'intensité est nulle.
	"""

	label: str = "3D"
	"""Libellé du groupe affiché dans l'interface."""
	setting_list = {"Point Size":      [SpinFloat, ["Point Size", "", 1, [0.1, 1000], 1, 1]],
					"Pixel Size":      [SpinInt, ["Pixel Size (nm)", "", 160, [1, 1000], 10]],
					"XY Scale":        [SpinFloat, ["XY Scale", "", 1.0, [0.0, 1000], 1.0, 1]],
					"Z Scale":         [SpinFloat, ["Z Scale", "", 1.0, [0.0, 1000], 1.0, 1]],
					"Remove Outliers": [CheckBox, ["Remove Outliers", "", False]]}
	"""Définition des paramètres du groupe et de leur configuration."""
	mode: int = 2
	"""Mode d'affichage du groupe dans l'interface."""


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # Crée et affecte la mise en page au widget
	group = Visualization3D()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
