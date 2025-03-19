"""
Ce fichier définit la classe :class:`.Settings`, utilisée pour gérer et enregistrer les paramètres nécessaires à la configuration de PALM Tracer.

**Fonctionnalités principales** :

- Permet le parsing et l'enregistrement des paramètres liés à l'interface utilisateur.
- Fournit une gestion structurée des paramètres par sections et algorithmes.

**Usage** :

La classe :class:`.Settings` est conçue pour interagir directement avec l'interface utilisateur en facilitant le paramétrage de PALM Tracer.
"""

from dataclasses import dataclass, field
from typing import Any, cast

from palm_tracer.Settings.Groups import *


##################################################
@dataclass
class Settings:
	"""
	Classe nécessaire au parsing et enregistrement des différents settings de PALM Tracer.

	Attributs :
			- :class:`palm_tracer.Settings.Groups.Batch` : Groupe de paramètres liés au batch.
			- :class:`palm_tracer.Settings.Groups.Calibration` : Groupe de paramètres liés à la calibration.
			- :class:`palm_tracer.Settings.Groups.Localization` : Groupe de paramètres liés à la localisation.
			- :class:`palm_tracer.Settings.Groups.Tracking` : Groupe de paramètres liés au tracking.
			- :class:`palm_tracer.Settings.Groups.VisualizationHR` : Groupe de paramètres liés à la visualisation haute résolution.
			- :class:`palm_tracer.Settings.Groups.VisualizationGraph` : Groupe de paramètres liés à la visualisation de graphiques.
			- :class:`palm_tracer.Settings.Groups.Filtering` : Groupe de paramètres liés au filtrage lors des processus.
	"""

	_settings: dict[str, BaseSettingGroup] = field(init=False, default_factory=dict[str, BaseSettingGroup])

	# ==================================================
	# region Initialization
	# ==================================================
	##################################################
	def __post_init__(self):
		"""Méthode appelée automatiquement après l'initialisation du dataclass."""
		self._settings = dict[str, BaseSettingGroup]()
		list_settings = [Batch, Calibration, Localization, Tracking, Gallery, VisualizationHR, VisualizationGraph, Filtering]
		for setting in list_settings:
			self._settings[setting.__name__] = setting()

		self._settings["Batch"].always_active()
		self._settings["Calibration"].always_active()

	##################################################
	def reset(self):
		"""Remet les valeurs par défaut des paramètres."""
		for _, setting in self._settings.items(): setting.reset()

	# ==================================================
	# endregion Initialization
	# ==================================================

	# ==================================================
	# region Getter/Setter
	# ==================================================
	##################################################
	@property
	def batch(self) -> Batch: return cast(Batch, self._settings["Batch"])

	##################################################
	@property
	def calibration(self) -> Calibration: return cast(Calibration, self._settings["Calibration"])

	##################################################
	@property
	def localization(self) -> Localization: return cast(Localization, self._settings["Localization"])

	##################################################
	@property
	def tracking(self) -> Tracking: return cast(Tracking, self._settings["Tracking"])

	##################################################
	@property
	def gallery(self) -> Gallery: return cast(Gallery, self._settings["Gallery"])

	##################################################
	@property
	def visualization_hr(self) -> VisualizationHR: return cast(VisualizationHR, self._settings["VisualizationHR"])

	##################################################
	@property
	def visualization_graph(self) -> VisualizationGraph: return cast(VisualizationGraph, self._settings["VisualizationGraph"])

	##################################################
	@property
	def filtering(self) -> Filtering: return cast(Filtering, self._settings["Filtering"])

	# ==================================================
	# endregion Getter/Setter
	# ==================================================

	# ==================================================
	# region Parsing
	# ==================================================
	##################################################
	def to_dict(self) -> dict[str, Any]:
		"""Renvoie un dictionnaire contenant toutes les informations de la classe."""
		return {"PALM Tracer Settings": {name: obj.to_dict() for name, obj in self._settings.items()}}

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
		for name, obj in self._settings.items():
			if name in groups: obj.update_from_dict(groups[name])

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
		for key, setting in self._settings.items():
			msg += f"  - {key} :\n{setting.tostring('    ')}"
		return msg

	##################################################
	def __str__(self) -> str: return self.tostring()

# ==================================================
# endregion IO
# ==================================================
