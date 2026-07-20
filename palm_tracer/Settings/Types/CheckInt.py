"""
Fichier contenant la classe :class:`CheckInt` dérivée de :class:`.BaseSettingType`, qui permet la gestion d'un paramètre type nombre entier.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, cast

from qtpy.QtCore import QSignalBlocker
from qtpy.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QSpinBox

from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType
from palm_tracer.Settings.Types.BaseUIType import BaseUIType
from palm_tracer.Tools import Ui


##################################################
@dataclass
class CheckInt(BaseSettingType):
	"""
	Classe pour un paramètre spécifique de type nombre entier.

	:param label: Nom du paramètre à afficher.
	:param tooltip: Description détaillée en overlay.
	:param default: Valeurs par défaut du paramètre.
	:param _limits: Valeurs limites du paramètre.
	"""

	default: int = 0
	"""Valeur par défaut du paramètre (:class:`int`)."""
	_value: int = field(init=False, default=0)
	"""Valeur actuelle du paramètre (:class:`int`)."""
	_active: bool = field(init=False, default=False)
	"""Indicateur d'activation du paramètre."""
	_limits: list[int] = field(default_factory=lambda: [0, 100])
	"""Valeurs limites du paramètre."""
	step: int = 1
	"""Pas à chaque appui sur une des flèches du paramètre."""

	##################################################
	def reset(self):
		super().reset()
		self.active = False

	# ==================================================
	# region Getter/Setter
	# ==================================================
	##################################################
	def get_ui(self, name: str = "default") -> BaseUIType:
		if name in self._uis: return self._uis[name]

		checkbox: QCheckBox = QCheckBox()
		spin: QSpinBox = Ui.make_spin(None, minimum=self.limits[0], maximum=self.limits[1], step=self.step, value=self.value, buttons=False)

		ui = BaseUIType(layout=QHBoxLayout(), label=QLabel(self.label), boxes=[checkbox, spin])
		ui.set_tooltip(self.tooltip)  # .					 Ajout du Tooltip

		checkbox.setChecked(self.active)
		checkbox.toggled.connect(self.set_active)  # .		 Connecte le changement de valeur pour que les autres UI se mettent à jour
		spin.setKeyboardTracking(False)  # .				 Empèche la mise à jour à chaque appuie clavier (attend la fin de l'édition)
		spin.valueChanged.connect(self.set_value_from_ui)  # Connecte le changement de valeur pour que les autres UI se mettent à jour

		ui.layout.addWidget(checkbox)
		ui.layout.addWidget(spin)
		ui.layout.addStretch(1)  # .						 Pousse tout à gauche, espace vide à droite.

		self._uis[name] = ui  # .							 Ajoute l'ui au dictionnaire
		return ui

	##################################################
	@property
	def active(self) -> bool:
		"""Indicateur d'activation du paramètre (:class:`bool`)."""
		return self._active

	##################################################
	@active.setter
	def active(self, value: bool):
		"""Contrôle la modification de l'état actif."""
		if self._active == value: return
		self._active = value
		for ui in self._uis.values():
			b = cast(QCheckBox, ui.boxes[0])
			with QSignalBlocker(b): b.setChecked(value)
		self.emit(value)

	##################################################
	@property
	def value(self) -> int:
		"""Valeur actuelle du paramètre (:class:`list[int]`)."""
		return self._value

	##################################################
	@value.setter
	def value(self, value: int):
		"""Valeur actuelle du paramètre (:class:`list[int]`)."""
		if self._value == value: return
		self._value = value
		for ui in self._uis.values():
			b = cast(QSpinBox, ui.boxes[1])
			with QSignalBlocker(b): b.setValue(value)

		self.emit(value)

	##################################################
	@property
	def limits(self) -> list[int]:
		"""Valeur actuelle du paramètre (:class:`list[int]`)."""
		return self._limits

	##################################################
	@limits.setter
	def limits(self, value: list[int]):
		"""Valeur actuelle du paramètre (:class:`list[int]`)."""
		if self._limits == value: return
		self._limits = value
		if self._value < self._limits[0]: self._value = self._limits[0]
		if self._value > self._limits[1]: self._value = self._limits[1]
		for ui in self._uis.values():
			b = cast(QSpinBox, ui.boxes[1])
			with QSignalBlocker(b): Ui.update_spin_limits(b, self._limits[0], self._limits[1])

	# ==================================================
	# endregion Getter/Setter
	# ==================================================

	# ==================================================
	# region Parsing
	# ==================================================
	##################################################
	def to_compact_dict(self) -> dict[str, Any]:
		return {"value": self.value, "limits": self.limits, "active": self.active}

	##################################################
	def update_from_compact_dict(self, data: dict[str, Any]):
		self.limits = data["limits"]  # Récupération des limites avant de mettre à jour la valeur
		self.value = data["value"]
		self.active = data["active"]

	# ==================================================
	# endregion Parsing
	# ==================================================

	# ==================================================
	# region Callbacks
	# ==================================================
	##################################################
	def set_active(self, state: int):
		"""Mets à jour l'état actif du groupe lorsque la checkbox est modifiée."""
		self.active = bool(state)


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QWidget, QFormLayout, QPushButton

	app = QApplication(sys.argv)
	w = QWidget()
	form = QFormLayout(w)  # crée et assigne le layout au widget
	setting = CheckInt("Test", "tooltip")
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
