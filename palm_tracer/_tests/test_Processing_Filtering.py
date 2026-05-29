"""
Fichier des tests pour la classe PALMTracer

.. note:: Il est fréquent que la vérificaiton du log ne se fasse qu'au nombre de lignes, car au moins 15 lignes à chaque process.
"""
import shutil

import pytest

from palm_tracer._tests.Utils import *
from palm_tracer.Processing import Filtering
from palm_tracer.Settings.Groups import Filters

OUTPUT_FOLDER = INPUT_DIR / "stack_PALM_Tracer"
OUTPUT_FOLDER_2 = INPUT_DIR / "stack_quadrant_PALM_Tracer"


@pytest.fixture
def pt():
	"""fixture interne."""
	obj = PALMTracer()
	yield obj
	try: obj._logger.close()
	except Exception: pass


##################################################
def clean_output():
	"""Vide les dossiers de sorties."""
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
	shutil.rmtree(OUTPUT_FOLDER_2, ignore_errors=True)


##################################################
def check_output(folder: Path, csv: Optional[list[int]] = None, log: Optional[list[int]] = None, json: Optional[list[int]] = None,
				 tif: Optional[list[int]] = None, png: Optional[list[int]] = None, clean: bool = True):
	"""Vérifie si la sortie correspond à ce qui est attendu."""
	if not folder.is_dir(): pytest.fail("Dossier invalide.")

	for ext, v in {"csv": csv, "log": log, "json": json, "tif": tif, "png": png}.items():
		if v is None: continue
		r = f"*.{ext}"
		files = list(folder.glob(r))
		n = len(files)
		if len(v) == 1:
			if n != v[0]: pytest.fail(f"Il devrait y avoir {v[0]} fichier(s) '{r}', trouvé(s) : {n} ({files}).")
		elif not v[0] <= n <= v[1]: pytest.fail(f"Il devrait y avoir entre {v[0]} et {v[1]} fichiers '{r}', trouvé(s) : {n} ({files}).")

	if clean: shutil.rmtree(folder, ignore_errors=True)


##################################################
def check_capsys(capsys, n_lines: int, steps: list[tuple[bool, int]]):
	"""
	Vérifie dans le capsys les éléments activé ou non et la correspondance du nombre de lignes.

	:param capsys:
	:param n_lines:
	:param steps:
	"""
	lines = get_lines_output(capsys)
	# for i in range(len(lines)): print(f"{i}: {lines[i]}")
	assert len(lines) == n_lines
	step_name = ["Localization", "Beads Extraction", "Tracking", "Blinking Reconnection", "Tracks Computes",
				 "High-resolution visualization", "Graphical visualization", "Gallery generation"]
	for i in range(8):
		status, line = steps[i]
		status_str = "enabled" if status else "disabled"
		assert re.fullmatch(TS_PATTERN + rf"\s{step_name[i]} {status_str}\.", lines[line])


##################################################
def test_filter_bad(qtbot):
	"""Test pour le filtrage complet."""
	filters = Filters()
	f = Filtering(filters)
	res = f.localization(pd.DataFrame())
	assert res.empty, "Un dataframe vide doit être retourné."
	res = f.tracking(pd.DataFrame())
	assert res.empty, "Un dataframe vide doit être retourné."
	res = f.tracks_compute(pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame())
	for r in res: assert r.empty, "Un dataframe vide doit être retourné."


