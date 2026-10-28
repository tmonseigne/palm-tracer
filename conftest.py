"""Configure les fixtures et les hooks Pytest communs à la suite de tests."""

from __future__ import annotations

import json
import os
import platform
import shutil
import sys
import types
from contextlib import suppress
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import cpuinfo
import napari
import psutil
import pytest
from napari._qt.qt_viewer import QtViewer
from napari._vispy.canvas import VispyCanvas
from pytest_metadata.plugin import metadata_key
from qtpy.QtWidgets import QApplication

from palm_tracer.Tools import FileDialog, FileIO, Ui
from tests.Monitoring import Monitoring

os.environ["QT_QPA_PLATFORM"] = "offscreen"
os.environ["QT_OPENGL"] = "software"
os.environ["NAPARI_GUI_BACKEND"] = "none"
os.environ["VISPY_USE_APP"] = "mock"

all_tests_monitoring = Monitoring()


# ==================================================
# region Fixtures pytest
# ==================================================
@pytest.fixture
def import_without_dependency(monkeypatch):
	"""
	Fournit une fabrique important une copie isolée d'un module sans une dépendance optionnelle.

	:param monkeypatch: Fixture restaurant les importations et le registre des modules après le test.
	:return: Fabrique renvoyant le module chargé avec son mécanisme de repli.
	"""

	# --------------------------------------------------
	def _import(module_name: str, dependency: str):
		"""
		Simule une dépendance absente uniquement pendant l'importation de la copie.

		:param module_name: Nom du module applicatif déjà chargé.
		:param dependency: Nom exact de l'importation devant lever :class:`ImportError`.
		:return: Copie du module, sans remplacer le module applicatif original.
		"""
		alias = f"_test_{module_name.replace('.', '_')}"
		spec = spec_from_file_location(alias, sys.modules[module_name].__file__)
		assert spec is not None and spec.loader is not None
		module = module_from_spec(spec)
		original_import = __import__

		# --------------------------------------------------
		def _missing_import(name, global_vars=None, local_vars=None, fromlist=(), level=0):
			"""Refuse la dépendance ciblée et délègue toutes les autres importations."""
			if name == dependency: raise ImportError(f"Unavailable dependency: {dependency}")
			return original_import(name, global_vars, local_vars, fromlist, level)

		# Le patch d'import reste limité à l'exécution du module pour ne pas affecter les callbacks Qt.
		with monkeypatch.context() as context:
			context.setitem(sys.modules, alias, module)
			context.setattr("builtins.__import__", _missing_import)
			spec.loader.exec_module(module)
		return module

	return _import


# --------------------------------------------------
@pytest.fixture(autouse=True)
def isolated_user_config(monkeypatch, tmp_path):
	"""
	Isole les paramètres et modèles utilisateur de chaque test.

	:param monkeypatch: Fixture remplaçant temporairement les chemins de configuration.
	:param tmp_path: Dossier temporaire propre au test.
	:return: Dossier de configuration temporaire, créé uniquement par le code testé.
	"""
	folder = tmp_path / ".palm_tracer"
	monkeypatch.setattr(FileIO, "CONFIG_DIR", folder)
	for name in ("USER_SETTINGS_FILE", "USER_UI_STATE_FILE", "USER_ASTIGMATISM_MODEL", "DEFAULT_ASTIGMATISM_MODEL"):
		monkeypatch.setattr(FileIO, name, folder / getattr(FileIO, name).name)
	return folder


# --------------------------------------------------
@pytest.fixture
def user_model_path(isolated_user_config):
	"""Fournit le chemin temporaire du modèle astigmatique utilisateur."""
	return isolated_user_config / "astigmatism_3d_model.csv"


# --------------------------------------------------
@pytest.fixture
def copy_input(tmp_path):
	"""
	Fournit une fabrique copiant une entrée de référence dans le dossier temporaire du test.

	:param tmp_path: Dossier temporaire propre au test.
	:return: Fabrique renvoyant le chemin de la copie, fichier ou dossier.
	"""
	folder = Path(__file__).parent / "tests" / "input"

	# --------------------------------------------------
	def _copy(name: str) -> Path:
		"""
		Copie une entrée en conservant son nom et ses éventuels sous-dossiers.

		:param name: Chemin relatif de l'entrée dans ``tests/input``.
		:return: Chemin de la copie temporaire.
		"""
		source, destination = folder / name, tmp_path / name
		if not destination.exists():
			destination.parent.mkdir(parents=True, exist_ok=True)
			if source.is_dir(): shutil.copytree(source, destination)
			else: shutil.copy2(source, destination)
		return destination

	return _copy


# --------------------------------------------------
@pytest.fixture
def input_stack(copy_input):
	"""Fournit une copie temporaire de la pile principale."""
	return copy_input("stack.tif")


