"""
Fichier contenant la classe :class:`FileList` dérivée de :class:`.BaseSettingType`, qui permet la gestion d'un paramètre type liste de fichiers.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QComboBox, QFileDialog,QVBoxLayout, QHBoxLayout, QPushButton

from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType
from palm_tracer.Tools import Ui


##################################################
@dataclass
class FileList(BaseSettingType):
	"""
	Classe pour un paramètre spécifique de type recherche de fichier.

	Attributs :
		- **label** (:class:`str`) : Nom du paramètre à afficher.
		- **_layout** (:class:`QFormLayout`) : Le calque associé à ce paramètre, initialisé par défaut à un :class:`QFormLayout`.
		- **_signal** (:class:`SignalWrapper`) : Signal permettant de communiquer avec l'interface.
		- **default** (:class:`int`) : Valeur par défaut du paramètre (aucun fichier).
		- **items** (:class:`list[str]`) : Liste des fichiers actuels.
		- **box** (:class:`QComboBox`) : ComboBox affichant les fichiers de la liste.
		- **buttons** (:class:`dict[str, QPushButton]`) : Boutons d'action [+], [-], [clear].
	"""

	default: int = -1
	value: int = field(init=False, default=-1)

	items: list[str] = field(default_factory=lambda: [])
	"""Liste des fichiers actuels."""
	buttons: dict[str, QPushButton] = field(init=False)
	""" Boutons d'action [+], [-], [clear]."""

	_box: QComboBox = field(init=False)

	##################################################
	def get_value(self) -> int:
		self.value = self._box.currentIndex()
		return self.value

	##################################################
	def set_value(self, value: int):
		if 0 <= value < len(self.items):
			self.value = value
			self._box.setCurrentIndex(value)
			self.emit()

	##################################################
	def get_selected(self) -> str:
		value = self.get_value()
		if 0 <= value < len(self.items):
			return self.items[value]
		return ""

	##################################################
	def get_list(self) -> list[str]: return self.items

	##################################################
	def update_box(self, items: Optional[list[str]] = None):
		"""Met à jour la ComboBox pour refléter la liste actuelle des fichiers."""
		with self.signal_blocked():
			self._box.clear()
			if items is not None: self.items = items
			self._box.addItems(self.items)

	##################################################
	def add_file(self):
		"""Ajoute un fichier à la liste via un QFileDialog."""
		# Déterminer le répertoire initial pour la boîte de dialogue
		initial_dir = (self.items[-1] if self.items else ".")  # Utiliser le dernier fichier ou le répertoire courant
		path, _ = QFileDialog.getOpenFileName(None, "Sélectionner un fichier", initial_dir, "Tous les fichiers (*)")
		if path and Path(path).is_file():
			self.items.append(path)
			self.update_box()
			self.set_value(len(self.items) - 1)

	##################################################
	def remove_file(self):
		"""Supprime le fichier actuellement sélectionné dans la ComboBox."""
		current_index = self._box.currentIndex()
		if 0 <= current_index < len(self.items):
			self.items.pop(current_index)
			self.update_box()
			self.set_value(0)

	##################################################
	def clear_files(self):
		"""Vide la liste des fichiers."""
		self.items.clear()
		self.update_box()
		self.emit()

	##################################################
	def to_dict(self) -> dict[str, Any]:
		return {"type": type(self).__name__, "label": self.label, "default": self.default, "items": self.items, "value": self.value}

	##################################################
	def update_from_dict(self, data: dict[str, Any]):
		self.label = data.get("label", "")
		self.default = data.get("default", False)
		self.update_box(data.get("items", [""]))
		self.set_value(data.get("value", self.value))

	##################################################
	def initialize(self):
		self._layout = QVBoxLayout()
		Ui.init_layout(self._layout)

		self._box = QComboBox(None)						  # Création de la boite.
		self.update_box()								  # Ajout des choix possibles.
		self.set_value(self.default)					  # Définition de la valeur.
		self._box.currentIndexChanged.connect(self.emit)  # Ajout de la connexion lors d'un changement de selection

		# Créer les boutons d'action
		self.buttons = {"add": QPushButton("+"), "remove": QPushButton("-"), "clear": QPushButton("Clear")}
		self.buttons["add"].clicked.connect(self.add_file)
		self.buttons["remove"].clicked.connect(self.remove_file)
		self.buttons["clear"].clicked.connect(self.clear_files)

		# Créer un layout horizontal pour les boutons
		actions = QHBoxLayout()
		actions.addWidget(self.buttons["add"])
		actions.addWidget(self.buttons["remove"])
		actions.addWidget(self.buttons["clear"])

		self._layout.addLayout(actions)
		self._layout.addWidget(self._box)


	##################################################
	def reset(self): self.clear_files()