##################################################
def test_localization(qtbot):
	"""Test pour le filtrage complet."""
	src = pd.read_csv(INPUT_DIR / "ref" / "stack-localizations-103.6_True_4_1.0_0.0_7.csv")
	filters = Filters()
	f = Filtering(filters)

	filters["Plane"].active = True
	filters["Plane"].value = [1, 9]  # .	Suppression du dernier plan uniquement 411/451 : 40 suppression(s)
	fl = filters.localization
	fl["Intensity"].active = True
	fl["Intensity"].value = [100, 20000]  # 391/411 : 20 suppression(s)
	fl["Sigma X"].active = True
	fl["Sigma X"].value = [0, 10]  # .		Aucune suppression
	fl["Sigma Y"].active = True
	fl["Sigma Y"].value = [0, 10]  # .		Aucune suppression
	fl["Circularity"].active = True  # .	Aucune suppression
	fl["Theta"].active = True
	fl["Theta"].value = [-60, 60]  # .		346/391 : 45 suppression(s)
	fl["Z"].active = True  # .				Aucune suppression
	fl["MSE XY"].active = True
	fl["MSE XY"].value = [0.05, 10]  # .	345/366 : 1 suppression(s)
	# fl["MSE Z"].active = True # .			La colonne est à -1 le filtre est forcément sur un nombre positif donc on passerait à 0 éléments
	res = f.localization(src)

	ref = [["Plane", 1, 9], ["Integrated Intensity", 100, 20000], ["MSE XY", 0.01, 10],
		   ["Sigma X", 0, 10], ["Sigma Y", 0, 10], ["Theta", -60, 60],
		   ["Circularity", 0, 1], ["Z", -1, 1]]
	for r in ref:
		assert res[r[0]].between(r[1], r[2]).all(), f"Le DataFrame contient des valeurs hors [{r[1]}:{r[2]}] dans la colonne {r[0]}."

	res, ref = len(res), 345
	assert res == ref, f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"

	fl["MSE Z"].active = True  # .			La colonne est à -1 le filtre est forcément sur un nombre positif donc on passerait à 0 éléments
	res = f.localization(src)
	assert res.empty, "Un dataframe vide doit être retourné."


##################################################
def test_tracking(qtbot):
	"""Test pour le filtrage des plans."""
	src = pd.read_csv(INPUT_DIR / "ref" / "stack-blinking.csv")
	filters = Filters()
	f = Filtering(filters)

	filters.tracking["Length"].active = True
	filters.tracking["Length"].value = [3, 10000]  # 166/435 : 269 suppression(s)

	res = f.tracking(src)
	res, ref = len(res), 166
	assert res == ref, f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"


##################################################
def test_tracks_compute(qtbot):
	"""Test pour le filtrage des plans."""
	tracks = pd.read_csv(INPUT_DIR / "ref" / "stack-blinking.csv")
	fit = pd.read_csv(INPUT_DIR / "ref" / "stack-blinking-Fit.csv")
	instant_d = pd.read_csv(INPUT_DIR / "ref" / "stack-blinking-InD.csv")
	msd = pd.read_csv(INPUT_DIR / "ref" / "stack-blinking-MSD.csv")
	filters = Filters()
	f = Filtering(filters)

	res = f.tracks_compute(tracks, msd, instant_d, fit)
	ref = [47, 9, 9, 9]  # Même sans filtre, il ne conserve que l'intersection (36, 46, 57, 71, 75, 87, 89, 138, 154).
	for i in range(len(ref)): assert len(res[i]) == ref[i], f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {len(res[i])}"

	ft = filters.tracking
	ft["Length"].active = True
	ft["Length"].value = [3, 10000]
	ft["Instant D"].active = True
	ft["Instant D"].value = [0.01, 5]
	ft["D Coeff"].active = True
	ft["D Coeff"].value = [1, 5]
	ft["Speed"].active = True
	ft["Speed"].value = [-10, 10]
	ft["Alpha"].active = True
	ft["Confinement"].value = [-10, 10]
	res = f.tracks_compute(tracks, msd, instant_d, fit)
	ref = [16, 3, 3, 3]
	for i in range(len(ref)): assert len(res[i]) == ref[i], f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {len(res[i])}"

	ft["Length"].value = [42, 10000]
	res = f.tracks_compute(tracks, msd, instant_d, fit)
	ref = [0, 0, 0, 0]
	for i in range(len(ref)): assert len(res[i]) == ref[i], f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {len(res[i])}"
