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

from dataclasses import dataclass

from qtpy.QtWidgets import QFormLayout, QHBoxLayout, QLabel, QVBoxLayout, QWidget


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
	"""Calque principal."""
	label: QLabel
	"""Widget associé au label."""
	boxes: list[QWidget]
	"""Objet QT permettant de manipuler le paramètre."""
	form: QFormLayout | None = None
	"""Formulaire parent dans lequel est le paramètre (utile lors d'un Hide & Seek)."""
	row: int = -1
	"""Position dans le formulaire parent (utile lors d'un Hide & Seek)."""

	# ==================================================
	# region Layout management
	# ==================================================
	##################################################
	def attach_to_form(self, form: QFormLayout):
		"""
		Enregistre le QFormLayout et la position dans le formulaire pour permettre un show/hide propre.

		:param form: :class:`QFormLayout` dans lequel va être inséré le paramètre.
		"""
		self.form = form
		self.row = form.rowCount()  # rowCount() avant addRow = index de la nouvelle ligne
		form.addRow(self.label, self.layout)

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

# ==================================================
# region Layout management
# ==================================================
