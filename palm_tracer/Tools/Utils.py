"""
Fichier de fonctions génériques pour la gestion des fichiers, l'affichage de messages colorés dans la console
et la manipulation d'images matricielles, comme l'ajout de grilles.

Ce module regroupe des utilitaires pour des tâches courantes et est structuré en plusieurs sections :

- Gestion de fichiers : manipulation des noms de fichiers et ajout d'extensions ou de suffixes.
- Affichage : impression de messages colorés pour les erreurs ou avertissements.
- Dessin : ajout de grilles sur des images représentées sous forme de matrices NumPy.

**Structure** :

1. **File Management**

   - :func:`add_extension` : Ajoute une extension à un fichier s'il n'en a pas.
   - :func:`add_suffix` : Ajoute un suffixe à un nom de fichier, tout en préservant l'extension.
   - :func:`get_timestamp_for_files` : Génère un horodatage au format adapté pour les noms de fichiers.
   - :func:`get_last_file` : Récupère le dernier fichier (le plus récent) d'un chemin et un pattern prédefini.

2. **Prints**

   - :func:`print_error` : Affiche un message d'erreur en rouge.
   - :func:`print_warning` : Affiche un avertissement en jaune.
   - :func:`print_success` : Affiche un message de validation en vert.

"""

import glob
import os
from datetime import datetime

from colorama import Fore, Style


# ==================================================
# region File Management
# ==================================================
##################################################
def add_extension(filename: str, extension: str) -> str:
	"""
	Ajoute l'extension au fichier si ce n'est pas déjà l'extension actuelle

	:param filename: Nom du fichier
	:param extension: Extension finale du fichier
	"""
	if not extension.startswith("."): extension = "." + extension  # S'assurer que l'extension commence par un point
	if not filename.endswith(extension): filename += extension	   # Si le fichier n'a pas déjà l'extension, on l'ajoute
	return filename


##################################################
def add_suffix(filename: str, suffix: str) -> str:
	"""
	Ajoute un suffixe à un nom de fichier (gère la possibilité d'une extension ou non au nom de fichier).

	:param filename: Nom de fichier d'origine.
	:param suffix: Suffixe à ajouter.
	:return: Nom de fichier avec l'horodatage ajouté.
	"""
	# Insérer le suffixe avant l'extension du fichier s'il y en a une
	if "." in filename:
		name, ext = filename.rsplit(".", 1)
		return f"{name}{suffix}.{ext}"
	return f"{filename}{suffix}"


##################################################
def get_timestamp_for_files(with_hour: bool = True) -> str:
	"""
	Créé un horodatage au format -AAAAMMJJ_HHMMSS pour un nom de fichier.

	:param with_hour: Ajoute ou non l'heure au timestamp
	:return: Horodatage.
	"""
	if with_hour: return datetime.now().strftime("%Y%m%d_%H%M%S")  # Formater la date et l'heure
	return datetime.now().strftime("%Y%m%d")					   # Formater la date


##################################################
def get_last_file(path: str, name: str) -> str:
	"""
	Récupère le dernier fichier (le plus récent) qui contient le paramètre `name` dans son nom dans le chemin `path`.

	:param path: Chemin du dossier où chercher les fichiers.
	:param name: Chaîne à rechercher dans les noms de fichiers.
	:return: Chemin complet du dernier fichier trouvé ou une chaîne vide si aucun fichier ne correspond.
	"""
	try:
		search_pattern = os.path.join(path, f"*{name}*")  # Générer le chemin avec le filtre pour les fichiers contenant `name`
		files = glob.glob(search_pattern)				  # Récupérer tous les fichiers correspondant au motif
		if not files: return ""							  # Aucun fichier trouvé
		files.sort(key=os.path.getmtime, reverse=True)	  # Trier les fichiers par date de modification décroissante
		return files[0]									  # Retourner le fichier le plus récent
	except Exception as e:
		print(f"Erreur lors de la recherche du fichier : {e}")
		return ""


# ==================================================
# endregion File Management
# ==================================================


# ==================================================
# region Prints
# ==================================================
##################################################
def print_error(msg: str):
	"""
	Affiche un message avec une couleur rouge

	:param msg: message à afficher
	"""
	print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)


##################################################
def print_warning(msg: str):
	"""
	Affiche un message avec une couleur jaune

	:param msg: message à afficher
	"""
	print(Fore.YELLOW + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)


##################################################
def print_success(msg: str):
	"""
	Affiche un message avec une couleur verte

	:param msg: message à afficher
	"""
	print(Fore.GREEN + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)

# ==================================================
# endregion Prints
# ==================================================
