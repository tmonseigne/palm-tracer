"""Définit la représentation Qt d'un type de paramètre."""

from __future__ import annotations

from dataclasses import dataclass, field

from qtpy.QtWidgets import QFormLayout, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from palm_tracer.Tools import Ui


##################################################
@dataclass
class BaseUIType:
	"""
	Représente une vue Qt associée à un paramètre configurable.

	Chaque vue conserve ses propres widgets, sa disposition et sa position éventuelle dans un formulaire.

	:param layout: Disposition contenant les widgets du paramètre.
	:param boxes: Widgets interactifs synchronisés avec le modèle.
	:param label: Libellé Qt associé au paramètre, s'il existe.
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
			if self.label is not None: self.label.hide()
			for b in self.boxes: b.hide()

	##################################################
	def show(self):
		"""Affiche le paramètre."""
		if self.form is not None and self.row >= 0: self.form.setRowVisible(self.row, True)
		else:  # fallback si pas attaché
			if self.label is not None: self.label.show()
			for b in self.boxes: b.show()

	##################################################
	def set_tooltip(self, tooltip: str):
		"""
		Ajoute un tooltip au Label.

		:param tooltip: Tooltip à ajouter.
		"""
		if self.label is not None: self.label.setToolTip(tooltip)
