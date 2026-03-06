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

	:param label: Nom du paramètre à afficher
	:param tooltip: Description détaillée en overlay.
	:param default: Valeur par défaut du paramètre.
	:param limits: Valeurs limites du paramètre.
	:param step: Pas à chaque appui sur une des flèches du paramètre.
	"""

	default: int = 0
	_value: int = field(init=False, default=0)

	limits: list[int] = field(default_factory=lambda: [0, 100])
	"""Valeurs limites du paramètre."""
	step: int = 1
	"""Pas à chaque appui sur une des flèches du paramètre."""

	_box: QSpinBox = field(init=False)

	# ==================================================
	# region Initialization
	# ==================================================
	##################################################
	def initialize(self):
		super().initialize()  # .					 Appelle l'initialisation de la classe mère.
		self._box = Ui.make_spin(None, minimum=self.limits[0], maximum=self.limits[1], step=self.step, value=self.default)
		self._box.setKeyboardTracking(False)  # .	 Empèche la mise à jour à chaque appuie clavier (attend la fin de l'édition)
		self._box.valueChanged.connect(self.emit)  # Définition du comportement lors de la modification des valeurs
		self._layout.addWidget(self._box)  # .		 Ajout du champ de texte.
		self._layout.addStretch(1)  # .				 Pousse tout à gauche, espace vide à droite.

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
		self._value = self._box.value()
		return self._value

	##################################################
	@value.setter
	def value(self, value: int):
		"""Valeur actuelle du paramètre (:class:`int`)."""
		self._value = value
		self._box.setValue(value)

	# ==================================================
	# endregion Getter/Setter
	# ==================================================

	# ==================================================
	# region  Parsing
	# ==================================================
	##################################################
	def to_dict(self) -> dict[str, Any]:
		return {"type": type(self).__name__, "label": self.label, "default": self.default, "limits": self.limits,
				"step": self.step, "value": self._value}

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
		self.value = data.get("value", self.default)
