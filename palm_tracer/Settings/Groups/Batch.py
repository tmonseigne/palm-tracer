"""Définit le groupe de paramètres du traitement par lots."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import cast

import numpy as np
from qtpy.QtWidgets import QPushButton

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Groups.BaseUIGroup import BaseUIGroup
from palm_tracer.Settings.Types import BaseSettingType, Combo, FileList
from palm_tracer.Tools import FileIO


# --------------------------------------------------
@dataclass
class Batch(BaseSettingGroup):
	"""
	Regroupe les paramètres du traitement par lots.

	Paramètres regroupés :

	- ``Files`` (:class:`~palm_tracer.Settings.Types.FileList.FileList`) : fichiers à traiter.
	- ``Mode`` (:class:`~palm_tracer.Settings.Types.Combo.Combo`) : traite un seul fichier, chaque fichier séparément ou tous les fichiers comme une
	  acquisition unique.
	"""

	label: str = "Batch"
	"""Libellé du groupe affiché dans l'interface."""
	_settings: dict[str, BaseSettingGroup | BaseSettingType] = field(init=False, default_factory=lambda: {
			"Files": FileList("Files", "TIFF or Metamorph STK acquisitions to process. Select the current file from the list.",
							  FileIO.STACK_EXTENSIONS, FileIO.STACK_FILE_FILTER),
			"Mode":  Combo("Mode", "Process the selected file, each file independently, or all files as a single acquisition.",
						   0, ["Only one", "Each File separately", "All in One"])
			})
	"""Paramètres du groupe, créés indépendamment pour chaque instance."""
	_mode: int = field(init=False, default=1)
	"""Mode d'affichage du groupe dans l'interface."""
	_plane_cache: dict[str, tuple[int, int, int]] = field(init=False, default_factory=dict)
	"""Profondeur TIFF indexée par chemin, taille et date de modification du fichier."""

	# --------------------------------------------------
	def get_ui(self, name: str = "default", mode: int = -1) -> BaseUIGroup:
		"""Relie aussi le bouton Clear au retour au mode « Only one » lors de la création de l'interface."""
		if name in self._uis: return self._uis[name]
		ui = super().get_ui(name, mode)
		clear_button = cast(QPushButton, cast(FileList, self._settings["Files"]).get_ui(name).boxes[2])
		clear_button.clicked.connect(self._settings["Mode"].reset)
		return ui

	# --------------------------------------------------
	def get_paths(self, suffix: str = "_PALM_Tracer") -> list[str]:
		"""
		Construit les chemins des dossiers de résultats selon les fichiers du lot et le mode sélectionné.

		:param suffix: Suffixe ajouté au nom de chaque fichier sans extension pour former le chemin du dossier de résultats.
		:return: Chemins des dossiers de résultats ; si la liste est vide, chemin du suffixe dans le répertoire courant.
		"""
		file_list = cast(FileList, self._settings["Files"])
		mode = self._settings["Mode"].value

		files = file_list.items.copy()
		results: list[str] = []
		if files:  # Si au moins un fichier est présent
			if mode == 0: files = [file_list.current_text]
			elif mode == 2: files = [files[0]]
			for file in files:
				path = Path(file)
				results.append(str(path.with_suffix("")) + suffix)
			return results

		return [str(Path.cwd() / suffix)]  # Utilise le répertoire courant si aucun fichier n'est présent.

	# --------------------------------------------------
	def get_stacks(self) -> list[np.ndarray]:
		"""
		Récupère la liste de piles en fonction des paramètres.

		:return: Pile sélectionnée, piles séparées ou pile concaténée selon le mode ; liste vide si le lot ne contient aucun fichier.
		:raises ValueError: Si les dimensions des piles ne permettent pas leur concaténation.
		"""
		res = list[np.ndarray]()
		file_list = cast(FileList, self._settings["Files"])
		files = file_list.items
		mode = self._settings["Mode"].value
		if not files: return res  # .					   Aucun fichier dans le Batch
		if mode == 0:  # .								   Mode Only One
			res.append(FileIO.open_tif(file_list.current_text))
		else:  # .										   Mode fichiers séparés ou concaténés
			for file in files:
				res.append(FileIO.open_tif(file))
			if mode == 2:  # .							   Mode fichiers concaténés
				try:
					res = [np.concatenate(res, axis=0)]  # On concatène la liste des fichiers
				except ValueError as e:
					raise ValueError(f"Unable to concatenate stacks: {e}") from e

		return res

	# --------------------------------------------------
	def get_plane_count(self) -> int | None:
		"""
		Retourne le nombre de plans selon le mode de traitement, avec mise en cache des profondeurs TIFF.

		:return: Profondeur du fichier sélectionné, profondeur maximale des fichiers séparés ou somme des profondeurs des fichiers concaténés.
			Renvoie ``None`` si aucun fichier n'est disponible dans le mode sélectionné.
		"""
		file_list = cast(FileList, self._settings["Files"])
		for path in self._plane_cache.keys() - set(file_list.items): del self._plane_cache[path]  # Si la liste a été réduite, le cache doit être revu.
		files = file_list.items if self._settings["Mode"].value != 0 else [file_list.current_text]  # Tous les fichiers ou seulement le fichier sélectionné.
		if not files or not files[0]: return None  # Aucun fichier

		plane_count = 0
		for file in files:
			stat = Path(file).stat()
			cached = self._plane_cache.get(file)
			if cached is None or cached[:2] != (stat.st_size, stat.st_mtime_ns):  # Si le fichier a évolué ou n'a jamais été évalué.
				cached = (stat.st_size, stat.st_mtime_ns, FileIO.read_tif_shape(file)[0])  # Taille, date, profondeur
				self._plane_cache[file] = cached
			if self._settings["Mode"].value == 2: plane_count += cached[2]
			else: plane_count = max(plane_count, cached[2])
		return plane_count


# --------------------------------------------------
if __name__ == "__main__":
	import sys

	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # Crée et affecte la mise en page au widget
	group = Batch()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
