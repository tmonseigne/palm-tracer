"""
Module de surveillance des ressources système pendant l'exécution de tests.

Ce fichier contient une classe principale :class:`Monitoring` permettant de suivre en temps réel l'utilisation des
ressources système (CPU, mémoire, disque) durant l'exécution de tests. Il offre des fonctionnalités de surveillance,
de mise à jour des données et de visualisation graphique des résultats.

**Contenu** :

1. **Classe principale**

   - :class:`Monitoring` : Classe pour surveiller et analyser les ressources utilisées.

2. **Fonctionnalités**

   - Surveillance des ressources système (CPU, mémoire, disque) via `psutil`.
   - Génération de graphiques interactifs avec `plotly`.
   - Sauvegarde des résultats au format texte, HTML ou JSON.
   - Gestion des intervalles de mise à jour via des threads.

"""

import os
import platform
import re
import threading
import time
from dataclasses import dataclass, field
from typing import Any, List

import plotly.express as px  # Pour accéder aux couleurs qualitatives
import plotly.graph_objects as go
import psutil
from plotly.subplots import make_subplots

from palm_tracer.Tools.Drawing import draw_test_section, get_color_map_by_name
from palm_tracer.Tools.Utils import print_error, print_warning

MEMORY_RATIO = 1.0 / (1024 * 1024)

try:
	from pynvml import nvmlDeviceGetHandleByIndex, nvmlDeviceGetUtilizationRates, nvmlInit, nvmlShutdown, nvmlDeviceGetCount

	HAVE_GPU = not os.getenv("GITHUB_ACTIONS") == "true"
except ImportError:
	print_warning("pynvml non disponible, le monitoring GPU sera désactivé.")
	HAVE_GPU = False


