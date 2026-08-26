"""blabla"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

import pandas as pd

from palm_tracer.Tools import FileIO, Ui

if TYPE_CHECKING:
	from palm_tracer.UI.ResultsUI import ResultsUI  # Hack pour éviter les imports cycliques


##################################################
@dataclass
class Results:
	"""Conserve les résultats des traitements et leurs représentations Qt."""

	_data: dict[str, pd.DataFrame] = field(init=False, default_factory=lambda: {
			"loc":   pd.DataFrame(), "dft": pd.DataFrame(), "bds": pd.DataFrame(),  # .	   Localisations.
			"trc":   pd.DataFrame(), "blk": pd.DataFrame(),  # .						   Trajectoires.
			"MSD":   pd.DataFrame(), "InD": pd.DataFrame(), "Fit": pd.DataFrame(),  # .	   Calculs sur les Trajectoires.
			"f_loc": pd.DataFrame(), "f_dft": pd.DataFrame(),  # .						   Localisations Filtrées.
			"f_trc": pd.DataFrame(), "f_blk": pd.DataFrame(),  # .						   Trajectoires Filtrées.
			"f_MSD": pd.DataFrame(), "f_InD": pd.DataFrame(), "f_Fit": pd.DataFrame()})  # Calculs sur Trajectoires filtrées.
	"""Résultats des différents calculs."""

	_uis: dict[str, "ResultsUI"] = field(init=False, default_factory=dict)
	"""Interfaces d'information."""

	_stack_name: str = field(init=False, default="")
	"""Nom du fichier en cours d'analyse."""

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
		Indique le nom du fichier à enregistrer ``folder / name-timestamp.extension``.

		:param name: Nom du fichier.
		:param path: Chemin du dossier.
		:param timestamp: Suffixe des fichiers pour un traitement (timestamp au format ``YYYYMMDD_HHMMSS``).
		:param ext: Extension du fichier (par défaut csv, exception pour le log, les paramètres et les visualizations).
		:return: Chemin complet vers le fichier.
		"""
		return Path(path).resolve() / f"{name}-{timestamp}.{ext}"

	##################################################
	def output_name_by_key(self, key: str, path: str | Path, timestamp: str, ext: str = "csv") -> Path:
		"""
		Indique le nom du fichier à enregistrer ``folder / name-timestamp.extension``.

		:param key: Clé du fichier.
		:param path: Chemin du dossier.
		:param timestamp: Suffixe des fichiers pour un traitement (timestamp au format ``YYYYMMDD_HHMMSS``).
		:param ext: Extension du fichier (par défaut csv, exception pour le log, les paramètres et les visualizations).
		:return: Chemin complet vers le fichier.
		"""
		return self.output_name(self.KEYS_TO_FILE[key], path, timestamp, ext)

	##################################################
	def load(self, stack_name: str, path: str | Path, timestamp: str):
		"""Charge les précédents résultats du chemin et timestamp en parametre."""
		self.reset()  # Réinitialisation des DataFrames de résultats
		self.stack_name = stack_name
		folder = Path(path).resolve()
		print(f"\tLoading files from the '{str(folder)}' folder with the timestamp {timestamp}.")

		for key, filename in self.KEYS_TO_FILE.items():
			file = self.output_name(filename, folder, timestamp)

			if not file.is_file():  # .		  Fichier inexistant
				print(f"\tFile '{filename}' not found.")
				continue

			try: data = pd.read_csv(file)  # .Lecture du fichier CSV avec pandas.
			except Exception as exception:  # Echec lors de la lecture
				Ui.print_warning(f"\tError loading file '{filename}': {exception}")
				continue

			self._data[key] = data
			print(f"\tFile '{filename}' loaded successfully.")

		self.update_uis()

	##################################################
	def reset(self):
		"""Vide entièrement les DataFrame de résultat."""
		for key in self._data: self._data[key] = pd.DataFrame()
		self.update_uis()

	##################################################
	def reset_filtered(self):
		"""Vide entièrement les DataFrames de résultat filtrés."""
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
	def __getitem__(self, key: str) -> pd.DataFrame: return self._data[key]

	##################################################
	def __setitem__(self, key: str, value: pd.DataFrame):
		self._data[key] = value
		self.update_uis()

	##################################################
	def __iter__(self): return iter(self._data)

	##################################################
	def _get_active_key(self, keys: tuple[str, ...]) -> str:
		"""

		:param keys:
		:return:
		"""
		return next((key for key in reversed(keys) if not self._data[key].empty), keys[0], )

	##################################################
	@property
	def stack_name(self) -> str:
		"""Nom du fichier en cours d'analyse (:class:`str`)."""
		return self._stack_name

	##################################################
	@stack_name.setter
	def stack_name(self, stack_name: str):
		"""Met à jour le nom du fichier en cours d'analyse ainsi que l'affichage des widgets."""
		self._stack_name = stack_name
		self.update_uis()

	##################################################
	def get_localization_key(self) -> str:
		"""Clé des localisations (filtrées si le tableau est non vide) et corrigées si le tableau est non vide également."""
		return self._get_active_key(("loc", "f_loc", "dft", "f_dft"))

	##################################################
	def get_tracks_key(self) -> str:
		"""Clé des localisations (filtrées si le tableau est non vide) et corrigées si le tableau est non vide également."""
		return self._get_active_key(("trc", "f_trc", "blk", "f_blk"))

	##################################################
	def get_tracks_compute_key(self) -> list[str]:
		"""Clé des calculs sur trajectoires (filtrées si le tableau est non vide)."""
		return [self._get_active_key(("MSD", "f_MSD")), self._get_active_key(("InD", "f_InD")), self._get_active_key(("Fit", "f_Fit"))]

	##################################################
	@property
	def localizations(self) -> pd.DataFrame:
		"""Getter du :class:`DataFrame <pandas.DataFrame>` de la localisation (filtrée si elle est non vide)."""
		return self._data[self.get_localization_key()]

	##################################################
	@property
	def beads(self) -> pd.DataFrame:
		"""Getter du :class:`DataFrame <pandas.DataFrame>` des billes détectées."""
		return self._data["bds"]

	##################################################
	@property
	def tracks(self) -> pd.DataFrame:
		"""Getter du :class:`DataFrame <pandas.DataFrame>` du suivi (filtré s'il est non vide) et reconnecté s'il est non vide également."""
		return self._data[self.get_tracks_key()]

	##################################################
	@property
	def tracks_compute(self) -> dict[str, pd.DataFrame]:
		"""Getter du trio de :class:`DataFrame <pandas.DataFrame>` des calculs sur trajectoires (filtrées si le tableau est non vide)."""
		keys = self.get_tracks_compute_key()
		return {"MSD": self._data[keys[0]], "InD": self._data[keys[1]], "Fit": self._data[keys[2]]}

	##################################################
	def get_status(self) -> dict[str, str]:
		"""
		Retourne un dictionnaire décrivant le statut des tableaux actuellement chargés dans ``_df``
		pour les différentes catégories de données (Localisations, Trajectoires, MSD, Diffusion instantanée, Fit).

		Cette méthode analyse chaque tableau pour savoir s'il correspond :
			- à un tableau standard,
			- à un tableau filtré,
			- à un tableau reconnecté (pour les trajectoires),
			- à un tableau corrigé (pour les localisations),
			- ou à une absence de données.

		Les statuts retournés sont des chaînes de caractères provenant de la constante globale :data:`FILE_STATUS`.

		Le dictionnaire retourné contient systématiquement les clés suivantes : ``Localizations``, ``Beads``, ``Tracks``, ``MSD``, ``Instant D``, ``MSD Fit``

		:return: Un dictionnaire ``{str: str}`` contenant le statut de chaque type de tableau.
		"""
		res = {"File":          self.stack_name if self._stack_name else "No File",
			   "Localizations": self.get_df_status(self._data["loc"], self._data["f_loc"], "localizations"),
			   "Beads":         self.get_df_status(self._data["bds"], self._data["bds"], "localizations"),
			   "Tracks":        self.get_df_status(self._data["trc"], self._data["f_trc"], "tracks"),
			   "MSD":           self.get_df_status(self._data["MSD"], self._data["f_MSD"], "tracks"),
			   "Instant D":     self.get_df_status(self._data["InD"], self._data["f_InD"], "tracks"),
			   "MSD Fit":       self.get_df_status(self._data["Fit"], self._data["f_Fit"], "tracks")}

		# Remplacement du Tracking si blinking est différent de No
		blk = self.get_df_status(self._data["blk"], self._data["f_blk"], "tracks", "Reconnected")
		if blk != "No": res["Tracks"] = blk

		return res

	##################################################
	@staticmethod
	def get_df_status(original: pd.DataFrame, filtered: pd.DataFrame, name: str, pre: str = "") -> str:
		"""
		Retourne le status d'un ensemble de dataframe en fonction de sa version initiale et filtrée.
		(indique également le nombre d'éléments avant et après filtre pour affichage).

		:param original: Dataframe initial.
		:param filtered: Dataframe filtré.
		:param name: Nom du type de données (localizations, tracks)
		:param pre: Ajoute un prefixe (exemple "reconnected" pour les trajectoires reconnectées)
		:return: Une chaine de caractère dépendant de si le tableau a été filtré et indiquant le nombre d'éléments (ainsi que le nombre filtrés si besoin).
		"""
		n_init, n_filt = len(original), len(filtered)
		yes = f"Yes {pre}" if pre else "Yes"

		if n_init == 0: return "No"
		if n_filt == 0 or n_filt == n_init: return f"{yes} ({n_init} {name})"
		else: return f"{yes} Filtered ({n_filt}/{n_init} {name})"

	# ==================================================
	# region Entrées-sorties
	# ==================================================

	# ==================================================
	# endregion Entrées-sorties
	# ==================================================
	##################################################
	def save(self, key: str, path: str | Path, timestamp: str):
		"""

		:param key:
		:param path:
		:param timestamp:
		"""
		self._data[key].to_csv(self.output_name(self.KEYS_TO_FILE[key], path, timestamp), index=False)

	##################################################
	def save_filtered(self, path: str | Path, timestamp: str = ""):
		"""
		Enregistre tous les fichiers filtrés s'ils ne sont pas vides.

		:param path:
		:param timestamp:
		"""
		timestamp = FileIO.get_timestamp_for_files() if not timestamp else timestamp
		for key, fname in self.KEYS_TO_FILE.items():
			# Il s'agit d'un filtre, il n'est pas vide et il a une taille différente de l'original
			if "f_" in key and not self._data[key].empty and len(self._data[key]) != len(self._data[key[2:]]):
				self.save(key, path, timestamp)

	# ==================================================
	# region Interface
	# ==================================================
	##################################################
	def get_ui(self, name: str = "default", margin: int = 5) -> "ResultsUI":
		"""
		Retourne une représentation Qt des résultats, existante ou nouvellement créée.

		:param name: Nom identifiant la représentation.
		:return: Représentation Qt synchronisée avec les résultats.
		"""
		if name in self._uis: return self._uis[name]

		from palm_tracer.UI.ResultsUI import ResultsUI  # Hack pour éviter les imports cycliques

		ui = ResultsUI(margin=margin)
		ui.update_status(self.get_status())
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
		for ui in self._uis.values(): ui.update_status(status)
