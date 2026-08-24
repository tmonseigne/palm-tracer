"""Définit le groupe de paramètres du traitement par lots."""

from __future__ import annotations

from dataclasses import dataclass
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
	Classe contenant les informations de batch de fichiers :

	Attributs :
		- **Files** (:class:`FileList <palm_tracer.Settings.Types.FileList.FileList>`) : Liste des fichiers au Batch.
		- **Mode** (:class:`Combo <palm_tracer.Settings.Types.Combo.Combo>`) : Méthode d'utilisation du Batch
		  (Un seul fichier est traité ou chaque fichier est traité séparément ou l'ensemble des fichiers correspondent à une seule acquisition).
	"""

	label: str = "Batch"
	setting_list = {
			"Files": [FileList, ["Files", ""]],
			"Mode":  [Combo, ["Mode", "", 0, ["Only one", "Each File separately", "All in One"]]],
			}
	mode: int = 1

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
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # crée et assigne le layout au widget
	group = Batch()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
