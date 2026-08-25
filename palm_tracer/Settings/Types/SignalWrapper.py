"""Fournit une abstraction des signaux Qt avec regroupement des émissions bloquées."""

from __future__ import annotations

from typing import Any, Callable, Optional

from qtpy.QtCore import QObject, Signal


##################################################
class SignalWrapper(QObject):
	"""
	Encapsule un signal Qt et regroupe les émissions produites pendant son blocage.

	Les connexions et déconnexions sont déléguées au signal interne. Dans un contexte :meth:`blocked`, les appels à :meth:`emit` mémorisent uniquement
	la dernière valeur ; celle-ci est émise une seule fois à la sortie du blocage externe.
	"""

	_signal = Signal(object)
	"""Signal encapsulé, prêt à être utilisé dans l'application."""

	##################################################
	def __init__(self):
		"""Initialise l'objet SignalWrapper."""
		super().__init__()  # .							 Appelle le constructeur de la classe parent QObject.
		self._block_count: int = 0  # .					 Compteur de blocs imbriqués.
		self._pending: bool = False  # .				 Indique si une émission est en attente.
		self._pending_value: Any = None  # .			 Dernière valeur reçue pendant le blocage.
		self._slots: list[Callable[[Any], None]] = []  # Liste des Fonctions ou slots connectés.
		self._emit_on_unblock_stack: list[bool] = []  # .Liste des émissions à conserver

	##################################################
	def connect(self, f: Callable[[Any], None], **kwargs):
		"""
		Connecte une fonction ou un slot au signal encapsulé.

		:param f: Fonction ou slot à connecter.
		"""
		self._signal.connect(f)  # Connexion de la fonction fournie au signal.
		self._slots.append(f)

	def disconnect(self, f: Optional[Callable[[Any], None]] = None) -> int:
		"""
		Déconnecte ``f`` si fourni, sinon **tous** les slots. Retourne le nombre de déconnecté.

		:param f: Fonction ou slot à déconnecter.
		:return: Nombre de slots déconnectés.
		"""
		n = 0
		if f is None:
			# Déconnecte tous les signaux connus
			for s in list(self._slots):
				try:
					self._signal.disconnect(s)
					n += 1
				except (TypeError, RuntimeError): pass  # Signal déjà déconnecté ou objet détruit : ignorer
			self._slots.clear()
			return n

		# Déconnecte un slot précis
		try:
			self._signal.disconnect(f)
			n = 1
		except (TypeError, RuntimeError): n = 0

		# Nettoie le registre
		try: self._slots.remove(f)
		except ValueError: pass
		return n

	##################################################
	def emit(self, value: Any = None, **kwargs):
		"""Émet le signal encapsulé."""
		if self._block_count > 0:
			self._pending = True
			self._pending_value = value
			return
		self._signal.emit(value)  # Émission du signal.

	##################################################
	# --- Gestion du blocage des signaux ---
	class BlockCtx:
		"""
		Gère le blocage temporaire d'un :class:`SignalWrapper` dans une instruction ``with``.

		:param owner: Signal encapsulé dont les émissions sont bloquées.
		:param emit_last: Émet la dernière valeur mémorisée à la sortie du contexte externe.
		"""

		def __init__(self, owner: "SignalWrapper", emit_last: bool = True):
			"""
			Initialise l'instance.

			:param owner: Signal encapsulé dont les émissions sont bloquées.
			:param emit_last: Si ``True``, émet la dernière valeur mémorisée à la sortie du contexte.
			"""
			self._o = owner
			self._emit_last = emit_last

		def __enter__(self):
			"""
			Active le contexte de blocage et retourne son gestionnaire.

			:return: Gestionnaire de contexte actif.
			"""
			self._o._block_begin(self._emit_last)
			return self

		def __exit__(self, exc_type, exc, tb):
			"""
			Termine le contexte de blocage sans masquer les exceptions.

			:param exc_type: Type de l'exception levée.
			:param exc: Exception levée.
			:param tb: Trace de l'exception.
			:return: Toujours ``False`` afin de propager les exceptions.
			"""
			self._o._block_end()
			return False

	def blocked(self, emit_last: bool = True) -> "BlockCtx":
		"""
		Retourne un contexte de blocage des signaux.

		:param emit_last: Si ``True``, émet la dernière valeur à la fin du blocage. Si ``False``, ignore toutes les émissions reçues pendant le blocage.
		"""
		return SignalWrapper.BlockCtx(self, emit_last)

	def _block_begin(self, emit_last: bool):
		"""Démarre (ou imbrique) un blocage."""
		self._block_count += 1
		self._emit_on_unblock_stack.append(emit_last)

	def _block_end(self):
		"""Termine un blocage et émet éventuellement la dernière valeur mémorisée."""
		if self._block_count == 0: return
		emit_last = self._emit_on_unblock_stack.pop()
		self._block_count -= 1
		if self._block_count != 0: return
		# Fin du blocage externe : on émet une seule fois si nécessaire.
		pending_value, has_pending = self._pending_value, self._pending
		self._pending, self._pending_value = False, None
		if has_pending and emit_last: self._signal.emit(pending_value)
