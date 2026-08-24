"""Définit un paramètre de sélection dans une liste déroulante."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, cast, Optional

from qtpy.QtCore import QSignalBlocker
from qtpy.QtWidgets import QComboBox, QHBoxLayout, QLabel

from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType
from palm_tracer.Settings.Types.BaseUIType import BaseUIType


##################################################
@dataclass
class Combo(BaseSettingType):
	"""Représente un choix effectué dans une liste déroulante.

	:param label: Libellé affiché dans l'interface.
	:param tooltip: Description affichée dans l'infobulle.
	:param default: Indice sélectionné par défaut.
	:param _items: Libellés des choix proposés.
	"""

	default: int = 0
	"""Valeur (position dans la liste) par défaut du paramètre (:class:`int`)."""
	_value: int = field(init=False, default=0)
	"""Valeur (position dans la liste) actuelle du paramètre (:class:`int`)."""

	_items: list[str] = field(default_factory=lambda: [""])
	"""Choix de la liste déroulante (:class:`list[str]`)."""

	# ==================================================
	# region Getter/Setter
	# ==================================================
	##################################################
	def get_ui(self, name: str = "default") -> BaseUIType:
		if name in self._uis: return self._uis[name]

		box: QComboBox = QComboBox()
		ui = BaseUIType(layout=QHBoxLayout(), label=QLabel(self.label), boxes=[box])
		ui.set_tooltip(self.tooltip)  # .						   Ajout du Tooltip

		box.addItems(self._items)  # .							   Ajout des choix possibles.
		box.setCurrentIndex(self.value)
		box.currentIndexChanged.connect(self.set_value_from_ui)  # Connecte le changement de valeur pour que les autres UI se mettent à jour

		ui.layout.addWidget(box)  # .							   Ajout du champ de texte.
		ui.layout.addStretch(1)  # .							   Pousse tout à gauche, espace vide à droite.

		self._uis[name] = ui  # .								   Ajoute l'ui au dictionnaire
		return ui

	##################################################
	@property
	def value(self) -> int:
		"""Valeur actuelle du paramètre (position dans la liste en :class:`int`)."""
		return self._value

	##################################################
	@value.setter
	def value(self, value: int):
		"""Valeur actuelle du paramètre (position dans la liste en :class:`int`)."""
		if self._value == value: return
		self._value = value
		for ui in self._uis.values():
			b = cast(QComboBox, ui.boxes[0])
			with QSignalBlocker(b): b.setCurrentIndex(value)

		self.emit(value)

	##################################################
	@property
	def current_text(self) -> str:
		"""Valeur actuelle du paramètre (élément dans la liste en :class:`str`)."""
		return self._items[self.value] if 0 <= self.value < len(self._items) else ""

	##################################################
	@property
	def items(self) -> list[str]:
		"""Récupère la liste des éléments."""
		return self._items

	##################################################
	@items.setter
	def items(self, items: Optional[list[str]] = None):
		"""Mets à jour les :class:`QComboBox` pour refléter la liste actuelle des options."""
		if items is not None: self._items = items
		for ui in self._uis.values():
			b = cast(QComboBox, ui.boxes[0])
			with QSignalBlocker(b):
				b.clear()
				b.addItems(self._items)
		self.value = 0

	# ==================================================
	# endregion Getter/Setter
	# ==================================================

	# ==================================================
	# region Parsing
	# ==================================================
	##################################################
	def to_compact_dict(self) -> dict[str, Any]:
		return {"value": self.value, "items": self.items}

	##################################################
	def update_from_compact_dict(self, data: dict[str, Any]):
		self.items = data["items"]  # Récupération de la liste des éléments avant de mettre à jour la valeur
		self.value = data["value"]


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QWidget, QFormLayout, QPushButton

	app = QApplication(sys.argv)
	w = QWidget()
	form = QFormLayout(w)  # crée et assigne le layout au widget
	setting = Combo("Test", "tooltip", 0, ["1", "2", "3"])
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
