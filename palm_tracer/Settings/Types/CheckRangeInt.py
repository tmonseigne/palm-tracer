"""
Fichier contenant la classe :class:`CheckRangeInt` dérivée de :class:`.BaseSettingType`, qui permet la gestion d'un paramètre type interval de nombre entier.
"""

from dataclasses import dataclass, field
from typing import Any

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QSpinBox

from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType


##################################################
@dataclass
class CheckRangeInt(BaseSettingType):
	"""
	Classe pour un paramètre spécifique de type interval de nombre entier.

	Attributs :
			- **label (str)** : Nom du paramètre à afficher.
			- **_layout (QFormLayout)** : Le calque associé à ce paramètre, initialisé par défaut à un QFormLayout.
			- **default ([int, int])** : Valeurs par défaut du paramètre.
			- **limit ([int, int])** : Valeurs minimale et maximale du paramètre.
			- **value ([int, int])** : Valeurs minimale et maximale actuelles du paramètre.
			- **box ([QSpinBox, QSpinBox])** : Objet QT permettant de manipuler le paramètre.
	"""

	default: list[int] = field(default_factory=lambda: [0, 100])
	limit: list[int] = field(default_factory=lambda: [0, 100])
	value: list[int] = field(init=False, default_factory=lambda: [0, 100])
	_active: bool = field(init=False, default=False)
	_checkbox: QCheckBox = field(init=False)
	box: list[QSpinBox] = field(init=False, default_factory=lambda: [QSpinBox(), QSpinBox()])

	##################################################
	@property
	def active(self) -> bool:
		"""Permet la lecture de l'état actif."""
		return self._active

	##################################################
	@active.setter
	def active(self, value: bool):
		"""Contrôle la modification de l'état actif."""
		self._checkbox.setChecked(value)
		self.toggle_active(1 if value else 0)

	##################################################
	def get_value(self) -> list[int]:
		for i in range(2): self.value[i] = self.box[i].value()
		return self.value

	##################################################
	def set_value(self, value: list[int]):
		self.value = value
		for i in range(2): self.box[i].setValue(value[i])
		self.emit(value)

	##################################################
	def to_dict(self) -> dict[str, Any]:
		return {"type":    type(self).__name__, "active": self._active, "label": self.label,
				"default": self.default, "limit": self.limit, "value": self.value}

	##################################################
	def update_from_dict(self, data: dict[str, Any]):
		# Mise à jour des membres
		self.label = data.get("label", "")
		self.default = data.get("default", [0, 0])
		self.limit = data.get("limit", [0, 100])
		self.active = data.get("active", False)

		# Mise à jour des boites QT
		for i in range(2):
			self.box[i].setRange(self.limit[0], self.limit[1])
			self.set_value(data.get("value", self.default))

	##################################################
	def initialize(self):
		super().initialize()  # Appelle l'initialisation de la classe mère.

		# Check box
		self._checkbox = QCheckBox()
		self._checkbox.setChecked(self._active)
		self._checkbox.stateChanged.connect(self.toggle_active)

		# Spin box
		for i in range(2):
			self.box[i] = QSpinBox(None)									# Création de la boite.
			self.box[i].setAlignment(Qt.AlignmentFlag.AlignCenter)			# Définir l'alignement au centre.
			self.box[i].setFixedWidth(30)									# Réduit la largeur
			self.box[i].setRange(self.limit[0], self.limit[1])				# Définition du min, max.
			self.box[i].setValue(self.default[i])							# Définition de la valeur par défaut
			self.box[i].setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)  # Supprime les flèches

		self.box[0].valueChanged.connect(self.check_min)  # Définition du comportement lors de la modification des valeurs
		self.box[1].valueChanged.connect(self.check_max)  # Définition du comportement lors de la modification des valeurs

		# Ligne du paramètre
		hbox = QHBoxLayout()
		hbox.addWidget(self._checkbox)
		hbox.addWidget(QLabel(self.label + " : "))
		hbox.addWidget(self.box[0])
		hbox.addWidget(QLabel(" → "))
		hbox.addWidget(self.box[1])

		self._layout.addRow(hbox)

	##################################################
	def reset(self): self.set_value(self.default)

	##################################################
	def toggle_active(self, state: int):
		"""Met à jour l'état actif du groupe lorsque la checkbox est modifiée."""
		self._active = bool(state)

	##################################################
	def check_min(self, value: int):
		"""S'assure que min ≤ max."""
		self.value[0] = value
		if self.value[0] > self.value[1]:
			self.box[1].setValue(self.value[0])  # Ajuste max si min dépasse max

	##################################################
	def check_max(self, value: int):
		"""S'assure que min ≤ max."""
		self.value[1] = value
		if self.value[1] < self.value[0]:
			self.box[0].setValue(self.value[1])  # Ajuste min si max est trop bas
