"""
Fichier contenant la classe :class:`palm_tracer.Settings.Groups.TracksCompute` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de calcul sur les trajectoires nécessaires à la configuration de PALM Tracer.
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import CheckBox, Combo, SpinInt


##################################################
@dataclass
class TracksCompute(BaseSettingGroup):
	"""
	Classe contenant les paramètres de Calcul sur les trajectoires
	"""

	label: str = "Tracks Compute"
	setting_list = {"MSD":               [CheckBox, ["MSD", False]],
					"Instant Diffusion": [CheckBox, ["Instant Diffusion", False]],
					"Fit Length":        [SpinInt, ["Fit Length", 4, 2, 1000, 1]],
					"3D":                [CheckBox, ["3D", False]],
					"Log Scale":         [CheckBox, ["Log Scale", False]],
					"Fit":               [Combo, ["Fit", 0, ["None", "Linear", "Power", "Exponential"]]]}

#	##################################################
#	def initialize_ui(self):
#		super().initialize_ui()
#		self._settings["Fit"].connect(self.toggle_fit_mode)
#
#	##################################################
#	def toggle_fit_mode(self, mode):
#		"""Change le mode d'ajustement."""
#		if mode == 0:
#			self._settings["Fit Length"].hide()
#		else:
#			self._settings["Fit Length"].show()
