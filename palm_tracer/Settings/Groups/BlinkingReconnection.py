"""
Fichier contenant la classe :class:`palm_tracer.Settings.Groups.TrackingBlinkingReconnection` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de reconnexion de trajectoires en cas de scintillement nécessaires à la configuration de PALM Tracer.
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import Combo, SpinFloat, SpinInt


##################################################
@dataclass
class BlinkingReconnection(BaseSettingGroup):
	"""
	Classe contenant les paramètres de reconnexion de trajectoires en cas de scintillement.

	Par principe, on pourrait mettre le minimum de la Distance maximale à 2.
	Mais, si on veut reconnecter sur deux plans consécutifs avec des distances plus longues que la sélection d'origine, c'est possible.

	Attributs :
		- **Mode** (:class:`Combo <palm_tracer.Settings.Types.Combo.Combo>`) : Méthode de déplacement du point (par défaut : `Immobile`).
		- **Max Duration** (:class:`SpinInt <palm_tracer.Settings.Types.SpinInt.SpinInt>`) :
		  Durée maximale du scintillement en nombre de plans (par défaut : `1`).
		- **Max Speed** (:class:`SpinFloat <palm_tracer.Settings.Types.SpinFloat.SpinFloat>`) : Vitesse maximale du point en μm/plan (par défaut : `1.0`).
	"""

	label: str = "Blinking Reconnection"
	setting_list = {"Mode":         [Combo, ["Mode", "Expected type of movement of points.", 0, ["Immobile", "Diffuse", "Linear"]]],
					"Max Duration": [SpinInt, ["Max Duration (plane)", "Maximum blinking duration in number of planes", 1, [1, 1000], 1]],
					"Max Distance": [SpinFloat, ["Max Distance (px)", "Maximum distance between two planes for a point.", 1.0, [0.0, 20.0], 1.0, 2]]}


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # crée et assigne le layout au widget
	group = BlinkingReconnection()
	group.active = True
	w.layout().addWidget(group.widget)
	w.show()
	sys.exit(app.exec_())
