""" Fichier des tests pour le monitoring. """

import os
import time
from pathlib import Path

try:
	import torch

	HAVE_GPU = not os.getenv("GITHUB_ACTIONS") == "true"
except ImportError:
	HAVE_GPU = False

from palm_tracer.Tools import Monitoring

OUTPUT_DIR = Path(__file__).parent / "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)
default_duration = 2


# ==================================================
# region Simulations
# ==================================================
##################################################
def simulate_cpu_usage(monitoring: Monitoring, intensity: int = 1000000, duration: float = default_duration):
	"""
	Simule une utilisation importante de CPU en effectuant des calculs intensifs.

	:param monitoring: Moniteur à manipuler
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

	:param monitoring: Moniteur à manipuler
	:param tensor_size: Taille des matrices carrées utilisées pour les calculs.
	:param duration: Durée en secondes pendant laquelle les opérations GPU sont répétées.
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
		_ = c.sum().item()		# Force le calcul immédiat (évite lazy eval de PyTorch)

	torch.cuda.empty_cache()
	print("GPU simulation complete.")


##################################################
def simulate_memory_usage(monitoring: Monitoring, size: int = 50, duration: float = default_duration):
	"""
	Simule une utilisation importante de mémoire en allouant un tableau de bytes.

	:param monitoring: Moniteur à manipuler
	:param size: Taille totale de mémoire à allouer (en mégaoctets).
	:param duration: Temps pendant lequel la mémoire reste allouée (en secondes).
	"""
	monitoring.add_test_info("_tests/test_simulation_memory.py::test_allocate_memory")
	print(f"Allocating {size} MB of memory...")
	allocated_memory = bytearray(size * 1024 * 1024)  # Alloue un tableau de bytes
	monitoring.add_test_info("_tests/test_simulation_memory.py::test_hold_memory")
	print(f"Memory allocated. Holding for {duration} seconds...")
	time.sleep(duration)							  # Garde la mémoire allouée pour observer l'impact
	monitoring.add_test_info("_tests/test_simulation_memory.py::test_release_memory")
	print("Releasing memory.")
	del allocated_memory							  # Libère la mémoire


##################################################
def simulate_disk_io(monitoring: Monitoring, file_size: int = 1, duration: float = default_duration, file_name: str = "temp_test_file.bin"):
	"""
	Simule des opérations intensives de disque en écrivant et lisant un fichier volumineux.

	:param monitoring: Moniteur à manipuler
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
	"""Test basique sur la classe."""
	monitoring = Monitoring()
	monitoring.start(0.1)
	time.sleep(1)
	monitoring.stop()
	print(f"\n{monitoring}")
	assert True


##################################################
def test_monitoring_save():
	"""Test d'enregistrement des graphiques."""
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
	assert True
