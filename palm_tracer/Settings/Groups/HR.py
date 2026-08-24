"""Définit le groupe de paramètres du rendu haute résolution."""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Groups.BaseUIGroup import BaseUIGroup
from palm_tracer.Settings.Groups.HR3D import HR3D
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
	Regroupe les paramètres des reconstructions haute résolution.

	Paramètres regroupés :

	- ``Dimension`` (:class:`~palm_tracer.Settings.Types.ButtonGroup.ButtonGroup`) : mode de reconstruction 2D, pile Z ou rotation 3D.
	- ``Type`` (:class:`~palm_tracer.Settings.Types.ButtonGroup.ButtonGroup`) : famille de données, localisations ou trajectoires.
	- ``Source`` (:class:`~palm_tracer.Settings.Types.Combo.Combo`) : grandeur utilisée pour colorer ou pondérer les points.
	- ``Color mode`` (:class:`~palm_tracer.Settings.Types.Combo.Combo`) : additionne les contributions superposées ou conserve leur maximum.
	- ``Ratio`` (:class:`~palm_tracer.Settings.Types.SpinInt.SpinInt`) : facteur d'agrandissement ; valeur par défaut : ``4``.
	- ``Crop`` (:class:`~palm_tracer.Settings.Types.CheckBox.CheckBox`) : retire automatiquement les bordures vides.
	- ``Remove Beads`` (:class:`~palm_tracer.Settings.Types.CheckBox.CheckBox`) : exclut les billes de la reconstruction.
	- ``Drift Correction`` et ``Smooth Drift`` (:class:`~palm_tracer.Settings.Types.CheckBox.CheckBox`) : appliquent puis lissent la correction de dérive.
	- ``Gaussian`` (:class:`~palm_tracer.Settings.Groups.HRGaussian.HRGaussian`) : paramètres du rendu gaussien.
	- ``3D`` (:class:`~palm_tracer.Settings.Groups.HR3D.HR3D`) : paramètres de la pile ou de la rotation 3D.
	"""

	label: str = "High Resolution"
	"""Libellé du groupe affiché dans l'interface."""
	setting_list = {"Dimension":        [ButtonGroup, ["Dimension", "", 0, ["2D", "Z-Stack", "3D Rotation"]]],
					"Type":             [ButtonGroup, ["Type", "", 0, ["Localization", "Tracks"]]],
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
					"Gaussian":         [HRGaussian, []],
					"3D":               [HR3D, []]
					}
	"""Définition des paramètres du groupe et de leur configuration."""

	##################################################
	@property
	def gaussian(self) -> HRGaussian:
		"""Groupe de paramètres liés à la représentation gaussienne (:class:`~palm_tracer.Settings.Groups.HRGaussian.HRGaussian`)."""
		return cast(HRGaussian, self._settings["Gaussian"])

	##################################################
	@property
	def hr_3d(self) -> HR3D:
		"""Groupe de paramètres liés à la reconstruction 3D (:class:`~palm_tracer.Settings.Groups.HR3D.HR3D`)."""
		return cast(HR3D, self._settings["3D"])

	##################################################
	def initialize(self):
		"""Initialise les connexions entre les paramètres."""
		super().initialize()
		self._settings["Dimension"].connect(self.toggle_dimension)
		self._settings["Type"].connect(self.toggle_type)
		self.toggle_dimension()
		self.toggle_type()

	##################################################
	def get_ui(self, name: str = "default", mode: int = -1) -> BaseUIGroup:
		ui = super().get_ui(name, mode)
		self.toggle_dimension()
		self.toggle_type()
		return ui

	##################################################
	def toggle_dimension(self):
		"""Désactive l'option tracking dans le cas de la 3D et affiche/masque les options 3D."""
		s = cast(ButtonGroup, self._settings["Type"])
		if self._settings["Dimension"].value == 0:
			self._settings["3D"].hide()
			s.active_item(1, True)
		else:
			self._settings["3D"].show()
			s.active_item(1, False)
			s.value = 0
			if self._settings["Dimension"].value == 1:
				self._settings["3D"]["Z Step"].show()
				self._settings["3D"]["Axis"].hide()
				self._settings["3D"]["Frames"].hide()
			else:
				self._settings["3D"]["Z Step"].hide()
				self._settings["3D"]["Axis"].show()
				self._settings["3D"]["Frames"].show()

	##################################################
	def toggle_type(self):
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
