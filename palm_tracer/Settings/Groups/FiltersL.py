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
	- ``MSE XY`` et ``MSE Z`` (:class:`~palm_tracer.Settings.Types.CheckRangeFloat.CheckRangeFloat`) : intervalles des scores de qualité ;
	  valeur par défaut : ``[0.0, 1.0]``, plus grand = meilleur. Les noms historiques sont conservés :
	  XY contient la corrélation de Pearson au carré, Z le score de compatibilité des sigmas défini dans
	  :meth:`palm_tracer.Processing.Palm.Palm.astigmatism_3d_estimation`. Les anciens fichiers peuvent encore contenir une SSE pour Z.
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
			"MSE XY":      CheckRangeFloat("MSE XY", "Squared Pearson correlation range for the XY fit, from 0 to 1; higher is better.", [0, 1], [0, 1]),
			"MSE Z":       CheckRangeFloat("MSE Z", ("Sigma compatibility score range for the astigmatism model, from 0 to 1; higher is better. "
													 "Legacy files may contain a sum of squared errors instead."), [0, 1], [0, 1])
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
