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
	Classe contenant les paramètres de Calcul sur les trajectoires :

	Attributs :
		- **MSD** (:class:`CheckBox <palm_tracer.Settings.Types.CheckBox.CheckBox>`) :
		  Calcul du MSD par trajectoire et par plans successifs (par défaut : `False`).
		- **Instant Diffusion** (:class:`CheckBox <palm_tracer.Settings.Types.CheckBox.CheckBox>`) :
		  Calcul de la diffusion instantanée par trajectoire et par plans successifs (par défaut : `False`).
		- **Fit Length** (:class:`SpinInt <palm_tracer.Settings.Types.SpinInt.SpinInt>`) :
		  Longueur de la fenêtre de calcul initiale des métriques génériques (par défaut : `4`).
		- **3D** (:class:`CheckBox <palm_tracer.Settings.Types.CheckBox.CheckBox>`) :
		  Utilisation ou non de la coordonnée Z dans les calculs (par défaut : `False`).
		- **Log Scale** (:class:`CheckBox <palm_tracer.Settings.Types.CheckBox.CheckBox>`) :
		  Utilisation ou non d'une échelle logarithmique pour les résultats (par défaut : `False`).
		- **Fit** (:class:`Combo <palm_tracer.Settings.Types.Combo.Combo>`) :
		  Méthode d'ajustement du mouvement de la trajectoire (par défaut : `None`).
	"""

	label: str = "Tracks Compute"
	setting_list = {"MSD":               [CheckBox, ["MSD", "", False]],
					"Instant Diffusion": [CheckBox, ["Instant Diffusion", "", False]],
					"Fit Length":        [SpinInt, ["Fit Length", "", 4, [2, 1000], 1]],
					"3D":                [CheckBox, ["3D", "Use the Z-axis during computes.", False]],
					"Log Scale":         [CheckBox, ["Log Scale", "Use log scale before saving results.", False]],
					"Fit":               [Combo, ["Fit", "Expected tracks movement to fit.", 0, ["None", "Linear", "Power", "Exponential"]]]}


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


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # crée et assigne le layout au widget
	group = TracksCompute()
	group.active = True
	w.layout().addWidget(group.widget)
	w.show()
	sys.exit(app.exec_())
