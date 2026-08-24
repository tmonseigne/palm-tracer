"""Définit un paramètre entier représenté par une boîte de sélection numérique."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import cast

from qtpy.QtCore import QSignalBlocker
from qtpy.QtWidgets import QHBoxLayout, QLabel, QSpinBox

from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType
from palm_tracer.Settings.Types.BaseUIType import BaseUIType
from palm_tracer.Tools import Ui


##################################################
@dataclass
class SpinInt(BaseSettingType):
	"""Représente un entier avec une boîte de sélection numérique.

	:param label: Libellé affiché dans l'interface.
	:param tooltip: Description affichée dans l'infobulle.
	:param default: Valeur par défaut.
	:param limits: Bornes minimale et maximale autorisées.
	:param step: Incrément appliqué par la boîte de sélection numérique.
	"""

	default: int = 0
	"""Valeur par défaut du paramètre (:class:`int`)."""
	_value: int = field(init=False, default=0)
	"""Valeur actuelle du paramètre (:class:`int`)."""

	limits: list[int] = field(default_factory=lambda: [0, 100])
	"""Valeurs limites du paramètre."""
	step: int = 1
	"""Pas à chaque appui sur une des flèches du paramètre."""

	# ==================================================
	# region Getter/Setter
	# ==================================================
	##################################################
	def get_ui(self, name: str = "default") -> BaseUIType:
		if name in self._uis: return self._uis[name]

		box: QSpinBox = Ui.make_spin(None, minimum=self.limits[0], maximum=self.limits[1], step=self.step, value=self.value)
		ui = BaseUIType(layout=QHBoxLayout(), label=QLabel(self.label), boxes=[box])
		ui.set_tooltip(self.tooltip)  # .					Ajout du Tooltip

		box.setKeyboardTracking(False)  # .					Empèche la mise à jour à chaque appuie clavier (attend la fin de l'édition)
		box.valueChanged.connect(self.set_value_from_ui)  # Connecte le changement de valeur pour que les autres UI se mettent à jour

		ui.layout.addWidget(box)  # .						Ajout du champ de texte.
		ui.layout.addStretch(1)  # .						Pousse tout à gauche, espace vide à droite.

		self._uis[name] = ui  # .							Ajoute l'ui au dictionnaire
		return ui

	##################################################
	@property
	def value(self) -> int:
		"""Valeur actuelle du paramètre (:class:`int`)."""
		return self._value

	##################################################
	@value.setter
	def value(self, value: int):
		"""Valeur actuelle du paramètre (:class:`int`)."""
		if self._value == value: return
		self._value = value
		for ui in self._uis.values():
			b = cast(QSpinBox, ui.boxes[0])
			with QSignalBlocker(b): b.setValue(value)

		self.emit(value)


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QWidget, QFormLayout, QPushButton

	app = QApplication(sys.argv)
	w = QWidget()
	form = QFormLayout(w)  # crée et assigne le layout au widget
	setting = SpinInt("Test", "tooltip")
	setting.get_ui("default").attach_to_form(form)
	setting.get_ui("second").attach_to_form(form)
	counter = 0


	def add_setting_ui():
		global counter
		counter += 1
		name = f"dynamic_{counter}"
		setting.get_ui(name).attach_to_form(form)


	button = QPushButton("Ajouter une UI")
	button.clicked.connect(add_setting_ui)
	form.addRow(button)
	w.show()
	sys.exit(app.exec_())
