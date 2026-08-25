"""Définit le groupe de paramètres de filtrage des trajectoires."""

from __future__ import annotations

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import CheckIntSelection, CheckRangeFloat, CheckRangeInt


##################################################
@dataclass
class FiltersT(BaseSettingGroup):
	"""
	Regroupe les filtres applicables aux trajectoires et à leurs métriques.

	Paramètres regroupés :

	- ``Track`` (:class:`~palm_tracer.Settings.Types.CheckIntSelection.CheckIntSelection`) : identifiants individuels ou intervalles, par exemple
	  ``1-10;15;20-25``.
	- ``Length`` (:class:`~palm_tracer.Settings.Types.CheckRangeInt.CheckRangeInt`) : intervalle de longueur ; valeur par défaut : ``[1, 10000]``.
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
	setting_list = {
			"Track":       [CheckIntSelection, ["Track ID", "Selected Track IDs. Use - to specify a range and ; "
															"to separate multiple values or ranges. Example: 1-10;15;20-25."]],
			"Length":      [CheckRangeInt, ["Length", "", [1, 10000], [1, 100000]]],
			"Instant D":   [CheckRangeFloat, ["Instant D", "", [-5, 5], [-10, 10]]],
			"D Coeff":     [CheckRangeFloat, ["D Coeff (μm²/s)", "", [-5, 5], [-10, 10]]],
			"Alpha":       [CheckRangeFloat, ["Alpha (Power)", "", [-10, 10], [-100, 100]]],
			"Speed":       [CheckRangeFloat, ["Speed (µm/s)", "", [0, 1], [0, 100]]],
			"Confinement": [CheckRangeFloat, ["Confinement (µm)", "", [-10, 10], [-100, 100]]]
			}
	"""Définition des paramètres du groupe et de leur configuration."""
	mode: int = 1
	"""Mode d'affichage du groupe dans l'interface."""

	##################################################
	def deactivate_filters(self):
		"""Désactive tous les filtres."""
		for key in self.setting_list: self._settings[key].active = False


##################################################
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
