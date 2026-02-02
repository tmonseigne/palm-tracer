"""
Fichier contenant la classe :class:`BrowseFile` dérivée de :class:`.BaseSettingType`, qui permet la gestion d'un paramètre type recherche de fichier.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QFileDialog, QLineEdit, QPushButton

from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType


##################################################
@dataclass
class BrowseFile(BaseSettingType):
	"""
	Classe pour un paramètre spécifique de type recherche de fichier.

	Attributs :
		- **label** (:class:`str`) : Nom du paramètre à afficher.
		- **_layout** (:class:`QFormLayout`) : Le calque associé à ce paramètre, initialisé par défaut à un :class:`QFormLayout`.
		- **_signal** (:class:`SignalWrapper`) : Signal permettant de communiquer avec l'interface.
		- **default** (:class:`str`) : Valeur par défaut du paramètre.
		- **value** (:class:`str`) : Valeur actuelle du paramètre.
		- **box** (:class:`QLineEdit`) : Objet QT permettant de manipuler le paramètre.
	"""

	default: str = ""
	value: str = field(init=False, default="")
	_box: QLineEdit = field(init=False, default_factory=lambda: QLineEdit())

	# ==================================================
	# region Initialization
	# ==================================================
	##################################################
	def initialize(self):
		super().initialize()  # .							  Appelle l'initialisation de la classe mère
		self._box.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Définition de l'alignement du calque à gauche.

		browse_button = QPushButton("Choisir un fichier")  # .Ajout d'un bouton pour permettre de choisir le fichier
		browse_button.clicked.connect(self.browse_file)  # .  Connexion du bouton à la méthode de sélection

		# Disposer le QLineEdit et le bouton dans un calque horizontal
		self._layout.addWidget(self._box)  # .				  Ajout du champ de texte
		self._layout.addWidget(browse_button)  # .			  Ajout du bouton de sélection
		self._layout.addStretch(1)  # .						  Pousse tout à gauche, espace vide à droite

	# ==================================================
	# endregion Initialization
	# ==================================================

	# ==================================================
	# region Getter/Setter
	# ==================================================
	##################################################
	def get_value(self) -> str:
		self.value = self._box.text()
		return self.value

	##################################################
	def set_value(self, value: str):
		self.value = value
		self._box.setText(value)

	# ==================================================
	# endregion Getter/Setter
	# ==================================================

	# ==================================================
	# region  Parsing
	# ==================================================
	##################################################
	def to_dict(self) -> dict[str, Any]:
		return {"type": type(self).__name__, "label": self.label, "value": self.value}

	##################################################
	def update_from_dict(self, data: dict[str, Any]):
		self.label = data.get("label", "")
		self.set_value(data.get("value", ""))

	# ==================================================
	# endregion  Parsing
	# ==================================================

	# ==================================================
	# region  Callbacks
	# ==================================================
	##################################################
	def browse_file(self):
		"""Ouvre un dialogue de sélection de fichier et met à jour la boîte avec le chemin sélectionné."""
		current = Path(self.get_value())
		# Si le chemin par défaut n'est pas valide, on utilise le chemin principal du projet
		if not current.exists() or current == Path.cwd(): current = Path.cwd()
		path, _ = QFileDialog.getOpenFileName(self._box, "Sélectionner un fichier", str(current))
		if not path: return
		if Path(path).is_file(): self._box.setText(path)  # Met à jour le chemin dans la boîte de texte
