"""Définit le groupe de paramètres de génération des graphiques."""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Groups.BaseUIGroup import BaseUIGroup
from palm_tracer.Settings.Groups.GraphDisplay import GraphDisplay
from palm_tracer.Settings.Types import ButtonGroup, CheckBox, Combo, SpinInt

DATA_SRC: dict[str, list] = {
		"Localization":     ["Integrated Intensity", "Sigma X", "Sigma Y", "Circularity", "Theta",
							 "X", "Y", "Z", "Surface", "MSE XY", "MSE Z", "Count per Plane"],
		"Tracking":         ["Length", "Length On", "Length Off", "MSD", "Instant D",
							 "Total Intensity", "D(0) (μm²/s)", "MSD(0) (μm²)", "MSE(0)", "A (μm²/s)", "B (μm²)", "MSE",
							 "Alpha", "Average Speed (Last-First)(μm/s)", "A (μm²)", "B (s)", "C (μm²)", "Confinement Radius (μm)"],
		"No Dual":          ["Count per Plane", "MSD"],
		"Tracking Scatter": ["Integrated Intensity", "Integrated Intensity Mean", "MSD", "MSD Mean", "Instant D", "Instant D Mean", "Track Count"],
		}


##################################################
@dataclass
class Graph(BaseSettingGroup):
	"""
	Regroupe les paramètres de sélection des graphiques.

	Paramètres regroupés :

	- ``Mode`` (:class:`~palm_tracer.Settings.Types.ButtonGroup.ButtonGroup`) : mode de représentation, histogramme, courbes Scatter ou nuage de points utilisant deux sources.
	- ``Type`` (:class:`~palm_tracer.Settings.Types.ButtonGroup.ButtonGroup`) : famille de données, localisations ou trajectoires.
	- ``Source`` (:class:`~palm_tracer.Settings.Types.Combo.Combo`) : première grandeur représentée.
	- ``Source B`` (:class:`~palm_tracer.Settings.Types.Combo.Combo`) : seconde grandeur représentée lorsque le mode ``Dual`` est actif.
	- ``MSD Step`` (:class:`~palm_tracer.Settings.Types.SpinInt.SpinInt`) : décalage temporel sélectionné pour le MSD.
	- ``Display`` (:class:`~palm_tracer.Settings.Groups.GraphDisplay.GraphDisplay`) : options de rendu du graphique.
	"""

	label: str = "Graph"
	"""Libellé du groupe affiché dans l'interface."""
	setting_list = {
			"Mode":     [ButtonGroup, ["Mode", "Dual Source Allow second source for Graph in a point cloud for source A by source B.",
									   0, ["Histogram", "Scatter", "Dual Source"]]],
			"Type":     [ButtonGroup, ["Type", "", 0, ["Localization", "Tracks"]]],
			"Source":   [Combo, ["Source", "Data selected for Graph.", 0, DATA_SRC["Localization"]]],
			"Source B": [Combo, ["Source", "Data selected for Graph.", 0, DATA_SRC["Localization"]]],
			"MSD Step": [SpinInt, ["MSD Step", "Step selected for display.", 1, [1, 10000], 1]],
			"Display":  [GraphDisplay, []]}
	"""Définition des paramètres du groupe et de leur configuration."""

	##################################################
	@property
	def display(self) -> GraphDisplay:
		"""Groupe de paramètres liés aux filtres sur la localization (:class:`~palm_tracer.Settings.Groups.FiltersL.FiltersL`)."""
		return cast(GraphDisplay, self._settings["Display"])

	##################################################
	def initialize(self):
		"""Initialise les connexions entre les paramètres."""
		super().initialize()
		self._settings["Mode"].connect(self.toggle_mode)
		self._settings["Type"].connect(self.toggle_type)
		self._settings["Source"].connect(self.toggle_src)
		self.toggle_mode(self._settings["Mode"].value)
		self.toggle_src()

	##################################################
	def get_ui(self, name: str = "default", mode: int = -1) -> BaseUIGroup:
		ui = super().get_ui(name, mode)
		self.toggle_mode(self._settings["Mode"].value)
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
		if src.current_text == "MSD" and self._settings["Mode"].value == 0: self._settings["MSD Step"].show()
		else: self._settings["MSD Step"].hide()

	##################################################
	def toggle_mode(self, mode: int):
		"""
		Adapte les sources et les options d'affichage au mode sélectionné.
		Les limites sont activées en histogramme et Dual Source, désactivées en Scatter.

		:param mode: Mode sélectionné : ``0`` pour l'histogramme, ``1`` pour le Scatter et ``2`` pour le Dual Source.
		"""
		self._settings["Source B"].show() if mode == 2 else self._settings["Source B"].hide()
		for key in ("Bins", "Cumul", "Count", "Gauss Mix"): self.display[key].show() if mode == 0 else self.display[key].hide()
		for key in ("Gauss", "KDE", "Poiss", "Exp"): self.display[key].hide() if mode == 1 else self.display[key].show()
		self.display["Limits"].value = mode != 1
		self._update_src()

	##################################################
	def _update_src(self):
		"""Actualise les sources en conservant les libellés disponibles, sinon sélectionne le premier choix."""
		# Liste de base
		if self._settings["Type"].value == 0: src = DATA_SRC["Localization"]
		elif self._settings["Mode"].value == 1: src = DATA_SRC["Tracking Scatter"]
		else: src = DATA_SRC["Tracking"]

		# En cas de Source multiple, suppression de certaines sources
		if self._settings["Mode"].value == 2: src = [s for s in src if s not in DATA_SRC["No Dual"]]

		# Conserve chaque sélection par libellé, même si son indice change dans la nouvelle liste.
		for key in ("Source", "Source B"):
			source = cast(Combo, self._settings[key])
			if source.items == src: continue
			selected = source.current_text
			with source.signal_blocked():
				source.items = src
				source.value = src.index(selected) if selected in src else 0
		self.toggle_src()


##################################################
if __name__ == "__main__":
	import sys

	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # Crée et affecte la mise en page au widget
	group = Graph()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
