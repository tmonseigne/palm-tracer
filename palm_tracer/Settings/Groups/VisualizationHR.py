"""
Fichier contenant la classe :class:`VisualizationHR` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de visualisation haute résolution nécessaires à la configuration de PALM Tracer.
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import Combo, SpinInt

HR_SOURCE = ["All", "Integrated Intensity", "Sigma X", "Sigma Y", "Circularity", "Theta", "MSE XY", "Z", "MSE Z"]


##################################################
@dataclass
class VisualizationHR(BaseSettingGroup):
	"""
	Classe contenant les paramètres de Visualisation haute résolution :
	"""

	label: str = "High Resolution"
	setting_list = {"Ratio":  [SpinInt, ["Up scaling ratio", 2, 1, 100, 1]],
					"Type":   [Combo, ["Type", 0, ["Localisations", "Tracks"]]],
					"Source": [Combo, ["Source", 0, HR_SOURCE]]}

	##################################################
	def initialize_ui(self):
		super().initialize_ui()
		self._settings["Type"].connect(self.toggle_type)

	##################################################
	def toggle_type(self, mode):
		"""Change le mode d'ajustement."""
		if mode == 0:
			self._settings["Source"].show()
		elif mode == 1:
			self._settings["Source"].hide()
