"""Gère les résultats des traitements et leurs représentations Qt."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

import pandas as pd

from palm_tracer.Tools import FileIO, Ui

if TYPE_CHECKING:
	from palm_tracer.UI.ResultsUI import ResultsUI  # Import conditionnel pour éviter une dépendance cyclique à l'exécution.


##################################################
@dataclass
class Results:
	"""Conserve les résultats des traitements et leurs représentations Qt."""

	_data: dict[str, pd.DataFrame] = field(init=False, default_factory=lambda: {
			"loc":   pd.DataFrame(), "dft": pd.DataFrame(), "bds": pd.DataFrame(),  # .	   Localisations.
			"trc":   pd.DataFrame(), "blk": pd.DataFrame(),  # .						   Trajectoires.
			"MSD":   pd.DataFrame(), "InD": pd.DataFrame(), "Fit": pd.DataFrame(),  # .	   Analyses des trajectoires.
			"f_loc": pd.DataFrame(), "f_dft": pd.DataFrame(),  # .						   Localisations filtrées.
			"f_trc": pd.DataFrame(), "f_blk": pd.DataFrame(),  # .						   Trajectoires filtrées.
			"f_MSD": pd.DataFrame(), "f_InD": pd.DataFrame(), "f_Fit": pd.DataFrame()})  # Analyses des trajectoires filtrées.
	"""Résultats des différents calculs."""

	_uis: dict[str, "ResultsUI"] = field(init=False, default_factory=dict)
	"""Interfaces d'information."""

	_stack_name: str = field(init=False, default="")
	"""Nom du fichier en cours d'analyse, sans dossiers ni extension."""
	_stack_path: Path | None = field(init=False, default=None)
	"""Chemin du fichier en cours d'analyse, conservé pour l'infobulle."""
	_results_folder: Path | None = field(init=False, default=None)
	"""Dossier associé aux résultats courants, ou aucun dossier avant leur sélection."""

	KEYS_TO_FILE: dict[str, str] = field(init=False, default_factory=lambda: {
			"loc": "localizations", "f_loc": "localizations_filtered",
			"dft": "localizations_corrected", "f_dft": "localizations_corrected_filtered",
			"bds": "beads",
			"trc": "tracking", "f_trc": "tracking_filtered",
			"blk": "tracking_reconnected", "f_blk": "tracking_reconnected_filtered",
			"MSD": "tracking_MSD", "f_MSD": "tracking_MSD_filtered",
			"InD": "tracking_InstantD", "f_InD": "tracking_InstantD_filtered",
			"Fit": "tracking_Fit", "f_Fit": "tracking_Fit_filtered"})
	"""Alias entre les noms de fichiers et les clés dans le dictionnaire de DataFrames."""

	# ==================================================
	# region Initialisation
	# ==================================================
	##################################################
	@staticmethod
	def output_name(name: str, path: str | Path, timestamp: str, ext: str = "csv") -> Path:
		"""
		Construit le chemin d'un fichier de résultat sous la forme ``path / name-timestamp.ext``.

		:param name: Nom du fichier.
		:param path: Chemin du dossier.
		:param timestamp: Suffixe des fichiers pour un traitement (timestamp au format ``YYYYMMDD_HHMMSS``).
		:param ext: Extension du fichier ; valeur par défaut : ``csv``.
		:return: Chemin complet vers le fichier.
		"""
		return Path(path).resolve() / f"{name}-{timestamp}.{ext}"

	##################################################
	def output_name_by_key(self, key: str, path: str | Path, timestamp: str, ext: str = "csv") -> Path:
		"""
		Construit le chemin d'un fichier de résultat à partir de sa clé.

		:param key: Clé du fichier.
		:param path: Chemin du dossier.
		:param timestamp: Suffixe des fichiers pour un traitement (timestamp au format ``YYYYMMDD_HHMMSS``).
		:param ext: Extension du fichier ; valeur par défaut : ``csv``.
		:return: Chemin complet vers le fichier.
		"""
		return self.output_name(self.KEYS_TO_FILE[key], path, timestamp, ext)

	##################################################
	def load(self, stack_name: str, path: str | Path, timestamp: str):
		"""
		Charge les résultats précédemment enregistrés pour une pile et un traitement.

		:param stack_name: Nom de la pile en cours d'analyse.
		:param path: Dossier contenant les fichiers de résultats.
		:param timestamp: Suffixe identifiant le traitement à charger.
		"""
		self.reset()  # Réinitialise les DataFrames de résultats.
		self.stack_name = stack_name
		folder = Path(path).resolve()
		self.results_folder = folder
		print(f"\tLoading files from the '{str(folder)}' folder with the timestamp {timestamp}.")

		for key, filename in self.KEYS_TO_FILE.items():
			file = self.output_name(filename, folder, timestamp)

			if not file.is_file():  # .		  Fichier inexistant.
				print(f"\tFile '{filename}' not found.")
				continue

			try: data = pd.read_csv(file)  # . Lecture du fichier CSV avec pandas.
			except Exception as exception:  # Échec lors de la lecture.
				Ui.print_warning(f"\tError loading file '{filename}': {exception}")
				continue

			self._data[key] = data
			print(f"\tFile '{filename}' loaded successfully.")

		self.update_uis()

	##################################################
	def reset(self):
		"""Vide entièrement les DataFrames de résultats."""
		for key in self._data: self._data[key] = pd.DataFrame()
		self.update_uis()

	##################################################
	def reset_filtered(self):
		"""Vide entièrement les DataFrames de résultats filtrés."""
		for key in self._data:
			if key.startswith("f_"): self._data[key] = pd.DataFrame()
		self.update_uis()

	# ==================================================
	# endregion Initialisation
	# ==================================================

	# ==================================================
	# region Accesseurs
	# ==================================================
	##################################################
	def __getitem__(self, key: str) -> pd.DataFrame:
		"""Retourne le DataFrame associé à la clé indiquée."""
		return self._data[key]

	##################################################
	def __setitem__(self, key: str, value: pd.DataFrame):
		"""
		Remplace le DataFrame associé à une clé.

		:param key: Clé du résultat à remplacer.
		:param value: Nouveau DataFrame.
		"""
		self._data[key] = value
		self.update_uis()

	##################################################
	def __iter__(self):
		"""Retourne un itérateur sur les clés des résultats."""
		return iter(self._data)

	##################################################
	def _get_active_key(self, keys: tuple[str, ...]) -> str:
		"""
		Retourne la dernière clé associée à un résultat non vide, ou la première clé par défaut.

		:param keys: Clés classées par priorité croissante.
		:return: Clé du résultat actif.
		"""
		return next((key for key in reversed(keys) if not self._data[key].empty), keys[0], )

	##################################################
	@property
	def stack_name(self) -> str:
		"""Nom du fichier en cours d'analyse, sans dossiers ni extension."""
		return self._stack_name

	##################################################
	@stack_name.setter
	def stack_name(self, stack_name: str):
		"""
		Normalise le nom affiché et conserve le chemin complet pour l'infobulle.

		Le dossier des résultats est dissocié lorsque le chemin du fichier change,
		même si les deux fichiers portent le même nom dans des dossiers différents.

		:param stack_name: Nom ou chemin du fichier ; une chaîne vide supprime le fichier courant.
		"""
		path = Path(stack_name) if stack_name else None
		if path != self._stack_path or path is None: self._results_folder = None
		self._stack_path = path
		self._stack_name = path.stem if path is not None else ""
		self.update_uis()

	##################################################
	@property
	def results_folder(self) -> Path | None:
		"""Dossier absolu des résultats courants, ou :obj:`None` si aucun dossier n'est associé."""
		return self._results_folder

	##################################################
	@results_folder.setter
	def results_folder(self, path: str | Path | None):
		"""Mémorise le dossier des résultats et actualise les boutons de toutes les vues."""
		self._results_folder = Path(path).resolve() if path is not None else None
		self.update_uis()

	##################################################
	def get_localization_key(self) -> str:
		"""Clé des localisations actives, en privilégiant les variantes filtrées et corrigées."""
		return self._get_active_key(("loc", "f_loc", "dft", "f_dft"))

	##################################################
	def get_tracks_key(self) -> str:
		"""Clé des trajectoires actives, en privilégiant les variantes filtrées et reconnectées."""
		return self._get_active_key(("trc", "f_trc", "blk", "f_blk"))

	##################################################
	def get_track_analysis_key(self) -> list[str]:
		"""Clés des analyses des trajectoires, en privilégiant leurs variantes filtrées."""
		return [self._get_active_key(("MSD", "f_MSD")), self._get_active_key(("InD", "f_InD")), self._get_active_key(("Fit", "f_Fit"))]

	##################################################
	@property
	def localizations(self) -> pd.DataFrame:
		"""Localisations actives (:class:`~pandas.DataFrame`)."""
		return self._data[self.get_localization_key()]

	##################################################
	@property
	def beads(self) -> pd.DataFrame:
		"""Billes détectées (:class:`~pandas.DataFrame`)."""
		return self._data["bds"]

	##################################################
	@property
	def tracks(self) -> pd.DataFrame:
		"""Trajectoires actives (:class:`~pandas.DataFrame`), éventuellement filtrées et reconnectées."""
		return self._data[self.get_tracks_key()]

	##################################################
	@property
	def track_analysis(self) -> dict[str, pd.DataFrame]:
		"""Analyses actives des trajectoires, éventuellement filtrés (:class:`~pandas.DataFrame`)."""
		keys = self.get_track_analysis_key()
		return {"MSD": self._data[keys[0]], "InD": self._data[keys[1]], "Fit": self._data[keys[2]]}

	##################################################
	def get_status(self) -> dict[str, str]:
		"""
		Construit les statuts des différentes catégories de résultats actuellement chargées.

		:return: Statuts indexés par catégorie de résultat.
		"""
		res = {"File":               self.stack_name if self._stack_name else "No File",
			   "Localizations":      self.get_df_status(self._data["loc"], self._data["f_loc"], "localizations"),
			   "Beads":              self.get_df_status(self._data["bds"], self._data["bds"], "localizations"),
			   "Tracks":             self.get_df_status(self._data["trc"], self._data["f_trc"], "tracks"),
			   "Tracks Reconnected": self.get_df_status(self._data["blk"], self._data["f_blk"], "tracks"),
			   "MSD":                self.get_df_status(self._data["MSD"], self._data["f_MSD"], "tracks"),
			   "Instant D":          self.get_df_status(self._data["InD"], self._data["f_InD"], "tracks"),
			   "MSD Fit":            self.get_df_status(self._data["Fit"], self._data["f_Fit"], "tracks")}

		return res

	##################################################
	@staticmethod
	def get_df_status(original: pd.DataFrame, filtered: pd.DataFrame, name: str, pre: str = "") -> str:
		"""
		Construit le statut d'un résultat à partir de ses versions initiale et filtrée.

		En présence d'une colonne ``Track``, les identifiants de trajectoire distincts et non nuls sont comptés ;
		sinon, le nombre de lignes est utilisé.

		:param original: DataFrame initial.
		:param filtered: DataFrame filtré.
		:param name: Nom du type de données, par exemple ``localizations`` ou ``tracks``.
		:param pre: Qualificatif ajouté au statut, par exemple ``Reconnected``.
		:return: Statut accompagné du nombre d'éléments avant et, si nécessaire, après filtrage.
		"""
		n_init = original["Track"].nunique() if "Track" in original.columns else len(original)
		n_filt = filtered["Track"].nunique() if "Track" in filtered.columns else len(filtered)
		yes = f"Yes {pre}" if pre else "Yes"

		if n_init == 0: return "No"
		if n_filt == 0 or n_filt == n_init: return f"{yes} ({n_init} {name})"
		else: return f"{yes} Filtered ({n_filt}/{n_init} {name})"

	# ==================================================
	# region Entrées-sorties
	# ==================================================
	##################################################
	def save(self, key: str, path: str | Path, timestamp: str):
		"""
		Enregistre un résultat dans un fichier CSV.

		:param key: Clé du résultat à enregistrer.
		:param path: Dossier de destination.
		:param timestamp: Suffixe identifiant le traitement.
		"""
		filename = self.output_name(self.KEYS_TO_FILE[key], path, timestamp)
		self._data[key].to_csv(filename, index=False)
		self.results_folder = filename.parent

	##################################################
	def save_filtered(self, path: str | Path, timestamp: str = ""):
		"""
		Enregistre tous les résultats filtrés non vides et différents de leur version initiale.

		:param path: Dossier de destination.
		:param timestamp: Suffixe identifiant le traitement ; généré automatiquement lorsqu'il est vide.
		"""
		timestamp = FileIO.get_timestamp_for_files() if not timestamp else timestamp
		for key, fname in self.KEYS_TO_FILE.items():
			# Il s'agit d'un filtre, il n'est pas vide et il a une taille différente de l'original
			if "f_" in key and not self._data[key].empty and len(self._data[key]) != len(self._data[key[2:]]):
				self.save(key, path, timestamp)

	# ==================================================
	# endregion Entrées-sorties
	# ==================================================

	# ==================================================
	# region Interface
	# ==================================================
	##################################################
	def _open_results_folder(self):
		"""Ouvre le dossier courant dans l'explorateur du système lorsqu'il existe."""
		from qtpy.QtCore import QUrl
		from qtpy.QtGui import QDesktopServices

		if self._results_folder is not None and self._results_folder.is_dir():
			QDesktopServices.openUrl(QUrl.fromLocalFile(str(self._results_folder)))

	##################################################
	def _clear_result(self, keys: tuple[str, ...]):
		"""
		Vide les variantes d'une catégorie de résultats et actualise toutes les vues.

		Les autres catégories et le nom de la pile sont conservés.

		:param keys: Clés des DataFrames de la catégorie à vider.
		"""
		for key in keys: self._data[key] = pd.DataFrame()
		self.update_uis()

	##################################################
	def get_ui(self, name: str = "default", margin: int = 5) -> "ResultsUI":
		"""
		Retourne une représentation Qt des résultats, existante ou nouvellement créée.

		:param name: Nom identifiant la représentation.
		:param margin: Marges internes de la représentation, en pixels.
		:return: Représentation Qt synchronisée avec les résultats.
		"""
		if name in self._uis: return self._uis[name]

		from palm_tracer.UI.ResultsUI import ResultsUI  # Import différé pour éviter une dépendance cyclique.

		ui = ResultsUI(margin=margin)
		ui._open_folder_button.clicked.connect(self._open_results_folder)
		categories = {
				"Localizations":      ("loc", "f_loc", "dft", "f_dft"),
				"Beads":              ("bds",),
				"Tracks":             ("trc", "f_trc"),
				"Tracks Reconnected": ("blk", "f_blk"),
				"MSD":                ("MSD", "f_MSD"),
				"Instant D":          ("InD", "f_InD"),
				"MSD Fit":            ("Fit", "f_Fit"),
				}
		for category, keys in categories.items():
			ui._clear_buttons[category].clicked.connect(lambda checked=False, result_keys=keys: self._clear_result(result_keys))
		ui.update_status(self.get_status())
		ui._labels["File"].setToolTip(str(self._stack_path) if self._stack_path is not None else "")
		ui.update_results_folder(self._results_folder)
		self._uis[name] = ui
		return ui

	##################################################
	def clean_ui(self, name: str = "default"):
		"""
		Supprime l'interface Qt associée au nom donné.

		:param name: Nom de l'interface dans le dictionnaire.
		"""
		self._uis.pop(name, None)

	##################################################
	def update_uis(self):
		"""Actualise toutes les représentations Qt associées aux résultats."""
		status = self.get_status()
		for ui in self._uis.values():
			ui.update_status(status)
			ui._labels["File"].setToolTip(str(self._stack_path) if self._stack_path is not None else "")
			ui.update_results_folder(self._results_folder)
