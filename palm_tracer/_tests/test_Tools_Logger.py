"""Teste l'enregistrement du journal d'activité."""

from palm_tracer._tests.Utils import *
from palm_tracer.Tools import Logger

LOG_PATH = OUTPUT_DIR / "test_logger.log"


##################################################
def test_logger(capsys):
	"""Vérifie le logger."""
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


##################################################
def test_logger_bad_use(capsys):
	"""Vérifie l'une mauvaise utilisation du Logger."""
	logger = Logger()
	logger.close()
	logger.add("Message without logger open.")

	lines = get_lines_output(capsys)
	assert len(lines) == 2
	assert re.fullmatch(TS_PATTERN + r"\sMessage without logger open\.", lines[0])
	assert re.fullmatch(TS_PATTERN + r"\sNo log file open for writing\.", lines[1])


##################################################
def test_logger_with_use(capsys):
	"""Vérifie l'une mauvaise utilisation du Logger."""
	with Logger() as logger:
		logger.open(LOG_PATH)
		logger.add("Message")

	lines = get_lines_output(capsys)
	assert len(lines) == 3
	assert re.fullmatch(TS_PATTERN + rf"\sLog opened : {re.escape(str(LOG_PATH))}", lines[0])
	assert re.fullmatch(TS_PATTERN + rf"\sMessage", lines[1])
	assert re.fullmatch(TS_PATTERN + rf"\sLog closed : {re.escape(str(LOG_PATH))}", lines[2])
