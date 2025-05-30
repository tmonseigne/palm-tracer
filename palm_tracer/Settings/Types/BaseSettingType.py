"""
Fichier contenant la classe :class:`BaseSettingType` et ses sous-classes pour la gestion des paramètres d'interface utilisateur.

Ce module définit la classe abstraite :class:`BaseSettingType`, qui sert de base pour la création de différents types de paramètres dans une interface utilisateur Qt.
Les sous-classes permettent de gérer des paramètres spécifiques tels que les entiers, les flottants et les listes déroulantes.
Ces classes sont utilisées pour créer et configurer des widgets de paramètres dans une interface graphique.
"""

from dataclasses import dataclass, field
from typing import Any

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QFormLayout, QLabel

from palm_tracer.Settings.Types.SignalWrapper import SignalWrapper


##################################################
@dataclass
class BaseSettingType:
	"""
	Classe mère abstraite pour la gestion des paramètres dans l'interface utilisateur.

	Cette classe représente un paramètre d'interface utilisateur avec un calque spécifique. Elle est utilisée comme
	base pour des paramètres plus spécifiques. Chaque paramètre pourra hériter de cette classe pour définir son
	comportement et ses options spécifiques.

	Attributs :
			- **label (str)** : Nom du paramètre à afficher.
			- **_layout (QFormLayout)** : Le calque associé à ce paramètre, initialisé par défaut à un QFormLayout.
			- **_signal (SignalWrapper)** : Signal permettant de communiquer avec l'interface.
	"""

	label: str = ""
	"""Nom du paramètre à afficher."""
	_layout: QFormLayout = field(init=False)
	"""Calque principal."""
	_signal: SignalWrapper = field(init=False, default_factory=SignalWrapper)
	"""Signal permettant de communiquer avec l'interface."""

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
		self._layout = QFormLayout(None)
		self._layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Définir l'alignement du calque à gauche.

	##################################################
	def reset(self):
		"""Réinitialise le paramètre à sa valeur par défaut."""
		raise NotImplementedError("La méthode 'reset' doit être implémentée dans la sous-classe.")

	# ==================================================
	# endregion Initialization
	# ==================================================

	# ==================================================
	# region Getter/Setter
	# ==================================================
	##################################################
	@property
	def layout(self) -> QFormLayout:
		"""
		Retourne le calque associé à ce paramètre.

		Cette méthode permet d'accéder au calque pour intégrer le paramètre dans l'interface utilisateur.

		:return: Le calque associé à ce paramètre.
		"""
		return self._layout

	##################################################
	def get_value(self) -> Any:
		"""
		Retourne la valeur du paramètre.

		Cette méthode permet d'accéder à la valeur du paramètre pour la récupérer dans l'interface utilisateur.

		:return: La valeur associée à ce paramètre.
		"""
		raise NotImplementedError("La méthode 'get_value' doit être implémentée dans la sous-classe.")

	##################################################
	def set_value(self, value: Any):
		"""Appliquer la valeur au paramètre"""
		raise NotImplementedError("La méthode 'set_value' doit être implémentée dans la sous-classe.")

	# ==================================================
	# endregion Getter/Setter
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
		""" Met à jour la classe à partir d'un dictionnaire."""
		raise NotImplementedError("La méthode 'update_from_dict' doit être implémentée dans la sous-classe.")

	# ==================================================
	# endregion Parsing
	# ==================================================

	# ==================================================
	# region Manipulation
	# ==================================================
	##################################################
	def add_row(self, box):
		"""
		Ajoute la ligne avec le label et l'input

		:param box: Input box à ajouter
		"""
		self._layout.addRow(QLabel(self.label + " : "), box)  # Ajoute le setting.

	##################################################
	def connect(self, f: Any):
		"""
		Connecte une fonction ou un slot au signal encapsulé.

		:param f: Fonction ou slot à connecter.
		"""
		self._signal.connect(f)  # Connexion de la fonction fournie au signal.

	##################################################
	def emit(self, value: Any = None):
		"""
		Émet le signal encapsulé.

		Utilisé pour notifier les parties de l'application abonnées au signal.
		"""
		self._signal.emit(value)  # Émission du signal.

# ==================================================
# endregion Manipulation
# ==================================================
