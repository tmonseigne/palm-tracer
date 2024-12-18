"""
Fichier contenant la classe `Calibration` dérivée de `BaseSettingGroup`, qui regroupe les paramètres de calibration nécessaires
à la configuration de PALM Tracer.

**Attributs de la classe Calibration** :

- **Pixel Size (IntSetting)** : Taille d'un pixel en nanomètres.
  - Plage : [1, 500] nm
  - Pas : 10
  - Valeur par défaut : 160 nm

- **Exposure (IntSetting)** : Temps d'exposition par image en millisecondes.
  - Plage : [1, 1000] ms
  - Pas : 10
  - Valeur par défaut : 50 ms

- **Intensity (FloatSetting)** : Intensité lumineuse exprimée en photons par unités analogiques-numériques (ADU).
  - Plage : [0.0, 1.0] photon/ADU
  - Pas : 0.01
  - Précision : 2
  - Valeur par défaut : 0.0120 photon/ADU

"""

from dataclasses import dataclass

from palm_tracer.Settings.Group.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.SettingTypes import FloatSetting, IntSetting


##################################################
@dataclass
class Calibration(BaseSettingGroup):
	"""
	Classe contenant les informations de calibration :

	Attributs :

		- **Pixel Size (IntSetting)** : Taille d'un pixel en nanomètres (par défaut : 160).
		- **Exposure (IntSetting)** : Temps d'exposition en millisecondes par image (par défaut : 50).
		- **Intensity (FloatSetting)** : Intensité lumineuse en photons par Unités analogique-numériques (ADU) (par défaut : 0.0120).
	"""

	# ==================================================
	# region Initialization
	# ==================================================
	##################################################
	def initialize(self):
		""" Initialise le dictionnaire de paramètres. """
		super().initialize()  # Appelle l'initialisation de la classe mère.
		self._settings["Pixel Size"] = IntSetting(label="Pixel Size (nm)", min=1, max=500, step=10, default=160)
		self._settings["Exposure"] = IntSetting(label="Exposure Time (ms/frame)", min=1, max=1000, step=10, default=50)
		self._settings["Intensity"] = FloatSetting(label="Intensity (photon/ADU)", min=0.0, max=1, step=0.01, default=0.0120)

# ==================================================
# endregion Initialization
# ==================================================
