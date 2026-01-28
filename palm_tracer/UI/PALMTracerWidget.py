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
from napari.utils.notifications import show_error, show_info, show_warning
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QApplication, QFileDialog, QHBoxLayout, QPushButton, QSizePolicy, QTabWidget, QVBoxLayout, QWidget

from palm_tracer.PALMTracer import PALMTracer
from palm_tracer.Settings.Types import FileList
from palm_tracer.Tools import open_json, open_tif, print_warning, save_json
from palm_tracer.UI.GraphViewerWidget import GraphViewerWidget
from palm_tracer.UI.Viewer3DWidget import create_viewer3d
from palm_tracer.UI.ViewerHRWidget import create_viewerhr

try: from napari.qt.threading import thread_worker, FunctionWorker				# chemin public, à préférer
except ImportError:    from superqt.utils import thread_worker, FunctionWorker  # très rare fallback

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
		# ----- Viewers -----
		self.viewer = viewer
		self.viewer_hr: Optional[Viewer] = None
		self.viewer_3d: Optional[Viewer] = None
		self.viewer_graph: Optional[GraphViewerWidget] = None
		# ----- Threading -----
		self._processing = False  # pour éviter les clics multiples
		self._worker: Optional[FunctionWorker] = None  # worker napari en cours
		self._tearing_down = False  # vrai pendant le teardown pour ignorer les callbacks
		# ----- Objets -----
		self.pt = PALMTracer()
		self.last_file = ""
		self._preview_locs: dict[str, None | np.ndarray] = {"Past": None, "Present": None, "Future": None}
		# ----- UI -----
		self._init_ui()
		self._connect_signal()
		self._on_startup()

	##################################################
	def _init_ui(self):
		""" Initialisation de l'interface utilisateur du widget. """
		# Base
		self.setLayout(QVBoxLayout())
		# -- Size policy / bornes --
		self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
		self.setMinimumWidth(360)  # borne basse réaliste (à ajuster)
		self.setMinimumHeight(220)

		# Viewer Button
		self.btn_viewer_graph = QPushButton("Open Graph Viewer")
		self.btn_viewer_hr = QPushButton("Open HR Viewer")
		self.btn_viewer_3d = QPushButton("Open 3D Viewer")

		# Load Setting Button
		btn_load = QPushButton("Load Setting")
		btn_load.clicked.connect(self._on_load_setting_btn)
		btn_reset = QPushButton("Reset Setting")
		btn_reset.clicked.connect(self._on_reset_setting_btn)
		setting_action_row = QHBoxLayout()
		setting_action_row.addWidget(btn_load)
		setting_action_row.addWidget(btn_reset)
		action_widget = QWidget()  # Encapsulation dans un QWidget
		action_widget.setLayout(setting_action_row)
		self.layout().addWidget(action_widget)

		self.layout().addWidget(self.pt.settings.batch.widget)
		self.layout().addWidget(self.pt.settings.calibration.widget)

		# Ajout des onglets
		tabs = QTabWidget()  # Création du QTabWidget
		tabs.addTab(self._create_tab([self.pt.settings.localization.widget, self.pt.settings.tracking.widget,
									  self.pt.settings.tracks_compute.widget]), "Processing")
		tabs.addTab(self._create_tab([self.pt.settings.gallery.widget, self.pt.settings.visualization_hr.widget, self.pt.settings.visualization_graph.widget,
									  self.btn_viewer_graph, self.btn_viewer_hr, self.btn_viewer_3d]), "Visualization")
		tabs.addTab(self._create_tab([self.pt.settings.filtering.widget]), "Filtering")

		# Layout principal
		self.layout().addWidget(tabs)

		# Add Specific behaviour
		# On supprime tous les layers et on charge le fichier tif dans un layer Raw
		self.pt.settings.batch["Files"].connect(self._reset_layer)

		# Calcul automatique du Seuil
		self.pt.settings.localization["Auto Threshold"].connect(self._auto_threshold)

		# Connexion à chaque changement de paramètres
		self.viewer.dims.events.current_step.connect(lambda: self._thread_process(self._preview, self._add_detection_layers))
		self.pt.settings.connect(self._on_change_setting)

		# Launch/Load Button
		btn_process = QPushButton("Start Processing")
		btn_process.clicked.connect(lambda: self._thread_process(self.pt.process))
		btn_load = QPushButton("Load Last Result")
		btn_load.clicked.connect(lambda *_: self.pt.load())
		btn_action_row = QHBoxLayout()
		btn_action_row.addWidget(btn_process)
		btn_action_row.addWidget(btn_load)
		action_widget = QWidget()
		action_widget.setLayout(btn_action_row)
		self.layout().addWidget(action_widget)

	def _connect_signal(self):
		"""Connecte les signaux UI aux callbacks."""
		self.btn_viewer_graph.clicked.connect(self._open_graph_viewer)
		self.btn_viewer_hr.clicked.connect(self._open_hr_viewer)
		self.btn_viewer_3d.clicked.connect(self._open_3d_viewer)

	##################################################
	def _on_startup(self):
		"""Action lors du démarrage après l'initialisation de l'UI."""
		CONFIG_DIR.mkdir(parents=True, exist_ok=True)  # Création du dossier de config s'il n'existe pas
		self._load_setting(SETTINGS_FILE)

	##################################################
	@staticmethod
	def _create_tab(widgets: list[QWidget]) -> QWidget:
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
	# region Threading
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
		if self.last_file == "": return
		self._processing = True
		self._freeze_ui(True)  # à la place de layout().setEnabled(False)

		@thread_worker(start_thread=False)
		def _run_background() -> None: compute_func()  # STRICTEMENT aucun accès au viewer/layers ici

		w: FunctionWorker = cast(FunctionWorker, _run_background())
		self._worker = w

		# s'exécute dans le thread UI
		if post_func is not None: w.returned.connect(lambda _ok: (not self._tearing_down) and post_func())

		def _finish(*_args: object) -> None:  # UI thread : fin propre
			self._worker = None
			self._process_done()

		w.finished.connect(_finish)
		w.errored.connect(lambda e: show_error(f"Erreur dans le thread : {e}"))
		w.start()

	##################################################
	def _process_done(self):
		"""
		Finalise un traitement en réactivant l'interface et met à jour l'affichage.

		Cette méthode est appelée lorsque le traitement est terminé.
		Elle réactive l'interface utilisateur (UI), restaure le curseur et effectue les mises à jour nécessaires sur l'interface principale.
		Elle doit être appelée depuis le thread principal (GUI).
		"""
		self._processing = False
		self._freeze_ui(False)  # à la place de layout().setEnabled(False)
		show_info("Thread Process done")

	##################################################
	def prepare_teardown(self, timeout_ms: int = 30_000):
		"""À appeler avant viewer.close() pour stopper les workers et neutraliser les callbacks UI."""
		self._tearing_down = True

		try:  # Déconnecter ce qui peut encore déclencher des callbacks durant la fermeture
			self.viewer.dims.events.current_step.disconnect()
			self.pt.settings.disconnect()
		except (TypeError, RuntimeError): pass  # TypeError : aucune connexion existante, RuntimeError : déjà déconnecté / objet détruit

		# Demander l'arrêt du worker en cours et attendre sa fin
		if self._worker is not None:
			try:
				self._worker.quit()
				FunctionWorker.await_workers(timeout_ms)  # attend jusqu'à 30s que tous les workers quittent
			except (RuntimeError, AttributeError): pass   # Worker déjà terminé ou thread détruit
			self._worker = None

		self._freeze_ui(False)  # Réactive l'UI si gelée

	##################################################
	def _freeze_ui(self, on: bool) -> None:
		"""Gèle/réactive proprement l'UI sans casser la géométrie."""
		self.setDisabled(on)			# au lieu de self.layout().setEnabled(False)
		self.setUpdatesEnabled(not on)  # stoppe/reprend les repaints
		if on: QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
		else:
			try: QApplication.restoreOverrideCursor()
			except RuntimeError: pass  # Aucun curseur à restaurer

	# ==================================================
	# endregion Threading
	# ==================================================

	# ==================================================
	# region Settings Callback
	# ==================================================
	##################################################
	def _load_setting(self, filename: Path):
		"""Chargement d'un fichier de setting."""
		if filename.exists():
			try:
				show_info(f"Chargement du fichier de configuration '{filename}'.")
				# Bloque les signaux, agrège les multiples .emit() potentiels :
				with self.pt.settings.signal_blocked():
					cfg = open_json(str(filename))
					self.pt.settings.update_from_dict(cfg)
					self.pt.settings.localization["Preview"].set_value(False)
			except Exception as e:
				show_warning(f"Erreur lors du chargement du fichier '{filename}' : {e}")

	##################################################
	def _on_load_setting_btn(self):
		"""Action lors d'un clic sur le bouton Load setting."""
		filename, _ = QFileDialog.getOpenFileName(None, "Sélectionner un fichier de paramètres", ".", "Fichiers JSON (*.json)")
		self._load_setting(Path(filename))

	##################################################
	def _on_reset_setting_btn(self):
		"""Action lors d'un clic sur le bouton Reset setting."""
		self.pt.settings.reset()

	##################################################
	def _on_change_setting(self):
		""" Mets à jour le fichier de setting et la preview à chaque changement de setting."""
		# Save settings
		save_json(str(SETTINGS_FILE), self.pt.settings.to_dict())
		self._thread_process(self._preview, self._add_detection_layers)

	# ==================================================
	# endregion Settings Callback
	# ==================================================

	# ==================================================
	# region Layers Callback
	# ==================================================
	##################################################
	def _reset_layer(self):
		"""Lors de la mise à jour du batch, le fichier en preview dans Napari est mis à jour."""
		if self._tearing_down or not getattr(self, "viewer", None): return
		self.pt.settings.localization["Preview"].set_value(False)
		selected_file = cast(FileList, self.pt.settings.batch["Files"]).get_selected()
		if not selected_file:
			self.last_file = ""
			self.viewer.layers.clear()
			return

		if self.last_file == selected_file: return
		else: self.last_file = selected_file

		self.viewer.layers.clear()  # Nettoyez tous les layers existants dans le viewer

		# Chargez le fichier TIF sélectionné comme un layer Raw dans le viewer
		try:
			raw_data = open_tif(selected_file)
			self.viewer.add_image(raw_data, name="Raw")
			show_info(f"Loaded {selected_file} into Napari viewer.")
		except Exception as e:
			show_error(f"Error loading {selected_file}: {e}")

	##################################################
	def _add_detection_layers(self):
		""" Ajoute des calques à Napari pour les localisations sur le plan actuel, précédent et suivant. """
		if self._tearing_down or not getattr(self, "viewer", None): return
		state_args = {
				"Past":    {"border": 0.2, "edge": 0.2, "color": "cyan", "face": "transparent"},
				"Present": {"border": 0.4, "edge": 0.4, "color": "lime", "face": "lime"},
				"Future":  {"border": 0.2, "edge": 0.2, "color": "orange", "face": "transparent"}
				}
		for state, points in self._preview_locs.items():
			if not self.pt.settings.localization["Preview"].get_value() or points is None or points.size == 0:
				if f"Points {state}" in self.viewer.layers:
					try: self.viewer.layers.remove(self.viewer.layers[f"Points {state}"])
					except Exception as e: print_warning(F"erreur lors de la suppression de l'ancien calque : {e}")
				if f"ROI {state}" in self.viewer.layers:
					try: self.viewer.layers.remove(self.viewer.layers[f"ROI {state}"])
					except Exception as e: print_warning(F"erreur lors de la suppression de l'ancien calque : {e}")
				continue

			args = state_args[state]

			# Points
			l_name = f"Points {state}"
			if l_name in self.viewer.layers:
				layer = self.viewer.layers[l_name]
				layer.data = points  # Remplace tous les points
				layer.size = 1		 # Remets les différents arguments en cas de nombre de points différents
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
			# Si le calque existe mais n'est pas du bon type, on le supprime
			if l_name in self.viewer.layers:
				layer = self.viewer.layers[l_name]
				# Cas particulier en cas de changement de formes.
				# Il a du mal à mettre à jour, une suppression complete est necessaire bien que couteuse en temps
				if layer.shape_type[0] != s_type:
					try: self.viewer.layers.remove(self.viewer.layers[l_name])
					except Exception as e: print_warning(f"Erreur lors de la suppression de l'ancien calque : {e}")
					self.viewer.add_shapes(rois, shape_type=s_type, edge_color=args["color"], edge_width=args["edge"], face_color="transparent", name=l_name)
				else:
					layer.data = rois		   # Remplace toutes les formes
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
			# show_warning("Aucun fichier en preview.")
			return None
		layer = self.viewer.layers["Raw"]					 # Récupération du layer Raw
		plane_idx = self.viewer.dims.current_step[0] + time  # Récupération de l'index du plan actuellement affiché plus delta de temps
		if plane_idx < 0 or plane_idx >= self.viewer.layers["Raw"].data.shape[0]: return None
		plane = layer.data[plane_idx]						 # Récupération des données du plan affiché
		return np.asarray(plane, dtype=np.uint16)			 # Renvoie sous le format numpy

	##################################################
	def _preview(self):
		"""Action lors d'un clic sur le bouton de preview."""
		if self._tearing_down or not getattr(self, "viewer", None) or not self.pt.settings.localization["Preview"].get_value(): return

		past, present, future = self._get_actual_image(-1), self._get_actual_image(), self._get_actual_image(1)
		if present is None: return

		s = self.pt.settings.localization.get_settings()
		try: t, w, f, fp = (s["Threshold"], s["Watershed"], self.pt.settings.localization.get_fit(), self.pt.settings.localization.get_fit_params())
		except Exception: raise
		self._preview_locs = {
				"Past":    None if past is None else self.pt.filter_localizations(self.pt.palm.localization(past, t, w, f, fp))[["Y", "X"]].to_numpy(),
				"Present": self.pt.filter_localizations(self.pt.palm.localization(present, t, w, f, fp))[["Y", "X"]].to_numpy(),
				"Future":  None if future is None else self.pt.filter_localizations(self.pt.palm.localization(future, t, w, f, fp))[["Y", "X"]].to_numpy()
				}

		# Affichage console (les notifications posent problème en thread externe)
		l_past, l_present, l_future = map(lambda x: len(x) if x is not None else 0,
										  (self._preview_locs.get("Past"), self._preview_locs.get("Present"), self._preview_locs.get("Future")))
		print(f"Preview des {l_past + l_present + l_future} points détectés ({l_present} sur l'image actuelle, "
			  f"{l_past} sur l'image précédente, {l_future} sur l'image suivante).")

	##################################################
	def _auto_threshold(self):
		"""Action lors d'un clic sur le bouton auto du seuillage."""
		if self._tearing_down or not getattr(self, "viewer", None): return
		image = self._get_actual_image()
		if image is None: return
		threshold = self.pt.palm.auto_threshold(image, self.pt.settings.localization.get_fit_params())  # Calcul du seuil automatique
		print(f"Auto Threshold : {threshold:.2f}")
		# show_info(f"Auto Threshold : {threshold:.2f}") Durant les thread externe, dangereux de faire appel à l'interface
		self.pt.settings.localization["Threshold"].set_value(threshold)  # Changement du seuil dans les settings

	# ==================================================
	# endregion Layers Callback
	# ==================================================

	# ==================================================
	# region Extern Viewer
	# ==================================================
	##################################################
	def _open_hr_viewer(self):  # pragma: no cover pytest à du mal avec les ouvertures en série de fenêtres
		"""Ouvre une instance napari avec le Viewer Haute Résolution, si elle n'existe pas déjà."""
		if self.viewer_hr is None:
			self.viewer_hr = create_viewerhr(self.pt)
			self._bind_viewer_lifecycle("viewer_hr")

	##################################################
	def _open_3d_viewer(self):  # pragma: no cover pytest à du mal avec les ouvertures en série de fenêtres
		"""Ouvre une instance napari avec le Viewer 3D, si elle n'existe pas déjà."""
		if self.viewer_3d is None:
			self.viewer_3d = create_viewer3d()
			self._bind_viewer_lifecycle("viewer_3d")

	##################################################
	def _open_graph_viewer(self):  # pragma: no cover pytest à du mal avec les ouvertures en série de fenêtres
		"""Ouvre la visionneuse de graphiques, s'il n'existe pas déjà."""
		if self.viewer_graph is None:
			w = GraphViewerWidget(self.pt)
			w.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
			# Quand le widget est détruit, remettre la réf à None
			w.destroyed.connect(lambda *_: setattr(self, "viewer_graph", None))
			w.resize(1280, 720)
			self.viewer_graph = w

		# (re)montrer et mettre au premier plan
		self.viewer_graph.show()
		self.viewer_graph.raise_()
		self.viewer_graph.activateWindow()

	##################################################
	def _bind_viewer_lifecycle(self, viewer_attr: str) -> None:
		"""Connecte la destruction de la fenêtre Qt d'un viewer Napari à la remise à None."""
		viewer = getattr(self, viewer_attr)
		if viewer is None: return
		qt_window = viewer.window._qt_window									  # QMainWindow
		qt_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)		  # garantit que "close" détruit vraiment la fenêtre.
		qt_window.destroyed.connect(lambda *_: setattr(self, viewer_attr, None))  # Quand la fenêtre est détruite, on invalide le pointeur Python.

	# ==================================================
	# endregion Extern Viewer
	# ==================================================


##################################################
if __name__ == "__main__":  # pragma: no cover
	import napari

	_viewer = napari.Viewer()											# Crée le viewer napari
	_viewer.title = "PALMTracer"										# Modifier le titre de la fenêtre
	_w = PALMTracerWidget(_viewer)										# Crée ton widget en lui passant le viewer
	_viewer.window.add_dock_widget(_w, name="Viewer 3D", area="right")  # L'ajoute comme dock widget dans la fenêtre napari
	napari.run()														# Lance la boucle Qt gérée par napari
