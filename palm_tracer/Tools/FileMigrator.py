"""
Ce fichier contient la classe :class:`FileMigrator` permettant de lire un dossier de résultat de PALMTracer depuis Metamorph vers le format actuel.
"""
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import NamedTuple

import numpy as np
import pandas as pd

from palm_tracer.Processing.Parsing import FILES_COLUMNS, get_meta, MODEL_ROWS, N_COL_META
from palm_tracer.Tools import FileIO, Ui


##################################################
class Link(NamedTuple):
	"""
	Structure permettant le lien entre nouvelle et ancienne nomenclature.

	:param old: Ancien nom de fichier.
	:param new: Nouveau nom de fichier.
	"""
	old: str
	new: str


##################################################
@dataclass
class FileMigrator:
	"""
	Outil de migration d'un dossier de traitement PALMTracer (ancien format Metamorph) vers le format Python plus récent.

	Le principe est :
		- l'utilisateur pointe un dossier d'entrée (un dossier se terminant par ``.PT``) ;
		- :meth:`analyze` inspecte les fichiers et les classes par type (loc/trc/MSD/...) ;
		- :meth:`migrate` crée un dossier de sortie et exécute ensuite les conversions nécessaires.

	.. note::
	   Cette classe ne modifie **pas** le dossier d'entrée : elle lit depuis :attr:`input_folder` et écrit dans :attr:`output_folder`.

	Attributs :
		- input_folder: Dossier source sélectionné par l'utilisateur.
		- output_folder: Dossier cible où seront écrits les fichiers convertis.
		- files: Dictionnaire ``{type: [paths...]}`` rempli par :meth:`analyze`.
		- suffix: Suffixe optionnel ajouté au nom du dossier de sortie.
		- meta: Métadonnées globales du jeu de données. Une ligne initialisée à -1 qui sera mis à jour avec durant la migration des fichiers.
	"""

	FILES_LINK: dict[str, Link] = field(init=False, default_factory=lambda:
	{"loc": Link("locPALMTracer.txt", "localizations"),
	 "trc": Link("trcPALMTracer.txt", "tracking"),
	 "A3D": Link("3DFit.txt", "astigmatism_3d_model"),
	 "MSD": Link("trcPALMTracer-Full-MSD.txt", "tracking_MSD"),
	 "InD": Link("trcPALMTracer-Full-Dinst.txt", "tracking_InstantD"),
	 "Fit": Link("trcPALMTracer-Full-D.txt", "tracking_Fit")})
	"""Correspondances entre les anciens noms et les nouveaux."""

	input_folder: Path = field(init=False, default_factory=lambda: Path())
	"""Dossier source sélectionné par l'utilisateur."""
	output_folder: Path = field(init=False, default_factory=lambda: Path())
	"""Dossier cible où seront écrits les fichiers convertis."""
	files: dict[str, list[Path]] = field(init=False, default_factory=lambda: {"loc":    [], "trc": [], "A3D": [],
																			  "MSD":    [], "InD": [], "Fit": [],
																			  "Unused": []})
	"""Dictionnaire ``{type: [paths...]}`` rempli par :meth:`analyze`."""
	suffix: str = field(init=False, default="")
	"""Suffixe optionnel ajouté au nom du dossier de sortie."""
	meta: pd.DataFrame = field(init=False, default_factory=lambda: get_meta(np.zeros(shape=(1, N_COL_META), dtype=int) - 1))
	"""Métadonnées globales du jeu de données. Une ligne initialisée à -1 qui sera mis à jour avec durant la migration des fichiers."""

	##################################################
	def open(self, folder: Path):
		"""
		Sélectionne le dossier d'entrée contenant les résultats PALMTracer.

		Le dossier Metamorph / PALMTracer est généralement nommé ``<monfichier>.PT``.
		Si ce n'est pas le cas, un avertissement est affiché (sans empêcher l'analyse).

		:param folder: Chemin du dossier à analyser.
		:raises FileNotFoundError: Si ``folder`` n'existe pas.
		:raises NotADirectoryError: Si ``folder`` n'est pas un dossier.
		:raises ValueError: Si ``folder`` ne finit pas par .PT comme un dossier de sortie type de PALMTracer sur Metamorph.
		"""
		if not folder.exists(): raise FileNotFoundError(f"Input folder does not exist: {folder}")
		if not folder.is_dir(): raise NotADirectoryError(f"Input path is not a directory: {folder}")
		if folder.suffix.lower() != ".pt": raise ValueError(f"Input folder should be named like 'something.PT' (MetaMorph output): {folder}")
		self.input_folder = folder

	##################################################
	def analyze(self):
		"""
		Analyse :attr:`input_folder` et classe les fichiers reconnus par catégorie.

		Effets de bord :
			- réinitialise :attr:`files` puis la remplit avec des chemins trouvés.
			- ne lit pas le contenu des fichiers (uniquement leur présence).

		:raises RuntimeError: Si aucun dossier n'a été sélectionné via :meth:`open`.
		"""
		if self.input_folder == Path(): raise RuntimeError("No input folder selected. Call 'open(folder)' before 'analyze()'.")

		for key in self.files: self.files[key].clear()  # .							  Reset propre (évite d'empiler d'anciennes analyses).
		old_name_to_key = {link.old: key for key, link in self.FILES_LINK.items()}  # Index inversé : ancien nom ⇾ clé logique

		# Parcours non récursif : uniquement les fichiers présents à la racine du dossier PT
		for p in self.input_folder.iterdir():
			if not p.is_file(): continue
			key = old_name_to_key.get(p.name, "Unused")
			self.files[key].append(p)

		# Tri pour reproductibilité (tests / logs).
		for key in self.files: self.files[key].sort(key=lambda x: x.as_posix())

	##################################################
	def migrate(self):
		"""
		Lance la migration vers le format récent.

		Règle de nommage du dossier de sortie :
		- si l'entrée est ``monfichierdebase.PT`` alors sortie ``monfichierdebase_PALM_Tracer``

		.. warning:: Cette méthode suppose que :meth:`open` et :meth:`analyze` ont déjà été appelées.

		:raises RuntimeError: Si :attr:`input_folder` n'est pas défini.
		"""

		if self.input_folder == Path(): raise RuntimeError("No input folder selected. Call 'open(folder)' before 'analyze()'.")

		# Création du dossier de sortie
		stem = self.input_folder.stem  # "abc" si "abc.PT"
		out_name = f"{stem}_PALM_Tracer"
		self.output_folder = self.input_folder.with_name(out_name)

		# Création du dossier de sortie
		self.output_folder.mkdir(parents=True, exist_ok=True)

		self.suffix = FileIO.get_timestamp_for_files()  # Récupération d'un timestamp pour les fichiers
		self.migrate_localization()
		self.migrate_tracks()
		self.migrate_tracks_msd()
		self.migrate_tracks_instant_diffusion()
		self.migrate_tracks_fit()
		self.migrate_astigmatism_3d_model()
		self.make_meta()

	##################################################
	def make_meta(self):
		"""Écriture du fichier meta uniquement si au moins une valeur est différente de -1."""
		if (self.meta != -1).any().any(): self.meta.to_csv(self.output_folder / f"meta-{self.suffix}.csv", index=False)

	##################################################
	def update_meta(self, column: str, v: int | float):
		"""
		Mets à jour l'objet meta et vérifie si une valeur différente est présente.

		:param column: Colonne à mettre à jour
		:param v: Valeur à insérer
		"""
		ref = self.meta.loc[0, column]
		if ref == -1: self.meta.loc[0, column] = v
		elif ref != v:
			Ui.print_warning(f"Warning that the '{column}' metadata differs between several files to be migrated ({ref} VS {v}). "
							 f"The first one ({ref}) will be retained.")

	##################################################
	def migrate_localization(self):
		"""
		Migre le fichier de localisations PALMTracer vers le format courant.

		Cette méthode :
			- lit le fichier ``locPALMTracer.txt`` s'il est présent
			- extrait les métadonnées globales (dimensions, calibration temporelle et spatiale)
			- mets à jour :attr:`meta` via :meth:`update_meta`
			- renomme et complète les colonnes selon ``FILES_COLUMNS["Localization"]``
			- écrit le fichier CSV converti dans :attr:`output_folder`.

		Le fichier de sortie est nommé : ``<new_name>-<timestamp>.csv`` où ``new_name`` correspond à ``FILES_LINK["loc"].new``.
		"""
		if len(self.files["loc"]) == 0: Ui.print_warning("No localization file in folder.")
		else:
			file = self.files["loc"][0]
			data, header = self.open_old_file(file, header=True, skiprows=2)
			metas = [v.strip() for v in header[1].split("\t")]
			self.update_meta("Width", int(metas[0]))
			self.update_meta("Height", int(metas[1]))
			self.update_meta("Plane Number", int(metas[2]))
			self.update_meta("Pixel Size (μm)", float(metas[4]))
			self.update_meta("Exposure Time (s/frame)", float(metas[5]))

			data = self.dataframe_migrator(data, FILES_COLUMNS["Localization"]["columns"])
			data.to_csv(self.output_folder / f"{self.FILES_LINK['loc'].new}-{self.suffix}.csv", index=False)  # Enregistrement
			Ui.print_success("Localization file migrated.")

	##################################################
	def migrate_tracks(self):
		"""
		Migre le fichier de tracking PALMTracer vers le format courant.

		Cette méthode :
			- lit le fichier ``trcPALMTracer.txt`` s'il est présent
			- extrait et harmonise les métadonnées globales (image, calibration)
			- renomme et complète les colonnes selon ``FILES_COLUMNS["Tracking"]``
			- écrit le fichier CSV converti dans :attr:`output_folder`.

		Le fichier de sortie est nommé : ``<new_name>-<timestamp>.csv`` où ``new_name`` correspond à ``FILES_LINK["trc"].new``.
		"""
		if len(self.files["trc"]) == 0: Ui.print_warning("No tracking file in folder.")
		else:
			file = self.files["trc"][0]
			data, header = self.open_old_file(file, header=True, skiprows=2)
			metas = [v.strip() for v in header[1].split("\t")]
			self.update_meta("Width", int(metas[0]))
			self.update_meta("Height", int(metas[1]))
			self.update_meta("Plane Number", int(metas[2]))
			self.update_meta("Pixel Size (μm)", float(metas[4]))
			self.update_meta("Exposure Time (s/frame)", float(metas[5]))

			data = self.dataframe_migrator(data, FILES_COLUMNS["Tracking"]["columns"])
			data.to_csv(self.output_folder / f"{self.FILES_LINK['trc'].new}-{self.suffix}.csv", index=False)  # Enregistrement
			Ui.print_success("Tracking file migrated.")

	##################################################
	def migrate_astigmatism_3d_model(self):
		"""
		Migre le fichier de modèle d'astigmatisme 3D PALMTracer.

		Cette méthode :
			- lit le fichier ``3DFit.txt`` s'il est présent
			- assigne explicitement les noms de colonnes et les indices de lignes
			  à partir de ``FILES_COLUMNS["Astigmatism 3D Model"]`` et ``MODEL_ROWS``
			- écrit le modèle sous forme de CSV dans :attr:`output_folder`.

		Le fichier de sortie est nommé : ``<new_name>-<timestamp>.csv`` où ``new_name`` correspond à ``FILES_LINK["A3D"].new``.
		"""
		if len(self.files["A3D"]) == 0: Ui.print_warning("No Astimagmatism 3D Model file in folder.")
		else:
			file = self.files["A3D"][0]
			data, header = self.open_old_file(file, header=False, skiprows=2)
			data.columns = FILES_COLUMNS["Astigmatism 3D Model"]["columns"]
			data.index = MODEL_ROWS
			data.to_csv(self.output_folder / f"astigmatism_3d_model-{self.suffix}.csv")  # Enregistrement
			Ui.print_success("Astimagmatism 3D Model file migrated.")

	##################################################
	def migrate_tracks_msd(self):
		"""
		Migre le fichier MSD (Mean Square Displacement) PALMTracer.

		Cette méthode :
			- lit un fichier à structure irrégulière (nombre de colonnes variable par ligne)
			- supprime la colonne ROI (première colonne)
			- renomme les colonnes sous la forme : ``Track, <metric> 1, <metric> 2, ..., <metric> N`` ;
			- écrit le fichier CSV converti dans :attr:`output_folder`.

		Le nom de la métrique est issu de ``FILES_COLUMNS["MSD"]["columns"]``.

		Le fichier de sortie est nommé : ``<new_name>-<timestamp>.csv`` où ``new_name`` correspond à ``FILES_LINK["MSD"].new``.
		"""
		if len(self.files["MSD"]) == 0: Ui.print_warning("No MSD file in folder.")
		else:
			file = self.files["MSD"][0]
			data, header = self.open_old_irregular_file(file, skiprows=2)
			data = data.iloc[:, 1:].copy()  # .																	Suppression de la colonne ROI
			data.columns = ["Track"] + [f"{FILES_COLUMNS['MSD']['columns'][1]} {i}" for i in range(1, data.shape[1])]
			data.to_csv(self.output_folder / f"{self.FILES_LINK['MSD'].new}-{self.suffix}.csv", index=False)  # Enregistrement
			Ui.print_success("MSD file migrated.")

	##################################################
	def migrate_tracks_instant_diffusion(self):
		"""
		Migre le fichier de diffusion instantanée PALMTracer.

		Cette méthode :
			- lit un fichier à structure irrégulière (nombre de colonnes variable par ligne)
			- supprime la colonne ROI (première colonne)
			- renomme les colonnes sous la forme : ``Track, <metric> 1, <metric> 2, ..., <metric> N`` ;
			- écrit le fichier CSV converti dans :attr:`output_folder`.

		Le nom de la métrique est issu de ``FILES_COLUMNS["InD"]["columns"]``.

		Le fichier de sortie est nommé : ``<new_name>-<timestamp>.csv`` où ``new_name`` correspond à ``FILES_LINK["InD"].new``.
		"""
		if len(self.files["InD"]) == 0: Ui.print_warning("No Instant Diffusion file in folder.")
		else:
			file = self.files["InD"][0]
			data, header = self.open_old_irregular_file(file, skiprows=2)
			data = data.iloc[:, 1:].copy()  # .																	Suppression de la colonne ROI
			data.columns = ["Track"] + [f"{FILES_COLUMNS['Instant Diffusion']['columns'][1]} {i}" for i in range(1, data.shape[1])]  # Renommage
			data.to_csv(self.output_folder / f"{self.FILES_LINK['InD'].new}-{self.suffix}.csv", index=False)  # Enregistrement
			Ui.print_success("Instant Diffusion file migrated.")

	##################################################
	def migrate_tracks_fit(self):
		"""
		Migre le fichier d'ajustement de trajectoires PALMTracer.

		Cette méthode :
			- lit le fichier ``trcPALMTracer-Full-D.txt``
			- neutralise la colonne ROI (remplacée par une valeur constante)
			- corrige l'ordre des colonnes (ROI / Track)
			- détecte automatiquement le mode d'ajustement en fonction du nombre de colonnes
			- applique les noms de colonnes appropriés à partir de ``FILES_COLUMNS``
			- écrit le fichier CSV converti dans :attr:`output_folder`.

		Le mode d'ajustement est déterminé comme suit :
			- 9 colonnes  → Fit mode 1.
			- 10 colonnes → Fit mode 2.
			- 11 colonnes → Fit mode 3.

		.. warning:: Toute incohérence sur le nombre de colonnes peut conduire à un mauvais mode d'ajustement.
		"""
		if len(self.files["Fit"]) == 0: Ui.print_warning("No Fit file in folder.")
		else:
			file = self.files["Fit"][0]
			data, header = self.open_old_file(file, header=True, skiprows=3)
			data.iloc[:, 0] = -1  # La colonne ROI n'est plus utilisé, mais sera remplacé par la colonne length (à -1).
			cols = list(data.columns)
			ncols = len(cols)
			cols[0], cols[1] = cols[1], cols[0]  # .															Switch les noms de colonnes ROI et Trace
			data = data[cols]  # .																				Change l'ordre des colonnes
			cols = FILES_COLUMNS["Fit"]["columns"].copy()
			fit_mode = 1 if ncols == 9 else 2 if ncols == 10 else 3
			cols += FILES_COLUMNS[f"Fit_{fit_mode}"]["columns"]
			data.columns = cols  # .																			Remplacer les noms de colonnes
			data.to_csv(self.output_folder / f"{self.FILES_LINK['Fit'].new}-{self.suffix}.csv", index=False)  # Enregistrement
			Ui.print_success("Fit file migrated.")

	##################################################
	@staticmethod
	def open_old_file(file: Path, header: bool = True, skiprows: int = 2, sep: str = "\t") -> tuple[pd.DataFrame, list[str]]:
		"""
			Ouvre un fichier PALMTracer (MetaMorph) au format texte tabulé.

			Le fichier est supposé structuré de la façon suivante :
				- ``skiprows`` premières lignes : informations globales (dimensions, calibration, options…)
				- ligne suivante (optionnelle)   : titres des colonnes
				- reste du fichier               : données tabulaires

			:param file: Chemin vers le fichier PALMTracer à ouvrir.
			:param header: Indique si une ligne de titres de colonnes est présente après les lignes d'en-tête.
			:param skiprows: Nombre de lignes d'informations à lire et à conserver avant les données.
			:param sep: Séparateur de colonnes utilisé dans le fichier.
			:return: Tuple ``(dataframe, header_lines)`` avec les données numériques et la liste des lignes d'informations brutes (sans ``\\n``).
			:raises FileNotFoundError: Si le fichier n'existe pas.
		"""
		if not file.is_file(): raise FileNotFoundError(f"Filename invalid: {file}")

		header_lines: list[str] = []
		with file.open("r", encoding="utf-8", errors="replace") as f:
			for _ in range(skiprows):
				line = f.readline()
				if not line:
					raise ValueError(f"File does not contain {skiprows} header lines: {file}")
				header_lines.append(line.rstrip("\n"))

		df = pd.read_csv(file, sep=sep, header=0 if header else None, skiprows=skiprows, engine="python")  # On récupère le tableau
		return df, header_lines

	##################################################
	@staticmethod
	def open_old_irregular_file(file: Path, skiprows: int = 2, sep: str = "\t", ) -> tuple[pd.DataFrame, list[str]]:
		"""
		Ouvre un fichier PALMTracer (MetaMorph) au format texte tabulé, en tolérant les lignes avec un nombre de colonnes variable.

		Si certaines lignes n'ont pas le même nombre de colonnes, la fonction :
		- détecte le nombre maximal de colonnes,
		- complète les lignes plus courtes avec des valeurs manquantes (NaN),
		- tronque les lignes plus longues à la largeur max (rare, mais protège).

		:param file: Chemin vers le fichier PALMTracer à ouvrir.
		:param skiprows: Nombre de lignes d'informations à lire et à conserver avant les données.
		:param sep: Séparateur de colonnes utilisé dans le fichier.
		:return: Tuple ``(dataframe, header_lines)``.
		:raises FileNotFoundError: Si le fichier n'existe pas.
		:raises ValueError: Si le fichier ne contient pas assez de lignes d'en-tête.
		"""
		if not file.is_file(): raise FileNotFoundError(f"Filename invalid: {file}")

		# 1) Lecture brute
		lines = file.read_text(encoding="utf-8", errors="replace").splitlines()

		if len(lines) < skiprows: raise ValueError(f"File does not contain {skiprows} header lines: {file}")

		header_lines = lines[:skiprows]
		data_lines = lines[skiprows:]

		# 2) Gestion de la ligne de titre si présente
		start_idx = 0

		# 3) Split des lignes data et détection largeur max
		rows: list[list[str]] = []
		max_cols = 0

		for line in data_lines[start_idx:]:
			row = line.rstrip("\n").split(sep)
			rows.append(row)
			if len(row) > max_cols: max_cols = len(row)

		# Pas de données
		if max_cols == 0: return pd.DataFrame(), header_lines

		# 4) Rectangularisation (pad avec None)
		rect_rows: list[list[str]] = []
		for row in rows:
			if len(row) < max_cols: row += [""] * (max_cols - len(row))
			elif len(row) > max_cols: row = row[:max_cols]
			rect_rows.append(row)

		return pd.DataFrame(rect_rows), header_lines

	##################################################
	@staticmethod
	def column_migrator(name: str) -> str:
		"""
		Retourne une clé actuelle à partir d'un nom de colonne ancien.

		:param name: Nom de la colonne en entrée
		:return: Nom de la nouvelle colonne
		"""
		# Nettoyage du nom de la colonne
		s = name.strip().lower()  # .		 Changement de casse
		s = s.replace("_", "")  # .			 Remplacement des underscores
		s = re.sub(r"\(.*?\)", "", s)  # .	 Supprime tout ce qui est entre parenthèses
		s = re.sub(r"\s+", "", s).strip()  # Remplacement des espaces

		if s in ("mse", "msegauss", "msegaussian"): return "MSE XY"
		if s in ("angle", "anglerad", "angle(rad)"): return "Theta"

		# Familles : centroidx/y/z, sigmax/y
		if s.startswith("centroidx"): return "X"
		if s.startswith("centroidy"): return "Y"
		if s.startswith("centroidz"): return "Z"
		if s.startswith("sigmax"): return "Sigma X"
		if s.startswith("sigmay"): return "Sigma Y"

		# Autres colonnes assez stables ou identiques
		if s == "intensity0": return "Intensity 0"
		if s == "intensityoffset": return "Intensity Offset"
		if s == "intensity": return "Intensity"
		if s == "integratedintensity": return "Integrated Intensity"

		if s == "id": return "Id"
		if s == "plane": return "Plane"
		if s == "index": return "Index"
		if s == "channel": return "Channel"
		if s == "surface": return "Surface"
		if s == "circularity": return "Circularity"
		if s == "track": return "Track"

		if s == "pairdistance": return "Pair Distance"
		if s == "msez": return "MSE Z"
		return s

	##################################################
	def dataframe_migrator(self, data: pd.DataFrame, target_cols: list[str]) -> pd.DataFrame:
		"""
		Normalise un DataFrame PALMTracer vers un schéma de colonnes cible.

		Cette méthode :
			- renomme les colonnes existantes à l'aide de :meth:`column_migrator`
			- ignore les colonnes non reconnues
			- ajoute les colonnes manquantes initialisées à 0
			- retourne le DataFrame réordonné selon ``target_cols``.

		:param data: DataFrame d'entrée issue du format PALMTracer.
		:param target_cols: Liste ordonnée des colonnes attendues dans le format cible.
		:return: :class:`DataFrame <pandas.DataFrame>` conforme au schéma cible.
		"""
		# Renommage robuste : on construit old_col ⇾ new_col
		rename_map: dict[str, str] = {}
		for col in data.columns:
			key = self.column_migrator(col)
			if key in target_cols: rename_map[col] = key

		data = data.rename(columns=rename_map)  # Renommage des paires trouvées

		# Ajout des colonnes manquantes
		for col in target_cols:
			if col not in data.columns: data[col] = 0

		return data[target_cols]  # Tri dans le bon ordre (et on ignore les colonnes extra)
