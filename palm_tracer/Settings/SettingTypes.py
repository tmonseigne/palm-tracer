"""
Fichier contenant la classe `BaseSettingType` et ses sous-classes pour la gestion des paramètres d'interface utilisateur.

Ce module définit la classe abstraite `BaseSettingType`, qui sert de base pour la création de différents types de paramètres dans une interface utilisateur Qt.
Les sous-classes permettent de gérer des paramètres spécifiques tels que les entiers, les flottants et les listes déroulantes.
Ces classes sont utilisées pour créer et configurer des widgets de paramètres dans une interface graphique.

**Classes** :

    - Setting : Classe de base pour un paramètre d'interface utilisateur.
    - CheckSetting : Paramètre de type Check box.
    - ComboSetting : Paramètre de type liste déroulante avec options.
    - FileSetting : Paramètre de type ouverture de fichier.
    - FloatSetting : Paramètre de type flottant (float).
    - IntSetting : Paramètre de type entier (integer).
"""

import os
from dataclasses import dataclass, field
from typing import Any

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QCheckBox, QComboBox, QDoubleSpinBox, QFileDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpinBox


# ==================================================
# region Base Setting
# ==================================================
@dataclass
class BaseSettingType:
	"""
	Classe mère abstraite pour la gestion des paramètres dans l'interface utilisateur.

	Cette classe représente un paramètre d'interface utilisateur avec un calque spécifique. Elle est utilisée comme
	base pour des paramètres plus spécifiques. Chaque paramètre pourra hériter de cette classe pour définir son
	comportement et ses options spécifiques.

	Attributs :
			- **label (str)** : Nom du paramètre.
			- **_layout (QHBoxLayout)** : Le calque associé à ce paramètre, initialisé par défaut à un QHBoxLayout.
	"""

	label: str = ""
	_layout: QFormLayout = field(init=False)

	##################################################
	def __post_init__(self):
		"""Méthode appelée automatiquement après l'initialisation du dataclass."""
		self.initialize()

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

	##################################################
	def to_dict(self) -> dict[str, Any]:
		"""Renvoie un dictionnaire contenant toutes les informations de la classe."""
		raise NotImplementedError("La méthode 'to_dict' doit être implémentée dans la sous-classe.")

	##################################################
	@classmethod
	def from_dict(cls, data: dict[str, Any]) -> "BaseSettingType":
		"""Créé une instance de la classe à partir d'un dictionnaire."""
		raise NotImplementedError("La méthode 'from_dict' doit être implémentée dans la sous-classe.")

	##################################################
	def initialize(self):
		"""Initialise le paramètre."""
		self._layout = QFormLayout(None)
		self._layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Définir l'alignement du calque à gauche.

	##################################################
	def reset(self):
		"""Réinitialise le paramètre à sa valeur par défaut."""
		raise NotImplementedError("La méthode 'reset' doit être implémentée dans la sous-classe.")

	##################################################
	def add_row(self, box):
		"""
		Ajoute la ligne avec le label et l'input

		:param box: Input box à ajouter
		"""
		self._layout.addRow(QLabel(self.label + " : "), box)  # Ajoute le setting.


# ==================================================
# endregion Base Setting
# ==================================================


# ==================================================
# region Setting Int
# ==================================================
@dataclass
class IntSetting(BaseSettingType):
	"""Classe pour un paramètre spécifique de type SpinBox Entier."""

	default: int = 0
	min: int = 0
	max: int = 100
	step: int = 1
	value: int = field(init=False, default=0)
	box: QSpinBox = field(init=False)

	##################################################
	def get_value(self) -> int:
		self.value = self.box.value()
		return self.value

	##################################################
	def set_value(self, value: int):
		self.value = value
		self.box.setValue(value)

	##################################################
	def to_dict(self) -> dict[str, Any]:
		return {"type": type(self).__name__, "label": self.label, "default": self.default,
				"min":  self.min, "max": self.max, "step": self.step, "value": self.value}

	##################################################
	@classmethod
	def from_dict(cls, data: dict[str, Any]) -> "IntSetting":
		res = cls(data.get("label", ""), data.get("default", 0), data.get("min", 0), data.get("max", 100), data.get("step", 1))
		res.set_value(data.get("value", 0))
		return res

	##################################################
	def initialize(self):
		super().initialize()									# Appelle l'initialisation de la classe mère.
		self.box = QSpinBox(None)								# Création de la boite.
		self.box.setAlignment(Qt.AlignmentFlag.AlignLeft)		# Définir l'alignement du calque à gauche.
		self.box.setRange(self.min, self.max)					# Définition du min, max.
		self.box.setSingleStep(self.step)						# Définition du pas à chaque appuie sur une flèche.
		self.set_value(self.default)							# Définition de la valeur.
		self.add_row(self.box)									# Ajoute le spin au calque.

	##################################################
	def reset(self): self.set_value(self.default)


