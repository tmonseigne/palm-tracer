"""
Module d'enregistrement d'un journal d'activité du process.

Ce fichier contient une classe principale :class:`Logger` permettant d'enregistrer les différentes étapes du process.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional, TextIO

from palm_tracer.Tools import Ui


##################################################
@dataclass
class Logger:
	"""Classe du journal d'activité.

	Notes
	-----
	- L'ouverture est idempotente : si un fichier est déjà ouvert, il est fermé avant de rouvrir.
	- La fermeture est idempotente : `close()` peut être appelée plusieurs fois sans erreurs.
	- La classe implémente le protocole context manager pour garantir la fermeture.
	"""

	filename: str = field(init=False, default="")
	"""Chemin du fichier de log ouvert (vide si aucun)."""
	file_handle: Optional[TextIO] = field(init=False, default_factory=TextIO)
	"""Handle du fichier ouvert (``None`` si fermé)."""
	_isopen: bool = field(init=False, default=False)
	"""Indicateur d'ouverture du fichier."""

	##################################################
	def open(self, filename: str | Path):
		"""
		Ouvre le fichier de log en mode ajout.

		:param filename: Chemin du fichier de log.

		.. note:: Si un fichier était déjà ouvert, il est fermé avant la réouverture afin d'éviter les handles orphelins
				  (particulièrement problématiques sous Windows).
		"""
		# Si déjà ouvert, on ferme proprement avant de rouvrir.
		if self._isopen: self.close()

		self.filename = str(filename)
		try:
			self.file_handle = open(self.filename, "a", encoding="utf-8", newline="\n")  # Ouverture en mode ajout
			self._isopen = True
			print(f"[{self._get_time()}] Log opened : {self.filename}")
		except Exception as e:
			# État cohérent même en cas d'échec.
			self.file_handle = None
			self._isopen = False
			Ui.print_error(f"Error opening file {self.filename} : {e}")

	##################################################
	def close(self):
		"""Ferme le fichier de log.

		.. note:: Méthode idempotente : peut être appelée plusieurs fois.
				  Force un flush + fsync pour limiter les surprises d'I/O (notamment sous Windows).
		"""
		if not self._isopen or self.file_handle is None:
			# On ne spamme pas de warnings ici : fermer un logger déjà fermé est un cas normal.
			self.filename = ""
			self.file_handle = None
			self._isopen = False
			return

		try:
			# Fin de fichier propre.
			self.file_handle.write("\n")
			self.file_handle.flush()
			try: os.fsync(self.file_handle.fileno())
			except Exception: pass  # fsync peut ne pas être disponible sur certains backends ; non bloquant.
			self.file_handle.close()
			print(f"[{self._get_time()}] Log closed : {self.filename}")
		except Exception as e:
			Ui.print_error(f"Error closing file {self.filename} : {e}")
		finally:
			self.filename = ""
			self.file_handle = None
			self._isopen = False

	##################################################
	def add(self, msg: str):
		"""Ajoute un message au log."""
		timestamped_msg = f"[{self._get_time()}] {msg}"
		print(timestamped_msg)  # Affiche le message dans la console
		if not self._isopen or self.file_handle is None:
			Ui.print_warning(f"[{self._get_time()}] No log file open for writing.")
			return

		try:
			self.file_handle.write(timestamped_msg + "\n")
			self.file_handle.flush()  # S'assure que les données sont écrites immédiatement
			try: os.fsync(self.file_handle.fileno())
			except Exception: pass
		except Exception as e:
			Ui.print_error(f"Error writing to file {self.filename} : {e}")

	##################################################
	def __enter__(self) -> "Logger":
		"""Permet l'utilisation via :code:`with`."""
		return self

	##################################################
	def __exit__(self, exc_type, exc, tb) -> None:
		"""Garantit la fermeture du fichier."""
		self.close()

	##################################################
	def __del__(self) -> None:
		"""
		Best-effort : évite de laisser un handle ouvert si l'objet est détruit.

		.. note:: Ne doit jamais lever d'exception.
		"""
		try: self.close()
		except Exception: pass

	##################################################
	@staticmethod
	def _get_time() -> str:
		"""Renvoie la date et l'heure actuelles sous forme de chaîne formatée."""
		return datetime.now().strftime("%d-%m-%Y %H:%M:%S")
