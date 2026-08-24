"""Définit un paramètre représenté par un bouton d'action."""

from __future__ import annotations

from dataclasses import dataclass

from qtpy.QtWidgets import QHBoxLayout, QPushButton

from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType
from palm_tracer.Settings.Types.BaseUIType import BaseUIType


##################################################
@dataclass
class Button(BaseSettingType):
	"""
	Représente une action déclenchée par un bouton Qt.

	:param label: Libellé affiché sur le bouton.
	:param tooltip: Description affichée dans l'infobulle.
	"""

	##################################################
	def reset(self):
		"""Réinitialise le paramètre à sa valeur par défaut."""
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
