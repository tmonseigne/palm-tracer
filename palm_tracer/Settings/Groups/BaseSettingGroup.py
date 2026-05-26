"""
Fichier contenant la classe :class:`BaseSettingGroup` et ses sous-classes pour la gestion des groupes de paramètres.

Ce module définit la classe abstraite :class:`.BaseSettingGroup`, qui sert de base pour la création de différents groupes de paramètres.
"""
from __future__ import annotations

import copy
from contextlib import AbstractContextManager, ExitStack, nullcontext
from dataclasses import dataclass, field
from typing import Any, Optional, Union

from qtpy.QtCore import QSignalBlocker

from palm_tracer.Settings.Groups.BaseUI import BaseUI
from palm_tracer.Settings.Types import BaseSettingType, CheckRangeFloat, CheckRangeInt


##################################################
@dataclass
class BaseSettingGroup:
	"""Classe mère pour un groupe de paramètres."""

	label: str = field(init=False, default="Base Setting Group")
	"""Nom du Groupe."""
	setting_list = dict[str, list[Union["BaseSettingGroup", BaseSettingType, Any]]]()
	"""Liste des paramètres du groupe (:class:`dict[str, list[Union[BaseSettingGroup, BaseSettingType, Any]]]`)."""
	mode: int = 0
	"""Méthode d'affichage du groupe par défaut."""
	_active: bool = field(init=False, default=False)
	"""État du groupe (activé ou non)"""
	_settings: dict[str, Union["BaseSettingGroup", BaseSettingType]] = field(init=False)
	"""Liste des visualisations de settings (inputs) du groupe (:class:`dict[str, Union[BaseSettingGroup, BaseSettingType]]`)."""
	_uis: dict[str, BaseUI] = field(init=False, default_factory=lambda: dict[str, BaseUI]())
	"""Dictionnaire des interfaces qui ont été créé pour ce groupe de paramètres."""

	# ==================================================
	# region Initialization
	# ==================================================
	##################################################
	def __post_init__(self):
		"""Méthode appelée automatiquement après l'initialisation du dataclass."""
		self.initialize()
		if self.mode != 0: self.active = True

	##################################################
	def initialize(self):
		"""Initialise le dictionnaire de paramètres."""
		self._settings = dict[str, Union["BaseSettingGroup", BaseSettingType]]()
		for key, value in self.setting_list.items():
			args = copy.deepcopy(value[1])
			self._settings[key] = value[0](*args)

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
	def get_ui(self, name: str = "default", mode: int = -1) -> BaseUI:
		"""
		Retourne un objet :class:`.BaseUI`, existant ou le créé si necessaire.

		:param name: Nom de l'interface dans le dictionnaire
		:param mode: Méthode de création du groupe.
			- -1 : Valeur par défaut du groupe
			- 0 : Avec un titre et une checkbox pour activer/desactiver le groupe
			- 1 : Etat lorsque l'on utilise la méthode always actif (la check box n'est pas créé)
			- 2 : Etat remove header (aucune création de l'espace titre)
			- 3 : A l'intérieur d'une QGroupBox (prochainement)
		"""
		if name in self._uis: return self._uis[name]
		if mode < 0: mode = self.mode
		ui = BaseUI(name=self.label, mode=mode)
		if ui.checkbox is not None:  ui.checkbox.toggled.connect(self.set_active)  # Connecte le changement de la checkbox
		ui.active(self.active if mode == 0 else True)
		body = ui.body_layout

		for setting in self._settings.values():
			if isinstance(setting, BaseSettingGroup): body.addRow(setting.get_ui(name).widget)
			else: setting.get_ui(name).attach_to_form(body)

		self._uis[name] = ui  # Ajoute l'ui au dictionnaire
		return ui

	##################################################
	def clean_ui(self, name: str):
		"""
		Supprime l'interface Qt associée au nom donné.

		:param name: Nom de l'interface dans le dictionnaire
		"""
		self._uis.pop(name, None)

		for setting in self._settings.values():
			setting.clean_ui(name)

	##################################################
	@property
	def active(self) -> bool:
		"""État du groupe, activé ou non (:class:`bool`)."""
		return self._active

	##################################################
	@active.setter
	def active(self, value: bool):
		"""Contrôle la modification de l'état actif."""
		if self._active == value: return
		self._active = value
		for ui in self._uis.values():
			if ui.checkbox is None: continue
			with QSignalBlocker(ui.checkbox):
				ui.checkbox.setChecked(value)
				ui.active(value)

	##################################################
	@property
	def value(self) -> Any:
		"""Fonction vide nécessaire aux parcours automatiques."""
		return

	##################################################
	@value.setter
	def value(self, value: Any): return

	##################################################
	@property
	def settings_names(self) -> list[str]:
		"""Récupère les noms des paramètres de ce groupe."""
		return list(self._settings.keys())

	##################################################
	@property
	def settings(self) -> dict[str, Any]:
		"""Récupère les valeurs des paramètres."""
		res: dict[str, Any] = {}
		for key, setting in self._settings.items():
			if isinstance(setting, BaseSettingType): res[key] = setting.value
			else: res.update({f"{key} {sub_key}": value for sub_key, value in setting.settings.items()})
		return res

	##################################################
	def __getitem__(self, key: str) -> Union["BaseSettingGroup", BaseSettingType]:
		"""Surcharge de l'opérateur []"""
		return self._settings[key]

	##################################################
	def __contains__(self, key: str) -> bool:
		"""Surcharge pour vérifier si une clé existe"""
		return key in self._settings

	##################################################
	def __iter__(self):
		"""Surcharge pour obtenir l'itérable des clés"""
		return iter(self._settings)

	# ==================================================
	# endregion Getter/Setter
	# ==================================================

	# ==================================================
	# region Hide and Seek
	# ==================================================
	##################################################
	def hide(self):
		"""Cache le paramètre."""
		for ui in self._uis.values(): ui.hide()

	##################################################
	def show(self):
		"""Affiche le paramètre."""
		for ui in self._uis.values(): ui.show()

	# ==================================================
	# endregion Hide and Seek
	# ==================================================

	# ==================================================
	# region Parsing
	# ==================================================
	##################################################
	def to_compact_dict(self) -> dict[str, Any]:
		"""Renvoie un dictionnaire minimal contenant la valeur du setting."""
		return {"active": self.active, "settings": {name: setting.to_compact_dict() for name, setting in self._settings.items()}}

	##################################################
	def update_from_compact_dict(self, data: dict[str, Any]):
		"""Mets à jour la classe à partir d'un dictionnaire minimal."""
		self.active = data.get("active", False)
		settings = data["settings"]
		for key, value in self.setting_list.items():  # Appelle `update_from_compact_dict` pour chaque élément de setting_list
			if key in settings: self._settings[key].update_from_compact_dict(settings[key])

	##################################################
	def tostring(self, line_prefix: str = "") -> str:
		"""
		Retourne une chaîne de caractères correspondant à la liste des paramètres.

		:param line_prefix: Préfixe de chaque ligne (par exemple pour ajouter une indentation)
		:return: Une description textuelle des paramètres.
		"""
		msg = f"{line_prefix}- Activate : {self.active}\n"
		for key, setting in self._settings.items():
			if isinstance(setting, BaseSettingGroup): msg += f"{line_prefix}- {key} :\n{setting.tostring(f'{line_prefix}  ')}"
			elif isinstance(setting, CheckRangeFloat | CheckRangeInt):
				msg += f"{line_prefix}- {key} : {'Activate' if setting.active else 'Deactivate'} {setting.value}\n"
			else: msg += f"{line_prefix}- {key} : {setting.value}\n"
		return msg

	##################################################
	def __str__(self) -> str: return self.tostring()

	# ==================================================
	# endregion Parsing
	# ==================================================

	# ==================================================
	# region Callbacks
	# ==================================================
	##################################################
	def set_active(self, state: int):
		"""Mets à jour l'état actif du groupe lorsque la checkbox est modifiée."""
		self.active = bool(state)

	# ==================================================
	# endregion Callbacks
	# ==================================================

	# ==================================================
	# region Signals
	# ==================================================
	##################################################
	def connect(self, f: Any):
		"""
		Connecte une fonction ou un slot à tous les éléments du groupe.

		:param f: Fonction ou slot à connecter.
		"""
		for _, setting in self._settings.items(): setting.connect(f)

	##################################################
	def disconnect(self, f: Optional[Any] = None):
		"""
		Déconnecte une fonction ou un slot à tous les éléments du groupe.

		:param f: Fonction ou slot à déconnecter.
		:return: Nombre de slots déconnectés
		"""
		for _, setting in self._settings.items(): setting.disconnect(f)

	##################################################
	def signal_blocked(self) -> AbstractContextManager[Any]:
		"""
		Blocage des signaux pour tout le groupe (récursif).
		Retourne un context manager utilisable avec `with ...:`.
		"""
		if not self._settings: return nullcontext()

		stack = ExitStack()
		for setting in self._settings.values(): stack.enter_context(setting.signal_blocked())  # Chaque enfant doit lui-même retourner un context manager
		return stack
