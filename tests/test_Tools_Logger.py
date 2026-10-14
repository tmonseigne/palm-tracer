"""Teste l'enregistrement du journal d'activité."""

from unittest.mock import Mock

import pytest

from palm_tracer.Tools import Logger
from tests.Utils import *
from tests.Utils import strip_ansi

LOG_PATH = OUTPUT_DIR / "test_logger.log"


# --------------------------------------------------
def test_logger(capsys):
	"""Enchaîne ouverture, écritures et fermeture en vérifiant chaque message horodaté."""
	logger = Logger()
	logger.open(LOG_PATH)
	logger.add("First message")
	logger.add("")
	logger.add("after blank")
	logger.close()

	lines = get_lines_output(capsys)
	assert len(lines) == 5
	assert re.fullmatch(TS_PATTERN + rf"\sLog opened : {re.escape(str(LOG_PATH))}", lines[0])
	assert re.fullmatch(TS_PATTERN + r"\sFirst message", lines[1])
	assert re.fullmatch(TS_PATTERN + r"\s*", lines[2])  # re.fullmatch(TS_PATTERN + r"\s*", l) ligne vide timestampée
	assert re.fullmatch(TS_PATTERN + r"\safter blank", lines[3])
	assert re.fullmatch(TS_PATTERN + rf"\sLog closed : {re.escape(str(LOG_PATH))}", lines[4])


# --------------------------------------------------
def test_logger_reopen(tmp_path, capsys):
	"""Ferme le premier fichier avant d'ouvrir un second journal avec la même instance."""
	logger = Logger()
	first, second = tmp_path / "first.log", tmp_path / "second.log"
	# Première ouverture, puis réutilisation du logger avec un autre fichier.
	logger.open(first)
	first_handle = logger.file_handle
	try:
		logger.open(second)
		assert first_handle.closed
		assert logger.filename == str(second)
		logger.add("Second journal")
	finally: logger.close()
	assert "Second journal" not in first.read_text(encoding="utf-8")
	assert "Second journal" in second.read_text(encoding="utf-8")
	assert f"Log closed : {first}" in capsys.readouterr().out


# --------------------------------------------------
def test_logger_open_error(tmp_path, capsys):
	"""Remet le logger dans un état fermé si le dossier du fichier n'existe pas."""
	logger = Logger()
	path = tmp_path / "missing" / "test.log"
	logger.open(path)
	assert not logger._isopen
	assert logger.file_handle is None
	assert not path.exists()
	assert f"Error opening file {path}" in strip_ansi(capsys.readouterr().out)


# --------------------------------------------------
@pytest.mark.parametrize("operation", ["write", "flush", "close"], ids=["write-failed", "flush-failed", "close-failed"])
def test_logger_close_error(capsys, operation):
	"""Restaure l'état fermé même lorsqu'une étape de fermeture du journal échoue."""
	logger = Logger()
	handle = Mock()
	handle.fileno.side_effect = OSError("No file descriptor")
	getattr(handle, operation).side_effect = OSError("File locked")
	logger.filename, logger.file_handle, logger._isopen = "test.log", handle, True
	logger.close()
	assert logger.filename == ""
	assert logger.file_handle is None
	assert not logger._isopen
	assert "Error closing file test.log : File locked" in strip_ansi(capsys.readouterr().out)
	# Une seconde fermeture doit rester silencieuse après l'échec.
	logger.close()
	assert capsys.readouterr().out == ""


# --------------------------------------------------
def test_logger_bad_use(capsys):
	"""Ferme un logger déjà fermé puis vérifie l'avertissement d'écriture sans fichier ouvert."""
	logger = Logger()
	logger.close()
	logger.add("Message without logger open.")

	lines = get_lines_output(capsys)
	assert len(lines) == 2
	assert re.fullmatch(TS_PATTERN + r"\sMessage without logger open\.", lines[0])
	assert re.fullmatch(TS_PATTERN + r"\sNo log file open for writing\.", lines[1])


# --------------------------------------------------
@pytest.mark.parametrize("operation", ["write", "flush"], ids=["write-failed", "flush-failed"])
def test_logger_add_error(capsys, operation):
	"""Signale une écriture impossible sans perdre le handle du journal ouvert."""
	logger = Logger()
	handle = Mock()
	getattr(handle, operation).side_effect = OSError("Disk full")
	logger.filename, logger.file_handle, logger._isopen = "test.log", handle, True
	try:
		logger.add("Message")
		assert logger.file_handle is handle
		assert logger._isopen
		assert "Error writing to file test.log : Disk full" in strip_ansi(capsys.readouterr().out)
	finally:
		# Le faux handle ne correspond à aucun fichier réel à fermer.
		logger.file_handle, logger._isopen = None, False


# --------------------------------------------------
def test_logger_with_use(capsys):
	"""Vérifie la fermeture automatique du journal à la sortie du gestionnaire de contexte."""
	with Logger() as logger:
		logger.open(LOG_PATH)
		logger.add("Message")

	lines = get_lines_output(capsys)
	assert len(lines) == 3
	assert re.fullmatch(TS_PATTERN + rf"\sLog opened : {re.escape(str(LOG_PATH))}", lines[0])
	assert re.fullmatch(TS_PATTERN + r"\sMessage", lines[1])
	assert re.fullmatch(TS_PATTERN + rf"\sLog closed : {re.escape(str(LOG_PATH))}", lines[2])
