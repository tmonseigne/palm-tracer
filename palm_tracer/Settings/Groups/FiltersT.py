"""Définit le groupe de paramètres de filtrage des trajectoires."""

from __future__ import annotations

from dataclasses import dataclass, field

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import BaseSettingType, CheckIntSelection, CheckRangeFloat, CheckRangeInt


# --------------------------------------------------
@dataclass
class FiltersT(BaseSettingGroup):
	"""
	Regroupe les filtres applicables aux trajectoires et à leurs métriques.

	Paramètres regroupés :

	- ``Track`` (:class:`~palm_tracer.Settings.Types.CheckIntSelection.CheckIntSelection`) : identifiants individuels ou intervalles, par exemple
	  ``1-10;15;20-25``.
	- ``Length`` (:class:`~palm_tracer.Settings.Types.CheckRangeInt.CheckRangeInt`) : intervalle de longueur ; valeur par défaut : ``[1, 10000]``.
	- ``Time Inside ROI`` (:class:`~palm_tracer.Settings.Types.CheckRangeInt.CheckRangeInt`) : pourcentage des points de la trajectoire situés dans la
	  zone d'intérêt sélectionnée ; valeur par défaut : ``[0, 100]``. Désactivé, ce critère ignore la ROI.
	  Activé, il conserve tous les points des trajectoires retenues, même ceux à l'extérieur de la ROI.
	- ``Instant D`` et ``D Coeff`` (:class:`~palm_tracer.Settings.Types.CheckRangeFloat.CheckRangeFloat`) : intervalles des coefficients de
	  diffusion ; valeur par défaut : ``[-5.0, 5.0]``.
	- ``Alpha`` (:class:`~palm_tracer.Settings.Types.CheckRangeFloat.CheckRangeFloat`) : intervalle de l'exposant du mouvement ; valeur par défaut :
	  ``[-10.0, 10.0]``.
	- ``Speed`` (:class:`~palm_tracer.Settings.Types.CheckRangeFloat.CheckRangeFloat`) : intervalle de vitesse ; valeur par défaut : ``[0.0, 1.0]`` µm/s.
	- ``Confinement`` (:class:`~palm_tracer.Settings.Types.CheckRangeFloat.CheckRangeFloat`) : intervalle de confinement ; valeur par défaut :
	  ``[-10.0, 10.0]`` µm.

	.. todo:: Vérifier les ordres de grandeur et les valeurs par défaut, puis adapter dynamiquement la borne supérieure de ``Length`` aux données.
	"""

	label: str = "Tracks"
	"""Libellé du groupe affiché dans l'interface."""
	_settings: dict[str, BaseSettingGroup | BaseSettingType] = field(init=False, default_factory=lambda: {
			"Track":       CheckIntSelection("Track ID", ("Selected Track IDs. Use - to specify a range and ; "
														  "to separate multiple values or ranges. Example: 1-10;15;20-25.")),
			"Length":      CheckRangeInt("Length", "Track length range, in number of localized points.", [1, 100000], [1, 100000]),
			"ROI Time":    CheckRangeInt("Time Inside ROI (%)",
										 "Keep tracks whose percentage of points inside the selected ROI is within the inclusive range. "
										 "Keep all their points, including points outside the ROI. When unchecked, ignore the ROI for track selection. "
										 "0-100% keeps all tracks.", [0, 100], [0, 100]),
			"Instant D":   CheckRangeFloat("Instant D", "Instant diffusion coefficient range, in square micrometers per second (µm²/s).", [-5, 5], [-10, 10]),
			"D Coeff":     CheckRangeFloat("D Coeff (μm²/s)", "Diffusion coefficient range, in square micrometers per second (µm²/s).", [-5, 5], [-10, 10]),
			"Alpha":       CheckRangeFloat("Alpha (Power)", "Anomalous diffusion exponent range for the power-law fit.", [-10, 10], [-100, 100]),
			"Speed":       CheckRangeFloat("Speed (µm/s)", "Average speed range, in micrometers per second (µm/s).", [0, 1], [0, 100]),
			"Confinement": CheckRangeFloat("Confinement (µm)", "Confinement radius range, in micrometers (µm).", [-10, 10], [-100, 100])
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
	group = FiltersT()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
