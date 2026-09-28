"""Définit le groupe de paramètres du traitement par lots."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import cast

import numpy as np

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import Combo, FileList
from palm_tracer.Tools import FileIO, Ui


##################################################
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
	setting_list = {
			"Files": [FileList, ["Files", ""]],
			"Mode":  [Combo, ["Mode", "", 0, ["Only one", "Each File separately", "All in One"]]],
			}
	"""Définition des paramètres du groupe et de leur configuration."""
	mode: int = 1
	"""Mode d'affichage du groupe dans l'interface."""
	_plane_cache: dict[str, tuple[int, int, int]] = field(init=False, default_factory=dict)
	"""Profondeur TIFF indexée par chemin, taille et date de modification du fichier."""

	##################################################
	def get_paths(self, suffix: str = "_PALM_Tracer") -> list[str]:
		"""
		Génère un chemin basé sur les fichiers du Batch et le mode sélectionné.

		:param suffix: Suffixe à ajouter au nom du dossier créé.
		:return: Chemin complet du dossier généré.
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

		return [str(Path.cwd() / suffix)]  # Retourne le chemin courant si aucun fichiers

	##################################################
	def get_stacks(self) -> list[np.ndarray]:
		"""
		Récupère la liste de piles en fonction des paramètres.

		:return: Une liste de piles en fonction du Batch (une seule pile, un ensemble de piles concaténées ou un groupe de piles).
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
			if mode == 2:  # .							   Mode fichiers Concaténés
				try:
					res = [np.concatenate(res, axis=0)]  # On concatène la liste des fichiers
				except ValueError as e:
					Ui.print_warning(f"Error when concatenating stacks (they will be processed independently):\nValueError: {e}")

		return res

	##################################################
	def get_plane_count(self) -> int | None:
		"""Retourne le nombre de plans du fichier courant ou de l'acquisition concaténée.

		:return: Nombre de plans, ou ``None`` si aucun fichier n'est sélectionné.
		"""
		file_list = cast(FileList, self._settings["Files"])
		for path in self._plane_cache.keys() - set(file_list.items): del self._plane_cache[path]  # Si la liste a été réduite, le cache doit être revu.
		files = file_list.items if self._settings["Mode"].value != 0 else [file_list.current_text]  # Mode All in one ou only one
		if not files or not files[0]: return None  # Aucun Fichier

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


##################################################
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
