"""
Fichier contenant la classe :class:`CheckBox` dérivée de :class:`.BaseSettingType`, qui permet la gestion d'un paramètre type case à cocher.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import cast

from qtpy.QtCore import QSignalBlocker
from qtpy.QtWidgets import QCheckBox, QHBoxLayout, QLabel

from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType
from palm_tracer.Settings.Types.BaseUIType import BaseUIType


##################################################
@dataclass
class CheckBox(BaseSettingType):
	"""
	Classe pour un paramètre spécifique de type case à cocher.

	:param label: Nom du paramètre à afficher.
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
	def get_ui(self, name: str = "default") -> BaseUIType:
		if name in self._uis: return self._uis[name]

		box: QCheckBox = QCheckBox()
		ui = BaseUIType(layout=QHBoxLayout(), label=QLabel(self.label), boxes=[box])
		ui.set_tooltip(self.tooltip)  # .			   Ajout du Tooltip

		box.setChecked(self._value)
		box.toggled.connect(self.set_value_from_ui)  # Connecte le changement de valeur pour que les autres UI se mettent à jour

		ui.layout.addWidget(box)  # .				   Ajout du champ de texte.
		ui.layout.addStretch(1)  # .				   Pousse tout à gauche, espace vide à droite.

		self._uis[name] = ui  # .					   Ajoute l'ui au dictionnaire
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
			with QSignalBlocker(b): b.setChecked(self._value)

		self.emit(value)


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QWidget, QFormLayout, QPushButton

	app = QApplication(sys.argv)
	w = QWidget()
	form = QFormLayout(w)  # crée et assigne le layout au widget
	setting = CheckBox("Test", "tooltip")
	setting.get_ui("default").attach_to_form(form)
	setting.get_ui("second").attach_to_form(form)
	counter = 0


	def add_setting_ui():
		global counter
		counter += 1
		name = f"dynamic_{counter}"
		setting.get_ui(name).attach_to_form(form)


	button = QPushButton("Ajouter une UI")
	button.clicked.connect(add_setting_ui)
	form.addRow(button)
	w.show()
	sys.exit(app.exec_())
