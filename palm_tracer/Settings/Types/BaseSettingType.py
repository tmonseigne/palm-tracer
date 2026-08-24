"""Définit la classe de base commune aux types de paramètres."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, cast, Optional

from qtpy.QtWidgets import QFormLayout, QPushButton

from palm_tracer.Settings.Types.BaseUIType import BaseUIType
from palm_tracer.Settings.Types.SignalWrapper import SignalWrapper


##################################################
@dataclass
class BaseSettingType:
	"""
	Classe mère abstraite pour la gestion des paramètres dans l'interface utilisateur.

	Cette classe représente un paramètre d'interface utilisateur avec un calque spécifique.
	Elle est utilisée comme	base pour des paramètres plus spécifiques.
	Chaque paramètre pourra hériter de cette classe pour définir son comportement et ses options spécifiques.

	:param label: Nom du paramètre à afficher.
	:param tooltip: Description détaillée en overlay.
	"""

	label: str = ""
	"""Nom du paramètre à afficher (:class:`str`)."""
	tooltip: str = ""
	"""Description détaillée en overlay (:class:`str`)."""
	default: Any = field(init=False, default=None)
	"""Valeur par défaut du paramètre (:class:`str`, :class:`int`, :class:`float`...)."""
	_value: Any = field(init=False, default=None)
	"""Valeur actuelle du paramètre (:class:`str`, :class:`int`, :class:`float`...)."""
	_signal: SignalWrapper = field(init=False, default_factory=lambda: SignalWrapper())
	"""Signal permettant de communiquer avec l'interface."""
	_uis: dict[str, BaseUIType] = field(init=False, default_factory=lambda: dict[str, BaseUIType]())
	"""Dictionnaire des interfaces qui ont été créé pour ce paramètre."""

	# ==================================================
	# region Initialization
	# ==================================================
	##################################################
	def __post_init__(self):
		"""Méthode appelée automatiquement après l'initialisation du dataclass."""
		self.value = self.default

	##################################################
	def reset(self):
		"""Réinitialise le paramètre à sa valeur par défaut."""
		self.value = self.default

	# ==================================================
	# endregion Initialization
	# ==================================================

	# ==================================================
	# region Getter/Setter
	# ==================================================
	##################################################
	def get_ui(self, name: str = "default") -> BaseUIType:
		"""
		Retourne un objet :class:`.BaseUIType`, existant ou le créé si nécessaire.

		:param name: Nom de l'interface dans le dictionnaire.
		:return: Interface du paramètre (:class:`palm_tracer.Settings.Types.BaseUIType.BaseUIType`).
		"""
		raise NotImplementedError("La méthode 'get_ui' doit être implémentée dans la sous-classe.")

	##################################################
	def clean_ui(self, name: str):
		"""
		Supprime l'interface Qt associée au nom donné.

		:param name: Nom de l'interface dans le dictionnaire.
		"""
		self._uis.pop(name, None)

	##################################################
	@property
	def value(self) -> Any:
		"""Valeur actuelle du paramètre (:class:`str`, :class:`int`, :class:`float`...)."""
		return True

	##################################################
	@value.setter
	def value(self, value: Any):
		"""Valeur actuelle du paramètre (:class:`str`, :class:`int`, :class:`float`...)."""
		pass

	##################################################
	def set_value_from_ui(self, value: Any):
		"""Mets à jour la valeur à chaque modification de l'UI (appelle le setter)."""
		self.value = value

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
		return {"value": self.value}

	##################################################
	def update_from_compact_dict(self, data: dict[str, Any]):
		"""Mets à jour la classe à partir d'un dictionnaire minimal."""
		self.value = data["value"]  # Appel du Setter

	# ==================================================
	# endregion Parsing
	# ==================================================

	# ==================================================
	# region Signals
	# ==================================================
	##################################################
	def attach_to_form(self, ui_name: str, form: QFormLayout):
		"""
		Connecte un bouton directement et non le paramètre en lui-même.

		:param ui_name: Nom de l'interface à connecter.
		:param form: Formulaire qui va recevoir le widget.
		"""
		self.get_ui(ui_name).attach_to_form(form)

	##################################################
	def connect_button(self, f: Any, ui_name: str = "default", n: int = 0):
		"""
		Connecte un bouton directement et non le paramètre en lui-même.

		:param f: Fonction ou slot à connecter.
		:param ui_name: Nom de l'interface à connecter.
		:param n: Numéro de la boîte contenant le bouton.
		"""
		b = cast(QPushButton, self.get_ui(ui_name).boxes[n])
		b.clicked.connect(f)

	##################################################
	def connect(self, f: Any):
		"""
		Connecte une fonction ou un slot au signal encapsulé.

		:param f: Fonction ou slot à connecter.
		"""
		self._signal.connect(f)  # Connexion de la fonction fournie au signal.

	##################################################
	def disconnect(self, f: Optional[Any] = None) -> int:
		"""
		Déconnecte `f` si fourni, sinon **tous** les slots. Retourne le nombre de déconnecté.

		:param f: Fonction ou slot à déconnecter.
		:return: Nombre de slots déconnectés.
		"""
		return self._signal.disconnect(f)

	##################################################
	def emit(self, value: Any = None):
		"""
		Émet le signal encapsulé.

		Utilisé pour notifier les parties de l'application abonnées au signal.

		:param value: Valeur à émettre.
		"""
		self._signal.emit(value)  # Émission du signal.

	##################################################
	def signal_blocked(self, emit_last: bool = True) -> SignalWrapper.BlockCtx:
		"""
		Contexte de blocage des signaux de ce paramètre.

		:param emit_last: Si ``True``, émet la dernière valeur à la fin du blocage.
		                  Si ``False``, ignore toutes les émissions reçues pendant le blocage.
		"""
		return self._signal.blocked(emit_last)

	##################################################
	def sync(self, other: "BaseSettingType"):
		"""
		Synchronise ce paramètre avec un autre paramètre.

		Quand ce paramètre change, la valeur est propagée vers ``other``.

		:param other: Autre paramètre à synchroniser.
		"""

		def sync(setting: "BaseSettingType", value: Any):
			with setting.signal_blocked(emit_last=False): setting.value = value

		self.connect(lambda v: sync(other, v))
		other.connect(lambda v: sync(self, v))
