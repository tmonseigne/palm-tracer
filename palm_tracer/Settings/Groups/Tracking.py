"""
Fichier contenant la classe `Tracking` dérivée de `BaseSettingGroup`,
qui regroupe les paramètres de tracking nécessaires à la configuration de PALM Tracer.


.. todo::
	Vérifier l'ordre de grandeur et le valeurs par défaut des paramètres de tracking.
"""

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import SpinFloat


##################################################
@dataclass
class Tracking(BaseSettingGroup):
	"""
	Classe contenant les paramètres de Tracking :
	"""

	label: str = "Tracking"
	setting_list = {"Max Distance": [SpinFloat, ["Max Distance", 5.0, 0.0, 1000, 1.0, 2]],
					"Min Length":   [SpinFloat, ["Min Length", 1.0, 0.0, 1000, 1.0, 2]],
					"Decrease": [SpinFloat, ["Decrease", 10.0, 0.0, 1000, 1.0, 2]],
					"Cost Birth": [SpinFloat, ["Cost Birth", 0.5, 0.0, 1000, 1.0, 2]]}