# --------------------------------------------------
@pytest.fixture
def output_folder(input_stack):
	"""Fournit le dossier de résultats associé à la pile temporaire, sans le créer."""
	return input_stack.with_name(f"{input_stack.stem}_PALM_Tracer")


# --------------------------------------------------
@pytest.fixture
def fake_qfiledialog(monkeypatch):
	"""
	Fixture générique pour simuler les sélecteurs Qt directs ou centralisés dans :mod:`palm_tracer.Tools.FileDialog`.

	Usage dans un test :

	import palm_tracer.GUI.AlignmentWidget as alignment_mod

	fake_qfiledialog(alignment_mod, "/chemin/vers/stack.tif")
	# ⇾ le prochain dialogue d'ouverture de l'outil
	#    renverra ("/chemin/vers/stack.tif", "TIFF images (*.tif *.tiff)")

	fake_qfiledialog(alignment_mod, None)
	# ⇾ simule un "Cancel" (aucun fichier choisi)

	:param monkeypatch: Fixture Pytest utilisée pour remplacer les méthodes de :class:`QFileDialog`.
	:return: Fabrique configurant les réponses simulées d'un :class:`QFileDialog`.
	"""

	# --------------------------------------------------
	def _factory(target, filename: str | list[str] | None, filter_str: str = "TIFF images (*.tif *.tiff)"):
		"""
		Configure les réponses des dialogues utilisés directement ou via FileDialog par le module donné.

		:param target: Module Python ou classe utilisant les dialogues (ex. ``palm_tracer.UI.AlignmentWidget``).
		:param filename: Chemin complet du fichier à renvoyer, liste de chemins pour une sélection multiple ou :obj:`None` pour simuler l'annulation.
		:param filter_str: Chaîne de filtre à renvoyer avec le filename (optionnel).
		"""

		# 1) Déterminer le module à partir de target
		# Pour une classe, retrouve le module qui la définit.
		module = target if isinstance(target, types.ModuleType) else sys.modules[target.__module__]

		# Les widgets délèguent désormais leurs dialogues au module FileDialog commun.
		dialog = getattr(module, "QFileDialog", FileDialog.QFileDialog)

		# --------------------------------------------------
		def _fake_get_open_file_name(parent=None, caption="", directory="", *args, **kwargs):
			"""
			Simule la sélection d'un fichier à ouvrir.

			:param parent: Widget parent.
			:param caption: Titre de la boîte de dialogue.
			:param directory: Dossier initial de la boîte de dialogue.
			:param args: Arguments positionnels ignorés par le substitut.
			:param kwargs: Arguments nommés utilisés pour configurer le substitut.
			:return: Nom de fichier et filtre simulés.
			"""
			if filename is None: return "", ""  # Cas où l'utilisateur clique sur "Annuler"
			return filename, filter_str

		# --------------------------------------------------
		def _fake_get_open_file_names(parent=None, caption="", directory="", *args, **kwargs):
			"""
			Simule la sélection de plusieurs fichiers à ouvrir.

			:param parent: Widget parent.
			:param caption: Titre de la boîte de dialogue.
			:param directory: Dossier initial de la boîte de dialogue.
			:param args: Arguments positionnels ignorés par le substitut.
			:param kwargs: Arguments nommés utilisés pour configurer le substitut.
			:return: Liste des noms de fichiers et filtre simulés.
			"""
			if filename is None: return [], ""  # Cas où l'utilisateur clique sur "Annuler"
			return ([filename] if isinstance(filename, str) else filename), filter_str

		# --------------------------------------------------
		def _fake_get_existing_directory(parent=None, caption="", directory="", *args, **kwargs):
			"""
			Simule la sélection d'un dossier existant.

			:param parent: Widget parent.
			:param caption: Titre de la boîte de dialogue.
			:param directory: Dossier initial de la boîte de dialogue.
			:param args: Arguments positionnels ignorés par le substitut.
			:param kwargs: Arguments nommés utilisés pour configurer le substitut.
			:return: Dossier simulé.
			"""
			if filename is None: return ""  # Cas où l'utilisateur clique sur "Annuler"
			return filename

		# --------------------------------------------------
		def _fake_get_save_file_name(parent=None, caption="", directory="", *args, **kwargs):
			"""
			Simule la sélection d'un fichier à enregistrer.

			:param parent: Widget parent.
			:param caption: Titre de la boîte de dialogue.
			:param directory: Dossier initial de la boîte de dialogue.
			:param args: Arguments positionnels ignorés par le substitut.
			:param kwargs: Arguments nommés utilisés pour configurer le substitut.
			:return: Nom de fichier et filtre simulés.
			"""
			if filename is None: return "", ""  # Cas où l'utilisateur clique sur "Annuler"
			return filename, filter_str

		# PATCH : on remplace les méthodes de QFileDialog utilisées par ce module
		monkeypatch.setattr(dialog, "getOpenFileName", _fake_get_open_file_name)
		monkeypatch.setattr(dialog, "getOpenFileNames", _fake_get_open_file_names)
		monkeypatch.setattr(dialog, "getSaveFileName", _fake_get_save_file_name)
		monkeypatch.setattr(dialog, "getExistingDirectory", _fake_get_existing_directory)

	return _factory


