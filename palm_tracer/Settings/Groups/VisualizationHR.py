"""
Fichier contenant la classe :class:`VisualizationHR` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de visualisation haute résolution nécessaires à la configuration de PALM Tracer.
"""
from __future__ import annotations

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Groups.BaseUI import BaseUI
from palm_tracer.Settings.Types import Combo, SpinInt

HR_LOC_SOURCE = ["All", "Integrated Intensity", "Sigma X", "Sigma Y", "Circularity", "Theta", "MSE XY", "Z", "MSE Z"]
HR_TRC_SOURCE = ["All", "Track Number", "Length", "Instant D", "MSD", "Total Intensity"]


##################################################
@dataclass
class VisualizationHR(BaseSettingGroup):
	"""
	Classe contenant les paramètres de Visualisation haute résolution :

	Attributs :
		- **Ratio** (:class:`SpinInt <palm_tracer.Settings.Types.SpinInt.SpinInt>`) : Facteur d'agrandissement (par défaut : `2`).
		- **Type** (:class:`Combo <palm_tracer.Settings.Types.Combo.Combo>`) :
		  Choix du type de visualisation (Localisation ou trajectoires (par défaut : `Localizations`).
		- **Source** (:class:`Combo <palm_tracer.Settings.Types.Combo.Combo>`) :
		  Élément de la localisation (trajectoire) permettant de définir l'intensité (par défaut : `All`).
	"""

	label: str = "High Resolution"
	setting_list = {"Ratio":    [SpinInt, ["Up scaling ratio", "", 2, [1, 100], 1]],
					"Type":     [Combo, ["Type", "", 0, ["Localizations", "Tracks"]]],
					"Source L": [Combo, ["Source", "", 1, HR_LOC_SOURCE]],
					"Source T": [Combo, ["Source", "", 1, HR_TRC_SOURCE]]}

	##################################################
	def initialize(self):
		"""Initialise le dictionnaire de paramètres."""
		super().initialize()
		self._settings["Type"].connect(self.toggle_type)

	##################################################
	def get_ui(self, name: str = "default", mode: int = -1) -> BaseUI:
		ui = super().get_ui(name, mode)
		self.toggle_type(self._settings["Type"].value)
		return ui

	##################################################
	def toggle_type(self, mode):
		"""Change le mode d'ajustement."""
		if mode == 0:
			self._settings["Source L"].show()
			self._settings["Source T"].hide()
		elif mode == 1:
			self._settings["Source L"].hide()
			self._settings["Source T"].show()
		else:  # Impossible mais prévu
			self._settings["Source L"].hide()
			self._settings["Source T"].hide()


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # crée et assigne le layout au widget
	group = VisualizationHR()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
