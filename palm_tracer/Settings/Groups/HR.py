"""
Fichier contenant la classe :class:`HR` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de visualisation haute résolution nécessaires à la configuration de PALM Tracer.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Groups.HRGaussian import HRGaussian
from palm_tracer.Settings.Types import ButtonGroup, CheckBox, Combo, SpinInt

DATA_SRC: dict[str, list] = {
		"Localization": ["Integrated Intensity", "Sigma X", "Sigma Y", "Circularity", "Theta",
						 "Surface", "MSE XY", "MSE Z"],
		"Tracking":     ["Track Number", "Plane", "Intensity", "Duration", "Length"]
		}


##################################################
@dataclass
class HR(BaseSettingGroup):
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
	setting_list = {"Type":             [ButtonGroup, ["Type", "", 0, ["Localization", "Tracks"]]],
					"Source":           [Combo, ["Source", "Data selected for Reconstruction.", 0, DATA_SRC["Localization"]]],
					"Color mode":       [Combo, ["Color mode",
												 "When overlapping, select whether the pixel values are added together "
												 "or whether only the maximum value is retained.", 0, ["Addition", "Max"]]],
					"Ratio":            [SpinInt, ["Up scaling ratio", "Image upscale ratio.", 4, [1, 256], 2]],
					"Crop":             [CheckBox, ["Auto Crop",
													"Remove all black Frame around reconstruction (Usefull when you make reconstruciton on a part of field). "
													"Keep 5 pixel of margin.", True]],
					"Remove Beads":     [CheckBox, ["Remove Beads", "Remove beads during reconstruction.", True]],
					"Drift Correction": [CheckBox, ["Drift Correction", "Apply a drift correction (Note: The beads must have been extracted before.)", True]],
					"Smooth Drift":     [CheckBox, ["Smooth Drift", "Apply a smooth on drift correction", True]],
					"Gaussian":         [HRGaussian, []]}

	##################################################
	def check_beads(self, state: bool):
		"""

		:param state:
		"""
		if state:
			self._settings["Remove Beads"].show()
			self._settings["Drift Correction"].show()
			self._settings["Smooth Drift"].show()
		else:
			self._settings["Remove Beads"].hide()
			self._settings["Drift Correction"].hide()
			self._settings["Smooth Drift"].hide()

	##################################################
	def update_src(self):
		"""Change la liste des sources pour les graphiques."""
		src = cast(Combo, self._settings["Source"])

		if self._settings["Type"].value == 0:
			src.items = DATA_SRC["Localization"]
			self._settings["Gaussian"].show()

		else:
			src.items = DATA_SRC["Tracking"]
			self._settings["Gaussian"].active = False
			self._settings["Gaussian"].hide()


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # crée et assigne le layout au widget
	group = HR()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