##################################################
@dataclass
class Monitoring:
	"""
	Classe de monitoring qui suit l'utilisation des ressources (CPU, mémoire, disque) pendant l'exécution des tests.

	Cette classe collecte les informations sur l'utilisation des ressources du système durant l'exécution des tests.
	Elle fournit des fonctionnalités pour démarrer et arrêter la surveillance, mettre à jour les valeurs des ressources,
	et générer des graphiques ou des fichiers texte avec ces données.

	Attributs :
			- **cpu (List[float])** : Liste des valeurs d'utilisation du CPU.
			- **memory (List[float])** : Liste des valeurs d'utilisation de la mémoire.
			- **disk (List[float])** : Liste des valeurs d'utilisation du disque.
			- **times (List[float])** : Liste des timestamps correspondant aux valeurs des ressources.
			- **monitoring (bool)** : Indique si la surveillance est en cours ou non.
			- **thread (threading.Thread)** : Le thread qui exécute le monitoring.
			- **tests_info (List[dict])** : Liste des informations relatives aux tests exécutés.
			- **interval (float)** : Intervalle de temps entre chaque mise à jour des données en secondes.

	"""

	interval: float = 1.0
	"""Intervalle de temps entre chaque mise à jour des données en secondes."""
	_cpu: List[float] = field(init=False, default_factory=list)
	"""Liste des valeurs d'utilisation du CPU."""
	_gpu: List[float] = field(init=False, default_factory=list)
	"""Liste des valeurs d'utilisation du GPU."""
	_memory: List[float] = field(init=False, default_factory=list)
	"""Liste des valeurs d'utilisation de la mémoire."""
	_disk: List[float] = field(init=False, default_factory=list)
	"""Liste des valeurs d'utilisation du disque."""
	_times: List[float] = field(init=False, default_factory=list)
	"""Liste des timestamps."""
	_monitoring: bool = field(init=False, default=False)
	"""Indique si la surveillance est en cours ou non."""
	_thread: threading.Thread = field(init=False, default_factory=threading.Thread)
	"""Le thread qui exécute le monitoring."""
	_tests_info: List[dict] = field(init=False, default_factory=list)  # Liste des informations des tests
	"""Liste des informations relatives aux tests exécutés."""
	_figure: go.Figure = field(init=False, default_factory=go.Figure)
	"""Figure finale du monitoring."""
	_gpu_handle: Any = field(init=False, default=None)
	"""GPU à surveiller."""

	# ==================================================
	# region Monitoring Manipulation
	# ==================================================
	##################################################
	@property
	def n_entries(self) -> int:
		"""
		Retourne le nombre d'entrées (mesures) dans le monitoring.

		:return: Nombre d'entrées dans les listes de données.
		"""
		return len(self._times)

	##################################################
	def _reset(self):
		"""Réinitialise toutes les données de monitoring (CPU, mémoire, disque, etc.)."""
		self._cpu.clear()
		self._gpu.clear()
		if HAVE_GPU:
			nvmlInit()
			self._gpu_handle = nvmlDeviceGetHandleByIndex(0)  # Suppose qu’un seul GPU est utilisé
		self._memory.clear()
		self._disk.clear()
		self._times.clear()
		self._tests_info.clear()
		self._monitoring = False
		self._thread = threading.Thread()

	##################################################
	def _update(self):
		"""Met à jour les valeurs d'utilisation du CPU, de la mémoire et du disque en fonction des processus en cours."""
		# Sélection de processus
		if not self._thread.is_alive(): return			 # pragma: no cover	(n'arrive qu'en cas de crash)
		pytest_pid = os.getpid()						 # PID de pytest
		pytest_proc = psutil.Process(pytest_pid)		 # Récupère le processus parent
		children = pytest_proc.children(recursive=True)  # Cible les processus enfants
		processes = [pytest_proc] + children			 # Inclut le processus principal et ses enfants

		self._cpu.append(sum(proc.cpu_percent(interval=self.interval) for proc in processes))
		self._memory.append(sum(proc.memory_info().rss for proc in processes))
		# "Darwin" est le nom de macOS dans platform.system()
		if platform.system() != "Darwin": self._disk.append(sum(proc.io_counters().write_bytes for proc in processes))
		else: self._disk.append(0)						 # pragma: no cover

		if self._gpu_handle:
			try:
				util = nvmlDeviceGetUtilizationRates(self._gpu_handle)
				self._gpu.append(util.gpu)
			except Exception: self._gpu.append(0)		 # Erreur lors de la lecture de l'utilisation GPU
		else: self._gpu.append(0)						 # Aucun GPU détecté

		self._times.append(time.time())

	##################################################
	def start(self, interval: float = 1.0):
		"""
		Démarre la surveillance des ressources.

		:param interval: Intervalle de mise à jour des données (en secondes).
		"""
		self._reset()
		self.interval = interval
		self._monitoring = True
		self._thread = threading.Thread(target=self.monitor)
		self._thread.start()

	##################################################
	def monitor(self):
		"""Surveille les ressources en continu dans un thread séparé."""
		while self._monitoring and self._thread.is_alive():
			self._update()
			time.sleep(self.interval)

	##################################################
	def stop(self):
		"""Arrête la surveillance et effectue une dernière mise à jour des valeurs."""
		self._monitoring = False
		self._update()  # Dernière entrée
		if self._thread.is_alive(): self._thread.join()
		self._update_array_for_readability()
		if HAVE_GPU: nvmlShutdown()
		self._draw()

	##################################################
	def add_test_info(self, name: str):
		"""
		Ajoute des informations sur un test dans la liste des tests.

		:param name: Le nom complet du test, au format "<path>test_<file>.py::test_<test_name>".
		"""
		match = re.match(r".*test_(.*)\.py::test_(.*)", name)
		if match:
			file = match.group(1).replace("_", " ").title()  # Récupère le nom du fichier et change la casse
			test = match.group(2).replace("_", " ").title()  # Récupère le nom du test et change la casse
			self._tests_info.append({"File": file, "Test": test, "Timestamp": time.time()})

	##################################################
	def _update_array_for_readability(self, round_time: int = 2):
		"""
		Met à jour les tableaux pour faciliter la lecture (ajustement des timestamps et normalisation).

		:param round_time: Le nombre de décimales pour arrondir les timestamps.
		"""
		first_time = self._times[0]

		for test_info in self._tests_info: test_info["Timestamp"] = round(test_info["Timestamp"] - first_time, round_time)
		self._times = [round(t - first_time, round_time) for t in self._times]

		num_cores = psutil.cpu_count(logical=True)
		self._cpu = [c / num_cores for c in self._cpu]														  # Division par le nombre de CPU
		self._memory = [m * MEMORY_RATIO for m in self._memory]												  # Passage en Mo
		self._disk = [(self._disk[i] - self._disk[i - 1]) * MEMORY_RATIO for i in range(1, len(self._disk))]  # Passage en Mo et en delta d'utilisation
		self._disk.insert(0, 0)																				  # Ajouter 0 au début pour restaurer la taille

	# ==================================================
	# endregion Monitoring Manipulation
	# ==================================================

	# ==================================================
	# region Drawing
	# ==================================================
	##################################################
	@staticmethod
	def get_y_range(data, padding_ratio: float = 0.0):
		"""
		Calcule la plage de valeurs de l'axe Y avec un espacement supplémentaire autour des valeurs.

		:param data: Liste des données pour lesquelles la plage doit être calculée.
		:param padding_ratio: Rapport d'espacement ajouté à la plage des données.
		:return: La plage calculée [min, max] avec l'espacement ajouté.
		"""
		min_val, max_val = min(data), max(data)
		padding = (max_val - min_val) * padding_ratio  # Calcul de la marge en haut et en bas
		return [min_val - padding, max_val + padding]

	##################################################
	def _draw(self):
		"""Génère un graphique interactif des ressources utilisées pendant les tests et l'enregistre."""
		self._figure = make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.05,
									 subplot_titles=("CPU Usage (%)", "GPU Usage (%)", "Memory Usage (Mo)", "Disk Usage (IO Mo)"))
		color_map = get_color_map_by_name([test["File"] for test in self._tests_info], px.colors.qualitative.Plotly)

		params = [{"y": self._cpu, "name": "CPU Usage (%)", "line": dict(color="blue")},
				  {"y": self._gpu, "name": "GPU Usage (%)", "line": dict(color="darkblue")},
				  {"y": self._memory, "name": "Memory Usage (Mo)", "line": dict(color="green")},
				  {"y": self._disk, "name": "Disk Usage (IO Mo)", "line": dict(color="red")}]

		for i in range(len(params)):
			self._figure.add_trace(go.Scatter(x=self._times, y=params[i]["y"], mode="lines",
											  name=params[i]["name"], line=params[i]["line"]), row=i + 1, col=1)
			draw_test_section(self._figure, self.get_y_range(params[i]["y"]), self._tests_info, color_map, self._times[-1], i + 1)

		# add_color_map_legend
		self._figure.update_layout(width=1200, height=800,
								   margin={"t": 50, "l": 5, "r": 5, "b": 5},
								   title_text="Resource Usage Over Time", showlegend=False)
		for i in range(len(params)):
			self._figure.update_yaxes(showgrid=False, row=i + 1, col=1)			  # Supprimer la grille verticale
			self._figure.update_xaxes(showgrid=False, row=i + 1, col=1)			  # Supprimer la grille horizontale
		self._figure.update_xaxes(title_text="Time (s)", row=len(params), col=1)  # Place le titre X uniquement sur le graphique du bas

	# ==================================================
	# endregion Drawing
	# ==================================================

	# ==================================================
	# endregion IO
	# ==================================================
	##################################################
	def save(self, filename: str, full_html: bool = False):
		"""
		Sauvegarde les données de monitoring dans un fichier spécifié en fonction de l'extension du fichier.

		Cette méthode permet de sauvegarder les informations de monitoring dans différents formats en fonction de l'extension du fichier fourni :

				- `.png` : Sauvegarde une image de la figure générée par la méthode `draw`.
				- `.html` : Sauvegarde la figure au format HTML.
				- `.json` : Sauvegarde les données au format JSON.
				- Pour d'autres formats, les informations de monitoring seront enregistrées sous forme de texte brut.

		Le format texte contient les informations suivantes :

				- Timestamps : Liste des timestamps collectés pendant le monitoring.
				- CPU Usage : Utilisation du CPU.
				- Memory Usage : Utilisation de la mémoire.
				- Disk Usage : Utilisation du disque.
				- Liste des tests : Détails des tests effectués, incluant le fichier, le test et le timestamp.

		:param filename: Le chemin et nom du fichier dans lequel les données de monitoring seront enregistrées.
						 Le format de sauvegarde sera déterminé en fonction de l'extension du fichier (ex. `.png`, `.html`, `.json`).
		:param full_html: Option pour l'enregistrement html permettant de ne sauver que le div
		"""
		try:
			_, extension = os.path.splitext(filename)
			if extension in [".png", ".jpg", ".jpeg", ".bmp", ".svg"]:
				print_warning("Kaleido doesn't work so well need update. No Image Saved.")
			# self._figure.write_image(filename, width=1280, height=720, scale=1, engine="kaleido")
			elif extension == ".html":
				self._figure.write_html(filename, full_html=full_html)
			elif extension == ".json":
				self._figure.write_json(filename)
			else:
				with open(filename, "w", encoding="utf-8") as f:
					f.write(f"Timestamps : {self._times}\n")
					f.write(f"CPU Usage : {self._cpu}\n")
					f.write(f"GPU Usage : {self._gpu}\n")
					f.write(f"Memory Usage : {self._memory}\n")
					f.write(f"Disk Usage : {self._disk}\n")
					f.write("Liste des tests : \n")
					for test in self._tests_info: f.write(f"{test['File']}, {test['Test']}, {test['Timestamp']}\n")
		except Exception as e:
			print_error(f"Erreur lors de la sauvegarde des données : {e}")

	##################################################
	def tostring(self) -> str:
		"""
		Retourne une représentation textuelle des données de monitoring.

		:return: Chaîne décrivant les données de monitoring.
		"""
		return (f"{self.n_entries} entrées.\nTimestamps : {self._times}\n"
				f"CPU Usage : {self._cpu}\nGPU Usage : {self._gpu}\n"
				f"Memory Usage : {self._memory}\nDisk Usage : {self._disk}")

	##################################################
	def __str__(self) -> str: return self.tostring()

# ==================================================
# endregion IO
# ==================================================
