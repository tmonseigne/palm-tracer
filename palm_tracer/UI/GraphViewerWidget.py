"""
Fournit le widget de visualisation interactive des données PALM avec Plotly.

.. todo:: Avertir l'utilisateur avant l'affichage de plus de dix millions de points et permettre de mémoriser son choix.
"""

from __future__ import annotations

from pathlib import Path
from typing import cast

from qtpy.compat import isalive
from qtpy.QtCore import QEvent, QObject, Qt, QTimer
from qtpy.QtGui import QDropEvent, QHideEvent, QShowEvent
from qtpy.QtWidgets import QAbstractSpinBox, QApplication, QFrame, QGridLayout, QGroupBox, QHBoxLayout, QPushButton, QSplitter, QVBoxLayout, QWidget

from palm_tracer.PALMTracer import PALMTracer
from palm_tracer.Settings.Groups import Graph
from palm_tracer.Settings.Types import BaseSettingType, Combo, FileList, SpinInt
from palm_tracer.Tools import Ui
from palm_tracer.UI.BasePlotlyWidget import BasePlotlyWidget

# ==================================================
# region Constantes
# ==================================================
TIPS = {
		"Actualize": "Updates files/data from PALMTracer status.",
		"Export":    "Opens a dialog box and exports the figure according to the selected extension.",
		}


# ==================================================
# endregion Constantes
# ==================================================

