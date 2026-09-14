"""Teste la migration des anciens résultats Metamorph."""

import shutil

import pytest

from palm_tracer._tests.Utils import *
from palm_tracer.Tools.FileMigrator import FileMigrator

INPUT_FOLDER = INPUT_DIR / "stack.PT"
OUTPUT_FOLDER = INPUT_DIR / "stack_PALM_Tracer"


# ==================================================
# region Analyse et orchestration
# ==================================================
##################################################
def test_open():
	"""Vérifie la classe FileMigrator."""
	m = FileMigrator()

	m.open(INPUT_FOLDER)


##################################################
@pytest.mark.parametrize("args, kwargs, error", [
		pytest.param((INPUT_DIR,), {}, ValueError, id="directory-without-results"),
		pytest.param((INPUT_DIR / 'stack.tif',), {}, NotADirectoryError, id="file-instead-of-directory"),
		pytest.param((Path('Bad Folder'),), {}, FileNotFoundError, id="missing-directory")])
def test_open_invalid(args, kwargs, error):
	"""Vérifie les erreurs attendues avant toute ouverture valide."""
	with pytest.raises(error): FileMigrator().open(*args, **kwargs)


##################################################
def test_analyze():
	"""Vérifie la classe FileMigrator."""
	m = FileMigrator()
	print(m.input_folder)

	m.open(INPUT_FOLDER)
	m.analyze()
	m.analyze()  # Lancement successif pour vérifier le nettoyage des listes de fichiers.

	for key in m.FILES_LINK:
		res, ref = str(m.files[key][0]), str(INPUT_FOLDER / m.FILES_LINK[key].old)
		assert len(m.files["loc"]) == 1, f"Plus d'un fichier a été trouvé pour la clé {key}."
		assert res == ref, f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	assert len(m.files["Unused"]) == 3, "Les trois fichiers de log n'ont pas été trouvé."


##################################################
@pytest.mark.parametrize("args, kwargs, error", [pytest.param((), {}, RuntimeError, id="no-directory")])
def test_analyze_invalid(args, kwargs, error):
	"""Vérifie les erreurs attendues avant toute ouverture valide."""
	with pytest.raises(error): FileMigrator().analyze(*args, **kwargs)


##################################################
def test_migrate(capsys):
	"""Vérifie la classe FileMigrator."""
	m = FileMigrator()
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)  # Supprime récursivement le dossier et tout son contenu pour n'avoir rien à charger.

	m.open(INPUT_FOLDER)
	m.migrate()  # Sans analyse avant, il va créer le dossier puis ne rien faire à chaque élément
	lines = get_lines_output(capsys)
	assert len(lines) == 6  # Pour les 6 fichiers
	assert OUTPUT_FOLDER.exists(), "Le dossier de sortie aurait du être créé."
	assert OUTPUT_FOLDER.is_dir(), "Le chemin de sortie n'est pas un dossier."
	assert not any(OUTPUT_FOLDER.iterdir()), "Le dossier de sortie devrait être vide."
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)  # Supprimer le dossier

	m.analyze()
	m.migrate()
	lines = get_lines_output(capsys)
	assert len(lines) == 7  # Pour les 6 fichiers et le warning de taille
	for ref_file in sorted((REF_DIR / "stack_PALM_Tracer").glob("*.csv")):
		res_file = sorted(OUTPUT_FOLDER.glob(f"{ref_file.stem}-*.csv"))[0]
		ref, res = pd.read_csv(ref_file), pd.read_csv(res_file)
		ref, res = ref.apply(pd.to_numeric, errors="coerce"), res.apply(pd.to_numeric, errors="coerce")
		pd.testing.assert_frame_equal(ref, res, check_dtype=False), f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)


##################################################
@pytest.mark.parametrize("args, kwargs, error", [pytest.param((), {}, RuntimeError, id="no-directory")])
def test_migrate_invalid(args, kwargs, error):
	"""Vérifie les erreurs attendues avant toute ouverture valide."""
	with pytest.raises(error): FileMigrator().migrate(*args, **kwargs)


# ==================================================
# endregion Analyse et orchestration
# ==================================================

