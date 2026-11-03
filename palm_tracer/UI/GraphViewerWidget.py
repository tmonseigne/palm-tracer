"""Fournit le widget de visualisation interactive des données PALM avec Plotly."""

from __future__ import annotations

from pathlib import Path
from typing import cast

from qtpy.QtCore import Qt, QTimer
from qtpy.QtWidgets import QApplication, QFrame, QGridLayout, QGroupBox, QHBoxLayout, QPushButton, QSpinBox, QSplitter, QVBoxLayout, QWidget

from palm_tracer.PALMTracer import PALMTracer
from palm_tracer.Settings.Groups import Graph
from palm_tracer.Settings.Types import BaseSettingType, Combo, FileList, SpinInt
from palm_tracer.Tools import FileIO, Ui
from palm_tracer.UI.BasePlotlyWidget import BasePlotlyWidget
from palm_tracer.UI.Napari import get_current_palmtracer

# ==================================================
# region Constantes
# ==================================================
TIPS = {
		"Export":    "Opens a dialog box and exports the figure according to the selected extension.",
		}


# ==================================================
# endregion Constantes
# ==================================================

# --------------------------------------------------
class GraphViewerWidget(BasePlotlyWidget):
	"""
	Affiche interactivement les graphiques associés aux données PALM.

	Le widget sélectionne une famille de données et une ou deux sources, délègue la construction des figures à :class:`~palm_tracer.Processing.Grapher.Grapher`
	et permet leur export en HTML, PNG ou PDF.

	:param palmtracer: Instance principale dont les données sont visualisées. La référence est conservée sans effectuer de copie.

	.. note:: Si QtWebEngine n'est pas disponible, le widget utilise un affichage textuel de remplacement.

	.. todo:: Avertir l'utilisateur avant l'affichage de plus de dix millions de points et permettre de mémoriser son choix.
	"""

	UI_NAME: str = "Graph Viewer"
	"""Nom de l'interface de visualisation des graphiques."""
	DROP_MULTIPLE: bool = False
	"""Limite le dépôt à une seule pile."""
	DROP_EXTENSIONS: tuple[str, ...] = FileIO.STACK_EXTENSIONS
	"""Extensions des piles dont les résultats peuvent être chargés."""

	# ==================================================
	# region Initialisation
	# ==================================================
	def __init__(self, palmtracer: PALMTracer | None = None):
		"""
		Initialise le widget (UI, connexions, état initial) et lie PALMTracer.

		:param palmtracer: Instance principale :class:`~palm_tracer.PALMTracer` sans copie (référence partagée).
		"""
		super().__init__(palmtracer=palmtracer)
		# Initialisation des membres
		self._graph_settings: Graph = self.pt.settings.graph

		# Construction UI
		self._init_ui()
		self._connect_signals()
		self._actualize()  # Actualisation des statuts et tracé initial

	# --------------------------------------------------
	def _init_ui(self):
		"""
		Construit les panneaux de paramètres et de visualisation.

		Le panneau gauche regroupe les informations, les sources, l’affichage, les filtres et l’export.
		Le panneau droit héberge la figure Plotly, ou un affichage textuel si QtWebEngine est indisponible.
		"""
		self.pt.clean_ui(self.UI_NAME)
		main_layout = QHBoxLayout(self)
		Ui.init_layout(main_layout)

		# --- Séparateur redimensionnable ---
		splitter = QSplitter(Qt.Orientation.Horizontal, self)
		main_layout.addWidget(splitter)

		# --- Colonne gauche ---
		left = QFrame(self)
		left.setFrameShape(QFrame.Shape.StyledPanel)
		left.setMinimumWidth(self.LEFT_PANEL_MINIMUM_WIDTH)
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
			setting = self._graph_settings[key]
			if isinstance(setting, BaseSettingType):
				setting.get_ui(self.UI_NAME).attach_to_form(form)
				if isinstance(setting, Combo):
					setting.get_ui(self.UI_NAME).boxes[0].setMinimumWidth(200)

		# --- Bloc Affichage (2 colonnes) ---
		display_settings = self._graph_settings.display
		grp_display = QGroupBox("Display")
		grid = QGridLayout(grp_display)
		Ui.init_layout(grid)
		for i, key in enumerate(display_settings):
			row, col = i // 2, (i % 2) * 2
			display_setting = cast(BaseSettingType, display_settings[key])
			ui = display_setting.get_ui(self.UI_NAME)
			if isinstance(display_setting, SpinInt): Ui.set_spin_buttons(cast(QSpinBox, ui.boxes[0]), False)
			grid.addLayout(ui.layout, row, col)
			grid.addWidget(ui.label, row, col + 1)

		grid.setColumnStretch(1, 1)
		grid.setColumnStretch(3, 1)
		grid.setRowStretch(grid.rowCount(), 1)

		# --- Bloc Filtres ---
		grp_filters, vbox_filters = Ui.make_group(self, "Filters")
		# Intégration des Filtres
		self._filters = self.pt.settings.filters
		self._filters_ui = self._filters.get_ui(self.UI_NAME)
		vbox_filters.addWidget(self._filters_ui.widget)
		# Masquage initial
		self._filters["Save"].get_ui(self.UI_NAME).hide()

		# --- Actions ---
		actions_row = QHBoxLayout()
		self._btn_export = QPushButton("Export figure")
		self._btn_export.setToolTip(TIPS["Export"])
		actions_row.addStretch(1)
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

	# --------------------------------------------------
	def _connect_signals(self):
		"""Connecte les signaux UI aux callbacks."""
		# Connexion des boutons Filters de cette UI
		self.pt.connect_filters_button(self.UI_NAME)

		# Sources
		self._graph_settings["Type"].connect(self._toggle_type)

		# Settings Connexion
		self._graph_settings.connect(self._actualize)
		self.pt.results.connect(self._actualize)

		# Export
		self._btn_export.clicked.connect(self._on_export)

	# --------------------------------------------------
	def closeEvent(self, event):
		"""
		Nettoyage de l'UI des paramètres lors de la fermeture de la fenêtre.

		:param event: Événement de fermeture Qt.
		"""
		self._graph_settings.disconnect(self._actualize)
		self.pt.results.disconnect(self._actualize)
		try: self.pt.clean_ui(self.UI_NAME)
		finally: super().closeEvent(event)

	# ==================================================
	# endregion Initialisation
	# ==================================================

	# ==================================================
	# region Glisser-déposer
	# ==================================================
	def _drop_files(self, paths: list[str]):
		"""
		Charge la pile unique acceptée par le filtre commun.

		:param paths: Liste contenant le chemin local de la pile déposée.
		"""
		self._add_stack(paths[0])

	# ==================================================
	# endregion Glisser-déposer
	# ==================================================

	# ==================================================
	# region Liaison avec PALMTracer
	# ==================================================
	def _toggle_type(self, btn_id: int):
		"""
		Met à jour la liste des sources et l'affichage des filtres.

		:param btn_id: Identifiant du bouton domaine sélectionné (0=Localization, 1=Tracking).
		"""
		if btn_id == 0: self._filters.show_part(self.UI_NAME, localization=True, tracking=False)  # Localisation
		else: self._filters.show_part(self.UI_NAME, localization=False, tracking=True)  # .			Tracking

	# --------------------------------------------------
	def _add_stack(self, path: str):
		"""
		Ajoute la pile déposée, charge ses derniers résultats et redessine le graphe.

		:param path: Chemin local de la pile à ajouter au Batch partagé avec le widget principal.
		"""
		with self.pt.results.signal_blocked():
			cast(FileList, self.pt.settings.batch["Files"]).add_files([path])
			# Sans chemin explicite, load() utilise le premier dossier du Batch, pas celui de la pile déposée.
			self.pt.load(str(Path(path).with_suffix("")) + "_PALM_Tracer")

	# --------------------------------------------------
	def _actualize(self):
		"""Reconstruit le graphique à partir des paramètres et des résultats courants."""
		self._update_plot()  # Puis redessiner le graphe.

	# --------------------------------------------------
	def _update_plot(self):
		"""Construit la figure Plotly courante en fonction du domaine et de la source."""
		self._fig = self.pt.graph()
		self._update_web_widget()


# --------------------------------------------------
def open_graphviewer():  # pragma: no cover — Aucun lancement de fenêtre sans contrôle en CI
	"""Ouvre le Graph Viewer autonome avec l'instance du widget principal dans la fenêtre Napari active."""
	widget = GraphViewerWidget(palmtracer=get_current_palmtracer())
	widget.show_standalone()


# --------------------------------------------------
if __name__ == "__main__":
	import sys

	app = QApplication(sys.argv)
	w = GraphViewerWidget()
	w.show_standalone()
	sys.exit(app.exec_())
