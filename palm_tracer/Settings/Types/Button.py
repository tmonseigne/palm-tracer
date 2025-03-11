"""
Fichier contenant la classe :class:`Button` dérivée de :class:`.BaseSettingType`, qui permet la gestion d'un paramètre type boutton à cliquer.
"""

from dataclasses import dataclass, field
from typing import Any

from qtpy.QtCore import Qt
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

	text: str = "Button"
	box: QPushButton = field(init=False, default_factory=QPushButton)

	##################################################
	def get_value(self) -> bool: return True

	##################################################
	def set_value(self, value: str): pass

	##################################################
	def to_dict(self) -> dict[str, Any]:
		return {"type": type(self).__name__, "text": self.text}

	##################################################
	def update_from_dict(self, data: dict[str, Any]):
		self.label = data.get("label", "")
		self.text = data.get("text", "")
		self.box.setText(self.text)

	##################################################
	def initialize(self):
		super().initialize()			   # Appelle l'initialisation de la classe mère.
		self.box = QPushButton(self.text)  # Création de la boite.
		self.add_row(self.box)			   # Ajoute la check box au calque.

	##################################################
	def reset(self): pass

	##################################################
	def connect(self, f: Any): self.box.clicked.connect(f)
