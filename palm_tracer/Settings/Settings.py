"""
Ce fichier définit la classe `Settings`, utilisée pour gérer et enregistrer les paramètres nécessaires à la configuration de PALM Tracer.

**Fonctionnalités principales** :

- Permet le parsing et l'enregistrement des paramètres liés à l'interface utilisateur.
- Fournit une gestion structurée des paramètres par sections et algorithmes.

**Usage** :

La classe `Settings` est conçue pour interagir directement avec l'interface utilisateur en facilitant le paramétrage de PALM Tracer.
"""

from dataclasses import dataclass, field
from typing import Any, cast

from palm_tracer.Settings.Groups import *


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
		self._groups["Batch"].activate()
		self._groups["Calibration"].activate()

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
	def __setitem__(self, key: str, value: BaseSettingGroup):
		""" Surcharge pour assigner une valeur avec [] """
		self._groups[key] = value

	##################################################
	def __contains__(self, key: str) -> bool:
		"""Surcharge pour vérifier si une clé existe"""
		return key in self._groups

	##################################################
	def __iter__(self):
		"""Surcharge pour obtenir l'itérable des clés"""
		return iter(self._groups)

	##################################################
	def get_output_path(self, suffix: str = "_PALM_Tracer"):
		""" Récupère le chemin des dossiers de sortie des fichiers PALM Tracer"""
		return cast(Batch, self._groups["Batch"]).get_path(suffix)

	# ==================================================
	# endregion Getter/Setter
	# ==================================================

	# ==================================================
	# region Parsing
	# ==================================================
	##################################################
	def to_dict(self) -> dict[str, Any]:
		"""Renvoie un dictionnaire contenant toutes les informations de la classe."""
		return {"PALM Tracer Settings": {name: group.to_dict() for name, group in self._groups.items()}}

	##################################################
	@classmethod
	def from_dict(cls, data: dict[str, Any]) -> "Settings":
		"""Créé une instance de la classe à partir d'un dictionnaire."""
		res = cls()  # Instancie la classe appelée
		groups = data["PALM Tracer Settings"]
		for key, value in groups.items():
			if key in res: res[key] = create_group_from_dict(value)  # if key exist to avoid bad settings in dictionary
		return res

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
