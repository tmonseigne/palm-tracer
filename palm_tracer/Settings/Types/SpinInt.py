"""
Fichier contenant la classe :class:`SpinInt` dérivée de :class:`.BaseSettingType`, qui permet la gestion d'un paramètre type nombre entier.
"""

from dataclasses import dataclass, field
from typing import Any

from qtpy.QtWidgets import QSpinBox

from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType
from palm_tracer.Tools import Ui


##################################################
@dataclass
class SpinInt(BaseSettingType):
	"""
	Classe pour un paramètre spécifique de type nombre entier.

	Attributs :
		- **label** (:class:`str`) : Nom du paramètre à afficher.
		- **default** (:class:`int`) : Valeur par défaut du paramètre.
		- **limits** (:class:`int`) : Valeurs limites du paramètre.
		- **step** (:class:`int`) : Pas à chaque appuie sur une des flèches du paramètre.
		- **value** (:class:`int`) : Valeur actuelle du paramètre.
		- **box** (:class:`QSpinBox`) : Objet QT permettant de manipuler le paramètre.
		- **_layout** (:class:`QFormLayout`) : Le calque associé à ce paramètre, initialisé par défaut à un :class:`QFormLayout`.
		- **_signal** (:class:`SignalWrapper`) : Signal permettant de communiquer avec l'interface.
	"""

	default: int = 0
	value: int = field(init=False, default=0)

	limits: list[int] = field(default_factory=lambda: [0, 100])
	"""Valeurs limites du paramètre."""
	step: int = 1
	"""Pas à chaque appuie sur une des flèches du paramètre."""

	_box: QSpinBox = field(init=False)

	# ==================================================
	# region Initialization
	# ==================================================
	##################################################
	def initialize(self):
		super().initialize()  # .					 Appelle l'initialisation de la classe mère.
		self._box = Ui.make_spin(None, minimum=self.limits[0], maximum=self.limits[1], step=self.step, value=self.default)
		self._box.valueChanged.connect(self.emit)  # Définition du comportement lors de la modification des valeurs
		self.set_value(self.default)  # .			 Définition de la valeur.
		self._layout.addWidget(self._box)  # .		 Ajout du champ de texte.
		self._layout.addStretch(1)  # .				 Pousse tout à gauche, espace vide à droite.

	# ==================================================
	# endregion Initialization
	# ==================================================

	# ==================================================
	# region Getter/Setter
	# ==================================================
	##################################################
	def get_value(self) -> int:
		self.value = self._box.value()
		return self.value

	##################################################
	def set_value(self, value: int):
		self.value = value
		self._box.setValue(value)

	# ==================================================
	# endregion Getter/Setter
	# ==================================================

	# ==================================================
	# region  Parsing
	# ==================================================
	##################################################
	def to_dict(self) -> dict[str, Any]:
		return {"type":   type(self).__name__, "label": self.label, "default": self.default,
				"limits": self.limits, "step": self.step, "value": self.value}

	##################################################
	def update_from_dict(self, data: dict[str, Any]):
		# Mise à jour des membres
		self.label = data.get("label", "")
		self.default = data.get("default", False)
		self.limits = data.get("limits", [0, 100])
		self.step = data.get("step", 1)
		# Mise à jour de la boite QT
		self._box.setRange(self.limits[0], self.limits[1])
		self._box.setSingleStep(self.step)
		self.set_value(data.get("value", self.default))
