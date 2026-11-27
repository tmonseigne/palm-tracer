"""Définit le groupe de paramètres de filtrage des localisations."""

from __future__ import annotations

from dataclasses import dataclass, field

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import BaseSettingType, CheckRangeFloat, CheckRangeInt


# --------------------------------------------------
@dataclass
class FiltersL(BaseSettingGroup):
	"""
	Regroupe les filtres applicables aux localisations.

	Paramètres regroupés :

	- ``Z`` (:class:`~palm_tracer.Settings.Types.CheckRangeInt.CheckRangeInt`) : intervalle axial ; valeur par défaut : ``[-2000, 2000]`` nm.
	- ``Intensity`` (:class:`~palm_tracer.Settings.Types.CheckRangeInt.CheckRangeInt`) : intervalle d'intensité intégrée ; valeur par défaut :
	  ``[0, 10000000]``.
	- ``Sigma X`` et ``Sigma Y`` (:class:`~palm_tracer.Settings.Types.CheckRangeFloat.CheckRangeFloat`) : intervalles des écarts-types selon X et Y ;
	  valeur par défaut : ``[0.0, 10.0]`` pixel.
	- ``Circularity`` (:class:`~palm_tracer.Settings.Types.CheckRangeFloat.CheckRangeFloat`) : intervalle de circularité ; valeur par défaut :
	  ``[0.0, 1.0]``.
	- ``Theta`` (:class:`~palm_tracer.Settings.Types.CheckRangeFloat.CheckRangeFloat`) : intervalle angulaire ; valeur par défaut :
	  ``[-90.0, 90.0]`` degrés.
	- ``XY Quality`` et ``Z Quality`` (:class:`~palm_tracer.Settings.Types.CheckRangeFloat.CheckRangeFloat`) : intervalles des scores de qualité ;
	  valeur par défaut : ``[0.0, 1.0]``. Une valeur élevée indique un meilleur accord avec le modèle. En XY, le score est le carré de la
	  corrélation de Pearson. En Z, il mesure la compatibilité des largeurs avec le modèle d'astigmatisme selon
	  :meth:`palm_tracer.Processing.Palm.Palm.astigmatism_3d_estimation`.
	"""

	label: str = "Localization"
	"""Libellé du groupe affiché dans l'interface."""
	_settings: dict[str, BaseSettingGroup | BaseSettingType] = field(init=False, default_factory=lambda: {
			"Z":           CheckRangeInt("Z", "Axial position range, in nanometers (nm).", [-2000, 2000], [-2000, 2000]),
			"Intensity":   CheckRangeInt("Intensity", "Integrated intensity range, in image intensity units (ADU).", [0, 10000000], [0, 10000000]),
			"Sigma X":     CheckRangeFloat("Sigma X", "Standard deviation range along X, in acquisition pixels.", [0, 10], [0, 10]),
			"Sigma Y":     CheckRangeFloat("Sigma Y", "Standard deviation range along Y, in acquisition pixels.", [0, 10], [0, 10]),
			"Circularity": CheckRangeFloat("Circularity", "Circularity range, from 0 to 1 (dimensionless); 1 corresponds to equal X and Y sigmas.",
										   [0, 1], [0, 1]),
			"Theta":       CheckRangeFloat("Theta", "Orientation angle range, in degrees (°).", [-90, 90], [-90, 90]),
			"XY Quality":  CheckRangeFloat("XY Quality", "How well the fitted spot matches the observed spot shape. From 0 to 1, higher is better.",
										   [0, 1], [0, 1]),
			"Z Quality":   CheckRangeFloat("Z Quality", "How well the measured spot widths match the calibration model at the estimated Z. "
														"From 0 to 1, higher is better.", [0, 1], [0, 1])
			})
	"""Paramètres du groupe, créés indépendamment pour chaque instance."""
	_mode: int = field(init=False, default=1)
	"""Mode d'affichage du groupe dans l'interface."""

	# --------------------------------------------------
	def deactivate_filters(self):
		"""Désactive tous les filtres."""
		for setting in self._settings.values(): setting.active = False


# --------------------------------------------------
if __name__ == "__main__":
	import sys

	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # Crée et affecte la mise en page au widget
	group = FiltersL()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
