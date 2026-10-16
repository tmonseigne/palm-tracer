"""
Surveille les ressources système utilisées pendant l'exécution des tests.

Le suivi couvre notamment le processeur, la mémoire, le disque et, lorsqu'il est disponible, le processeur graphique.
"""

from __future__ import annotations

import logging
import os
import platform
import re
import threading
import time
from collections.abc import Sequence
from contextlib import suppress
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, TypedDict

import numpy as np
import plotly.express as px  # Pour accéder aux couleurs qualitatives
import plotly.graph_objects as go
import psutil
from plotly.subplots import make_subplots

MEMORY_RATIO = 1.0 / (1024 * 1024)

try:
	import pynvml

	HAVE_GPU = os.getenv("GITHUB_ACTIONS") != "true"
except ImportError:
	pynvml = None
	logging.warning("pynvml is not available, GPU monitoring will be disabled.")
	HAVE_GPU = False


class MonitoringTestInfo(TypedDict):
	"""Informations d’un test associées aux mesures de ressources."""

	File: str
	"""Nom du fichier de test."""
	Test: str
	"""Nom du test."""
	Timestamp: float
	"""Instant du test, en secondes."""


class _MonitoringTrace(TypedDict):
	"""Paramètres d’une courbe de ressources transmise à Plotly."""

	y: list[float]
	"""Mesures de la ressource."""
	name: str
	"""Libellé de la courbe."""
	line: dict[str, str]
	"""Style du tracé."""


