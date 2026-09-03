"""Teste la surveillance des ressources système."""

import time

import psutil
from plotly.subplots import make_subplots

from palm_tracer._tests.Utils import *
from palm_tracer.Tools import Monitoring

try:
	import torch

	HAVE_GPU = not os.getenv("GITHUB_ACTIONS") == "true"
except ImportError:
	HAVE_GPU = False

default_duration = 2


# ==================================================
# region Simulations
# ==================================================
##################################################
def simulate_cpu_usage(monitoring: Monitoring, intensity: int = 1000000, duration: float = default_duration):
	"""
	Simule une utilisation importante de CPU en effectuant des calculs intensifs.

	:param monitoring: Moniteur à manipuler.
	:param duration: Durée pendant laquelle le CPU sera sollicité (en secondes).
	:param intensity: Nombre de calculs dans chaque itération (détermine l'intensité).
	"""
	monitoring.add_test_info("_tests/test_simulation_cpu.py::test_high_cpu_usage")
	print(f"Simulating high CPU usage for {duration} seconds...")
	start_time = time.time()
	while time.time() - start_time < duration:
		_ = [x ** 2 for x in range(intensity)]  # Effectue des calculs inutiles pour simuler une charge CPU
	print("CPU simulation complete.")


##################################################
def simulate_gpu_usage(monitoring: Monitoring, tensor_size: int = 4096, duration: float = default_duration):
	"""
	Simule une utilisation importante de GPU en effectuant des calculs intensifs.

	:param monitoring: Moniteur à manipuler.
	:param tensor_size: Taille des matrices carrées utilisées pour les calculs.
	:param duration: Durée en secondes pendant lesquelles les opérations GPU sont répétées.
	"""
	monitoring.add_test_info("_tests/test_simulation_gpu.py::test_gpu_computation")
	# Installation de pytorch via le generatuer de lien de leur site en fonction de votre CUDA
	# Ex : pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
	if not torch.cuda.is_available():
		print("Aucun GPU CUDA disponible pour la simulation.")
		return

	print(f"Simulating GPU usage for {duration} seconds with matrix size {tensor_size}x{tensor_size}...")
	start_time = time.time()
	a = torch.randn((tensor_size, tensor_size), device="cuda")
	b = torch.randn((tensor_size, tensor_size), device="cuda")
	while time.time() - start_time < duration:
		c = torch.matmul(a, b)  # Multiplication matricielle sur le GPU
		_ = c.sum().item()  # .	  Force le calcul immédiat (évite lazy eval de PyTorch)

	torch.cuda.empty_cache()
	print("GPU simulation complete.")


##################################################
def simulate_memory_usage(monitoring: Monitoring, size: int = 50, duration: float = default_duration):
	"""
	Simule une utilisation importante de mémoire en allouant un tableau de bytes.

	:param monitoring: Moniteur à manipuler.
	:param size: Taille totale de mémoire à allouer (en mégaoctets).
	:param duration: Temps pendant lequel la mémoire reste allouée (en secondes).
	"""
	monitoring.add_test_info("_tests/test_simulation_memory.py::test_allocate_memory")
	print(f"Allocating {size} MB of memory...")
	allocated_memory = bytearray(size * 1024 * 1024)  # Alloue un tableau de bytes
	monitoring.add_test_info("_tests/test_simulation_memory.py::test_hold_memory")
	print(f"Memory allocated. Holding for {duration} seconds...")
	time.sleep(duration)  # .							Garde la mémoire allouée pour observer l'impact
	monitoring.add_test_info("_tests/test_simulation_memory.py::test_release_memory")
	print("Releasing memory.")
	del allocated_memory  # .							Libère la mémoire


##################################################
def simulate_disk_io(monitoring: Monitoring, file_size: int = 1, duration: float = default_duration, file_name: str = "temp_test_file.bin"):
	"""
	Simule des opérations intensives de disque en écrivant et lisant un fichier volumineux.

	:param monitoring: Moniteur à manipuler.
	:param file_size: Taille du fichier à écrire (en mégaoctets).
	:param duration: Temps pendant lequel le fichier est maintenu sur le disque (en secondes).
	:param file_name: Nom du fichier temporaire utilisé pour l'opération.
	"""
	monitoring.add_test_info("_tests/test_simulation_disk.py::test_disk_write")
	print(f"Writing a file of size {file_size} MB...")
	with open(file_name, "wb") as f: f.write(bytearray(file_size * 1024 * 1024))  # Écriture d'un fichier de la taille spécifiée

	monitoring.add_test_info("_tests/test_simulation_disk.py::test_disk_hold")
	print(f"File written. Holding for {duration} seconds...")
	time.sleep(duration)  # Maintient le fichier pour observer son impact

	monitoring.add_test_info("_tests/test_simulation_disk.py::test_disk_delete")
	print("Deleting the file...")
	os.remove(file_name)  # Supprime le fichier
	print("Disk I/O simulation complete.")


