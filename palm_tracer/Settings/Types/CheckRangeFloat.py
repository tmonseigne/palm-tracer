"""Définit un intervalle flottant dont l'application peut être activée ou désactivée."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, cast

from qtpy.QtCore import QSignalBlocker
from qtpy.QtWidgets import QCheckBox, QDoubleSpinBox, QHBoxLayout, QLabel, QSpinBox

from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType
from palm_tracer.Settings.Types.BaseUIType import BaseUIType
from palm_tracer.Tools import Ui


##################################################
@dataclass
class CheckRangeFloat(BaseSettingType):
	"""
	Représente un intervalle flottant dont l'application peut être activée ou désactivée.

	:param label: Libellé affiché dans l'interface.
	:param tooltip: Description affichée dans l'infobulle.
	:param default: Bornes sélectionnées par défaut.
	:param _limits: Bornes minimale et maximale autorisées.
	:param step: Incrément appliqué par les boîtes de sélection numérique.
	:param precision: Nombre de décimales affichées.
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
		"""Réinitialise le paramètre à sa valeur par défaut."""
		super().reset()
		self.active = False

	# ==================================================
	# region Accesseurs
	# ==================================================
	##################################################
	def get_ui(self, name: str = "default") -> BaseUIType:
		if name in self._uis: return self._uis[name]

		checkbox: QCheckBox = QCheckBox()
		spin_min: QSpinBox = Ui.make_spin(None, minimum=self.limits[0], maximum=self.limits[1], step=self.step,
										  value=self.value[0], decimals=self.precision, buttons=False)
		spin_max: QSpinBox = Ui.make_spin(None, minimum=self.limits[0], maximum=self.limits[1], step=self.step,
										  value=self.value[1], decimals=self.precision, buttons=False)

		ui = BaseUIType(layout=QHBoxLayout(), label=QLabel(self.label), boxes=[checkbox, spin_min, spin_max])
		ui.set_tooltip(self.tooltip)  # .			   Ajout du Tooltip

		checkbox.setChecked(self.active)
		checkbox.toggled.connect(self.set_active)  # .	Connecte le changement de valeur pour que les autres UI se mettent à jour
		spin_min.setKeyboardTracking(False)  # .	   Empèche la mise à jour à chaque appuie clavier (attend la fin de l'édition)
		spin_min.valueChanged.connect(self.set_min)  # Connecte le changement de valeur pour que les autres UI se mettent à jour
		spin_max.setKeyboardTracking(False)  # .	   Empèche la mise à jour à chaque appuie clavier (attend la fin de l'édition)
		spin_max.valueChanged.connect(self.set_max)  # Connecte le changement de valeur pour que les autres UI se mettent à jour

		ui.layout.addWidget(checkbox)
		ui.layout.addWidget(spin_min)
		ui.layout.addWidget(QLabel("→"))
		ui.layout.addWidget(spin_max)
		ui.layout.addStretch(1)  # .				   Pousse tout à gauche, espace vide à droite.

		self._uis[name] = ui  # .					   Ajoute l'ui au dictionnaire
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

		if self.min > self.max: self.max = value
		else: self.emit(value)

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

		if self.max < self.min: self.min = value
		else: self.emit(value)

	##################################################
	@property
	def value(self) -> list[float]:
		"""Valeur actuelle du paramètre (:class:`list[float]`)."""
		return self._value

	##################################################
	@value.setter
	def value(self, value: list[float]):
		"""Valeur actuelle du paramètre (:class:`list[float]`)."""
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
		if self.min < self._limits[0]: self.min = self._limits[0]
		if self.max > self._limits[1]: self.max = self._limits[1]
		for ui in self._uis.values():
			for i in range(2):
				b = cast(QDoubleSpinBox, ui.boxes[i + 1])
				with QSignalBlocker(b): Ui.update_spin_limits(b, self._limits[0], self._limits[1])

	# ==================================================
	# endregion Accesseurs
	# ==================================================

	# ==================================================
	# region Sérialisation
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
	# endregion Sérialisation
	# ==================================================

	# ==================================================
	# region Fonctions de rappel
	# ==================================================
	##################################################
	def set_active(self, state: int):
		"""Met à jour l'état actif du groupe lorsque la checkbox est modifiée."""
		self.active = bool(state)

	##################################################
	def set_min(self, value: float):
		"""S'assure que min ≤ max."""
		self.min = value

	##################################################
	def set_max(self, value: float):
		"""S'assure que min ≤ max."""
		self.max = value


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QWidget, QFormLayout, QPushButton

	app = QApplication(sys.argv)
	w = QWidget()
	form = QFormLayout(w)  # Crée et affecte la mise en page au widget
	setting = CheckRangeFloat("Test", "tooltip")
	setting.get_ui("default").attach_to_form(form)
	setting.get_ui("second").attach_to_form(form)
	counter = 0


	def add_setting_ui():
		"""Ajoute une nouvelle interface du paramètre au formulaire."""
		global counter
		counter += 1
		name = f"dynamic_{counter}"
		setting.get_ui(name).attach_to_form(form)


	button = QPushButton("Ajouter une UI")
	button.clicked.connect(add_setting_ui)
	form.addRow(button)
	w.show()
	sys.exit(app.exec_())
