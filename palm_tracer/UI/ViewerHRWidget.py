"""
Widget d'affichage Haute Résolution pour Napari permettant de charger un dossier de résultats et de visualiser les points.

Ce widget ajoute dans le dock de Napari :
	- un bouton de chargement du dossier,
	- trois champs pour contrôler les paramètres de visualisation Haute Résolution,
	- un calque Napari Points/trajectoires mis à jour dynamiquement.
	- Un boutotn pour sauvegarder une image PNG résultat
"""
from pathlib import Path
from typing import cast

import napari
import numpy as np
from napari.utils.notifications import show_info, show_warning
from qtpy.QtWidgets import QApplication, QFileDialog, QGroupBox, QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from palm_tracer.PALMTracer import PALMTracer
from palm_tracer.Processing.Visualization import render_hr_image, render_tracks_image
from palm_tracer.Settings.Groups import Filtering
from palm_tracer.Settings.Groups.VisualizationHR import HR_LOC_SOURCE, HR_TRC_SOURCE
from palm_tracer.Settings.Types import CheckBox, Combo, FileList, SpinInt
from palm_tracer.Tools import FileIO, Ui

# ==================================================
# region Constantes
# ==================================================
DATA_SRC: dict[str, list] = {
		"Localization": ["Count", "X", "Y", "Z", "Integrated Intensity",
						 "Sigma X", "Sigma Y", "Circularity", "Theta", "Surface", "MSE XY", "MSE Z"],
		"Tracking":     ["Length"],
		}

TIPS = {
		"Add Stack":       "Add a stack to the batch and load the latest results for it.\n"
						   "Please note that if you are coming from the main widget, the batch will be updated because the settings are linked.",

		"Source":          "Data selected for Graph.",
		"Gaussian":        "",
		"Fixed Intensity": "",

		"Actualize":       "Updates files/data from PALMTracer status.",
		"Generate":        "Generate HR Visualization.",
		"Save":            "Opens a dialog box and save the visualization generated.",
		}


# ==================================================
# endregion Constantes
# ==================================================