# --------------------------------------------------
@pytest.fixture
def patched_napari_viewer(monkeypatch, qtbot):
	"""
	Sécurise la création d'un viewer Napari en environnement de test/CI.

	Cette fixture :
	- neutralise les accès OpenGL problématiques lors de l'initialisation du canvas ;
	- désactive la création réelle des layers VisPy ;
	- effectue un nettoyage agressif avant et après le test pour limiter les
	  effets de bord entre tests.

	Attention :
	- le patch OpenGL doit être appliqué avant l'appel à ``make_napari_viewer()`` ;
	- cette fixture vise des tests unitaires/Qt, pas des tests de rendu réel.

	:param monkeypatch: Fixture Pytest utilisée pour remplacer temporairement les composants graphiques.
	:param qtbot: Fixture pytest-qt utilisée pour gérer l'environnement Qt du test.
	"""

	# --------------------------------------------------
	def _cleanup():
		"""Ferme les viewers/fenêtres Napari et les top-level widgets Qt restants."""
		try:
			# Selon les versions, _instances peut être un WeakSet ou assimilé.
			instances = list(getattr(napari.viewer.Viewer, "_instances", []))
			for viewer in instances:
				with suppress(Exception): viewer.close()
		except Exception: pass

		# 2) Fermer toutes les fenêtres/top-level widgets Qt restantes
		try:
			app = QApplication.instance()
			if app is not None:
				for widget in list(app.topLevelWidgets()):
					with suppress(Exception): widget.close()
				app.processEvents()
		except Exception: pass

	# 3) GC pour aider les weakrefs / destructions tardives
	# try: gc.collect()
	# except Exception: pass

	# --- nettoyage avant test
	_cleanup()

	# --- patch OpenGL et VisPy
	monkeypatch.setattr("napari._vispy.utils.gl.get_max_texture_sizes", lambda: (4096, 4096), raising=True)
	monkeypatch.setattr("napari._vispy.canvas.get_max_texture_sizes", lambda: (4096, 4096), raising=True)
	monkeypatch.setattr("napari._vispy.canvas.VispyCanvas._clean_and_update_scenegraph", lambda self: None, raising=True)
	monkeypatch.setattr("napari._vispy.canvas.VispyCanvas._resume_scene_graph_update", lambda self: None, raising=True)
	with suppress(Exception): monkeypatch.setattr("vispy.app.backends._qt.get_physical_dpi", lambda *args, **kwargs: 96, raising=True)

	# --------------------------------------------------
	def _fake_add_layer(self, layer):
		"""
		Simule l'ajout d'un calque à la liste.

		:param layer: Calque concerné.
		:return: Toujours ``None``.
		"""
		return None  # Ignore la création réelle du visuel VisPy associé à un layer.

	# --------------------------------------------------
	def _fake_remove_layer(self, event):
		"""
		Simule le retrait d'un calque de la liste.

		:param event: Événement décrivant le calque retiré.
		:return: Toujours ``None``.
		"""
		return None  # Ignore la suppression réelle du visuel VisPy associé à un layer.

	# --------------------------------------------------
	def _fake_reorder_layers(self):
		"""
		Simule la réorganisation des calques.

		:return: Toujours ``None``.
		"""
		return None  # Ignore le réordonnancement réel des visuels VisPy.

	monkeypatch.setattr(QtViewer, "_add_layer", _fake_add_layer, raising=True)
	monkeypatch.setattr(VispyCanvas, "_remove_layer", _fake_remove_layer, raising=True)
	monkeypatch.setattr(VispyCanvas, "_reorder_layers", _fake_reorder_layers, raising=True)

	yield

	# --- nettoyage après test
	_cleanup()


# ==================================================
# endregion Fixtures pytest
# ==================================================

# ==================================================
# region Hooks pytest
# ==================================================
def _is_qt_or_napari_test(item) -> bool:
	"""Indique si le test utilise Qt ou Napari."""
	if item is None: return False
	fixture_names = set(getattr(item, "fixturenames", []))
	keywords = set(item.keywords)
	nodeid = str(getattr(item, "nodeid", "")).lower()

	return bool({"qtbot", "patched_napari_viewer"} & fixture_names
				or {"qt", "napari"} & keywords
				or "napari" in nodeid or "qt" in nodeid or "gui" in nodeid)


