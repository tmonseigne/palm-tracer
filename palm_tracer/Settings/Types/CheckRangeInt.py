"""
Fichier contenant la classe :class:`CheckRangeInt` dérivée de :class:`.BaseSettingType`, qui permet la gestion d'un paramètre type interval de nombre entier.
"""

from dataclasses import dataclass, field
from typing import Any

from qtpy.QtWidgets import QCheckBox, QLabel, QSpinBox

from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType
from palm_tracer.Tools import Ui


##################################################
@dataclass
class CheckRangeInt(BaseSettingType):
	"""
	Classe pour un paramètre spécifique de type interval de nombre entier.

	Attributs :
		- **label** (:class:`str`) : Nom du paramètre à afficher.
		- **_layout** (:class:`QFormLayout`) : Le calque associé à ce paramètre, initialisé par défaut à un :class:`QFormLayout`.
		- **_signal** (:class:`SignalWrapper`) : Signal permettant de communiquer avec l'interface.
		- **default** (:class:`[int, int]`) : Valeurs par défaut du paramètre.
		- **limit** (:class:`[int, int]`) : Valeurs minimale et maximale du paramètre.
		- **value** (:class:`[int, int]`) : Valeurs minimale et maximale actuelles du paramètre.
		- **_active** (:class:`bool`) : Indicateur d'activation du paramètre.
		- **_checkbox** (:class:`QCheckBox`) : CheckBox pour activer le paramètre.
		- **box** (:class:`[QSpinBox, QSpinBox]`) : Objet QT permettant de manipuler le paramètre.
	"""

	default: list[int] = field(default_factory=lambda: [0, 100])
	value: list[int] = field(init=False, default_factory=lambda: [0, 100])
	limits: list[int] = field(default_factory=lambda: [0, 100])
	"""Valeur limite du paramètre."""

	_active: bool = field(init=False, default=False)
	"""Indicateur d'activation du paramètre."""
	_checkbox: QCheckBox = field(init=False)
	"""CheckBox pour activer le paramètre."""
	_box: list[QSpinBox] = field(init=False, default_factory=lambda: [QSpinBox(), QSpinBox()])

	# ==================================================
	# region Initialization
	# ==================================================
	##################################################
	def initialize(self):
		super().initialize()  # Appelle l'initialisation de la classe mère.

		# Check box
		self._checkbox = QCheckBox()
		self._checkbox.setChecked(self._active)
		self._checkbox.stateChanged.connect(self.toggle_active)
		self._checkbox.stateChanged.connect(self.emit)  # Ajout de la connexion lors d'un changement

		# Spin box
		for i in range(2):
			# Création de la boite.
			self._box[i] = Ui.make_spin(None, minimum=self.limits[0], maximum=self.limits[1], value=self.default[i], buttons=False)
			self._box[i].valueChanged.connect(self.emit)  # Définition du comportement lors de la modification des valeurs

		self._box[0].valueChanged.connect(self.check_min)  # Définition du comportement lors de la modification des valeurs
		self._box[1].valueChanged.connect(self.check_max)  # Définition du comportement lors de la modification des valeurs

		# Ligne du paramètre
		self._layout.addWidget(self._checkbox)
		self._layout.addWidget(self._box[0])
		self._layout.addWidget(QLabel("→"))
		self._layout.addWidget(self._box[1])
		self._layout.addStretch(1)  # pousse tout à gauche, espace vide à droite

	# ==================================================
	# endregion Initialization
	# ==================================================

	# ==================================================
	# region Getter/Setter
	# ==================================================
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
	@property
	def box(self) -> list[QSpinBox]:
		"""
		Retourne l'objet QT principal associé à ce paramètre.

		:return: Le :class:`QWidget` associé à ce paramètre.
		"""
		return self._box

	##################################################
	def get_value(self) -> list[int]:
		for i in range(2): self.value[i] = self._box[i].value()
		return self.value

	##################################################
	def set_value(self, value: list[int]):
		self.value = value
		for i in range(2): self._box[i].setValue(value[i])

	# ==================================================
	# endregion Getter/Setter
	# ==================================================

	# ==================================================
	# region  Hide and Seek
	# ==================================================
	##################################################
	def hide(self):
		"""Cache les widgets."""
		for b in self._box: b.hide()

	##################################################
	def show(self):
		"""Affiche les widgets."""
		for b in self._box: b.show()

	# ==================================================
	# endregion  Hide and Seek
	# ==================================================

	# ==================================================
	# region Parsing
	# ==================================================
	##################################################
	def to_dict(self) -> dict[str, Any]:
		return {"type":    type(self).__name__, "active": self._active, "label": self.label,
				"default": self.default, "limit": self.limits, "value": self.value}

	##################################################
	def update_from_dict(self, data: dict[str, Any]):
		# Mise à jour des membres
		self.label = data.get("label", "")
		self.default = data.get("default", [0, 0])
		self.limits = data.get("limit", [0, 100])
		self.active = data.get("active", False)

		# Mise à jour des boites QT
		for i in range(2):
			self._box[i].setRange(self.limits[0], self.limits[1])
			self.set_value(data.get("value", self.default))

	# ==================================================
	# endregion Parsing
	# ==================================================

	# ==================================================
	# region  Callbacks
	# ==================================================
	##################################################
	def toggle_active(self, state: int):
		"""Met à jour l'état actif du groupe lorsque la checkbox est modifiée."""
		self._active = bool(state)

	##################################################
	def check_min(self, value: int):
		"""S'assure que min ≤ max."""
		self.value[0] = value
		if self.value[0] > self.value[1]:
			self._box[1].setValue(self.value[0])  # Ajuste max si min dépasse max

	##################################################
	def check_max(self, value: int):
		"""S'assure que min ≤ max."""
		self.value[1] = value
		if self.value[1] < self.value[0]:
			self._box[0].setValue(self.value[1])  # Ajuste min si max est trop bas
