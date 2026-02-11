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

	:param label: Nom du paramètre à afficher
	:param tooltip: Description détaillée en overlay.
	:param default: Valeurs par défaut du paramètre.
	:param items: Choix de la liste déroulante.
	"""

	default: int = 0
	_value: int = field(init=False, default=0)
	items: list[str] = field(default_factory=lambda: [""])
	"""Choix de la liste déroulante (:class:`list[str]`)."""

	_box: QComboBox = field(init=False, default_factory=lambda: QComboBox())

	# ==================================================
	# region Initialization
	# ==================================================
	##################################################
	def initialize(self):
		super().initialize()  # .							Appelle l'initialisation de la classe mère.
		self._box.addItems(self.items)  # .					Ajout des choix possibles.
		self._box.currentIndexChanged.connect(self.emit)  # Ajout de la connexion lors d'un changement
		self.value = self.default  # .						Définition de la valeur.
		self._layout.addWidget(self._box)  # .				Ajout du champ de texte
		self._layout.addStretch(1)  # .						Pousse tout à gauche, espace vide à droite

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
		self._value = value
		self._box.setCurrentIndex(value)

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
		# Mise à jour des membres
		self.label = data.get("label", "")
		self.default = data.get("default", False)
		self.update_box(data.get("items", [""]))
		self.value = data.get("value", self.default)

	# ==================================================
	# endregion  Parsing
	# ==================================================

	# ==================================================
	# region  Callbacks
	# ==================================================
	##################################################
	def update_box(self, items: Optional[list[str]] = None):
		"""Met à jour la ComboBox pour refléter la liste actuelle des options."""
		with self.signal_blocked():
			self._box.clear()
			if items is not None: self.items = items
			self._box.addItems(self.items)
