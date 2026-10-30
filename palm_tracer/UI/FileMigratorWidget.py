"""Fournit le widget de migration des anciens résultats Metamorph."""

from __future__ import annotations

from pathlib import Path

from qtpy.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget

from palm_tracer.PALMTracer import PALMTracer
from palm_tracer.Tools import FileDialog, FileMigrator, Ui
from palm_tracer.UI.BaseWidget import BaseWidget
from palm_tracer.UI.Napari import get_current_palmtracer


class FileMigratorWidget(BaseWidget):
	"""
	Fournit l'interface de migration des anciens dossiers de résultats Metamorph.

	:param parent: Widget Qt parent.
	:param palmtracer: Instance partagée, ou :obj:`None` pour en créer une.
	"""

	UI_NAME: str = "File Migrator Tool"
	"""Nom de l'interface de migration."""
	DROP_MULTIPLE: bool = False
	"""Limite le dépôt à un dossier de résultats."""
	DROP_DIRECTORIES: bool = True
	"""Autorise le dépôt du dossier Metamorph à analyser."""

	# ==================================================
	# region Initialisation
	# ==================================================
	def __init__(self, parent: QWidget | None = None, palmtracer: PALMTracer | None = None):
		"""
		Construit le widget et initialise l'interface.

		:param parent: Widget parent Qt, ou :obj:`None` si widget racine.
		:param palmtracer: Instance partagée, ou :obj:`None` pour en créer une.
		"""
		super().__init__(parent, palmtracer)

		self._fm: FileMigrator = FileMigrator()

		self._init_ui()
		self._connect_signals()

	# --------------------------------------------------
	def _init_ui(self):
		"""Construit l'interface utilisateur (onglets + boutons) en conservant un style proche du Graph Viewer."""
		main_layout = QVBoxLayout(self)
		Ui.init_layout(main_layout)

		self._btn_load_folder = QPushButton("Load folder")
		self._btn_load_folder.setToolTip("Folder must be a PALMTracer analysis result in Metamorph and ends with .PT.")

		self._lbl_load_folder = Ui.make_path_label("No folder loaded")

		self._btn_migrate = QPushButton("Migrate")
		self._btn_migrate.setToolTip("Start migration to the actual format.")

		self._filelist: dict[str, dict[str, QLabel]] = {
				"loc":    {"label": QLabel("Localization:"), "value": QLabel("--")},
				"trc":    {"label": QLabel("Tracking:"), "value": QLabel("--")},
				"MSD":    {"label": QLabel("Tracking MSD:"), "value": QLabel("--")},
				"InD":    {"label": QLabel("Tracking Instant Diffusion:"), "value": QLabel("--")},
				"Fit":    {"label": QLabel("Tracking Fit"), "value": QLabel("--")},
				"A3D":    {"label": QLabel("Astigmatism 3D Model:"), "value": QLabel("--")},
				"Unused": {"label": QLabel("Unused files:"), "value": QLabel("--")}}

		main_layout.addWidget(self._btn_load_folder)
		main_layout.addWidget(self._lbl_load_folder)
		main_layout.addLayout(Ui.make_info_grid(self._filelist, "Files", 2), stretch=1)
		main_layout.addWidget(self._btn_migrate)
		main_layout.addStretch(1)

	# --------------------------------------------------
	def _connect_signals(self):
		"""Connecte les signaux aux callbacks."""
		self._btn_load_folder.clicked.connect(self._on_load_folder)
		self._btn_migrate.clicked.connect(self._on_migrate)

	# ==================================================
	# endregion Initialisation
	# ==================================================

	# ==================================================
	# region Fonctions de rappel
	# ==================================================
	def _drop_files(self, paths: list[str]):
		"""
		Charge le dossier de résultats déposé sans lancer sa migration.

		:param paths: Liste contenant le chemin du dossier Metamorph.
		"""
		if len(paths) != 1 or not Path(paths[0]).is_dir():
			self.notify_warning("Drop one Metamorph result folder (.PT).")
			return
		self._load_folder(paths[0])

	# --------------------------------------------------
	def _update_filelist(self):
		"""Mise à jour de la liste des fichiers."""
		for key, item in self._fm.files.items():
			if key != "Unused": self._filelist[key]["value"].setText("--" if len(item) == 0 else item[0].name)
			else: self._filelist[key]["value"].setText("--" if len(item) == 0 else "\n".join(n.name for n in item))

	# --------------------------------------------------
	def _on_load_folder(self):
		"""Callback du bouton 'Load folder'."""
		# --- boîte de dialogue pour sélectionner un dossier ---
		folder = FileDialog.open_directory(self, "Select folder")

		if not folder:
			self.notify_warning("No folder selected.")
			return
		self._load_folder(folder)

	# --------------------------------------------------
	def _load_folder(self, folder: str):
		"""
		Analyse le dossier choisi par dialogue ou déposé et actualise la liste des fichiers.

		:param folder: Chemin local du dossier de résultats Metamorph.
		"""

		# --- lecture du dossier ---
		try:
			path = Path(folder)
			self._fm.open(path)
			self._fm.analyze()
			self._update_filelist()
		except Exception as e:
			self.notify_error(f"Unable to read the folder : {e}.")
			return

		# --- mise à jour du label associé au bouton ---
		Ui.update_path_label(self._lbl_load_folder, path)

		self.notify_success("Folder loaded successfully.")

	# --------------------------------------------------
	def _on_migrate(self):
		"""Callback du bouton 'Migrate'."""
		try:
			self._fm.migrate()
		except Exception as e:
			self.notify_error(f"Error during migration: {e}.")
			return
		self.notify_success("Migration successful.")


# --------------------------------------------------
def open_migrator():  # pragma: no cover — Aucun lancement de fenêtre sans contrôle en CI
	"""
	Ouvre la fenêtre de l'outil de migration en mode autonome.

	Cette fonction est utilisée par le plugin Napari comme point d'entrée :
	elle crée un :class:`FileMigratorWidget` et l'affiche dans une fenêtre autonome dont la référence est gérée par la base commune.
	"""
	widget = FileMigratorWidget(palmtracer=get_current_palmtracer())
	widget.show_standalone(500, 250)


# --------------------------------------------------
if __name__ == "__main__":
	import sys

	app = QApplication(sys.argv)
	w = FileMigratorWidget()
	w.show_standalone(500, 250)
	sys.exit(app.exec_())
