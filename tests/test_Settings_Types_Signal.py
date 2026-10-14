"""Teste l'abstraction et le regroupement des signaux Qt."""

from typing import Any, List
from unittest.mock import Mock

import pytest

from palm_tracer.Settings.Types import SignalWrapper


# --------------------------------------------------
@pytest.fixture
def sw() -> SignalWrapper:
	"""Instance fraîche de SignalWrapper pour chaque test."""
	return SignalWrapper()


# ==================================================
# region Connexion et déconnexion
# ==================================================
def test_connect_and_emit_direct(sw: SignalWrapper):
	"""Vérifie la connexion d'un slot Python et émission immédiate."""
	received: List[Any] = []
	sw.connect(lambda v: received.append(v))

	sw.emit("X")
	assert received == ["X"]


# --------------------------------------------------
def test_disconnect(sw: SignalWrapper):
	"""Vérifie la connexion d'un slot Python et émission immédiate."""
	received: List[Any] = []
	received2: List[Any] = []
	# --------------------------------------------------
	def slot(value):
		"""Mémorise la valeur reçue par le premier slot."""
		received.append(value)

	# --------------------------------------------------
	def slot2(value):
		"""Mémorise la valeur reçue par le second slot."""
		received2.append(value)
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


# --------------------------------------------------
@pytest.mark.parametrize("disconnect_all", [False, True], ids=["single-slot", "all-slots"])
@pytest.mark.parametrize("error", [TypeError, RuntimeError], ids=["already-disconnected", "destroyed-object"])
def test_disconnect_unavailable_signal(sw: SignalWrapper, monkeypatch, disconnect_all, error):
	"""Nettoie le registre des slots même lorsque Qt ne peut plus les déconnecter."""
	# Prépare un slot enregistré, puis simule un signal devenu indisponible.
	slot = Mock()
	sw.connect(slot)
	signal = Mock()
	signal.disconnect.side_effect = error("Signal unavailable")
	monkeypatch.setattr(sw, "_signal", signal)

	assert sw.disconnect(None if disconnect_all else slot) == 0
	assert sw._slots == []
	signal.disconnect.assert_called_once_with(slot)
	slot.assert_not_called()


# ==================================================
# endregion Connexion et déconnexion
# ==================================================

# ==================================================
# region Blocage des signaux
# ==================================================
def test_blocked_returns_context_manager_instance(sw: SignalWrapper):
	"""Vérifie que blocked() retourne bien un context manager du bon type (BlockCtx)."""
	ctx = sw.blocked()
	assert isinstance(ctx, SignalWrapper.BlockCtx)


# --------------------------------------------------
@pytest.mark.parametrize("values", [
		pytest.param(("A", "B", "C"), id="successive-values"),
		pytest.param(tuple(range(10)), id="repeated-overwrites")])
def test_block_simple_coalescence_last_value(sw: SignalWrapper, values):
	"""N'émet que la dernière valeur reçue pendant le blocage, quel que soit le nombre d'écrasements."""
	received: List[Any] = []
	sw.connect(lambda v: received.append(v))

	with sw.blocked():
		for value in values: sw.emit(value)

	assert received == [values[-1]]


# --------------------------------------------------
def test_block_without_emits_no_output(sw: SignalWrapper):
	"""Vérifie que si aucun emit() pendant le blocage : rien n'est émis à la sortie."""
	received: List[Any] = []
	sw.connect(lambda v: received.append(v))

	with sw.blocked():
		# Aucune émission
		pass

	assert received == []


# --------------------------------------------------
def test_nested_blocks_emit_once_at_outer_exit(sw: SignalWrapper):
	"""Vérifie que les blocages imbriqués : aucune émission avant le dernier __exit__."""
	received: List[Any] = []
	sw.connect(lambda v: received.append(v))

	with sw.blocked():
		with sw.blocked():
			sw.emit(1)
			sw.emit(2)
		# À ce stade, toujours rien
		assert received == []
		# Encore du bruit
		sw.emit(3)

	# Une seule émission à la fin, avec la dernière valeur (3)
	assert received == [3]


# --------------------------------------------------
def test_emit_default_none_coalesced(sw: SignalWrapper):
	"""Vérifie qu'un appel emit() sans valeur (None par défaut) pendant blocage → émis ensuite."""
	received: List[Any] = []
	sw.connect(lambda v: received.append(v))

	with sw.blocked(): sw.emit()

	assert received == [None]


# --------------------------------------------------
def test_block_flags_reset_after_flush(sw: SignalWrapper):
	"""Vérifie qu'après la sortie et l'émission coalescée, les drapeaux internes doivent être réinitialisés."""
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


# --------------------------------------------------
def test_block_without_emit(sw: SignalWrapper):
	"""Vérifie qu'après la sortie et l'émission coalescée, les drapeaux internes doivent être réinitialisés."""
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


# --------------------------------------------------
def test_emit_direct_after_previous_block(sw: SignalWrapper):
	"""Vérifie qu'après un blocage avec émission, un emit direct doit passer immédiatement (et ne pas être coalescé par un ancien état)."""
	received: List[Any] = []
	sw.connect(lambda v: received.append(v))

	with sw.blocked(): sw.emit("first")
	# Ici, on a reçu 'first' une fois
	assert received == ["first"]

	# Émission directe : doit s'ajouter immédiatement
	sw.emit("second")
	assert received == ["first", "second"]


# --------------------------------------------------
def test_internal_block_begin_end_paths(sw: SignalWrapper):
	"""Vérifie le scénario ``internal_block_begin_end_paths``."""
	received: List[Any] = []
	sw.connect(lambda v: received.append(v))

	# 1) _block_end() quand rien n'est bloqué : ne doit pas lever ni émettre
	sw._block_end()
	assert received == []

	# 2) begin/end sans pending : ne doit rien émettre
	sw._block_begin(True)
	sw._block_end()
	assert received == []


# ==================================================
# endregion Blocage des signaux
# ==================================================
