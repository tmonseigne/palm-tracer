"""
Fichier contenant la classe :class:`Graph` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de visualisation de graphique nécessaires à la configuration de PALM Tracer.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Groups.BaseUI import BaseUI
from palm_tracer.Settings.Groups.GraphDisplay import GraphDisplay
from palm_tracer.Settings.Types import ButtonGroup, CheckBox, Combo, SpinInt

DATA_SRC: dict[str, list] = {
		"Localization": ["Integrated Intensity", "Sigma X", "Sigma Y", "Circularity", "Theta",
						 "X", "Y", "Z", "Surface", "MSE XY", "MSE Z", "Localizations Count"],
		"Tracking":     ["Length"],
		"No Dual":      ["Localizations Count", "Length", "MSD"],
		}


##################################################
@dataclass
class Graph(BaseSettingGroup):
	"""
	Classe contenant les paramètres de Visualization :

	Attributs :
		- **Mode** (:class:`Combo <palm_tracer.Settings.Types.Combo.Combo>`) :
		  Type de graphiques à générer (histogram, heat map, violon) (par défaut : `All`).
		- **Source** (:class:`Combo <palm_tracer.Settings.Types.Combo.Combo>`) : Élément de la localisation à analyser (par défaut : `All`).
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
	def initialize(self):
		"""Initialise le dictionnaire de paramètres."""
		super().initialize()
		self._settings["Source"].connect(self.toggle_src)

	##################################################
	def get_ui(self, name: str = "default", mode: int = -1) -> BaseUI:
		ui = super().get_ui(name, mode)
		self.toggle_src(self._settings["Source"].value)
		return ui

	##################################################
	def toggle_src(self, value):
		"""Affiche ou masque l'option msd step à chaque changement de source."""
		src = cast(Combo, self._settings["Source"])
		if src.current_text == "MSD": self._settings["MSD Step"].show()
		else: self._settings["MSD Step"].hide()

	##################################################
	def update_src(self, optionnal: list[str] | None = None):
		"""Change la liste des sources pour les graphiques."""
		# Liste de base
		if self._settings["Type"].value == 0: src = DATA_SRC["Localization"]
		else: src = DATA_SRC["Tracking"]

		# Ajout optionnel (pour le Tracking suivant les éléments disponibles)
		if optionnal is not None: src += optionnal

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
