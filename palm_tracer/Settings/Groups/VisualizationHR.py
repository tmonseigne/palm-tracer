"""
Fichier contenant la classe :class:`VisualizationHR` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de visualisation haute résolution nécessaires à la configuration de PALM Tracer.
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
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
		  Element de la localisation (trajectoire) permettant de définir l'intensité (par défaut : `All`).
	"""

	label: str = "High Resolution"
	setting_list = {"Ratio":    [SpinInt, ["Up scaling ratio", "", 2, [1, 100], 1]],
					"Type":     [Combo, ["Type", "", 0, ["Localizations", "Tracks"]]],
					"Source L": [Combo, ["Source", "", 1, HR_LOC_SOURCE]],
					"Source T": [Combo, ["Source", "", 1, HR_TRC_SOURCE]]}

	##################################################
	def initialize_ui(self):
		super().initialize_ui()
		self._settings["Source T"].hide()
		self._settings["Type"].connect(self.toggle_type)

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
