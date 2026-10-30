"""Définit le groupe de paramètres de suivi des particules."""

from __future__ import annotations

from dataclasses import dataclass, field

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import BaseSettingType, SpinFloat


# --------------------------------------------------
@dataclass
class Tracking(BaseSettingGroup):
	"""
	Regroupe les paramètres de suivi des particules.

	Paramètres regroupés :

	- ``Max Distance`` (:class:`~palm_tracer.Settings.Types.SpinFloat.SpinFloat`) : distance maximale entre deux plans pour associer un point ; valeur
	  par défaut : ``1.0`` pixel.
	"""

	label: str = "Tracking"
	"""Libellé du groupe affiché dans l'interface."""
	_settings: dict[str, BaseSettingGroup | BaseSettingType] = field(init=False, default_factory=lambda: {
			"Max Distance": SpinFloat("Max Distance", "Maximum distance between two planes for a point, in pixels.", 1.0, [0.0, 20.0], 1.0, 2)
			})
	"""Paramètres du groupe, créés indépendamment pour chaque instance."""


# --------------------------------------------------
if __name__ == "__main__":
	import sys

	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # Crée et affecte la mise en page au widget
	group = Tracking()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
