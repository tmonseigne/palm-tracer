"""Définit le groupe de paramètres de reconnexion des trajectoires interrompues par le scintillement."""

from __future__ import annotations

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import Combo, SpinFloat, SpinInt


##################################################
@dataclass
class BlinkingReconnection(BaseSettingGroup):
	"""
	Regroupe les paramètres de reconnexion des trajectoires interrompues par le scintillement.

	Paramètres regroupés :

	- ``Mode`` (:class:`~palm_tracer.Settings.Types.Combo.Combo`) : modèle de déplacement attendu, parmi ``Immobile``, ``Diffuse`` et ``Linear``.
	- ``Max Duration`` (:class:`~palm_tracer.Settings.Types.SpinInt.SpinInt`) : durée maximale de l'interruption ; valeur par défaut : ``1`` plan.
	- ``Max Distance`` (:class:`~palm_tracer.Settings.Types.SpinFloat.SpinFloat`) : distance maximale de reconnexion ; valeur par défaut : ``1.0`` pixel.

	.. note:: Une distance supérieure à celle du suivi initial reste autorisée afin de reconnecter des points éloignés sur deux plans consécutifs.
	"""

	label: str = "Blinking Reconnection"
	"""Libellé du groupe affiché dans l'interface."""
	setting_list = {"Mode":         [Combo, ["Mode", "Expected type of movement of points.", 0, ["Immobile", "Diffuse", "Linear"]]],
					"Max Duration": [SpinInt, ["Max Duration (plane)", "Maximum blinking duration in number of planes", 1, [1, 1000], 1]],
					"Max Distance": [SpinFloat, ["Max Distance (px)", "Maximum distance between two planes for a point.", 1.0, [0.0, 20.0], 1.0, 2]]}
	"""Définition des paramètres du groupe et de leur configuration."""


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # crée et assigne le layout au widget
	group = BlinkingReconnection()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