##################################################
class GraphViewerWidget(BasePlotlyWidget):
	"""
	Affiche interactivement les graphiques associés aux données PALM.

	Le widget sélectionne une famille de données et une ou deux sources, délègue la construction des figures à :class:`~palm_tracer.Processing.Grapher.Grapher`
	et permet leur export en HTML, PNG ou PDF.

	:param palmtracer: Instance principale dont les données sont visualisées. La référence est conservée sans effectuer de copie.

	.. note:: Si QtWebEngine n'est pas disponible, le widget utilise un affichage textuel de remplacement.
	"""

	UI_NAME: str = "Graph Viewer"
	"""Nom de l'interface de visualisation des graphiques."""

	# ==================================================
	# region Initialisation
	# ==================================================
	##################################################
	def __init__(self, palmtracer: PALMTracer | None = None):
		"""
		Initialise le widget (UI, connexions, état initial) et lie PALMTracer.

		:param palmtracer: Instance principale :class:`~palm_tracer.PALMTracer` sans copie (référence partagée).
		"""
		super().__init__()
		self.setWindowTitle(self.UI_NAME)
		# Initialisation des membres
		self.pt = PALMTracer() if palmtracer is None else palmtracer
		self._graph_settings: Graph = self.pt.settings.graph
		self._drop_window: QWidget | None = None  # Fenêtre Qt dont les dépôts chargent une pile.
		self._drop_accepts: bool = False  # État des dépôts à restaurer lorsque le widget est masqué.

		# Construction UI
		self._init_ui()
		self._connect_signals()
		self._actualize()  # Actualisation des statuts et tracé initial

	##################################################
	def _init_ui(self):
		"""
		Construit l'interface utilisateur :
			- Colonne gauche :
				- Informations : Nom du fichier, présence Localizations/Tracking.
				- Domaine : 2 boutons exclusifs (Localization/Tracking).
				- Source : ComboBox dépendante du domaine sélectionné.
				- Filtres : Section réservée (non implémentée).
				- Actions : Actualize files / Export…
			- Zone droite :
				- QWebEngineView hébergeant la figure Plotly (ou fallback texte si indisponible).
		"""
		self.pt.clean_ui(self.UI_NAME)
		main_layout = QHBoxLayout(self)
		Ui.init_layout(main_layout)

		self.setStyleSheet("""QAbstractSpinBox { padding: 1px 10px; min-width: 10px; min-height: 18px; }
		QLineEdit { min-height: 20px; padding: 2px; }
		QComboBox { padding: 3px 10px 3px 8px; }""")

		# --- Séparateur redimensionnable ---
		splitter = QSplitter(Qt.Orientation.Horizontal, self)
		main_layout.addWidget(splitter)

		# --- Colonne gauche ---
		left = QFrame(self)
		left.setFrameShape(QFrame.Shape.StyledPanel)
		left.setMinimumWidth(300)
		vbox = QVBoxLayout(left)
		Ui.init_layout(vbox)
		scroll_content = QWidget()
		scroll_layout = QVBoxLayout(scroll_content)
		Ui.init_layout(scroll_layout)
		scroll_area = Ui.make_vertical_scroll(scroll_content)

		# --- Mise en page globale ---
		splitter.addWidget(left)
		splitter.addWidget(self._web)
		# La partie droite récupère l'espace supplémentaire.
		splitter.setStretchFactor(0, 0)
		splitter.setStretchFactor(1, 1)
		# Taille initiale de la colonne adaptée au contenu.
		self._splitter_resize_timer = QTimer(self)
		self._splitter_resize_timer.setSingleShot(True)
		self._splitter_resize_timer.timeout.connect(lambda: splitter.setSizes([max(left.sizeHint().width(), left.minimumWidth()), 1000]))
		self._splitter_resize_timer.start(0)

		# --- Bloc Source (donnée) + Type de graphe ---
		grp_source = QGroupBox("Source")
		form = Ui.make_form(grp_source)
		for key in self._graph_settings:
			if isinstance(self._graph_settings[key], BaseSettingType):
				self._graph_settings[key].get_ui(self.UI_NAME).attach_to_form(form)
				if isinstance(self._graph_settings[key], Combo):
					self._graph_settings[key].get_ui(self.UI_NAME).boxes[0].setMinimumWidth(200)

		# --- Bloc Affichage (2 colonnes) ---
		display_settings = self._graph_settings.display
		grp_display = QGroupBox("Display")
		grid = QGridLayout(grp_display)
		Ui.init_layout(grid)
		for i, key in enumerate(display_settings):
			row, col = i // 2, (i % 2) * 2
			ui = display_settings[key].get_ui(self.UI_NAME)
			if isinstance(display_settings[key], SpinInt): cast(QAbstractSpinBox, ui.boxes[0]).setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
			grid.addLayout(ui.layout, row, col)
			grid.addWidget(ui.label, row, col + 1)

		grid.setColumnStretch(1, 1)
		grid.setColumnStretch(3, 1)
		grid.setRowStretch(grid.rowCount(), 1)

		# --- Bloc Filtres ---
		grp_filters, vbox_filters = Ui.make_group(self, "Filters")
		# Integration des Filtres
		self._filters = self.pt.settings.filters
		self._filters_ui = self._filters.get_ui(self.UI_NAME)
		vbox_filters.addWidget(self._filters_ui.widget)
		# Masquage initial
		self._filters["Save"].get_ui(self.UI_NAME).hide()

		# --- Actions ---
		actions_row = QHBoxLayout()
		self._btn_actualize = QPushButton("Actualize files")
		self._btn_actualize.setToolTip(TIPS["Actualize"])
		self._btn_export = QPushButton("Export figure")
		self._btn_export.setToolTip(TIPS["Export"])
		actions_row.addStretch(1)
		actions_row.addWidget(self._btn_actualize)
		actions_row.addWidget(self._btn_export)

		# --- Mise en page dans le scroll ---
		scroll_layout.addWidget(self.pt.results.get_ui(self.UI_NAME).widget)
		scroll_layout.addWidget(grp_source)
		scroll_layout.addWidget(grp_display)
		scroll_layout.addWidget(grp_filters)
		scroll_layout.addStretch()  # Optionnel mais recommandé

		# --- Mise en page globale ---
		vbox.addWidget(scroll_area)
		vbox.addLayout(actions_row)

		# --- Affiche / masque les éléments en fonction des paramètres initiaux ---
		self._toggle_type(self._graph_settings["Type"].value)
		self._graph_settings.toggle_mode(self._graph_settings["Mode"].value)
		self._graph_settings.toggle_src()

	##################################################
	def _connect_signals(self):
		"""Connecte les signaux UI aux callbacks."""
		# Connexion des boutons Filters de cette UI
		self.pt.connect_filters_button(self.UI_NAME)

		# Sources
		self._graph_settings["Type"].connect(self._toggle_type)

		# Settings Connexion
		self._graph_settings.connect(self._update_plot)
		self._filters.connect_button(self._actualize, self.UI_NAME, "reset")
		self._filters.connect_button(self._actualize, self.UI_NAME, "update")

		# Action Row a supprimer
		self._btn_actualize.clicked.connect(self._actualize)
		self._btn_export.clicked.connect(self._on_export)

	##################################################
	def closeEvent(self, event):
		"""
		Nettoyage de l'UI des paramètres lors de la fermeture de la fenêtre.

		:param event: Événement de fermeture Qt.
		"""
		try: self.pt.clean_ui(self.UI_NAME)
		finally: super().closeEvent(event)

	# ==================================================
	# endregion Initialisation
	# ==================================================

	# ==================================================
	# region Glisser-déposer
	# ==================================================
	##################################################
	def showEvent(self, event: QShowEvent):
		"""
		Active l'interception dans la fenêtre autonome des graphiques.

		:param event: Événement d'affichage Qt.
		"""
		super().showEvent(event)
		if self._drop_window is not None and isalive(self._drop_window): return
		window = self
		self._drop_window = window
		self._drop_accepts = window.acceptDrops()
		window.setAcceptDrops(True)
		QApplication.instance().installEventFilter(self)

	##################################################
	def hideEvent(self, event: QHideEvent):
		"""
		Retire le filtre et restaure l'état des dépôts si la fenêtre Qt existe encore.

		:param event: Événement de masquage Qt.
		"""
		QApplication.instance().removeEventFilter(self)
		window = self._drop_window
		self._drop_window = None
		if window is not None and isalive(window): window.setAcceptDrops(self._drop_accepts)
		super().hideEvent(event)

	##################################################
	def eventFilter(self, watched: QObject, event: QEvent) -> bool:
		"""
		Intercepte le dépôt d'une seule pile locale dans la fenêtre des graphiques.

		Les dépôts multiples, les dossiers et les fichiers absents sont refusés.
		Les autres fenêtres et les glissements sans fichier local restent inchangés.

		:param watched: Objet Qt destinataire de l'événement.
		:param event: Événement à filtrer.
		:return: ``True`` si l'événement est consommé avant son traitement habituel.
		"""
		if event.type() not in (QEvent.Type.DragEnter, QEvent.Type.DragMove, QEvent.Type.Drop): return False
		window = self._drop_window
		if window is None or not isalive(window) or not isinstance(watched, QWidget): return False
		if watched is not window and not window.isAncestorOf(watched): return False
		drop = cast(QDropEvent, event)
		urls = drop.mimeData().urls()
		if not any(url.isLocalFile() for url in urls): return False
		if len(urls) != 1 or not Path(urls[0].toLocalFile()).is_file():
			drop.ignore()
			return True
		drop.setDropAction(Qt.DropAction.CopyAction)
		drop.accept()
		if event.type() == QEvent.Type.Drop: self._add_stack(urls[0].toLocalFile())
		return True

	# ==================================================
	# endregion Glisser-déposer
	# ==================================================

	# ==================================================
	# region Liaison avec PALMTracer
	# ==================================================
	##################################################
	def _toggle_type(self, btn_id: int):
		"""
		Met à jour la liste des sources et l'affichage des filtres.

		:param btn_id: Identifiant du bouton domaine sélectionné (0=Localization, 1=Tracking).
		"""
		if btn_id == 0: self._filters.show_part(self.UI_NAME, localization=True, tracking=False)  # Localisation
		else: self._filters.show_part(self.UI_NAME, localization=False, tracking=True)  # .			Tracking

	##################################################
	def _add_stack(self, path: str):
		"""
		Ajoute la pile déposée, charge ses derniers résultats et redessine le graphe.

		:param path: Chemin local de la pile à ajouter au Batch partagé avec le widget principal.
		"""
		cast(FileList, self.pt.settings.batch["Files"]).add_files([path])
		# Sans chemin explicite, load() utilise le premier dossier du Batch, pas celui de la pile déposée.
		self.pt.load(str(Path(path).with_suffix("")) + "_PALM_Tracer")
		self._actualize()  # Actualisation des statuts

	##################################################
	def _actualize(self):
		"""Actualise les statuts des fichiers/données depuis l'état PALMTracer et redessine le graph."""
		self._update_plot()  # Puis redessiner le graphe.

	##################################################
	def _update_plot(self):
		"""Construit la figure Plotly courante en fonction du domaine et de la source."""
		self._fig = self.pt.graph()
		self._update_web_widget()


##################################################
if __name__ == "__main__":
	import sys

	app = QApplication(sys.argv)
	w = GraphViewerWidget()
	w.resize(1280, 720)
	w.show()
	sys.exit(app.exec_())
