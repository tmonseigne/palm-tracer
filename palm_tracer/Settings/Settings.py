"""
Ce fichier définit la classe `Settings`, utilisée pour gérer et enregistrer les paramètres nécessaires à la configuration de PALM Tracer.

**Fonctionnalités principales** :

- Permet le parsing et l'enregistrement des paramètres liés à l'interface utilisateur.
- Fournit une gestion structurée des paramètres par sections et algorithmes.

**Usage** :

La classe `Settings` est conçue pour interagir directement avec l'interface utilisateur en facilitant le paramétrage de PALM Tracer.
"""

from dataclasses import dataclass, field
from typing import Any

from qtpy.QtWidgets import QFormLayout

from palm_tracer.Settings.Groups import *


##################################################
@dataclass
class Settings:
	"""Classe nécessaire au parsing et enregistrement des différents settings de PALM Tracer"""

	batch: Batch = field(init=False, default_factory=Batch)
	calibration: Calibration = field(init=False, default_factory=Calibration)
	localisation: Localisation = field(init=False, default_factory=Localisation)

	# ==================================================
	# region Initialization
	# ==================================================
	##################################################
	def __post_init__(self):
		"""Méthode appelée automatiquement après l'initialisation du dataclass."""
		self.batch.always_active()
		self.calibration.always_active()

	##################################################
	def reset(self):
		"""Remet les valeurs par défaut des paramètres."""
		self.batch.reset()
		self.calibration.reset()
		self.localisation.reset()

	# ==================================================
	# endregion Initialization
	# ==================================================

	# ==================================================
	# region Getter/Setter
	# ==================================================
	##################################################
	def get_layouts(self) -> list[QFormLayout]:
		return [self.batch.layout,
				self.calibration.layout,
				self.localisation.layout]

	# ==================================================
	# endregion Getter/Setter
	# ==================================================

	# ==================================================
	# region Parsing
	# ==================================================
	##################################################
	def to_dict(self) -> dict[str, Any]:
		"""Renvoie un dictionnaire contenant toutes les informations de la classe."""
		return {"PALM Tracer Settings": {"Batch":        self.batch.to_dict(),
										 "Calibration":  self.calibration.to_dict(),
										 "Localisation": self.localisation.to_dict()}}

	##################################################
	@classmethod
	def from_dict(cls, data: dict[str, Any]) -> "Settings":
		"""Créé une instance de la classe à partir d'un dictionnaire."""
		res = cls()  # Instancie la classe appelée
		res.update_from_dict(data)
		return res

	##################################################
	def update_from_dict(self, data: dict[str, Any]):
		""" Met à jour la classe à partir d'un dictionnaire."""
		groups = data["PALM Tracer Settings"]
		self.batch.update_from_dict(groups["Batch"])
		self.calibration.update_from_dict(groups["Calibration"])
		self.localisation.update_from_dict(groups["Localisation"])

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
		msg += f"  - Batch :\n{self.batch.tostring("    ")}"
		msg += f"  - Calibration :\n{self.calibration.tostring("    ")}"
		msg += f"  - Localisation :\n{self.localisation.tostring("    ")}"
		return msg

	##################################################
	def __str__(self) -> str: return self.tostring()

	# ==================================================
	# endregion IO
	# ==================================================
