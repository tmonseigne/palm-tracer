"""
Fichier contenant la classe `SpinInt` dérivée de `BaseSettingType`, qui permet la gestion d'un paramètre type nombre entier.
"""

from dataclasses import dataclass, field
from typing import Any

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QSpinBox

from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType


##################################################
@dataclass
class SpinInt(BaseSettingType):
	"""
	Classe pour un paramètre spécifique de type nombre entier.

	Attributs :
			- **label (str)** : Nom du paramètre à afficher.
			- **_layout (QFormLayout)** : Le calque associé à ce paramètre, initialisé par défaut à un QFormLayout.
			- **default (int)** : Valeur par défaut du paramètre.
			- **min (int)** : Valeur minimale du paramètre.
			- **max (int)** : Valeur maximale du paramètre.
			- **step (int)** : Pas à chaque appuie sur une des flèches du paramètre.
			- **value (int)** : Valeur actuelle du paramètre.
			- **box (QSpinBox)** : Objet QT permettant de manipuler le paramètre.
	"""

	default: int = 0
	min: int = 0
	max: int = 100
	step: int = 1
	value: int = field(init=False, default=0)
	box: QSpinBox = field(init=False)

	##################################################
	def get_value(self) -> int:
		self.value = self.box.value()
		return self.value

	##################################################
	def set_value(self, value: int):
		self.value = value
		self.box.setValue(value)

	##################################################
	def to_dict(self) -> dict[str, Any]:
		return {"type": type(self).__name__, "label": self.label, "default": self.default,
				"min":  self.min, "max": self.max, "step": self.step, "value": self.value}

	##################################################
	def update_from_dict(self, data: dict[str, Any]):
		# Mise à jour des membres
		self.label = data.get("label", "")
		self.default = data.get("default", False)
		self.min = data.get("min", 0)
		self.max = data.get("max", 100)
		self.step = data.get("step", 1)
		# Mise à jour de la boite QT
		self.box.setRange(self.min, self.max)
		self.box.setSingleStep(self.step)
		self.set_value(data.get("value", self.default))

	##################################################
	def initialize(self):
		super().initialize()								# Appelle l'initialisation de la classe mère.
		self.box = QSpinBox(None)							# Création de la boite.
		self.box.setAlignment(Qt.AlignmentFlag.AlignLeft)   # Définir l'alignement du calque à gauche.
		self.box.setRange(self.min, self.max)				# Définition du min, max.
		self.box.setSingleStep(self.step)					# Définition du pas à chaque appuie sur une flèche.
		self.set_value(self.default)						# Définition de la valeur.
		self.add_row(self.box)								# Ajoute le spin au calque.

	##################################################
	def reset(self): self.set_value(self.default)
