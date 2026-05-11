"""
Fichier contenant la classe :class:`CheckBox` dérivée de :class:`.BaseSettingType`, qui permet la gestion d'un paramètre type case à cocher.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, cast

from qtpy.QtCore import QSignalBlocker, Qt
from qtpy.QtWidgets import QCheckBox, QHBoxLayout, QLabel

from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType
from palm_tracer.Settings.Types.BaseUI import BaseUI


##################################################
@dataclass
class CheckBox(BaseSettingType):
	"""
	Classe pour un paramètre spécifique de type case à cocher.

	:param label: Nom du paramètre à afficher
	:param tooltip: Description détaillée en overlay.
	:param default: Valeur par défaut du paramètre.
	"""

	default: bool = False
	"""Valeur par défaut du paramètre (:class:`bool`)."""
	_value: bool = field(init=False, default=False)
	"""Valeur actuelle du paramètre (:class:`bool`)."""

	# ==================================================
	# region Getter/Setter
	# ==================================================
	##################################################
	def get_ui(self, name: str = "default") -> BaseUI:
		if name in self._uis: return self._uis[name]

		box: QCheckBox = QCheckBox()
		ui = BaseUI(layout=QHBoxLayout(), label=QLabel(self.label), boxes=[box])
		ui.set_tooltip(self.tooltip)  # .					Ajout du Tooltip

		box.stateChanged.connect(self.set_value_from_ui)  # Connecte le changement de valeur pour que les autres UI se mettent à jour

		ui.layout.addWidget(box)  # .						Ajout du champ de texte.
		ui.layout.addStretch(1)  # .						Pousse tout à gauche, espace vide à droite.

		self._uis[name] = ui  # .							Ajoute l'ui au dictionnaire
		return ui

	##################################################
	@property
	def value(self) -> bool:
		"""Valeur actuelle du paramètre (:class:`bool`)."""
		return self._value

	##################################################
	@value.setter
	def value(self, value: bool):
		"""Valeur actuelle du paramètre (:class:`bool`)."""
		if self._value == value: return
		self._value = value
		for ui in self._uis.values():
			b = cast(QCheckBox, ui.boxes[0])
			with QSignalBlocker(b): b.setCheckState(Qt.CheckState.Checked if value else Qt.CheckState.Unchecked)

		self.emit(value)


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QWidget, QFormLayout

	app = QApplication(sys.argv)
	w = QWidget()
	form = QFormLayout(w)  # crée et assigne le layout au widget
	setting = CheckBox("Test", "tooltip")
	setting.get_ui("default").attach_to_form(form)
	setting.get_ui("second").attach_to_form(form)
	w.show()
	sys.exit(app.exec_())
