"""
Fichier contenant la classe :class:`BaseSettingGroup` et ses sous-classes pour la gestion des groupes de paramètres.

Ce module définit la classe abstraite :class:`.BaseSettingGroup`, qui sert de base pour la création de différents groupes de paramètres.
"""
from contextlib import AbstractContextManager, ExitStack, nullcontext
from dataclasses import dataclass, field
from typing import Any, Callable, cast, Optional, Union

from qtpy import QT_API
from qtpy.QtWidgets import QCheckBox, QFormLayout, QLabel, QWidget

from palm_tracer.Settings.Types import BaseSettingType
from palm_tracer.Tools import Ui

if QT_API.startswith("pyqt"):  # . 	pragma: no cover — dépend de l'environnement
	from qtpy import sip  # .		dispo quand le binding est PyQt

	_IS_PYQT = True
else:  # .							pragma: no cover — dépend de l'environnement
	import shiboken6  # .			dispo quand le binding est PySide6

	_IS_PYQT = False


##################################################
@dataclass
class BaseSettingGroup:
	"""Classe mère pour un groupe de paramètres."""

	label: str = field(init=False, default="Base Setting Group")
	"""Nom du Groupe."""
	setting_list = dict[str, list[Union["BaseSettingGroup", BaseSettingType, Any]]]()
	"""Liste des paramètres du groupe (:class:`dict[str, list[Union[BaseSettingGroup, BaseSettingType, Any]]]`)."""

	_active: bool = field(init=False, default=False)
	"""État du groupe (activé ou non)"""
	_inner_groups = list[str]()
	"""Liste des sous-groupes de settings du groupe."""
	_settings: dict[str, Union["BaseSettingGroup", BaseSettingType]] = field(init=False)
	"""Liste des visualisations de settings (inputs) du groupe (:class:`dict[str, Union[BaseSettingGroup, BaseSettingType]]`)."""
	_widget: QWidget = field(init=False)
	"""Widget principal du groupe."""
	_title: Optional[QLabel] = field(init=False)
	"""QLabel du titre du Groupe (:class:`QLabel`)."""
	_checkbox: Optional[QCheckBox] = field(init=False)
	"""Case à cocher pour activer ou non le groupe (:class:`QCheckBox`)."""
	_header: Optional[QFormLayout] = field(init=False)
	"""Titre du groupe (:class:`QFormLayout`)."""
	_body: QWidget = field(init=False)
	"""Corps du groupe encapsulé dans un QWidget pour avoir un Hide/Show disponible (:class:`QWidget`)."""

	# ==================================================
	# region Initialization
	# ==================================================
	##################################################
	def __post_init__(self):
		"""Méthode appelée automatiquement après l'initialisation du dataclass."""
		self.initialize()
		self.initialize_ui()

	##################################################
	def initialize(self):
		"""Initialise le dictionnaire de paramètres."""
		self._settings = dict[str, Union["BaseSettingGroup", BaseSettingType]]()
		for key, value in self.setting_list.items(): self._settings[key] = value[0](*value[1])

	##################################################
	def initialize_ui(self):
		"""Initialise l'interface utilisateur."""
		# Base
		self._widget = QWidget()
		layout = Ui.make_form(self._widget)

		# Title Row
		self._title = QLabel(f"{self.label}")
		self._title.setStyleSheet("font-weight: bold;")  # Style pour le label de titre
		self._checkbox = QCheckBox()
		self._checkbox.stateChanged.connect(self.toggle_active)

		self._header = QFormLayout(None)
		self._header.addRow(self._checkbox, self._title)
		layout.addRow(self._header)

		# Settings part (must be managed by the derived class.)
		self._body = QWidget()
		body = QFormLayout(self._body)
		body.setContentsMargins(5, 0, 0, 0)  # Léger décalage.
		for key, setting in self._settings.items():
			if isinstance(setting, BaseSettingGroup): body.addRow(setting.widget)
			else: setting.attach_to_form(body)

		layout.addRow(self._body)

		self._widget.setLayout(layout)

		# Active ou non le groupe
		self.active = self._active

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
	def widget(self) -> QWidget:
		"""Retourne le calque associé à ce groupe de paramètres (:class:`QWidget`)."""
		return self._widget

	##################################################
	@property
	def active(self) -> bool:
		"""État du groupe, activé ou non (:class:`bool`)."""
		return self._active

	##################################################
	@active.setter
	def active(self, value: bool):
		"""Contrôle la modification de l'état actif."""
		if self._checkbox is not None and self.is_valid(self._checkbox): self._checkbox.setChecked(value)
		self.toggle_active(1 if value else 0)

	##################################################
	@property
	def value(self):
		"""Fonction vide nécessaire aux parcours automatiques."""
		return

	##################################################
	@value.setter
	def value(self, value: Any):
		"""Fonction vide nécessaire aux parcours automatiques."""
		return

	##################################################
	@property
	def settings_names(self) -> list[str]:
		"""Récupère les noms des paramètres de ce groupe."""
		return list(self._settings.keys())

	##################################################
	@property
	def settings(self) -> dict[str, Any]:
		"""Récupère les valeurs des paramètres."""
		res = {key: setting.value for key, setting in self._settings.items()}
		for group in self._inner_groups:
			setting_group = cast(BaseSettingGroup, self._settings[group])
			res.pop(group, None)  # Supprime la clé si elle existe
			tmp = {f"{group} {key}": value for key, value in setting_group.settings.items()}
			res = {**res, **tmp}  # Fusionne les dictionnaires
		return res

	##################################################
	def __getitem__(self, key: str) -> Union["BaseSettingGroup", BaseSettingType]:
		"""Surcharge de l'opérateur []"""
		return self._settings[key]

	##################################################
	# def __setitem__(self, key: str, value: Union["BaseSettingGroup", BaseSettingType]):
	# 	"""Surcharge pour assigner une valeur avec []"""
	# 	self._settings[key] = value

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
	@staticmethod
	def is_valid(obj: object):
		"""Vérifie qu'un objet est toujours valide et non supprimé."""
		return obj is not None and ((_IS_PYQT and not sip.isdeleted(obj)) or (not _IS_PYQT and shiboken6.isValid(obj)))

	##################################################
	@staticmethod
	def _find_form_row_of_widget(form: QFormLayout, w: QWidget) -> int:  # pragma: no cover —  lié aux étrangetés de QT Python
		"""Retourne l'index de ligne contenant le widget `w`, ou -1 si absent."""
		for r in range(form.rowCount()):
			for role in (QFormLayout.ItemRole.LabelRole, QFormLayout.ItemRole.FieldRole, QFormLayout.ItemRole.SpanningRole):
				item = form.itemAt(r, role)
				if item is not None and item.widget() is w:
					return r
		return -1

	##################################################
	def hide(self):
		"""Cache le widget."""
		self._widget.hide()

	##################################################
	def show(self):
		"""Affiche le widget."""
		self._widget.show()

	##################################################
	def toggle_active(self, state: int):
		"""Mets à jour l'état actif du groupe lorsque la checkbox est modifiée."""
		self._active = bool(state)
		self._body.show() if self._active else self._body.hide()

	##################################################
	def always_active(self):
		"""Active toujours le groupe et supprime la checkbox de l'interface."""
		# Appeler la méthode active pour forcer l'état actif
		self.active = True
		# Supprimer la checkbox et réorganiser le layout
		cb = getattr(self, "_checkbox", None)
		if self.is_valid(cb):
			try:
				self._header.layout().removeWidget(cb)  # Retirer la checkbox du layout
				cb.setParent(None)
				cb.deleteLater()
			except RuntimeError: pass
			self._checkbox = None

	##################################################
	def remove_header(self):
		"""Active toujours le groupe et supprime la partie header de l'interface."""
		self.always_active()
		# Suppression du titre
		tit = getattr(self, "_title", None)
		hdr = getattr(self, "_header", None)
		if self.is_valid(hdr) and self.is_valid(tit):
			try:
				if hdr.layout() is not None: hdr.layout().removeWidget(tit)  # Retirer le titre du layout
				tit.setParent(None)  # .									   Supprime la parenté
				tit.deleteLater()  # .										   Détruire le titre
			except RuntimeError: pass  # .									   Si déjà retirée
			self._title = None

		# Suppression du header
		if self.is_valid(hdr) and self.is_valid(self._widget):
			try:
				layout = cast(QFormLayout, self._widget.layout())  # .		   Récupérer le layout principal (QFormLayout)
				row = self._find_form_row_of_widget(layout, hdr)  # .		   Récupération de la ligne
				if row >= 0: layout.removeRow(row)  # .						   Suppression sûre
				hdr.setParent(None)  # .									   Supprime la parenté
				hdr.deleteLater()  # .										   Détruire le titre
			except RuntimeError: pass  # .									   Si déjà retirée
			self._header = None

		# Suppression de la marge
		body_layout = cast(QFormLayout, self._body.layout())  # .			   Récupérer le layout du widget _body
		body_layout.setContentsMargins(0, 0, 0, 0)

	# ==================================================
	# endregion Hide and Seek
	# ==================================================

	# ==================================================
	# region Parsing
	# ==================================================
	##################################################
	def to_dict(self) -> dict[str, Any]:
		"""Renvoie un dictionnaire contenant toutes les informations de la classe."""
		return {"type":     type(self).__name__, "active": self._active, "label": self.label,
				"settings": {name: setting.to_dict() for name, setting in self._settings.items()}, }

	##################################################
	@classmethod
	def from_dict(cls, data: dict[str, Any]) -> "BaseSettingGroup":
		"""Créé une instance de la classe à partir d'un dictionnaire."""
		res = cls()  # Instancie la classe appelée
		res.update_from_dict(data)
		return res

	##################################################
	def update_from_dict(self, data: dict[str, Any]):
		"""Mets à jour la classe à partir d'un dictionnaire."""
		self.label = data.get("label", self.label)
		self.active = data.get("active", False)
		settings = data["settings"]
		for key, value in self.setting_list.items():  # Appelle `update_from_dict` pour chaque élément de setting_list
			if key in settings: self._settings[key].update_from_dict(settings[key])

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
			else: msg += f"{line_prefix}- {key} : {setting.value}\n"
		return msg

	##################################################
	def __str__(self) -> str: return self.tostring()

	# ==================================================
	# endregion Parsing
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
	def disconnect(self, f: Optional[Callable[[Any], None]] = None):
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
