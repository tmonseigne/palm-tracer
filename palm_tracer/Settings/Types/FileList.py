"""
Fichier contenant la classe `FileList` dérivée de `BaseSettingType`, qui permet la gestion d'un paramètre type liste de fichiers.

.. todo::
	Envoi de signaux en double avec le update item et le currentIndexChanged à voir pour la suite, pour le moment ce n'est pas gênant.
	Il passe par une phase avec 0 Items (la fonction clear et envoie un signal à ce moment).
"""

from dataclasses import dataclass, field
from typing import Any

from qtpy.QtCore import QObject, Qt, Signal
from qtpy.QtWidgets import QComboBox, QFileDialog, QHBoxLayout, QPushButton

from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType


##################################################
class SignalWrapper(QObject):
	signal = Signal()

	def __init__(self): super().__init__()

	def connect(self, f): self.signal.connect(f)

	def emit(self): self.signal.emit()


##################################################
@dataclass
class FileList(BaseSettingType):
	"""
	Classe pour un paramètre spécifique de type recherche de fichier.

	Attributs :
			- **label (str)** : Nom du paramètre à afficher.
			- **_layout (QFormLayout)** : Le calque associé à ce paramètre, initialisé par défaut à un QFormLayout.
			- **default (int)** : Valeur par défaut du paramètre (aucun fichier).
        	- **items (list[str])** : Liste des fichiers actuels.
        	- **box (QComboBox)** : ComboBox affichant les fichiers de la liste.
        	- **buttons (dict[str, QPushButton])** : Boutons d'action [+], [-], [clear].
	"""

	default: int = -1
	items: list[str] = field(default_factory=lambda: [])
	value: int = field(init=False, default=-1)
	box: QComboBox = field(init=False)
	buttons: dict[str, QPushButton] = field(init=False)
	signal: SignalWrapper = field(init=False, default_factory=SignalWrapper)

	##################################################
	def get_value(self) -> int:
		self.value = self.box.currentIndex()
		return self.value

	##################################################
	def set_value(self, value: int):
		if 0 <= value < len(self.items):
			self.value = value
			self.box.setCurrentIndex(value)

	##################################################
	def get_selected(self) -> str:
		value = self.get_value()
		if 0 <= value < len(self.items):
			return self.items[value]
		return ""

	##################################################
	def get_list(self) -> list[str]: return self.items

	##################################################
	def update_box(self):
		"""Met à jour la ComboBox pour refléter la liste actuelle des fichiers."""
		self.box.clear()
		self.box.addItems(self.items)

	##################################################
	def add_file(self):  # pragma: no cover
		"""Ajoute un fichier à la liste via un QFileDialog."""
		# Déterminer le répertoire initial pour la boîte de dialogue
		initial_dir = (self.items[-1] if self.items else ".")  # Utiliser le dernier fichier ou le répertoire courant
		filename, _ = QFileDialog.getOpenFileName(None, "Sélectionner un fichier", initial_dir, "Tous les fichiers (*)")
		if filename:
			self.items.append(filename)
			self.update_box()
			self.set_value(len(self.items) - 1)

	##################################################
	def remove_file(self):  # pragma: no cover
		"""Supprime le fichier actuellement sélectionné dans la ComboBox."""
		current_index = self.box.currentIndex()
		if 0 <= current_index < len(self.items):
			self.items.pop(current_index)
			self.update_box()
			self.set_value(0)

	##################################################
	def clear_files(self):
		"""Vide la liste des fichiers."""
		self.items.clear()
		self.update_box()
		self.signal.emit()

	##################################################
	def to_dict(self) -> dict[str, Any]:
		return {"type": type(self).__name__, "label": self.label, "default": self.default, "items": self.items, "value": self.value}

	##################################################
	def update_from_dict(self, data: dict[str, Any]):
		self.label = data.get("label", "")
		self.default = data.get("default", False)
		self.items = data.get("items", [""])
		self.set_value(data.get("value", self.default))

	##################################################
	def initialize(self):
		super().initialize()  # Appelle l'initialisation de la classe mère.
		self.signal = SignalWrapper()
		self.box = QComboBox(None)	  # Création de la boite.
		# self.box.setFixedWidth(150) # Réduire la largeur de la boite.
		self.update_box()			  # Ajout des choix possibles.
		self.set_value(self.default)  # Définition de la valeur.
		self.box.currentIndexChanged.connect(self.signal.emit)  # Ajout de la connexion lors d'un changement de selection

		# Créer les boutons d'action
		self.buttons = {"add": QPushButton("+"), "remove": QPushButton("-"), "clear": QPushButton("Clear")}
		self.buttons["add"].clicked.connect(self.add_file)
		self.buttons["remove"].clicked.connect(self.remove_file)
		self.buttons["clear"].clicked.connect(self.clear_files)

		# Créer un layout horizontal pour les boutons
		button_layout = QHBoxLayout()
		button_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Définition de l'alignement du calque à gauche.
		button_layout.addWidget(self.buttons["add"])
		button_layout.addWidget(self.buttons["remove"])
		button_layout.addWidget(self.buttons["clear"])

		self.add_row(button_layout)
		self._layout.addRow(self.box)

	##################################################
	def reset(self): self.clear_files()
