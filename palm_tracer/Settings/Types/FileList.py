"""
Fichier contenant la classe :class:`FileList` dérivée de :class:`.BaseSettingType`, qui permet la gestion d'un paramètre type liste de fichiers.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from qtpy.QtWidgets import QComboBox, QFileDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType
from palm_tracer.Tools import Ui


##################################################
@dataclass
class FileList(BaseSettingType):
	"""
	Classe pour un paramètre spécifique de type recherche de fichier.

	:param label: Nom du paramètre à afficher
	:param tooltip: Description détaillée en overlay.
	"""

	default: int = field(init=False, default=0)
	_value: int = field(init=False, default=0)

	items: list[str] = field(init=False, default_factory=lambda: [])
	"""Liste des fichiers actuels (:class:`list[str]`)."""
	buttons: dict[str, QPushButton] = field(init=False)
	"""Boutons d'action [+], [-], [clear] (:class:`dict[str, QPushButton]`)."""

	_box: QComboBox = field(init=False, default_factory=lambda: QComboBox())

	# ==================================================
	# region Initialization
	# ==================================================
	##################################################
	def initialize(self):
		self._label_widget = QLabel(self.label)
		self._layout = QVBoxLayout()
		Ui.init_layout(self._layout)

		self.update_box()  # .								Ajout des choix possibles.
		self.value = self.default  # .					Définition de la valeur.
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

	# ==================================================
	# endregion Initialization
	# ==================================================

	# ==================================================
	# region Getter/Setter
	# ==================================================
	##################################################
	@property
	def value(self) -> int:
		"""Valeur actuelle du paramètre (:class:`int`)."""
		self._value = self._box.currentIndex()
		return self._value

	##################################################
	@value.setter
	def value(self, value: int):
		"""Valeur actuelle du paramètre (:class:`int`)."""
		if 0 <= value < len(self.items):
			self._value = value
			self._box.setCurrentIndex(value)
			self.emit()

	##################################################
	def get_selected(self) -> str:
		"""Récupère l'élément sélectionné."""
		value = self._value
		if 0 <= value < len(self.items):
			return self.items[value]
		return ""

	##################################################
	def get_list(self) -> list[str]:
		"""Récupère la liste des éléments."""
		return self.items

	# ==================================================
	# endregion Getter/Setter
	# ==================================================

	# ==================================================
	# region  Parsing
	# ==================================================
	##################################################
	def to_dict(self) -> dict[str, Any]:
		return {"type": type(self).__name__, "label": self.label, "default": self.default, "items": self.items, "value": self._value}

	##################################################
	def update_from_dict(self, data: dict[str, Any]):
		self.label = data.get("label", "")
		self.default = data.get("default", False)
		self.update_box(data.get("items", [""]))
		self.value = data.get("value", self._value)

	##################################################
	def to_compact_dict(self) -> dict[str, Any]:
		"""Renvoie un dictionnaire minimal contenant la valeur du setting."""
		return {"items": self.items, "value": self._value}

	##################################################
	def update_from_compact_dict(self, data: dict[str, Any]):
		"""Mets à jour la classe à partir d'un dictionnaire minimal."""
		self.update_box(data["items"])
		self.value = data["value"]

	# ==================================================
	# endregion  Parsing
	# ==================================================

	# ==================================================
	# region Callbacks
	# ==================================================
	##################################################
	def update_box(self, items: Optional[list[str]] = None):
		"""Mets à jour la ComboBox pour refléter la liste actuelle des fichiers."""
		with self.signal_blocked():
			self._box.clear()
			if items is not None: self.items = items
			self._box.addItems(self.items)

	##################################################
	def add_file(self):
		"""Ajoute un fichier à la liste via un :class:`QFileDialog`."""
		# Déterminer le répertoire initial pour la boîte de dialogue
		initial_dir = (self.items[-1] if self.items else ".")  # Utiliser le dernier fichier ou le répertoire courant
		path, _ = QFileDialog.getOpenFileName(None, "Sélectionner un fichier", initial_dir, "Tous les fichiers (*)")
		if path and Path(path).is_file():
			self.items.append(path)
			self.update_box()
			self.value = len(self.items) - 1

	##################################################
	def remove_file(self):
		"""Supprime le fichier actuellement sélectionné dans la :class:`QComboBox`."""
		current_index = self._box.currentIndex()
		if 0 <= current_index < len(self.items):
			self.items.pop(current_index)
			self.update_box()
			self.value = 0

	##################################################
	def clear_files(self):
		"""Vide la liste des fichiers."""
		self.items.clear()
		self.update_box()
		self.emit()
