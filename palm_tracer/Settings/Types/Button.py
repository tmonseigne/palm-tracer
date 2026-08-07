"""
Fichier contenant la classe :class:`Button` dérivée de :class:`.BaseSettingType`, qui permet la gestion d'un paramètre type bouton à cliquer.
"""
from __future__ import annotations

from dataclasses import dataclass

from qtpy.QtWidgets import QHBoxLayout, QPushButton

from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType
from palm_tracer.Settings.Types.BaseUIType import BaseUIType


##################################################
@dataclass
class Button(BaseSettingType):
	"""
	Classe pour un paramètre spécifique de type bouton à cliquer.

	:param label: Nom du paramètre à afficher.
	:param tooltip: Description détaillée en overlay.
	"""

	##################################################
	def reset(self):
		pass

	##################################################
	def get_ui(self, name: str = "default") -> BaseUIType:
		if name in self._uis: return self._uis[name]

		box: QPushButton = QPushButton(self.label)  # Création de la boîte.
		ui = BaseUIType(layout=QHBoxLayout(), boxes=[box])
		box.setToolTip(self.tooltip)  # .			  Ajout du Tooltip
		box.clicked.connect(self.emit)  # .			  L'emission du signal se fera lors du clic sur le bouton
		ui.layout.addWidget(box)  # .				  Ajout du champ de texte.

		self._uis[name] = ui  # .					  Ajoute l'ui au dictionnaire
		return ui


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QWidget, QFormLayout

	app = QApplication(sys.argv)
	w = QWidget()
	form = QFormLayout(w)  # crée et assigne le layout au widget
	setting = Button("Test", "tooltip")
	setting.get_ui("default").attach_to_form(form)
	setting.get_ui("second").attach_to_form(form)
	setting.connect_button(lambda: print("Hello"), "default", 0)
	setting.connect_button(lambda: print("Bonjour"), "second", 0)
	w.show()
	sys.exit(app.exec_())
