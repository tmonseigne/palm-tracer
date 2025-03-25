"""
Ce sous-package contient les fonctions de chargement et utilisation de DLL externes pour le projet.

Ce sous-package regroupe des utilitaires pour :

- Chargement de DLLs : chargement des bibliothèques nécessaires au traitement d'image.
- Traitement d'images : exécution de traitements via DLLs pour détecter des points sur une image.
- Calcul et parsing de paramètres   estimation du nombre de points détectables en fonction des dimensions de l'image et de la densité.


"""
from pathlib import Path

# Exemple d'importation des modules pour un accès direct
from . import Parsing
from .Load import load_dll
from .PalmCPU import PalmCPU
from .PalmGPU import PalmGPU
from .Tracking import Tracking

DLL_PATH = Path(__file__).parent.parent.parent / "DLL"

# Définir la liste des symboles exportés
__all__ = ["load_dll", "PalmCPU", "PalmGPU", "Tracking", "Parsing"]
