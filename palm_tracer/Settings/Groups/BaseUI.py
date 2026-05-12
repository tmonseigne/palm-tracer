"""
Fichier contenant la classe :class:`BaseUI`.

Ce module définit une classe de base pour la représentation graphique d'un paramètre dans l'interface utilisateur Qt.

Cette classe est utilisée comme conteneur des éléments Qt associés à une vue spécifique d'un :class:`BaseSettingType`.

Elle permet de gérer indépendamment plusieurs instances d'interface (multi-vues) pour un même modèle de données (pattern MVC simplifié).

Chaque instance de :class:`BaseUI` correspond à une **vue unique** d'un setting, et contient tous les objets Qt nécessaires à son affichage et son interaction.

Cette séparation permet :
    - de dupliquer facilement l'interface sans dupliquer les données,
    - de synchroniser automatiquement toutes les vues,
    - de simplifier la gestion du cycle de vie des widgets Qt.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from qtpy.QtWidgets import QCheckBox, QFormLayout, QLabel, QVBoxLayout, QWidget

from palm_tracer.Tools import Ui


##################################################
@dataclass
class BaseUI:
	"""
	Classe de base représentant une vue Qt associée à un setting.

	Cette classe encapsule tous les objets Qt nécessaires à l'affichage d'un paramètre dans une interface utilisateur.

	Elle est conçue pour être instanciée plusieurs fois pour un même setting, afin de permettre la duplication d'interface (multi-fenêtres, preview, etc.).

	Chaque instance est indépendante en termes de widgets Qt, mais synchronisée avec le modèle de données auquel elle est associée.
	"""

	name: str
	"""Nom du groupe."""
	mode: int
	"""Méthode de construction de l'interface."""
	layout: QFormLayout = field(init=False)
	"""Calque principal."""
	widget: QWidget = field(init=False)
	"""Widget principal du groupe."""
	checkbox: QCheckBox | None = field(init=False, default=None)
	"""Case à cocher pour activer ou non le groupe (:class:`QCheckBox`)."""
	_body: QWidget = field(init=False)
	"""Corps du groupe encapsulé dans un QWidget pour avoir un Hide/Show disponible (:class:`QWidget`)."""
	body_layout: QFormLayout = field(init=False)
	"""Calque du corps du groupe."""

	##################################################
	def __post_init__(self):
		"""Méthode appelée automatiquement après l'initialisation du dataclass."""
		header = None
		self.checkbox = None
		if self.mode == 0:  # Classique avec un titre et une checkbox pour activer/desactiver le groupe
			self.checkbox = QCheckBox()
			self.checkbox.stateChanged.connect(self.active)  # Connecte le changement de valeur pour que les autres UI se mettent à jour

		if self.mode <= 1:  # La check box n'est pas présente et le groupe est toujours actif avec un titre
			title = QLabel(self.name)
			title.setStyleSheet("font-weight: bold;")  # Style pour le label de titre
			header = QFormLayout(None)
			if self.checkbox is not None: header.addRow(self.checkbox, title)
			else: header.addRow(title)

		# Base
		self.widget = QWidget()
		self.layout = Ui.make_form(self.widget)
		self.widget.setLayout(self.layout)
		if header is not None: self.layout.addRow(header)

		self._body = QWidget()
		self.body_layout = QFormLayout(self._body)
		self.body_layout.setContentsMargins(5, 0, 0, 0)  # Léger décalage.
		self.layout.addRow(self._body)
		self.widget.setLayout(self.layout)

	# ==================================================
	# region Layout management
	# ==================================================
	##################################################
	def attach_to_form(self, form: QFormLayout):
		"""
		Ajoute le groupe à un formulaire

		:param form: :class:`QFormLayout` dans lequel va être inséré le paramètre.
		"""
		form.addRow(self.layout)

	##################################################
	def hide(self):
		"""Cache le groupe de paramètres."""
		self.widget.hide()

	##################################################
	def show(self):
		"""Affiche le groupe de paramètres."""
		self.widget.show()

	##################################################
	def active(self, state: bool):
		"""
		Affiche ou cache le corps du groupe

		:param state: Statut
		"""
		self._body.show() if state else self._body.hide()

# ==================================================
# region Layout management
# ==================================================