# ==================================================
# endregion Setting Int
# ==================================================

# ==================================================
# region Setting Float
# ==================================================
@dataclass
class FloatSetting(BaseSettingType):
	""" Classe pour un paramètre spécifique de type SpinBox réel. """
	default: float = 0.0
	min: float = 0.0
	max: float = 100.0
	step: float = 1.0
	precision: int = 2
	value: float = field(init=False, default=0.0)
	box: QDoubleSpinBox = field(init=False)

	##################################################
	def get_value(self) -> float:
		self.value = self.box.value()
		return self.value

	##################################################
	def set_value(self, value: float):
		self.value = value
		self.box.setValue(value)

	##################################################
	def to_dict(self) -> dict[str, Any]:
		return {"type":  type(self).__name__, "label": self.label, "default": self.default,
				"min":   self.min, "max": self.max, "step": self.step, "precision": self.precision,
				"value": self.value}

	##################################################
	@classmethod
	def from_dict(cls, data: dict[str, Any]) -> "FloatSetting":
		res = cls(data.get("label", ""), data.get("default", 0.0),
				  data.get("min", 0.0), data.get("max", 100.0),
				  data.get("step", 1.0), data.get("precision", 2))
		res.set_value(data.get("value", 0.0))
		return res

	##################################################
	def initialize(self):
		super().initialize()							   # Appelle l'initialisation de la classe mère.
		self.box = QDoubleSpinBox(None)					   # Création de la boite.
		self.box.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Définir l'alignement du calque à gauche.
		self.box.setRange(self.min, self.max)			   # Définition du min, max.
		self.box.setSingleStep(self.step)	 			   # Définition du pas à chaque appuie sur une flèche.
		self.box.setDecimals(self.precision) 			   # Définition de la précision à afficher.
		self.set_value(self.default)		 			   # Définition de la valeur.
		self.add_row(self.box)				 			   # Ajoute le spin au calque.

	##################################################
	def reset(self): self.set_value(self.default)


# ==================================================
# endregion Setting Float
# ==================================================


# ==================================================
# region Setting Check Box
# ==================================================
@dataclass
class CheckSetting(BaseSettingType):
	"""Classe pour un paramètre spécifique de type CheckBox."""

	default: bool = False
	value: bool = field(init=False, default=False)
	box: QCheckBox = field(init=False, default_factory=QCheckBox)

	##################################################
	def get_value(self) -> bool:
		if self.box.checkState() == Qt.CheckState.Unchecked: self.value = False
		else: self.value = True
		return self.value

	##################################################
	def set_value(self, value: bool):
		self.value = value
		if value: self.box.setCheckState(Qt.CheckState.Checked)
		else:     self.box.setCheckState(Qt.CheckState.Unchecked)

	##################################################
	def to_dict(self) -> dict[str, Any]:
		return {"type": type(self).__name__, "label": self.label, "default": self.default, "value": self.value}

	##################################################
	@classmethod
	def from_dict(cls, data: dict[str, Any]) -> "CheckSetting":
		res = cls(data.get("label", ""), data.get("default", False))
		res.set_value(data.get("value", False))
		return res

	##################################################
	def initialize(self):
		super().initialize()		  # Appelle l'initialisation de la classe mère.
		self.box = QCheckBox()		  # Création de la boite.
		self.set_value(self.default)  # Définition de la valeur.
		self.add_row(self.box)		  # Ajoute la check box au calque.

	##################################################
	def reset(self): self.set_value(self.default)


# ==================================================
# endregion Setting Check Box
# ==================================================


