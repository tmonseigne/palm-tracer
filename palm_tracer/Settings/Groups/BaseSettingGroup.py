"""
Fichier contenant la classe `BaseSettingGroup` et ses sous-classes pour la gestion des groupes de paramètres.

Ce module définit la classe abstraite `BaseSettingGroup`, qui sert de base pour la création de différents groupes de paramètres.

.. todo::
   Ajout d'un get_widget pour le sous-groupe
"""

from dataclasses import dataclass, field
from typing import Any, Union

from palm_tracer.Settings.Types import BaseSettingType


##################################################
@dataclass
class BaseSettingGroup:
	"""
	Classe mère pour un groupe de setting :

	Attributs :
			- **_settings (dict[str, Union[BaseSettingGroup, BaseSettingType]])** : Liste des settings du groupe
	"""

	active: bool = field(init=False, default=False)
	_settings: dict[str, Any] = field(init=False)
	setting_list = dict[str, list[Any]]()

	# ==================================================
	# region Initialization
	# ==================================================
	##################################################
	def __post_init__(self):
		"""Méthode appelée automatiquement après l'initialisation du dataclass."""
		self.initialize()

	##################################################
	def initialize(self):
		"""Initialise le dictionnaire de paramètres."""
		self._settings = dict[str, Any]()
		for key, value in self.setting_list.items():
			self._settings[key] = value[0](*value[1])

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
	def get_setting_names(self) -> list[str]:
		"""Récupère le nom des paramètres de ce groupe."""
		return list(self._settings.keys())

	##################################################
	def __getitem__(self, key: str) -> Any:
		"""Surcharge de l'opérateur []"""
		return self._settings[key]

	##################################################
	def __setitem__(self, key: str, value: Any):
		"""Surcharge pour assigner une valeur avec []"""
		self._settings[key] = value

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

	# ==================================================
	# endregion Getter/Setter
	# ==================================================

	# ==================================================
	# region IO
	# ==================================================
	##################################################
	def to_dict(self) -> dict[str, Any]:
		"""Renvoie un dictionnaire contenant toutes les informations de la classe."""
		return {"type":     type(self).__name__, "active": self.active,
				"settings": {name: setting.to_dict() for name, setting in self._settings.items()}, }

	##################################################
	@classmethod
	def from_dict(cls, data: dict[str, Any]) -> "BaseSettingGroup":
		"""Créé une instance de la classe à partir d'un dictionnaire."""
		res = cls()  # Instancie la classe appelée
		res.active = data.get("active", False)
		settings = data["settings"]
		for key, value in cls.setting_list.items():  # Appelle `from_dict` pour chaque élément de setting_list
			if key in settings: res[key] = value[0].from_dict(settings[key])
		return res

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
