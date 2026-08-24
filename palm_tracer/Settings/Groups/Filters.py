"""Définit le groupe principal des paramètres de filtrage."""

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
	"""Regroupe les paramètres de filtrage communs aux localisations et aux trajectoires.

	Paramètres regroupés :

	- ``Save`` (:class:`~palm_tracer.Settings.Types.CheckBox.CheckBox`) : enregistre séparément les résultats filtrés ; valeur par défaut :
	  ``False``.
	- ``Plane`` (:class:`~palm_tracer.Settings.Types.CheckRangeInt.CheckRangeInt`) : intervalle des plans conservés ; valeur par défaut :
	  ``[1, 100000]``.
	- ``ROI`` (:class:`~palm_tracer.Settings.Types.CheckInt.CheckInt`) : indice de la zone d'intérêt utilisée pour le filtrage spatial.
	- ``Localization`` (:class:`~palm_tracer.Settings.Groups.FiltersL.FiltersL`) : filtres propres aux localisations.
	- ``Tracks`` (:class:`~palm_tracer.Settings.Groups.FiltersT.FiltersT`) : filtres propres aux trajectoires.

	.. todo:: Vérifier les ordres de grandeur et les valeurs par défaut des filtres, notamment la plage de l'intensité intégrée des localisations.
	"""

	label: str = "Filters"
	setting_list = {
			"Save":         [CheckBox, ["Save filtered", "Save filtered datas in _filtered.csv file.", False]],
			"Plane":        [CheckRangeInt, ["Plane", "Limits the planes to be used.", [1, 100000], [1, 100000]]],
			"ROI":          [CheckInt, ["ROI", "ROI selected for filtering. Selected ROI appear in yellow.", 1, [1, 1]]],
			"Localization": [FiltersL, []],
			"Tracks":       [FiltersT, []]
			}
	mode: int = 0
	buttons: dict[str, dict[str, QPushButton]] = field(init=False, default_factory=lambda: dict[str, dict[str, QPushButton]]())
	"""Dictionnaire des Boutons d'action Reset, Update, Save (:class:`dict[str, QPushButton]`) pour chaque UI."""

	##################################################
	def __post_init__(self):
		super().__post_init__()
		self.active = True

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
		ui.body_layout.setContentsMargins(5, 0, 0, 0)  # Très léger décalage.

		ui.layout.addItem(QSpacerItem(0, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

		self.buttons[name] = {"reset": QPushButton("Reset"), "update": QPushButton("Update"), "save": QPushButton("Save")}
		self.buttons[name]["reset"].setToolTip("Uncheck all filters and delete filtered data.")
		self.buttons[name]["update"].setToolTip("Compute filtered data.")
		self.buttons[name]["save"].setToolTip("Save filtered data in csv file.")
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
	def show_part(self, ui_name: str = "default", localization: bool = True, tracking: bool = True):
		"""
		Affiche/Cache les parties à filtrer.

		:param ui_name: Nom de l'interface à modifier.
		:param localization: Partie Localization.
		:param tracking: Partie Tracking.
		"""
		self.localization.get_ui(ui_name).show() if localization else self.localization.get_ui(ui_name).hide()
		self.tracking.get_ui(ui_name).show() if tracking else self.tracking.get_ui(ui_name).hide()


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
