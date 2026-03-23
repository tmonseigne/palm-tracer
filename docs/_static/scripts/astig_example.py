"""Example script for SPT processing."""
from __future__ import annotations

import shutil
from pathlib import Path
from typing import cast

from palm_tracer import PALMTracer
from palm_tracer.Settings.Groups import Batch, Filters, HR, Localization
from palm_tracer.Settings.Types import CheckRangeFloat, CheckRangeInt, FileList

# region ---------- Valeurs à modifier ----------
DATA_PATH: Path = Path(__file__).parent / "data"  # Le dossier data se situe dans le même dossier que ce script
MODEL_PATH: Path = DATA_PATH / "3d_model.csv"  # .	Nom du fichier de modèle d'astigmatisme 3D
FILES_PATH: list[Path] = [DATA_PATH / "GFP.stk"]  # Nom du/des fichiers à charger (une fonction peut générer la liste des fichiers)
RESET_RESULT: bool = True  # .						Supprime les précédents résultats

THRESHOLD: float = 650  # .							Seuil pour la détection
ROI_SIZE: int = 11  # .								Taille de la zone d'intérêt
WATERSHED: bool = True  # .							Activation du Watershed
FIT: int = 1  # .									Activation du Fit Gaussien
GAUSSIAN: int = 2  # .								Activation Mode d'ajustement
GAUSSIAN_SIGMA: float = 1.0  # .					Valeur initiale du Sigma
GAUSSIAN_THETA: float = 2.0  # .					Valeur Initiale du Theta
Z_MAX: int = 550  # .								Borne en Z pour l'estimation 3D
X_FILTER = [100, 150]  # .							Filtre sur X
Y_FILTER = [100, 150]  # .							Filtre sur Y
MSE_FILTER = [0, 0.9]  # .							Filtre sur MSE XY

VIZ_RATIO: int = 32  # . 							Taille du rendu Haute Résolution
VIZ_INTENSITY: int = 10000  # .						Intenisté fixe pour tous les points
VIZ_SIZE: float = 0.5  # .							Taille du rendu Gaussien
# endregion ---------- Valeurs à modifier ----------

# region ---------- Création des objets initiaux ----------
pt = PALMTracer()
settings = pt.settings  # Paramètres de Palm Tracer
# endregion ---------- Création des objets ----------

# region ---------- Application des paramètres ----------
bat_s: Batch = pt.settings.batch
file_list = cast(FileList, bat_s["Files"])
file_list.items = [str(p) for p in FILES_PATH]  # .	Ajout des fichiers

loc_s: Localization = pt.settings.localization
loc_s.active = True  # .							Activation de la localisation
loc_s["Threshold"].value = THRESHOLD
loc_s["ROI Size"].value = ROI_SIZE
loc_s["Watershed"].value = WATERSHED
loc_s["Fit"].value = FIT
loc_s.gaussian["Mode"].value = GAUSSIAN
loc_s.gaussian["Sigma"].value = GAUSSIAN_SIGMA
loc_s.gaussian["Theta"].value = GAUSSIAN_THETA
loc_s.gaussian["Z"].value = True  # .				Active l'estimation du Z.
loc_s.gaussian["Z max"].value = Z_MAX
loc_s.gaussian["Model"].value = str(MODEL_PATH)

filt_s: Filters = pt.settings.filters
filt_s["Save"].value = True  # Enregistrement des fichiers filtrés
cast(CheckRangeInt, filt_s.localization["X"]).active = True
filt_s.localization["X"].value = X_FILTER
cast(CheckRangeInt, filt_s.localization["Y"]).active = True
filt_s.localization["Y"].value = Y_FILTER
cast(CheckRangeFloat, filt_s.localization["MSE XY"]).active = True
filt_s.localization["MSE XY"].value = MSE_FILTER

viz_s: HR = pt.settings.hr
viz_s.active = True  # .							Activation du rendu HR
viz_s["Ratio"].value = VIZ_RATIO
viz_s.gaussian.active = True
viz_s.gaussian["Intensity"].value = VIZ_INTENSITY
viz_s.gaussian["Fixed Intensity"].value = True
viz_s.gaussian["Size"].value = VIZ_SIZE
# endregion ---------- Application des paramètres ----------

# ---------- Lancement ----------
if RESET_RESULT:
	paths: list[str] = bat_s.get_paths()
	for path in paths: shutil.rmtree(path, ignore_errors=True)

pt.process()
