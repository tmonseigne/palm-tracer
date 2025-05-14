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

	Attributs :
			- **label (str)** : Nom du paramètre à afficher.
			- **_layout (QFormLayout)** : Le calque associé à ce paramètre, initialisé par défaut à un QFormLayout.
			- **_signal (SignalWrapper)** : Signal permettant de communiquer avec l'interface.
			- **default (bool)** : Valeur par défaut du paramètre.
			- **value (bool)** : Valeur actuelle du paramètre.
			- **box (QSpinBox)** : Objet QT permettant de manipuler le paramètre.
	"""

	default: bool = False
	"""Valeur par défaut du paramètre."""
	value: bool = field(init=False, default=False)
	"""Valeur actuelle du paramètre."""
	box: QCheckBox = field(init=False, default_factory=QCheckBox)
	"""Objet QT permettant de manipuler le paramètre."""

	##################################################
	def get_value(self) -> bool:
		if self.box.checkState() == Qt.CheckState.Unchecked: self.value = False
		else: self.value = True
		return self.value

	##################################################
	def set_value(self, value: bool):
		self.value = value
		if value: self.box.setCheckState(Qt.CheckState.Checked)
		else:     self.box.setCheckState(Qt.CheckState.Unchecked)

	##################################################
	def to_dict(self) -> dict[str, Any]:
		return {"type": type(self).__name__, "label": self.label, "default": self.default, "value": self.value}

	##################################################
	def update_from_dict(self, data: dict[str, Any]):
		self.label = data.get("label", "")
		self.default = data.get("default", False)
		self.set_value(data.get("value", False))

	##################################################
	def initialize(self):
		super().initialize()		  # Appelle l'initialisation de la classe mère.
		self.box = QCheckBox()		  # Création de la boite.
		self.set_value(self.default)  # Définition de la valeur.
		self.box.stateChanged.connect(self.emit)  # Ajout de la connexion lors d'un changement
		self.add_row(self.box)		  # Ajoute la check box au calque.

	##################################################
	def reset(self): self.set_value(self.default)
