"""
Fichier de fonctions de manipulation de fichiers

Ce module regroupe diverses fonctions pour la gestion et la manipulation de fichiers.
"""

import json
import os
from typing import Any


# ==================================================
# region JSON IO
# ==================================================
##################################################
def save_json(filename: str, data: dict[str, Any]):
	"""
	Enregistre un dictionnaire au format JSON.

	:param filename: Chemin du fichier JSON de sortie.
	:param data: Données à enregistrer.
	"""
	with open(filename, "w", encoding="utf-8") as file: json.dump(data, file, indent=4, ensure_ascii=False)


##################################################
def open_json(filename: str) -> dict[str, Any]:
	"""
	Ouvre un fichier JSON et récupère le dictionnaire.

	:param filename: Chemin du fichier JSON d'entrée.
	:return: Dictionnaire contenu dans le JSON.
	"""
	if not os.path.isfile(filename): raise OSError(f"Le fichier \"{filename}\" est introuvable.")
	with open(filename, "r", encoding="utf-8") as file: return json.load(file)

# ==================================================
# endregion JSON IO
# ==================================================
