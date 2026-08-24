"""Définit le groupe de paramètres de filtrage des localisations."""

from __future__ import annotations

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import CheckRangeFloat, CheckRangeInt


##################################################
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
	- ``MSE XY`` et ``MSE Z`` (:class:`~palm_tracer.Settings.Types.CheckRangeFloat.CheckRangeFloat`) : intervalles des erreurs quadratiques moyennes ;
	  valeur par défaut : ``[0.0, 1.0]``.
	"""

	label: str = "Localization"
	"""Libellé du groupe affiché dans l'interface."""
	setting_list = {
			"Z":           [CheckRangeInt, ["Z", "", [-2000, 2000], [-2000, 2000]]],
			"Intensity":   [CheckRangeInt, ["Intensity", "", [0, 10000000], [0, 10000000]]],
			"Sigma X":     [CheckRangeFloat, ["Sigma X", "", [0, 10], [0, 10]]],
			"Sigma Y":     [CheckRangeFloat, ["Sigma Y", "", [0, 10], [0, 10]]],
			"Circularity": [CheckRangeFloat, ["Circularity", "", [0, 1], [0, 1]]],
			"Theta":       [CheckRangeFloat, ["Theta", "", [-90, 90], [-90, 90]]],
			"MSE XY":      [CheckRangeFloat, ["MSE XY", "", [0, 1], [0, 1]]],
			"MSE Z":       [CheckRangeFloat, ["MSE Z", "", [0, 1], [0, 1]]]
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
	lay = QVBoxLayout(w)  # crée et assigne le layout au widget
	group = FiltersL()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
