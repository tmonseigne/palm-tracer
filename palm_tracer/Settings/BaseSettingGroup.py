"""
Fichier contenant la classe `BaseSettingGroup` et ses sous-classes pour la gestion des paramètres d'interface utilisateur.

Ce module définit la classe abstraite `BaseSettingType`, qui sert de base pour la création de différents types de paramètres dans une interface utilisateur Qt.
Les sous-classes permettent de gérer des paramètres spécifiques tels que les entiers, les flottants et les listes déroulantes.
Ces classes sont utilisées pour créer et configurer des widgets de paramètres dans une interface graphique.

Classes :

    - Setting : Classe de base pour un paramètre d'interface utilisateur.
    - CheckSetting : Paramètre de type Check box.
    - ComboSetting : Paramètre de type liste déroulante avec options.
    - FileSetting : Paramètre de type ouverture de fichier.
    - FloatSetting : Paramètre de type flottant (float).
    - IntSetting : Paramètre de type entier (integer).
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
			msg += f"{line_prefix}- {key} : {setting.label} ({setting.get_value()})\n"
		return msg

	##################################################
	def __str__(self) -> str: return self.tostring()

# ==================================================
# endregion IO
# ==================================================
