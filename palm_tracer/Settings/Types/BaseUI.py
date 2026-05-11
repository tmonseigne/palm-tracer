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

from qtpy.QtWidgets import QFormLayout, QHBoxLayout, QLabel, QVBoxLayout, QWidget

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

	layout: QHBoxLayout | QVBoxLayout
	"""Calque principal (:class:`QVBoxLayout` dans la plupart des cas, :class:`QHBoxLayout` pour des cas particuliers)."""
	boxes: list[QWidget]
	"""Objets QT permettant de manipuler le paramètre (:class:`QCheckBox`, :class:`QSpinBox`, :class:`QComboBox`...)."""
	label: QLabel | None = None
	""":class:`QLabel` contenant le nom du paramètre."""
	form: QFormLayout | None = field(init=False, default=None)
	"""Formulaire parent dans lequel est le paramètre (utile lors d'un Hide & Seek)."""
	row: int = field(init=False, default=-1)
	"""Position dans le formulaire parent (utile lors d'un Hide & Seek)."""

	##################################################
	def __post_init__(self):
		"""Méthode appelée automatiquement après l'initialisation du dataclass."""
		Ui.init_layout(self.layout, 0, 0)  # .				Initialise le layout

	# ==================================================
	# region Layout management
	# ==================================================
	##################################################
	def attach_to_form(self, form: QFormLayout):
		"""
		Enregistre le :class:`QFormLayout` et la position dans le formulaire pour permettre un show/hide propre.

		:param form: :class:`QFormLayout` dans lequel va être inséré le paramètre.
		"""
		self.form = form
		self.row = form.rowCount()  # rowCount() avant addRow = index de la nouvelle ligne
		if self.label is not None: form.addRow(self.label, self.layout)
		else: form.addRow(self.layout)

	##################################################
	def hide(self):
		"""Cache le paramètre."""
		if self.form is not None and self.row >= 0: self.form.setRowVisible(self.row, False)
		else:  # fallback si pas attaché
			self.label.hide()
			for b in self.boxes: b.hide()

	##################################################
	def show(self):
		"""Affiche le paramètre."""
		if self.form is not None and self.row >= 0: self.form.setRowVisible(self.row, True)
		else:  # fallback si pas attaché
			self.label.show()
			for b in self.boxes: b.show()

	##################################################
	def set_tooltip(self, tooltip: str):
		"""
		Ajoute un tooltip au Label.

		:param tooltip: tooltip à ajouter
		"""
		if self.label is not None: self.label.setToolTip(tooltip)
