"""
Fichier contenant la classe :class:`CheckRangeInt` dérivée de :class:`.BaseSettingType`, qui permet la gestion d'un paramètre type interval de nombre flottant.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, cast

from qtpy.QtCore import QSignalBlocker, Qt
from qtpy.QtWidgets import QCheckBox, QDoubleSpinBox, QHBoxLayout, QLabel, QSpinBox

from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType
from palm_tracer.Settings.Types.BaseUI import BaseUI
from palm_tracer.Tools import Ui


##################################################
@dataclass
class CheckRangeFloat(BaseSettingType):
	"""
	Classe pour un paramètre spécifique de type interval de nombre flottant.

	:param label: Nom du paramètre à afficher
	:param tooltip: Description détaillée en overlay.
	:param default: Valeurs par défaut du paramètre.
	:param _limits: Valeurs limites du paramètre.
	:param precision: Précision du paramètre.
	"""

	default: list[float] = field(default_factory=lambda: [-1.0, 1.0])
	"""Valeur par défaut du paramètre (:class:`list[float]`)."""
	_value: list[float] = field(init=False, default_factory=lambda: [-1.0, 1.0])
	"""Valeur actuelle du paramètre (:class:`list[float]`)."""

	_active: bool = field(init=False, default=False)
	"""Indicateur d'activation du paramètre."""
	_limits: list[float] = field(default_factory=lambda: [-1.0, 1.0])
	"""Valeurs limites du paramètre."""
	step: float = 0.1
	"""Pas à chaque appui sur une des flèches du paramètre."""
	precision: int = 2
	"""Précision du paramètre."""

	##################################################
	def reset(self):
		super().reset()
		self.active = False

	# ==================================================
	# region Getter/Setter
	# ==================================================
	##################################################
	def get_ui(self, name: str = "default") -> BaseUI:
		if name in self._uis: return self._uis[name]

		checkbox: QCheckBox = QCheckBox()
		spin_min: QSpinBox = Ui.make_spin(None, minimum=self.limits[0], maximum=self.limits[1], step=self.step,
										  value=self.default[0], decimals=self.precision, buttons=False)
		spin_max: QSpinBox = Ui.make_spin(None, minimum=self.limits[0], maximum=self.limits[1], step=self.step,
										  value=self.default[1], decimals=self.precision, buttons=False)

		ui = BaseUI(layout=QHBoxLayout(), label=QLabel(self.label), boxes=[checkbox, spin_min, spin_max])
		ui.set_tooltip(self.tooltip)  # .				  Ajout du Tooltip

		checkbox.stateChanged.connect(self.set_active)  # Connecte le changement de valeur pour que les autres UI se mettent à jour
		spin_min.setKeyboardTracking(False)  # .		  Empèche la mise à jour à chaque appuie clavier (attend la fin de l'édition)
		spin_min.valueChanged.connect(self.set_min)  # .  Connecte le changement de valeur pour que les autres UI se mettent à jour
		spin_max.setKeyboardTracking(False)  # .		  Empèche la mise à jour à chaque appuie clavier (attend la fin de l'édition)
		spin_max.valueChanged.connect(self.set_max)  # .  Connecte le changement de valeur pour que les autres UI se mettent à jour

		ui.layout.addWidget(checkbox)
		ui.layout.addWidget(spin_min)
		ui.layout.addWidget(QLabel("→"))
		ui.layout.addWidget(spin_max)
		ui.layout.addStretch(1)  # .					  Pousse tout à gauche, espace vide à droite.

		self._uis[name] = ui  # .						  Ajoute l'ui au dictionnaire
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
			with QSignalBlocker(b): b.setCheckState(Qt.CheckState.Checked if value else Qt.CheckState.Unchecked)

	##################################################
	@property
	def min(self) -> float:
		"""Indicateur de la valeur minimale du paramètre (:class:`float`)."""
		return self._value[0]

	##################################################
	@min.setter
	def min(self, value: float):
		"""Contrôle la modification de la valeur minimale."""
		if self._value[0] == value: return
		self._value[0] = value
		for ui in self._uis.values():
			b = cast(QDoubleSpinBox, ui.boxes[1])
			with QSignalBlocker(b): b.setValue(value)
		self.emit(value)

	##################################################
	@property
	def max(self) -> float:
		"""Indicateur de la valeur maximale du paramètre (:class:`float`)."""
		return self._value[1]

	##################################################
	@max.setter
	def max(self, value: float):
		"""Contrôle la modification de la valeur maximale."""
		if self._value[1] == value: return
		self._value[1] = value
		for ui in self._uis.values():
			b = cast(QDoubleSpinBox, ui.boxes[2])
			with QSignalBlocker(b): b.setValue(value)
		self.emit(value)

	##################################################
	@property
	def value(self) -> list[float]:
		"""Valeur actuelle du paramètre (:class:`list[float]`)."""
		return self._value

	##################################################
	@value.setter
	def value(self, value: list[float]):
		"""Valeur actuelle du paramètre (:class:`list[float]`)."""
		if self._value == value: return
		self._value = value
		self.min = value[0]
		self.max = value[1]

	##################################################
	@property
	def limits(self) -> list[float]:
		"""Valeur actuelle du paramètre (:class:`list[float]`)."""
		return self._limits

	##################################################
	@limits.setter
	def limits(self, value: list[float]):
		"""Valeur actuelle du paramètre (:class:`list[float]`)."""
		if self._limits == value: return
		self._limits = value
		for ui in self._uis.values():
			for i in range(2):
				b = cast(QDoubleSpinBox, ui.boxes[i + 1])
				with QSignalBlocker(b): Ui.update_spin_limits(b, self._limits[0], self._limits[1])

	# ==================================================
	# endregion Getter/Setter
	# ==================================================

	# ==================================================
	# region  Parsing
	# ==================================================
	##################################################
	def to_dict(self) -> dict[str, Any]:
		return {"type":  type(self).__name__, "label": self.label, "default": self.default, "active": self._active,
				"limit": self.limits, "step": self.step, "precision": self.precision, "value": self._value}

	##################################################
	def update_from_dict(self, data: dict[str, Any]):
		# Mise à jour des membres
		self.label = data.get("label", "")
		self.default = data.get("default", False)
		self.active = data.get("active", False)
		self.limits = data.get("limits", [-1.0, 1.0])
		self.step = data.get("step", 0.1)
		self.precision = data.get("precision", 2)
		self.value = data.get("value", self.default)

	# ==================================================
	# endregion Parsing
	# ==================================================

	# ==================================================
	# region  Callbacks
	# ==================================================
	##################################################
	def set_active(self, state: int):
		"""Mets à jour l'état actif du groupe lorsque la checkbox est modifiée."""
		self.active = bool(state)

	##################################################
	def set_min(self, value: float):
		"""S'assure que min ≤ max."""
		self.min = value
		if self.min > self.max: self.max = value

	##################################################
	def set_max(self, value: float):
		"""S'assure que min ≤ max."""
		self.max = value
		if self.max < self.min: self.min = value


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QWidget, QFormLayout

	app = QApplication(sys.argv)
	w = QWidget()
	form = QFormLayout(w)  # crée et assigne le layout au widget
	spin = CheckRangeFloat("Test", "tooltip")
	spin.get_ui("default").attach_to_form(form)
	spin.get_ui("second").attach_to_form(form)
	w.show()
	sys.exit(app.exec_())
