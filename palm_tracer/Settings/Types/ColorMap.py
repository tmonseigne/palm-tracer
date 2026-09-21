"""Définit un paramètre de sélection de colormap avec aperçu."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, ClassVar, cast

import numpy as np
from matplotlib import colormaps
from qtpy.QtCore import QSignalBlocker, QSize
from qtpy.QtGui import QBrush, QColor, QIcon, QLinearGradient, QPainter, QPixmap
from qtpy.QtWidgets import QColorDialog, QComboBox, QPushButton, QWidget

from palm_tracer.Settings.Types.BaseUIType import BaseUIType
from palm_tracer.Settings.Types.Combo import Combo

MAX_UI_8 = np.iinfo(np.uint8).max
MAX_UI_16 = np.iinfo(np.uint16).max


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
	PICKER_ICON_SIZE: ClassVar[QSize] = QSize(32, 14)
	"""Dimensions de l'aperçu affiché sur le bouton du sélecteur de couleur."""
	GRADIENT_STOPS: ClassVar[int] = 32
	"""Nombre de couleurs échantillonnées pour dessiner un aperçu."""
	CUSTOM_LABEL: ClassVar[str] = "Custom"
	"""Préfixe de l'entrée temporaire créée par le sélecteur de couleur."""

	_items: list[str] = field(default_factory=lambda: list(ColorMap.AVAILABLE_MAPS))
	"""Noms des colormaps proposées."""
	_custom_color: QColor | None = field(init=False, default=None, repr=False)
	"""Couleur finale du dégradé personnalisé temporaire."""

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
		button = QPushButton()
		button.setFixedWidth(self.PICKER_ICON_SIZE.width() + 10)
		button.setFlat(True)
		button.setIconSize(self.PICKER_ICON_SIZE)
		button.setToolTip("Select a custom color map from black to the chosen color.")
		button.setIcon(self._create_custom_icon(self._custom_color or QColor("white"), self.PICKER_ICON_SIZE))
		button.clicked.connect(lambda _checked=False, source=button: self._open_color_picker(source))
		ui.boxes.append(button)
		ui.layout.insertWidget(1, button)
		ui.layout.insertSpacing(1, 4)
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
			self._custom_color = None
		for ui in self._uis.values():
			box = cast(QComboBox, ui.boxes[0])
			with QSignalBlocker(box):
				self._populate_box(box)
				box.setCurrentIndex(0)
			self._update_picker_button(ui)
		self.value = 0

	##################################################
	def set_custom_color(self, color: QColor):
		"""
		Crée ou remplace la colormap temporaire allant du noir à la couleur choisie.

		La colormap est ajoutée en dernière position et immédiatement sélectionnée. Une modification ultérieure remplace cette même entrée sans agrandir
		la liste.

		:param color: Couleur finale du dégradé.
		"""
		if not color.isValid(): return

		is_replacement = self._custom_color is not None
		self._custom_color = QColor(color)
		label = f"{self.CUSTOM_LABEL} ({self._custom_color.name()})"
		if is_replacement: self._items[-1] = label
		else: self._items.append(label)

		custom_index = len(self._items) - 1
		already_selected = self.value == custom_index
		for ui in self._uis.values():
			box = cast(QComboBox, ui.boxes[0])
			with QSignalBlocker(box):
				self._populate_box(box)
				box.setCurrentIndex(custom_index)
			self._update_picker_button(ui)

		self.value = custom_index
		if already_selected: self.emit(custom_index)

	##################################################
	def get_lut(self, max_value: int = MAX_UI_16) -> np.ndarray:
		"""
		Construit la table de correspondance RGB de la colormap sélectionnée.

		L'indice zéro reste noir. Les indices suivants échantillonnent uniformément toute la colormap, de sorte que l'indice ``max_value`` corresponde à
		sa dernière couleur.

		:param max_value: Plus grand indice de la table, inclus.
		:return: Table RGB de forme ``(max_value + 1, 3)`` et de type :class:`~numpy.uint8`.
		:raises ValueError: Si ``max_value`` est négatif.
		"""
		if max_value < 0:
			raise ValueError("La valeur maximale de la LUT doit être positive ou nulle.")

		lut = np.zeros((max_value + 1, 3), dtype=np.uint8)
		if max_value == 0: return lut

		positions = np.linspace(0.0, 1.0, max_value, dtype=float)
		if self._custom_color is not None and self.value == len(self._items) - 1:
			final_color = np.array(self._custom_color.getRgb()[:3], dtype=float) / MAX_UI_8
			rgb = positions[:, None] * final_color
		else: rgb = colormaps.get_cmap(self.current_text)(positions, bytes=False)[:, :3]
		lut[1:] = np.rint(rgb * MAX_UI_8).astype(np.uint8)
		return lut

	# ==================================================
	# endregion Accesseurs
	# ==================================================

	# ==================================================
	# region Sérialisation
	# ==================================================
	##################################################
	def to_compact_dict(self) -> dict[str, Any]:
		"""
		Renvoie le paramètre sans inclure la colormap personnalisée temporaire.

		:return: Dictionnaire sérialisable sans la colormap personnalisée temporaire.
		"""
		if self._custom_color is None: return super().to_compact_dict()

		custom_index = len(self._items) - 1
		value = self.default if self.value == custom_index else self.value
		return {"value": value, "items": self._items[:-1]}

	# ==================================================
	# endregion Sérialisation
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
		for index, color_map in enumerate(self._items):
			is_custom = self._custom_color is not None and index == len(self._items) - 1
			icon = self._create_custom_icon(self._custom_color) if is_custom else self._create_icon(color_map)
			box.addItem(icon, color_map)

	##################################################
	def _open_color_picker(self, parent: QWidget):
		"""
		Ouvre le sélecteur Qt et applique la couleur validée.

		:param parent: Widget auquel rattacher la boîte de dialogue.
		"""
		initial_color = self._custom_color or QColor("white")
		color = QColorDialog.getColor(initial_color, parent, "Select Custom Color Map")
		if color.isValid(): self.set_custom_color(color)

	##################################################
	def _update_picker_button(self, ui: BaseUIType):
		"""
		Met à jour l'aperçu du bouton associé à une interface.

		:param ui: Interface contenant le bouton.
		"""
		if len(ui.boxes) < 2: return
		color = self._custom_color or QColor("white")
		cast(QPushButton, ui.boxes[1]).setIcon(self._create_custom_icon(color, self.PICKER_ICON_SIZE))

	##################################################
	@classmethod
	def _create_icon(cls, name: str) -> QIcon:
		"""
		Crée l'icône de dégradé d'une colormap Matplotlib.

		:param name: Nom de la colormap.
		:return: Icône du dégradé, ou icône vide si le nom est inconnu.
		"""
		try:
			color_map = colormaps.get_cmap(name)
		except ValueError:
			return QIcon()

		stops: list[tuple[float, QColor]] = []
		for i in range(cls.GRADIENT_STOPS):
			position = i / (cls.GRADIENT_STOPS - 1)
			red, green, blue, alpha = color_map(position)
			stops.append((position, QColor.fromRgbF(float(red), float(green), float(blue), float(alpha))))
		return cls._create_gradient_icon(stops)

	##################################################
	@classmethod
	def _create_custom_icon(cls, color: QColor, size: QSize | None = None) -> QIcon:
		"""
		Crée l'aperçu d'un dégradé linéaire allant du noir à une couleur.

		:param color: Couleur finale du dégradé.
		:param size: Dimensions de l'icône ; utilise :attr:`ICON_SIZE` par défaut.
		:return: Icône du dégradé.
		"""
		return cls._create_gradient_icon([(0.0, QColor("black")), (1.0, color)], size)

	##################################################
	@classmethod
	def _create_gradient_icon(cls, stops: list[tuple[float, QColor]], size: QSize | None = None) -> QIcon:
		"""
		Dessine une icône à partir de points de couleur ordonnés.

		:param stops: Couples ``(position, couleur)`` avec une position comprise entre zéro et un.
		:param size: Dimensions de l'icône ; utilise :attr:`ICON_SIZE` par défaut.
		:return: Icône du dégradé.
		"""
		icon_size = size or cls.ICON_SIZE
		width, height = icon_size.width(), icon_size.height()
		gradient = QLinearGradient(0, 0, width, 0)
		for position, color in stops:
			gradient.setColorAt(position, color)

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
