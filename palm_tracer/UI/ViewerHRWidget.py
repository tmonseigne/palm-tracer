"""
Widget d'affichage Haute Résolution pour Napari permettant de charger un dossier de résultats et de visualiser les points.

Ce widget ajoute dans le dock de Napari :
	- un bouton de chargement du dossier,
	- trois champs pour contrôler les paramètres de visualisation Haute Résolution,
	- un calque Napari Points/trajectoires mis à jour dynamiquement.
	- Un boutotn pour sauvegarder une image PNG résultat

.. todo:: Warning si plus de 10 millions de points sur un affichage (avec option se souvenir du choix).
"""
from pathlib import Path
from typing import cast

import napari
import numpy as np
import pandas as pd
from napari.utils.notifications import show_info, show_warning
from qtpy.QtWidgets import QApplication, QGroupBox, QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from palm_tracer.PALMTracer import PALMTracer
from palm_tracer.Processing import Drift, Renderer
from palm_tracer.Settings.Groups import Filtering
from palm_tracer.Settings.Types import CheckBox, Combo, FileList, SpinFloat, SpinInt
from palm_tracer.Tools import FileIO, Ui

# ==================================================
# region Constantes
# ==================================================
DATA_SRC: dict[str, list] = {
		"Localization": ["Count", "X", "Y", "Z", "Integrated Intensity",
						 "Sigma X", "Sigma Y", "Circularity", "Theta", "Surface", "MSE XY", "MSE Z"],
		"Tracking":     ["Track Number", "Plane", "Intensity", "Duration", "Length"]
		}

