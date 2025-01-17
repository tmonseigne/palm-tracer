"""
Fichier contenant la classe `BaseSettingGroup` et ses sous-classes pour la gestion des groupes de paramètres.

Ce module définit la classe abstraite `BaseSettingGroup`, qui sert de base pour la création de différents groupes de paramètres.
"""

from dataclasses import dataclass, field
from typing import Any, Union

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QCheckBox, QFormLayout, QLabel, QWidget

from palm_tracer.Settings.Types import BaseSettingType


##################################################
@dataclass
class BaseSettingGroup:
	"""
	Classe mère pour un groupe de setting :

	Attributs :
			- **active (bool)** : État du groupe (activé ou non)
			- **label (str)** : Nom du Groupe
			- **setting_list (dict[str, list[Union[BaseSettingGroup, BaseSettingType, Any]]]()** : Liste des settings du groupe.
			- **_settings (dict[str, Union[BaseSettingGroup, BaseSettingType]])** : Liste des visualisations de settings (inputs) du groupe.
			- **_layout (QFormLayout)** : Layout principal du groupe.
			- **_title (QLabel)** : Nom du Groupe (objet QT).
			- **_checkbox (QCheckBox)** : Case à cocher pour activer ou non le groupe.
			- **_header (QFormLayout)** : Titre du groupe.
			- **_body (QWidget)** : Corps du groupe (encapsulé dans un QWidget pour avoir un Hide/Show disponible).
	"""

	_active: bool = field(init=False, default=False)
	label: str = field(init=False, default="Base Setting Group")
	setting_list = dict[str, list[Union["BaseSettingGroup", BaseSettingType, Any]]]()
	_settings: dict[str, Union["BaseSettingGroup", BaseSettingType]] = field(init=False)
	_layout: QFormLayout = field(init=False)
	_title: QLabel = field(init=False)
	_checkbox: QCheckBox = field(init=False)
	_header: QFormLayout = field(init=False)
	_body: QWidget = field(init=False)

	# ==================================================
	# region Initialization
	# ==================================================
	##################################################
	def __post_init__(self):
		"""Méthode appelée automatiquement après l'initialisation du dataclass."""
		self.initialize()
		self.initialize_ui()

	##################################################
	def initialize(self):
		"""Initialise le dictionnaire de paramètres."""
		self._settings = dict[str, Union["BaseSettingGroup", BaseSettingType]]()
		for key, value in self.setting_list.items():
			self._settings[key] = value[0](*value[1])

	##################################################
	def initialize_ui(self):
		"""Initialise l'interface utilisateur."""
		# Base
		self._layout = QFormLayout(None)
		self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # Définir l'alignement du calque en haut.

		# Title Row
		self._title = QLabel(f"{self.label}")
		self._title.setStyleSheet("font-weight: bold;")  # Style pour le label de titre
		self._checkbox = QCheckBox()
		self._checkbox.stateChanged.connect(self.toggle_active)

		self._header = QFormLayout(None)
		self._header.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Définir l'alignement du calque à gauche.
		self._header.addRow(self._checkbox, self._title)
		self._layout.addRow(self._header)

		# Settings part (must be managed by the derived class.)
		self._body = QWidget()
		body = QFormLayout(self._body)
		body.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Définir l'alignement du calque à gauche.
		body.setContentsMargins(20, 0, 0, 0)  # Léger décalage.
		for key, setting in self._settings.items():
			body.addRow(setting.layout)
		self._layout.addRow(self._body)

		# Active ou non le groupe
		self.active = self._active

	##################################################
	def reset(self):
		"""Remet les valeurs par défaut des paramètres."""
		for _, setting in self._settings.items():
			setting.reset()

	# ==================================================
	# endregion Initialization
	# ==================================================

	# ==================================================
	# region Getter/Setter
	# ==================================================
	##################################################
	@property
	def layout(self) -> QFormLayout:
		"""Retourne le calque associé à ce groupe de paramètres."""
		return self._layout

	##################################################
	@property
	def active(self) -> bool:
		"""Permet la lecture de l'état actif."""
		return self._active

	##################################################
	@active.setter
	def active(self, value: bool):
		"""Contrôle la modification de l'état actif."""
		if self._active != value:
			self._checkbox.setChecked(value)
			self.toggle_active(1 if value else 0)

	##################################################
	def get_setting_names(self) -> list[str]:
		"""Récupère le nom des paramètres de ce groupe."""
		return list(self._settings.keys())

	##################################################
	def __getitem__(self, key: str) -> Union["BaseSettingGroup", BaseSettingType]:
		"""Surcharge de l'opérateur []"""
		return self._settings[key]

	##################################################
	# def __setitem__(self, key: str, value: Union["BaseSettingGroup", BaseSettingType]):
	# 	"""Surcharge pour assigner une valeur avec []"""
	# 	self._settings[key] = value

	##################################################
	def __contains__(self, key: str) -> bool:
		"""Surcharge pour vérifier si une clé existe"""
		return key in self._settings

	##################################################
	def __iter__(self):
		"""Surcharge pour obtenir l'itérable des clés"""
		return iter(self._settings)

	##################################################
	def get_value(self): return

	##################################################
	def set_value(self, value: Any): return

	##################################################
	def toggle_active(self, state: int):
		"""Met à jour l'état actif du groupe lorsque la checkbox est modifiée."""
		self._active = bool(state)
		self._body.show() if self._active else self._body.hide()

	##################################################
	def always_active(self):
		""" Active toujours le groupe et supprime la checkbox de l'interface. """
		# Appeler la méthode active pour forcer l'état actif
		self.active = True
		# Supprimer la checkbox et réorganiser le layout
		if self._checkbox:
			self._header.layout().removeWidget(self._checkbox)  # Retirer la checkbox du layout
			self._checkbox.deleteLater()  # Détruire la checkbox
			# Ajouter des espaces au nom du groupe pour conserver à minima l'alignement, oui et non à voir.
			# self._title.setText(f"       {self.label}")


	# ==================================================
	# endregion Getter/Setter
	# ==================================================

	# ==================================================
	# region IO
	# ==================================================
	##################################################
	def to_dict(self) -> dict[str, Any]:
		"""Renvoie un dictionnaire contenant toutes les informations de la classe."""
		return {"type":     type(self).__name__, "active": self._active, "label": self.label,
				"settings": {name: setting.to_dict() for name, setting in self._settings.items()}, }

	##################################################
	@classmethod
	def from_dict(cls, data: dict[str, Any]) -> "BaseSettingGroup":
		"""Créé une instance de la classe à partir d'un dictionnaire."""
		res = cls()  # Instancie la classe appelée
		res.update_from_dict(data)
		return res

	##################################################
	def update_from_dict(self, data: dict[str, Any]):
		""" Met à jour la classe à partir d'un dictionnaire."""
		self.label = data.get("label", self.label)
		self.active = data.get("active", False)
		settings = data["settings"]
		for key, value in self.setting_list.items():  # Appelle `update_from_dict` pour chaque élément de setting_list
			if key in settings: self._settings[key].update_from_dict(settings[key])

	##################################################
	def tostring(self, line_prefix: str = "") -> str:
		"""
		Retourne une chaîne de caractères correspondant à la liste des settings.

		:param line_prefix: Préfixe de chaque ligne (par exemple pour ajouter une indentation)
		:return: Une description textuelle des paramètres.
		"""
		msg = f"{line_prefix}- Activate : {self.active}\n"
		for key, setting in self._settings.items():
			if isinstance(setting, BaseSettingGroup):
				msg += f"{line_prefix}- {key} :\n{setting.tostring(f"{line_prefix}  ")}"
			else: msg += f"{line_prefix}- {key} : {setting.get_value()}\n"
		return msg

	##################################################
	def __str__(self) -> str: return self.tostring()

	# ==================================================
	# endregion IO
	# ==================================================
