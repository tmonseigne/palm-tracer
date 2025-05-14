"""
Fichier contenant la classe :class:`Combo` dérivée de :class:`.BaseSettingType`, qui permet la gestion d'un paramètre type liste déroulante.
"""

from dataclasses import dataclass, field
from typing import Any, Optional

from qtpy.QtWidgets import QComboBox

from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType


##################################################
@dataclass
class Combo(BaseSettingType):
	"""
	Classe pour un paramètre spécifique de type liste déroulante.

	Attributs :
			- **label (str)** : Nom du paramètre à afficher.
			- **_layout (QFormLayout)** : Le calque associé à ce paramètre, initialisé par défaut à un QFormLayout.
			- **_signal (SignalWrapper)** : Signal permettant de communiquer avec l'interface.
			- **default (int)** : Valeur par défaut du paramètre.
			- **items (list[str])** : Choix de la liste déroulante.
			- **value (int)** : Valeur actuelle du paramètre.
			- **box (QComboBox)** : Objet QT permettant de manipuler le paramètre.
	"""

	default: int = 0
	"""Valeur par défaut du paramètre."""
	items: list[str] = field(default_factory=lambda: [""])
	"""Choix de la liste déroulante."""
	value: int = field(init=False, default=0)
	"""Valeur actuelle du paramètre."""
	box: QComboBox = field(init=False)
	"""Objet QT permettant de manipuler le paramètre."""

	##################################################
	def get_value(self) -> int:
		self.value = self.box.currentIndex()
		return self.value

	##################################################
	def set_value(self, value: int):
		self.value = value
		self.box.setCurrentIndex(value)

	##################################################
	def update_box(self, items: Optional[list[str]] = None):
		"""Met à jour la ComboBox pour refléter la liste actuelle des options."""
		self.box.clear()
		if items is not None: self.items = items
		self.box.addItems(self.items)

	##################################################
	def to_dict(self) -> dict[str, Any]:
		return {"type": type(self).__name__, "label": self.label, "default": self.default, "items": self.items, "value": self.value}

	##################################################
	def update_from_dict(self, data: dict[str, Any]):
		# Mise à jour des membres
		self.label = data.get("label", "")
		self.default = data.get("default", False)
		self.update_box(data.get("items", [""]))
		self.set_value(data.get("value", self.default))

	##################################################
	def initialize(self):
		super().initialize()							 # Appelle l'initialisation de la classe mère.
		self.box = QComboBox(None)						 # Création de la boite.
		# self.box.setFixedWidth(150)					 # Réduire la largeur de la boite.
		self.box.addItems(self.items)					 # Ajout des choix possibles.
		self.box.currentIndexChanged.connect(self.emit)  # Ajout de la connexion lors d'un changement de selection
		self.set_value(self.default)					 # Définition de la valeur.
		self.add_row(self.box)							 # Ajoute la liste déroulante au calque.

	##################################################
	def reset(self): self.set_value(self.default)
