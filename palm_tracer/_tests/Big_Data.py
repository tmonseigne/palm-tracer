""" Fichier des tests pour l'utilisation de la DLL CPU. """

from pathlib import Path

import pytest

from palm_tracer._tests.Utils import *
from palm_tracer.Processing import Palm
from palm_tracer.Tools import open_tif, print_warning

INPUT_DIR = Path(__file__).parent / "input"
OUTPUT_DIR = Path(__file__).parent / "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)

thresh = 340.6
file = "Tubulin-A647-3D-stacks_1"
path = Path(f"{INPUT_DIR}/big input/{file}.tif")


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_palm_cpu(make_napari_viewer):
	"""
	Test pour le process sur des données importantes.

	- DLL Recompilé stade 0 : ~10min, utilisation de CPU inférieur à 4% (1 seul coeur), Memory Usage 4-5Giga. Passage à VS 2022
	  l'augmentation de durée peut être du aux nombreux old method dnas la DLL non optimisé dans les compilateurs recents (malloc/free...)
	- DLL Recompilé stade 1 : même temps Passage à C++20
	- DLL Recompilé stade 2 : même temps suppression de commentaires e code (normal aucune influence) et arrangement des fichiers
	- DLL Recompilé stade 3 : même temps passage a une suele fonction pour lancer le process.
	- DLL Recompilé stade 4 : légere diminution avec const definition.
	- DLL Recompilé stade 5 : ~7min30s Factorisation du calcul de la PSF gain Total ~25%.
	- DLL Recompilé stade 6 : ~3min20s Factorisation du calcul de la derivé gain Total ~65%.
	- DLL Recompilé stade 7 : ~4min30s Factorisation du calcul de la matrice inverse gain Total ~55%
	  (sécurisation des pointeurs en vue du multithread pour cette fonction).
	- DLL Recompilé stade 8 : ~4min-5min Factorisation de constantes gain Total ~60%
	- DLL Recompilé stade 9 : ~4min30-5min Factorisation de calcul d'intensité et init de p gain Total ~55%
	- DLL Recompilé stade 10 : ~4min30-5min début d'utilisation de std vector et transform gain Total ~55%
	- DLL Recompilé stade 11 : ~4min50-5min Factorisation du calcul du RSS gain Total ~52%
	- DLL Recompilé stade 12 : ~4min30-5min Utilisation des transform sur les vecteur gain Total ~55%
	- DLL Recompilé stade 13 : ~4min30-5min Utilisation de size_t au lieu d'unsigned gain Total ~55%
	- DLL Recompilé stade 14 : ~4min30-5min Utilisation de double au lieu de float gain Total ~55%
	  YOUHOU Moins de cast et meilleure précision sans perte de performance
	  (memory toujours entre 4 et 5giga peut etre une limite par thread ? à vérifier si les swap de mémoire ralentissent le process)
	- DLL Recompilé stade 15 : ~4min30-5min uniformisation de la segmentation gain Total ~55%
	- DLL Recompilé stade 16 : ~4min30-5min uniformisation de Atrous gain Total ~55%
	- DLL Recompilé stade 17 : ~4min30-5min uniformisation de double gain Total ~55%
	- DLL Recompilé stade 18 : ~3min30-4min PARALLELISATION GAUSSIAN FIT gain Total ~65%
	  ENtre 20 et 90% d'utilisation CPU Ram à 4Giga
	- DLL Recompilé stade 19 : ~3min-3min30 Limitation à 4 threads pour accès mémoire simultanée gain Total ~70%
	  15% d'utilisation CPU Ram à 4Giga
	- DLL Recompilé stade 20 : ~2min30 Limitation aux nombres de coeur physiques et ajout d'une limite dynamique gain Total ~75%
	  10-20% d'utilisation CPU Ram à 4Giga
	- DLL Recompilé stade 21 : ~2min10 Suppression de la limite physique et conservation de la limite dynamique gain Total ~78%
	  10-20% d'utilisation CPU Ram à 4Giga
  	- DLL Recompilé stade 22 : ~20s Passage à l'appel de la stack au lieu de plan par plan gain Total ~96% + 15s d'analyse du csv dans python
	  jusqu'à 100% d'utilisation CPU Ram à 8Giga en process + quantité importante lors du passage à pandas (30s et 40Giga à vérifier sur pc moins performant).

	"""
	palm = Palm()
	if path.exists() and path.is_file():
		stack = open_tif(str(path))
		suffix = get_loc_suffix(threshold=thresh)
		localizations = palm.localization(stack, thresh, default_watershed, default_fit, get_fit_params())
		if save_output: localizations.to_csv(f"{OUTPUT_DIR}/{file}-localizations-{suffix}.csv", index=False)
		assert len(localizations) > 0, "Aucune localisation trouvé"
	else:
		print_warning("Test non effectué car fichier manquant.")
	assert True


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_palm_gpu(make_napari_viewer):
	"""
	Test pour le process sur des données importantes.

	- DLL Recompilé stade 0 : ~2min15, départ de la nouvelle dll
	- DLL Recompilé stade 1 : ~2min40, départ de la nouvelle dll calcul de la décomposition en wavelett
	  Opération la plus rentable à lancer sur GPU pour éviter les aller retours mémoire, conclusion :
	  - Perte de performance
	  - Manque de pertinennce tant que les calculs sont simple et sur des images simples
	    (sur une pile de plusieurs milliers d'images, cela "pourrait" devenir interessant)
	  - Ma carte graphique est d'un très haut niveau donc sur une classique possiblement encore plus de perte.
	  - la quantité d'utilisation du CPU baisse évidemment

	"""
	palm = Palm("GPU")
	if path.exists() and path.is_file():
		stack = open_tif(str(path))
		suffix = get_loc_suffix(threshold=thresh)
		localizations = palm.localization(stack, thresh, default_watershed, default_fit, sigma, theta, roi)
		if save_output: localizations.to_csv(f"{OUTPUT_DIR}/{file}-localizations-{suffix}.csv", index=False)
		assert len(localizations) > 0, "Aucune localisation trouvé"
	else:
		print_warning("Test non effectué car fichier manquant.")
	assert True


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_tracking(make_napari_viewer):
	"""
	Test pour le process sur des données importantes.

	- DLL Recompilé stade 0 : ~10min (-2min pour le chargement du fichier ~8min),
	  utilisation de CPU inférieur à 4% (1 seul coeur), Memory Usage 1.5-3Giga. Passage à VS 2022
	- DLL Recompilé stade 1 : ~4min30 (-2min pour le chargement du fichier ~2min30),
	  utilisation de CPU inférieur à 4% (1 seul coeur), Memory Usage 1.5-3Giga. Precalcul et suppression du code inutile
	- DLL Recompilé stade 1 : ~4min15 (-2min pour le chargement du fichier ~2min15),
	  utilisation de CPU inférieur à 4% (1 seul coeur), Memory Usage 1.5-3Giga. suppression du code inutilisé

	"""
	palm = Palm()
	suffix = get_loc_suffix(threshold=thresh)
	path_tracking = Path(f"{INPUT_DIR}/big input/{file}-localizations-{suffix}.csv")

	if path_tracking.exists() and path_tracking.is_file():
		localizations = pd.read_csv(path_tracking)
		tracks = palm.tracking(localizations, max_distance, min_life, decrease, cost_birth)
		if save_output: tracks.to_csv(f"{OUTPUT_DIR}/{file}-tracking-{suffix}.csv", index=False)
		assert len(localizations) > 0, "Aucune localisation trouvé"
	else:
		print_warning(f"Test non effectué car fichier '{path_tracking}' manquant.")
	assert True
