import json
import os
import platform
import sys
import types

import cpuinfo
import psutil
import pytest
from pytest_metadata.plugin import metadata_key

from palm_tracer.Tools import Monitoring, print_error, print_warning

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
def fake_getopenfilename(monkeypatch):
	"""
	Fixture générique pour simuler QFileDialog.getOpenFileName sur n'importe
	quel module Qt qui a importé QFileDialog.

	Usage dans un test :

		import palm_tracer.GUI.AlignmentWidget as alignment_mod

		fake_getopenfilename(alignment_mod, "/chemin/vers/stack.tif")
		# -> le prochain appel à alignment_mod.QFileDialog.getOpenFileName(...)
		#    renverra ("/chemin/vers/stack.tif", "TIFF images (*.tif *.tiff)")

		fake_getopenfilename(alignment_mod, None)
		# -> simule un "Cancel" (aucun fichier choisi)
	"""

	def _factory(target, filename: str | None, filter_str: str = "TIFF images (*.tif *.tiff)"):
		"""
		Configure un faux QFileDialog.getOpenFileName dans le module donné.

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

		# PATCH : on remplace la méthode getOpenFileName utilisée par ce module
		monkeypatch.setattr(module.QFileDialog, "getOpenFileName", _fake_get_open_file_name)

	return _factory


##################################################
def cpu_infos() -> str:
	info = cpuinfo.get_cpu_info()
	res = info.get("brand_raw") or info.get("processor", "Unknown Processor")

	try:  # Coeurs / threads (tolérant aux erreurs) En cas de problème notamment sur mac
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
	except FileNotFoundError: print_warning("Json File not found.")


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
		except Exception as e: print_error(f"Impossible de sauvegarder le monitoring au format {ext} : {e}")
	add_to_json("reports/test_report.json", "metadata", session.config.stash[metadata_key])


##################################################
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_protocol(item, nextitem):
	"""Capture les informations sur chaque test"""
	global all_tests_monitoring
	all_tests_monitoring.add_test_info(item.nodeid)
	return None
