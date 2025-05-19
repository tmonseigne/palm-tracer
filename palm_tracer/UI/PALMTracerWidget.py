"""
Module contenant la classe :class:`PALMTracerWidget` pour l'interface principale de l'application.

Ce module définit la classe :class:`.PALMTracerWidget`, qui crée et gère l'interface utilisateur principale de l'application.
Elle contient des sections de paramètres organisées sous forme de layout,
permettant de modifier différents paramètres pour l'exécution des algorithmes et l'affichage des résultats.

.. todo::
    Pour le moment, la partie permettant de mettre en attente et annuler des preview ne fonctionne pas car Napari freeze le temps de la mise à jour.
    l'utilisation de thread pour lancer certaines fonctions est problématique à l'heure actuelle.
"""
from pathlib import Path
from typing import Callable, cast, Optional

import napari
import numpy as np
from napari import Viewer
from qtpy.QtCore import Qt, QThread
from qtpy.QtWidgets import QApplication, QFileDialog, QPushButton, QTabWidget, QVBoxLayout, QWidget

from palm_tracer.PALMTracer import PALMTracer
from palm_tracer.Processing import Palm
from palm_tracer.Settings.Types import FileList
from palm_tracer.Tools import open_json, open_tif, print_error, print_warning, save_json
from palm_tracer.UI.Worker import Worker

CONFIG_DIR = Path.home() / ".palm_tracer"
SETTINGS_FILE = CONFIG_DIR / "settings.json"


