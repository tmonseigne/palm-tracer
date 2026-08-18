"""
Fichier contenant la classe :class:`Graph` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de visualisation de graphique nécessaires à la configuration de PALM Tracer.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Groups.BaseUIGroup import BaseUIGroup
from palm_tracer.Settings.Groups.GraphDisplay import GraphDisplay
from palm_tracer.Settings.Types import ButtonGroup, CheckBox, Combo, SpinInt

DATA_SRC: dict[str, list] = {
		"Localization": ["Integrated Intensity", "Sigma X", "Sigma Y", "Circularity", "Theta",
						 "X", "Y", "Z", "Surface", "MSE XY", "MSE Z", "Localizations Count"],
		"Tracking":     ["Length", "Length On", "Length Off", "MSD", "Instant D",
						 "Total Intensity", "D(0) (μm²/s)", "MSD(0) (μm²)", "MSE(0)", "A (μm²/s)", "B (μm²)", "MSE",
						 "Alpha", "Average Speed (Last-First)(μm/s)", "A (μm²)", "B (s)", "C (μm²)", "Confinement Radius (μm)", "Length Scatter"],
		"No Dual":      ["Localizations Count", "Length", "Length On", "Length Off", "MSD", "Length Scatter"],
		}


##################################################
@dataclass
class Graph(BaseSettingGroup):
	"""
	Classe contenant les paramètres de Visualisation :

	Attributs :
		- **Type** (:class:`ButtonGroup <palm_tracer.Settings.Types.ButtonGroup.ButtonGroup>`) : Type de données à représenter (localisations ou suivi).
		- **Source** (:class:`Combo <palm_tracer.Settings.Types.Combo.Combo>`) : Source des données à représenter.
		- **Dual** (:class:`CheckBox <palm_tracer.Settings.Types.CheckBox.CheckBox>`) : Active la représentation de deux sources.
		- **Source B** (:class:`Combo <palm_tracer.Settings.Types.Combo.Combo>`) : Source secondaire des données à représenter.
		- **MSD Step** (:class:`SpinInt <palm_tracer.Settings.Types.SpinInt.SpinInt>`) : Lors de la représentation du MSD, sélection de l'étape à représenter.
		- **Display** (:class:`GraphDisplay <palm_tracer.Settings.Groups.GraphDisplay.GraphDisplay>`) : Options d'affichage du graphique.
	"""

	label: str = "Graph"
	setting_list = {
			"Type":     [ButtonGroup, ["Type", "", 0, ["Localization", "Tracks"]]],
			"Source":   [Combo, ["Source", "Data selected for Graph.", 0, DATA_SRC["Localization"]]],
			"Dual":     [CheckBox, ["Dual Source", "Allow second source for Graph in scatter plot source A by source B."]],
			"Source B": [Combo, ["Source", "Data selected for Graph.", 0, DATA_SRC["Localization"]]],
			"MSD Step": [SpinInt, ["MSD Step", "Step selected for display.", 1, [1, 10000], 1]],
			"Display":  [GraphDisplay, []]}

	##################################################
	@property
	def display(self) -> GraphDisplay:
		"""Groupe de paramètres liés aux filtres sur la localization (:class:`FiltersL <palm_tracer.Settings.Groups.FiltersL.FiltersL>`)."""
		return cast(GraphDisplay, self._settings["Display"])

	##################################################
	def initialize(self):
		super().initialize()
		self._settings["Type"].connect(self.toggle_type)
		self._settings["Dual"].connect(self.toggle_dual)
		self._settings["Source"].connect(self.toggle_src)
		self.toggle_dual(self._settings["Dual"].value)
		self.toggle_src()

	##################################################
	def get_ui(self, name: str = "default", mode: int = -1) -> BaseUIGroup:
		ui = super().get_ui(name, mode)
		self.toggle_dual(self._settings["Dual"].value)
		self.toggle_src()
		return ui

	##################################################
	def toggle_type(self):
		"""Change la liste des sources pour les graphiques."""
		self._update_src()

	##################################################
	def toggle_src(self):
		"""Affiche ou masque l'option msd step à chaque changement de source."""
		src = cast(Combo, self._settings["Source"])
		if src.current_text == "MSD": self._settings["MSD Step"].show()
		else: self._settings["MSD Step"].hide()

	##################################################
	def toggle_dual(self, value: bool):
		"""Affiche/Masque la seconde source."""
		self._settings["Source B"].show() if value else self._settings["Source B"].hide()
		self._update_src()

	##################################################
	def _update_src(self):
		"""Change la liste des sources pour les graphiques."""
		# Liste de base
		if self._settings["Type"].value == 0: src = DATA_SRC["Localization"]
		else: src = DATA_SRC["Tracking"]

		# En cas de Source multiple, suppression de certaines sources
		if self._settings["Dual"].value: src = [s for s in src if s not in DATA_SRC["No Dual"]]

		# Attribution aux deux sources
		cast(Combo, self._settings["Source"]).items = src
		cast(Combo, self._settings["Source B"]).items = src


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # crée et assigne le layout au widget
	group = Graph()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
