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
		- **label** (:class:`str`) : Nom du paramètre à afficher.
		- **_layout** (:class:`QFormLayout`) : Le calque associé à ce paramètre, initialisé par défaut à un :class:`QFormLayout`.
		- **_signal** (:class:`SignalWrapper`) : Signal permettant de communiquer avec l'interface.
		- **default** (:class:`bool`) : Valeur par défaut du paramètre.
		- **value** (:class:`bool`) : Valeur actuelle du paramètre.
		- **box** (:class:`QSpinBox`) : Objet QT permettant de manipuler le paramètre.
	"""

	default: bool = False
	value: bool = field(init=False, default=False)
	_box: QCheckBox = field(init=False)

	# ==================================================
	# region Initialization
	# ==================================================
	##################################################
	def initialize(self):
		super().initialize()  # .					 Appelle l'initialisation de la classe mère.
		self._box = QCheckBox()  # .				 Création de la boite.
		self.set_value(self.default)  # .			 Définition de la valeur.
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
	def get_value(self) -> bool:
		if self._box.checkState() == Qt.CheckState.Unchecked: self.value = False
		else: self.value = True
		return self.value

	##################################################
	def set_value(self, value: bool):
		self.value = value
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
		return {"type": type(self).__name__, "label": self.label, "default": self.default, "value": self.value}

	##################################################
	def update_from_dict(self, data: dict[str, Any]):
		self.label = data.get("label", "")
		self.default = data.get("default", False)
		self.set_value(data.get("value", False))