# --------------------------------------------------
def cpu_infos() -> str:
	"""
	Collecte les informations relatives au processeur.

	:return: Informations disponibles sur le processeur.
	"""
	info = cpuinfo.get_cpu_info()
	res = info.get("brand_raw") or info.get("processor", "Unknown Processor")

	try:  # Cœurs / threads (tolérant aux erreurs) En cas de problème notamment sur mac
		cores = psutil.cpu_count(logical=False) or os.cpu_count()
		threads = psutil.cpu_count(logical=True) or os.cpu_count()
	except Exception: cores = threads = os.cpu_count()

	try:  # En cas de problème notamment sur mac
		freq = "Unknown frequency"
		if hasattr(psutil, "cpu_freq"):
			cpu_info = psutil.cpu_freq(percpu=False)
			if cpu_info and getattr(cpu_info, "current", None): freq = f"{cpu_info.current / 1000:.2f} GHz"
		res += f" ({freq} - {cores} Cores ({threads} Logical))"
	except RuntimeError: res += "(No CPU Infos)"
	return res


# --------------------------------------------------
def add_to_json(path, datas_name, datas):
	"""
	Ajoute des données à un fichier JSON.

	:param path: Chemin du fichier JSON.
	:param datas_name: Clé des données à ajouter.
	:param datas: Données à ajouter.
	"""
	try:
		with open(path) as f: data = json.load(f)
		data[datas_name] = datas
		with open(path, "w") as f: json.dump(data, f, indent=4)
	except FileNotFoundError: Ui.print_warning("Json File not found.")


# --------------------------------------------------
# Fonction pour configurer les métadonnées du rapport
# --------------------------------------------------
@pytest.hookimpl
def pytest_metadata(metadata):
	"""
	Complète les métadonnées du rapport Pytest.

	:param metadata: Métadonnées du rapport Pytest.
	"""
	metadata["System"] = platform.system()
	metadata["Platform"] = platform.platform()
	metadata["CPU"] = cpu_infos()
	metadata["RAM"] = f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB"

	## Ajout de la carte graphique si disponible
	try:
		from pynvml import nvmlDeviceGetCount, nvmlDeviceGetHandleByIndex, nvmlDeviceGetMemoryInfo, nvmlDeviceGetName, nvmlInit, nvmlShutdown

		nvmlInit()
		count = nvmlDeviceGetCount()
		if count > 0:
			handle = nvmlDeviceGetHandleByIndex(0)  # Premier GPU
			name_raw = nvmlDeviceGetName(handle)
			name = name_raw.decode("utf-8") if isinstance(name_raw, bytes) else name_raw
			memory = nvmlDeviceGetMemoryInfo(handle).total // (1024 * 1024)  # Taille en Mo
			metadata["GPU"] = f"{name} (Memory: {memory} MB)"
		else:
			metadata["GPU"] = "No GPU found"
		nvmlShutdown()
	except Exception as e:
		metadata["GPU"] = f"Error detecting GPU: {str(e)}"


# --------------------------------------------------
@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
	"""
	Initialise les mesures au démarrage de la session Pytest.

	:param session: Session Pytest.
	"""
	global all_tests_monitoring
	all_tests_monitoring.start(0.1)


# --------------------------------------------------
@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
	"""
	Finalise et enregistre les mesures de la session Pytest.

	:param session: Session Pytest.
	:param exitstatus: Code de sortie de la session Pytest.
	"""
	global all_tests_monitoring
	all_tests_monitoring.stop()
	for ext in ["png", "html", "json", "txt"]:
		try: all_tests_monitoring.save(f"reports/monitoring.{ext}")
		except Exception as e: Ui.print_error(f"Unable to save monitoring in format {ext} : {e}")
	add_to_json("reports/test_report.json", "metadata", session.config.stash[metadata_key])


# --------------------------------------------------
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_protocol(item, nextitem):
	"""Capture les informations sur chaque test."""
	global all_tests_monitoring
	all_tests_monitoring.add_test_info(item.nodeid)
	return None


# --------------------------------------------------
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
	"""À l'initialisation de chaque test."""
	global all_tests_monitoring
	if _is_qt_or_napari_test(item) and all_tests_monitoring.is_running: all_tests_monitoring.pause()


# --------------------------------------------------
@pytest.hookimpl(trylast=True)
def pytest_runtest_teardown(item, nextitem):
	"""Au nettoyage de chaque test."""
	global all_tests_monitoring
	if _is_qt_or_napari_test(item) and not _is_qt_or_napari_test(nextitem): all_tests_monitoring.resume()
# ==================================================
# endregion Hooks pytest
# ==================================================
