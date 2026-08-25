"""Définit un paramètre de sélection de valeurs entières et d'intervalles."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, cast

from qtpy.QtCore import QSignalBlocker
from qtpy.QtGui import QValidator
from qtpy.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QLineEdit

from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType
from palm_tracer.Settings.Types.BaseUIType import BaseUIType


##################################################
class IntSelectionValidator(QValidator):
	"""Valide la syntaxe d'une sélection de valeurs entières et d'intervalles."""

	##################################################
	def validate(self, text: str, pos: int) -> tuple[QValidator.State, str, int]:
		"""
		Valide la syntaxe d'une sélection entière.

		Les valeurs individuelles et les intervalles sont séparés par ``;``.
		Un intervalle est défini avec ``-``.

		:param text: Texte à valider.
		:param pos: Position actuelle du curseur.
		:return: État de validation, texte et position du curseur.
		"""
		if not text.strip(): return QValidator.State.Acceptable, text, pos

		# Pendant la saisie, on autorise uniquement les caractères utiles.
		if re.fullmatch(r"[0-9;\-\s]*", text) is None: return QValidator.State.Invalid, text, pos

		try: CheckIntSelection.parse(text)
		except ValueError: return QValidator.State.Intermediate, text, pos

		return QValidator.State.Acceptable, text, pos


##################################################
@dataclass
class CheckIntSelection(BaseSettingType):
	"""
	Représente une sélection activable de valeurs entières et d'intervalles.

	Les éléments sont séparés par des points-virgules et les intervalles par un tiret.
	Par exemple, ``1-10;15;20-25`` sélectionne les valeurs de 1 à 10, la valeur 15 et les valeurs de 20 à 25.

	:param label: Libellé affiché dans l'interface.
	:param tooltip: Description affichée dans l'infobulle.
	:param default: Sélection textuelle par défaut.
	"""

	default: str = ""
	"""Valeur par défaut du paramètre (:class:`str`)."""
	_value: str = field(init=False, default="")
	"""Valeur actuelle du paramètre (:class:`str`)."""
	_active: bool = field(init=False, default=False)
	"""Indicateur d'activation du paramètre."""

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
		line_edit = QLineEdit(self.value)
		line_edit.setValidator(IntSelectionValidator(line_edit))
		line_edit.setPlaceholderText("Ex: 1-10;15;20-25")

		ui = BaseUIType(layout=QHBoxLayout(), label=QLabel(self.label), boxes=[checkbox, line_edit])
		ui.set_tooltip(self.tooltip)  # .			 Ajout du Tooltip

		checkbox.setChecked(self.active)
		checkbox.toggled.connect(self.set_active)  # Connecte le changement de valeur pour que les autres UI se mettent à jour
		line_edit.editingFinished.connect(lambda: self.set_value_from_ui(line_edit.text()))  # Connecte le changement de valeur uniquement à la fin

		ui.layout.addWidget(checkbox)
		ui.layout.addWidget(line_edit)

		self._uis[name] = ui  # .					 Ajoute l'ui au dictionnaire
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
	def value(self) -> str:
		"""Sélection actuelle sous sa forme textuelle normalisée (:class:`str`)."""
		return self._value

	##################################################
	@value.setter
	def value(self, value: str):
		"""Contrôle et normalise la modification de la sélection."""
		normalized = self.normalize(value)
		if self._value == normalized: return
		self._value = normalized
		for ui in self._uis.values():
			b = cast(QLineEdit, ui.boxes[1])
			with QSignalBlocker(b): b.setText(normalized)

		self.emit(value)

	##################################################
	@property
	def ranges(self) -> list[tuple[int, int]]:
		"""Intervalles correspondant à la sélection actuelle."""
		return self.parse(self.value)

	# ==================================================
	# endregion Accesseurs
	# ==================================================

	# ==================================================
	# region Sélection
	# ==================================================
	##################################################
	@staticmethod
	def parse(value: str) -> list[tuple[int, int]]:
		"""
		Convertit une sélection textuelle en intervalles entiers.

		:param value: Sélection à convertir, par exemple ``"1-10;15;20-25"``.
		:return: Liste d'intervalles inclusifs sous la forme ``[(min, max), ...]``.
		"""
		value = value.strip()
		if not value: return []

		ranges: list[tuple[int, int]] = []
		for element in value.split(";"):
			element = element.strip()
			if not element: continue

			match = re.fullmatch(r"(\d+)(?:\s*-+\s*(\d+))?", element)
			if match is None: continue

			minimum = int(match.group(1))
			maximum = int(match.group(2)) if match.group(2) is not None else minimum
			ranges.append((maximum, minimum)) if minimum > maximum else ranges.append((minimum, maximum))

		ranges.sort()
		# Fusion des intervalles consécutifs (ou déjà présent dans le range actuel)
		merged: list[tuple[int, int]] = []
		for minimum, maximum in ranges:
			if not merged or minimum > merged[-1][1] + 1:
				merged.append((minimum, maximum))
				continue

			merged[-1] = (merged[-1][0], max(merged[-1][1], maximum))

		return merged

	##################################################
	@classmethod
	def normalize(cls, value: str) -> str:
		"""
		Normalise la représentation textuelle d'une sélection.

		:param value: Sélection à normaliser.
		:return: Sélection normalisée sans espaces superflus.
		"""
		return ";".join(str(minimum) if minimum == maximum else f"{minimum}-{maximum}" for minimum, maximum in cls.parse(value))

	##################################################
	def contains(self, value: int) -> bool:
		"""
		Indique si une valeur entière appartient à la sélection.

		:param value: Valeur à rechercher.
		:return: ``True`` si la valeur appartient à au moins un intervalle, sinon ``False``.
		"""
		return any(minimum <= value <= maximum for minimum, maximum in self.ranges)

	# ==================================================
	# endregion Sélection
	# ==================================================

	# ==================================================
	# region Sérialisation
	# ==================================================
	##################################################
	def to_compact_dict(self) -> dict[str, Any]:
		return {"value": self.value, "active": self.active}

	##################################################
	def update_from_compact_dict(self, data: dict[str, Any]):
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
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QWidget, QFormLayout, QPushButton

	app = QApplication(sys.argv)
	w = QWidget()
	form = QFormLayout(w)  # Crée et affecte la mise en page au widget
	setting = CheckIntSelection("Test", "tooltip")
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
