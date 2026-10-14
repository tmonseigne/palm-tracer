"""Teste le widget de migration des anciens résultats Metamorph."""

from qtpy.QtCore import Qt

from palm_tracer.UI.FileMigratorWidget import FileMigratorWidget  # Classe
from tests.Utils import *
from tests.Utils import strip_ansi


# ==================================================
# region Initialisation
# ==================================================
def test_widget_creation(qtbot):
	"""Vérifie la création du widget."""
	w = FileMigratorWidget()
	qtbot.addWidget(w)
	w.resize(500, 250)
	w.show()
	qtbot.waitExposed(w)
	w.close()


# ==================================================
# endregion Initialisation
# ==================================================

# ==================================================
# region Fonctions de rappel
# ==================================================
def test_bad_load(qtbot, capsys, monkeypatch, fake_qfiledialog):
	"""Vérifie la gestion des erreurs avec la boîte de dialogue d'ouverture de fichier."""
	w = FileMigratorWidget()
	qtbot.addWidget(w)
	w.resize(500, 250)
	w.show()
	qtbot.waitExposed(w)

	# Simuler un "Cancel" sur le QFileDialog
	fake_qfiledialog(FileMigratorWidget, None)
	qtbot.mouseClick(w._btn_load_folder, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "No folder selected." in lines[-1]

	# Bad file Input
	fake_qfiledialog(FileMigratorWidget, "bad folder")
	qtbot.mouseClick(w._btn_load_folder, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Unable to read the folder" in lines[-1]

	w.close()


# --------------------------------------------------
def test_migrate(qtbot, capsys, monkeypatch, fake_qfiledialog, copy_input):
	"""Vérifie le lancement de la migration depuis le widget."""
	# Préparation d'une copie temporaire des anciens résultats et affichage du widget.
	input_folder = copy_input("stack.PT")
	w = FileMigratorWidget()
	qtbot.addWidget(w)
	w.resize(500, 250)
	w.show()
	qtbot.waitExposed(w)

	# Sélection du dossier temporaire contenant les anciens résultats.
	fake_qfiledialog(FileMigratorWidget, str(input_folder))
	qtbot.mouseClick(w._btn_load_folder, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Folder loaded successfully." in lines[-1]

	# Lancement de la migration depuis l'interface et vérification du message de succès.
	qtbot.mouseClick(w._btn_migrate, Qt.MouseButton.LeftButton)
	lines = get_lines_output(capsys)
	assert "Migration successful." in lines[-1]


	w.close()


# --------------------------------------------------
def test_migrate_error(qtbot, capsys, monkeypatch):
	"""Signale une migration impossible sans afficher de message de succès."""
	w = FileMigratorWidget()
	qtbot.addWidget(w)

	# Simule l'échec de l'écriture lors du lancement de la migration.
	def fail_migrate():
		"""Simule une erreur d'écriture des résultats migrés."""
		raise OSError("Output unavailable")

	monkeypatch.setattr(w._fm, "migrate", fail_migrate)
	w._on_migrate()
	output = strip_ansi(capsys.readouterr().out)
	assert "Error during migration: Output unavailable." in output
	assert "Migration successful." not in output


# ==================================================
# endregion Fonctions de rappel
# ==================================================
