"""
Fichier contenant la classe :class:`BrowseFile` dérivée de :class:`.BaseSettingType`, qui permet la gestion d'un paramètre type recherche de fichier.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QFileDialog, QLineEdit, QPushButton, QApplication, QStyle
from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType


##################################################
@dataclass
class BrowseFile(BaseSettingType):
	"""
	Classe pour un paramètre spécifique de type recherche de fichier.

	:param label: Nom du paramètre à afficher
	:param tooltip: Description détaillée en overlay.
	:param default: Valeur par défaut du paramètre.
	"""

	default: str = ""
	_value: str = field(init=False, default="")
	_box: QLineEdit = field(init=False, default_factory=lambda: QLineEdit())

	# ==================================================
	# region Initialization
	# ==================================================
	##################################################
	def initialize(self):
		super().initialize()  # .							  Appelle l'initialisation de la classe mère
		self._box.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Définition de l'alignement du calque à gauche.

		browse_button = QPushButton()  # .					  Ajout d'un bouton pour permettre de choisir le fichier
		browse_button.setIcon(QApplication.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon))
		browse_button.clicked.connect(self.browse_file)  # .  Connexion du bouton à la méthode de sélection

		# Disposer le QLineEdit et le bouton dans un calque horizontal
		self._layout.addWidget(self._box)  # .				  Ajout du champ de texte
		self._layout.addWidget(browse_button)  # .			  Ajout du bouton de sélection

	# ==================================================
	# endregion Initialization
	# ==================================================

	# ==================================================
	# region Getter/Setter
	# ==================================================
	##################################################
	@property
	def value(self) -> str:
		"""Valeur actuelle du paramètre (:class:`str`)."""
		self._value = self._box.text()
		return self._value

	##################################################
	@value.setter
	def value(self, value: str):
		"""Valeur actuelle du paramètre (:class:`str`)."""
		self._value = value
		self._box.setText(value)

	# ==================================================
	# endregion Getter/Setter
	# ==================================================

	# ==================================================
	# region  Parsing
	# ==================================================
	##################################################
	def to_dict(self) -> dict[str, Any]:
		return {"type": type(self).__name__, "label": self.label, "value": self._value}

	##################################################
	def update_from_dict(self, data: dict[str, Any]):
		self.label = data.get("label", "")
		self.value = data.get("value", "")

	# ==================================================
	# endregion  Parsing
	# ==================================================

	# ==================================================
	# region  Callbacks
	# ==================================================
	##################################################
	def browse_file(self):
		"""Ouvre un dialogue de sélection de fichiers et mets à jour la boîte avec le chemin sélectionné."""
		current = Path(self.value)
		# Si le chemin par défaut n'est pas valide, on utilise le chemin principal du projet
		if not current.exists() or current == Path.cwd(): current = Path.cwd()
		path, _ = QFileDialog.getOpenFileName(self._box, "Sélectionner un fichier", str(current))
		if not path: return
		if Path(path).is_file(): self._box.setText(path)  # Mets à jour le chemin dans la boîte de texte