# ==================================================
# region Setting List
# ==================================================
@dataclass
class ComboSetting(BaseSettingType):
	"""Classe pour un paramètre spécifique de type Liste déroulante."""

	choices: list[str] = field(default_factory=lambda: [""])
	value: int = field(init=False, default=0)
	box: QComboBox = field(init=False)

	##################################################
	def get_value(self) -> int:
		self.value = self.box.currentIndex()
		return self.value

	##################################################
	def set_value(self, value: int):
		self.value = value
		self.box.setCurrentIndex(value)

	##################################################
	def to_dict(self) -> dict[str, Any]:
		return {"type": type(self).__name__, "label": self.label, "choices": self.choices, "value": self.value}

	##################################################
	@classmethod
	def from_dict(cls, data: dict[str, Any]) -> "ComboSetting":
		res = cls(data.get("label", ""), data.get("choices", [""]))
		res.set_value(data.get("value", 0))
		return res

	##################################################
	def initialize(self):
		super().initialize()  			 # Appelle l'initialisation de la classe mère.
		self.box = QComboBox(None)		 # Création de la boite.
		self.box.setFixedWidth(150)		 # Réduire la largeur de la boite.
		self.box.addItems(self.choices)  # Ajout des choix possibles.
		self.set_value(0)		 		 # Définition de la valeur.
		self.add_row(self.box)			 # Ajoute la liste déroulante au calque.

	##################################################
	def reset(self): self.set_value(0)


# ==================================================
# endregion Setting List
# ==================================================


# ==================================================
# region Setting File
# ==================================================
@dataclass
class FileSetting(BaseSettingType):
	"""Classe pour un paramètre spécifique de type Ouverture de fichier."""

	value: str = field(init=False, default="")
	box: QLineEdit = field(init=False)  # Boîte de texte pour afficher le chemin

	##################################################
	def get_value(self) -> str:
		self.value = self.box.text()
		return self.value

	##################################################
	def set_value(self, value: str):
		self.value = value
		self.box.setText(value)

	##################################################
	def to_dict(self) -> dict[str, Any]:
		return {"type": type(self).__name__, "label": self.label, "value": self.value}

	##################################################
	@classmethod
	def from_dict(cls, data: dict[str, Any]) -> "FileSetting":
		res = cls(data.get("label", ""))
		res.set_value(data.get("value", ""))
		return res

	##################################################
	def initialize(self):
		super().initialize()							   # Appelle l'initialisation de la classe mère
		self.box = QLineEdit()							   # Création de la boite.
		self.box.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Définir l'alignement du calque à gauche.

		# Ajouter un bouton à côté pour permettre de choisir le fichier
		browse_button = QPushButton("Choisir un fichier")
		browse_button.clicked.connect(self.browse_file)	   # Connecter le bouton à la méthode de sélection

		# Disposer le QLineEdit et le bouton dans un calque horizontal
		layout = QHBoxLayout()							   # Création d'un calque intermédiaire comprenant le champ de texte et le bouton de sélection.
		layout.setAlignment(Qt.AlignmentFlag.AlignLeft)	   # Définir l'alignement du calque à gauche.
		layout.addWidget(self.box)						   # Ajout du champ de texte
		layout.addWidget(browse_button)					   # Ajout du bouton de sélection

		self.add_row(layout)							   # Ajouter au calque principal du setting.

	##################################################
	def browse_file(self):  # pragma: no cover
		"""Ouvre un dialogue de sélection de fichier et met à jour la boîte avec le chemin sélectionné."""
		current = self.get_value()
		# Si le chemin par défaut n'est pas valide, on utilise le chemin principal du projet
		if not os.path.exists(current) or current == "": current = os.getcwd()
		path, _ = QFileDialog.getOpenFileName(self.box, "Sélectionner un fichier", current)
		if path: self.box.setText(path)  # Met à jour le chemin dans la boîte de texte

	##################################################
	def reset(self): self.set_value("")


# ==================================================
# endregion Setting File
# ==================================================


def create_setting(data: dict[str, Any]) -> "BaseSettingType":
	""" Créé un setting en fonction d'un dictionnaire en entrée. """
	if not "type" in data: raise ValueError("Le dictionnaire ne contient pas la clé 'type'.")
	if data["type"] == "IntSetting": return IntSetting.from_dict(data)
	elif data["type"] == "FloatSetting": return FloatSetting.from_dict(data)
	elif data["type"] == "CheckSetting": return CheckSetting.from_dict(data)
	elif data["type"] == "ComboSetting": return ComboSetting.from_dict(data)
	elif data["type"] == "FileSetting": return FileSetting.from_dict(data)
	raise ValueError("Le dictionnaire ne contient pas un type de paramètre valide.")
