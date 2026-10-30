"""Définit le groupe de paramètres de calibration."""

from __future__ import annotations

from dataclasses import dataclass, field

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import BaseSettingType, SpinFloat


# --------------------------------------------------
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
	_settings: dict[str, BaseSettingGroup | BaseSettingType] = field(init=False, default_factory=lambda: {
			"Pixel Size": SpinFloat("Pixel Size (μm)", "Physical size of an acquisition pixel, in micrometers (µm).", 0.160, [0.001, 1.0], 0.01, 3),
			"Exposure":   SpinFloat("Exposure Time (s/frame)", "Exposure time in seconds per frame (s/frame).", 0.050, [0.001, 1.0], 0.01, 3),
			"Intensity":  SpinFloat("Intensity (photon/ADU)", "Intensity conversion factor in photons per ADU (photon/ADU).", 0.0120, [0.0, 1.0], 0.001, 4)
			})
	"""Paramètres du groupe, créés indépendamment pour chaque instance."""
	_mode: int = field(init=False, default=1)
	"""Mode d'affichage du groupe dans l'interface."""


# --------------------------------------------------
if __name__ == "__main__":
	import sys

	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # Crée et affecte la mise en page au widget
	group = Calibration()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
