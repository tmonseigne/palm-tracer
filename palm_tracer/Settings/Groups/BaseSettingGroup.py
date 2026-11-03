"""Définit la classe de base commune aux groupes de paramètres."""

from __future__ import annotations

from contextlib import AbstractContextManager, ExitStack
from dataclasses import dataclass, field
from typing import Any

from qtpy.QtCore import QSignalBlocker

from palm_tracer.Settings.Groups.BaseUIGroup import BaseUIGroup
from palm_tracer.Settings.Types import BaseSettingType, CheckRangeFloat, CheckRangeInt, SignalWrapper


# --------------------------------------------------
@dataclass
class BaseSettingGroup:
	"""
	Gère un ensemble cohérent de paramètres et ses représentations Qt.

	Les sous-classes construisent leurs paramètres dans la fabrique de :attr:`_settings`. La classe de base initialise leurs connexions,
	crée leurs vues et assure leur sérialisation.
	"""

	label: str = field(init=False, default="Base Setting Group")
	"""Nom du groupe."""
	_mode: int = field(init=False, default=0)
	"""Méthode d'affichage du groupe par défaut."""
	_active: bool = field(init=False, default=False)
	"""État du groupe (activé ou non)."""
	_settings: dict[str, BaseSettingGroup | BaseSettingType] = field(init=False, default_factory=dict)
	"""Dictionnaire des paramètres du groupe, indexé par leur nom."""
	_uis: dict[str, BaseUIGroup] = field(init=False, default_factory=lambda: dict[str, BaseUIGroup]())
	"""Dictionnaire des interfaces qui ont été créées pour ce groupe de paramètres."""
	_signal: SignalWrapper = field(init=False, default_factory=SignalWrapper)
	"""Notification agrégée des changements du groupe, après synchronisation de ses dépendances."""

	# ==================================================
	# region Initialisation
	# ==================================================
	def __post_init__(self):
		"""Méthode appelée automatiquement après l'initialisation du dataclass."""
		self.initialize()
		# Les observateurs sont raccordés après les callbacks qui synchronisent les paramètres dépendants.
		for setting in self._settings.values(): setting.connect_after(self._signal.emit)
		if self._mode != 0: self.active = True

	# --------------------------------------------------
	def initialize(self):
		"""Initialise les connexions des paramètres dans les sous-classes qui en ont besoin."""

	# --------------------------------------------------
	def reset(self):
		"""Remet les valeurs par défaut des paramètres."""
		with self.signal_blocked():
			for setting in self._settings.values(): setting.reset()

	# ==================================================
	# endregion Initialisation
	# ==================================================

	# ==================================================
	# region Accesseurs
	# ==================================================
	def get_ui(self, name: str = "default", mode: int = -1) -> BaseUIGroup:
		"""
		Retourne une interface (:class:`~palm_tracer.Settings.Groups.BaseUIGroup.BaseUIGroup`) existante ou en crée une si nécessaire.

		:param name: Nom de l'interface dans le dictionnaire.
		:param mode: Méthode de création du groupe.

			- -1 : Valeur par défaut du groupe
			- 0 : Avec un titre et une checkbox pour activer/désactiver le groupe
			- 1 : Groupe toujours actif, sans case à cocher
			- 2 : Groupe sans en-tête

		:return: Interface du groupe (:class:`~palm_tracer.Settings.Groups.BaseUIGroup.BaseUIGroup`).
		"""
		if name in self._uis: return self._uis[name]
		if mode < 0: mode = self._mode
		ui = BaseUIGroup(name=self.label, mode=mode)
		if ui.checkbox is not None:
			ui.checkbox.setChecked(self.active)  # .		Active ou non la Check Box
			ui.checkbox.toggled.connect(self.set_active)  # Connecte le changement de la checkbox
		ui.active(self.active if mode == 0 else True)
		body = ui.body_layout

		for setting in self._settings.values():
			if isinstance(setting, BaseSettingGroup): body.addRow(setting.get_ui(name).widget)
			else: setting.get_ui(name).attach_to_form(body)

		self._uis[name] = ui  # Ajoute l'UI au dictionnaire
		return ui

	# --------------------------------------------------
	def clean_ui(self, name: str = "default"):
		"""
		Supprime l'interface Qt associée au nom donné.

		:param name: Nom de l'interface dans le dictionnaire.
		"""
		self._uis.pop(name, None)

		for setting in self._settings.values():
			setting.clean_ui(name)

	# --------------------------------------------------
	@property
	def active(self) -> bool:
		"""État du groupe, activé ou non (:class:`bool`)."""
		return self._active

	# --------------------------------------------------
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
		self._signal.emit()

	# --------------------------------------------------
	@property
	def value(self) -> Any:
		"""Fonction vide nécessaire aux parcours automatiques."""
		return

	# --------------------------------------------------
	@value.setter
	def value(self, value: Any):
		"""
		Définit la valeur du groupe de paramètres.

		:param value: Nouvelle valeur du groupe.
		"""
		return

	# --------------------------------------------------
	@property
	def settings_names(self) -> list[str]:
		"""Récupère les noms des paramètres de ce groupe."""
		return list(self._settings.keys())

	# --------------------------------------------------
	@property
	def settings(self) -> dict[str, Any]:
		"""Récupère les valeurs des paramètres."""
		res: dict[str, Any] = {}
		for key, setting in self._settings.items():
			if isinstance(setting, BaseSettingType): res[key] = setting.value
			else: res.update({f"{key} {sub_key}": value for sub_key, value in setting.settings.items()})
		return res

	# --------------------------------------------------
	def __getitem__(self, key: str) -> BaseSettingGroup | BaseSettingType:
		"""Surcharge de l'opérateur []."""
		return self._settings[key]

	# --------------------------------------------------
	def __contains__(self, key: str) -> bool:
		"""Surcharge pour vérifier si une clé existe."""
		return key in self._settings

	# --------------------------------------------------
	def __iter__(self):
		"""Surcharge pour obtenir l'itérable des clés."""
		return iter(self._settings)

	# ==================================================
	# endregion Accesseurs
	# ==================================================

	# ==================================================
	# region Visibilité
	# ==================================================
	def hide(self):
		"""Cache le paramètre."""
		for ui in self._uis.values(): ui.hide()

	# --------------------------------------------------
	def show(self):
		"""Affiche le paramètre."""
		for ui in self._uis.values(): ui.show()

	# ==================================================
	# endregion Visibilité
	# ==================================================

	# ==================================================
	# region Sérialisation
	# ==================================================
	def to_compact_dict(self) -> dict[str, Any]:
		"""Renvoie un dictionnaire minimal contenant la valeur du setting."""
		return {"active": self.active, "settings": {name: setting.to_compact_dict() for name, setting in self._settings.items()}}

	# --------------------------------------------------
	def update_from_compact_dict(self, data: dict[str, Any]):
		"""Met à jour la classe à partir d'un dictionnaire minimal."""
		with self.signal_blocked():
			self.active = data.get("active", False)
			settings = data["settings"]
			for key, setting in self._settings.items():
				if key in settings: setting.update_from_compact_dict(settings[key])

	# --------------------------------------------------
	def tostring(self, line_prefix: str = "") -> str:
		"""
		Retourne une chaîne de caractères correspondant à la liste des paramètres.

		:param line_prefix: Préfixe de chaque ligne (par exemple pour ajouter une indentation).
		:return: Une description textuelle des paramètres.
		"""
		msg = f"{line_prefix}- Activate : {self.active}\n"
		for key, setting in self._settings.items():
			if isinstance(setting, BaseSettingGroup): msg += f"{line_prefix}- {key} :\n{setting.tostring(f'{line_prefix}  ')}"
			elif isinstance(setting, (CheckRangeFloat, CheckRangeInt)):
				msg += f"{line_prefix}- {key} : {'Activate' if setting.active else 'Deactivate'} {setting.value}\n"
			else: msg += f"{line_prefix}- {key} : {setting.value}\n"
		return msg

	# --------------------------------------------------
	def __str__(self) -> str:
		"""
		Retourne une représentation textuelle de l'objet.

		:return: Représentation textuelle de l'objet.
		"""
		return self.tostring()

	# ==================================================
	# endregion Sérialisation
	# ==================================================

	# ==================================================
	# region Fonctions de rappel
	# ==================================================
	def set_active(self, state: int):
		"""Met à jour l'état actif du groupe lorsque la checkbox est modifiée."""
		self.active = bool(state)

	# ==================================================
	# endregion Fonctions de rappel
	# ==================================================

	# ==================================================
	# region Signaux
	# ==================================================
	def connect(self, f: Any):
		"""
		Connecte une fonction ou un slot à la notification finale des changements du groupe.

		:param f: Fonction ou slot appelé avec :obj:`None` après synchronisation des paramètres.
		"""
		self._signal.connect(f)

	# --------------------------------------------------
	def connect_after(self, f: Any):
		"""
		Connecte une notification finale après le signal ordinaire.

		Les callbacks directs sont terminés ; les callbacks transférés vers un autre thread ne sont pas attendus.

		:param f: Fonction ou slot appelé avec :obj:`None`.
		"""
		self._signal.connect_after(f)

	# --------------------------------------------------
	def disconnect(self, f: Any | None = None):
		"""
		Déconnecte les observateurs enregistrés par :meth:`connect`.

		Les connexions établies par :meth:`connect_after` et les dépendances internes sont conservées.

		:param f: Fonction ou slot à déconnecter, ou :obj:`None` pour tous les observateurs ordinaires.
		:return: Nombre de slots ordinaires déconnectés.
		"""
		return self._signal.disconnect(f)

	# --------------------------------------------------
	def signal_blocked(self, emit_last: bool = True) -> AbstractContextManager[Any]:
		"""
		Diffère les signaux des paramètres et publie le groupe après synchronisation des dépendances.

		:param emit_last: Publie la notification finale du groupe et des sous-groupes, ou les rend silencieux.
			Les callbacks individuels restent exécutés au déblocage pour synchroniser les valeurs et les contrôles.
		:return: Contexte de blocage des paramètres et des notifications du groupe.
		"""
		# noinspection PyAbstractClass
		stack = ExitStack()
		stack.enter_context(self._signal.blocked(emit_last))
		for setting in self._settings.values():
			# Les callbacks individuels restent nécessaires pour synchroniser les dépendances internes.
			context = setting.signal_blocked(emit_last) if isinstance(setting, BaseSettingGroup) else setting.signal_blocked()
			stack.enter_context(context)
		return stack
