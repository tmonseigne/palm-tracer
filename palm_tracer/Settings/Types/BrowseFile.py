"""
Fichier contenant la classe :class:`BrowseFile` dérivée de :class:`.BaseSettingType`, qui permet la gestion d'un paramètre type recherche de fichier.
"""

import os
from dataclasses import dataclass, field
from typing import Any

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QFileDialog, QHBoxLayout, QLineEdit, QPushButton

from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType


##################################################
@dataclass
class BrowseFile(BaseSettingType):
	"""
	Classe pour un paramètre spécifique de type recherche de fichier.

	Attributs :
			- **label (str)** : Nom du paramètre à afficher.
			- **_layout (QFormLayout)** : Le calque associé à ce paramètre, initialisé par défaut à un QFormLayout.
			- **default (str)** : Valeur par défaut du paramètre.
			- **value (str)** : Valeur actuelle du paramètre.
			- **box (QLineEdit)** : Objet QT permettant de manipuler le paramètre.
	"""

	default: str = ""
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
		self.emit(value)

	##################################################
	def to_dict(self) -> dict[str, Any]:
		return {"type": type(self).__name__, "label": self.label, "value": self.value}

	##################################################
	def update_from_dict(self, data: dict[str, Any]):
		self.label = data.get("label", "")
		self.set_value(data.get("value", ""))

	##################################################
	def initialize(self):
		super().initialize()  # Appelle l'initialisation de la classe mère
		self.box = QLineEdit()  # Création de la boite.
		self.box.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Définition de l'alignement du calque à gauche.

		browse_button = QPushButton("Choisir un fichier")  # Ajout d'un bouton pour permettre de choisir le fichier
		browse_button.clicked.connect(self.browse_file)  # Connexion du bouton à la méthode de sélection

		# Disposer le QLineEdit et le bouton dans un calque horizontal
		layout = QHBoxLayout()  # Création d'un calque intermédiaire comprenant le champ de texte et le bouton de sélection.
		layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Définition de l'alignement du calque à gauche.
		layout.addWidget(self.box)  # Ajout du champ de texte
		layout.addWidget(browse_button)  # Ajout du bouton de sélection

		self.add_row(layout)  # Ajouter au calque principal du setting.

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
