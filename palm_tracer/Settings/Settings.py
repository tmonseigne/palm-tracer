"""
Ce fichier définit la classe `Settings`, utilisée pour gérer et enregistrer les paramètres nécessaires à la configuration de PALM Tracer.

**Fonctionnalités principales** :

- Permet le parsing et l'enregistrement des paramètres liés à l'interface utilisateur.
- Fournit une gestion structurée des paramètres par sections et algorithmes.

**Usage** :

La classe `Settings` est conçue pour interagir directement avec l'interface utilisateur en facilitant le paramétrage de PALM Tracer.
"""

from dataclasses import dataclass, field

from palm_tracer.Settings.Group.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Group.Batch import Batch
from palm_tracer.Settings.Group.Calibration import Calibration
from palm_tracer.Settings.Group.Localisation import Localisation


##################################################
@dataclass
class Settings:
	"""Classe nécessaire au parsing et enregistrement des différents settings de PALM Tracer"""

	_groups: dict[str, BaseSettingGroup] = field(init=False, default_factory=dict[str, BaseSettingGroup])

	# ==================================================
	# region Initialization
	# ==================================================
	##################################################
	def __post_init__(self):
		"""Méthode appelée automatiquement après l'initialisation du dataclass."""
		self._groups["Batch"] = Batch()
		self._groups["Calibration"] = Calibration()
		self._groups["Localisation"] = Localisation()

	##################################################
	def reset(self):
		"""Remet les valeurs par défaut des paramètres."""
		for _, group in self._groups.items():
			group.reset()

	# ==================================================
	# endregion Initialization
	# ==================================================

	# ==================================================
	# region Getter/Setter
	# ==================================================
	##################################################
	def get_group_names(self) -> list[str]:
		"""Récupère le nom des groupes de paramètres."""
		return list(self._groups.keys())

	##################################################
	def __getitem__(self, key: str) -> BaseSettingGroup:
		"""Surcharge de l'opérateur []"""
		return self._groups[key]

	##################################################
	# def __setitem__(self, key: str, value: BaseSettingGroup):
	#	""" Surcharge pour assigner une valeur avec [] """
	#	self._groups[key] = value

	##################################################
	def __contains__(self, key: str) -> bool:
		"""Surcharge pour vérifier si une clé existe"""
		return key in self._groups

	##################################################
	def __iter__(self):
		"""Surcharge pour obtenir l'itérable des clés"""
		return iter(self._groups)

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
	def tostring(self) -> str:
		"""
		Retourne une chaîne de caractères correspondant à la liste des settings.

		:return: Une description textuelle des paramètres de PALM Tracer.
		"""
		msg = f"Settings :\n"
		for key, group in self._groups.items():
			msg += f"  - {key} :\n{group.tostring("    ")}"
		return msg

	##################################################
	def __str__(self) -> str: return self.tostring()

# ==================================================
# endregion IO
# ==================================================