##################################################
class PALMTracerWidget(QWidget):
	"""Widget principal gérant toute l'interface"""

	# ==================================================
	# region Init
	# ==================================================
	##################################################
	def __init__(self, viewer: "napari.viewer.Viewer"):
		"""
		Initialise le widget principal de l'interface utilisateur.

		Cette méthode configure l'interface en ajoutant différentes sections de paramètres dans la mise en page.

		:param viewer: Viewer napari.
		"""
		super().__init__()
		self.viewer = viewer
		self.viewer_hr: Optional[Viewer] = None
		self.filedialog = QFileDialog(self)
		self.pt = PALMTracer()
		self.last_file = ""
		self._preview_locs: dict[str, None | np.ndarray] = {"Past": None, "Present": None, "Future": None}
		self._processing = False  # pour éviter les clics multiples
		self.__init_ui()
		self.__on_startup()

	##################################################
	def __init_ui(self):
		""" Initialisation de l'interface utilisateur du widget. """
		# Base
		self.setLayout(QVBoxLayout())
		self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)

		# Load Setting Button
		btn = QPushButton("Load Setting")
		btn.clicked.connect(self._load_setting)
		self.layout().addWidget(btn)

		self.layout().addWidget(self.pt.settings.batch.widget)
		self.layout().addWidget(self.pt.settings.calibration.widget)

		# Ajout des onglets
		tabs = QTabWidget()  # Création du QTabWidget
		tabs.addTab(self.__create_tab([self.pt.settings.localization.widget, self.pt.settings.tracking.widget]), "Processing")
		tabs.addTab(self.__create_tab([self.pt.settings.gallery.widget, self.pt.settings.visualization_hr.widget,
									   self.pt.settings.visualization_graph.widget]), "Visualization")
		tabs.addTab(self.__create_tab([self.pt.settings.filtering.widget]), "Filtering")

		# Layout principal
		self.layout().addWidget(tabs)

		# Add Specific behaviour
		# Lors de l'ajout d'un fichier avec le bouton +, -, clear du setting batch -> Files, le FileList est mis à jour et le selected également.
		# La mise à jour du selected fait qu'on le recharge pour la visu napari.
		# On supprime tous les layers et on charge le fichier tif dans un layer Raw
		setting = self.pt.settings.batch["Files"]
		if setting and isinstance(setting, FileList):  # pragma: no cover (toujours vrai)
			setting.connect(self._reset_layer)

		# Calcul de la preview
		self.pt.settings.localization["Preview"].connect(lambda: self._thread_process(self._preview, self._add_detection_layers))
		self.viewer.dims.events.current_step.connect(self._on_plane_change)

		# Calcul automatique du Seuil
		self.pt.settings.localization["Auto Threshold"].connect(self._auto_threshold)

		# Connexion à chaque changement de paramètres
		self.pt.settings.connect(self._on_change)

		# Launch Button
		btn = QPushButton("Start Processing")
		btn.clicked.connect(lambda: self._thread_process(self.pt.process, self._show_high_res_image))
		self.layout().addWidget(btn)

	##################################################
	def __on_startup(self):
		"""Action lors du démarrage après l'initialisation de l'UI."""
		CONFIG_DIR.mkdir(parents=True, exist_ok=True)  # Création du dossier de config s'il n'existe pas
		self._load_setting(SETTINGS_FILE)

	##################################################
	@staticmethod
	def __create_tab(widgets: list[QWidget]) -> QWidget:
		"""Crée l'onglet 'Processing' avec son QFormLayout"""
		widget = QWidget()
		layout = QVBoxLayout()
		layout.setAlignment(Qt.AlignmentFlag.AlignTop)

		for w in widgets: layout.addWidget(w)

		widget.setLayout(layout)
		return widget

	# ==================================================
	# endregion Init
	# ==================================================

	# ==================================================
	# region Callback
	# ==================================================
	##################################################
	def _thread_process(self, compute_func: Callable[[], None], post_func: Optional[Callable[[], None]] = None):
		"""
		Démarre un traitement long dans un thread séparé et met à jour l'interface.

		Cette méthode désactive l'interface utilisateur (UI) et change le curseur en "attente" pendant l'exécution de la fonction passée en paramètre.
		Elle vérifie si un fichier est en cours de prévisualisation avant de lancer le traitement.
		Le traitement est exécuté dans un thread séparé pour ne pas bloquer l'interface principale de l'application.

		:param compute_func: La fonction à exécuter dans un thread séparé. Elle ne doit pas prendre de paramètres et ne retourne rien.
		:param post_func: La fonction à exécuter après le thread. Elle ne doit pas prendre de paramètres et ne retourne rien.
		"""
		if self._processing: return
		if self.last_file == "":
			print_warning("Aucun fichier en preview.")
			return
		self._processing = True
		self.layout().setEnabled(False)							   # désactive l'interface
		QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)  # Changement du curseur
		QApplication.processEvents()							   # met à jour l'interface

		self.thread = QThread(self)
		self.worker = Worker(compute_func)
		self.worker.moveToThread(self.thread)
		self.thread.started.connect(self.worker.run)
		self.worker.finished.connect(self.thread.quit)
		self.worker.finished.connect(self.worker.deleteLater)
		self.thread.finished.connect(self.thread.deleteLater)
		if post_func: self.worker.result.connect(post_func)
		self.worker.finished.connect(lambda: self._process_done())
		self.worker.error.connect(lambda msg: print_error(f"Erreur dans le thread : {msg}"))
		self.thread.start()  # Lancer le traitement

	##################################################
	def _process_done(self):
		"""
		Finalise un traitement en réactivant l'interface et met à jour l'affichage.

		Cette méthode est appelée lorsque le traitement est terminé.
		Elle réactive l'interface utilisateur (UI), restaure le curseur et effectue les mises à jour nécessaires sur l'interface principale.
		Elle doit être appelée depuis le thread principal (GUI).
		"""
		self.layout().setEnabled(True)		  # Réactive l'interface
		QApplication.restoreOverrideCursor()  # Changement du curseur
		QApplication.processEvents()		  # met à jour l'interface
		self._processing = False

	##################################################
	def _load_setting(self, filename: Path):
		"""Chargement d'un fichier de setting."""
		if filename.exists():
			try:
				self.pt.settings.update_from_dict(open_json(str(filename)))
				print(f"Chargement du fichier de configuration '{filename}'.")
			except Exception as e:
				print_warning(f"Erreur lors du chargement du fichier '{filename}' : {e}")

	##################################################
	def _on_load_setting_btn(self):  # pragma: no cover
		"""Action lors d'un clic sur le bouton Load setting."""
		filename, _ = self.filedialog.getOpenFileName(None, "Sélectionner un fichier de paramètres", ".", "Fichiers JSON (*.json)")
		self._load_setting(Path(filename))

	##################################################
	def _reset_layer(self):
		"""Lors de la mise à jour du batch, le fichier en preview dans Napari est mis à jour."""
		selected_file = cast(FileList, self.pt.settings.batch["Files"]).get_selected()
		if not selected_file:
			self.last_file = ""
			print_warning("Aucun fichier sélectionné.")
			return

		if self.last_file == selected_file: return
		else: self.last_file = selected_file

		# Nettoyez tous les layers existants dans le viewer
		self.viewer.layers.clear()

		# Chargez le fichier TIF sélectionné comme un layer Raw dans le viewer
		try:
			raw_data = open_tif(selected_file)
			self.viewer.add_image(raw_data, name="Raw")
			print(f"Loaded {selected_file} into Napari viewer.")
		except Exception as e:
			print_error(f"Error loading {selected_file}: {e}")

	##################################################
	def _add_detection_layers(self):
		""" Ajoute des calques à Napari pour les localisations sur le plan actuel, précédent et suivant. """
		state_args = {
				"Past":    {"border": 0.2, "edge": 0.2, "color": "cyan", "face": "transparent"},
				"Present": {"border": 0.4, "edge": 0.4, "color": "lime", "face": "lime"},
				"Future":  {"border": 0.2, "edge": 0.2, "color": "orange", "face": "transparent"}
				}
		for state, points in self._preview_locs.items():
			if points is None or points.size == 0:
				if f"Points {state}" in self.viewer.layers: self.viewer.layers.remove(self.viewer.layers[f"Points {state}"])
				if f"ROI {state}" in self.viewer.layers: self.viewer.layers.remove(self.viewer.layers[f"ROI {state}"])
				continue

			args = state_args[state]

			# Points
			l_name = f"Points {state}"
			if l_name in self.viewer.layers:
				layer = self.viewer.layers[l_name]
				layer.data = points  # Remplace tous les points
				layer.size = 1  # Remets les différents arguments en cas de nombre de points différents
				layer.border_color = args["color"]
				layer.border_width = args["border"]
				layer.face_color = args["face"]
			else: self.viewer.add_points(points, size=1, border_color=args["color"], face_color=args["face"], border_width=args["border"], name=l_name)
			self.viewer.layers[l_name].editable = False

			# ROIs seulement pour le present
			if state != "Present": continue
			roi_size = self.pt.settings.localization["ROI Size"].get_value()
			roi_shape = self.pt.settings.localization["ROI Shape"].get_value()
			half_size = roi_size / 2
			if roi_shape == 0:  # Ellipses
				# Chaque ellipse = [[y_center, x_center], [y_radius, x_radius]]
				rois = np.array([[[float(y), float(x)], [float(half_size), float(half_size)]] for y, x in points], dtype=np.float32)
				s_type = "ellipse"
			else:  # Rectangles (coins opposés)
				rois = [[[y - half_size, x - half_size], [y + half_size, x + half_size]] for y, x in points]
				s_type = "rectangle"

			l_name = f"ROI {state}"
			# Si le calque existe mais n’est pas du bon type, on le supprime
			if l_name in self.viewer.layers:
				layer = self.viewer.layers[l_name]
				# Cas particulier en cas de changement de formes.
				# Il a du mal à mettre à jour, une suppression complete est necessaire bien que couteuse en temps
				if layer.shape_type != s_type:
					self.viewer.layers.remove(self.viewer.layers[f"ROI {state}"])
					self.viewer.add_shapes(rois, shape_type=s_type, edge_color=args["color"], edge_width=args["edge"], face_color="transparent", name=l_name)
				else:
					layer.data = rois  # Remplace toutes les formes
					layer.shape_type = s_type  # Remets les différents arguments en cas de nombre de ROI différents
					layer.edge_color = args["color"]
					layer.edge_width = args["edge"]
					layer.face_color = "transparent"
			else:
				self.viewer.add_shapes(rois, shape_type=s_type, edge_color=args["color"], edge_width=args["edge"], face_color="transparent", name=l_name)
			self.viewer.layers[l_name].editable = False

	##################################################
	def _get_actual_image(self, time: int = 0) -> Optional[np.ndarray]:
		"""
		Récupère l'image actuelle plus ou moins un temps indiqué en paramètres
		:param time: différence de temps entre l'image actuellement affichée et celle désirée.
		:return: l'image désirée (actuellement affichée si time = 0).
		"""
		if self.last_file == "":
			print_warning("Aucun fichier en preview.")
			return None
		layer = self.viewer.layers["Raw"]					 # Récupération du layer Raw
		plane_idx = self.viewer.dims.current_step[0] + time  # Récupération de l'index du plan actuellement affiché plus delta de temps
		if plane_idx < 0 or plane_idx >= self.viewer.layers["Raw"].data.shape[0]: return None
		plane = layer.data[plane_idx]						 # Récupération des données du plan affiché
		return np.asarray(plane, dtype=np.uint16)			 # Renvoie sous le format numpy

	##################################################
	def _on_change(self):
		""" Mets à jour le fichier de setting et la preview à chaque changement de setting."""
		# Save settings
		save_json(str(SETTINGS_FILE), self.pt.settings.to_dict())
		if "Points Present" in self.viewer.layers: self._thread_process(self._preview, self._add_detection_layers)

	##################################################
	def _on_plane_change(self, event):
		"""
		Met à jour la preview au changement du plan affiché dans Napari.
		:param event:
		"""
		if "Points Present" in self.viewer.layers: self._thread_process(self._preview, self._add_detection_layers)

	##################################################
	def _preview(self):
		"""Action lors d'un clic sur le bouton de preview."""
		past, present, future = self._get_actual_image(-1), self._get_actual_image(), self._get_actual_image(1)
		if present is None: return

		s = self.pt.settings.localization.get_settings()
		t, w, m, gs, gt, r = (s["Threshold"], s["Watershed"], Palm.get_fit(s["Fit"], s["Gaussian Fit Mode"]),
							   s["Gaussian Fit Sigma"], s["Gaussian Fit Theta"], s["ROI Size"])
		self._preview_locs = {
				"Past":    None if past is None else self.pt.filter_localizations(self.pt.palm.run(past, t, w, m, gs, gt, r))[["Y", "X"]].to_numpy(),
				"Present": self.pt.filter_localizations(self.pt.palm.run(present, t, w, m, gs, gt, r))[["Y", "X"]].to_numpy(),
				"Future":  None if future is None else self.pt.filter_localizations(self.pt.palm.run(future, t, w, m, gs, gt, r))[["Y", "X"]].to_numpy()
				}

		l_past, l_present, l_future = map(lambda x: len(x) if x is not None else 0,
										  (self._preview_locs.get("Past"), self._preview_locs.get("Present"), self._preview_locs.get("Future")))
		print(f"Preview des {l_past + l_present + l_future} points détectés "
			  f"({l_present} sur l'image actuelle, {l_past} sur l'image précédente, {l_future} sur l'image suivante).")

	##################################################
	def _auto_threshold(self):
		"""Action lors d'un clic sur le bouton auto du seuillage."""
		image = self._get_actual_image()
		if image is None: return
		threshold = self.pt.palm.auto_threshold(image)					 # Calcul du seuil automatique
		print(f"Auto Threshold : {threshold}")
		self.pt.settings.localization["Threshold"].set_value(threshold)  # Changement du seuil dans les settings

	##################################################
	def _show_high_res_image(self):  # pragma: no cover le systeme pytest à du mal avec les ouvertures en série de fenêtres
		"""
		Ouvre la fenêtre de visualisation ou la met à jour si elle existe déjà.
		"""
		if self.pt.visualization is None: return

		# Vérifier si la fenêtre existe déjà, mise à jour de l'image si la fenêtre est déjà ouverte
		if not hasattr(self, "high_res_window") or self.viewer_hr is None:
			self.viewer_hr = Viewer()
			# Modifier le titre de la fenêtre
			self.viewer_hr.window._qt_window.setWindowTitle(f"High Resolution Visualization")
			# Cacher la barre de menu
			self.viewer_hr.window._qt_window.menuBar().setVisible(False)

		self.viewer_hr.layers.clear()
		self.viewer_hr.add_image(self.pt.visualization, name="Visualization", visible=False)
		if self.pt.localizations is None: return
		points = self.pt.localizations[["Y", "X"]].to_numpy() * self.pt.settings.visualization_hr.get_settings()["Ratio"]
		layer = self.viewer_hr.add_points(points, size=1, face_color="lime", name="Points")
		layer.editable = False

	# ==================================================
	# endregion Callback
	# ==================================================
