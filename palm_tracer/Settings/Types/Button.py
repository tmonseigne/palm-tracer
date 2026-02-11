"""
Fichier contenant la classe :class:`Button` dérivée de :class:`.BaseSettingType`, qui permet la gestion d'un paramètre type bouton à cliquer.
"""

from dataclasses import dataclass, field
from typing import Any

from qtpy.QtWidgets import QPushButton

from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType


##################################################
@dataclass
class Button(BaseSettingType):
	"""
	Classe pour un paramètre spécifique de type bouton à cliquer.

	:param label: Nom du paramètre à afficher
	:param tooltip: Description détaillée en overlay.
	"""

	_box: QPushButton = field(init=False)

	# ==================================================
	# region Initialization
	# ==================================================
	##################################################
	def initialize(self):
		super().initialize()  # .			   Appelle l'initialisation de la classe mère.
		self._box = QPushButton(self.label)  # Création de la boite.
		self._layout.addWidget(self._box)  # . Ajout du champ de texte

	##################################################
	def reset(self): pass

	# ==================================================
	# endregion Initialization
	# ==================================================

	# ==================================================
	# region  Parsing
	# ==================================================
	##################################################
	def to_dict(self) -> dict[str, Any]:
		return {"type": type(self).__name__, "label": self.label}

	##################################################
	def update_from_dict(self, data: dict[str, Any]):
		self.label = data.get("label", "")
		self._box.setText(self.label)

	# ==================================================
	# endregion  Parsing
	# ==================================================

	# ==================================================
	# region  Callbacks
	# ==================================================
	##################################################
	def connect(self, f: Any): self._box.clicked.connect(f)
