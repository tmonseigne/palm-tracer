"""
Orchestre le chargement, le traitement, le filtrage et l'enregistrement des données PALM.

.. todo:: Documenter précisément la stratégie de filtrage appliquée aux calculs, aux visualisations et aux sauvegardes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal, Optional, cast

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from palm_tracer.Processing import Drift, Filtering, Gallery, Grapher, Palm, Parsing, Renderer
from palm_tracer.Processing.Step import Step, StepAction, prepare_step_action
from palm_tracer.Results import Results
from palm_tracer.Settings import Settings
from palm_tracer.Settings.Types import CheckRangeInt, ColorMap, Combo, FileList
from palm_tracer.Tools import FileIO, Logger, Ui

MAX_UI_16 = np.iinfo(np.uint16).max


##################################################
@dataclass
class PALMTracer:
	"""
	Orchestre un traitement PALM complet et conserve ses données intermédiaires et finales.

	La classe coordonne la configuration, les appels à la DLL PALM, le pipeline de traitement, le filtrage, la production des visualisations et la
	sauvegarde des résultats.
	"""

	settings: Settings = field(init=False, default_factory=Settings)
	"""Classe principale des paramètres PALMTracer."""
	palm: Palm = field(init=False, default_factory=Palm)
	"""Interface vers la DLL C++ Palm."""
	_logger: Logger = field(init=False, default_factory=Logger)
	"""Journal d'activité."""
	filtering: Filtering = field(init=False)
	"""Outil de filtrage."""
	results: Results = field(init=False, default_factory=Results)
	"""Résultats des différents calculs."""

	_path: str = field(init=False, default="")
	"""Dossier de sortie pour le fichier en cours de traitement."""
	_stack: Optional[np.ndarray] = field(init=False, default=None)
	"""Pile en cours de traitement."""
	_timestamp: str = field(init=False, default="")
	"""Suffixe des fichiers pour un traitement (timestamp au format ``YYYYMMDD_HHMMSS``)."""
	_timestamp_previous: str = field(init=False, default="")
	"""Suffixe des fichiers pour le traitement précédent (timestamp au format ``YYYYMMDD_HHMMSS``)."""
	_loading: bool = field(init=False, default=False)
	"""Indique qu'un chargement est en cours pour empêcher la réentrance depuis les signaux des paramètres."""

	_grapher: Grapher = field(init=False, default_factory=Grapher)
	"""Générateur de graphique."""
	_renderer: Renderer = field(init=False, default_factory=Renderer)
	"""Générateur de rendu."""

	_STEPS: list[Step] = field(init=False)
	"""Listes des étapes du pipeline de traitement."""

	# ==================================================
	# region Initialisation
	# ==================================================
	##################################################
	def __post_init__(self):
		"""Méthode appelée automatiquement après l'initialisation du dataclass."""
		self.filtering = Filtering(self.settings.filters, self.settings.rois)

		self._STEPS: list[Step] = [
				Step("localization", ["loc"], self._localization, self.filtering.localization),
				Step("beads", ["bds"], self._beads_extraction, lambda x: x, allow_dirty=True, apply_filter=False),
				Step("tracking", ["trc"], self._tracking, self.filtering.tracking),
				Step("blinking", ["blk"], self._blinking_reconnection, self.filtering.tracking),
				Step("track_analysis", ["MSD", "InD", "Fit"], self._track_analysis, self.filtering.track_analysis),
				# Step("gallery", "gallery", ["gallery"], self._gallery),
				# Step("graphical visualization", "visualization_graph", ["graph"], self._visualization_graph),
				# Step("high-resolution visualization", "visualization_hr", ["hr"], self._visualization_hr),
				]

	##################################################
	def is_dll_valid(self) -> bool:
		"""
		Vérifie la validité de la DLL utilisée par le plugin.

		:return: True si la DLL est valide, False sinon.
		"""
		return self.palm.is_valid()

	##################################################
	def clean_ui(self, name: str = "default"):
		"""
		Supprime l'interface Qt associée au nom donné pour les résultats et les paramètres.

		:param name: Nom de l'interface dans le dictionnaire.
		"""
		self.results.clean_ui(name)
		self.settings.clean_ui(name)

	# ==================================================
	# endregion Initialisation
	# ==================================================

	# ==================================================
	# region Accesseurs
	# ==================================================
	##################################################
	@property
	def path(self) -> str:
		"""Dossier de sortie pour le fichier en cours de traitement."""
		return self._path

	##################################################
	@property
	def stack(self) -> np.ndarray:
		"""Pile en cours de traitement."""
		return self._stack

	##################################################
	@property
	def suffix(self) -> str:
		"""Suffixe des fichiers pour un traitement (timestamp au format ``YYYYMMDD_HHMMSS``)."""
		return self._timestamp

	##################################################
	def _output_name(self, name: str, ext: str = "csv", previous: bool = False) -> Path:
		"""
		Indique le nom du fichier à enregistrer CHEMIN / name-Timestamp.extension.

		:param name: Nom du fichier.
		:param ext: Extension du fichier (par défaut csv, exception pour le log, les paramètres et les visualizations).
		:param previous: Si True, application du précédent timestamp. Sinon Timestamp Actuel.
		:return: Nom du fichier.
		"""
		return Path(self._path).resolve() / f"{name}-{self._timestamp_previous if previous else self._timestamp}.{ext}"

	##################################################
	def _save_setting_group(self, group_name: Literal["HR", "Filters"]):
		"""
		Met à jour un seul groupe dans le fichier de paramètres du traitement courant.

		:param group_name: Nom du groupe à enregistrer, sans écraser les autres paramètres du fichier.
		"""
		if not self._path or not self._timestamp: return
		settings_filename = self._output_name("settings", "json")
		if not settings_filename.is_file(): return

		data = FileIO.open_json(settings_filename)
		group = self.settings.hr if group_name == "HR" else self.settings.filters
		data["PALM Tracer Settings"][group_name] = group.to_compact_dict()
		FileIO.save_json(settings_filename, data)

	##################################################
	def output_viz_name(self) -> Path:
		"""
		Indique le nom du fichier de visualisation à enregistrer CHEMIN / name-Timestamp.extension.

		:return: Nom du fichier.
		"""
		s = self.settings.hr.settings
		dim, typ, rat, src, dft = s["Dimension"], s["Type"], s["Ratio"], s["Source"], s["Drift Correction"]
		suffix_drift = "_corrected" if dft else ""
		if dim == 0: suffix_dim, ext = "2d", "png"
		elif dim == 1: suffix_dim, ext = "z_stack", "tif"
		elif dim == 2: suffix_dim, ext = "3D_rotation", "tif"
		else: suffix_dim, ext = "track_stack", "tif"
		suffix_type = "localizations" if typ == 0 else "tracks"
		name = f"visualization_{suffix_dim}_{suffix_type}{suffix_drift}_x{rat}_{src}"
		return self._output_name(name, ext=ext, previous=False)

	# ==================================================
	# endregion Accesseurs
	# ==================================================

	# ==================================================
	# region Traitements
	# ==================================================
	##################################################
	def load(self, path: str = ""):
		"""Charge les précédents résultats du fichier courant sans chargement imbriqué.

		La restauration des paramètres peut déclencher un nouvel appel via les widgets
		connectés au Batch. Cet appel est ignoré pour préserver le dossier et le timestamp
		du chargement en cours ; un appel ultérieur reste possible.

		:param path: Dossier des résultats, ou chaîne vide pour utiliser le premier dossier du Batch.
		"""
		if self._loading: return
		self._loading = True
		try: self._load_results(path)
		finally: self._loading = False

	##################################################
	def _load_results(self, path: str):
		"""Effectue le chargement des paramètres, des résultats et de la pile.

		:param path: Dossier des résultats, ou chaîne vide pour utiliser le premier dossier du Batch.
		"""
		if not self.is_dll_valid():
			Ui.print_warning("Process not completed due to missing DLLs.")
			self.results.reset()
			return

		# --- Chargement des paramètres ---
		file = cast(FileList, self.settings.batch["Files"]).current_text
		self.results.stack_name = file
		self._path = self.settings.batch.get_paths()[0] if path == "" else path  # Parsing du batch
		self.results.results_folder = Path(self._path) if file else None
		settings_filename = FileIO.get_last_file(self._path, "settings")
		self._timestamp = FileIO.extract_suffix(settings_filename)
		if not settings_filename or not self._timestamp:
			Ui.print_warning("No valid settings file to load.")
			self.results.reset()
			return

		print(f"Loading setting file '{settings_filename}'.")
		with self.settings.signal_blocked():
			cfg = FileIO.open_json(settings_filename)
			self.settings.update_from_compact_dict(cfg)
			self.settings.localization["Preview"].value = False

		# --- Chargement des fichiers associés à ces paramètres. ---
		self.results.load(file, self._path, self._timestamp)

		# --- Chargement de la pile ---
		try:
			self._stack = self.settings.batch.get_stacks()[0]
			print(f"\tStack loaded successfully (size: {self._stack.shape}).")
		except Exception as e:
			print(f"\tError loading stack: {e}")

	##################################################
	def process(self):
		"""Lance le process de PALM selon les éléments en paramètres."""

		if not self.is_dll_valid():
			Ui.print_warning("Process not completed due to missing DLLs.")
			return

		# --- Parsing du batch ---
		paths = self.settings.batch.get_paths()
		stacks = self.settings.batch.get_stacks()
		if len(stacks) == 0:
			Ui.print_warning("No files.")
			return

		# --- Parcours du batch ---
		for self._path, self._stack in zip(paths, stacks):
			# Réinitialisation des DataFrames de résultats
			self.results.reset()

			# Logger
			Path(self._path).mkdir(parents=True, exist_ok=True)
			self._timestamp = FileIO.get_timestamp_for_files()
			self._logger.open(self._output_name("log", "log"))
			self._logger.add("Start Processing.")
			self._logger.add(f"Output folder: {self._path}")

			# Chargement du dernier Setting
			previous_settings_filename = FileIO.get_last_file(self._path, "settings")
			self._timestamp_previous = FileIO.extract_suffix(previous_settings_filename)
			if Path(previous_settings_filename).is_file():
				previous_settings = Settings()
				previous_settings.update_from_compact_dict(FileIO.open_json(previous_settings_filename))
			else:
				previous_settings = None

			# Save meta file (Création du DataFrame et sauvegarde en CSV)
			self.save_meta()

			# Enregistrement des paramètres une première fois pour avoir une trace
			FileIO.save_json(self._output_name("settings", "json"), self.settings.to_compact_dict())
			self._logger.add("Settings saved.")

			# Lancement des traitements
			pipeline_dirty = False
			for step in self._STEPS: pipeline_dirty = self._process_step(step, previous_settings, pipeline_dirty)

			# Lancement de la génération de Galeries
			if self.settings.gallery.active:
				self._logger.add("Gallery generation enabled.")
				self._gallery()
			else: self._logger.add("Gallery generation disabled.")

			# Lancement de la Visualisation graphique
			if self.settings.graph.active:
				self._logger.add("Graphical visualization enabled.")
				self._visualization_graph()
			else: self._logger.add("Graphical visualization disabled.")

			# Lancement de la Visualisation Haute Résolution
			if self.settings.hr.active:
				self._logger.add("High-resolution visualization enabled.")
				self._visualization_hr()
			else: self._logger.add("High-resolution visualization disabled.")

			# Enregistrement des paramètres (qui ont pu être modifié durant le process)
			FileIO.save_json(self._output_name("settings", "json"), self.settings.to_compact_dict())
			# Fermeture du Log
			self._logger.add("Processing complete.")
			self._logger.close()
			FileIO.cleanup_process(self._path, self._timestamp_previous)

	##################################################
	def save_meta(self):
		"""Sauvegarde le fichier méta (Création du DataFrame et sauvegarde en CSV si différent du précédent)."""
		prev_name = Path(self._output_name("meta", previous=True))
		prev_meta = pd.read_csv(prev_name) if prev_name.is_file() else None

		depth, height, width = self._stack.shape
		sc = self.settings.calibration
		meta = Parsing.get_meta([height, width, depth, sc["Pixel Size"].value, sc["Exposure"].value, sc["Intensity"].value])
		name = self._output_name("meta")

		if isinstance(prev_meta, pd.DataFrame) and np.allclose(prev_meta.to_numpy(), meta.to_numpy()): prev_name.rename(name)
		else: meta.to_csv(name, index=False)
		self._logger.add("Meta file saved.")

	##################################################
	def _process_step(self, step: Step, previous_settings: Settings | None, pipeline_dirty: bool) -> bool:
		"""
		Éffectue une étape du pipeline.

		:param step: Étape du pipeline.
		:param previous_settings: Paramètres du précédent pipeline.
		:param pipeline_dirty: État du pipeline (si True, Reuse est devenu impossible).
		:return: État d'invalidation du pipeline après le traitement de l'étape.
		"""
		group = getattr(self.settings, step.group_name)
		previous_group = getattr(previous_settings, step.group_name) if isinstance(previous_settings, Settings) else None

		action = prepare_step_action(group, previous_group, pipeline_dirty, step.allow_dirty)

		# --- Étape désactivée ---
		if action == StepAction.Skip:
			self._logger.add(f"{group.label} disabled.")
			return pipeline_dirty

		# --- Étape à récupérer du précédent pipeline ---
		if action == StepAction.Reuse:
			self._logger.add(f"{group.label} load previous result (Timestamp : {self._timestamp_previous}).")
			success = True
			for key in step.keys:
				old_file = self.results.output_name_by_key(key, self._path, self._timestamp_previous)
				new_file = self.results.output_name_by_key(key, self._path, self._timestamp)
				try:
					self.results[key] = pd.read_csv(old_file)
					self._logger.add(f"\tFile '{old_file.name}' loaded successfully, {len(self.results[key])} row(s) found.")
					old_file.rename(new_file)  # On renomme le fichier pour qu'à la prochaine étape, ce process soit celui du csv.
				except Exception as e:
					self._logger.add(f"\tError loading file '{old_file.name}': {e}")
					self.results[key] = pd.DataFrame()
					success = False

			if not success and group.active: action = StepAction.Compute

		# --- Étape à calculer ---
		if action == StepAction.Compute:
			self._logger.add(f"{group.label} enabled.")
			try: step.process_func()
			except Exception: raise
			pipeline_dirty = True  # Pipeline incohérent pour la suite, on évitera de réutiliser des éléments précédents, car un calcul a été fait

		# --- Filtrage ---
		if not step.apply_filter: return pipeline_dirty
		# Cas standard : un seul DataFrame
		if len(step.keys) == 1:
			f_key = f"f_{step.keys[0]}"
			self.results[f_key] = step.filter_func(self.results[step.keys[0]])
			n_init, n_end = len(self.results[step.keys[0]]), len(self.results[f_key])
			if n_init != n_end:
				self._logger.add(f"\t\tFiltering of file {n_end} row(s) instead of {n_init}: {n_init - n_end} deletion(s).")
				if self.settings.filters["Save"].value and n_end != 0:
					self._logger.add(f"\t\tSaving the filtered file.")
					self.results.save(f_key, self._path, self._timestamp)
			else:
				self.results[f_key] = pd.DataFrame()
		# Cas spécial de l'analyse des trajectoires, qui modifie plusieurs résultats simultanément
		else:
			n_init = len(self.results["MSD"])
			o_name = self.results.get_tracks_key()
			if "f_" not in o_name: o_name = f"f_{o_name}"  # Si aucun filtre la clé sera sans le f_ devant
			self.results[o_name], self.results["f_MSD"], self.results["f_InD"], self.results["f_Fit"] \
				= step.filter_func(self.results.tracks, self.results["MSD"], self.results["InD"], self.results["Fit"])

			n_end = len(self.results["f_MSD"])
			if n_init != n_end:
				self._logger.add(f"\t\tFiltering of files {n_end} row(s) instead of {n_init}: {n_init - n_end} deletion(s)")
				if self.settings.filters["Save"].value:
					for key, name in [(o_name, "tracking"), ("f_MSD", "MSD"), ("f_InD", "Instant Diffusion"), ("f_Fit", "Fit")]:
						if not self.results[key].empty:
							self._logger.add(f"\t\tSaving the filtered {name} file.")
							self.results.save(key, self._path, self._timestamp)
			else:
				for key in ["f_MSD", "f_InD", "f_Fit"]: self.results[key] = pd.DataFrame()

		return pipeline_dirty

	##################################################
	def _localization(self):
		"""Lance la localisation à partir des paramètres de l'interface."""
		# Parse settings
		s = self.settings.localization.settings
		filters = self.settings.filters
		# Filtre sur les plans
		planes = filters["Plane"].value
		planes = list(range(planes[0] - 1, planes[1])) if filters["Plane"].active else None
		fit = self.settings.localization.get_fit()
		try: fit_params = self.settings.localization.get_fit_params()
		except Exception: raise
		# Run command
		self.results["loc"] = self.palm.localization(self._stack, s["Threshold"], s["Watershed"], fit, fit_params, planes)

		# Estimation du Z.
		if not self.results["loc"].empty and fit in (3, 4) and s["Gaussian Fit Z"]:
			model = self._get_astigmatism_model(Path(s["Gaussian Fit Model"]))

			if model.empty:
				self._logger.add("\tNo valid astigmatism model file for Z Estimation "
								 "(by default, file must be in output folder or in same folder as the stack).")
			else:
				z_max = s["Gaussian Fit Z max"]
				pixel_size = self.settings.calibration["Pixel Size"].value * 1000  # Passage en nanomètres
				points = self.results["loc"].loc[:, ["Sigma X", "Sigma Y"]].to_numpy(dtype=float, copy=True)
				estimated_z = self.palm.astigmatism_3d_estimation(points, pixel_size, model.to_numpy(), z_max)
				self.results["loc"][["Z", "MSE Z"]] = estimated_z

		self._logger.add(f"\tSaving the localization file ({len(self.results['loc'])} localization(s) found).")
		self.results.save("loc", self._path, self._timestamp)

	##################################################
	def _get_astigmatism_model(self, path: Path) -> pd.DataFrame:
		"""
		Charge un modèle d'astigmatisme 3D depuis un fichier CSV.

		La fonction tente de lire le fichier spécifié par ``path``.
		Si ce chemin n'est pas valide, elle cherche automatiquement un fichier nommé ``astigmatism_3d_model.csv`` dans :
		le dossier ``self._path``, puis dans le dossier parent de ``self._path``.

		Si aucun fichier valide n'est trouvé, ou si le fichier est invalide, une DataFrame vide est retournée.

		:param path: Chemin vers un fichier CSV contenant le modèle d'astigmatisme.
		:return: DataFrame contenant le modèle si valide, sinon une DataFrame vide.
		:raises Exception: Aucune exception n'est propagée. En cas d'erreur de lecture, un message est affiché via ``Ui.print_error``.

		.. note::
		        Le fichier doit respecter la forme attendue définie par ``Parsing.SHAPE_MODEL``.
		        Si ce n'est pas le cas, le modèle est considéré comme invalide.

		.. tip:: Permet de rendre l'appel robuste en cas de chemin utilisateur invalide, en utilisant automatiquement des emplacements par défaut du projet.
		"""
		res = pd.DataFrame()
		final_path = Path(path)

		if not final_path.is_file():
			model_name = "astigmatism_3d_model.csv"
			_path = Path(self._path)
			final_path = _path / model_name
			if not final_path.is_file():
				final_path = _path.parent / model_name
				if not final_path.is_file(): return pd.DataFrame()

		try:
			res = pd.read_csv(final_path, index_col=0)
			if res.shape != Parsing.SHAPE_MODEL: return pd.DataFrame()
		except Exception as e: Ui.print_error(f"Unable to read the model file: {e}.")

		return res

	##################################################
	def _beads_extraction(self):
		"""Extrait les billes des localisations."""
		df = self.results.localizations  # Récupère automatiquement le "bon" DataFrame (filtré ou non)
		if "Integrated Intensity" in df.columns: df = df[df["Integrated Intensity"] > 0]  # Suppression des éléments où l'ajustement a échoué.
		if df.empty:
			self._logger.add("\tNo localizations data calculated, no additional calculations can be performed.")
			return

		s = self.settings.beads.settings
		try: self.results["bds"] = Drift.extract_beads(df, s["Max Distance"], s["3D"], strict=False, k=2)
		except ValueError: self.results["bds"] = pd.DataFrame()
		if self.results["bds"].empty:
			self._logger.add("\tNo beads found.")
			return
		self._logger.add(f"\tSaving the beads file ({self.results['bds'].iloc[-1, 0]} beads(s) found).")
		self.results.save("bds", self._path, self._timestamp)

	##################################################
	def _tracking(self):
		"""Lance le suivi à partir des paramètres de l'interface."""
		df = self.results.localizations  # Récupère automatiquement le "bon" DataFrame (filtré ou non)
		if "Integrated Intensity" in df.columns: df = df[df["Integrated Intensity"] > 0]  # Suppression des éléments où l'ajustement a échoué.
		if df.empty:
			self._logger.add("\tNo localizations data calculated, no additional calculations can be performed.")
			return

		s = self.settings.tracking.settings
		self.results["trc"] = self.palm.tracking(df, s["Max Distance"])

		self._logger.add(f"\tSaving the tracking file ({len(self.results['trc'])} point(s) found).")
		self.results.save("trc", self._path, self._timestamp)

	##################################################
	def _blinking_reconnection(self):
		"""Lance le tracking à partir des paramètres de l'interface."""
		df = self.results["trc"]  # Récupère le DataFrame du suivi non filtré (si jamais il existe)
		if df.empty:
			self._logger.add("\tNo tracking data calculated, no additional calculations can be performed.")
			return

		s = self.settings.blinking.settings
		self.results["blk"] = self.palm.blinking_reconnection(df, 1, s["Mode"], s["Max Duration"], s["Max Distance"])

		self._logger.add(f"\tSaving the reconnected tracking file ({len(self.results['blk'])} point(s) found).")
		self.results.save("blk", self._path, self._timestamp)

	##################################################
	def _track_analysis(self):
		"""Lance les analyses des trajectoires à partir des paramètres de l'interface."""
		df = self.results.tracks  # Récupère automatiquement le "bon" DataFrame (blinking et filtré ou non)
		if df.empty:
			self._logger.add("\tNo tracking data available, no track analysis can be performed.")
			return

		# Parse settings
		sc = self.settings.calibration.settings
		s = self.settings.track_analysis.settings

		if not s["MSD"] and not s["Instant Diffusion"] and s["Fit"] == 0:
			self._logger.add("\tNo metrics selected, no track analysis can be performed.")
			return

		if s["MSD"] and s["Fit"] == 0: s["Fit"] = 1  # Si le MSD est sélectionné et pas d'ajustement, on fait un ajustement minimal.

		# Run command (pixel size doit rester en micromètre cette fois, car toutes les mesures seront en micromètres carré)
		res = self.palm.track_analysis(df, s["MSD"], s["Instant Diffusion"], s["3D"],
									   sc["Pixel Size"], sc["Exposure"], s["Fit"], np.array([s["Fit Length"]], dtype=float))
		for key in res: self.results[key] = res[key]

		for key, name in [("MSD", "MSD"), ("InD", "Instant Diffusion"), ("Fit", "Fit")]:
			if s[name] and not res[key].empty:
				self._logger.add(f"\tSaving the {name} file.")
				self.results.save(key, self._path, self._timestamp)

	# ==================================================
	# endregion Traitements
	# ==================================================

	# ==================================================
	# region Filtrage
	# ==================================================
	##################################################
	def reset_filtered(self):
		"""Vide entièrement les DataFrames filtrés dans ``df``."""
		with self.settings.signal_blocked(): self.settings.filters.deactivate_filters()
		self.results.reset_filtered()
		self._save_setting_group("Filters")

	##################################################
	def update_filtered(self, last: bool = True):
		"""
		Recalcule les filtres sur le dernier DataFrame disponible pour chacun si last est sélectionné, sinon sur l'original.

		:param last: Utilise les dernières versions des DataFrames si ``True``, sinon les données brutes seront utilisées.
		"""
		df = {}
		for key in ["loc", "dft", "trc", "blk", "MSD", "InD", "Fit"]:
			df[key] = self.results[key] if self.results[f"f_{key}"].empty or not last else self.results[f"f_{key}"]

		self.results["f_loc"] = self.filtering.localization(df["loc"])
		self.results["f_dft"] = self.filtering.localization(df["dft"])
		self.results["f_trc"] = self.filtering.tracking(df["trc"])
		self.results["f_blk"] = self.filtering.tracking(df["blk"])

		o_name = "f_trc" if self.results["f_blk"].empty else "f_blk"
		self.results[o_name], self.results["f_MSD"], self.results["f_InD"], self.results["f_Fit"] \
			= self.filtering.track_analysis(self.results.tracks, df["MSD"], df["InD"], df["Fit"])

		for key in ["loc", "dft", "trc", "blk"]:
			f_key = f"f_{key}"
			if len(self.results[key]) == len(self.results[f_key]): self.results[f_key] = pd.DataFrame()

		if self.settings.filters["Save"].value: self.save_filtered()
		self._save_setting_group("Filters")

	##################################################
	def save_filtered(self):
		"""Enregistre tous les fichiers filtrés s'ils ne sont pas vides."""
		self.results.save_filtered(self._path, "")

	##################################################
	def connect_filters_button(self, ui_name: str = "default"):
		"""Connecte les boutons d'une interface de filtre."""
		filters = self.settings.filters
		filters.connect_button(self.reset_filtered, ui_name, "reset")
		filters.connect_button(self.update_filtered, ui_name, "update")
		filters.connect_button(self.save_filtered, ui_name, "save")

	# ==================================================
	# endregion Filtrage
	# ==================================================

	# ==================================================
	# region Visualisation
	# ==================================================
	##################################################
	def _gallery(self):
		"""Lance la génération d'une galerie à partir des paramètres passés en paramètres."""
		s = self.settings.gallery.settings
		loc = self.results.localizations
		if loc.empty:
			self._logger.add(f"\tNo localization data for gallery generation.")
			return
		gallery = Gallery.make_gallery(self._stack, loc, s["ROI Size"], s["ROIs Per Line"])
		self._logger.add(f"\tSaving gallery ({s}).")
		FileIO.save_tif(gallery, self._output_name(f"gallery_{s['ROI Size']}_{s['ROIs Per Line']}", "tif"))

	# ==================== Graph ====================
	##################################################
	def graph(self) -> go.Figure:
		"""Construit la figure Plotly courante en fonction du domaine et de la source."""
		s = self.settings.graph.settings
		mode, limit, sigma = s["Mode"], s["Display Limits"], s["Display Sigma"]
		kde, gauss, gauss_mix = s["Display KDE"], s["Display Gauss"], s["Display Gauss Mix"]
		poiss, expo = s["Display Poiss"], s["Display Exp"]
		cumul, density, bins = s["Display Cumul"], not s["Display Count"], s["Display Bins"]

		# Préparation des Données
		graph_data = self._get_graph_data()
		data, title = graph_data["data"], graph_data["title"]
		xlabel, ylabel = graph_data.get("xlabel", ""), graph_data.get("ylabel", "")
		# TODO : avertir avant l'affichage de plusieurs millions de valeurs.

		# Selection du graphique à afficher
		# --- Histogramme ---
		if mode == 0:
			bins = graph_data.get("bins", bins)
			fit_limit = graph_data.get("fit_limit", -np.inf)
			return self._grapher.histogram(data, title, xlabel=xlabel, ylabel=ylabel, limit=limit, show_sigma=sigma, kde=kde, gaussian=gauss, poissonian=poiss,
										   exponential=expo, density=density, cumulative=cumul, bins=bins, gaussian_mixture=gauss_mix, fit_limit=fit_limit)
		# --- Courbe Scatter plot ---
		if mode == 1: return self._grapher.scatter(data, title, xlabel=xlabel, ylabel=ylabel, limit=limit, show_sigma=sigma, names=graph_data.get("names"))

		# --- Nuage de points ---
		return self._grapher.cloud(data, title, xlabel=xlabel, ylabel=ylabel, limit=limit, show_sigma=sigma, kde=kde, gaussian=gauss,
								   poissonian=poiss, exponential=expo)

	##################################################
	@staticmethod
	def _log_data(data: np.ndarray, log: bool) -> np.ndarray:
		"""
		Application du log avec suppression du warning pour les valeurs ≤ 0 et remplacement par Nan de ces valeurs.

		:param data: Données à transformer.
		:param log: Application du log ou non.
		:return: Données transformées.
		"""
		with np.errstate(divide='ignore', invalid='ignore'): return np.where(data > 0, np.log10(data), np.nan) if log else data

	##################################################
	def _get_graph_data(self) -> dict[str, Any]:
		"""
		Récupère et prépare les données pour l'affichage.

		:return: Dictionnaire des données, du titre et des arguments de rendu définis par les sources.
		"""
		s = self.settings.graph.settings
		src_id, mode, log_scale = s["Type"], s["Mode"], s["Display Log Scale"]
		src_a = cast(Combo, self.settings.graph["Source"]).current_text

		graph_data = self._get_graph_data_from_src(src_id, src_a, log_scale, mode == 2)
		if mode == 2:
			src_b = cast(Combo, self.settings.graph["Source B"]).current_text
			graph_data["title"] += f" / {src_b}"
			graph_data["xlabel"], graph_data["ylabel"] = src_a, src_b
			d = graph_data["data"]
			d_b = self._get_graph_data_from_src(src_id, src_b, log_scale, mode == 2)["data"]
			if src_id == 1 and d.ndim == 2 and d_b.ndim == 2:
				source_a = pd.DataFrame(d, columns=["Track", "Source A"])
				source_b = pd.DataFrame(d_b, columns=["Track", "Source B"])
				common = source_a.merge(source_b, on="Track", how="inner", sort=False)
				graph_data["data"] = common[["Source A", "Source B"]].to_numpy().T if not common.empty else np.empty(0)
			elif d.ndim != d_b.ndim or d_b.size != d.size: graph_data["data"] = np.empty(0)
			else: graph_data["data"] = np.vstack((d, d_b))

		return graph_data

	##################################################
	def _get_graph_data_from_src(self, src_type: int, src: str, log_scale: bool = False, with_track_ids: bool = False) -> dict[str, Any]:
		"""
		Oriente la préparation d'une source vers le domaine et le mode concernés.

		:param src_type: Domaine sélectionné : localisations (0) ou trajectoires (1).
		:param src: Grandeur à représenter.
		:param log_scale: Applique le logarithme aux valeurs, après l'éventuelle moyenne.
		:param with_track_ids: Conserve les identifiants nécessaires à l'association des sources de trajectoires en Dual.
		:return: Dictionnaire contenant toujours ``data`` et ``title``. Les clés ``xlabel``, ``ylabel``, ``names``,
			``fit_limit`` et ``bins`` sont ajoutées selon la source et le mode.
		"""
		mode = self.settings.graph["Mode"].value
		if src_type == 0: return self._get_localization_graph_data(src, mode, log_scale)
		if mode == 1: return self._get_track_scatter_data(src, log_scale)
		return self._get_track_graph_data(src, log_scale, with_track_ids)

	##################################################
	def _get_localization_graph_data(self, src: str, mode: int, log_scale: bool) -> dict[str, Any]:
		"""
		Prépare les valeurs individuelles, les comptes ou les moyennes par plan des localisations.

		Les plans sans localisation ont un compte nul et une moyenne absente (NaN).
		L'intervalle couvre le premier au dernier plan représenté dans les résultats actifs.

		:param src: Grandeur de localisation à représenter.
		:param mode: Mode sélectionné : histogramme (0), Scatter (1) ou Dual (2).
		:param log_scale: Applique le logarithme aux valeurs, après la moyenne en Scatter.
		:return: Données et titre, avec axes en Scatter et seuil d'ajustement pour les sources concernées en histogramme.
		"""
		graph_data: dict[str, Any] = {"data": np.empty(0), "title": f"Localizations {src}"}
		if mode == 1: graph_data["xlabel"], graph_data["ylabel"] = "Plane", src
		if mode == 0 and not log_scale and src in {"Integrated Intensity", "Sigma X", "Sigma Y", "Circularity", "Surface", "MSE XY", "MSE Z"}:
			graph_data["fit_limit"] = -1.0  # Les échecs à -1 sont déjà supprimés par le logarithme ; zéro reste admissible.

		df = self.results.localizations
		if df.empty: return graph_data
		if src == "Count per Plane":
			plane = df["Plane"].astype(int)
			planes = np.arange(int(plane.min()), int(plane.max()) + 1, dtype=int)
			counts = plane.groupby(plane).size().reindex(pd.Index(planes), fill_value=0).to_numpy(dtype=int)
			graph_data["data"] = np.vstack((planes, counts))
			return graph_data

		column = df.get(src)
		if column is None: return graph_data
		values = column.to_numpy(dtype=float)
		if mode != 1:
			graph_data["data"] = self._log_data(values, log_scale)
			return graph_data

		finite_values = pd.Series(np.where(np.isfinite(values), values, np.nan), index=df.index)
		means = finite_values.groupby(df["Plane"].astype(int), sort=True).mean()
		planes = np.arange(int(means.index.min()), int(means.index.max()) + 1, dtype=int)
		# Les plans vides restent absents de la moyenne, contrairement au compte qui vaut zéro.
		values = means.reindex(pd.Index(planes)).to_numpy(dtype=float)
		graph_data["data"] = np.vstack((planes, self._log_data(values, log_scale)))
		graph_data["title"] += " Mean per Plane"
		return graph_data

	##################################################
	def _get_track_scatter_data(self, src: str, log_scale: bool) -> dict[str, Any]:
		"""
		Prépare les courbes individuelles ou moyennes des trajectoires, ou leurs trois comptages par plan.

		Les courbes individuelles ont la forme ``(T, 2, N)`` et les courbes moyennes ``(2, N)``.
		Les steps et fenêtres sont des indices relatifs à chaque trajectoire ; les intensités et comptes utilisent les plans réels.
		Les valeurs négatives et non finies sont absentes. Zéro et le plancher positif de diffusion restent admissibles.

		:param src: Source Scatter : intensité, MSD, diffusion instantanée, leur moyenne ou compte des trajectoires.
		:param log_scale: Applique le logarithme aux valeurs, après l'éventuelle moyenne.
		:return: Données, titre, axes et noms des courbes lorsqu'ils sont nécessaires.
		"""
		graph_data: dict[str, Any] = {"data": np.empty(0), "title": f"Tracks {src}"}
		mean, source = src.endswith(" Mean"), src.removesuffix(" Mean")
		labels = {"Track Count": ("Plane", "Track Count"), "Integrated Intensity": ("Plane", "Integrated Intensity"),
				  "MSD":         ("Step (planes)", "MSD (μm²)"), "Instant D": ("Window", "Instant D (μm²/s)")}
		if source not in labels or (mean and source == "Track Count"): return graph_data
		xlabel, ylabel = labels[source]
		graph_data["xlabel"], graph_data["ylabel"] = xlabel, f"log10({ylabel})" if log_scale else ylabel

		# Comptage
		if source == "Track Count":
			graph_data["names"] = ["In Progress", "Present", "Absent"]
			graph_data["data"] = self._get_track_count_data(log_scale)
			return graph_data

		# Intensité intégrée
		if source == "Integrated Intensity":
			if not mean and "Track" in self.results.tracks.columns:
				graph_data["names"] = [f"Track {track}" for track in self.results.tracks["Track"].drop_duplicates().astype(int)]  # Plusieurs courbes
			graph_data["data"] = self._get_track_intensity_data(mean, log_scale)
			return graph_data

		# MSD et Instant Diffusion
		key, prefix = ("InD", "Window ") if source == "Instant D" else ("MSD", "Step ")
		df = self.results.track_analysis[key]
		if df.empty or "Track" not in df.columns: return graph_data
		if not mean: graph_data["names"] = [f"Track {track}" for track in df["Track"].astype(int)]  # Plusieurs courbes identifiées
		columns = [col for col in df.columns if col.startswith(prefix) and col[len(prefix):].isdigit() and int(col[len(prefix):]) > 0]
		if not columns: return graph_data
		steps = np.arange(1, max(int(col[len(prefix):]) for col in columns) + 1, dtype=int)
		values = df.reindex(columns=[f"{prefix}{step}" for step in steps]).to_numpy(dtype=float)
		valid = np.isfinite(values) & (values >= 0)
		values = np.where(valid, values, np.nan)
		if mean:  # Moyenne des trajectoires
			counts = valid.sum(axis=0)
			means = np.full(steps.size, np.nan)
			# Chaque trajectoire admissible possède le même poids au step ou à la fenêtre considéré.
			np.divide(np.nansum(values, axis=0), counts, out=means, where=counts > 0)
			graph_data["data"] = np.vstack((steps, self._log_data(means, log_scale)))
		else: graph_data["data"] = np.stack((np.broadcast_to(steps, values.shape), self._log_data(values, log_scale)), axis=1)
		return graph_data

	##################################################
	def _get_track_graph_data(self, src: str, log_scale: bool, with_track_ids: bool) -> dict[str, Any]:
		"""
		Prépare une grandeur de trajectoire pour l'histogramme ou le Dual Source.

		Les longueurs proviennent des points des trajectoires, les autres grandeurs des analyses actives.
		Les règles de classes entières et d'exclusion des sentinelles lors des ajustements sont transmises dans le dictionnaire.

		:param src: Grandeur de trajectoire à représenter.
		:param log_scale: Applique une transformation logarithmique aux valeurs.
		:param with_track_ids: Conserve les identifiants et agrège les segments On/Off par trajectoire pour le Dual Source.
		:return: Données et titre, avec bins entiers pour les longueurs et seuil d'ajustement lorsqu'il est applicable.
		"""
		graph_data: dict[str, Any] = {"data": np.empty(0), "title": f"Tracks {src}"}
		if self.settings.graph["Mode"].value == 0:
			if src in {"Instant D", "D(0) (μm²/s)", "A (μm²/s)"}:
				graph_data["fit_limit"] = float(np.log10(Parsing.TRACK_ANALYSIS_MIN)) if log_scale else Parsing.TRACK_ANALYSIS_MIN
			elif src == "MSD" and not log_scale: graph_data["fit_limit"] = -1.0

		if "Length" in src:
			graph_data["bins"] = -1  # Bins sur des nombres entiers.
			graph_data["data"] = self._get_track_length_data(src, with_track_ids)
			return graph_data

		analysis = self.results.track_analysis
		if src == "Instant D":
			values = analysis["InD"].drop(columns=["Track"], errors="ignore").to_numpy().ravel()  # Mélange de toutes les valeurs
			values = self._log_data(values, log_scale)
			graph_data["data"] = values[np.isfinite(values)]
			return graph_data

		df = analysis["MSD"] if src == "MSD" else analysis["Fit"]
		if df.empty: return graph_data
		column = src
		if src == "MSD":
			column = f"Step {self.settings.graph['MSD Step'].value}"
			graph_data["title"] += f" {column}"
		if not {"Track", column}.issubset(df.columns): return graph_data
		tracks = df["Track"].astype(int).to_numpy()
		values = self._log_data(df[column].to_numpy(dtype=float), log_scale)
		data = np.column_stack((tracks, values))
		graph_data["data"] = data[np.isfinite(data).all(axis=1)]
		return graph_data

	##################################################
	def _get_track_length_data(self, src: str, with_track_ids: bool) -> np.ndarray:
		"""
		Calcule les durées totales, présentes (On) ou absentes (Off) des trajectoires actives.

		La longueur totale couvre le premier au dernier plan inclus.
		Les durées ``On`` sont les segments de présence consécutive, et les durées ``Off`` les intervalles absents entre ces segments.
		En Dual Source, les durées On/Off sont moyennées par trajectoire.

		:param src: Source de longueur : ``Length``, ``Length On`` ou ``Length Off``.
		:param with_track_ids: Renvoie un couple identifiant/valeur par trajectoire au lieu des durées individuelles.
		:return: Durées sous forme 1D, ou couples trajectoire/durée sous forme ``(T, 2)``.
			L'ancienne source ``Length Scatter`` conserve également les identifiants.
		"""
		df = self.results.tracks
		if df.empty: return np.empty(0)
		tracks_planes = df.groupby("Track", sort=False)["Plane"]
		if src in {"Length Scatter", "Length"}:
			bounds = tracks_planes.agg(["min", "max"])
			total_lengths = (bounds["max"] - bounds["min"] + 1).to_numpy()
			if src == "Length Scatter" or with_track_ids: return np.column_stack((bounds.index.to_numpy(), total_lengths))
			return total_lengths

		lengths: list[int] = []
		lengths_by_track: list[tuple[int, float]] = []
		for track, planes in tracks_planes:
			planes_array = np.sort(planes.dropna().unique())
			if planes_array.size == 0: continue  # pragma: no cover — Plane est toujours valide.
			diffs = np.diff(planes_array)
			breaks = np.flatnonzero(diffs > 1)
			if src == "Length On": track_lengths = np.diff(np.concatenate(([-1], breaks, [planes_array.size - 1])))
			elif src == "Length Off": track_lengths = diffs[breaks] - 1
			else: continue
			lengths.extend(track_lengths.tolist())
			if with_track_ids and track_lengths.size > 0: lengths_by_track.append((int(track), float(np.mean(track_lengths))))
		if with_track_ids: return np.asarray(lengths_by_track) if lengths_by_track else np.empty((0, 2))
		return np.asarray(lengths, dtype=int)

	##################################################
	def _get_track_intensity_data(self, mean: bool, log_scale: bool) -> np.ndarray:
		"""
		Prépare les intensités par trajectoire ou leur moyenne par plan réel.

		Les intensités négatives et non finies sont exclues. Les éventuels doublons d'un couple trajectoire/plan sont moyennés
		pour que chaque trajectoire contribue une seule fois par plan. Les absences restent des trous, sans interpolation.

		:param mean: Renvoie une seule moyenne par plan si ``True``, sinon une courbe par trajectoire.
		:param log_scale: Applique le logarithme après l'éventuelle moyenne.
		:return: Couples plan/intensité sous forme ``(2, N)`` ou ``(T, 2, N)``, complétés par NaN.
		"""
		df = self.results.tracks
		if df.empty or not {"Track", "Plane", "Integrated Intensity"}.issubset(df.columns): return np.empty(0)
		values = df["Integrated Intensity"].to_numpy(dtype=float)
		values = pd.Series(np.where(np.isfinite(values) & (values >= 0), values, np.nan), index=df.index)
		points = values.groupby([df["Track"], df["Plane"].astype(int)], sort=False).mean()
		if mean:
			means = points.groupby(level=1, sort=True).mean()
			planes = np.arange(int(means.index.min()), int(means.index.max()) + 1, dtype=int)
			return np.vstack((planes, self._log_data(means.reindex(pd.Index(planes)).to_numpy(dtype=float), log_scale)))

		curves: list[np.ndarray] = []
		for _, track in points.groupby(level=0, sort=False):
			track = track.droplevel(0).sort_index()
			planes = track.index.to_numpy(dtype=float)
			intensities = self._log_data(track.to_numpy(dtype=float), log_scale)
			# Un seul NaN par intervalle absent suffit à interrompre la ligne, sans allouer tous les plans de chaque trajectoire.
			gaps = np.flatnonzero(np.diff(planes) > 1) + 1
			curves.append(np.vstack((np.insert(planes, gaps, np.nan), np.insert(intensities, gaps, np.nan))))
		if not curves: return np.empty(0)  # pragma: no cover - Garde impossible, car vérifié en amont.
		data = np.full((len(curves), 2, max(curve.shape[1] for curve in curves)), np.nan)
		for i, curve in enumerate(curves): data[i, :, :curve.shape[1]] = curve
		return data

	##################################################
	def _get_track_count_data(self, log_scale: bool) -> np.ndarray:
		"""
		Compte par plan les trajectoires en cours, présentes et absentes, dans cet ordre.

		Une trajectoire est en cours du premier au dernier plan inclus. Elle est présente si elle possède un point au plan considéré,
		indépendamment de la validité de son intensité. Les doublons trajectoire/plan ne sont comptés qu'une fois.
		Avant logarithme, le nombre de trajectoires en cours est la somme des nombres de trajectoires présentes et absentes.

		:param log_scale: Applique le logarithme aux comptes ; les comptes nuls deviennent NaN.
		:return: Trois courbes de couples plan/compte sous forme ``(3, 2, N)``.
		"""
		df = self.results.tracks
		if df.empty or not {"Track", "Plane"}.issubset(df.columns): return np.empty(0)
		points = df[["Track", "Plane"]].drop_duplicates()
		bounds = points.groupby("Track", sort=False)["Plane"].agg(["min", "max"])
		planes = np.arange(int(bounds["min"].min()), int(bounds["max"].max()) + 1, dtype=int)
		# Somme cumulative des débuts et fins : évite de parcourir tous les plans de toutes les trajectoires.
		changes = np.zeros(planes.size + 1, dtype=int)
		np.add.at(changes, bounds["min"].to_numpy(dtype=int) - planes[0], 1)
		np.add.at(changes, bounds["max"].to_numpy(dtype=int) - planes[0] + 1, -1)
		in_progress = np.cumsum(changes[:-1])
		present = points.groupby("Plane").size().reindex(pd.Index(planes), fill_value=0).to_numpy(dtype=int)
		counts = np.vstack((in_progress, present, in_progress - present))
		return np.stack((np.broadcast_to(planes, counts.shape), self._log_data(counts, log_scale)), axis=1)

	##################################################
	def _visualization_graph(self):
		"""Lance la creation d'une visualisation graphique à partir des paramètres."""
		s = self.settings.graph.settings
		name = f"graph_{self.settings.graph['Type'].value}_{cast(Combo, self.settings.graph['Source']).current_text}"
		self.graph().write_html(self._output_name(name, ext=".html"))
		self._logger.add(f"\tSaving Graph ({s}).")

	# ==================== HR ====================
	##################################################
	def hr(self) -> dict[str, np.ndarray]:
		"""
		Génère une représentation en haute résolution des données.

		:return: Dictionnaire contenant l'image ``visualization``, les coordonnées vectorielles ``plot_data`` et, si les localisations actives sont
			filtrées, les coordonnées des points exclus ``plot_filtered``. Ces points partagent le repère du rendu sans contribuer à l'image.
		"""
		data = {"visualization": np.zeros((1, 1), dtype=np.uint16), "plot_data": np.zeros((1, 1), dtype=float)}
		if self._stack is None: return data

		# --- Paramètres ---
		s = self.settings.hr
		src = cast(Combo, s["Source"]).current_text
		upscale, color_scaling = s["Ratio"].value, s["Scaling"].value
		color_mode = 0 if src == "Count" else s["Color mode"].value  # .	La source Count impose le mode cumulatif.
		bg_color = round(s["Background"].value * MAX_UI_16 / 100)  # .		Conversion du pourcentage en intensité uint16.
		dimension, tracks = s["Dimension"].value, s["Type"].value == 1

		# Mise à jour de la zone de travail en fonction des données
		gaussian = s.gaussian.settings if s.gaussian.active else None
		# Les positions non corrigées ne bornent pas les déplacements produits par le drift.
		with_drift = s["Drift Correction"].value and not self.results.beads.empty
		crop_data, crop_margin = None, 5
		if s["Crop"].value and dimension in (0, 1, 3) and not with_drift:
			crop_data = self.results.tracks if tracks else self.results.localizations
			if tracks and dimension == 3:
				# Le demi-diamètre maximal du dessin HR est converti en pixels source, arrondis vers l'extérieur.
				st = s.track_stack
				radius = max(st["Head"].value, st["Width"].value) // 2
				crop_margin += int(np.ceil(radius / upscale))
		self.settings.rois.update_data_box(crop_data, gaussian, crop_margin)

		# Mise à jour de la zone de travail avec les régions d'intérêts
		time_filter = cast(CheckRangeInt, self.settings.filters.tracking["Time Inside ROI"]) if tracks else None
		limits = self.settings.rois.get_hr_limits(time_filter)
		x0, x1, y0, y1 = limits
		n_w, n_h = x1 - x0, y1 - y0
		self._renderer.set_size(n_w, n_h, upscale)

		viz_data, plot, uniform_z_step = self._prepare_hr_data(tracks, dimension, src, color_scaling, upscale, limits)
		data.update(plot)
		if viz_data is None: return data

		# --- Localisations ---
		if not tracks:
			if dimension == 0:  # .	-- Rendu 2D --
				viz = self._renderer.localizations(viz_data, color_mode, bg_color, gaussian)
			elif dimension == 1:  # -- Rendu Z Stack --
				z_step = s.hr_3d["Z Step"].value
				viz = self._renderer.z_stack(viz_data, color_mode, z_step if z_step != 0 else uniform_z_step, bg_color, gaussian)
			else:  # .				-- Rendu 3D Rotation --
				frames, axis = s.hr_3d["Frames"].value, s.hr_3d["Axis"].value
				viz = self._renderer.rotation_3d(viz_data, color_mode, uniform_z_step, frames, axis, bg_color, gaussian, crop=s["Crop"].value)
			data["visualization"] = viz
			return data

		# --- Tracks ---
		if dimension == 3:
			first_plane = int(np.min(viz_data[:, 1]))
			st = s.track_stack
			raw = self._stack[:, y0:y1, x0:x1] if st["Background"].value else None
			head_size, tail_width, tail_length = st["Head"].value, st["Width"].value, st["Length"].value
			fade_type, upscale_type, color_lut = st["Fade"].value, st["Upscale"].value, cast(ColorMap, st["Map"]).get_lut()
			viz = self._renderer.track_stack(viz_data, color_mode, bg_color, head_size, tail_width, tail_length, fade_type, raw, upscale_type, color_lut)
			# Aligne les trajectoires Napari sur le premier plan retenu par le renderer.
			if data["plot_data"].shape[0] > 0: data["plot_data"][:, 1] -= first_plane
			data["visualization"] = viz
			return data

		data["visualization"] = self._renderer.tracks(viz_data, color_mode, bg_color)
		return data

	##################################################
	def _prepare_hr_data(self, tracks: bool, dimension: int, source: str, color_scaling: float, upscale: float,
						 limits: tuple[int, int, int, int]) -> tuple[Optional[np.ndarray], dict[str, np.ndarray], float]:
		"""
		Prépare les données du rendu et du calque Napari haute résolution.

		Les trajectoires conservent leurs points extérieurs dans les données de rendu afin que les segments traversant la ROI soient correctement recadrés.
		Seules les coordonnées transmises au calque Napari sont limitées à la zone affichée.
		Pour les localisations filtrées, le DataFrame complet est transformé une seule fois avant de séparer les points conservés et exclus.

		:param tracks: True pour préparer des trajectoires, False pour préparer des localisations.
		:param dimension: Type de rendu demandé.
		:param source: Source utilisée pour calculer la couleur.
		:param color_scaling: Facteur appliqué à l'intensité de la couleur.
		:param upscale: Facteur d'agrandissement spatial.
		:param limits: Limites du rendu sous la forme ``(x_min, x_max, y_min, y_max)``.
		:return: Données éventuelles du renderer, dictionnaire des coordonnées vectorielles et pas uniforme sur Z.
		"""
		# Initialisation du dataframe.
		key = self.results.get_tracks_key() if tracks else self.results.get_localization_key()
		filtered = not tracks and key.startswith("f_")
		plot = {"plot_data": np.zeros((1, 1), dtype=float)}
		if filtered:
			plot["plot_filtered"] = np.empty((0, 3), dtype=float)
			df = self.results[key[2:]].copy()
			# La suppression des billes réinitialise les index : mémorise la sélection avant les transformations.
			df["_HR Retained"] = df.index.isin(self.results.localizations.index)
		else: df = self.results[key].copy()
		# Suppression des billes et correction du drift (modifie les index)
		if self.settings.hr["Remove Beads"].value: df = Drift.remove_beads(df, self.results.beads)
		df = self._correct_drift(df)
		if df.empty: return None, plot, 0.0

		# Ajout de la couleur.
		max_color = MAX_UI_16 if source == "Z" else 0
		if tracks: df = self._renderer.add_colors_to_tracks(df, source)
		elif filtered:
			# Les points exclus ne doivent pas changer la normalisation des couleurs du rendu conservé.
			retained = df["_HR Retained"]
			if not retained.any(): return None, plot, 0.0
			colored = self._renderer.add_colors_to_localizations(df.loc[retained].copy(), source, max_color)
			df["Color"] = 0.0
			df.loc[retained, "Color"] = colored["Color"].to_numpy()
		else: df = self._renderer.add_colors_to_localizations(df, source, max_color)
		df["Color"] *= color_scaling

		# Ajustement à la ROI
		x0, x1, y0, y1 = limits
		width, height = x1 - x0, y1 - y0
		df["X"] -= x0
		df["Y"] -= y0
		if not tracks: df = df[df["X"].between(0, width) & df["Y"].between(0, height)]

		retained = df.pop("_HR Retained").to_numpy(dtype=bool) if filtered else np.ones(len(df), dtype=bool)

		# Définition des éléments à récupérer.
		uniform_z_step = 0.0
		if tracks:  # .			-- Rendu de Trajectoires (2D et Track Stack). --
			viz_columns = ["Track", "Plane", "X", "Y", "Color"]
			plot_columns = ["Track", "Plane", "Y", "X"]
		elif dimension == 0:  # -- Rendu 2D. --
			viz_columns = ["X", "Y", "Color", "Sigma X", "Sigma Y", "Theta"]
			plot_columns = ["Y", "X"]
		else:  # .				-- Rendu 3D (Z Stack et 3D Rotation). --
			viz_columns = ["X", "Y", "Z", "Color", "Sigma X", "Sigma Y", "Theta"]
			plot_columns = ["Z", "Y", "X"]
			uniform_z_step = self._get_uniform_z_step()

		# Récupération des éléments.
		viz_data = (df.loc[retained, viz_columns] if filtered else df[viz_columns]).to_numpy(dtype=float)
		plot_data = df[plot_columns].to_numpy(dtype=float, copy=True)
		y_index, x_index = plot_columns.index("Y"), plot_columns.index("X")
		plot_data[:, [y_index, x_index]] *= upscale

		# Mise à jour pour l'affichage Napari.
		if tracks:
			# Le renderer conserve les extrémités extérieures, tandis que le calque Napari reste limité à l'image affichée.
			coords = np.round(plot_data[:, [y_index, x_index]])
			valid = (coords[:, 0] >= 0) & (coords[:, 0] <= height * upscale) & (coords[:, 1] >= 0) & (coords[:, 1] <= width * upscale)
			plot_data = plot_data[valid]
		elif dimension == 0:
			plot_data = np.column_stack((np.zeros(plot_data.shape[0], dtype=plot_data.dtype), plot_data))
		elif plot_data.shape[0] > 0:
			z_index = plot_columns.index("Z")
			z_step = self.settings.hr.hr_3d["Z Step"].value if dimension == 1 else 0
			z_step = z_step if z_step != 0 else uniform_z_step
			# Le Z Stack conserve l'origine des points retenus, même si un point exclu est plus bas.
			z_reference = plot_data[retained, z_index] if retained.any() else plot_data[:, z_index]
			z_origin = np.nanmin(z_reference)
			plot_data[:, z_index] = (plot_data[:, z_index] - z_origin) / z_step
			# Aligne le point vectoriel sur le plan choisi par le rendu ponctuel.
			if dimension == 1: plot_data[:, z_index] = np.floor(plot_data[:, z_index])

		if filtered: plot["plot_data"], plot["plot_filtered"] = plot_data[retained], plot_data[~retained]
		else: plot["plot_data"] = plot_data
		return viz_data, plot, uniform_z_step

	##################################################
	def _correct_drift(self, data: pd.DataFrame) -> pd.DataFrame:
		"""
		Vérifie si la correction de drift est activé, faisable et l'applique.

		:param data: Données à corriger.
		:return: Données corrigées.
		"""
		s = self.settings.hr
		if not s["Drift Correction"].value: return data
		beads = self.results.beads
		if beads.empty: return data
		# Application de la correction de drift
		drift = Drift.get_drift(beads, is_3d=False)
		if s["Smooth Drift"].value: drift[["X", "Y", "Z"]] = Drift.median_filter_centered(drift[["X", "Y", "Z"]].to_numpy())
		return Drift.remove_drift(data, drift, is_3d=False)

	##################################################
	def crop(self, img: np.ndarray, margin: int = 5) -> np.ndarray:
		"""
		Recadre automatiquement l'image (ou le volume) en supprimant les zones nulles autour, avec une marge configurable.

		:param img: Image à recadrer.
		:param margin: Nombre de pixels à conserver autour de la zone utile.
		:return: Image recadrée.
		"""
		if not self.settings.hr["Crop"].value: return img

		# --- Masque des pixels non nuls ---
		mask = img != 0
		is_rgb = img.ndim == 4 and img.shape[-1] == 3
		if is_rgb: mask = np.any(mask, axis=-1)  # Les canaux de couleur ne constituent pas un axe spatial.
		if not np.any(mask):
			shape = (1,) * mask.ndim + ((3,) if is_rgb else ())
			return np.zeros(shape, dtype=img.dtype)

		slices = []
		for axis in range(mask.ndim):
			# Projection sur tous les axes sauf l'axe courant
			proj_axes = tuple(i for i in range(mask.ndim) if i != axis)
			active = np.any(mask, axis=proj_axes)
			idx = np.where(active)[0]
			# Ajout marge (avec clamp pour ne pas dépasser les dimensions initiales)
			axis_min, axis_max = max(0, idx[0] - margin), min(img.shape[axis] - 1, idx[-1] + margin)
			slices.append(slice(axis_min, axis_max + 1))

		return img[tuple(slices)]

	##################################################
	def _get_uniform_z_step(self) -> float:
		"""
		Calcule le pas en nanomètre sur Z pour une échelle uniforme.

		:return: Pas sur Z identique au pas sur X et Y.
		"""
		pixel_size = self.settings.calibration["Pixel Size"].value * 1000  # Passage en Nanomètres
		upscale = self.settings.hr["Ratio"].value
		return pixel_size / upscale

	##################################################
	def _visualization_hr(self):
		"""Lance la creation d'une visualisation haute résolution à partir des paramètres passés en paramètres."""
		name = self.output_viz_name()
		viz = self.hr()["visualization"]
		self._logger.add(f"\tSaving high-resolution visualization.")
		if name.suffix == ".png": FileIO.save_png(self.crop(viz), name)  # Si extension png.
		else: FileIO.save_tif(self.crop(viz), name)  # .				   Si extension tif.
		return
