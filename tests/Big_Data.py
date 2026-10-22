"""Teste les traitements PALM sur des jeux de données volumineux."""

import gc
import hashlib
import json
import time
from datetime import datetime

import psutil
import pytest

from palm_tracer.Processing import Palm
from palm_tracer.Processing.Drift import extract_beads, get_drift, remove_drift
from palm_tracer.Tools import FileIO, Ui
from tests.Utils import *

# TRESH, FILE = 340.6, "Tubulin-A647-3D-stacks_1"
TRESH, FILE = 450, "uTub_Cy3"
FILE_PATH = INPUT_DIR / "big input" / f"{FILE}.tif"

# TRESH, FILE = 60, "EOS2-20ms-4000f002"
# FILE_PATH = INPUT_DIR / "big input" / "sptPALM" / f"{FILE}.stk"

LOC_PATH = INPUT_DIR / "big input" / f"{FILE}-localizations-{get_loc_suffix(threshold=TRESH)}.csv"
TRC_PATH = INPUT_DIR / "big input" / f"{FILE}-tracking-{get_trc_suffix()}.csv"


# --------------------------------------------------
def test_palm_cpu(monkeypatch):
	"""
	Test pour le process sur des données importantes.

	- DLL Recompilé stade 0 : ~10min, utilisation de CPU inférieur à 4% (1 seul cœur), Memory Usage 4-5Giga. Passage à VS 2022
	  l'augmentation de durée peut être du aux nombreux old method dans la DLL non optimisé dans les compilateurs recents (malloc/free...)
	- DLL Recompilé stade 1 : même temps Passage à C++20
	- DLL Recompilé stade 2 : même temps suppression de commentaires e code (normal aucune influence) et arrangement des fichiers
	- DLL Recompilé stade 3 : même temps passage a une seule fonction pour lancer le process.
	- DLL Recompilé stade 4 : légere diminution avec const définition.
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
	  (memory toujours entre 4 et 5giga peut être une limite par thread ? à vérifier si les swap de mémoire ralentissent le process)
	- DLL Recompilé stade 15 : ~4min30-5min uniformisation de la segmentation gain Total ~55%
	- DLL Recompilé stade 16 : ~4min30-5min uniformisation de Atrous gain Total ~55%
	- DLL Recompilé stade 17 : ~4min30-5min uniformisation de double gain Total ~55%
	- DLL Recompilé stade 18 : ~3min30-4min PARALLÉLISATION GAUSSIAN FIT gain Total ~65%
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
	# Comparaison séquentielle volontaire : même pile, mêmes allocations, aucune écriture CSV.
	if not FILE_PATH.is_file(): pytest.skip(f"Pile volumineuse absente : {FILE_PATH}")
	dlls = [(name, FileIO.load_dll(name)) for name in ("CPU", "CPU_previous")]
	for name, dll in dlls:
		assert dll is not None, f"DLL indisponible : PALMTracer_{name}"
	palm = Palm()
	phases = []
	events = []
	process = psutil.Process()
	report_path = Path("reports/palm-cpu-comparison.json")
	report_path.parent.mkdir(parents=True, exist_ok=True)

	# --------------------------------------------------
	def mark(name):
		"""Repère chaque phase dans la console et dans l'historique de comparaison."""
		events.append({"name": name, "epoch_s": time.time()})
		print(f"[PALM BENCH] {datetime.now().isoformat(timespec='milliseconds')} {name}", flush=True)

	mark("load_stack_begin")
	stack = FileIO.open_tif(FILE_PATH)
	mark("load_stack_end")
	# Fixer le budget évite que les allocations du premier passage modifient le découpage du second.
	allocation_budget = palm.max_allocation_bytes()
	monkeypatch.setattr(palm, "max_allocation_bytes", lambda: allocation_budget)
	fit_params = get_fit_params(2)
	metadata = {"input":                   str(FILE_PATH), "shape": list(stack.shape), "input_bytes": stack.nbytes,
				"allocation_budget_bytes": allocation_budget, "threshold": TRESH, "watershed": default_watershed, "fit": 2,
				"logical_cpus":            psutil.cpu_count(), "physical_cpus": psutil.cpu_count(logical=False),
				"openmp_environment":      {key: value for key, value in os.environ.items() if key.startswith(("OMP_", "KMP_"))}}
	for index, (name, dll) in enumerate(dlls):
		if index:
			mark("pause_begin")
			time.sleep(5)
			mark("pause_end")
		palm._dll = dll
		palm._bind()
		native = dll.Localization
		calls = []

		# --------------------------------------------------
		def measured_localization(*args):
			"""Chronomètre le calcul natif séparément des allocations et de la conversion en DataFrame."""
			block = len(calls) + 1
			mark(f"{name}_native_{block}_begin")
			start, cpu_start = time.perf_counter(), time.process_time()
			count = native(*args)
			elapsed, cpu_elapsed = time.perf_counter() - start, time.process_time() - cpu_start
			calls.append({"wall_s": elapsed, "cpu_s": cpu_elapsed, "written_values": count, "frames": args[5].value})
			mark(f"{name}_native_{block}_end")
			print(f"[PALM BENCH] {name} bloc {block}: natif={elapsed:.3f}s, CPU={cpu_elapsed:.3f}s, valeurs={count}", flush=True)
			mark(f"{name}_dataframe_{block}")
			return count

		monkeypatch.setattr(dll, "Localization", measured_localization)
		mark(f"{name}_process_begin")
		baseline_rss = process.memory_info().rss
		start = time.perf_counter()
		localizations = palm.localization(stack, TRESH, default_watershed, 2, fit_params)
		elapsed = time.perf_counter() - start
		mark(f"{name}_process_end")
		rows = len(localizations)
		assert rows > 0, f"Aucune localisation avec {name}"
		path = Path(dll._name)
		phase = {"dll":           path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "wall_s": elapsed,
				 "native_wall_s": sum(call["wall_s"] for call in calls), "native_cpu_s": sum(call["cpu_s"] for call in calls),
				 "rows":          rows, "rss_before_bytes": baseline_rss, "rss_after_bytes": process.memory_info().rss, "native_calls": calls}
		phases.append(phase)
		print(f"[PALM BENCH] {name} terminé : total={elapsed:.3f}s, natif={phase['native_wall_s']:.3f}s, localisations={rows}", flush=True)
		mark(f"{name}_cleanup_begin")
		del localizations
		gc.collect()
		mark(f"{name}_cleanup_end")
		report_path.write_text(json.dumps({"metadata": metadata, "phases": phases, "events": events}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
	assert phases[0]["rows"] == phases[1]["rows"], "Le nombre de localisations diffère : comparer les résultats avant de conclure sur les performances."


# --------------------------------------------------
def test_tracking():
	"""
	Test pour le process sur des données importantes.

	- DLL Recompilé stade 0 : ~10min (-2min pour le chargement du fichier ~8min),
	  utilisation de CPU inférieur à 4% (1 seul cœur), Memory Usage 1.5-3Giga. Passage à VS 2022
	- DLL Recompilé stade 1 : ~4min30 (-2min pour le chargement du fichier ~2min30),
	  utilisation de CPU inférieur à 4% (1 seul cœur), Memory Usage 1.5-3Giga. Pré-calcul et suppression du code inutile
	- DLL Recompilé stade 1 : ~4min15 (-2min pour le chargement du fichier ~2min15),
	  utilisation de CPU inférieur à 4% (1 seul cœur), Memory Usage 1.5-3Giga. suppression du code inutilisé
	- DLL Recompilé stade 1 : ~4min15 (-2min pour le chargement du fichier ~2min15),
	  utilisation de CPU inférieur à 4% (1 seul cœur), Memory Usage 1.5-3Giga. suppression du code inutilisé

	Tubulin-A647-3D-stacks_1
		10-15min
	avec uTub_Cy3
		BOUCLE INFINI abandon

	NEW Tracking
	Tubulin
		Sans parallélisation : 2 s
	uTub_Cy3
		Sans parallélisation : 46 s environ 7s de calcul le reste pour ouverture et fermeture de fichiers
		Avec parallélisation : 33 s environ 2s

	"""
	palm = Palm()

	if LOC_PATH.exists() and LOC_PATH.is_file():
		localizations = pd.read_csv(LOC_PATH)
		tracks = palm.tracking(localizations, max_distance)
		if save_output: tracks.to_csv(TRC_PATH, index=False)
		assert len(tracks) > 0, "Aucune localisation trouvé"
	else:
		Ui.print_warning(f"Test non effectué car fichier '{LOC_PATH}' manquant.")
	assert True


# --------------------------------------------------
def test_drift():
	"""
	Test Extraction des billes sur des données importantes.

	2 billes temps : 49s
	"""
	localizations = pd.read_csv(LOC_PATH)
	beads = extract_beads(localizations, 1, is_3d=False)
	assert len(beads) > 0, "Aucune bille trouvé"
	if save_output: beads.to_csv(f"{OUTPUT_DIR}/{FILE}-beads.csv", index=False)

	# on ne va prendre qu'une bille pour éviter la moyenne et avoir à la fin un drift de 0 sur la bille sélectionné une fois corrigé.
	beads = beads[beads["Bead"] == 1]
	drift = get_drift(beads, False)
	if save_output: drift.to_csv(f"{OUTPUT_DIR}/{FILE}-drift.csv", index=False)
	corrected_beads = remove_drift(beads, drift, False)
	if save_output: corrected_beads.to_csv(f"{OUTPUT_DIR}/{FILE}-corrected_beads.csv", index=False)
	drift = get_drift(corrected_beads, False)
	assert np.allclose(drift[["X", "Y", "Z"]].to_numpy(), 0)
