"""
Fichier contenant la classe :class:`CheckBox` dérivée de :class:`.BaseSettingType`, qui permet la gestion d'un paramètre type case à cocher.
"""

from dataclasses import dataclass, field
from typing import Any

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QCheckBox

from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType


##################################################
@dataclass
class CheckBox(BaseSettingType):
	"""
	Classe pour un paramètre spécifique de type case à cocher.

	:param label: Nom du paramètre à afficher
	:param tooltip: Description détaillée en overlay.
	:param default: Valeur par défaut du paramètre.
	"""

	default: bool = False
	_value: bool = field(init=False, default=False)
	_box: QCheckBox = field(init=False, default_factory=lambda: QCheckBox())

	# ==================================================
	# region Initialization
	# ==================================================
	##################################################
	def initialize(self):
		super().initialize()  # .					 Appelle l'initialisation de la classe mère.
		self.value = self.default  # .				 Définition de la valeur.
		self._box.stateChanged.connect(self.emit)  # Ajout de la connexion lors d'un changement
		self._layout.addWidget(self._box)  # .		 Ajout du champ de texte
		self._layout.addStretch(1)  # .				 Pousse tout à gauche, espace vide à droite

	# ==================================================
	# endregion Initialization
	# ==================================================

	# ==================================================
	# region Getter/Setter
	# ==================================================
	##################################################
	@property
	def value(self) -> bool:
		"""Valeur actuelle du paramètre (:class:`bool`)."""
		if self._box.checkState() == Qt.CheckState.Unchecked: self._value = False
		else: self._value = True
		return self._value

	##################################################
	@value.setter
	def value(self, value: bool):
		"""Valeur actuelle du paramètre (:class:`bool`)."""
		self._value = value
		if value: self._box.setCheckState(Qt.CheckState.Checked)
		else:     self._box.setCheckState(Qt.CheckState.Unchecked)

	# ==================================================
	# endregion Getter/Setter
	# ==================================================

	# ==================================================
	# region  Parsing
	# ==================================================
	##################################################
	def to_dict(self) -> dict[str, Any]:
		return {"type": type(self).__name__, "label": self.label, "default": self.default, "value": self._value}

	##################################################
	def update_from_dict(self, data: dict[str, Any]):
		self.label = data.get("label", "")
		self.default = data.get("default", False)
		self.value = data.get("value", False)