class ViewerHRWidget(QWidget):
	"""
	Widget d'affichage HR pour un viewer Napari.

	Ce widget permet :
		- de charger un dossier,
		- de modifier la taille des points
		- de modifier le facteur d'agrandissement
		- de sélectionner la source d'information permettant la coloration des points
		- de créer ou mettre à jour un calque de type :class:`napari.layers.Points` ou :class:`napari.layers.Tracks`.
		- de sauvegarder une image PNG résultat de la visualisation.

	**Remarque** : peut être lancé directement avec la commande ``napari -w palm-tracer "Viewer HR"``

	:param viewer: Instance du viewer Napari où sera ajouté le calque HR.
	:param palmtracer: Instance PALMTracer à lier.
	"""

	# ==================================================
	# region Initialisation
	# ==================================================
	##################################################
	def __init__(self, viewer: napari.Viewer, palmtracer: PALMTracer):
		"""
		Initialise le widget et configure l'interface graphique (boutons, champs numériques, checkbox).

		La création du calque Napari se fait plus tard dans :meth:`update_layer` lorsqu'un fichier CSV est chargé.

		:param viewer: Viewer Napari cible.
		"""
		super().__init__()
		self.viewer = viewer
		self._pt = palmtracer
		self._file: str = ""
		self.visualization: np.ndarray = np.zeros((1, 1), dtype=np.uint16)

		# Construction UI
		self._init_ui()
		self._connect_signals()
		self._on_source_changed(0)  # Change la source pour Localization à l'origine

	##################################################
	def _init_ui(self):
		"""
		Construit l'interface utilisateur :
				- Informations : Nom du fichier, présence Localizations/Tracking.
				- Domaine : 3 boutons exclusifs (Stack/Localization/Tracking).
				- Source : ComboBox dépendante du domaine sélectionné.
				- Filtres : Section réservée (non implémentée).
				- Actions : Actualize files / Export…
		"""
		self._widget = QWidget()
		layout = QVBoxLayout(self._widget)
		Ui.init_layout(layout, space=10)
		self.setLayout(layout)

		# --- Boutton pour charger une stack ---
		self._btn_add_stack = QPushButton("Add Stack")
		self._btn_add_stack.setToolTip(TIPS["Add Stack"])

		# --- Bloc Infos (lecture seule) ---
		grp_infos, self._status = Ui.make_file_info_group(margin=10)

		# --- Bloc Sources ---
		grp_source = QGroupBox("Source")

		h, self._btg_src, self._btn_src = Ui.make_exclusive_btn_group(["Localization", "Tracks"])

		form = Ui.make_form(grp_source)
		Ui.init_layout(form, margin=10)
		form.addRow(h)
		# Combo box
		self._cmb_src = Combo("Source", TIPS["Source"])
		self._cmb_src.box.setMinimumWidth(200)
		self._cmb_src.attach_to_form(form)

		self._gaussian = CheckBox("Gaussian", TIPS["Gaussian"])
		self._gaussian.attach_to_form(form)

		self._fix = CheckBox("Fixed Intensity", TIPS["Fixed Intensity"])
		self._fix.attach_to_form(form)

		self.upscale_spin = SpinInt("Upscale Ratio", "", 4, [1, 100], 2)
		self.upscale_spin.attach_to_form(form)

		# --- Bloc Filtres ---
		grp_filters, vbox_filters = Ui.make_group(self, "Filters", margin=10)
		# Integration des Filtres
		self._filters = Filtering()
		self._filters.update_from_dict(self._pt.settings.filtering.to_dict())
		vbox_filters.addWidget(self._filters.widget)
		# Masquage initial
		self._filters["Save"].hide()
		self._filters["Localization"].remove_header()
		self._filters["Tracks"].remove_header()
		self._filters["Tracks"].hide()

		# --- Actions ---
		actions_row = QHBoxLayout()
		Ui.init_layout(actions_row)
		self._btn_actualize = QPushButton("Actualize files")
		self._btn_actualize.setToolTip(TIPS["Actualize"])
		self._btn_generate = QPushButton("Generate")
		self._btn_generate.setToolTip(TIPS["Generate"])
		self._btn_save = QPushButton("Save")
		self._btn_save.setToolTip(TIPS["Save"])
		actions_row.addStretch(1)  # permet d'aligner à droite
		actions_row.addWidget(self._btn_actualize)
		actions_row.addWidget(self._btn_generate)
		actions_row.addWidget(self._btn_save)

		layout.addWidget(self._btn_add_stack)
		layout.addWidget(grp_infos)
		layout.addWidget(grp_source)
		layout.addWidget(grp_filters)
		layout.addLayout(actions_row)

	##################################################
	def _connect_signals(self):
		"""Connecte les signaux UI aux callbacks."""
		self._btn_add_stack.clicked.connect(self._add_stack)

		# Sources
		self._btg_src.idClicked.connect(self._on_source_changed)

		# Filters
		self._filters.buttons["reset"].clicked.connect(self._reset_filtered)
		self._filters.buttons["update"].clicked.connect(self._update_filtered)
		self._filters.buttons["save"].clicked.connect(self._pt.save_filtered)

		# Action Row
		self._btn_actualize.clicked.connect(self._actualize)
		self._btn_generate.clicked.connect(self._generate)
		self._btn_save.clicked.connect(self._save)

	# ==================================================
	# endregion Initialisation
	# ==================================================

	# ==================================================
	# region UI Callback
	# ==================================================
	##################################################
	def _update_status(self):
		"""Mets à jour les status des fichiers."""
		self._file = (cast(FileList, self._pt.settings.batch["Files"]).get_selected())
		self._status["File"].setText(Path(self._file).name if self._file else "No File")
		status = self._pt.get_status()
		for key in status: self._status[key].setText(status[key])

	##################################################
	def _on_source_changed(self, btn_id: int):
		"""
		Mets à jour la liste des sources selon le domaine choisi puis redessine.

		:param btn_id: Identifiant du bouton domaine sélectionné (0=Stack, 1=Localization, 2=Tracking).
		"""
		self._is_updating = True
		# Remplir la ComboBox 'Source' en fonction du domaine
		if btn_id == 0: src = DATA_SRC["Localization"]  # Stack
		else: src = self._get_tracks_src()  # .			  Tracking
		with self._cmb_src.signal_blocked(): self._cmb_src.update_box(src)
		self._update_filters_ui()  # .					  Mise à jour des filtres à afficher
		self._is_updating = False

	##################################################
	def _update_filters_ui(self):
		"""
		Mets à jour les filtres à afficher.
		Selon la source, les filtres ne seront pas les mêmes (pour ne pas surcharger l'interface de filtres inutiles).
		"""
		if self._btg_src.checkedId() == 0:  # Localizations
			self._filters["Localization"].show()
			self._filters["Tracks"].hide()
		else:  # .							  Tracking
			self._filters["Localization"].hide()
			self._filters["Tracks"].show()

	##################################################
	def _get_tracks_src(self) -> list[str]:
		"""
		Génère la liste des variables d'intérêt pour les Trajectoires en fonction des fichiers disponibles.

		:return: La liste des sources disponibles pour les trajectoires.
		"""
		res = list(DATA_SRC["Tracking"])
		if not self._pt.df["MSD"].empty: res += ["MSD"]
		if not self._pt.df["InD"].empty: res += ["Instant D"]
		if not self._pt.df["Fit"].empty: res += self._pt.df["Fit"].columns[2:].tolist()
		return res

	# ==================================================
	# endregion UI Callback
	# ==================================================

	# ==================================================
	# region PALMTracer Link
	# ==================================================
	##################################################
	def _add_stack(self):
		"""Permet le chargement d'une image tif pour bypass le chargement initial en lien avec le wiget principal."""
		cast(FileList, self._pt.settings.batch["Files"]).add_file()
		self._pt.load()  # . Chargement des derniers résultats
		self._actualize()

	##################################################
	def _actualize(self):
		"""
		Actualise les fichiers/données depuis l'état PALMTracer :
			- Mets à jour les libellés d'information et l'état d'activation des boutons de domaine.

		En cas d'erreur de lecture, logue l'erreur via :func:`palm_tracer.Tools.Ui.print_error`.
		"""
		with self._filters.signal_blocked(), self._pt.settings.signal_blocked():
			self._filters.update_from_dict(self._pt.settings.filtering.to_dict())
			# Métadonnées d'information
			self._update_status()
			if self._file != "":
				z, y, x = self._pt.stack.shape
				self._filters.update_limits(x, y, z)

	##################################################
	def _reset_filtered(self):
		"""Supprime les dataframes de filtre."""
		with self._filters.signal_blocked(), self._pt.settings.signal_blocked():
			self._pt.reset_filtered()  # Nettoyage des dataframes filtrés
			self._filters.reset()

	##################################################
	def _update_filtered(self):
		"""Applique les filtres sur les dataframes."""
		with self._filters.signal_blocked(), self._pt.settings.signal_blocked():
			self._pt.settings.filtering.update_from_dict(self._filters.to_dict())
			self._pt.update_filtered()  # Mise à jour des filtres

	##################################################
	def _save(self):
		"""Créé une image PNG de la visualisation actuelle."""
		return
		if self._filename:
			FileIO.save_png(self.visualization, self._filename)
			show_info("Saving the image file.")

	# ==================================================
	# endregion PALMTracer Link
	# ==================================================

	# ==================================================
	# region Drawing
	# ==================================================
	##################################################
	def _generate(self):
		"""Crée ou mets à jour le calque de points/trajectoires HR l'image de visualisation dans le viewer Napari."""
		path, stack, suffix = self._pt.path, self._pt.stack, self._pt.suffix
		if not path or not Path(path).is_dir():
			show_warning(f"The destination path '{path}' is invalid.")
			return

		if stack is None:
			show_warning(f"No stack loaded.")
			return

		depth, height, width = stack.shape

		# On supprime les calques (la mise à jour n'est pas optimale sous Napari).
		try: self.viewer.layers.clear()
		except Exception as e: show_warning(f"Error when deleting old layers: {e}")

		data_type = self.type_cmb.value
		data_source = self.source_cmb.value
		upscale = self.upscale_spin.value
		point_size = self.size_spin.value
		color = self.color_cmb.items[self.color_cmb.value]

		if data_type == 0:  # Localisations
			loc = self._pt.localizations
			if loc.empty:
				show_warning("No localization file available.")
				return
			points = loc[["Y", "X"]].to_numpy() * upscale
			layer = self.viewer.add_points(points, size=point_size, face_color="lime", name="Points")

			src = HR_LOC_SOURCE[data_source + 1]
			self.visualization = render_hr_image(width, height, upscale, loc[["X", "Y", src]].to_numpy())

		else:  # Trajectoires
			trc = self._pt.tracks
			if trc.empty:
				show_warning("No tracking file available.")
				return
			tracks_data = trc[["Track", "Plane", "Y", "X"]].to_numpy(dtype=float)
			tracks_data[:, 2:4] *= upscale
			layer = self.viewer.add_tracks(tracks_data, name="Tracks", blending="translucent")

			src = HR_TRC_SOURCE[data_source + 1]
			trc = self._pt.add_color_to_tracks(trc, src)
			trc.to_csv(f"{path}/tracking_hr_color-{suffix}.csv", index=False)
			self.visualization = render_tracks_image(width, height, upscale, trc)

		layer.editable = False
		if color != "grayscale": self.visualization = FileIO.grayscale_to_color(self.visualization, color)
		self._filename = f"{path}/visualization_{data_type}_x{upscale}_{src}-{suffix}.png"
		layer = self.viewer.add_image(self.visualization, name="Visualization", visible=False)
		self.viewer.layers.move(self.viewer.layers.index(layer), 0)


