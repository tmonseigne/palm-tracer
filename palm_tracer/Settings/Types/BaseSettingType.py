"""
Fichier contenant la classe :class:`BaseSettingType` et ses sous-classes pour la gestion des paramètres d'interface utilisateur.

Ce module définit la classe abstraite :class:`BaseSettingType`,
qui sert de base pour la création de différents types de paramètres dans une interface utilisateur Qt.
Les sous-classes permettent de gérer des paramètres spécifiques tels que les entiers, les flottants et les listes déroulantes.
Ces classes sont utilisées pour créer et configurer des widgets de paramètres dans une interface graphique.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from qtpy.QtWidgets import QFormLayout, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from palm_tracer.Settings.Types.SignalWrapper import SignalWrapper
from palm_tracer.Tools import Ui


##################################################
@dataclass
class BaseSettingType:
	"""
	Classe mère abstraite pour la gestion des paramètres dans l'interface utilisateur.

	Cette classe représente un paramètre d'interface utilisateur avec un calque spécifique.
	Elle est utilisée comme	base pour des paramètres plus spécifiques.
	Chaque paramètre pourra hériter de cette classe pour définir son comportement et ses options spécifiques.

	:param label: Nom du paramètre à afficher
	:param tooltip: Description détaillée en overlay.
	"""

	label: str = ""
	"""Nom du paramètre à afficher (:class:`str`)."""
	tooltip: str = ""
	"""Description détaillée en overlay."""
	default: Any = field(init=False, default=None)
	"""Valeur par défaut du paramètre (:class:`str`, :class:`int`, :class:`float`...)."""
	_value: Any = field(init=False, default=None)
	"""Valeur actuelle du paramètre (:class:`str`, :class:`int`, :class:`float`...)."""

	_layout: QHBoxLayout | QVBoxLayout = field(init=False)
	"""Calque principal."""
	_box: QWidget = field(init=False, default_factory=lambda: QWidget())
	"""Objet QT permettant de manipuler le paramètre."""
	_signal: SignalWrapper = field(init=False, default_factory=lambda: SignalWrapper())
	"""Signal permettant de communiquer avec l'interface."""

	# Elements additionnel pour le Hide and Seek
	_label_widget: QLabel = field(init=False)
	"""Widget associé au label."""
	_form_layout: Optional[QFormLayout] = field(init=False, default=None)
	"""Formulaire parent dans lequel est le paramètre."""
	_row_index: int = field(init=False, default=-1)
	"""Position dans le formulaire parent."""

	# ==================================================
	# region Initialization
	# ==================================================
	##################################################
	def __post_init__(self):
		"""Méthode appelée automatiquement après l'initialisation du dataclass."""
		self.initialize()

	##################################################
	def initialize(self):
		"""Initialise le paramètre."""
		self._label_widget = QLabel(self.label)
		if self.tooltip: self._label_widget.setToolTip(self.tooltip)
		self._layout = QHBoxLayout()
		Ui.init_layout(self._layout, 0, 0)

	##################################################
	def attach_to_form(self, form: QFormLayout):
		"""
		Enregistre le QFormLayout et la position dnas le formulaire pour permettre un show/hide propre.

		:param form: :class:`QFormLayout` dans lequel va être inséré le paramètre.
		"""
		self._form_layout = form
		self._row_index = form.rowCount()  # rowCount() avant addRow = index de la nouvelle ligne
		form.addRow(self._label_widget, self.layout)

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
	@property
	def layout(self) -> QHBoxLayout:
		"""Calque principal associé au paramètre."""
		return self._layout

	##################################################
	@property
	def box(self) -> QWidget:
		"""Objet QT permettant de manipuler le paramètre (:class:`QSpinBox`, :class:`QCheckBox`, :class:`QComboBox`...)."""
		return self._box

	##################################################
	@property
	def label_widget(self) -> QLabel:
		"""Objet QT pour le label associé au paramètre."""
		return self._label_widget

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

	# ==================================================
	# endregion Getter/Setter
	# ==================================================

	# ==================================================
	# region Hide and Seek
	# ==================================================
	##################################################
	def hide(self):
		"""Cache le paramètre."""
		if self._form_layout is not None and self._row_index >= 0: self._form_layout.setRowVisible(self._row_index, False)
		else:  # fallback si pas attaché
			self._label_widget.hide()
			self._box.hide()

	##################################################
	def show(self):
		"""Affiche le paramètre."""
		if self._form_layout is not None and self._row_index >= 0: self._form_layout.setRowVisible(self._row_index, True)
		else:  # fallback si pas attaché
			self._label_widget.show()
			self._box.show()

	# ==================================================
	# endregion Hide and Seek
	# ==================================================

	# ==================================================
	# region Parsing
	# ==================================================
	##################################################
	def to_dict(self) -> dict[str, Any]:
		"""Renvoie un dictionnaire contenant toutes les informations de la classe."""
		raise NotImplementedError("La méthode 'to_dict' doit être implémentée dans la sous-classe.")

	##################################################
	@classmethod
	def from_dict(cls, data: dict[str, Any]) -> "BaseSettingType":
		"""Créé une instance de la classe à partir d'un dictionnaire."""
		res = cls(data.get("label", ""))
		res.update_from_dict(data)
		return res

	##################################################
	def update_from_dict(self, data: dict[str, Any]):
		"""Met à jour la classe à partir d'un dictionnaire."""
		raise NotImplementedError("La méthode 'update_from_dict' doit être implémentée dans la sous-classe.")

	# ==================================================
	# endregion Parsing
	# ==================================================

	# ==================================================
	# region Signals
	# ==================================================
	##################################################
	def connect(self, f: Any):
		"""
		Connecte une fonction ou un slot au signal encapsulé.

		:param f: Fonction ou slot à connecter.
		"""
		self._signal.connect(f)  # Connexion de la fonction fournie au signal.

	##################################################
	def disconnect(self, f: Optional[Callable[[Any], None]] = None) -> int:
		"""
		Déconnecte `f` si fourni, sinon **tous** les slots. Retourne le nb déconnectés.

		:param f: Fonction ou slot à déconnecter.
		:return: Nombre de slots déconnectés
		"""
		return self._signal.disconnect(f)

	##################################################
	def emit(self, value: Any = None):
		"""
		Émet le signal encapsulé.

		Utilisé pour notifier les parties de l'application abonnées au signal.

		:param value: Valeur à emettre
		"""
		self._signal.emit(value)  # Émission du signal.

	def signal_blocked(self) -> SignalWrapper.BlockCtx:
		"""Contexte de blocage des signaux de ce paramètre."""
		return self._signal.blocked()
