"""
Fichier contenant la classe :class:`CheckRangeInt` dérivée de :class:`.BaseSettingType`, qui permet la gestion d'un paramètre type interval de nombre flottant.
"""

from dataclasses import dataclass, field
from typing import Any

from qtpy.QtWidgets import QCheckBox, QDoubleSpinBox, QLabel

from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType
from palm_tracer.Tools import Ui


##################################################
@dataclass
class CheckRangeFloat(BaseSettingType):
	"""
	Classe pour un paramètre spécifique de type interval de nombre flottant.

	:param label: Nom du paramètre à afficher
	:param tooltip: Description détaillée en overlay.
	:param default: Valeurs par défaut du paramètre.
	:param limits: Valeurs limites du paramètre.
	:param precision: Précision du paramètre.
	"""

	default: list[float] = field(default_factory=lambda: [-1, 1])
	_value: list[float] = field(init=False, default_factory=lambda: [-1, 1])

	limits: list[float] = field(default_factory=lambda: [-1, 1])
	"""Valeurs limites du paramètre."""
	precision: int = 2
	"""Précision du paramètre."""

	_active: bool = field(init=False, default=False)
	"""Indicateur d'activation du paramètre."""
	_checkbox: QCheckBox = field(init=False)
	"""CheckBox pour activer le paramètre."""
	_box: list[QDoubleSpinBox] = field(init=False, default_factory=lambda: [QDoubleSpinBox(), QDoubleSpinBox()])

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
			self._box[i] = Ui.make_spin(None, decimals=self.precision, minimum=self.limits[0], maximum=self.limits[1], value=self.default[i], buttons=False)
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
		"""Indicateur d'activation du paramètre (:class:`bool`)."""
		return self._active

	##################################################
	@active.setter
	def active(self, value: bool):
		"""Contrôle la modification de l'état actif."""
		self._checkbox.setChecked(value)
		self.toggle_active(1 if value else 0)

	##################################################
	@property
	def box(self) -> list[QDoubleSpinBox]:
		"""Objets QT permettant de manipuler le paramètre (liste de :class:`QDoubleSpinBox`)."""
		return self._box

	##################################################
	@property
	def value(self) -> list[float]:
		"""Valeurs actuelles du paramètre (:class:`list[float]`)."""
		for i in range(2): self._value[i] = self._box[i].value()
		return self._value

	##################################################
	@value.setter
	def value(self, value: list[float]):
		"""Valeurs actuelles du paramètre (:class:`list[float]`)."""
		self._value = value
		for i in range(2): self._box[i].setValue(value[i])

	# ==================================================
	# endregion Getter/Setter
	# ==================================================

	# ==================================================
	# region  Hide and Seek
	# ==================================================
	##################################################
	def hide(self):
		"""Cache le paramètre."""
		if self._form_layout is not None and self._row_index >= 0: self._form_layout.setRowVisible(self._row_index, False)
		else:  # fallback si pas attaché
			self._label_widget.hide()
			for b in self._box: b.hide()

	##################################################
	def show(self):
		"""Affiche le paramètre."""
		if self._form_layout is not None and self._row_index >= 0: self._form_layout.setRowVisible(self._row_index, True)
		else:  # fallback si pas attaché
			self._label_widget.show()
			for b in self._box: b.show()

	# ==================================================
	# endregion  Hide and Seek
	# ==================================================

	# ==================================================
	# region  Parsing
	# ==================================================
	##################################################
	def to_dict(self) -> dict[str, Any]:
		return {"type":    type(self).__name__, "active": self._active, "label": self.label,
				"default": self.default, "limit": self.limits, "value": self._value, "precision": self.precision}

	##################################################
	def update_from_dict(self, data: dict[str, Any]):
		# Mise à jour des membres
		self.label = data.get("label", "")
		self.default = data.get("default", [-1, 1])
		self.limits = data.get("limit", [-1, 1])
		self.precision = data.get("precision", 2)
		self.active = data.get("active", False)

		# Mise à jour des boites QT
		for i in range(2):
			self._box[i].setRange(self.limits[0], self.limits[1])
			self._box[i].setDecimals(self.precision)
			self.value = data.get("value", self.default)

	# ==================================================
	# endregion  Parsing
	# ==================================================

	# ==================================================
	# region  Callbacks
	# ==================================================
	##################################################
	def toggle_active(self, state: int):
		"""Mets à jour l'état actif du groupe lorsque la checkbox est modifiée."""
		self._active = bool(state)

	##################################################
	def check_min(self, value: float):
		"""S'assure que min ≤ max."""
		self._value[0] = value
		if self._value[0] > self._value[1]: self._box[1].setValue(self._value[0])  # Ajuste max si min dépasse max

	##################################################
	def check_max(self, value: float):
		"""S'assure que min ≤ max."""
		self._value[1] = value
		if self._value[1] < self._value[0]: self._box[0].setValue(self._value[1])  # Ajuste min si max est trop bas

	##################################################
	def update_limits(self, minimum: float | None = None, maximum: float | None = None):
		"""Mets à jour le max ."""
		for b in self._box: Ui.update_spin_limits(b, minimum, maximum)
