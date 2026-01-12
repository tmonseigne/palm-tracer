"""
Fichier contenant la classe :class:`SpinFloat` dérivée de :class:`.BaseSettingType`, qui permet la gestion d'un paramètre type nombre réel.
"""

from dataclasses import dataclass, field
from typing import Any

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QDoubleSpinBox

from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType


##################################################
@dataclass
class SpinFloat(BaseSettingType):
	"""
	Classe pour un paramètre spécifique de type nombre réel.

	Attributs :
		- **label** (:class:`str`) : Nom du paramètre à afficher.
		- **_layout** (:class:`QFormLayout`) : Le calque associé à ce paramètre, initialisé par défaut à un :class:`QFormLayout`.
		- **_signal** (:class:`SignalWrapper`) : Signal permettant de communiquer avec l'interface.
		- **default** (:class:`float`) : Valeur par défaut du paramètre.
		- **min** (:class:`float`) : Valeur minimale du paramètre.
		- **max** (:class:`float`) : Valeur maximale du paramètre.
		- **step** (:class:`float`) : Pas à chaque appuie sur une des flèches du paramètre.
		- **precision** (:class:`int`) : Précision du paramètre.
		- **value** (:class:`float`) : Valeur actuelle du paramètre.
		- **box** (:class:`QDoubleSpinBox`) : Objet QT permettant de manipuler le paramètre.
	"""
	default: float = 0.0
	"""Valeur par défaut du paramètre."""
	min: float = 0.0
	"""Valeur minimale du paramètre."""
	max: float = 100.0
	"""Valeur maximale du paramètre."""
	step: float = 1.0
	"""Pas à chaque appuie sur une des flèches du paramètre."""
	precision: int = 2
	"""Precision du paramètre."""
	value: float = field(init=False, default=0.0)
	"""Valeur actuelle du paramètre."""
	box: QDoubleSpinBox = field(init=False)
	"""Objet QT permettant de manipuler le paramètre."""

	##################################################
	def get_value(self) -> float:
		self.value = self.box.value()
		return self.value

	##################################################
	def set_value(self, value: float):
		self.value = value
		self.box.setValue(value)

	##################################################
	def to_dict(self) -> dict[str, Any]:
		return {"type":  type(self).__name__, "label": self.label, "default": self.default,
				"min":   self.min, "max": self.max, "step": self.step, "precision": self.precision,
				"value": self.value}

	##################################################
	def update_from_dict(self, data: dict[str, Any]):
		# Mise à jour des membres
		self.label = data.get("label", "")
		self.default = data.get("default", False)
		self.min = data.get("min", 0.0)
		self.max = data.get("max", 100.0)
		self.step = data.get("step", 1.0)
		self.precision = data.get("precision", 2)
		# Mise à jour de la boite QT
		self.box.setRange(self.min, self.max)
		self.box.setSingleStep(self.step)
		self.box.setDecimals(self.precision)
		self.set_value(data.get("value", self.default))

	##################################################
	def initialize(self):
		super().initialize()							   # Appelle l'initialisation de la classe mère.
		self.box = QDoubleSpinBox(None)					   # Création de la boite.
		self.box.setRange(self.min, self.max)			   # Définition du min, max.
		self.box.setSingleStep(self.step)				   # Définition du pas à chaque appuie sur une flèche.
		self.box.setDecimals(self.precision)			   # Définition de la précision à afficher.
		self.box.valueChanged.connect(self.emit)		   # Définition du comportement lors de la modification des valeurs
		self.set_value(self.default)					   # Définition de la valeur.
		self.add_row(self.box)							   # Ajoute le spin au calque.

	##################################################
	def reset(self): self.set_value(self.default)
