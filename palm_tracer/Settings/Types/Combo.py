"""
Fichier contenant la classe :class:`Combo` dérivée de :class:`.BaseSettingType`, qui permet la gestion d'un paramètre type liste déroulante.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, cast, Optional

from qtpy.QtCore import QSignalBlocker
from qtpy.QtWidgets import QComboBox, QHBoxLayout, QLabel

from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType
from palm_tracer.Settings.Types.BaseUI import BaseUI


##################################################
@dataclass
class Combo(BaseSettingType):
	"""
	Classe pour un paramètre spécifique de type liste déroulante.

	:param label: Nom du paramètre à afficher
	:param tooltip: Description détaillée en overlay.
	:param default: Valeurs par défaut du paramètre.
	:param _items: Choix de la liste déroulante.
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
	def get_ui(self, name: str = "default") -> BaseUI:
		if name in self._uis: return self._uis[name]

		box: QComboBox = QComboBox()
		ui = BaseUI(layout=QHBoxLayout(), label=QLabel(self.label), boxes=[box])
		ui.set_tooltip(self.tooltip)  # .						   Ajout du Tooltip

		box.addItems(self._items)  # .							   Ajout des choix possibles.
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
			b = cast(QComboBox, ui.boxes[3])
			with QSignalBlocker(b):
				b.clear()
				b.addItems(self._items)

	# ==================================================
	# endregion Getter/Setter
	# ==================================================

	# ==================================================
	# region Parsing
	# ==================================================
	##################################################
	def to_compact_dict(self) -> dict[str, Any]: return {"value": self.value, "items": self.items}

	##################################################
	def update_from_compact_dict(self, data: dict[str, Any]):
		self.items = data["items"]  # Récupération de la liste des éléments avant de mettre à jour la valeur
		self.value = data["value"]


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QWidget, QFormLayout

	app = QApplication(sys.argv)
	w = QWidget()
	form = QFormLayout(w)  # crée et assigne le layout au widget
	setting = Combo("Test", "tooltip", 0, ["1", "2", "3"])
	setting.get_ui("default").attach_to_form(form)
	setting.get_ui("second").attach_to_form(form)
	w.show()
	sys.exit(app.exec_())
