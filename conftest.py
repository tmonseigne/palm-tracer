import json
import os
import platform

import cpuinfo
import psutil
import pytest
from pytest_metadata.plugin import metadata_key

from palm_tracer.Tools import Monitoring, print_error, print_warning

os.environ["QT_QPA_PLATFORM"] = "offscreen"

all_tests_monitoring = Monitoring()


##################################################
@pytest.fixture
def qt_app():
	"""Fixture pour gérer une QApplication proprement"""
	from qtpy.QtWidgets import QApplication

	app = QApplication([])  # Initialisation de QApplication
	yield app
	#atexit.register(lambda: app.quit())  # Ajoutez un hook pour bien fermer QApplication


##################################################
def cpu_infos() -> str:
	info = cpuinfo.get_cpu_info()
	res = info.get("processor", "Unknown Processor")
	try:  # En cas de problème notamment sur mac
		cpu_info = psutil.cpu_freq(percpu=False)
		res += f" ({cpu_info.current / 1000} GHz - {psutil.cpu_count(logical=False)} Cores ({psutil.cpu_count(logical=True)} Logical))"
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
