"""
Fichier contenant la classe :class:`BaseSettingGroup` et ses sous-classes pour la gestion des groupes de paramètres.

Ce module définit la classe abstraite :class:`.BaseSettingGroup`, qui sert de base pour la création de différents groupes de paramètres.
"""

from dataclasses import dataclass, field
from typing import Any, cast, Union

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
			- **_widget (QWidget)** : Widget principal du groupe.
			- **_title (QLabel)** : Nom du Groupe (objet QT).
			- **_checkbox (QCheckBox)** : Case à cocher pour activer ou non le groupe.
			- **_header (QFormLayout)** : Titre du groupe.
			- **_body (QWidget)** : Corps du groupe (encapsulé dans un QWidget pour avoir un Hide/Show disponible).
	"""

	_active: bool = field(init=False, default=False)
	"""État du groupe (activé ou non)"""
	label: str = field(init=False, default="Base Setting Group")
	"""Nom du Groupe."""
	setting_list = dict[str, list[Union["BaseSettingGroup", BaseSettingType, Any]]]()
	"""Liste des settings du groupe."""
	_inner_groups = list[str]()
	"""Liste des sous-groupes de settings du groupe."""
	_settings: dict[str, Union["BaseSettingGroup", BaseSettingType]] = field(init=False)
	"""Liste des visualisations de settings (inputs) du groupe."""
	_widget: QWidget = field(init=False)
	"""Widget principal du groupe."""
	_title: QLabel = field(init=False)
	"""Nom du Groupe (objet QT)."""
	_checkbox: QCheckBox = field(init=False)
	"""Case à cocher pour activer ou non le groupe."""
	_header: QFormLayout = field(init=False)
	"""Titre du groupe."""
	_body: QWidget = field(init=False)
	"""Corps du groupe (encapsulé dans un QWidget pour avoir un Hide/Show disponible)"""

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
		self._widget = QWidget()
		layout = QFormLayout(self._widget)
		layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # Définir l'alignement du calque en haut.

		# Title Row
		self._title = QLabel(f"{self.label}")
		self._title.setStyleSheet("font-weight: bold;")  # Style pour le label de titre
		self._checkbox = QCheckBox()
		self._checkbox.stateChanged.connect(self.toggle_active)

		self._header = QFormLayout(None)
		self._header.addRow(self._checkbox, self._title)
		layout.addRow(self._header)

		# Settings part (must be managed by the derived class.)
		self._body = QWidget()
		body = QFormLayout(self._body)
		body.setContentsMargins(20, 0, 0, 0)  # Léger décalage.
		for key, setting in self._settings.items():
			if isinstance(setting, BaseSettingGroup): body.addRow(setting.widget)
			else: body.addRow(setting.layout)
		layout.addRow(self._body)

		self._widget.setLayout(layout)

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
	def widget(self) -> QWidget:
		"""Retourne le calque associé à ce groupe de paramètres."""
		return self._widget

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
	def get_setting_names(self) -> list[str]:
		"""Récupère le nom des paramètres de ce groupe."""
		return list(self._settings.keys())

	##################################################
	def get_settings(self) -> dict[str, Any]:
		"""
		Récupère les valeurs des Settings
		:return: Dictionnaire de valeurs
		"""
		res = {key: setting.get_value() for key, setting in self._settings.items()}
		for group in self._inner_groups:
			setting_group = cast(BaseSettingGroup, self._settings[group])
			res.pop(group, None)  # Supprime la clé si elle existe
			tmp = {f"{group} {key}": value for key, value in setting_group.get_settings().items()}
			res = {**res, **tmp}  # Fusionne les dictionnaires
		return res

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
	def get_value(self):
		"""Fonction vide necessaire aux parcours automatiques."""
		return

	##################################################
	def set_value(self, value: Any):
		"""Fonction vide necessaire aux parcours automatiques."""
		return

	# ==================================================
	# endregion Getter/Setter
	# ==================================================

	# ==================================================
	# region Hide and Seek
	# ==================================================
	##################################################
	def hide(self):
		"""Cache le widget."""
		self._widget.hide()

	##################################################
	def show(self):
		"""Affiche le widget."""
		self._widget.show()

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
		if self._header and self._checkbox:
			self._header.layout().removeWidget(self._checkbox)  # Retirer la checkbox du layout
			self._checkbox.deleteLater()  # Détruire la checkbox

	# Ajouter des espaces au nom du groupe pour conserver à minima l'alignement, oui et non à voir.
	# self._title.setText(f"       {self.label}")

	##################################################
	def remove_header(self):
		""" Active toujours le groupe et supprime la partie header de l'interface. """
		self.always_active()
		# Suppression du titre
		if self._header and self._title:
			self._header.layout().removeWidget(self._title)  # Retirer le titre du layout
			self._title.deleteLater()						 # Détruire le titre

		# Suppression du header
		if self._header and self._widget:		# pragma: no cover (toujours faux)
			layout = self._widget.layout()		# Récupérer le layout principal
			if isinstance(layout, QWidget):		# Vérifier que c'est bien un QFormLayout
				layout.removeRow(self._header)  # Supprimer la ligne du layout

		# Suppression de la marge
		body_layout = self._body.layout()				# Récupérer le layout du widget _body
		if isinstance(body_layout, QFormLayout):		# pragma: no cover (toujours vrai)
			body_layout.setContentsMargins(0, 0, 0, 0)  # Aucune marge

	# ==================================================
	# endregion Hide and Seek
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
				msg += f"{line_prefix}- {key} :\n{setting.tostring(f'{line_prefix}  ')}"
			else: msg += f"{line_prefix}- {key} : {setting.get_value()}\n"
		return msg

	##################################################
	def __str__(self) -> str: return self.tostring()

# ==================================================
# endregion IO
# ==================================================
