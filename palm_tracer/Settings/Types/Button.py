"""
Fichier contenant la classe :class:`Button` dérivée de :class:`.BaseSettingType`, qui permet la gestion d'un paramètre type boutton à cliquer.
"""

from dataclasses import dataclass, field
from typing import Any

from qtpy.QtWidgets import QPushButton

from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType


##################################################
@dataclass
class Button(BaseSettingType):
	"""
	Classe pour un paramètre spécifique de type case à cocher.

	Attributs :
			- **label (str)** : Nom du paramètre à afficher.
			- **_layout (QFormLayout)** : Le calque associé à ce paramètre, initialisé par défaut à un QFormLayout.
			- **value (bool)** : Valeur actuelle du paramètre.
			- **box (QSpinBox)** : Objet QT permettant de manipuler le paramètre.
	"""

	box: QPushButton = field(init=False, default_factory=QPushButton)

	##################################################
	def get_value(self) -> bool: return True

	##################################################
	def set_value(self, value: str): pass

	##################################################
	def to_dict(self) -> dict[str, Any]:
		return {"type": type(self).__name__, "label": self.label}

	##################################################
	def update_from_dict(self, data: dict[str, Any]):
		self.label = data.get("label", "")
		self.box.setText(self.label)

	##################################################
	def initialize(self):
		super().initialize()			   # Appelle l'initialisation de la classe mère.
		self.box = QPushButton(self.label)  # Création de la boite.
		self._layout.addRow(self.box)

	##################################################
	def reset(self): pass

	##################################################
	def connect(self, f: Any): self.box.clicked.connect(f)