TIPS = {
		"Add Stack":         "Add a stack to the batch and load the latest results for it.\n"
							 "Please note that if you are coming from the main widget, the batch will be updated because the settings are linked.",

		"Source":            "Data selected for Graph.",
		"Color Mode":        "When overlapping, select whether the pixel values are added together or whether only the maximum value is retained.",
		"Gaussian":          "Displays a Gaussian distribution for each location.",
		"G Intensity":       "Integrated intensity of the Gaussian curve if 'Fixed Intensity' is selected; otherwise, "
							 "the ratio by which the value selected in the source will be divided",
		"G Fixed Intensity": "Ensures that each point has the same intensity.",
		"G Shape":           "Defines the shape of the Gaussian distribution (Isotropic, Anisotropic, or Fixed Size, "
							 "so that each point has the same isotropic shape)",
		"G Size":            "The standard deviation of the Gaussian distribution if “Fixed Size” is selected.",
		"Upscale Ratio":     "Image upscale ratio",
		"Drift Correction":  "Apply a drift correction (Note: The beads must have been extracted before.)",
		"Auto Crop":         "Remove all black Frame around reconstruction (Usefull when you make reconstruciton on a part of field). Keep 5 pixel of margin",

		"Actualize":         "Updates files/data from PALMTracer status.",
		"Generate":          "Generate HR Visualization.",
		"Save":              "Save the visualization generated.",
		"Screenshot":        "Save the actual view of layers.",
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
		self._renderer = Renderer()
		self._file: str = ""
		self._filename: str = ""
		self._screenshot_filename: str = ""
		self.visualization: np.ndarray = np.zeros((1, 1), dtype=np.uint16)

		# Construction UI
		self._init_ui()
		self._connect_signals()
		self._on_source_changed(0)  # Change la source pour Localization à l'origine
		self._actualize()

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
		form = Ui.make_form(grp_source)
		Ui.init_layout(form, margin=10)

		h, self._btg_src, self._btn_src = Ui.make_exclusive_btn_group(["Localization", "Tracks"])

		self._cmb_src = Combo("Source", TIPS["Source"])
		self._cmb_src.box.setMinimumWidth(200)
		self._color_mode = Combo("Color mode", TIPS["Color Mode"], 0, ["Addition", "Max"])
		self._upscale = SpinInt("Upscale Ratio", TIPS["Upscale Ratio"], 4, [1, 100], 2)
		self._drift = CheckBox("Drift Correction", TIPS["Drift Correction"])
		self._auto_crop = CheckBox("Auto Crop", TIPS["Auto Crop"], True)
		self._gaussian = CheckBox("Gaussian", TIPS["Gaussian"])
		self._gauss_intensity = SpinInt("Intensity", TIPS["G Intensity"], 100, [1, 10000], 10)
		self._gauss_fixed_intensity = CheckBox("Fixed Intensity", TIPS["G Fixed Intensity"])
		self._gauss_shape = Combo("Shape", TIPS["G Shape"], 0, ["Fixed Size", "Isotrope", "Anisotrope"])
		self._gauss_shape_size = SpinFloat("Size", TIPS["G Size"], 1, [0, 10], 0.01, 3)

		form.addRow(h)
		self._cmb_src.attach_to_form(form)
		self._color_mode.attach_to_form(form)
		self._gaussian.attach_to_form(form)
		self._gauss_intensity.attach_to_form(form)
		self._gauss_fixed_intensity.attach_to_form(form)
		self._gauss_shape.attach_to_form(form)
		self._gauss_shape_size.attach_to_form(form)
		self._upscale.attach_to_form(form)
		self._drift.attach_to_form(form)
		self._auto_crop.attach_to_form(form)

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

		layout.addWidget(self._btn_add_stack)
		layout.addWidget(grp_infos)
		layout.addWidget(grp_source)
		layout.addWidget(grp_filters)
		layout.addLayout(actions_row)

		self._toggle_gaussian()

	##################################################
	def _connect_signals(self):
		"""Connecte les signaux UI aux callbacks."""
		self._btn_add_stack.clicked.connect(self._add_stack)

		# Sources
		self._btg_src.idClicked.connect(self._on_source_changed)
		self._gaussian.connect(self._toggle_gaussian)

		# Filters
		self._filters.buttons["reset"].clicked.connect(self._reset_filtered)
		self._filters.buttons["update"].clicked.connect(self._update_filtered)
		self._filters.buttons["save"].clicked.connect(self._pt.save_filtered)

		# Action Row
		self._btn_actualize.clicked.connect(self._actualize)
		self._btn_generate.clicked.connect(self._generate)
		self._btn_save.clicked.connect(self._save)
		self._btn_screenshot.clicked.connect(self._screenshot)

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
		# Remplir la ComboBox 'Source' en fonction du domaine
		if btn_id == 0:  # .		Stack
			src = DATA_SRC["Localization"]
			self._color_mode.show()
			self._gaussian.show()
		else:  # .					Tracking
			src = DATA_SRC["Tracking"]
			self._color_mode.hide()
			self._gaussian.value = False
			self._gaussian.hide()
		with self._cmb_src.signal_blocked(): self._cmb_src.update_box(src)
		self._update_filters_ui()  # Mise à jour des filtres à afficher

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
	def _toggle_gaussian(self):
		"""Montre ou cache les options réservées à la visualisation gaussienne."""
		if self._gaussian.value:
			self._gauss_intensity.show()
			self._gauss_fixed_intensity.show()
			self._gauss_shape.show()
			self._gauss_shape_size.show()
		else:
			self._gauss_intensity.hide()
			self._gauss_fixed_intensity.hide()
			self._gauss_shape.hide()
			self._gauss_shape_size.hide()

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
		"""
		with self._filters.signal_blocked(), self._pt.settings.signal_blocked():
			self._filters.update_from_dict(self._pt.settings.filtering.to_dict())
			# Métadonnées d'information
			self._update_status()
			if self._pt.stack is not None:
				z, y, x = self._pt.stack.shape
				self._filters.update_limits(x, y, z)

	##################################################
	def _reset_filtered(self):
		"""Supprime les dataframes de filtre."""
		with self._filters.signal_blocked(), self._pt.settings.signal_blocked():
			self._pt.reset_filtered()  # Nettoyage des dataframes filtrés
			self._filters.reset()
			self._update_status()

	##################################################
	def _update_filtered(self):
		"""Applique les filtres sur les dataframes."""
		with self._filters.signal_blocked(), self._pt.settings.signal_blocked():
			self._pt.settings.filtering.update_from_dict(self._filters.to_dict())
			self._pt.update_filtered()  # Mise à jour des filtres
			self._update_status()

	##################################################
	def _save(self):
		"""Créé une image PNG de la visualisation actuelle."""
		if self._filename:
			FileIO.save_png(self._crop(), self._filename)
			show_info("Image file saved successfully.")

	##################################################
	def _screenshot(self):  # pragma: no cover — Accès au canvas
		"""Créé une image PNG de la visualisation actuelle."""
		if self._screenshot_filename:
			self.viewer.screenshot(self._screenshot_filename, canvas_only=True)
			show_info("Screenshot saved successfully.")

	# ==================================================
	# endregion PALMTracer Link
	# ==================================================

	# ==================================================
	# region Drawing
	# ==================================================
	##################################################
	def _correct_drift(self, data: pd.DataFrame) -> pd.DataFrame:
		"""
		Vérifie si la correciton de drift est activé, faisable et l'applique.

		:param data:
		:return:
		"""
		if self._drift.value:  # Drift activé
			beads = self._pt.beads
			if beads.empty:  # Billes non calculées / trouvées
				show_warning("No beads file available to correct drift.")
				return data
			# Application de la correction de drift
			drift = Drift.get_drift(beads, is_3d=False)
			smooth = Drift.median_filter_centered(drift[["X", "Y", "Z"]].to_numpy())
			drift[["X", "Y", "Z"]] = smooth
			return Drift.remove_drift(data, drift, is_3d=False)
		return data

	##################################################
	def _crop(self, margin: int = 5) -> np.ndarray:
		"""
		Recadre automatiquement l'image en supprimant les zones nulles autour,
		avec une marge configurable.

		:param margin: Nombre de pixels à conserver autour de la zone utile.
		:return: Image recadrée.
		"""
		if not self._auto_crop.value: return self.visualization
		img = self.visualization

		# --- Masque des pixels non nuls ---
		mask = img != 0
		if not np.any(mask): return np.zeros((1, 1), dtype=img.dtype)  # Si tout est noir

		# --- Indices min/max ---
		rows, cols = np.any(mask, axis=1), np.any(mask, axis=0)  # Projection sur les axes
		y_min, y_max = np.where(rows)[0][[0, -1]]
		x_min, x_max = np.where(cols)[0][[0, -1]]

		# --- Ajout marge (avec clamp) ---
		y_min, y_max = max(0, y_min - margin), min(img.shape[0] - 1, y_max + margin)
		x_min, x_max = max(0, x_min - margin), min(img.shape[1] - 1, x_max + margin)

		return img[y_min:y_max + 1, x_min:x_max + 1]  # Crop

	##################################################
	def _generate(self):
		"""Crée ou mets à jour le calque de points/trajectoires HR l'image de visualisation dans le viewer Napari."""
		self._filename = ""
		path, stack, suffix = self._pt.path, self._pt.stack, self._pt.suffix

		if stack is None or not path or not Path(path).is_dir():
			show_warning(f"No stack processed loaded.")
			return

		depth, height, width = stack.shape

		# On supprime les calques (la mise à jour n'est pas optimale sous Napari).
		try: self.viewer.layers.clear()
		except Exception as e: show_warning(f"Error when deleting old layers: {e}")
		self.visualization = np.zeros((1, 1), dtype=np.uint16)  # Remise à 0 du calque de visualisation

		src_id = self._btg_src.checkedId()
		src = self._cmb_src.current_text
		upscale = self._upscale.value
		self._renderer.set_size(width, height, upscale)

		if src_id == 0:  # Localisations
			loc = self._correct_drift(self._pt.localizations)
			if loc.empty:
				show_warning("No localization file available.")
				return
			loc = self._renderer.add_colors_to_localizations(loc, src)

			# Calque de points (attention n'envoyer que X et Y (la couleur n'est pas à mettre ici) et dans le sens Y, X
			plot_data = loc[["Y", "X"]].to_numpy() * upscale
			layer = self.viewer.add_points(plot_data, size=1, face_color="lime", name="Localizations", visible=False)

			# Visualisation
			plot_data = loc[["X", "Y", "Color", "Sigma X", "Sigma Y", "Theta"]].to_numpy(dtype=np.float64)
			if self._gaussian.value:
				gaussian = {
						"Intensity":       self._gauss_intensity.value,
						"Fixed Intensity": self._gauss_fixed_intensity.value,
						"Shape":           self._gauss_shape.value,
						"Size":            self._gauss_shape_size.value
						}
			else: gaussian = None
			color_mode = 0 if src == "Count" else self._color_mode.value  # Si count, on est forcément en mode cumulatif, sinon on voit l'option.
			self.visualization = self._renderer.localizations(plot_data, color_mode, gaussian)

		else:  # Trajectoires
			trc = self._correct_drift(self._pt.tracks)
			if trc.empty:
				show_warning("No tracking file available.")
				return

			trc = self._renderer.add_colors_to_tracks(trc, src)
			trc = trc[["Track", "Plane", "X", "Y", "Color"]].to_numpy(dtype=np.float64)
			# Calque de points (attention n'envoyer que Tracks, Plane, Y et X (la couleur n'est pas à mettre ici).
			plot_data = trc[:, [0, 1, 3, 2]]
			plot_data[:, [2, 3]] *= upscale
			layer = self.viewer.add_tracks(plot_data, name="Tracks", blending="translucent", visible=False)
			# Visualisation (attention n'envoyer que Tracks, X, Y, Couleur (le plan ne sert plus).
			self.visualization = self._renderer.tracks(trc[:, [0, 2, 3, 4]])

		layer.editable = False
		filename_drift = '_corrected' if self._drift.value else ''
		suffix = f"{filename_drift}_x{upscale}_{src}-{suffix}.png"
		self._filename = f"{path}/visualization{suffix}"
		self._screenshot_filename = f"{path}/screenshot{suffix}"
		layer = self.viewer.add_image(self.visualization, name="Visualization")
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