# --------------------------------------------------
@dataclass
class Monitoring:
	"""
	Surveille les ressources système utilisées pendant l'exécution des tests.

	Les mesures du processeur, de la mémoire, du disque et, si disponible, du processeur graphique sont collectées dans un thread dédié puis représentées
	sous forme de graphiques ou de rapports.

	:param interval: Durée de mesure CPU par processus et pause entre deux cycles, en secondes.
	"""

	interval: float = 1.0
	"""Durée de mesure CPU par processus et pause entre deux cycles, en secondes."""
	_cpu: list[float] = field(init=False, default_factory=list)
	"""Liste des valeurs d'utilisation du CPU."""
	_gpu: list[float] = field(init=False, default_factory=list)
	"""Liste des valeurs d'utilisation du GPU."""
	_memory: list[float] = field(init=False, default_factory=list)
	"""Liste des valeurs d'utilisation de la mémoire."""
	_disk: list[float] = field(init=False, default_factory=list)
	"""Liste des valeurs d'utilisation du disque."""
	_times: list[float] = field(init=False, default_factory=list)
	"""Liste des timestamps."""
	_monitoring: bool = field(init=False, default=False)
	"""Indique si la surveillance est en cours ou non."""
	_thread: threading.Thread = field(init=False, default_factory=threading.Thread)
	"""Le thread qui exécute le monitoring."""
	_stop_event: threading.Event = field(init=False, default_factory=threading.Event)
	"""Événement utilisé pour demander l'arrêt propre du thread de monitoring."""
	_data_lock: threading.Lock = field(init=False, default_factory=threading.Lock)
	"""Verrou protégeant les tableaux de mesures contre les accès concurrents."""
	_tests_info: list[MonitoringTestInfo] = field(init=False, default_factory=list)  # Liste des informations des tests
	"""Liste des informations relatives aux tests exécutés."""
	_figure: go.Figure = field(init=False, default_factory=go.Figure)
	"""Figure finale du monitoring."""
	_gpu_handle: Any = field(init=False, default=None)
	"""GPU à surveiller."""

	# ==================================================
	# region Accesseurs
	# ==================================================
	@property
	def n_entries(self) -> int:
		"""Nombre de mesures enregistrées."""
		return len(self._times)

	# --------------------------------------------------
	@property
	def is_running(self) -> bool:
		"""Indique si le thread de monitoring est actuellement actif."""
		return self._thread.is_alive() and not self._stop_event.is_set()

	# ==================================================
	# endregion Accesseurs
	# ==================================================

	# ==================================================
	# region Gestion du suivi
	# ==================================================
	def _start_thread(self):
		"""Démarre le thread de monitoring sans réinitialiser les données."""
		self._stop_event.clear()
		self._monitoring = True
		self._thread = threading.Thread(target=self.monitor, daemon=True)
		self._thread.start()

	# --------------------------------------------------
	def _reset(self):
		"""Réinitialise toutes les données de monitoring (CPU, mémoire, disque, etc.)."""
		self._cpu.clear()
		self._gpu.clear()
		if HAVE_GPU and pynvml is not None:
			pynvml.nvmlInit()
			self._gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(0)  # Suppose qu'un seul GPU est utilisé
		self._memory.clear()
		self._disk.clear()
		self._times.clear()
		self._tests_info.clear()
		self._monitoring = False
		self._thread = threading.Thread()
		self._stop_event = threading.Event()
		self._data_lock = threading.Lock()

	# --------------------------------------------------
	def _update(self):
		"""Met à jour les valeurs d'utilisation du CPU, de la mémoire et du disque en fonction des processus en cours."""
		# Sélection de processus
		try:
			pytest_pid = os.getpid()  # .					   PID de pytest
			pytest_proc = psutil.Process(pytest_pid)  # .	   Récupère le processus parent
			children = pytest_proc.children(recursive=True)  # Cible les processus enfants
			processes = [pytest_proc, *children]  # .		   Inclut le processus principal et ses enfants
		except (psutil.NoSuchProcess, psutil.AccessDenied): return

		cpu, mem, disk = 0.0, 0, 0

		for proc in processes:
			try:
				# Mesure bloquante pendant self.interval secondes pour chaque processus.
				cpu += proc.cpu_percent(interval=self.interval)
				mem += proc.memory_info().rss
				# "Darwin" est le nom de macOS dans platform.system()
				if platform.system() != "Darwin": disk += proc.io_counters().write_bytes
			except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess): continue

		gpu = 0
		if self._gpu_handle and pynvml is not None:
			try:
				util = pynvml.nvmlDeviceGetUtilizationRates(self._gpu_handle)
				gpu = util.gpu
			except pynvml.NVMLError: gpu = 0  # Erreur lors de la lecture de l'utilisation GPU.

		with self._data_lock:
			self._cpu.append(cpu)
			self._memory.append(mem)
			self._disk.append(disk)
			self._gpu.append(gpu)
			self._times.append(time.time())

	# --------------------------------------------------
	def start(self, interval: float = 1.0):
		"""
		Démarre la surveillance des ressources.

		:param interval: Durée de mesure CPU par processus et pause entre deux cycles, en secondes.
		"""
		self._reset()
		self.interval = interval
		self._start_thread()

	# --------------------------------------------------
	def monitor(self):
		"""Surveille les ressources en continu dans un thread séparé."""
		while self._monitoring:
			self._update()
			self._stop_event.wait(self.interval)

	# --------------------------------------------------
	def stop(self):
		"""Arrête la surveillance, prépare les mesures et construit la figure."""
		self._monitoring = False
		self._stop_event.set()
		# self._update()  # Dernière entrée

		if self._thread.is_alive(): self._thread.join(timeout=max(self.interval * 3.0, 1.0))
		if HAVE_GPU and pynvml is not None:
			with suppress(pynvml.NVMLError): pynvml.nvmlShutdown()

		# if not self._times: return
		self._update_array_for_readability()
		self._draw()

	# --------------------------------------------------
	def pause(self):
		"""Arrête temporairement le thread de monitoring sans générer de graphique."""
		self._monitoring = False
		self._stop_event.set()
		if self._thread.is_alive(): self._thread.join(timeout=max(self.interval * 3.0, 1.0))

	# --------------------------------------------------
	def resume(self):
		"""Reprend la surveillance sans réinitialiser les données."""
		if self.is_running: return
		self._start_thread()

	# --------------------------------------------------
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

	# --------------------------------------------------
	def _update_array_for_readability(self, round_time: int = 2):
		"""
		Met à jour les tableaux pour faciliter la lecture (ajustement des timestamps et normalisation).

		:param round_time: Le nombre de décimales pour arrondir les timestamps.
		"""
		first_time = self._tests_info[0]["Timestamp"] if self._tests_info else self._times[0]
		first_sample_index = next((i for i, timestamp in enumerate(self._times) if timestamp >= first_time), len(self._times) - 1)
		self._cpu = self._cpu[first_sample_index:]
		self._gpu = self._gpu[first_sample_index:]
		self._memory = self._memory[first_sample_index:]
		self._disk = self._disk[first_sample_index:]
		self._times = self._times[first_sample_index:]

		for test_info in self._tests_info: test_info["Timestamp"] = round(test_info["Timestamp"] - first_time, round_time)
		self._times = [round(t - first_time, round_time) for t in self._times]

		num_cores = psutil.cpu_count(logical=True)
		self._cpu = [c / num_cores for c in self._cpu]  # .														Division par le nombre de CPU
		self._memory = [m * MEMORY_RATIO for m in self._memory]  # .											Passage en Mo
		self._disk = [(self._disk[i] - self._disk[i - 1]) * MEMORY_RATIO for i in range(1, len(self._disk))]  # Passage en Mo et en delta d'utilisation
		self._disk.insert(0, 0)  # .																			Ajouter 0 au début pour restaurer la taille

	# ==================================================
	# endregion Gestion du suivi
	# ==================================================

	# ==================================================
	# region Dessin
	# ==================================================
	@staticmethod
	def get_color_map_by_name(names: list[str], palette: list[str] = px.colors.qualitative.Plotly) -> dict[str, str]:
		"""
		Associe chaque nom de fichier distinct à une couleur de la palette.

		Cette fonction prend une liste de noms de fichiers et associe une couleur de la palette spécifiée à chaque nom de fichier.
		Si le nombre de fichiers dépasse le nombre de couleurs disponibles dans la palette, elle réutilise les couleurs de manière cyclique.

		:param names: Liste des noms des fichiers pour lesquels une couleur doit être attribuée.
		:param palette: Liste des couleurs à utiliser pour les fichiers. La palette ``Plotly`` est utilisée par défaut.
		:return: Dictionnaire où les clés sont les noms de fichiers et les valeurs sont les couleurs attribuées.
		"""
		unique_names = set(names)  # Récupérer les noms uniques
		color_map: dict[str, str] = {}  # .			 Dictionnaire pour associer chaque fichier à une couleur
		# Associer une couleur unique à chaque fichier.
		for color_index, name in enumerate(unique_names):
			color_map[name] = palette[color_index % len(palette)]

		return color_map

	# --------------------------------------------------
	@staticmethod
	def get_y_range(data: Sequence[float] | np.ndarray, padding_ratio: float = 0.0) -> list[float]:
		"""
		Calcule les bornes de l’axe Y avec une marge proportionnelle.

		:param data: Série non vide des valeurs à représenter.
		:param padding_ratio: Marge de chaque côté, exprimée comme fraction de l’étendue des données.
		:return: Bornes ``[minimum - marge, maximum + marge]``.
		"""
		min_val, max_val = min(data), max(data)
		padding = (max_val - min_val) * padding_ratio  # Calcul de la marge en haut et en bas
		return [min_val - padding, max_val + padding]

	# --------------------------------------------------
	@staticmethod
	def _build_test_section(y_range: list[float], tests: list[MonitoringTestInfo], color_map: dict[str, str],
							last_time: float, row: int) -> tuple[list[go.Scatter], list[dict[str, Any]]]:
		"""
		Construit les barres verticales et les zones colorées d'une section de tests.

		Les objets Plotly sont retournés sans être ajoutés individuellement à la figure afin de permettre
		leur insertion groupée et d'éviter les validations coûteuses à chaque itération.

		:param y_range: Bornes ``[minimum, maximum]`` de l’axe Y.

		:param tests: Une liste de dictionnaires représentant les tests effectués. Chaque dictionnaire doit contenir les clés :
				- "Timestamp" (float) : Le timestamp du test.
				- "File" (str) : Le nom du fichier associé au test.
				- "Test" (str) : Le nom du test effectué.

		:param color_map: Couleurs Plotly associées aux noms des fichiers de tests.

		:param last_time: Instant de fin de la dernière zone colorée, en secondes dans le même repère que les tests.

		:param row: Numéro du sous-graphique Plotly, à partir de 1, dans la première colonne.

		:return: Traces verticales et zones colorées à ajouter à la figure.
		"""
		traces: list[go.Scatter] = []
		shapes: list[dict[str, Any]] = []
		axis_suffix = "" if row == 1 else str(row)

		# Ajouter les barres verticales pour chaque test et des zones colorées en fonction du fichier
		for i, test in enumerate(tests):
			# Récupérer les informations du test et la couleur associée au fichier
			t, f, n = test["Timestamp"], test["File"], test["Test"]
			text = f"{f} - {n}"
			color = color_map[f]

			# Déterminer la plage pour la zone colorée
			# Si ce n'est pas le dernier test, la fin de la zone est le timestamp du test suivant sinon le dernier timestamp
			next_timestamp = tests[i + 1]["Timestamp"] if i < len(tests) - 1 else last_time

			shapes.append({"type": "rect", "x0": t, "x1": next_timestamp, "y0": y_range[0], "y1": y_range[1], "fillcolor": color, "opacity": 0.2,
						   "line": {"width": 0}, "xref": f"x{axis_suffix}", "yref": f"y{axis_suffix}"})
			traces.append(go.Scatter(x=[t, t], y=y_range, mode="lines", line={"color": color, "width": 0.5, "dash": "dash"},
									 name=text, hoverinfo="text", text=text))

		return traces, shapes

	# --------------------------------------------------
	@staticmethod
	def draw_test_section(fig: go.Figure, y_range: list[float], tests: list[MonitoringTestInfo],
						  color_map: dict[str, str], last_time: float, row: int):
		"""
		Ajoute des barres verticales et des zones colorées pour chaque test dans un graphique Plotly.

		:param fig: Figure Plotly à compléter.
		:param y_range: Bornes ``[minimum, maximum]`` de l’axe Y.
		:param tests: Informations relatives aux tests exécutés.
		:param color_map: Couleurs Plotly associées aux noms des fichiers de tests.
		:param last_time: Instant de fin de la dernière zone colorée, en secondes dans le même repère que les tests.
		:param row: Numéro du sous-graphique Plotly, à partir de 1, dans la première colonne.
		"""
		traces, shapes = Monitoring._build_test_section(y_range, tests, color_map, last_time, row)
		fig.add_traces(traces, rows=[row] * len(traces), cols=[1] * len(traces))
		fig.update_layout(shapes=[*fig.layout.shapes, *shapes])

	# --------------------------------------------------
	def _draw(self):
		"""Construit la figure interactive des ressources utilisées pendant les tests."""

		params: list[_MonitoringTrace] = [{"y": self._cpu, "name": "CPU Usage (%)", "line": {"color": "blue"}},
										  {"y": self._memory, "name": "Memory Usage (Mo)", "line": {"color": "green"}},
										  {"y": self._disk, "name": "Disk Usage (IO Mo)", "line": {"color": "red"}}]

		# Ajouter GPU seulement si pertinent
		if not np.allclose(self._gpu, 0): params.insert(1, {"y": self._gpu, "name": "GPU Usage (%)", "line": {"color": "darkblue"}})

		self._figure = make_subplots(rows=len(params), cols=1, shared_xaxes=True, vertical_spacing=0.05, subplot_titles=tuple(p["name"] for p in params))
		color_map = self.get_color_map_by_name([test["File"] for test in self._tests_info], px.colors.qualitative.Plotly)
		traces: list[go.Scatter] = []
		trace_rows: list[int] = []
		shapes: list[dict[str, Any]] = []

		for i in range(len(params)):
			row = i + 1
			traces.append(go.Scatter(x=self._times, y=params[i]["y"], mode="lines", name=params[i]["name"], line=params[i]["line"]))
			trace_rows.append(row)
			test_traces, test_shapes = self._build_test_section(self.get_y_range(params[i]["y"]), self._tests_info, color_map, self._times[-1], row)
			traces.extend(test_traces)
			trace_rows.extend([row] * len(test_traces))
			shapes.extend(test_shapes)

		self._figure.add_traces(traces, rows=trace_rows, cols=[1] * len(traces))
		self._figure.update_layout(shapes=shapes)

		# add_color_map_legend
		self._figure.update_layout(width=1200, height=len(params) * 200, margin={"t": 50, "l": 5, "r": 5, "b": 5},
								   title_text="Resource Usage Over Time", showlegend=False)
		for i in range(len(params)):
			self._figure.update_yaxes(showgrid=False, row=i + 1, col=1)  # .		Supprimer la grille verticale
			self._figure.update_xaxes(showgrid=False, row=i + 1, col=1)  # .		Supprimer la grille horizontale
		self._figure.update_xaxes(title_text="Time (s)", row=len(params), col=1)  # Place le titre X uniquement sur le graphique du bas

	# ==================================================
	# endregion Dessin
	# ==================================================

	# ==================================================
	# region Entrées / sorties
	# ==================================================
	def save(self, filename: str | Path, full_html: bool = False):
		"""
		Enregistre la figure ou les mesures selon l’extension du fichier.

		Les extensions ``.html`` et ``.json`` enregistrent la figure Plotly.
		Les autres extensions enregistrent les mesures et les informations de test en texte brut.
		Une erreur d’écriture est signalée dans la console sans être propagée.

		:param filename: Chemin du fichier de sortie ; son extension détermine le format.
		:param full_html: ``True`` pour un document HTML complet, ``False`` pour un fragment HTML.
		"""
		try:
			path = Path(filename)
			extension = path.suffix
			if extension == ".html":
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
		# Une erreur de rapport ne doit pas interrompre la session de tests.
		except Exception as e:  # noqa: BLE001
			logging.error("Error while saving data: %s", e)

	# --------------------------------------------------
	def tostring(self) -> str:
		"""
		Retourne une représentation textuelle des données de monitoring.

		:return: Chaîne décrivant les données de monitoring.
		"""
		return (f"{self.n_entries} entrées.\nTimestamps : {self._times}\n"
				f"CPU Usage : {self._cpu}\nGPU Usage : {self._gpu}\n"
				f"Memory Usage : {self._memory}\nDisk Usage : {self._disk}")

	# --------------------------------------------------
	def __str__(self) -> str:
		"""
		Retourne une représentation textuelle de l'objet.

		:return: Représentation textuelle de l'objet.
		"""
		return self.tostring()