# ==================================================
# region Migration des fichiers
# ==================================================
##################################################
def test_update_meta(capsys):
	"""Vérifie update_meta."""
	m = FileMigrator()

	ref = np.zeros(6) - 1
	assert np.allclose(m.meta, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {m.meta}"

	m.update_meta("Height", 1)  # Mise à Jour
	ref[0] = 1
	assert np.allclose(m.meta, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {m.meta}"
	m.update_meta("Height", 1)  # Données identiques
	assert np.allclose(m.meta, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {m.meta}"
	m.update_meta("Height", 2)  # Données différentes
	lines = get_lines_output(capsys)
	assert "Warning that the 'Height' metadata differs between several files to be migrated (1 VS 2)." in lines[0]
	assert np.allclose(m.meta, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {m.meta}"


# ==================================================
# endregion Migration des fichiers
# ==================================================

# ==================================================
# region Outils de conversion
# ==================================================
##################################################
def test_open_old_file():
	"""Vérifie open_old_file."""
	m = FileMigrator()

	df, header = m.open_old_file(INPUT_FOLDER / "3DFit.txt", header=False, skiprows=2)
	assert len(header) == 2, "Nombre de lignes incorrect."
	assert df.shape == (2, 5), "Taille du Dataframe incorrect."


##################################################
@pytest.mark.parametrize("args, kwargs, error", [
		pytest.param((INPUT_FOLDER,), {}, FileNotFoundError, id="directory-instead-of-file"),
		pytest.param((INPUT_DIR / 'File-01.txt',), {'skiprows': 4}, ValueError, id="invalid-content")])
def test_open_old_file_invalid(args, kwargs, error):
	"""Vérifie les erreurs attendues avant toute ouverture valide."""
	with pytest.raises(error): FileMigrator().open_old_file(*args, **kwargs)


##################################################
def test_open_old_irregular_file():
	"""Vérifie open_old_file."""
	m = FileMigrator()

	df, header = m.open_old_irregular_file(INPUT_FOLDER / "trcPALMTracer-Full-Dinst.txt", skiprows=15)
	assert len(header) == 15, "Nombre de lignes incorrect."
	assert df.empty, "Taille du Dataframe incorrect."

	df, header = m.open_old_irregular_file(INPUT_FOLDER / "trcPALMTracer-Full-Dinst.txt", skiprows=2)
	assert len(header) == 2, "Nombre de lignes incorrect."
	assert df.shape == (13, 7), "Taille du Dataframe incorrect."


##################################################
@pytest.mark.parametrize("args, kwargs, error", [
		pytest.param((INPUT_FOLDER,), {}, FileNotFoundError, id="directory-instead-of-file"),
		pytest.param((INPUT_DIR / 'File-01.txt',), {'skiprows': 4}, ValueError, id="invalid-content")])
def test_open_old_irregular_file_invalid(args, kwargs, error):
	"""Vérifie les erreurs attendues avant toute ouverture valide."""
	with pytest.raises(error): FileMigrator().open_old_irregular_file(*args, **kwargs)


##################################################
def test_column_migrator():
	"""Vérifie column_migrator."""
	m = FileMigrator()
	data = ["MSe", "MSE(Gauss)", "Angle(Rad)", "CentroidX", "Centroid Y", "Centroid Z (nm)", "SigmaX", "Sigma y",
			"Intensity_0", "Intensity Offset", "Intensity", "IntegratedIntensity",
			"Id", "Plane", "Index", "Channel", "Surface", "Circularity", "Track", "pairdistance", "MSE_Z(um)", "B l_An()k"]
	ref = ["MSE XY", "MSE XY", "Theta", "X", "Y", "Z", "Sigma X", "Sigma Y",
		   "Intensity 0", "Intensity Offset", "Intensity", "Integrated Intensity",
		   "Id", "Plane", "Index", "Channel", "Surface", "Circularity", "Track", "Pair Distance", "MSE Z", "blank"]

	for i in range(len(data)):
		res = m.column_migrator(data[i])
		assert ref[i] == res, f"Résultat incorrect.\nAttendu : {ref[i]}\nObtenu : {res}"

# ==================================================
# endregion Outils de conversion
# ==================================================
