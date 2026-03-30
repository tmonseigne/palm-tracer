import gc
import json
import os
import platform
import sys
import types

import cpuinfo
import napari
import psutil
import pytest
from pytest_metadata.plugin import metadata_key
from qtpy.QtWidgets import QApplication

from palm_tracer.Tools import Monitoring, Ui

os.environ["QT_QPA_PLATFORM"] = "offscreen"
os.environ["NAPARI_GUI_BACKEND"] = "none"
os.environ["VISPY_USE_APP"] = "mock"

all_tests_monitoring = Monitoring()


##################################################
@pytest.fixture
def qt_app():
	"""Fixture pour gérer une QApplication proprement"""
	from qtpy.QtWidgets import QApplication

	app = QApplication([])  # Initialisation de QApplication
	yield app
	# atexit.register(lambda: app.quit())  # Ajoutez un hook pour bien fermer QApplication

##################################################
@pytest.fixture
def fake_qfiledialog(monkeypatch):
	"""
	Fixture générique pour simuler QFileDialog.getOpenFileName et QFileDialog.getExistingDirectory sur n'importe quel module Qt qui a importé QFileDialog.

	Usage dans un test :

		import palm_tracer.GUI.AlignmentWidget as alignment_mod

		fake_qfiledialog(alignment_mod, "/chemin/vers/stack.tif")
		# ⇾ le prochain appel à alignment_mod.QFileDialog.getOpenFileName(...)
		#    renverra ("/chemin/vers/stack.tif", "TIFF images (*.tif *.tiff)")

		fake_qfiledialog(alignment_mod, None)
		# ⇾ simule un "Cancel" (aucun fichier choisi)
	"""

	def _factory(target, filename: str | None, filter_str: str = "TIFF images (*.tif *.tiff)"):
		"""
        Configure un faux QFileDialog.<method> dans le module donné.

		:param target: Module Python qui contient le symbole QFileDialog (ex. ``palm_tracer.UI.AlignmentWidget``).
		:param filename: Chemin complet du fichier à renvoyer. Mettre :obj:`None` pour simuler l'annulation.
		:param filter_str: Chaîne de filtre à renvoyer avec le filename (optionnel).
		"""

		# 1) Déterminer le module à partir de target
		if isinstance(target, types.ModuleType): module = target
		else: module = sys.modules[target.__module__]  # target est probablement une classe : on remonte à son module

		# Sanity check : QFileDialog doit exister dans ce module
		if not hasattr(module, "QFileDialog"): raise AttributeError(f"Le module {module.__name__!r} ne contient pas 'QFileDialog'.")

		def _fake_get_open_file_name(parent=None, caption="", directory="", *args, **kwargs):
			if filename is None: return "", ""  # Cas où l'utilisateur clique sur "Annuler"
			return filename, filter_str

		def _fake_get_existing_directory(parent=None, caption="", directory="", *args, **kwargs):
			if filename is None: return ""  # Cas où l'utilisateur clique sur "Annuler"
			return filename

		def _fake_get_save_file_name(parent=None, caption="", directory="", *args, **kwargs):
			if filename is None: return "", ""  # Cas où l'utilisateur clique sur "Annuler"
			return filename, filter_str

		# PATCH : on remplace les méthodes getOpenFileName et getExistingDirectory utilisées par ce module
		monkeypatch.setattr(module.QFileDialog, "getOpenFileName", _fake_get_open_file_name)
		monkeypatch.setattr(module.QFileDialog, "getSaveFileName", _fake_get_save_file_name)
		monkeypatch.setattr(module.QFileDialog, "getExistingDirectory", _fake_get_existing_directory)

	return _factory


##################################################
@pytest.fixture
def clean_napari(qtbot):
	"""
	Nettoie agressivement les viewers/fenêtres Napari avant et après un test.

	Cette fixture limite les effets de bord lorsqu'un test précédent a échoué
	pour de mauvaises raisons pendant son teardown.
	"""

	def _cleanup():
		# 1) Fermer les viewers Napari connus
		try:
			# Selon les versions, _instances peut être un WeakSet ou assimilé.
			instances = list(getattr(napari.viewer.Viewer, "_instances", []))
			for viewer in instances:
				try:
					if hasattr(viewer, "prepare_teardown"): viewer.prepare_teardown()
					# 2) dock widgets (cas le plus fréquent)
					if hasattr(viewer.window, "_dock_widgets"):
						for dock in viewer.window._dock_widgets.values():
							widget = dock.widget()
							if hasattr(widget, "prepare_teardown"):
								try: widget.prepare_teardown()
								except Exception: pass
				except Exception: pass

				try: viewer.close()
				except Exception: pass
		except Exception: pass

		# 2) Fermer toutes les fenêtres/top-level widgets Qt restantes
		try:
			app = QApplication.instance()
			if app is not None:
				for widget in list(app.topLevelWidgets()):
					try: widget.close()
					except Exception: pass
				app.processEvents()
		except Exception: pass

		# 3) GC pour aider les weakrefs / destructions tardives
		try: gc.collect()
		except Exception: pass

	# Nettoyage avant
	_cleanup()

	yield

	# Nettoyage après
	_cleanup()


