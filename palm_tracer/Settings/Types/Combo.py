"""
Fichier contenant la classe `Combo` dérivée de `BaseSettingType`, qui permet la gestion d'un paramètre type liste déroulante.
"""

from dataclasses import dataclass, field
from typing import Any

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
			- **default (int)** : Valeur par défaut du paramètre.
			- **items (list[str])** : Choix de la liste déroulante.
			- **value (int)** : Valeur actuelle du paramètre.
			- **box (QComboBox)** : Objet QT permettant de manipuler le paramètre.
	"""

	default: int = 0
	items: list[str] = field(default_factory=lambda: [""])
	value: int = field(init=False, default=0)
	box: QComboBox = field(init=False)

	##################################################
	def get_value(self) -> int:
		self.value = self.box.currentIndex()
		return self.value

	##################################################
	def set_value(self, value: int):
		self.value = value
		self.box.setCurrentIndex(value)

	##################################################
	def to_dict(self) -> dict[str, Any]:
		return {"type": type(self).__name__, "label": self.label, "default": self.default, "items": self.items, "value": self.value}

	##################################################
	def update_from_dict(self, data: dict[str, Any]):
		# Mise à jour des membres
		self.label = data.get("label", "")
		self.default = data.get("default", False)
		self.items = data.get("items", [""])
		# Mise à jour de la boite QT
		self.box.clear()
		self.box.addItems(self.items)
		self.set_value(data.get("value", self.default))

	##################################################
	def initialize(self):
		super().initialize()			# Appelle l'initialisation de la classe mère.
		self.box = QComboBox(None)		# Création de la boite.
		# self.box.setFixedWidth(150)	# Réduire la largeur de la boite.
		self.box.addItems(self.items)   # Ajout des choix possibles.
		self.set_value(self.default)    # Définition de la valeur.
		self.add_row(self.box)			# Ajoute la liste déroulante au calque.

	##################################################
	def reset(self): self.set_value(0)