# ==================================================
# endregion Simulations
# ==================================================


##################################################
def test_monitoring():
	"""Vérifie la classe."""
	monitoring = Monitoring()
	monitoring.start(0.1)
	time.sleep(1)
	monitoring.pause()
	time.sleep(1)
	monitoring.resume()
	monitoring.resume()
	time.sleep(1)
	monitoring.stop()
	print(f"\n{monitoring}")


##################################################
def test_monitoring_draw_test_section():
	"""Vérifie l'ajout groupé d'une section de tests à une figure Plotly."""
	figure = make_subplots(rows=2, cols=1)
	tests = [
		{"File": "Monitoring", "Test": "Premier", "Timestamp": 0.0},
		{"File": "Monitoring", "Test": "Second", "Timestamp": 1.0},
	]

	Monitoring.draw_test_section(figure, [0.0, 100.0], tests, {"Monitoring": "blue"}, 2.0, 2)

	assert len(figure.data) == 2
	assert len(figure.layout.shapes) == 2
	assert [trace.name for trace in figure.data] == ["Monitoring - Premier", "Monitoring - Second"]
	assert [trace.xaxis for trace in figure.data] == ["x2", "x2"]
	assert [shape.xref for shape in figure.layout.shapes] == ["x2", "x2"]
	assert [shape.yref for shape in figure.layout.shapes] == ["y2", "y2"]


##################################################
def test_monitoring_draw():
	"""Vérifie la construction groupée des traces et des zones du graphique."""
	monitoring = Monitoring()
	monitoring._times = [0.0, 1.0, 2.0]
	monitoring._cpu = [10.0, 20.0, 30.0]
	monitoring._gpu = [0.0, 0.0, 0.0]
	monitoring._memory = [100.0, 110.0, 120.0]
	monitoring._disk = [0.0, 1.0, 0.5]
	monitoring._tests_info = [
		{"File": "Monitoring", "Test": "Premier", "Timestamp": 0.0},
		{"File": "Monitoring", "Test": "Second", "Timestamp": 1.0},
	]

	monitoring._draw()

	assert len(monitoring._figure.data) == 9
	assert len(monitoring._figure.layout.shapes) == 6
	assert [shape.xref for shape in monitoring._figure.layout.shapes] == ["x", "x", "x2", "x2", "x3", "x3"]
	assert [shape.yref for shape in monitoring._figure.layout.shapes] == ["y", "y", "y2", "y2", "y3", "y3"]


##################################################
def test_monitoring_removes_samples_before_first_test(monkeypatch):
	"""Vérifie la suppression des mesures collectées avant le premier test."""
	monitoring = Monitoring()
	monitoring._times = [10.0, 20.0, 30.0]
	monitoring._cpu = [10.0, 20.0, 30.0]
	monitoring._gpu = [1.0, 2.0, 3.0]
	monitoring._memory = [10 * 1024 * 1024, 20 * 1024 * 1024, 30 * 1024 * 1024]
	monitoring._disk = [0, 1024 * 1024, 3 * 1024 * 1024]
	monitoring._tests_info = [
		{"File": "Monitoring", "Test": "Premier", "Timestamp": 20.0},
		{"File": "Monitoring", "Test": "Second", "Timestamp": 25.0},
	]
	monkeypatch.setattr(psutil, "cpu_count", lambda logical: 10)

	monitoring._update_array_for_readability()

	assert monitoring._times == [0.0, 10.0]
	assert monitoring._cpu == [2.0, 3.0]
	assert monitoring._gpu == [2.0, 3.0]
	assert monitoring._memory == [20.0, 30.0]
	assert monitoring._disk == [0, 2.0]
	assert [test["Timestamp"] for test in monitoring._tests_info] == [0.0, 5.0]


##################################################
def test_monitoring_save():
	"""Vérifie l'enregistrement des graphiques."""
	monitoring = Monitoring()
	monitoring.start(0.1)
	simulate_cpu_usage(monitoring)
	if HAVE_GPU: simulate_gpu_usage(monitoring)
	simulate_memory_usage(monitoring)
	simulate_disk_io(monitoring)
	monitoring.add_test_info("Invalid test infos")
	monitoring.stop()
	for ext in ["png", "html", "json", "txt"]:
		monitoring.save(f"{OUTPUT_DIR}/test_monitoring.{ext}")
