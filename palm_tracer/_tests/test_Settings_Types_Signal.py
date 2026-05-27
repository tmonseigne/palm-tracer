"""Tests unitaires pour SignalWrapper."""
from typing import Any, List

import pytest

from palm_tracer.Settings.Types import SignalWrapper


##################################################
@pytest.fixture
def sw() -> SignalWrapper:
	"""Instance fraîche de SignalWrapper pour chaque test."""
	return SignalWrapper()


##################################################
def test_connect_and_emit_direct(sw: SignalWrapper):
	"""Connexion d'un slot Python et émission immédiate."""
	received: List[Any] = []
	sw.connect(lambda v: received.append(v))

	sw.emit("X")
	assert received == ["X"]


##################################################
def test_disconnect(sw: SignalWrapper):
	"""Connexion d'un slot Python et émission immédiate."""
	received: List[Any] = []
	received2: List[Any] = []
	slot = lambda v: received.append(v)  # <– même objet pour connect & disconnect
	slot2 = lambda v: received2.append(v)
	sw.connect(slot)
	sw.connect(slot2)

	sw.emit("X")
	assert received == ["X"]
	assert received2 == ["X"]
	sw.disconnect(slot)
	sw.emit("Y")
	assert received == ["X"]  # .	  On n'est pas censé avoir reçu la suite.
	assert received2 == ["X", "Y"]  # On n'a pas déconnecté celui-là.
	sw.disconnect()
	sw.emit("Z")

	assert received == ["X"]  # .	  On n'est pas censé avoir reçu la suite.
	assert received2 == ["X", "Y"]  # On n'est pas censé avoir reçu la suite.


##################################################
def test_block_simple_coalescence_last_value(sw: SignalWrapper):
	"""
	Pendant un blocage, plusieurs emit() sont coalescés :
	une seule émission à la sortie, avec la DERNIÈRE valeur.
	"""
	received: List[Any] = []
	sw.connect(lambda v: received.append(v))

	with sw.blocked():
		sw.emit("A")
		sw.emit("B")  # Écrase A
		sw.emit("C")  # Écrase B

	# Une seule émission (C) après sortie du bloc
	assert received == ["C"]


##################################################
def test_block_without_emits_no_output(sw: SignalWrapper):
	"""Si aucun emit() pendant le blocage : rien n'est émis à la sortie."""
	received: List[Any] = []
	sw.connect(lambda v: received.append(v))

	with sw.blocked():
		# pas d'emit
		pass

	assert received == []


##################################################
def test_nested_blocks_emit_once_at_outer_exit(sw: SignalWrapper):
	"""Blocages imbriqués : aucune émission avant le dernier __exit__."""
	received: List[Any] = []
	sw.connect(lambda v: received.append(v))

	with sw.blocked():
		with sw.blocked():
			sw.emit(1)
			sw.emit(2)
		# à ce stade, toujours rien
		assert received == []
		# encore du bruit
		sw.emit(3)

	# Une seule émission à la fin, avec la dernière valeur (3)
	assert received == [3]


##################################################
def test_emit_default_none_coalesced(sw: SignalWrapper):
	"""Appel emit() sans valeur (None par défaut) pendant blocage → émis ensuite."""
	received: List[Any] = []
	sw.connect(lambda v: received.append(v))

	with sw.blocked(): sw.emit()

	assert received == [None]


##################################################
def test_block_flags_reset_after_flush(sw: SignalWrapper):
	"""Après la sortie et l'émission coalescée, les drapeaux internes doivent être réinitialisés."""
	received: List[Any] = []
	sw.connect(lambda v: received.append(v))

	# On déclenche une coalescence.
	with sw.blocked(): sw.emit("Z")

	# Après la sortie, les champs doivent être remis à zéro côté instance (un nouvel emit doit re-partir à propre).
	assert received == ["Z"]
	# Forcer un autre cycle de blocage pour vérifier que rien n'est 'retenu'.
	with sw.blocked(): pass
	# Pas d'émission supplémentaire.
	assert received == ["Z"]


##################################################
def test_block_without_emit(sw: SignalWrapper):
	"""Après la sortie et l'émission coalescée, les drapeaux internes doivent être réinitialisés."""
	received: List[Any] = []
	sw.connect(lambda v: received.append(v))

	# On déclenche un emit mais on n'est pas censé les récupérer après.
	with sw.blocked(False): sw.emit("Z")

	# Après la sortie, les champs doivent être remis à zéro côté instance.
	assert received == []

	sw.emit("Z")
	assert received == ["Z"]

	# Forcer un autre cycle de blocage pour vérifier que rien n'est 'retenu'.
	with sw.blocked(False): pass
	# Pas d'émission supplémentaire.
	assert received == ["Z"]


##################################################
def test_blocked_returns_context_manager_instance(sw: SignalWrapper):
	"""blocked() retourne bien un context manager du bon type (BlockCtx)."""
	ctx = sw.blocked()
	assert isinstance(ctx, SignalWrapper.BlockCtx)


##################################################
def test_internal_block_begin_end_paths(sw: SignalWrapper):
	"""
	Couvre explicitement les chemins internes :
	  - _block_end() appelé alors que le compteur est à 0 → early return
	  - _block_begin() puis _block_end() sans pending → pas d'émission
	"""
	received: List[Any] = []
	sw.connect(lambda v: received.append(v))

	# 1) _block_end() quand rien n'est bloqué : ne doit pas lever ni émettre
	sw._block_end()
	assert received == []

	# 2) begin/end sans pending : ne doit rien émettre
	sw._block_begin(True)
	sw._block_end()
	assert received == []


##################################################
def test_coalescence_overwrite_multiple_times(sw: SignalWrapper):
	"""Vérifie que la valeur en attente est toujours la dernière avant déblocage."""
	received: List[Any] = []
	sw.connect(lambda v: received.append(v))

	with sw.blocked():
		for i in range(10): sw.emit(i)
	assert received == [9]  # dernière


##################################################
def test_emit_direct_after_previous_block(sw: SignalWrapper):
	"""Après un blocage avec émission, un emit direct doit passer immédiatement (et ne pas être coalescé par un ancien état)."""
	received: List[Any] = []
	sw.connect(lambda v: received.append(v))

	with sw.blocked(): sw.emit("first")
	# Ici, on a reçu 'first' une fois
	assert received == ["first"]

	# Émission directe : doit s'ajouter immédiatement
	sw.emit("second")
	assert received == ["first", "second"]