##################################################
def create_viewerhr(palmtracer: PALMTracer | None = None) -> napari.Viewer:  # pragma: no cover — Aucun lancement de fenêtre sans controle en CI
	"""
	Crée une nouvelle fenêtre Napari HR, sans menu,
	et y ajoute le ViewerHRWidget docké à droite.

	Cette fonction NE lance PAS napari.run() : elle est faite
	pour être appelée depuis un plugin, donc dans une appli Qt déjà active.
	"""
	if palmtracer is None: palmtracer = PALMTracer()
	viewer = napari.Viewer(ndisplay=2)  # .									 Crée le viewer HR napari
	viewer.title = "HR Viewer"  # .											 Modifier le titre de la fenêtre
	viewer.window.main_menu.setVisible(False)  # .							 Cacher la barre de menu
	widget = ViewerHRWidget(viewer, palmtracer)  # .						 Crée le widget en lui passant le viewer
	viewer.window.add_dock_widget(widget, name="Viewer HR", area="right")  # L'ajoute comme dock widget dans la fenêtre napari
	return viewer


##################################################
def open_viewerhr(_viewer: "napari.viewer.Viewer" = None, ) -> QWidget:  # pragma: no cover — Aucun lancement de fenêtre sans controle en CI
	"""
	Callable utilisé par Napari pour le menu Plugins > PALM Tracer > Viewer HR.

	- Ignore le viewer courant.
	- Crée une nouvelle fenêtre Napari HR dédiée.
	- Retourne un QWidget stub (caché) juste pour satisfaire
	  l'API "widget plugin" de Napari.
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
	_v = create_viewerhr()
	napari.run()  # Lance la boucle Qt gérée par Napari
