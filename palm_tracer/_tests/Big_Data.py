"""Fichier des tests pour l'utilisation de la DLL CPU."""

from palm_tracer._tests.Utils import *
from palm_tracer.Processing import Palm
from palm_tracer.Processing.Drift import extract_beads
from palm_tracer.Tools import FileIO, Ui

#TRESH, FILE = 340.6, "Tubulin-A647-3D-stacks_1"
TRESH, FILE = 450, "uTub_Cy3"
FILE_PATH = INPUT_DIR / "big input" / f"{FILE}.tif"
LOC_PATH = INPUT_DIR / "big input" / f"{FILE}-localizations-{get_loc_suffix(threshold=TRESH)}.csv"
TRC_PATH = INPUT_DIR / "big input" / f"{FILE}-tracking-{get_trc_suffix()}.csv"


##################################################
def test_palm_cpu(qtbot):
	"""
	Test pour le process sur des données importantes.

	- DLL Recompilé stade 0 : ~10min, utilisation de CPU inférieur à 4% (1 seul cœur), Memory Usage 4-5Giga. Passage à VS 2022
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
	- DLL Recompilé stade 20 : ~2min30 Limitation aux nombres de cœur physiques et ajout d'une limite dynamique gain Total ~75%
	  10-20% d'utilisation CPU Ram à 4Giga
	- DLL Recompilé stade 21 : ~2min10 Suppression de la limite physique et conservation de la limite dynamique gain Total ~78%
	  10-20% d'utilisation CPU Ram à 4Giga
  	- DLL Recompilé stade 22 : ~20s Passage à l'appel de la stack au lieu de plan par plan gain Total ~96% + 15s d'analyse du csv dans python
	  jusqu'à 100% d'utilisation CPU Ram à 8Giga en process + quantité importante lors du passage à pandas (30s et 40Giga à vérifier sur pc moins performant).

	  avec uTub_Cy3
	- 1m33 avec 20Giga en entrée (1.8 Giga en sortie)

	"""
	palm = Palm()
	if FILE_PATH.exists() and FILE_PATH.is_file():
		stack = FileIO.open_tif(FILE_PATH)
		suffix = get_loc_suffix(threshold=TRESH)
		localizations = palm.localization(stack, TRESH, default_watershed, default_fit, get_fit_params(default_fit))
		if save_output: localizations.to_csv(f"{OUTPUT_DIR}/{FILE}-localizations-{suffix}.csv", index=False)
		assert len(localizations) > 0, "Aucune localisation trouvé"
	else:
		Ui.print_warning("Test non effectué car fichier manquant.")
	assert True


##################################################
def test_tracking(qtbot):
	"""
	Test pour le process sur des données importantes.

	- DLL Recompilé stade 0 : ~10min (-2min pour le chargement du fichier ~8min),
	  utilisation de CPU inférieur à 4% (1 seul cœur), Memory Usage 1.5-3Giga. Passage à VS 2022
	- DLL Recompilé stade 1 : ~4min30 (-2min pour le chargement du fichier ~2min30),
	  utilisation de CPU inférieur à 4% (1 seul cœur), Memory Usage 1.5-3Giga. Precalcul et suppression du code inutile
	- DLL Recompilé stade 1 : ~4min15 (-2min pour le chargement du fichier ~2min15),
	  utilisation de CPU inférieur à 4% (1 seul cœur), Memory Usage 1.5-3Giga. suppression du code inutilisé
	- DLL Recompilé stade 1 : ~4min15 (-2min pour le chargement du fichier ~2min15),
	  utilisation de CPU inférieur à 4% (1 seul cœur), Memory Usage 1.5-3Giga. suppression du code inutilisé

	avec uTub_Cy3
	BOUCLE INFINI

	"""
	palm = Palm()

	if LOC_PATH.exists() and LOC_PATH.is_file():
		localizations = pd.read_csv(LOC_PATH)
		suffix = get_trc_suffix()
		tracks = palm.tracking(localizations, max_distance, min_life, decrease, cost_birth)
		if save_output: tracks.to_csv(f"{OUTPUT_DIR}/{FILE}-tracking-{suffix}.csv", index=False)
		assert len(localizations) > 0, "Aucune localisation trouvé"
	else:
		Ui.print_warning(f"Test non effectué car fichier '{LOC_PATH}' manquant.")
	assert True


##################################################
def test_beads():
	"""Test Extraction des billes sur des données importantes."""
	localizations = pd.read_csv(LOC_PATH)
	beads = extract_beads(localizations, max_distance, is_3d=False)
	print(beads)
