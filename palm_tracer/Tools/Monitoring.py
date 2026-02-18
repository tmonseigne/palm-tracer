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
from pathlib import Path
from typing import Any, List

import plotly.express as px  # Pour accéder aux couleurs qualitatives
import plotly.graph_objects as go
import psutil
from plotly.subplots import make_subplots

from palm_tracer.Tools import Ui

MEMORY_RATIO = 1.0 / (1024 * 1024)

try:
	from pynvml import nvmlDeviceGetHandleByIndex, nvmlDeviceGetUtilizationRates, nvmlInit, nvmlShutdown, nvmlDeviceGetCount

	HAVE_GPU = not os.getenv("GITHUB_ACTIONS") == "true"
except ImportError:
	Ui.print_warning("pynvml is not available, GPU monitoring will be disabled.")
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
			- **cpu (:class:`List[float]`)** : Liste des valeurs d'utilisation du CPU.
			- **memory (:class:`List[float]`)** : Liste des valeurs d'utilisation de la mémoire.
			- **disk (:class:`List[float]`)** : Liste des valeurs d'utilisation du disque.
			- **times (:class:`List[float]`)** : Liste des timestamps correspondant aux valeurs des ressources.
			- **monitoring (:class:`bool`)** : Indique si la surveillance est en cours ou non.
			- **thread (:class:`threading.Thread`)** : Le thread qui exécute le monitoring.
			- **tests_info (:class:`List[dict]`)** : Liste des informations relatives aux tests exécutés.
			- **interval (:class:`float`)** : Intervalle de temps entre chaque mise à jour des données en secondes.

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
		"""Nombre d'entrées (mesures) dans le monitoring (:class:`int`)."""
		return len(self._times)

	##################################################
	def _reset(self):
		"""Réinitialise toutes les données de monitoring (CPU, mémoire, disque, etc.)."""
		self._cpu.clear()
		self._gpu.clear()
		if HAVE_GPU:
			nvmlInit()
			self._gpu_handle = nvmlDeviceGetHandleByIndex(0)  # Suppose qu'un seul GPU est utilisé
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
		try:
			pytest_pid = os.getpid()  # .					   PID de pytest
			pytest_proc = psutil.Process(pytest_pid)  # .	   Récupère le processus parent
			children = pytest_proc.children(recursive=True)  # Cible les processus enfants
			processes = [pytest_proc] + children  # .		   Inclut le processus principal et ses enfants
		except (psutil.NoSuchProcess, psutil.AccessDenied): return

		cpu, mem, disk = 0.0, 0, 0

		for proc in processes:
			try:
				# Non bloquant : psutil calcule le delta depuis l’appel précédent.
				cpu += proc.cpu_percent(interval=self.interval)
				mem += proc.memory_info().rss
				# "Darwin" est le nom de macOS dans platform.system()
				if platform.system() != "Darwin": disk += proc.io_counters().write_bytes
			except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess): continue

		self._cpu.append(cpu)
		self._memory.append(mem)
		self._disk.append(disk)

		if self._gpu_handle:
			try:
				util = nvmlDeviceGetUtilizationRates(self._gpu_handle)
				self._gpu.append(util.gpu)
			except Exception: self._gpu.append(0)  # Erreur lors de la lecture de l'utilisation GPU
		else: self._gpu.append(0)  # .				 Aucun GPU détecté

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
		self._thread = threading.Thread(target=self.monitor, daemon=True)
		self._thread.start()

	##################################################
	def monitor(self):
		"""Surveille les ressources en continu dans un thread séparé."""
		while self._monitoring:
			self._update()
			time.sleep(self.interval)

	##################################################
	def stop(self):
		"""Arrête la surveillance et effectue une dernière mise à jour des valeurs."""
		self._monitoring = False
		self._update()  # Dernière entrée
		if self._thread.is_alive(): self._thread.join(timeout=self.interval * 2.0)
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
		self._cpu = [c / num_cores for c in self._cpu]  # .														Division par le nombre de CPU
		self._memory = [m * MEMORY_RATIO for m in self._memory]  # .											Passage en Mo
		self._disk = [(self._disk[i] - self._disk[i - 1]) * MEMORY_RATIO for i in range(1, len(self._disk))]  # Passage en Mo et en delta d'utilisation
		self._disk.insert(0, 0)  # .																			Ajouter 0 au début pour restaurer la taille

	# ==================================================
	# endregion Monitoring Manipulation
	# ==================================================

	# ==================================================
	# region Drawing
	# ==================================================
	##################################################
	@staticmethod
	def get_color_map_by_name(names: list[str], palette: list[str] = px.colors.qualitative.Plotly) -> dict[str, str]:
		"""
		Génère un dictionnaire associant chaque nom de fichier à une couleur unique.

		Cette fonction prend une liste de noms de fichiers et associe une couleur de la palette spécifiée à chaque nom de fichier.
		Si le nombre de fichiers dépasse le nombre de couleurs disponibles dans la palette, elle réutilise les couleurs de manière cyclique.

		:param names: Liste des noms des fichiers pour lesquels une couleur doit être attribuée.
		:param palette: Liste des couleurs à utiliser pour les fichiers. Si non spécifié, la palette `Plotly` est utilisée par défaut.
		:return: Dictionnaire où les clés sont les noms de fichiers et les valeurs sont les couleurs attribuées.
		"""
		unique_names = set(names)  # Récupérer les noms uniques
		color_map = {}  # .			 Dictionnaire pour associer chaque fichier à une couleur
		color_index = 0  # .		 Associer une couleur unique à chaque fichier
		for name in unique_names:
			color_map[name] = palette[color_index % len(palette)]
			color_index += 1  # .	 Passer à la couleur suivante

		return color_map

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
	@staticmethod
	def draw_test_section(fig: go.Figure, y_range: list, tests: list[dict], color_map: dict, last_time: float, row: int):
		"""
		Ajoute des barres verticales et des zones colorées pour chaque test dans un graphique Plotly.

		Cette fonction ajoute des zones colorées en fonction des timestamps des tests et leur fichier associé,
		ainsi que des lignes verticales pour marquer chaque test. Elle est utilisée pour représenter graphiquement
		les périodes d'exécution de chaque test dans le temps.

		:param fig: L'objet figure de Plotly dans lequel les éléments (barres et lignes) seront ajoutés.

		:param y_range: La plage des valeurs sur l'axe Y pour la section du graphique où les zones colorées seront tracées.
				La plage est définie par deux valeurs [y_min, y_max].

		:param tests: Une liste de dictionnaires représentant les tests effectués. Chaque dictionnaire doit contenir les clés :
				- "Timestamp" (float) : Le timestamp du test.
				- "File" (str) : Le nom du fichier associé au test.
				- "Test" (str) : Le nom du test effectué.

		:param color_map: Un dictionnaire associant chaque fichier de test à une couleur. Le fichier est utilisé comme clé et la couleur
				(en format HTML) comme valeur.

		:param last_time: Le dernier timestamp enregistré, utilisé pour déterminer la fin de la zone colorée pour le dernier test.

		:param row: L'index de la ligne dans la figure Plotly (utile lorsque plusieurs sous-graphiques sont utilisés) pour ajouter
				les éléments (barres verticales et zones colorées) dans la section correspondante.

		:return: Cette fonction modifie l'objet `fig` en ajoutant des traces et des formes, mais ne retourne rien.
		"""

		# Ajouter les barres verticales pour chaque test et des zones colorées en fonction du fichier
		for i, test in enumerate(tests):
			# Récupérer les informations du test et la couleur associée au fichier
			t, f, n = test["Timestamp"], test["File"], test["Test"]
			text = f"{f} - {n}"
			color = color_map[f]

			# Déterminer la plage pour la zone colorée
			# Si ce n'est pas le dernier test, la fin de la zone est le timestamp du test suivant sinon le dernier timestamp
			if i < len(tests) - 1: next_timestamp = tests[i + 1]["Timestamp"]
			else: next_timestamp = last_time

			# Ajouter une zone colorée
			fig.add_shape(type="rect", x0=t, x1=next_timestamp, y0=y_range[0], y1=y_range[1],
						  fillcolor=color, opacity=0.2, line=dict(width=0), row=row, col=1)
			# Ajouter une ligne verticale pointillée
			fig.add_trace(go.Scatter(x=[t, t], y=y_range, mode="lines", line=dict(color=color, width=0.5, dash="dash"),
									 name=text, hoverinfo="text", text=text), row=row, col=1)

	##################################################
	def _draw(self):
		"""Génère un graphique interactif des ressources utilisées pendant les tests et l'enregistre."""
		self._figure = make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.05,
									 subplot_titles=("CPU Usage (%)", "GPU Usage (%)", "Memory Usage (Mo)", "Disk Usage (IO Mo)"))
		color_map = self.get_color_map_by_name([test["File"] for test in self._tests_info], px.colors.qualitative.Plotly)

		params = [{"y": self._cpu, "name": "CPU Usage (%)", "line": dict(color="blue")},
				  {"y": self._gpu, "name": "GPU Usage (%)", "line": dict(color="darkblue")},
				  {"y": self._memory, "name": "Memory Usage (Mo)", "line": dict(color="green")},
				  {"y": self._disk, "name": "Disk Usage (IO Mo)", "line": dict(color="red")}]

		for i in range(len(params)):
			self._figure.add_trace(go.Scatter(x=self._times, y=params[i]["y"], mode="lines",
											  name=params[i]["name"], line=params[i]["line"]), row=i + 1, col=1)
			self.draw_test_section(self._figure, self.get_y_range(params[i]["y"]), self._tests_info, color_map, self._times[-1], i + 1)

		# add_color_map_legend
		self._figure.update_layout(width=1200, height=800,
								   margin={"t": 50, "l": 5, "r": 5, "b": 5},
								   title_text="Resource Usage Over Time", showlegend=False)
		for i in range(len(params)):
			self._figure.update_yaxes(showgrid=False, row=i + 1, col=1)  # .		Supprimer la grille verticale
			self._figure.update_xaxes(showgrid=False, row=i + 1, col=1)  # .		Supprimer la grille horizontale
		self._figure.update_xaxes(title_text="Time (s)", row=len(params), col=1)  # Place le titre X uniquement sur le graphique du bas

	# ==================================================
	# endregion Drawing
	# ==================================================

	# ==================================================
	# endregion IO
	# ==================================================
	##################################################
	def save(self, filename: str | Path, full_html: bool = False):
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
			path = Path(filename)
			extension = path.suffix
			if extension in [".png", ".jpg", ".jpeg", ".bmp", ".svg"]:
				Ui.print_warning("Kaleido doesn't work so well need update. No Image Saved.")
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
			Ui.print_error(f"Error while saving data: {e}")

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
