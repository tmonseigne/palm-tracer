"""
Module d'enregistrement d'un journal d'activité du process.

Ce fichier contient une classe principale :class:`Logger` permettant d'enregistrer les différentes étapes du process.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import TextIO

from palm_tracer.Tools import Ui


##################################################
@dataclass
class Logger:
	"""	Classe du journal d'activité."""

	filename: str = field(init=False, default="")
	"""Fichier de log à ouvrir."""
	file_handle: TextIO = field(init=False, default_factory=TextIO)
	"""Gestionnaire de fichier."""
	_isopen: bool = field(init=False, default=False)
	"""Indicateur d'ouverture du fichier."""

	##################################################
	def open(self, filename: str):
		"""Ouvre le fichier de log."""
		self.filename = filename
		try:
			self.file_handle = open(self.filename, "a", encoding="utf-8")  # Ouverture en mode ajout
			self._isopen = True
			print(f"[{self._get_time()}] Log opened : {self.filename}")
		except Exception as e:
			Ui.print_error(f"Error opening file {self.filename} : {e}")

	##################################################
	def close(self):
		"""Ferme le fichier de log."""
		if self._isopen:
			self.file_handle.write("\n")
			self.file_handle.flush()
			self.file_handle.close()
			print(f"[{self._get_time()}] Log closed : {self.filename}")
		else:
			Ui.print_warning(f"[{self._get_time()}] No files to close.")
		self.filename = ""
		self.file_handle = TextIO()
		self._isopen = False

	##################################################
	def add(self, msg: str):
		"""Ajoute un message au log."""
		timestamped_msg = f"[{self._get_time()}] {msg}"
		print(timestamped_msg)  # Affiche le message dans la console
		if self._isopen:
			try:
				self.file_handle.write(timestamped_msg + "\n")
				self.file_handle.flush()  # S'assure que les données sont écrites immédiatement
			except Exception as e:
				Ui.print_error(f"Error writing to file {self.filename} : {e}")
		else:
			Ui.print_warning(f"[{self._get_time()}] No log file open for writing.")

	##################################################
	@staticmethod
	def _get_time() -> str:
		"""Renvoie la date et l'heure actuelles sous forme de chaîne formatée."""
		return datetime.now().strftime("%d-%m-%Y %H:%M:%S")
