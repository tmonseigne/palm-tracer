"""
Fichier contenant la classe :class:`GaussianFit` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres d'ajustement gaussien nécessaires à la configuration de PALM Tracer.
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import Combo, SpinFloat


##################################################
@dataclass
class GaussianFit(BaseSettingGroup):
	"""
	Classe contenant les paramètres du Gaussian Fit :

	Attributs :

		- **Mode** (:class:`Combo <palm_tracer.Settings.Types.Combo.Combo>`) : Méthode d'ajustement gaussien (par défaut : `Mode X, Y`).

			- `0` : `Mode X, Y` (theta et sigma sont fixes)
			- `1` : `Mode X, Y, Sigma` (theta est fixe, Sigma Non)
			- `2` : `Mode X, Y, SigmaX, SigmaY` (theta n'est pas fixe, Sigma Si)
			- `3` : `Mode X, Y, SigmaX, SigmaY, Theta` (theta et sigma ne sont pas fixes)

		- **Sigma** (:class:`SpinFloat <palm_tracer.Settings.Types.SpinFloat.SpinFloat>`) : Paramètre σ pour l'ajustement gaussien (par défaut : `1.0`).
		- **Theta** (:class:`SpinFloat <palm_tracer.Settings.Types.SpinFloat.SpinFloat>`) : Paramètre θ pour l'ajustement gaussien (par défaut : `1.0`).
	"""

	label: str = "Gaussian Fit"
	setting_list = {
			"Mode":  [Combo, ["Mode", "Selects the elements to fit.", 0, ["X, Y", "X, Y, Sigma", "X, Y, SigmaX, SigmaY", "X, Y, SigmaX, SigmaY, Theta"]]],
			"Sigma": [SpinFloat, ["σ", "Initial value of sigma.", 1.0, [0.0, 10.0], 0.1]],
			"Theta": [SpinFloat, ["θ", "Initial value of theta in degree.", 0.0, [-90, 90], 0.01]]
			}


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # crée et assigne le layout au widget
	group = GaussianFit()
	group.active = True
	w.layout().addWidget(group.widget)
	w.show()
	sys.exit(app.exec_())
