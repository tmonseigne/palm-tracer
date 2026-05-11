"""
Fichier contenant la classe :class:`Button` dérivée de :class:`.BaseSettingType`, qui permet la gestion d'un paramètre type bouton à cliquer.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, cast

from qtpy.QtWidgets import QHBoxLayout, QPushButton

from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType
from palm_tracer.Settings.Types.BaseUI import BaseUI


##################################################
@dataclass
class Button(BaseSettingType):
	"""
	Classe pour un paramètre spécifique de type bouton à cliquer.

	:param label: Nom du paramètre à afficher
	:param tooltip: Description détaillée en overlay.
	"""

	##################################################
	def reset(self): pass

	##################################################
	def get_ui(self, name: str = "default") -> BaseUI:
		if name in self._uis: return self._uis[name]

		box: QPushButton = QPushButton(self.label)  # Création de la boite.
		ui = BaseUI(layout=QHBoxLayout(), boxes=[box])
		box.setToolTip(self.tooltip)  # .			  Ajout du Tooltip
		ui.layout.addWidget(box)  # .				  Ajout du champ de texte.

		self._uis[name] = ui  # .					  Ajoute l'ui au dictionnaire
		return ui

	# ==================================================
	# region  Parsing
	# ==================================================
	##################################################
	def to_dict(self) -> dict[str, Any]:
		return {"type": type(self).__name__, "label": self.label}

	##################################################
	def update_from_dict(self, data: dict[str, Any]):
		self.label = data.get("label", "")
		for ui in self._uis.values():
			b = cast(QPushButton, ui.boxes[0])
			b.setText(self.label)


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QWidget, QFormLayout

	app = QApplication(sys.argv)
	w = QWidget()
	form = QFormLayout(w)  # crée et assigne le layout au widget
	button = Button("Test", "tooltip")

	button.get_ui("default").attach_to_form(form)
	button.get_ui("second").attach_to_form(form)

	button.connect_button(lambda: print("Hello"), "default", 0)
	button.connect_button(lambda: print("Bonjour"), "second", 0)

	w.show()
	sys.exit(app.exec_())
