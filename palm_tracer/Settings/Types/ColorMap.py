"""Définit un paramètre de sélection de colormap avec aperçu."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, cast

from matplotlib import colormaps
from qtpy.QtCore import QSignalBlocker, QSize
from qtpy.QtGui import QBrush, QColor, QIcon, QLinearGradient, QPainter, QPixmap
from qtpy.QtWidgets import QComboBox

from palm_tracer.Settings.Types.BaseUIType import BaseUIType
from palm_tracer.Settings.Types.Combo import Combo


##################################################
@dataclass
class ColorMap(Combo):
	"""
	Représente une colormap sélectionnée dans une liste déroulante avec aperçu.

	La liste proposée par défaut centralise les colormaps utilisées par PALM Tracer.
	Chaque entrée valide pour Matplotlib est accompagnée d'une icône représentant son dégradé.

	:param label: Libellé affiché dans l'interface.
	:param tooltip: Description affichée dans l'infobulle.
	:param default: Indice sélectionné par défaut.
	:param _items: Noms des colormaps proposées.
	"""

	AVAILABLE_MAPS: ClassVar[tuple[str, ...]] = ("viridis", "magma", "plasma", "inferno", "cividis", "turbo", "hsv")
	"""Colormaps proposées par défaut."""
	ICON_SIZE: ClassVar[QSize] = QSize(64, 14)
	"""Dimensions de l'aperçu affiché dans la liste."""
	GRADIENT_STOPS: ClassVar[int] = 32
	"""Nombre de couleurs échantillonnées pour dessiner un aperçu."""

	_items: list[str] = field(default_factory=lambda: list(ColorMap.AVAILABLE_MAPS))
	"""Noms des colormaps proposées."""

	# ==================================================
	# region Accesseurs
	# ==================================================
	##################################################
	def get_ui(self, name: str = "default") -> BaseUIType:
		"""
		Renvoie une interface existante ou crée une liste déroulante avec les aperçus.

		:param name: Nom de l'interface dans le dictionnaire.
		:return: Interface du paramètre.
		"""
		if name in self._uis:
			return self._uis[name]

		ui = super().get_ui(name)
		box = cast(QComboBox, ui.boxes[0])
		with QSignalBlocker(box):
			self._populate_box(box)
			box.setCurrentIndex(self.value)
		return ui

	##################################################
	@property
	def items(self) -> list[str]:
		"""Récupère la liste des éléments."""
		return self._items

	##################################################
	@items.setter
	def items(self, items: list[str] | None = None):
		"""
		Met à jour les listes déroulantes et les aperçus associés.

		:param items: Noms des colormaps à proposer. La liste actuelle est réutilisée lorsque la valeur vaut ``None``.
		"""
		if items is not None:
			self._items = items
		for ui in self._uis.values():
			box = cast(QComboBox, ui.boxes[0])
			with QSignalBlocker(box):
				self._populate_box(box)
		self.value = 0

	# ==================================================
	# endregion Accesseurs
	# ==================================================

	# ==================================================
	# region Aperçus
	# ==================================================
	##################################################
	def _populate_box(self, box: QComboBox):
		"""
		Remplit une liste déroulante avec les noms et aperçus des colormaps.

		:param box: Liste déroulante à mettre à jour.
		"""
		box.clear()
		box.setIconSize(self.ICON_SIZE)
		for color_map in self._items:
			box.addItem(self._create_icon(color_map), color_map)

	##################################################
	@classmethod
	def _create_icon(cls, name: str) -> QIcon:
		"""
		Crée l'icône de dégradé d'une colormap Matplotlib.

		:param name: Nom de la colormap.
		:return: Icône du dégradé, ou icône vide si le nom est inconnu.
		"""
		try: color_map = colormaps.get_cmap(name)
		except ValueError: return QIcon()

		width, height = cls.ICON_SIZE.width(), cls.ICON_SIZE.height()
		gradient = QLinearGradient(0, 0, width, 0)
		for i in range(cls.GRADIENT_STOPS):
			position = i / (cls.GRADIENT_STOPS - 1)
			red, green, blue, alpha = color_map(position)
			gradient.setColorAt(position, QColor.fromRgbF(float(red), float(green), float(blue), float(alpha)))

		pixmap = QPixmap(width, height)
		painter = QPainter(pixmap)
		painter.fillRect(pixmap.rect(), QBrush(gradient))
		painter.end()
		return QIcon(pixmap)


##################################################
if __name__ == "__main__":
	import sys

	from qtpy.QtWidgets import QApplication, QFormLayout, QPushButton, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	form = QFormLayout(w)  # Crée et affecte la mise en page au widget
	setting = ColorMap("Test", "tooltip", 0)
	setting.get_ui("default").attach_to_form(form)
	setting.get_ui("second").attach_to_form(form)
	counter = 0


	def add_setting_ui():
		"""Ajoute une nouvelle interface du paramètre au formulaire."""
		global counter
		counter += 1
		name = f"dynamic_{counter}"
		setting.get_ui(name).attach_to_form(form)


	button = QPushButton("Ajouter une UI")
	button.clicked.connect(add_setting_ui)
	form.addRow(button)
	w.show()
	sys.exit(app.exec_())
