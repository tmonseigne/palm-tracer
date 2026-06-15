"""
Fichier contenant la classe :class:`HRGaussian` dérivée de :class:`.BaseSettingGroup`,
qui regroupe les paramètres de visualisation haute résolution gaussienne nécessaires à la configuration de PALM Tracer.
"""
from __future__ import annotations

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import CheckBox, Combo, SpinFloat, SpinInt


##################################################
@dataclass
class HRGaussian(BaseSettingGroup):
	"""
	Classe contenant les paramètres de Visualisation haute résolution pour le rendu gaussien :

	Attributs :
		- **Intensity** (:class:`SpinInt <palm_tracer.Settings.Types.SpinInt.SpinInt>`) :
		  Intensité intégrée de la courbe gaussienne si l'option `Intensité fixe` est sélectionnée ;
		  sinon, le rapport par lequel la valeur sélectionnée dans la source sera divisée.
		- **Fixed Intensity** (:class:`CheckBox <palm_tracer.Settings.Types.CheckBox.CheckBox>`) : Garantit que chaque point a la même intensité.
		- **Shape** (:class:`Combo <palm_tracer.Settings.Types.Combo.Combo>`) :
		  Définit la forme de la distribution gaussienne (isotrope, anisotrope ou taille fixe, de sorte que chaque point ait la même forme isotrope).
		- **Size** (:class:`SpinFloat <palm_tracer.Settings.Types.SpinFloat.SpinFloat>`) :
		  L'écart-type de la distribution gaussienne si `Taille fixe` est sélectionné.
	"""

	label: str = "Gaussian Mode"
	setting_list = {"Intensity":       [SpinInt, ["Intensity", "Integrated intensity of the Gaussian curve if 'Fixed Intensity' is selected; otherwise, "
															   "the ratio by which the value selected in the source will be divided.", 100, [1, 100000], 10]],
					"Fixed Intensity": [CheckBox, ["Fixed Intensity", "Ensures that each point has the same intensity."]],
					"Shape":           [Combo, ["Shape", "Defines the shape of the Gaussian distribution (Isotropic, Anisotropic, or Fixed Size, "
														 "so that each point has the same isotropic shape).", 0, ["Fixed Size", "Isotrope", "Anisotrope"]]],
					"Size":            [SpinFloat, ["Size", "The standard deviation of the Gaussian distribution if \"Fixed Size\" is selected.",
													1, [0, 50], 0.01, 3]],
					}


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # crée et assigne le layout au widget
	group = HRGaussian()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
