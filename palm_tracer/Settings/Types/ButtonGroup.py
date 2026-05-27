"""
Fichier contenant la classe :class:`Button` dérivée de :class:`.BaseSettingType`, qui permet la gestion d'un paramètre type bouton à cliquer.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from qtpy.QtCore import QSignalBlocker
from qtpy.QtWidgets import QButtonGroup

from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType
from palm_tracer.Settings.Types.BaseUI import BaseUI
from palm_tracer.Tools import Ui


##################################################
@dataclass
class ButtonGroup(BaseSettingType):
	"""
	Classe pour un paramètre spécifique de type groupe de boutons.

	:param label: Nom du paramètre à afficher.
	:param tooltip: Description détaillée en overlay.
	"""
	default: int = 0
	"""Valeur (position dans la liste) par défaut du paramètre (:class:`int`)."""
	_value: int = field(init=False, default=0)
	"""Valeur (position dans la liste) actuelle du paramètre (:class:`int`)."""

	_items: list[str] = field(default_factory=lambda: [""])
	"""Choix de la liste déroulante (:class:`list[str]`)."""

	group: dict[str, QButtonGroup] = field(init=False, default_factory=lambda: dict[str, QButtonGroup]())
	"""Dictionnaire des Groupes de boutons."""

	# ==================================================
	# region Getter/Setter
	# ==================================================
	##################################################
	def get_ui(self, name: str = "default") -> BaseUI:
		if name in self._uis: return self._uis[name]

		h, self.group[name], buttons = Ui.make_exclusive_btn_group(self._items, 0)

		ui = BaseUI(layout=h, boxes=list(buttons.values()))
		ui.set_tooltip(self.tooltip)  # .							  Ajout du Tooltip

		self.group[name].button(self.value).setChecked(True)
		self.group[name].idClicked.connect(self.set_value_from_ui)  # Connecte le changement de valeur pour que les autres UI se mettent à jour

		self._uis[name] = ui  # .									  Ajoute l'ui au dictionnaire
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
		for g in self.group.values():
			with QSignalBlocker(g): g.button(value).setChecked(True)

		self.emit(value)

	##################################################
	@property
	def current_text(self) -> str:
		"""Valeur actuelle du paramètre (élément dans la liste en :class:`str`)."""
		return self._items[self.value] if 0 <= self.value < len(self._items) else ""


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QWidget, QFormLayout, QPushButton

	app = QApplication(sys.argv)
	w = QWidget()
	form = QFormLayout(w)  # crée et assigne le layout au widget
	setting = ButtonGroup("Test", "tooltip", 0, ["1", "2", "3"])
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
