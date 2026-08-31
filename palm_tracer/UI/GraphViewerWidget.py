"""
Fournit le widget de visualisation interactive des données PALM avec Plotly.

.. todo:: Avertir l'utilisateur avant l'affichage de plus de dix millions de points et permettre de mémoriser son choix.
"""

from __future__ import annotations

from typing import cast

from qtpy.QtCore import Qt, QTimer
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
		"Add Stack": "Add a stack to the batch and load the latest results for it.\n"
					 "Please note that if you are coming from the main widget, the batch will be updated because the settings are linked.",

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
		self._pt = PALMTracer() if palmtracer is None else palmtracer
		self._graph_settings: Graph = self._pt.settings.graph

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
		self._pt.clean_ui(self.UI_NAME)
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

		# --- Bouton pour charger une stack ---
		self._btn_add_stack = QPushButton("Add Stack")
		self._btn_add_stack.setToolTip(TIPS["Add Stack"])

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
		self._filters = self._pt.settings.filters
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
		scroll_layout.addWidget(self._pt.results.get_ui(self.UI_NAME).widget)
		scroll_layout.addWidget(grp_source)
		scroll_layout.addWidget(grp_display)
		scroll_layout.addWidget(grp_filters)
		scroll_layout.addStretch()  # Optionnel mais recommandé

		# --- Mise en page globbale ---
		vbox.addWidget(self._btn_add_stack)
		vbox.addWidget(scroll_area)
		vbox.addLayout(actions_row)

		# --- Affiche / masque les éléments en fonction des paramètres initiaux ---
		self._toggle_type(self._graph_settings["Type"].value)
		self._graph_settings["Display"]["Limits"].value = True
		self._graph_settings.toggle_dual(self._graph_settings["Dual"].value)
		self._graph_settings.toggle_src()

	##################################################
	def _connect_signals(self):
		"""Connecte les signaux UI aux callbacks."""
		# Connexion des boutons Filters de cette UI
		self._pt.connect_filters_button(self.UI_NAME)

		self._btn_add_stack.clicked.connect(self._add_stack)

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
		try: self._pt.clean_ui(self.UI_NAME)
		finally: super().closeEvent(event)

	# ==================================================
	# endregion Initialisation
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
	def _add_stack(self):
		"""Permet le chargement d'une image tif pour bypass le chargement initial en lien avec le wiget principal."""
		cast(FileList, self._pt.settings.batch["Files"]).add_file()
		self._pt.load()  # . Chargement des derniers résultats
		self._actualize()  # Actualisation des statuts

	##################################################
	def _actualize(self):
		"""Actualise les statuts des fichiers/données depuis l'état PALMTracer et redessine le graph."""
		self._graph_settings["Display"]["Limits"].value = True
		self._update_plot()  # Puis redessiner le graphe.

	##################################################
	def _update_plot(self):
		"""Construit la figure Plotly courante en fonction du domaine et de la source."""
		self._fig = self._pt.graph()
		self._update_web_widget()


##################################################
if __name__ == "__main__":
	import sys

	app = QApplication(sys.argv)
	w = GraphViewerWidget()
	w.resize(1280, 720)
	w.show()
	sys.exit(app.exec_())
