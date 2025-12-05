"""
Fichier contenant la classe :class:`SignalWrapper`.

Cette classe fournit une abstraction légère pour gérer des signaux dans une application basée sur Qt.
Elle encapsule un objet `Signal` de PyQt/PySide et facilite la gestion des connexions et des émissions de signaux.
"""
from typing import Any, Callable, Optional

from qtpy.QtCore import QObject, Signal


##################################################
class SignalWrapper(QObject):
	"""
	Encapsulation d'un signal Qt avec connexion, déconnexion, émission, blocage temporaire et coalescence.
		- :func:`blocked()` : contexte pour bloquer temporairement les signaux.
		- Pendant le blocage, les appels à :func:`emit(value)` ne propagent rien ; seule la **dernière** valeur est mémorisée.
		- À la fin du blocage externe (compteur à 0), une **seule** émission est effectuée avec la dernière valeur mémorisée (ou `None` si aucune).
	"""

	_signal = Signal(object)
	"""Signal encapsulé, prêt à être utilisé dans l'application."""
	_block_count: int = 0
	"""Compteur de blocs imbriqués."""
	_pending: bool = False
	"""Indique si une émission est en attente."""
	_pending_value: Any = None
	"""Dernière valeur reçue pendant le blocage."""
	_slots: list[Callable[[Any], None]] = []
	"""List des Fonctions ou slots connectés."""

	##################################################
	def __init__(self):
		"""Initialise l'objet SignalWrapper."""
		super().__init__()  # Appelle le constructeur de la classe parent QObject.

	##################################################
	def connect(self, f: Any):
		"""
		Connecte une fonction ou un slot au signal encapsulé.

		:param f: Fonction ou slot à connecter.
		"""
		self._signal.connect(f)  # Connexion de la fonction fournie au signal.
		self._slots.append(f)

	def disconnect(self, f: Optional[Callable[[Any], None]] = None) -> int:
		"""
		Déconnecte `f` si fourni, sinon **tous** les slots. Retourne le nb déconnectés.

		:param f: Fonction ou slot à déconnecter.
		:return: nombre de slots déconnectés
		"""
		n = 0
		if f is None:
			# déconnecte tout ce qu'on connaît
			for s in list(self._slots):
				try:
					self._signal.disconnect(s)
					n += 1
				except (TypeError, RuntimeError): pass  # déjà déconnecté / objet détruit → on ignore
			self._slots.clear()
			return n

		# déconnecte un slot précis
		try:
			self._signal.disconnect(f)
			n = 1
		except (TypeError, RuntimeError): n = 0

		# nettoie le registre
		try: self._slots.remove(f)
		except ValueError: pass
		return n

	##################################################
	def emit(self, value: Any = None):
		"""
		Émet le signal encapsulé.

		Utilisé pour notifier les parties de l'application abonnées au signal.
		"""
		if self._block_count > 0:
			self._pending = True
			self._pending_value = value
			return
		self._signal.emit(value)  # Émission du signal.

	##################################################
	# --- Gestion du blocage des signaux ---------------------------------------
	class BlockCtx:
		"""Contexte interne pour `with signal.blocked(): ...`."""
		def __init__(self, owner: "SignalWrapper"): self._o = owner
		def __enter__(self): self._o._block_begin()
		def __exit__(self, exc_type, exc, tb): self._o._block_end()

	def blocked(self) -> "BlockCtx":
		"""Retourne un contexte de blocage des signaux."""
		return SignalWrapper.BlockCtx(self)

	def _block_begin(self):
		"""Démarre (ou imbrique) un blocage."""
		self._block_count += 1

	def _block_end(self):
		"""
		Termine un blocage. Si c'était le dernier niveau, relance 1 seul `emit`
		avec la dernière valeur mémorisée.
		"""
		if self._block_count == 0:
			return
		self._block_count -= 1
		if self._block_count == 0:
			# Fin du blocage externe : on émet une seule fois si nécessaire.
			if self._pending:
				val = self._pending_value
				self._pending = False
				self._pending_value = None
				self._signal.emit(val)
