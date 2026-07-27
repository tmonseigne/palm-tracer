"""
Fichier contenant la classe :class:`Filters` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de filtrage nécessaires à la configuration de PALM Tracer.

.. todo:: Vérifier l'ordre de grandeur et les valeurs par défaut des paramètres des filtres
	      intensité c'est intensité intégré de la localisation donc potentiellement beaucouppppppp
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, cast

from qtpy.QtWidgets import QHBoxLayout, QPushButton, QSizePolicy, QSpacerItem

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Groups.BaseUIGroup import BaseUIGroup
from palm_tracer.Settings.Groups.FiltersL import FiltersL
from palm_tracer.Settings.Groups.FiltersT import FiltersT
from palm_tracer.Settings.Types import CheckBox, CheckInt, CheckRangeInt
from palm_tracer.Tools import Ui


##################################################
@dataclass
class Filters(BaseSettingGroup):
	"""
	Classe contenant les paramètres de filtrage :

	Attributs :
		- **Save** (:class:`CheckBox <palm_tracer.Settings.Types.CheckBox.CheckBox>`) :
		  Sauvegarde les éléments une fois filtrés (dans un fichier séparé du fichier non filtré)  (par défaut : `False`).
		- **Plane** (:class:`CheckRangeInt <palm_tracer.Settings.Types.CheckRangeInt.CheckRangeInt>`) :
		  Intervalle de plans sélectionné (par défaut : `[1,10000]`).
		- **ROI** (:class:`CheckInt <palm_tracer.Settings.Types.CheckInt.CheckInt>`) : ROI sélectionnée pour la sélection (par défaut : `1`).
		- **Localization** (:class:`FiltersL <palm_tracer.Settings.Groups.FiltersL.FiltersL>`) : Paramètres de filtrage de la Localisation.
		- **Tracks** (:class:`FiltersT <palm_tracer.Settings.Groups.FiltersT.FiltersT>`) : Paramètres de filtrage du Tracking.
	"""

	label: str = "Filters"
	setting_list = {
			"Save":         [CheckBox, ["Save filtered", "Save filtered datas in _filtered.csv file.", False]],
			"Plane":        [CheckRangeInt, ["Plane", "Limits the planes to be used.", [1, 100000], [1, 100000]]],
			"ROI":          [CheckInt, ["ROI", "ROI selected for filtering. Selected ROI appear in yellow.", 1, [1, 1]]],
			"Localization": [FiltersL, []],
			"Tracks":       [FiltersT, []]
			}
	mode: int = 2
	buttons: dict[str, dict[str, QPushButton]] = field(init=False, default_factory=lambda: dict[str, dict[str, QPushButton]]())
	"""Dictionnaire des Boutons d'action Reset, Update, Save (:class:`dict[str, QPushButton]`) pour chaque UI."""

	##################################################
	@property
	def localization(self) -> FiltersL:
		"""Groupe de paramètres liés aux filtres sur la localization (:class:`FiltersL <palm_tracer.Settings.Groups.FiltersL.FiltersL>`)."""
		return cast(FiltersL, self._settings["Localization"])

	##################################################
	@property
	def tracking(self) -> FiltersT:
		"""Groupe de paramètres liés aux filtres sur le suivi (:class:`FiltersT <palm_tracer.Settings.Groups.FiltersT.FiltersT>`)."""
		return cast(FiltersT, self._settings["Tracks"])

	##################################################
	def get_ui(self, name: str = "default", mode: int = -1) -> BaseUIGroup:
		ui = super().get_ui(name, mode)

		ui.layout.addItem(QSpacerItem(0, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

		self.buttons[name] = {"reset": QPushButton("Reset"), "update": QPushButton("Update"), "save": QPushButton("Save")}
		# Créer un layout horizontal pour les boutons
		actions = QHBoxLayout()
		Ui.init_layout(actions)
		actions.addWidget(self.buttons[name]["reset"])
		actions.addWidget(self.buttons[name]["update"])
		actions.addWidget(self.buttons[name]["save"])
		ui.layout.addRow(actions)
		return ui

	##################################################
	def deactivate_filters(self):
		""" Désactive tous les filtres."""
		self._settings["Save"].value = False
		self._settings["Plane"].active = False
		fl = cast(FiltersL, self._settings["Localization"])
		fl.deactivate_filters()
		ft = cast(FiltersT, self._settings["Tracks"])
		ft.deactivate_filters()

	##################################################
	def update_limits(self, plane_max: int | None = None):
		"""Mets à jour le min et le max de certains filtres."""
		with self.signal_blocked():
			if plane_max is not None:
				s = cast(CheckRangeInt, self._settings["Plane"])
				s.limits = [s.limits[0], plane_max]
				ft = cast(FiltersT, self._settings["Tracks"])
				s = cast(CheckRangeInt, ft["Length"])
				s.limits = [s.limits[0], plane_max]

	##################################################
	def connect_button(self, f: Any, ui_name: str = "default", name: str = "reset"):
		"""
		Connecte un bouton directement et non le paramètre en lui-même.

		:param f: Fonction ou slot à connecter.
		:param ui_name: Nom de l'interface à connecter.
		:param name: Nom du bouton dans l'interface.
		"""
		if ui_name in self.buttons and name in self.buttons[ui_name]:
			self.buttons[ui_name][name].clicked.connect(f)


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # crée et assigne le layout au widget
	group = Filters()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
