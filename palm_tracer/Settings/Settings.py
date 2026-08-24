"""Gère la configuration, la sérialisation et l'organisation des paramètres de PALM Tracer."""

from __future__ import annotations

from contextlib import AbstractContextManager, ExitStack
from dataclasses import dataclass, field
from typing import Any, Callable, cast, Optional

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Groups.BaseUIGroup import BaseUIGroup
from palm_tracer.Settings.Groups.Batch import Batch
from palm_tracer.Settings.Groups.BeadsExtraction import BeadsExtraction
from palm_tracer.Settings.Groups.BlinkingReconnection import BlinkingReconnection
from palm_tracer.Settings.Groups.Calibration import Calibration
from palm_tracer.Settings.Groups.Filters import Filters
from palm_tracer.Settings.Groups.Gallery import Gallery
from palm_tracer.Settings.Groups.Graph import Graph
from palm_tracer.Settings.Groups.HR import HR
from palm_tracer.Settings.Groups.Localization import Localization
from palm_tracer.Settings.Groups.Tracking import Tracking
from palm_tracer.Settings.Groups.TracksCompute import TracksCompute
from palm_tracer.Settings.ROIManager import ROIManager
from palm_tracer.Settings.Types import CheckInt, SpinInt


##################################################
@dataclass
class Settings:
	"""Classe nécessaire au parsing et enregistrement des différents paramètres de PALM Tracer."""

	_settings: dict[str, BaseSettingGroup] = field(init=False, default_factory=dict[str, BaseSettingGroup])
	"""Dictionnaire de groupes de paramètres."""
	_uis: dict[str, dict[str, BaseUIGroup]] = field(init=False, default_factory=lambda: dict[str, dict[str, BaseUIGroup]]())
	"""Dictionnaire des interfaces qui ont été créé pour ce groupe de paramètres."""
	rois: ROIManager = field(init=False)
	"""Manager des zones d'intérêts."""

	# ==================================================
	# region Initialization
	# ==================================================
	##################################################
	def __post_init__(self):
		"""Méthode appelée automatiquement après l'initialisation du dataclass."""
		self._settings = dict[str, BaseSettingGroup]()
		list_settings = [Batch, Calibration, Localization, BeadsExtraction, Tracking, BlinkingReconnection, TracksCompute,
						 Gallery, Graph, HR, Filters]
		for setting in list_settings: self._settings[setting.__name__] = setting()
		self._settings["Tracking"]["Max Distance"].sync(self._settings["BlinkingReconnection"]["Max Distance"])
		self.rois = ROIManager(cast(CheckInt, self.filters["ROI"]), cast(SpinInt, self.hr["Ratio"]))

	##################################################
	def reset(self):
		"""Remet les valeurs par défaut des paramètres."""
		for _, setting in self._settings.items(): setting.reset()

	##################################################
	def connect(self, f: Any):
		"""
		Connecte une fonction ou un slot à l'intégralité des paramètres.

		:param f: Fonction ou slot à connecter.
		"""
		for _, setting in self._settings.items(): setting.connect(f)

	##################################################
	def disconnect(self, f: Optional[Callable[[Any], None]] = None):
		"""
		Déconnecte une fonction ou un slot à tous les éléments du groupe.

		:param f: Fonction ou slot à déconnecter.
		:return: Nombre de slots déconnectés.
		"""
		for _, setting in self._settings.items(): setting.disconnect(f)

	##################################################
	def signal_blocked(self) -> AbstractContextManager[Any]:
		"""
		Blocage des signaux pour l'intégralité des paramètres.

		:return: Retourne un context manager utilisable avec `with ...:`.
		"""
		# if not self._settings: return nullcontext() # On n'a pas de settings vide
		stack = ExitStack()
		for group in self._settings.values(): stack.enter_context(group.signal_blocked())
		return stack

	# ==================================================
	# endregion Initialization
	# ==================================================

	# ==================================================
	# region Getter/Setter
	# ==================================================
	##################################################
	def get_ui(self, name: str = "default") -> dict[str, BaseUIGroup]:
		"""
		Retourne un dictionnaire d'objets :class:`.BaseUIGroup` (un par groupe de paramètres), existants ou les créés si nécessaire.

		:param name: Nom de l'interface dans le dictionnaire.
		"""
		if name in self._uis: return self._uis[name]
		ui = dict[str, BaseUIGroup]()
		for key, setting in self._settings.items(): ui[key] = setting.get_ui(name)
		self._uis[name] = ui  # Ajoute l'ui au dictionnaire
		return ui

	##################################################
	def clean_ui(self, name: str):
		"""
		Supprime récursivement les interfaces Qt associées au nom donné.

		:param name: Nom de l'interface dans le dictionnaire.
		"""
		for setting in self._settings.values(): setting.clean_ui(name)

	##################################################
	@property
	def batch(self) -> Batch:
		"""Groupe de paramètres liés au batch (:class:`Batch <palm_tracer.Settings.Groups.Batch.Batch>`)."""
		return cast(Batch, self._settings["Batch"])

	##################################################
	@property
	def calibration(self) -> Calibration:
		"""Groupe de paramètres liés à la calibration (:class:`Calibration <palm_tracer.Settings.Groups.Calibration.Calibration>`)."""
		return cast(Calibration, self._settings["Calibration"])

	##################################################
	@property
	def localization(self) -> Localization:
		"""Groupe de paramètres liés à la localisation (:class:`Localization <palm_tracer.Settings.Groups.Localization.Localization>`)."""
		return cast(Localization, self._settings["Localization"])

	##################################################
	@property
	def beads(self) -> BeadsExtraction:
		"""Groupe de paramètres liés à l'extraction des billes (:class:`BeadsExtraction <palm_tracer.Settings.Groups.BeadsExtraction.BeadsExtraction>`)."""
		return cast(BeadsExtraction, self._settings["BeadsExtraction"])

	##################################################
	@property
	def tracking(self) -> Tracking:
		"""Groupe de paramètres liés au suivi (:class:`Tracking <palm_tracer.Settings.Groups.Tracking.Tracking>`)."""
		return cast(Tracking, self._settings["Tracking"])

	##################################################
	@property
	def blinking(self) -> BlinkingReconnection:
		"""Groupe de paramètres liés à la correction du scintillement
		(:class:`BlinkingReconnection <palm_tracer.Settings.Groups.BlinkingReconnection.BlinkingReconnection>`)."""
		return cast(BlinkingReconnection, self._settings["BlinkingReconnection"])

	##################################################
	@property
	def tracks_compute(self) -> TracksCompute:
		"""Groupe de paramètres liés aux calculs sur trajectoires (:class:`TracksCompute <palm_tracer.Settings.Groups.TracksCompute.TracksCompute>`)."""
		return cast(TracksCompute, self._settings["TracksCompute"])

	##################################################
	@property
	def gallery(self) -> Gallery:
		"""Groupe de paramètres liés à la génération de galerie (:class:`Gallery <palm_tracer.Settings.Groups.Gallery.Gallery>`)."""
		return cast(Gallery, self._settings["Gallery"])

	##################################################
	@property
	def hr(self) -> HR:
		"""Groupe de paramètres liés à la Visualisation haute-résolution
		(:class:`HR <palm_tracer.Settings.Groups.HR.HR>`)."""
		return cast(HR, self._settings["HR"])

	##################################################
	@property
	def graph(self) -> Graph:
		"""Groupe de paramètres liés à la Visualisation graphique
		(:class:`Graph <palm_tracer.Settings.Groups.Graph.Graph>`)."""
		return cast(Graph, self._settings["Graph"])

	##################################################
	@property
	def filters(self) -> Filters:
		"""Groupe de paramètres liés au filtrage (:class:`Filters <palm_tracer.Settings.Groups.Filters.Filters>`)."""
		return cast(Filters, self._settings["Filters"])

	# ==================================================
	# endregion Getter/Setter
	# ==================================================

	# ==================================================
	# region Parsing
	# ==================================================
	##################################################
	def to_compact_dict(self) -> dict[str, Any]:
		"""Renvoie un dictionnaire minimal contenant la valeur du setting."""
		res = {"PALM Tracer Settings": {name: obj.to_compact_dict() for name, obj in self._settings.items()}}
		res["PALM Tracer Settings"]["ROIs"] = self.rois.to_dict_list()
		return res

	##################################################
	def update_from_compact_dict(self, data: dict[str, Any]):
		"""Mets à jour la classe à partir d'un dictionnaire minimal."""
		groups = data["PALM Tracer Settings"]
		for name, obj in self._settings.items():
			if name in groups: obj.update_from_compact_dict(groups[name])
		if "ROIs" in groups: self.rois.from_dict_list(groups["ROIs"])

	# ==================================================
	# endregion Parsing
	# ==================================================

	# ==================================================
	# region IO
	# ==================================================
	##################################################
	def tostring(self) -> str:
		"""
		Retourne une chaîne de caractères correspondant à la liste des paramètres.

		:return: Une description textuelle des paramètres de PALM Tracer.
		"""
		msg = f"Settings :\n"
		for key, setting in self._settings.items():
			msg += f"  - {key} :\n{setting.tostring('    ')}"
		return msg

	##################################################
	def __str__(self) -> str: return self.tostring()


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # crée et assigne le layout au widget
	settings = Settings()
	setting_ui = settings.get_ui()

	lay.addWidget(setting_ui["Batch"].widget)
	lay.addWidget(setting_ui["Calibration"].widget)
	lay.addWidget(setting_ui["Localization"].widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
