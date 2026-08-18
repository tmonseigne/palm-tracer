"""
Module contenant les fonctions de traitement de PALM.

.. todo:: Ajouter clairement un point dans la doc sur le systeme de filtre, l'enregistrement, le calcul sur l'intégralité des éléments
		  et filtre ensuite lors de la visualisation des graph et des sauvegarde si la case est coché...
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import cast, Optional

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from palm_tracer.Processing import Drift, Filtering, Gallery, Grapher, Palm, Parsing, Renderer
from palm_tracer.Processing.Step import prepare_step_action, Step, StepAction
from palm_tracer.Settings import Settings
from palm_tracer.Settings.Types import Combo
from palm_tracer.Tools import FileIO, Logger, Ui

MAX_UI_16 = np.iinfo(np.uint16).max
FILE_STATUS: list[str] = ["No", "Yes", "Yes (Filtered)",
						  "Yes (Reconnected)", "Yes (Reconnected and Filtered)",
						  "Yes (Corrected)", "Yes (Corrected and Filtered)"]


##################################################
@dataclass
class PALMTracer:
	"""Classe principale de PALM Tracer."""

	settings: Settings = field(init=False, default_factory=Settings)
	"""Classe principale des paramètres PALMTracer."""
	palm: Palm = field(init=False, default_factory=Palm)
	"""Interface vers la DLL C++ Palm."""
	_logger: Logger = field(init=False, default_factory=Logger)
	"""Journal d'activité."""
	filtering: Filtering = field(init=False)
	"""Outil de filtrage."""
	df: dict[str, pd.DataFrame] = field(init=False, default_factory=lambda: {
			"loc":   pd.DataFrame(), "dft": pd.DataFrame(), "bds": pd.DataFrame(), "trc": pd.DataFrame(), "blk": pd.DataFrame(),
			"MSD":   pd.DataFrame(), "InD": pd.DataFrame(), "Fit": pd.DataFrame(),
			"f_loc": pd.DataFrame(), "f_dft": pd.DataFrame(), "f_trc": pd.DataFrame(), "f_blk": pd.DataFrame(),
			"f_MSD": pd.DataFrame(), "f_InD": pd.DataFrame(), "f_Fit": pd.DataFrame()})
	"""Résultats des différents calculs."""

	_path: str = field(init=False, default="")
	"""Dossier de sortie pour le fichier en cours de traitement."""
	_stack: Optional[np.ndarray] = field(init=False, default=None)
	"""Pile en cours de traitement."""
	_timestamp: str = field(init=False, default="")
	"""Suffixe des fichiers pour un traitement (timestamp au format `YYYYMMDD_HHMMSS`)."""
	_timestamp_previous: str = field(init=False, default="")
	"""Suffixe des fichiers pour le traitement précédent (timestamp au format `YYYYMMDD_HHMMSS`)."""

	_grapher: Grapher = field(init=False, default_factory=Grapher)
	"""Générateur de graphique."""
	_renderer: Renderer = field(init=False, default_factory=Renderer)
	"""Générateur de rendu."""

	KEYS_TO_FILE: dict[str, str] = field(init=False, default_factory=lambda: {
			"loc": "localizations", "f_loc": "localizations_filtered",
			"dft": "localizations_corrected", "f_dft": "localizations_corrected_filtered", "bds": "beads",
			"trc": "tracking", "f_trc": "tracking_filtered",
			"blk": "tracking_reconnected", "f_blk": "tracking_reconnected_filtered",
			"MSD": "tracking_MSD", "f_MSD": "tracking_MSD_filtered",
			"InD": "tracking_InstantD", "f_InD": "tracking_InstantD_filtered",
			"Fit": "tracking_Fit", "f_Fit": "tracking_Fit_filtered"})
	"""Alias entre les noms de fichiers et les clés dans le dictionnaire de dataframes."""

	_STEPS: list[Step] = field(init=False)
	"""Listes des étapes du pipeline de traitement."""

	# ==================================================
	# region Initialization
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
				Step("tracks_compute", ["MSD", "InD", "Fit"], self._tracks_compute, self.filtering.tracks_compute),
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
	def reset_result(self):
		"""Vide entièrement les DataFrame de résultat dans `df`."""
		for key in self.df: self.df[key] = pd.DataFrame()

	# ==================================================
	# endregion Initialization
	# ==================================================

	# ==================================================
	# region Getter/Setter
	# ==================================================
	##################################################
	def get_localization_key(self) -> str:
		"""Clé des localisations (filtrées si le tableau est non vide) et corrigées si le tableau est non vide également."""
		if self.df["f_dft"].empty:
			if self.df["dft"].empty:
				if self.df["f_loc"].empty:
					return "loc"
				return "f_loc"
			return "dft"
		return "f_dft"

	##################################################
	def get_tracks_key(self) -> str:
		"""Clé des trajectoires (filtrées si le tableau est non vide) et reconnectées si le tableau est non vide également."""
		if self.df["f_blk"].empty:
			if self.df["blk"].empty:
				if self.df["f_trc"].empty:
					return "trc"
				return "f_trc"
			return "blk"
		return "f_blk"

	##################################################
	def get_tracks_compute_key(self) -> list[str]:
		"""Clé des calculs sur trajectoires (filtrées si le tableau est non vide)."""
		if self.df["f_MSD"].empty and self.df["f_InD"].empty and self.df["f_Fit"].empty:
			return ["MSD", "InD", "Fit"]
		return ["f_MSD", "f_InD", "f_Fit"]

	##################################################
	def get_status(self) -> dict[str, str]:
		"""
		Retourne un dictionnaire décrivant le statut des tableaux actuellement chargés dans ``self._df``
		pour les différentes catégories de données (Localisations, Trajectoires, MSD, Diffusion instantanée, Fit).

		Cette méthode analyse chaque tableau pour savoir s'il correspond :
			- à un tableau standard,
			- à un tableau filtré,
			- à un tableau reconnecté (pour les trajectoires),
			- à un tableau corrigé (pour les localisations),
			- ou à une absence de données.

		Les statuts retournés sont des chaînes de caractères provenant de la constante globale :data:`FILE_STATUS`.

		Le dictionnaire retourné contient systématiquement les clés suivantes :
		``Localization``, ``Beads``, ``Tracking``, ``MSD``, ``Instant D``, ``Fit``

		:return: Un dictionnaire ``{str: str}`` contenant le statut de chaque type de tableau.
		"""
		res = {"Localization": FILE_STATUS[0], "Tracking": FILE_STATUS[0], "MSD": FILE_STATUS[0], "Instant D": FILE_STATUS[0], "Fit": FILE_STATUS[0]}

		# --- Localisation ---
		if self.df["f_dft"].empty:
			if self.df["dft"].empty:
				if self.df["f_loc"].empty:
					if self.df["loc"].empty: res["Localization"] = FILE_STATUS[0]
					else: res["Localization"] = FILE_STATUS[1]
				else: res["Localization"] = FILE_STATUS[2]
			else: res["Localization"] = FILE_STATUS[5]
		else: res["Localization"] = FILE_STATUS[6]

		# --- Billes ---
		if self.df["bds"].empty: res["Beads"] = FILE_STATUS[0]
		else: res["Beads"] = FILE_STATUS[1]

		# --- Suivi ---
		if self.df["f_blk"].empty:
			if self.df["blk"].empty:
				if self.df["f_trc"].empty:
					if self.df["trc"].empty: res["Tracking"] = FILE_STATUS[0]
					else: res["Tracking"] = FILE_STATUS[1]
				else: res["Tracking"] = FILE_STATUS[2]
			else: res["Tracking"] = FILE_STATUS[3]
		else: res["Tracking"] = FILE_STATUS[4]

		# --- Calcul sur trajectoires ---
		tcs = [("MSD", "MSD"), ("InD", "Instant D"), ("Fit", "Fit")]
		for k1, k2 in tcs:
			if self.df[f"f_{k1}"].empty:
				if self.df[k1].empty: res[k2] = FILE_STATUS[0]
				else: res[k2] = FILE_STATUS[1]
			else: res[k2] = FILE_STATUS[2]
		return res

	##################################################
	@property
	def localizations(self) -> pd.DataFrame:
		"""Getter du :class:`DataFrame <pandas.DataFrame>` de la localisation (filtrée si elle est non vide)."""
		return self.df[self.get_localization_key()]

	##################################################
	@property
	def beads(self) -> pd.DataFrame:
		"""Getter du :class:`DataFrame <pandas.DataFrame>` des billes détectées."""
		return self.df["bds"]

	##################################################
	@property
	def tracks(self) -> pd.DataFrame:
		"""Getter du :class:`DataFrame <pandas.DataFrame>` du suivi (filtré s'il est non vide) et reconnecté s'il est non vide également."""
		return self.df[self.get_tracks_key()]

	##################################################
	@property
	def tracks_compute(self) -> dict[str, pd.DataFrame]:
		"""Getter du trio de :class:`DataFrame <pandas.DataFrame>` des calculs sur trajectoires (filtrées si le tableau est non vide)."""
		keys = self.get_tracks_compute_key()
		return {"MSD": self.df[keys[0]], "InD": self.df[keys[1]], "Fit": self.df[keys[2]]}

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
		"""Suffixe des fichiers pour un traitement (timestamp au format `YYYYMMDD_HHMMSS`)."""
		return self._timestamp

	##################################################
	def _output_name(self, name: str, ext: str = "csv", previous: bool = False) -> Path:
		"""
		Indique le nom du fichier à enregistrer CHEMIN / name-Timestamp.extension.

		:param name: Nomp du fichier.
		:param ext: Extension du fichier (par défaut csv, exception pour le log, les paramètres et les visualizations).
		:param previous: Si True, application du précédent timestamp. Sinon Timestamp Actuel.
		:return: Nom du fichier.
		"""
		return Path(self._path).resolve() / f"{name}-{self._timestamp_previous if previous else self._timestamp}.{ext}"

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
		else: suffix_dim, ext = "3D_rotation", "tif"
		suffix_type = "localizations" if typ == 0 else "tracks"
		name = f"visualization_{suffix_dim}_{suffix_type}{suffix_drift}_x{rat}_{src}"
		return self._output_name(name, ext=ext, previous=False)

	# ==================================================
	# endregion Getter/Setter
	# ==================================================

	# ==================================================
	# region Process
	# ==================================================
	##################################################
	def load(self, path: str = ""):
		"""Charge les précédents résultats du fichier courant."""
		if not self.is_dll_valid():
			Ui.print_warning("Process not completed due to missing DLLs.")
			return

		# --- Chargement des paramètres ---
		self._path = self.settings.batch.get_paths()[0] if path == "" else path  # Parsing du batch
		settings_filename = FileIO.get_last_file(self._path, "settings")
		self._timestamp = FileIO.extract_suffix(settings_filename)
		if not settings_filename or not self._timestamp:
			Ui.print_warning("No valid settings file to load.")
			return

		print(f"Loading setting file '{settings_filename}'.")
		with self.settings.signal_blocked():
			cfg = FileIO.open_json(settings_filename)
			self.settings.update_from_compact_dict(cfg)
			self.settings.localization["Preview"].value = False

		# --- Chargement des fichiers associés à ces paramètres. ---
		self.reset_result()  # Reset result Dataframes
		print(f"\tLoading files from the '{self._path}' folder with the timestamp {self._timestamp}.")
		for key, fname in self.KEYS_TO_FILE.items():
			f = self._output_name(fname)
			try:
				if Path(f).is_file():
					self.df[key] = pd.read_csv(f)  # Lecture du fichier CSV avec pandas
					print(f"\tFile '{fname}' loaded successfully.")
				else:
					self.df[key] = pd.DataFrame()
					print(f"\tFile '{fname}' not found.")
			except Exception as e:
				self.df[key] = pd.DataFrame()
				Ui.print_warning(f"\tError loading file '{fname}': {e}")

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
			# Reset result Dataframes
			self.reset_result()

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
		""" Sauvegarde le fichier méta (Création du DataFrame et sauvegarde en CSV si différent du précédent)."""
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

		:param step: Etape du pipeline.
		:param previous_settings: Paramètres du précédent pipeline.
		:param pipeline_dirty: État du pipeline (si True, Reuse est devenu impossible).
		"""
		group = getattr(self.settings, step.group_name)
		previous_group = getattr(previous_settings, step.group_name) if isinstance(previous_settings, Settings) else None

		action = prepare_step_action(group, previous_group, pipeline_dirty, step.allow_dirty)

		# --- Etape désactivée ---
		if action == StepAction.Skip:
			self._logger.add(f"{group.label} disabled.")
			return pipeline_dirty

		# --- Etape à récupérer du précédent pipeline ---
		if action == StepAction.Reuse:
			self._logger.add(f"{group.label} load previous result (Timestamp : {self._timestamp_previous}).")
			success = True
			for key in step.keys:
				old_file = self._output_name(self.KEYS_TO_FILE[key], previous=True)
				new_file = self._output_name(self.KEYS_TO_FILE[key])
				try:
					self.df[key] = pd.read_csv(old_file)
					self._logger.add(f"\tFile '{old_file.name}' loaded successfully, {len(self.df[key])} row(s) found.")
					old_file.rename(new_file)  # On renomme le fichier pour qu'à la prochaine étape, ce process soit celui du csv.
				except Exception as e:
					self._logger.add(f"\tError loading file '{old_file.name}': {e}")
					self.df[key] = pd.DataFrame()
					success = False

			if not success and group.active: action = StepAction.Compute

		# --- Etape à calculer ---
		if action == StepAction.Compute:
			self._logger.add(f"{group.label} enabled.")
			try: step.process_func()
			except Exception: raise
			pipeline_dirty = True  # Pipeline incohérent pour la suite, on évitera de réutiliser des éléments précédents, car un calcul a été fait

		# --- Filtrage ---
		if not step.apply_filter: return pipeline_dirty
		# Cas Standard Un seul dataframe
		if len(step.keys) == 1:
			f_key = f"f_{step.keys[0]}"
			self.df[f_key] = step.filter_func(self.df[step.keys[0]])
			n_init, n_end = len(self.df[step.keys[0]]), len(self.df[f_key])
			if n_init != n_end:
				self._logger.add(f"\t\tFiltering of file {n_end} row(s) instead of {n_init}: {n_init - n_end} deletion(s).")
				if self.settings.filters["Save"].value and n_end != 0:
					self._logger.add(f"\t\tSaving the filtered file.")
					self.df[f_key].to_csv(self._output_name(self.KEYS_TO_FILE[f_key]), index=False)
			else:
				self.df[f_key] = pd.DataFrame()
		# Cas spécial des tracks_compute qui modifient beaucoup de choses en même temps
		else:
			n_init = len(self.df["MSD"])
			o_name = self.get_tracks_key()
			if "f_" not in o_name: o_name = f"f_{o_name}"  # Si aucun filtre la clé sera sans le f_ devant
			self.df[o_name], self.df["f_MSD"], self.df["f_InD"], self.df["f_Fit"] \
				= step.filter_func(self.tracks, self.df["MSD"], self.df["InD"], self.df["Fit"])

			n_end = len(self.df["f_MSD"])
			if n_init != n_end:
				self._logger.add(f"\t\tFiltering of files {n_end} row(s) instead of {n_init}: {n_init - n_end} deletion(s)")
				if self.settings.filters["Save"].value:
					for key, name in [(o_name, "tracking"), ("f_MSD", "MSD"), ("f_InD", "Instant Diffusion"), ("f_Fit", "Fit")]:
						if not self.df[key].empty:
							self._logger.add(f"\t\tSaving the filtered {name} file.")
							self.df[key].to_csv(self._output_name(self.KEYS_TO_FILE[key]), index=False)
			else:
				for key in ["f_MSD", "f_InD", "f_Fit"]: self.df[key] = pd.DataFrame()

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
		self.df["loc"] = self.palm.localization(self._stack, s["Threshold"], s["Watershed"], fit, fit_params, planes)

		# Estimation du Z.
		if not self.df["loc"].empty and fit in (3, 4) and s["Gaussian Fit Z"]:
			model = self._get_astigmatism_model(Path(s["Gaussian Fit Model"]))

			if model.empty:
				self._logger.add("\tNo valid astigmatism model file for Z Estimation "
								 "(by default, file must be in output folder or in same folder as the stack).")
			else:
				z_max = s["Gaussian Fit Z max"]
				pixel_size = self.settings.calibration["Pixel Size"].value * 1000  # Passage en nanomètres
				points = self.df["loc"].loc[:, ["Sigma X", "Sigma Y"]].to_numpy(dtype=float, copy=True)
				estimated_z = self.palm.astigmatism_3d_estimation(points, pixel_size, model.to_numpy(), z_max)
				self.df["loc"][["Z", "MSE Z"]] = estimated_z

		self._logger.add(f"\tSaving the localization file ({len(self.df['loc'])} localization(s) found).")
		self.df["loc"].to_csv(self._output_name(self.KEYS_TO_FILE["loc"]), index=False)

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
		df = self.localizations  # Récupère automatiquement le "bon" dataframe (filtré ou non)
		if "Integrated Intensity" in df.columns: df = df[df["Integrated Intensity"] > 0]  # Suppression des éléments où l'ajustement a échoué.
		if df.empty:
			self._logger.add("\tNo localizations data calculated, no additional calculations can be performed.")
			return

		s = self.settings.beads.settings
		try: self.df["bds"] = Drift.extract_beads(df, s["Max Distance"], s["3D"], strict=False, k=2)
		except ValueError: self.df["bds"] = pd.DataFrame()
		if self.df["bds"].empty:
			self._logger.add("\tNo beads found.")
			return
		self._logger.add(f"\tSaving the beads file ({self.df['bds'].iloc[-1, 0]} beads(s) found).")
		self.df["bds"].to_csv(self._output_name(self.KEYS_TO_FILE["bds"]), index=False)

	##################################################
	def _tracking(self):
		"""Lance le suivi à partir des paramètres de l'interface."""
		df = self.localizations  # Récupère automatiquement le "bon" dataframe (filtré ou non)
		if "Integrated Intensity" in df.columns: df = df[df["Integrated Intensity"] > 0]  # Suppression des éléments où l'ajustement a échoué.
		if df.empty:
			self._logger.add("\tNo localizations data calculated, no additional calculations can be performed.")
			return

		s = self.settings.tracking.settings
		self.df["trc"] = self.palm.tracking(df, s["Max Distance"])

		self._logger.add(f"\tSaving the tracking file ({len(self.df['trc'])} point(s) found).")
		self.df["trc"].to_csv(self._output_name(self.KEYS_TO_FILE["trc"]), index=False)

	##################################################
	def _blinking_reconnection(self):
		"""Lance le tracking à partir des paramètres de l'interface."""
		df = self.df["trc"]  # Récupère le dataframe du suivi
		if df.empty:
			self._logger.add("\tNo tracking data calculated, no additional calculations can be performed.")
			return

		s = self.settings.blinking.settings
		self.df["blk"] = self.palm.blinking_reconnection(df, 1, s["Mode"], s["Max Duration"], s["Max Distance"])

		self._logger.add(f"\tSaving the reconnected tracking file ({len(self.df['blk'])} point(s) found).")
		self.df["blk"].to_csv(self._output_name(self.KEYS_TO_FILE["blk"]), index=False)

	##################################################
	def _tracks_compute(self):
		"""Lance les calculs sur les trajectoires à partir des paramètres de l'interface."""
		df = self.tracks  # Récupère automatiquement le "bon" dataframe (blinking et filtré ou non)
		if df.empty:
			self._logger.add("\tNo tracking data calculated, no additional calculations can be performed.")
			return

		# Parse settings
		sc = self.settings.calibration.settings
		s = self.settings.tracks_compute.settings

		if not s["MSD"] and not s["Instant Diffusion"] and s["Fit"] == 0:
			self._logger.add("\tNo metrics selected, no additional calculations can be performed.")
			return

		# Run command (pixel size doit rester en micromètre cette fois, car toutes les mesures seront en micromètres carré)
		res = self.palm.tracks_compute(df, s["MSD"], s["Instant Diffusion"], s["3D"], s["Log Scale"],
									   sc["Pixel Size"], sc["Exposure"], s["Fit"], np.array([s["Fit Length"]], dtype=np.float64))
		for key in res: self.df[key] = res[key]

		for key, name in [("MSD", "MSD"), ("InD", "Instant Diffusion"), ("Fit", "Fit")]:
			if s[name] and not res[key].empty:
				self._logger.add(f"\tSaving the {name} file.")
				res[key].to_csv(self._output_name(self.KEYS_TO_FILE[key]), index=False)

	# ==================================================
	# endregion Process
	# ==================================================

	# ==================================================
	# region Filtering
	# ==================================================
	##################################################
	def reset_filtered(self):
		"""Vide entièrement les DataFrames filtrés dans `df`."""
		with self.settings.signal_blocked(): self.settings.filters.reset()
		for key in self.df:
			if key.startswith("f_"): self.df[key] = pd.DataFrame()

	##################################################
	def update_filtered(self, last: bool = True):
		"""
		Recalcul les filtres sur le dernier dataframe disponible pour chacun si last est sélectionné, sinon sur l'original.

		:param last: Utilise les dernières versions des dataframes si `True`, sinon les données brutes seront utilisées.
		"""
		df = {}
		for key in ["loc", "dft", "trc", "blk", "MSD", "InD", "Fit"]:
			df[key] = self.df[key] if self.df[f"f_{key}"].empty or not last else self.df[f"f_{key}"]

		self.df["f_loc"] = self.filtering.localization(df["loc"])
		self.df["f_dft"] = self.filtering.localization(df["dft"])
		self.df["f_trc"] = self.filtering.tracking(df["trc"])
		self.df["f_blk"] = self.filtering.tracking(df["blk"])

		o_name = "f_trc" if self.df["f_blk"].empty else "f_blk"
		self.df[o_name], self.df["f_MSD"], self.df["f_InD"], self.df["f_Fit"] = self.filtering.tracks_compute(self.tracks, df["MSD"], df["InD"], df["Fit"])

		for key in ["loc", "dft", "trc", "blk"]:
			f_key = f"f_{key}"
			if len(self.df[key]) == len(self.df[f_key]): self.df[f_key] = pd.DataFrame()

		if self.settings.filters["Save"].value: self.save_filtered()

	##################################################
	def save_filtered(self):
		"""Enregistre tous les fichiers filtrés s'ils ne sont pas vides."""
		self._timestamp = FileIO.get_timestamp_for_files()
		for key, fname in self.KEYS_TO_FILE.items():
			# Il s'agit d'un filtre, il n'est pas vide et il a une taille différente de l'original
			if "f_" in key and not self.df[key].empty and len(self.df[key]) != len(self.df[key[2:]]):
				self.df[key].to_csv(self._output_name(fname), index=False)

	##################################################
	def connect_filters_button(self, ui_name: str = "default"):
		"""Connecte les boutons d'une interface de filtre."""
		filters = self.settings.filters
		filters.connect_button(self.reset_filtered, ui_name, "reset")
		filters.connect_button(self.update_filtered, ui_name, "update")
		filters.connect_button(self.save_filtered, ui_name, "save")

	# ==================================================
	# endregion Filtering
	# ==================================================

	# ==================================================
	# region Visualization
	# ==================================================
	##################################################
	def _gallery(self):
		"""Lance la génération d'une galerie à partir des paramètres passés en paramètres."""
		s = self.settings.gallery.settings
		if self.localizations.empty:
			self._logger.add(f"\tNo localization data for gallery generation.")
			return
		gallery = Gallery.make_gallery(self._stack, self.localizations, s["ROI Size"], s["ROIs Per Line"])
		self._logger.add(f"\tSaving gallery ({s}).")
		FileIO.save_tif(gallery, self._output_name(f"gallery_{s['ROI Size']}_{s['ROIs Per Line']}", "tif"))

	# ==================== Graph ====================
	##################################################
	def graph(self) -> go.Figure:
		"""Construit la figure Plotly courante en fonction du domaine et de la source."""
		s = self.settings.graph.settings
		src_id, dual = s["Type"], s["Dual"]
		src_a = cast(Combo, self.settings.graph["Source"]).current_text
		limit, sigma = s["Display Limits"], s["Display Sigma"]
		kde, gauss = s["Display KDE"], s["Display Gauss"]
		density, cumul = True, s["Display Cumul"]

		# Préparation des Données
		data, title = self._get_graph_data()
		# print(f"{data.shape}, {data.size}, {title}") with data.size over 10M make a warning message

		# Selection du graphique à afficher
		if src_id == 0 and src_a == "Localizations Count":
			return self._grapher.scatter(data, title, xlabel="Plane", ylabel="Count", limit=limit, show_sigma=sigma)
		if src_id == 1 and src_a == "Length Scatter":
			return self._grapher.scatter(data, title, xlabel="Track", ylabel="Length", limit=limit, show_sigma=sigma)
		if dual:
			src_b = cast(Combo, self.settings.graph["Source B"]).current_text
			return self._grapher.cloud(data, title, xlabel=src_a, ylabel=src_b, limit=limit, show_sigma=sigma, kde=kde, gaussian=gauss)
		return self._grapher.histogram(data, title, limit=limit, show_sigma=sigma, kde=kde, gaussian=gauss, density=density, cumulative=cumul)

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
	def _get_graph_data(self) -> tuple[np.ndarray, str]:
		"""
		Récupère et prépare les données pour l'affichage.

		:return:
		"""
		s = self.settings.graph.settings
		src_id, dual, log_scale = s["Type"], s["Dual"], s["Display Log Scale"]
		src_a = cast(Combo, self.settings.graph["Source"]).current_text

		d, t = self._get_graph_data_from_src(src_id, src_a, log_scale)
		if dual:
			src_b = cast(Combo, self.settings.graph["Source B"]).current_text
			t += f" / {src_b}"
			d_b, _ = self._get_graph_data_from_src(src_id, src_b, log_scale)
			if d.ndim == 2: d = d[:, 1]
			if d_b.ndim == 2: d_b = d_b[:, 1]
			if d_b.size != d.size: return np.empty(0), t
			d = np.column_stack((d, d_b))

		return d, t

	##################################################
	def _get_graph_data_from_src(self, src_id, src: str, log_scale: bool = False) -> tuple[np.ndarray, str]:
		"""Récupère et prépare les données pour l'affichage.

		:param src_id:
		:param src:
		:param log_scale:
		:return:
		"""
		# Localizations
		if src_id == 0:
			title = f"Localizations {src}"
			df = self.localizations
			if df.empty:  return np.empty(0), title
			if src == "Localizations Count":
				s = df["Plane"].astype(np.int64)
				planes = np.arange(int(s.min()), int(s.max()) + 1, dtype=int)  # Récupération des plans du min au max (si plans vides, ils seront compris)
				counts = (s.groupby(s).size().reindex(pd.Index(planes), fill_value=0).to_numpy(dtype=int))  # Comptage par groupe
				return np.column_stack((planes, counts)), src

			s = df.get(src)  # None si la colonne n'existe pas
			if s is None: return np.empty(0), title
			return self._log_data(s.to_numpy(dtype=float), log_scale), title

		# Tracks
		title = f"Tracks {src}"
		if "Length" in src:  # Cas particulier, il est peut-être dans le tableau Fit, mais on va utiliser le tableau Tracks initial.
			df = self.tracks
			if df.empty: return np.empty(0), title

			tracks_planes = df.groupby("Track", sort=False)["Plane"]

			if src in {"Length Scatter", "Length"}:
				group = tracks_planes.agg(["min", "max"])
				res = (group["max"] - group["min"] + 1).to_numpy()

				if src == "Length Scatter": return np.column_stack((group.index.to_numpy(), res)), title
				return res, title

			lengths: list[int] = []

			for _, planes in tracks_planes:
				planes_array = np.sort(planes.dropna().unique())
				if planes_array.size == 0: continue  # pragma: no cover — Techniqement impossible Plane est toujours valide

				diffs = np.diff(planes_array)
				breaks = np.flatnonzero(diffs > 1)

				if src == "Length On":  # Récupère la longueur des segments continus des trajectoires.
					segments = np.concatenate(([-1], breaks, [planes_array.size - 1],))
					lengths.extend(np.diff(segments).tolist())

				elif src == "Length Off":
					lengths.extend((diffs[breaks]).tolist())  # Récupère la longueur des blancs dans les trajectoires.

			return np.asarray(lengths, dtype=np.int64), title

		df = self.tracks_compute
		if src == "MSD":
			df = df["MSD"]
			if df.empty: return np.empty(0), title
			step = self.settings.graph["MSD Step"].value  # .										Récupération du numéro du Step.
			col = f"Step {step}"  # .																Récupération du nom de la colonne.
			title += f" {col}"
			if not {"Track", col}.issubset(df.columns): return np.empty(0), title  # .				Vérification de présence des colonnes
			track, values = df["Track"].astype(int).to_numpy(), df[col].astype(float).to_numpy()  # Séparation track et valeur
			df = np.column_stack((track, self._log_data(values, log_scale)))  # .					Application du log sur les valeurs
			return df[np.isfinite(df).all(axis=1)], title  # .										Retour avec filtrage des Lignes NaN

		if src == "Instant D":
			df = df["InD"].drop(columns=["Track"], errors="ignore").to_numpy().ravel()  # .			Récupération des colonnes
			if df.size == 0: return np.empty(0), title
			df = self._log_data(df, log_scale)  # .													Application du log sur les valeurs
			return df[np.isfinite(df)], title  # .													Retour avec filtrage des Lignes NaN

		df = df["Fit"]
		if df.empty: return np.empty(0), title
		if not {"Track", src}.issubset(df.columns): return np.empty(0), title  # .					Vérification de présence des colonnes
		track, values = df["Track"].astype(int).to_numpy(), df[src].astype(float).to_numpy()  # .	Séparation track et valeur
		df = np.column_stack((track, self._log_data(values, log_scale)))  # .						Application du log sur les valeurs
		return df[np.isfinite(df).all(axis=1)], title  # .											Retour avec filtrage des Lignes NaN

	##################################################
	def _visualization_graph(self):
		"""Lance la creation d'une visualisation graphique à partir des paramètres."""
		s = self.settings.graph.settings
		name = f"graph_{self.settings.graph['Type'].value}_{cast(Combo, self.settings.graph['Source']).current_text}"
		self.graph().write_html(self._output_name(name, ext=".html"))
		self._logger.add(f"\tSaving Graph ({s}).")

	# ==================== HR ====================
	##################################################
	def hr(self) -> tuple[np.ndarray, np.ndarray]:
		"""Génère une représentation en Haute Résolution des données."""
		viz, plot_data = np.zeros((1, 1), dtype=np.uint16), np.zeros((1, 1), dtype=np.float64)
		if self._stack is None: return viz, plot_data

		# --- Paramètres ---
		s = self.settings.hr
		src = cast(Combo, s["Source"]).current_text
		upscale = s["Ratio"].value
		x0, x1, y0, y1 = self.settings.rois.get_roi_limits()
		n_w, n_h = x1 - x0, y1 - y0
		self._renderer.set_size(n_w, n_h, upscale)

		# --- Localisations ---
		if s["Type"].value == 0:
			df = self.localizations.copy()
			if s["Remove Beads"].value: df = Drift.remove_beads(df, self.beads)
			df = self._correct_drift(df)
			if df.empty: return viz, plot_data
			df = self._renderer.add_colors_to_localizations(df, src)
			gaussian = s.gaussian.settings if s.gaussian.active else None
			color_mode = 0 if src == "Count" else s["Color mode"].value  # Si count, on est forcément en mode cumulatif, sinon on voit l'option.
			df["X"] -= x0  # Ajustement à la ROI sur X
			df["Y"] -= y0  # Ajustement à la ROI sur Y
			df = df[df["X"].between(0, n_w) & df["Y"].between(0, n_h)]  # Sélection dans les bornes

			if s["Dimension"].value == 0:  # .	 2D
				viz_data = df[["X", "Y", "Color", "Sigma X", "Sigma Y", "Theta"]].to_numpy(dtype=np.float64)  # Récupération
				plot_data = df[["Y", "X"]].to_numpy() * upscale  # Mise à l'échelle des X et Y.
				plot_data = np.column_stack((np.zeros((plot_data.shape[0], 1), dtype=plot_data.dtype), plot_data))
				viz = self._renderer.localizations(viz_data, color_mode, gaussian)  # Rendu
			else:  # . 							 3D
				viz_data = df[["X", "Y", "Z", "Color", "Sigma X", "Sigma Y", "Theta"]].to_numpy(dtype=np.float64)  # Récupération
				uniform_z_step = self._get_uniform_z_step()
				plot_data = df[["Z", "Y", "X"]].to_numpy(copy=True)
				z_min = np.nanmin(plot_data[:, 0])
				# On n'a pas besoin de les caster en entier, Napari n'est pas trop bête et si l'utilisateur passe en vue 3D, il aura les Z flottants.
				plot_data[:, 0] = (plot_data[:, 0] - z_min) / uniform_z_step
				plot_data[:, 1:] *= upscale  # Mise à l'échelle des X et Y.
				if s["Dimension"].value == 1:  # Z Stack
					z_step = s.hr_3d["Z Step"].value
					viz = self._renderer.z_stack(viz_data, color_mode, z_step if z_step != 0 else uniform_z_step, gaussian)  # Rendu
				else:  # .						   3D Rotation
					frames = s.hr_3d["Frames"].value
					axis = s.hr_3d["Axis"].value
					viz = self._renderer.rotation_3d(viz_data, color_mode, uniform_z_step, frames, axis, gaussian)  # Rendu

			return viz, plot_data

		# --- Tracks ---
		df = self._correct_drift(self.tracks.copy())
		if df.empty: return viz, plot_data
		df = self._renderer.add_colors_to_tracks(df, src)
		df["X"] -= x0  # Ajustement à la ROI sur X
		df["Y"] -= y0  # Ajustement à la ROI sur Y
		df = df[df["X"].between(0, n_w) & df["Y"].between(0, n_h)]  # Sélection dans les bornes
		df = df[["Track", "Plane", "X", "Y", "Color"]].to_numpy(dtype=np.float64)
		viz_data = df[:, [0, 2, 3, 4]]
		plot_data = df[:, [0, 1, 3, 2]]
		plot_data[:, [2, 3]] *= upscale
		viz = self._renderer.tracks(viz_data)
		return viz, plot_data

	##################################################
	def _correct_drift(self, data: pd.DataFrame) -> pd.DataFrame:
		"""
		Vérifie si la correction de drift est activé, faisable et l'applique.

		:param data: Données à corriger.
		:return: Données corrigées.
		"""
		s = self.settings.hr
		if not s["Drift Correction"].value: return data
		beads = self.beads
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
		if not np.any(mask): return np.zeros(tuple(1 for _ in range(img.ndim)), dtype=img.dtype)  # Si tout est noir

		slices = []
		for axis in range(img.ndim):
			# Projection sur tous les axes sauf l'axe courant
			proj_axes = tuple(i for i in range(img.ndim) if i != axis)
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
		viz, _ = self.hr()
		self._logger.add(f"\tSaving high-resolution visualization.")
		if name.suffix == ".png": FileIO.save_png(self.crop(viz), name)  # Si extension png.
		else: FileIO.save_tif(self.crop(viz), name)  # .				   Si extension tif.
		return
