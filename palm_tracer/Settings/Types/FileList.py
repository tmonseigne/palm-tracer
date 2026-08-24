"""Définit un paramètre contenant une liste de fichiers."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, cast, Optional

from qtpy.QtCore import QSignalBlocker
from qtpy.QtWidgets import QComboBox, QFileDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType
from palm_tracer.Settings.Types.BaseUIType import BaseUIType
from palm_tracer.Tools import Ui


##################################################
@dataclass
class FileList(BaseSettingType):
	"""
	Représente un paramètre contenant une liste de fichiers et une sélection active.

	:param label: Libellé affiché dans l'interface.
	:param tooltip: Description affichée dans l'infobulle.
	"""

	default: int = field(init=False, default=-1)
	"""Valeur (position dans la liste) par défaut du paramètre (:class:`int`)."""
	_value: int = field(init=False, default=-1)
	"""Valeur (position dans la liste) actuelle du paramètre (:class:`int`)."""

	_items: list[str] = field(init=False, default_factory=lambda: [])
	"""Liste des fichiers actuels (:class:`list[str]`)."""

	##################################################
	def reset(self):
		"""Réinitialise le paramètre à sa valeur par défaut."""
		self.clear_files()

	# ==================================================
	# region Getter/Setter
	# ==================================================
	##################################################
	def get_ui(self, name: str = "default") -> BaseUIType:
		if name in self._uis: return self._uis[name]

		btn_add, btn_rem, btn_clr = QPushButton("+"), QPushButton("-"), QPushButton("Clear")
		combo: QComboBox = QComboBox()

		ui = BaseUIType(layout=QVBoxLayout(), label=QLabel(self.label), boxes=[btn_add, btn_rem, btn_clr, combo])
		ui.set_tooltip(self.tooltip)  # .						   Ajout du Tooltip
		Ui.init_layout(ui.layout, 5, 5)

		combo.addItems(self._items)  # .							   Ajout des choix possibles.
		combo.currentIndexChanged.connect(self.set_value_from_ui)  # Connecte le changement de valeur pour que les autres UI se mettent à jour
		btn_add.clicked.connect(self.add_file)
		btn_rem.clicked.connect(self.remove_file)
		btn_clr.clicked.connect(self.clear_files)

		# Créer un layout horizontal pour les boutons
		actions = QHBoxLayout()
		actions.addWidget(btn_add)
		actions.addWidget(btn_rem)
		actions.addWidget(btn_clr)

		ui.layout.addLayout(actions)
		ui.layout.addWidget(combo)

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
			b = cast(QComboBox, ui.boxes[3])
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
		"""Met à jour les :class:`QComboBox` pour refléter la liste actuelle des options."""
		if items is not None: self._items = items
		for ui in self._uis.values():
			b = cast(QComboBox, ui.boxes[3])
			with QSignalBlocker(b):
				b.clear()
				b.addItems(self._items)
		self.value = 0

	# ==================================================
	# endregion Getter/Setter
	# ==================================================

	# ==================================================
	# region  Parsing
	# ==================================================
	##################################################
	def to_compact_dict(self) -> dict[str, Any]:
		return {"value": self._value, "items": self._items}

	##################################################
	def update_from_compact_dict(self, data: dict[str, Any]):
		self.items = data["items"]  # Récupération de la liste des éléments avant de mettre à jour la valeur
		self.value = data["value"]

	# ==================================================
	# endregion  Parsing
	# ==================================================

	# ==================================================
	# region Callbacks
	# ==================================================

	##################################################
	def add_file(self):
		"""Ajoute un fichier à la liste via un :class:`QFileDialog`."""
		# Déterminer le répertoire initial pour la boîte de dialogue
		initial_dir = (self._items[-1] if self._items else ".")  # Utiliser le dernier fichier ou le répertoire courant
		path, _ = QFileDialog.getOpenFileName(None, "Sélectionner un fichier", initial_dir, "Tous les fichiers (*)")
		if path and Path(path).is_file():
			self._items.append(path)
			self.items = None
			self.value = len(self._items) - 1

	##################################################
	def remove_file(self):
		"""Supprime le fichier actuellement sélectionné dans la :class:`QComboBox`."""
		current_index = self.value
		if 0 <= current_index < len(self._items):
			self._items.pop(current_index)
			self.items = None
			self.value = 0

	##################################################
	def clear_files(self):
		"""Vide la liste des fichiers."""
		self._items.clear()
		self.items = None
		self.value = -1
		self.emit()


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QWidget, QFormLayout

	app = QApplication(sys.argv)
	w = QWidget()
	form = QFormLayout(w)  # crée et assigne le layout au widget
	setting = FileList("Test", "tooltip")
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
