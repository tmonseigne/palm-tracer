"""
Fournit le widget Napari de visualisation haute résolution des résultats.

.. todo:: Avertir l'utilisateur avant l'affichage de plus de dix millions de points et permettre de mémoriser son choix.
"""

from __future__ import annotations

from pathlib import Path
from typing import cast

import napari
import numpy as np
from napari.utils.notifications import show_info, show_warning
from qtpy.QtWidgets import QApplication, QGroupBox, QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from palm_tracer.PALMTracer import PALMTracer
from palm_tracer.Settings.Groups import HR
from palm_tracer.Settings.Types import FileList
from palm_tracer.Tools import FileIO, Ui

# ==================================================
# region Constantes
# ==================================================
TIPS = {
		"Add Stack":  "Add a stack to the batch and load the latest results for it.\n"
					  "Please note that if you are coming from the main widget, the batch will be updated because the settings are linked.",

		"Actualize":  "Updates files/data from PALMTracer status.",
		"Generate":   "Generate HR Visualization.",
		"Save":       "Save the visualization generated.",
		"Screenshot": "Save the actual view of layers.",
		}


# ==================================================
# endregion Constantes
# ==================================================


class ViewerHRWidget(QWidget):
	"""
	Affiche les résultats PALM en haute résolution dans Napari.

	Le widget charge les résultats, configure la taille et la coloration des points, affiche les trajectoires et permet d'enregistrer la visualisation
	sous forme d'image PNG.

	:param viewer: Visionneuse Napari recevant les calques.
	:param palmtracer: Instance principale à laquelle le widget est associé.

	.. note:: Le widget peut être lancé avec la commande ``napari -w palm-tracer "Viewer HR"``.
	"""

	UI_NAME: str = "HR"
	"""Nom de l'interface de visualisation haute résolution."""
	LAYERS_NAME: list[str] = ["Visualization", "Points", "Tracks", "ROI Filter"]
	"""Noms des calques gérés par la visionneuse haute résolution."""

	# ==================================================
	# region Initialisation
	# ==================================================
	##################################################
	def __init__(self, viewer: napari.Viewer, palmtracer: PALMTracer | None = None):
		"""
		Initialise le widget et configure l'interface graphique (boutons, champs numériques, checkbox).

		La création du calque Napari se fait plus tard dans :meth:`update_layer` lorsqu'un fichier CSV est chargé.

		:param viewer: Viewer Napari cible.
		:param palmtracer: Instance PALMTracer à utiliser, ou :obj:`None` pour en créer une.
		"""
		super().__init__()
		self.viewer = viewer
		self._pt = PALMTracer() if palmtracer is None else palmtracer
		self._hr_settings: HR = self._pt.settings.hr
		self._filename: str = ""
		self._screenshot_filename: str = ""
		self.visualization: np.ndarray = np.zeros((1, 1, 1), dtype=np.uint16)

		self._layers = {self.LAYERS_NAME[0]: self.viewer.add_image(self.visualization, name=self.LAYERS_NAME[0]),
						self.LAYERS_NAME[1]: self.viewer.add_points(np.empty((0, 3), dtype=np.float32), name=self.LAYERS_NAME[1],
																	size=1, face_color="lime", visible=False),
						self.LAYERS_NAME[2]: self.viewer.add_tracks(np.array([[0, 0, 0, 0]], dtype=np.float32), name=self.LAYERS_NAME[2],
																	blending="translucent", visible=False),
						self.LAYERS_NAME[3]: self.viewer.add_shapes([], name=self.LAYERS_NAME[3], shape_type="polygon", edge_color="red",
																	edge_width=0.5, face_color="transparent")}

		for layer in self._layers.values(): layer.editable, layer.locked = False, True

		self._pt.settings.rois.layer_hr = self._layers[self.LAYERS_NAME[3]]  # Connexion du calque avec le manager.

		# Construction UI
		self._init_ui()
		self._connect_signals()
		self._actualize()

	##################################################

	def _init_ui(self):
		"""Construit l'interface utilisateur."""
		self._pt.settings.clean_ui(self.UI_NAME)

		self._widget = QWidget()

		layout = QVBoxLayout(self._widget)
		Ui.init_layout(layout, space=10)
		self.setLayout(layout)

		# --- Zone de scrolling ---
		scroll_content = QWidget()
		scroll_layout = QVBoxLayout(scroll_content)
		Ui.init_layout(scroll_layout, space=10)
		scroll_area = Ui.make_vertical_scroll(scroll_content)

		# --- Bouton pour charger une stack ---
		self._btn_add_stack = QPushButton("Add Stack")
		self._btn_add_stack.setToolTip(TIPS["Add Stack"])

		# --- Bloc Infos (lecture seule) ---
		grp_infos, self._status = Ui.make_file_info_group(margin=10)

		# --- Bloc Sources ---
		grp_source = QGroupBox("Source")
		ui = self._hr_settings.get_ui(self.UI_NAME)
		ui.body_layout.setContentsMargins(5, 15, 5, 5)
		grp_source.setLayout(ui.body_layout)
		self._hr_settings["Source"].get_ui(self.UI_NAME).boxes[0].setMinimumWidth(200)

		# --- Bloc Filtres ---
		grp_filters, vbox_filters = Ui.make_group(self, "Filters")
		# Integration des Filtres
		self._filters = self._pt.settings.filters
		self._filters_ui = self._filters.get_ui(self.UI_NAME)
		vbox_filters.addWidget(self._filters_ui.widget)
		# Masquage initial
		self._filters["Save"].get_ui(self.UI_NAME).hide()
		self._toggle_type(self._hr_settings["Type"].value)

		# --- Actions ---
		actions_row = QHBoxLayout()
		Ui.init_layout(actions_row)
		self._btn_actualize = QPushButton("Actualize")
		self._btn_actualize.setToolTip(TIPS["Actualize"])
		self._btn_generate = QPushButton("Generate")
		self._btn_generate.setToolTip(TIPS["Generate"])
		self._btn_save = QPushButton("Save")
		self._btn_save.setToolTip(TIPS["Save"])
		self._btn_screenshot = QPushButton("Screenshot")
		self._btn_screenshot.setToolTip(TIPS["Screenshot"])
		# actions_row.addStretch(1)  # permet d'aligner à droite
		actions_row.addWidget(self._btn_actualize)
		actions_row.addWidget(self._btn_generate)
		actions_row.addWidget(self._btn_save)
		actions_row.addWidget(self._btn_screenshot)

		# --- Mise en page dans le scroll ---
		scroll_layout.addWidget(grp_infos)
		scroll_layout.addWidget(grp_source)
		scroll_layout.addWidget(grp_filters)
		scroll_layout.addStretch()  # Optionnel, mais recommandé

		# --- Mise en page globbale ---
		layout.addWidget(self._btn_add_stack)
		layout.addWidget(scroll_area)
		layout.addLayout(actions_row)

	##################################################
	def _connect_signals(self):
		"""Connecte les signaux UI aux callbacks."""

		# Connexion des boutons Filters de cette UI
		self._pt.connect_filters_button(self.UI_NAME)

		self._btn_add_stack.clicked.connect(self._add_stack)
		self._hr_settings["Type"].connect(self._toggle_type)

		# Action Row
		self._btn_actualize.clicked.connect(self._actualize)
		self._btn_generate.clicked.connect(self._generate)
		self._btn_save.clicked.connect(self._save)
		self._btn_screenshot.clicked.connect(self._screenshot)

	##################################################
	def closeEvent(self, event):
		"""
		Nettoyage de l'UI des paramètres lors de la fermeture de la fenêtre.

		:param event: Événement de fermeture Qt.
		"""
		try: self._pt.settings.clean_ui(self.UI_NAME)
		finally: super().closeEvent(event)

	# ==================================================
	# endregion Initialisation
	# ==================================================

	# ==================================================
	# region Liaison avec PALMTracer
	# ==================================================
	##################################################
	def _check_beads(self):
		"""
		Affiche ou masque les élements liés aux billes si des données sont présentes ou non.
		Uniquement dans cette interface, l'interface principale conserve toutes les options si les billes sont calculées en cours de route.
		"""
		s_list = ["Remove Beads", "Drift Correction", "Smooth Drift"]
		if self._pt.beads.empty:
			for s in s_list: self._hr_settings[s].get_ui(self.UI_NAME).hide()
		else:
			for s in s_list: self._hr_settings[s].get_ui(self.UI_NAME).show()

	##################################################
	def _add_stack(self):
		"""Permet le chargement d'une image tif pour bypass le chargement initial en lien avec le wiget principal."""
		cast(FileList, self._pt.settings.batch["Files"]).add_file()
		self._pt.load()  # .	Chargement des derniers résultats
		self._actualize()  # Actualisation des statuts

	##################################################
	def _actualize(self):
		"""Actualise les statuts des fichiers/données depuis l'état PALMTracer."""
		file = cast(FileList, self._pt.settings.batch["Files"]).current_text
		self._status["File"].setText(Path(file).name if file else "No File")
		# Mise à jour des Status
		status = self._pt.get_status()
		for key in status: self._status[key].setText(status[key])
		self._check_beads()

	##################################################
	def _save(self):
		"""Créé une image PNG de la visualisation actuelle."""
		if self._filename:
			crop = self._pt.crop(self.visualization)
			if self._filename[-3:] == "png": FileIO.save_png(crop, self._filename, False)
			else: FileIO.save_tif(crop, self._filename)
			show_info("Image file saved successfully.")

	##################################################
	def _screenshot(self):  # pragma: no cover — Accès au canevas
		"""Créé une image PNG de l'aperçu de la visualisation actuelle (avec les régalges de color map, contraste."""
		if self._screenshot_filename:
			self.viewer.screenshot(self._screenshot_filename, canvas_only=True)
			show_info("Screenshot saved successfully.")

	##################################################
	def _toggle_type(self, btn_id: int):
		"""
		Met à jour la liste des sources et l'affichage des filtres.

		:param btn_id: Identifiant du bouton domaine sélectionné (0=Localization, 1=Tracking).
		"""
		if btn_id == 0: self._filters.show_part(self.UI_NAME, localization=True, tracking=False)  # Localisation
		else: self._filters.show_part(self.UI_NAME, localization=False, tracking=True)  # Tracking

	# ==================================================
	# endregion Liaison avec PALMTracer
	# ==================================================

	# ==================================================
	# region Dessin
	# ==================================================
	##################################################
	def _generate(self):
		"""Crée ou mets à jour le calque de points/trajectoires HR l'image de visualisation dans le viewer Napari."""
		self._filename = ""
		path, stack, suffix = self._pt.path, self._pt.stack, self._pt.suffix

		if stack is None or not path or not Path(path).is_dir():
			show_warning(f"No stack processed loaded.")
			return

		self.visualization, plot_data = self._pt.hr()
		if self.visualization.size <= 1:
			show_warning("No visualization available.")
			return

		# Changement des noms
		self._filename = str(self._pt.output_viz_name())
		self._screenshot_filename = f"{path}/screenshot-{suffix}-{FileIO.get_timestamp_for_files()}.png"

		# Mise à jour de la ROI qui a été utilisé
		self._pt.settings.rois.update_hr_box()

		if self._hr_settings["Type"].value == 0:  # Localisations
			self._layers[self.LAYERS_NAME[1]].data = plot_data
			self._layers[self.LAYERS_NAME[1]].face_color = "lime"
			self._layers[self.LAYERS_NAME[2]].visible = False
		else:  # Trajectoires
			self._layers[self.LAYERS_NAME[2]].data = plot_data
			self._layers[self.LAYERS_NAME[2]].blending = "translucent"
			self._layers[self.LAYERS_NAME[1]].visible = False

		self._layers[self.LAYERS_NAME[0]].data = self.visualization[np.newaxis, ...] if self.visualization.ndim == 2 else self.visualization
		self._layers[self.LAYERS_NAME[0]].visible = True
		self._pt.settings.rois.update_hr()
		self.viewer.reset_view()  # Recentrer et ajuster la vue


