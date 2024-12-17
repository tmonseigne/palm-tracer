"""
Fichier contenant la classe `BaseSettingGroup` et ses sous-classes pour la gestion des groupes de paramètres.

Ce module définit la classe abstraite `BaseSettingGroup`, qui sert de base pour la création de différents groupes de paramètres.

"""

from dataclasses import dataclass, field

from palm_tracer.Settings.SettingTypes import BaseSettingType


##################################################
@dataclass
class BaseSettingGroup:
	"""
	Classe mère pour un groupe de setting :

	Attributs :
		- **_settings (dict[str, BaseSettingType])** : Liste des settings du groupe
	"""

	_settings: dict[str, BaseSettingType] = field(init=False)

	# ==================================================
	# region Initialization
	# ==================================================
	##################################################
	def __post_init__(self):
		""" Méthode appelée automatiquement après l'initialisation du dataclass. """
		self.initialize()

	##################################################
	def initialize(self):
		""" Initialise le dictionnaire de paramètres. """
		self._settings = dict[str, BaseSettingType]()

	##################################################
	def reset(self):
		""" Remet les valeurs par défaut des paramètres. """
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
		""" Récupère le nom des paramètres de ce groupe. """
		return list(self._settings.keys())

	##################################################
	def __getitem__(self, key: str) -> BaseSettingType:
		""" Surcharge de l'opérateur [] """
		return self._settings[key]

	##################################################
	#def __setitem__(self, key: str, value: BaseSettingType):
	#	""" Surcharge pour assigner une valeur avec [] """
	#	self._settings[key] = value

	##################################################
	def __contains__(self, key: str) -> bool:
		""" Surcharge pour vérifier si une clé existe """
		return key in self._settings

	##################################################
	def __iter__(self):
		""" Surcharge pour obtenir l'itérable des clés """
		return iter(self._settings)

	# ==================================================
	# endregion Getter/Setter
	# ==================================================

	# ==================================================
	# region Parsing
	# ==================================================

	# ==================================================
	# endregion Parsing
	# ==================================================

	# ==================================================
	# region IO
	# ==================================================
	##################################################
	def tostring(self, line_prefix: str = "") -> str:
		"""
		Retourne une chaîne de caractères correspondant à la liste des settings.

		:param line_prefix: Préfixe de chaque ligne (par exemple pour ajouter une indentation)
		:return: Une description textuelle des paramètres.
		"""
		msg = ""
		for key, setting in self._settings.items():
			msg += f"{line_prefix}- {key} : {setting.get_value()}\n"
		return msg

	##################################################
	def __str__(self) -> str: return self.tostring()

# ==================================================
# endregion IO
# ==================================================
