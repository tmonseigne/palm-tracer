"""Présente un exemple de traitement de suivi de particules uniques."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import cast

from palm_tracer import PALMTracer
from palm_tracer.Settings.Groups import Batch, Filters, HR, Localization, Tracking
from palm_tracer.Settings.Types import CheckRangeFloat, CheckRangeInt, FileList

# region ---------- Valeurs à modifier ----------
DATA_PATH: Path = Path(__file__).parent / "data"  # Le dossier data se situe dans le même dossier que ce script
FILES_PATH: list[Path] = [DATA_PATH / "spt.stk"]  # Nom du/des fichiers à charger (une fonction peut générer la liste des fichiers)
RESET_RESULT: bool = True  # .						Supprime les précédents résultats

THRESHOLD: float = 60  # .							Seuil pour la détection
ROI_SIZE: int = 7  # .								Taille de la zone d'intérêt
WATERSHED: bool = True  # .							Activation du Watershed
FIT: int = 1  # .									Activation du Fit Gaussien
GAUSSIAN: int = 2  # .								Activation Mode d'ajustement
GAUSSIAN_SIGMA: float = 1.0  # .					Valeur initiale du Sigma
GAUSSIAN_THETA: float = 1.0  # .					Valeur Initiale du Theta

TRACKING_DISTANCE: float = 3.0  # .					Distance maximale pour le suivi

X_FILTER = [90, 160]  # .							Filtre sur X
Y_FILTER = [20, 80]  # .							Filtre sur Y
MSE_FILTER = [0, 0.8]  # .							Filtre sur MSE XY
LEN_FILTER = [10, 4000]  # .						Filtre sur la longueur des trajectoires

VIZ_RATIO: int = 8  # .								Taille du rendu Haute Résolution
# endregion ---------- Valeurs à modifier ----------

# region ---------- Application des paramètres ----------
pt = PALMTracer()  # .								Objet PALM Tracer
settings = pt.settings  # .							Paramètres de Palm Tracer

bat_s: Batch = pt.settings.batch  # .				Paramètres du batch
file_list = cast(FileList, bat_s["Files"])
file_list.items = [str(p) for p in FILES_PATH]  # .	Ajout des fichiers

loc_s: Localization = pt.settings.localization  # .	Paramètres de la localisation
loc_s.active = True  # .							Activation de la localisation
loc_s["Threshold"].value = THRESHOLD
loc_s["ROI Size"].value = ROI_SIZE
loc_s["Watershed"].value = WATERSHED
loc_s["Fit"].value = FIT
loc_s.gaussian["Mode"].value = GAUSSIAN
loc_s.gaussian["Sigma"].value = GAUSSIAN_SIGMA
loc_s.gaussian["Theta"].value = GAUSSIAN_THETA

trc_s: Tracking = pt.settings.tracking
trc_s.active = True  # Activation du suivi
trc_s["Max Distance"].value = TRACKING_DISTANCE

filt_s: Filters = pt.settings.filters  # .			Paramètres des filtres
filt_s["Save"].value = True  # .					Enregistrement des fichiers filtrés
pt.settings.rois.set_xy_roi(X_FILTER[0], X_FILTER[1], Y_FILTER[0], Y_FILTER[1])
cast(CheckRangeFloat, filt_s.localization["MSE XY"]).active = True
filt_s.localization["MSE XY"].value = MSE_FILTER
cast(CheckRangeInt, filt_s.tracking["Length"]).active = True
filt_s.tracking["Length"].value = LEN_FILTER

viz_s: HR = pt.settings.hr  # .						Paramètres de la visualisation Haute Résolution
viz_s.active = True  # .							Activation du rendu HR
viz_s["Type"].value = 1
viz_s["Ratio"].value = VIZ_RATIO
viz_s["Source"].value = 2
# endregion ---------- Application des paramètres ----------

# ---------- Lancement ----------
if RESET_RESULT:  # .								Suppression des précédents résultats si sélectionné
	paths: list[str] = bat_s.get_paths()
	for path in paths: shutil.rmtree(path, ignore_errors=True)

pt.process()