##################################################
def create_viewerhr(palmtracer: PALMTracer | None = None) -> tuple[napari.Viewer, QWidget]:
	"""
	Crée une nouvelle fenêtre Napari HR, sans menu, et y ajoute le ViewerHRWidget docké à droite.

	Cette fonction NE lance PAS napari.run() : elle est faite pour être appelée depuis un plugin, donc dans une appli Qt déjà active.

	:param palmtracer: Instance PALMTracer à utiliser, ou :obj:`None` pour en créer une.
	:return: Visionneuse Napari créée et widget haute résolution associé.
	"""
	if palmtracer is None: palmtracer = PALMTracer()
	viewer = napari.Viewer(ndisplay=2)  # .									 Crée le viewer HR napari
	viewer.title = "HR Viewer"  # .											 Modifier le titre de la fenêtre
	viewer.window.main_menu.setVisible(False)  # .							 Cacher la barre de menu
	widget = ViewerHRWidget(viewer, palmtracer)  # .						 Crée le widget en lui passant le viewer
	viewer.window.add_dock_widget(widget, name="Viewer HR", area="right")  # L'ajoute comme dock widget dans la fenêtre napari
	return viewer, widget


##################################################
def open_viewerhr(_viewer: "napari.viewer.Viewer" = None, ) -> QWidget:
	"""
	Callable utilisé par Napari pour le menu Plugins > PALM Tracer > Viewer HR.

	- Ignore le viewer courant.
	- Crée une nouvelle fenêtre Napari HR dédiée.
	- Retourne un QWidget stub (caché) juste pour satisfaire
	  l'API "widget plugin" de Napari.

	:param _viewer: Visionneuse Napari courante, volontairement ignorée.
	:return: Widget factice masqué attendu par l'API des plugins Napari.
	"""
	# Crée la nouvelle fenêtre HR
	create_viewerhr()

	# Stub minimal pour Napari (sera docké, mais caché)
	stub = QWidget()
	stub.hide()
	return stub


##################################################
if __name__ == "__main__":
	import napari

	app = QApplication.instance() or QApplication([])
	_v, _w = create_viewerhr()
	napari.run()  # Lance la boucle Qt gérée par Napari
