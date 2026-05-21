"""
Module contenant la classe :class:`FileMigratorWidget`, un outil minimaliste pour la gestion de l'ancien format de fichier Metamoprh.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from qtpy.QtWidgets import QApplication, QFileDialog, QLabel, QPushButton, QVBoxLayout, QWidget

from palm_tracer.Tools import FileMigrator, Ui

_windows = []  # pour garder une référence globale, éviter le Garbage Collector


class FileMigratorWidget(QWidget):
	"""Widget minimaliste pour la gestion de l'ancien format de fichier Metamoprh."""

	# ==================================================
	# region Initialization
	# ==================================================
	##################################################
	def __init__(self, parent: Optional[QWidget] = None):
		"""
		Construit le widget et initialise l'interface.

		:param parent: Widget parent Qt, ou :obj:`None` si widget racine.
		"""
		super().__init__(parent)
		self.setWindowTitle("File Migrator Tool")

		self._fm: FileMigrator = FileMigrator()

		self._init_ui()
		self._connect_signals()
		self.setStyleSheet(Ui.STYLESHEET_GENERAL)  # On applique un style général

	##################################################
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

	##################################################
	def _connect_signals(self):
		"""Connecte les signaux aux callbacks."""
		self._btn_load_folder.clicked.connect(self._on_load_folder)
		self._btn_migrate.clicked.connect(self._on_migrate)

	# ==================================================
	# endregion Initialization
	# ==================================================

	# ==================================================
	# region Callbacks
	# ==================================================
	##################################################
	def _update_filelist(self):
		"""Mise à jour de la liste des fichiers."""
		for key, item in self._fm.files.items():
			if key != "Unused": self._filelist[key]["value"].setText("--" if len(item) == 0 else item[0].name)
			else: self._filelist[key]["value"].setText("--" if len(item) == 0 else "\n".join(n.name for n in item))

	##################################################
	def _on_load_folder(self):
		"""Callback du bouton 'Load folder'."""
		# --- boîte de dialogue pour sélectionner un dossier ---
		folder = QFileDialog.getExistingDirectory(self, "Select folder", "")

		if not folder:
			Ui.print_warning("No folder selected.")
			return

		# --- lecture du dossier ---
		try:
			folder = Path(folder)
			self._fm.open(folder)
			self._fm.analyze()
			self._update_filelist()
		except Exception as e:
			Ui.print_error(f"Unable to read the folder : {e}.")
			return

		# --- mise à jour du label associé au bouton ---
		Ui.update_path_label(self._lbl_load_folder, folder)

		print(f"Folder loaded successfully.")

	##################################################
	def _on_migrate(self):
		"""Callback du bouton 'Migrate'."""
		try:
			self._fm.migrate()
		except Exception as e:
			Ui.print_error(f"Error during migration: {e}.")
			return
		Ui.print_success("Migration successfull.")


##################################################
def open_migrator():  # pragma: no cover — Aucun lancement de fenêtre sans controle en CI
	"""
	Ouvre la fenêtre de l'outil de migration en mode autonome.

	Cette fonction est utilisée par le plugin Napari comme point d'entrée :
	elle crée simplement un :class:`FileMigratorWidget`, l'affiche et le renvoie. Le widget ne dépend pas de Napari et s'ouvre dans sa propre fenêtre.
	"""
	widget = FileMigratorWidget()
	widget.resize(500, 250)
	widget.show()
	_windows.append(widget)  # éviter que Python le détruise en le stockant


##################################################
if __name__ == "__main__":
	import sys

	app = QApplication(sys.argv)
	w = FileMigratorWidget()
	w.resize(500, 250)
	w.show()
	sys.exit(app.exec_())
