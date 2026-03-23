"""
Fichier contenant la classe :class:`Filtering` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de filtrage nécessaires à la configuration de PALM Tracer.

.. todo:: Vérifier l'ordre de grandeur et les valeurs par défaut des paramètres des filtres
	      intensité c'est intensité intégré de la localisation donc potentiellement beaucouppppppp
"""

from dataclasses import dataclass, field
from typing import cast

from qtpy.QtWidgets import QFormLayout, QHBoxLayout, QPushButton

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Groups.FilteringL import FilteringL
from palm_tracer.Settings.Groups.FilteringT import FilteringT
from palm_tracer.Settings.Types import CheckBox, CheckRangeInt


##################################################
@dataclass
class Filtering(BaseSettingGroup):
	"""
	Classe contenant les paramètres de filtrage :

	Attributs :
		- **Save** (:class:`CheckBox <palm_tracer.Settings.Types.CheckBox.CheckBox>`) :
		  Sauvegarde les éléments une fois filtrés (dans un fichier séparé du fichier non filtré)  (par défaut : `False`).
		- **Plane** (:class:`CheckRangeInt <palm_tracer.Settings.Types.CheckRangeInt.CheckRangeInt>`) :
		  Interval de plans sélectionné (par défaut : `[1,10000]`).
		- **Localization** (:class:`FilteringL <palm_tracer.Settings.Groups.FilteringL.FilteringL>`) : Paramètres de filtrage de la Localisation.
		- **Tracks** (:class:`FilteringT <palm_tracer.Settings.Groups.FilteringT.FilteringT>`) : Paramètres de filtrage du Tracking.
	"""

	label: str = "Filtering"
	setting_list = {
			"Save":         [CheckBox, ["Save filtered", "Save filtered datas in _filtered.csv file.", False]],
			"Plane":        [CheckRangeInt, ["Plane", "", [1, 100000], [1, 100000]]],
			"Localization": [FilteringL, []],
			"Tracks":       [FilteringT, []]
			}
	_inner_groups = ["Localization", "Tracks"]

	buttons: dict[str, QPushButton] = field(init=False)
	"""Boutons d'action Reset, Update, Save (:class:`dict[str, QPushButton]`)."""

	##################################################
	def initialize_ui(self):
		super().initialize_ui()
		self.remove_header()
		self._settings["Localization"].always_active()
		self._settings["Tracks"].always_active()

		# Créer les boutons d'action
		self.buttons = {"reset": QPushButton("Reset"), "update": QPushButton("Update"), "save": QPushButton("Save")}
		# Créer un layout horizontal pour les boutons
		actions = QHBoxLayout()
		actions.addWidget(self.buttons["reset"])
		actions.addWidget(self.buttons["update"])
		actions.addWidget(self.buttons["save"])

		layout = cast(QFormLayout, self._widget.layout())
		layout.addRow(actions)

	##################################################
	def deactivate_filters(self):
		""" Désactive tous les filtres."""
		self._settings["Save"].value = False
		self._settings["Plane"].active = False
		fl = cast(FilteringL, self._settings["Localization"])
		fl.deactivate_filters()
		ft = cast(FilteringT, self._settings["Tracks"])
		ft.deactivate_filters()

	##################################################
	def update_limits(self, x_max: int | None = None, y_max: int | None = None, plane_max: int | None = None):
		"""Mets à jour le min et le max de certains filtres."""
		with self.signal_blocked():
			cast(CheckRangeInt, self._settings["Plane"]).update_limits(None, plane_max)
			fl = cast(FilteringL, self._settings["Localization"])
			cast(CheckRangeInt, fl["Y"]).update_limits(None, y_max)
			cast(CheckRangeInt, fl["X"]).update_limits(None, x_max)
			ft = cast(FilteringT, self._settings["Tracks"])
			cast(CheckRangeInt, ft["Length"]).update_limits(None, plane_max)



##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # crée et assigne le layout au widget
	group = Filtering()
	w.layout().addWidget(group.widget)
	w.show()
	sys.exit(app.exec_())
