""" Fichier des tests pour la lecture/écriture des fichiers. """
import shutil

import pytest

from palm_tracer._tests.Utils import *
from palm_tracer.Tools.FileMigrator import FileMigrator

INPUT_FOLDER = INPUT_DIR / "stack.PT"
OUTPUT_FOLDER = INPUT_DIR / "stack_PALM_Tracer"


##################################################
def test_open():
	""" Test de la classe FileMigrator. """
	m = FileMigrator()

	with pytest.raises(ValueError) as exception_info: m.open(INPUT_DIR)
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."

	with pytest.raises(NotADirectoryError) as exception_info: m.open(INPUT_DIR / "stack.tif")
	assert exception_info.type == NotADirectoryError, "L'erreur relevé n'est pas correcte."

	with pytest.raises(FileNotFoundError) as exception_info: m.open(Path("Bad Folder"))
	assert exception_info.type == FileNotFoundError, "L'erreur relevé n'est pas correcte."

	m.open(INPUT_FOLDER)


##################################################
def test_update_meta(capsys):
	"""Test basique de update_meta."""
	m = FileMigrator()

	ref = np.zeros(6) - 1
	assert np.allclose(m.meta, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {m.meta}"

	m.update_meta("Height", 1)  # Mise à Jour
	ref[0] = 1
	assert np.allclose(m.meta, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {m.meta}"
	m.update_meta("Height", 1)  # Données identique
	assert np.allclose(m.meta, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {m.meta}"
	m.update_meta("Height", 2)  # DOnnées différentes
	out, err = capsys.readouterr()
	assert "Warning that the 'Height' metadata differs between several files to be migrated (1 VS 2)." in out
	assert np.allclose(m.meta, ref, atol=0, rtol=0), f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {m.meta}"


##################################################
def test_open_old_file():
	"""Test basique de open_old_file."""
	m = FileMigrator()

	with pytest.raises(FileNotFoundError) as exception_info: m.open_old_file(INPUT_FOLDER)
	assert exception_info.type == FileNotFoundError, "L'erreur relevé n'est pas correcte."

	with pytest.raises(ValueError) as exception_info: m.open_old_file(INPUT_DIR / "File-01.txt", skiprows=4)
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."

	df, header = m.open_old_file(INPUT_FOLDER / "3DFit.txt", header=False, skiprows=2)
	assert len(header) == 2, "Nombre de lignes incorrect."
	assert df.shape == (2, 5), "Taille du Dataframe incorrect."


##################################################
def test_open_old_irregular_file():
	"""Test basique de open_old_file."""
	m = FileMigrator()

	with pytest.raises(FileNotFoundError) as exception_info: m.open_old_irregular_file(INPUT_FOLDER)
	assert exception_info.type == FileNotFoundError, "L'erreur relevé n'est pas correcte."

	with pytest.raises(ValueError) as exception_info: m.open_old_irregular_file(INPUT_DIR / "File-01.txt", skiprows=4)
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."

	df, header = m.open_old_irregular_file(INPUT_FOLDER / "trcPALMTracer-Full-Dinst.txt", skiprows=15)
	assert len(header) == 15, "Nombre de lignes incorrect."
	assert df.empty, "Taille du Dataframe incorrect."

	df, header = m.open_old_irregular_file(INPUT_FOLDER / "trcPALMTracer-Full-Dinst.txt", skiprows=2)
	assert len(header) == 2, "Nombre de lignes incorrect."
	assert df.shape == (13, 7), "Taille du Dataframe incorrect."


##################################################
def test_column_migrator():
	"""Test basique de column_migrator."""
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


##################################################
def test_analyze():
	""" Test de la classe FileMigrator. """
	m = FileMigrator()
	print(m.input_folder)
	with pytest.raises(RuntimeError) as exception_info: m.analyze()
	assert exception_info.type == RuntimeError, "L'erreur relevé n'est pas correcte."

	m.open(INPUT_FOLDER)
	m.analyze()
	m.analyze()  # Lancement successif pour vérifier le nettoyage des listes de fichiers.

	for key in m.FILES_LINK:
		res, ref = str(m.files[key][0]), str(INPUT_FOLDER / m.FILES_LINK[key].old)
		assert len(m.files["loc"]) == 1, f"Plus d'un fichier a été trouvé pour la clé {key}."
		assert res == ref, f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"

	assert len(m.files["Unused"]) == 3, "Les trois fichiers de log n'ont pas été trouvé."


##################################################
def test_migrate():
	""" Test de la classe FileMigrator. """
	m = FileMigrator()
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)  # Supprime récursivement le dossier et tout son contenu pour n'avoir rien à charger.

	with pytest.raises(RuntimeError) as exception_info: m.migrate()
	assert exception_info.type == RuntimeError, "L'erreur relevé n'est pas correcte."

	m.open(INPUT_FOLDER)
	m.migrate()  # Sans analyse avant, il va créé le dossier puis ne rien faire à chaque élément
	assert OUTPUT_FOLDER.exists(), "Le dossier de sortie aurait du être créé."
	assert OUTPUT_FOLDER.is_dir(), "Le chemin de sortie n'est pas un dossier."
	assert not any(OUTPUT_FOLDER.iterdir()), "Le dossier de sortie devrait être vide."
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)  # Supprimer le dossier

	m.analyze()
	m.migrate()
	for ref_file in sorted((REF_DIR / "stack_PALM_Tracer").glob("*.csv")):
		res_file = sorted(OUTPUT_FOLDER.glob(f"{ref_file.stem}-*.csv"))[0]
		ref, res = pd.read_csv(ref_file), pd.read_csv(res_file)
		ref, res = ref.apply(pd.to_numeric, errors="ignore"), res.apply(pd.to_numeric, errors="ignore")
		pd.testing.assert_frame_equal(ref, res, check_dtype=False), f"Résultat incorrect.\nAttendu : {ref}\nObtenu : {res}"
	shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