##################################################
@pytest.fixture
def fake_napari_layers(monkeypatch):
	"""Bypass des méthodes d'ajout de layers Napari qui déclenchent VisPy/OpenGL."""

	class DummyLayer:
		def __init__(self, name=""):
			self.name = name
			self.editable = True
			self.visible = True

	def _factory(viewer):
		def _fake_add_points(self, *args, **kwargs): return DummyLayer(kwargs.get("name", "Localizations"))

		def _fake_add_tracks(self, *args, **kwargs): return DummyLayer(kwargs.get("name", "Tracks"))

		def _fake_add_image(self, *args, **kwargs): return DummyLayer(kwargs.get("name", "Visualization"))

		def _fake_index(self, layer): return 0

		def _fake_move(self, src, dst): return None

		monkeypatch.setattr(type(viewer), "add_points", _fake_add_points)
		monkeypatch.setattr(type(viewer), "add_tracks", _fake_add_tracks)
		monkeypatch.setattr(type(viewer), "add_image", _fake_add_image)

		# Patch temporaire uniquement sur la classe réelle de LayerList
		monkeypatch.setattr(type(viewer.layers), "index", _fake_index)
		monkeypatch.setattr(type(viewer.layers), "move", _fake_move)

	return _factory


##################################################
def cpu_infos() -> str:
	info = cpuinfo.get_cpu_info()
	res = info.get("brand_raw") or info.get("processor", "Unknown Processor")

	try:  # Cœurs / threads (tolérant aux erreurs) En cas de problème notamment sur mac
		cores = psutil.cpu_count(logical=False) or os.cpu_count()
		threads = psutil.cpu_count(logical=True) or os.cpu_count()
	except Exception: cores = threads = os.cpu_count()

	try:  # En cas de problème notamment sur mac
		freq = f"Unknown frequency"
		if hasattr(psutil, "cpu_freq"):
			cpu_info = psutil.cpu_freq(percpu=False)
			if cpu_info and getattr(cpu_info, "current", None): freq = f"{cpu_info.current / 1000:.2f} GHz"
		res += f" ({freq} - {cores} Cores ({threads} Logical))"
	except RuntimeError: res += "(No CPU Infos)"
	return res


##################################################
def add_to_json(path, datas_name, datas):
	try:
		with open(path) as f: data = json.load(f)
		data[datas_name] = datas
		with open(path, "w") as f: json.dump(data, f, indent=4)
	except FileNotFoundError: Ui.print_warning("Json File not found.")


##################################################
# Fonction pour configurer les métadonnées du rapport
@pytest.hookimpl
def pytest_metadata(metadata):
	metadata["System"] = platform.system()
	metadata["Platform"] = platform.platform()
	metadata["CPU"] = cpu_infos()
	metadata["RAM"] = f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB"

	## Ajout de la carte graphique si disponible
	try:
		from pynvml import nvmlInit, nvmlShutdown, nvmlDeviceGetHandleByIndex, nvmlDeviceGetName, nvmlDeviceGetMemoryInfo, nvmlDeviceGetCount

		nvmlInit()
		count = nvmlDeviceGetCount()
		if count > 0:
			handle = nvmlDeviceGetHandleByIndex(0)  # Premier GPU
			name_raw = nvmlDeviceGetName(handle)
			name = name_raw.decode("utf-8") if isinstance(name_raw, bytes) else name_raw
			memory = nvmlDeviceGetMemoryInfo(handle).total // (1024 * 1024)  # en Mo
			metadata["GPU"] = f"{name} (Memory: {memory} MB)"
		else:
			metadata["GPU"] = "No GPU found"
		nvmlShutdown()
	except Exception as e:
		metadata["GPU"] = f"Error detecting GPU: {str(e)}"


##################################################
@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
	global all_tests_monitoring
	all_tests_monitoring.start(0.1)


##################################################
@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
	global all_tests_monitoring
	all_tests_monitoring.stop()
	for ext in ["png", "html", "json", "txt"]:
		try: all_tests_monitoring.save(f"reports/monitoring.{ext}")
		except Exception as e: Ui.print_error(f"Unable to save monitoring in format {ext} : {e}")
	add_to_json("reports/test_report.json", "metadata", session.config.stash[metadata_key])


##################################################
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_protocol(item, nextitem):
	"""Capture les informations sur chaque test"""
	global all_tests_monitoring
	all_tests_monitoring.add_test_info(item.nodeid)
	return None
