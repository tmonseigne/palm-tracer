"""
Module contenant la classe :class:`PALMTracerWidget` pour l'interface principale de l'application.

Ce module définit la classe :class:`.PALMTracerWidget`, qui crée et gère l'interface utilisateur principale de l'application.
Elle contient des sections de paramètres organisées sous forme de calque,
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
from napari.layers import Points, Shapes
from napari.utils.notifications import show_error, show_info, show_warning
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QApplication, QFileDialog, QHBoxLayout, QPushButton, QSizePolicy, QTabWidget, QVBoxLayout, QWidget

from palm_tracer.PALMTracer import PALMTracer
from palm_tracer.Settings.Types import FileList
from palm_tracer.Tools import Ui
from palm_tracer.Tools.FileIO import open_json, open_tif, save_json
from palm_tracer.UI.GraphViewerWidget import GraphViewerWidget
from palm_tracer.UI.KeyBlocker import KeyBlocker
from palm_tracer.UI.Viewer3DWidget import create_viewer3d
from palm_tracer.UI.ViewerHRWidget import create_viewerhr

try: from napari.qt.threading import thread_worker, FunctionWorker  # .		   Chemin public, à préférer
except ImportError: from superqt.utils import thread_worker, FunctionWorker  # Très rare fallback

CONFIG_DIR = Path.home() / ".palm_tracer"
SETTINGS_FILE = CONFIG_DIR / "settings.json"


##################################################
class PALMTracerWidget(QWidget):
	"""Widget principal gérant toute l'interface."""
	UI_NAME: str = "PALMTracer"

	# ==================================================
	# region Init
	# ==================================================
	##################################################
	def __init__(self, viewer: "napari.viewer.Viewer"):
		"""
		Initialise le widget principal de l'interface utilisateur.

		Cette méthode configure l'interface en ajoutant différentes sections de paramètres dans la mise en page.

		:param viewer: Viewer Napari.
		"""
		super().__init__()
		# ----- Viewers -----
		self.viewer = viewer
		self.viewer_hr: Optional[Viewer] = None
		self.viewer_hr_widget: Optional[QWidget] = None
		self.viewer_3d: Optional[Viewer] = None
		self.viewer_3d_widget: Optional[QWidget] = None
		self.viewer_graph: Optional[GraphViewerWidget] = None
		# ----- Threading -----
		self._processing = False  # .					 Permets d'éviter les clics multiples.
		self._worker: Optional[FunctionWorker] = None  # Worker Napari en cours
		# ----- Objets -----
		self.pt = PALMTracer()
		self.last_file = ""
		self._preview_locs: dict[str, np.ndarray] = {"Present": np.empty(0), "Filtered": np.empty(0), "Past": np.empty(0), "Future": np.empty(0)}
		# ----- UI -----
		self.key_blocker = KeyBlocker()
		self._init_ui()
		self._connect_signal()
		self._on_startup()

	##################################################
	def _init_ui(self):
		"""Initialisation de l'interface utilisateur du widget."""
		# Base
		main_layout = QVBoxLayout(self)
		Ui.init_layout(main_layout, 0, 0)
		# -- Size policy / bornes --
		self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
		self.setMinimumWidth(360)  # borne basse réaliste (à ajuster)
		self.setMinimumHeight(220)

		# Viewer Button
		self.btn_viewer_gr = QPushButton("Graph Viewer")
		self.btn_viewer_hr = QPushButton("HR Viewer")
		self.btn_viewer_3d = QPushButton("3D Viewer")

		# Load Setting Button
		self.btn_load_setting = QPushButton("Load Setting")
		self.btn_reset_setting = QPushButton("Reset Setting")
		setting_action_row = QHBoxLayout()
		setting_action_row.addWidget(self.btn_load_setting)
		setting_action_row.addWidget(self.btn_reset_setting)
		action_widget = QWidget()  # Encapsulation dans un QWidget
		action_widget.setLayout(setting_action_row)
		self.layout().addWidget(action_widget)

		setting_ui = self.pt.settings.get_ui(self.UI_NAME)
		self.layout().addWidget(setting_ui["Batch"].widget)
		self.layout().addWidget(setting_ui["Calibration"].widget)

		# Ajout des onglets
		tabs = QTabWidget()  # Création du QTabWidget
		tabs.setStyleSheet("""QTabWidget::tab-bar { alignment: left; }""")
		tabs.addTab(self._create_tab([setting_ui["Localization"].widget, setting_ui["BeadsExtraction"].widget, setting_ui["Tracking"].widget,
									  setting_ui["BlinkingReconnection"].widget, setting_ui["TracksCompute"].widget]), "Processing")
		tabs.addTab(self._create_tab([setting_ui["Gallery"].widget, setting_ui["Graph"].widget, setting_ui["HR"].widget,
									  self.btn_viewer_gr, self.btn_viewer_hr, self.btn_viewer_3d]), "Visualization")
		tabs.addTab(self._create_tab([setting_ui["Filters"].widget]), "Filtering")

		# Layout principal
		self.layout().addSpacing(10)
		self.layout().addWidget(tabs)

		# Launch/Load Button
		self.btn_process = QPushButton("Start Processing")
		self.btn_load_result = QPushButton("Load Last Result")
		btn_action_row = QHBoxLayout()
		btn_action_row.addWidget(self.btn_process)
		btn_action_row.addWidget(self.btn_load_result)
		action_widget = QWidget()
		action_widget.setLayout(btn_action_row)
		self.layout().addWidget(action_widget)

	##################################################
	def _connect_signal(self):
		"""Connecte les signaux UI aux callbacks."""
		# Boutons QT classiques
		self.btn_viewer_gr.clicked.connect(self._open_graph_viewer)
		self.btn_viewer_hr.clicked.connect(self._open_hr_viewer)
		self.btn_viewer_3d.clicked.connect(self._open_3d_viewer)
		self.btn_load_setting.clicked.connect(self._on_load_setting_btn)
		self.btn_reset_setting.clicked.connect(self._on_reset_setting_btn)
		# lambda *_: Absorbe les arguments du QPushButton pour ne pas envoyer True à load qui a un argument str par défaut vide qui doit le rester.
		self.btn_load_result.clicked.connect(lambda *_: self.pt.load())
		self.btn_process.clicked.connect(lambda: self._thread_process(self.pt.process))

		self.pt.settings.batch["Files"].connect(self._reset_layer)  # .					 Supprime les calques et charge le fichier tif dans un calque Raw
		self.pt.settings.localization["Auto Threshold"].connect(self._auto_threshold)  # Calcul automatique du Seuil
		self.pt.settings.connect(self._on_change_setting)  # .							 Connexion à chaque changement de paramètres

		filters = self.pt.settings.filters["Localization"]
		filters["X"].connect(self._add_roi_filter_layer)  # .							 Mise à jour de la ROI dans l'affichage.
		filters["Y"].connect(self._add_roi_filter_layer)  # .							 Mise à jour de la ROI dans l'affichage.
		self.pt.connect_filters_button(self.UI_NAME)

		# Update de preview en changeant des filtres ou des paramètres de localisation
		self.pt.settings.localization.connect(lambda: self._thread_process(self._preview, self._add_preview_layers))
		self.pt.settings.filters.connect(lambda: self._thread_process(self._preview, self._add_preview_layers))

		# Update de preview en changeant de plan
		self.viewer.dims.events.current_step.connect(lambda: self._thread_process(self._preview, self._add_preview_layers))
		self.viewer.layers.selection.events.active.connect(self._on_select_layer)
		self.viewer.window.qt_viewer.installEventFilter(self.key_blocker)

	##################################################
	def _on_startup(self):
		"""Action lors du démarrage après l'initialisation de l'UI."""
		CONFIG_DIR.mkdir(parents=True, exist_ok=True)  # Création du dossier de config s'il n'existe pas
		self._load_setting(SETTINGS_FILE)

	##################################################
	@staticmethod
	def _create_tab(widgets: list[QWidget]) -> QWidget:
		"""
		Crée un onglet scrollable contenant une liste de widgets.

		Le contenu est placé dans une QScrollArea (style "page web") avec un scroll vertical
		et une largeur qui s'adapte à l'onglet.
		"""
		# Widget "conteneur" qui porte le layout réel
		tab, layout = Ui.make_tab()

		for w in widgets: layout.addWidget(w)

		# Important : permet au contenu de ne pas "collapser" et d'être en mode "colonne"
		tab.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)

		# ScrollArea permet d'avoir une barre de défilement si la fenêtre est trop petite.
		return Ui.make_vertical_scroll(tab)

	# ==================================================
	# endregion Init
	# ==================================================

	# ==================================================
	# region Threading
	# ==================================================
	##################################################
	def _thread_process(self, compute_func: Callable[[], None], post_func: Optional[Callable[[], None]] = None):
		"""
		Démarre un traitement long dans un thread séparé et mets à jour l'interface.

		Cette méthode désactive l'interface utilisateur (UI) et change le curseur en "attente" pendant l'exécution de la fonction passée en paramètre.
		Elle vérifie si un fichier est en cours de prévisualisation avant de lancer le traitement.
		Le traitement est exécuté dans un thread séparé pour ne pas bloquer l'interface principale de l'application.

		:param compute_func: Fonction à exécuter dans un thread séparé. Elle ne doit pas prendre de paramètres et ne retourne rien.
		:param post_func: Fonction à exécuter après le thread. Elle ne doit pas prendre de paramètres et ne retourne rien.
		"""
		if self._processing: return
		if self.last_file == "": return
		self._processing = True
		self._freeze_ui(True)

		@thread_worker(start_thread=False)
		def _run_background() -> None: compute_func()  # STRICTEMENT aucun accès au viewer/layers ici, pragma: no cover —  lancement sur thread.

		w: FunctionWorker = cast(FunctionWorker, _run_background())
		self._worker = w

		# s'exécute dans le thread UI
		if post_func is not None: w.returned.connect(lambda _ok: post_func())

		def _finish(*_args: object) -> None:  # UI thread : fin propre
			self._worker = None
			self._process_done()

		w.finished.connect(_finish)
		w.errored.connect(lambda e: show_error(f"Error in thread: {e}"))
		w.start()

	##################################################
	def _process_done(self):
		"""
		Finalise un traitement en réactivant l'interface et mets à jour l'affichage.

		Cette méthode est appelée lorsque le traitement est terminé.
		Elle réactive l'interface utilisateur (UI), restaure le curseur et effectue les mises à jour nécessaires sur l'interface principale.
		Elle doit être appelée depuis le thread principal (GUI).
		"""
		# show_info("Thread Process done.")
		self._processing = False
		self._freeze_ui(False)

	##################################################
	def _freeze_ui(self, on: bool) -> None:
		"""Gèle/réactive proprement l'UI sans casser la géométrie."""
		self.setDisabled(on)  # .		  Au lieu de self.layout().setEnabled(False/True)
		self.setUpdatesEnabled(not on)  # Stoppe/reprend les repaints
		if on: QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
		else:
			try: QApplication.restoreOverrideCursor()
			except RuntimeError: pass  # .Aucun curseur à restaurer

	# ==================================================
	# endregion Threading
	# ==================================================

	# ==================================================
	# region Settings Callback
	# ==================================================
	##################################################
	def _load_setting(self, filename: Path):
		"""Chargement d'un fichier de paramètres."""
		if filename.exists():
			try:
				# Bloque les signaux, agrège les multiples .emit() potentiels :
				with self.pt.settings.signal_blocked():
					cfg = open_json(str(filename))
					show_info(f"Loading the setting file '{filename}'.")
					self.pt.settings.update_from_compact_dict(cfg)
					self.pt.settings.localization["Preview"].value = False
					self.pt.settings.filters.deactivate_filters()
			except Exception as e:
				show_warning(f"Error loading file '{filename}': {e}")

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
		"""Mets à jour le fichier de paramètres général."""
		# Save settings
		save_json(str(SETTINGS_FILE), self.pt.settings.to_compact_dict())

	# ==================================================
	# endregion Settings Callback
	# ==================================================

	# ==================================================
	# region Layers Callback
	# ==================================================
	##################################################
	def _remove_layer(self, name: str):
		"""Supprime un calque s'il existe et rend silencieuses les erreurs internes à Napari."""
		try:
			if name in self.viewer.layers: self.viewer.layers.remove(self.viewer.layers[name])
		except Exception as e: Ui.print_warning(F"Error when deleting the old layer '{name}' : {e}")

	##################################################
	def _reset_layer(self):
		"""Lors de la mise à jour du batch, le fichier en preview dans Napari est mis à jour."""
		self.pt.settings.localization["Preview"].value = False
		self.pt.settings.filters.deactivate_filters()
		selected_file = cast(FileList, self.pt.settings.batch["Files"]).current_text
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
			filters = self.pt.settings.filters
			# Update Max
			z, y, x = raw_data.shape
			filters.update_limits(x, y, z)

		except Exception as e:
			show_error(f"Error loading {selected_file}: {e}")

	##################################################
	def _add_preview_layers(self):
		"""Ajoute des calques à Napari pour les localisations sur le plan actuel, précédent et suivant."""
		state_args = {
				"Present":  {"border": 0.4, "edge": 0.5, "color": "lime", "face": "lime"},
				"Filtered": {"border": 0.2, "edge": 0.5, "color": "red", "face": "red"},
				"Past":     {"border": 0.2, "edge": 0.5, "color": "cyan", "face": "transparent"},
				"Future":   {"border": 0.2, "edge": 0.5, "color": "orange", "face": "transparent"},
				}
		for state, points in self._preview_locs.items():
			if not self.pt.settings.localization["Preview"].value or points.size == 0:
				self._remove_layer(f"Points {state}")
				self._remove_layer(f"ROI {state}")
				continue

			args = state_args[state]

			# Points
			l_name = f"Points {state}"
			if l_name in self.viewer.layers:
				layer = self.viewer.layers[l_name]
				layer.data = points  # Remplace tous les points
				layer.size = 1  # .	   Remets les différents arguments en cas de nombre de points différents
				layer.border_color = args["color"]
				layer.border_width = args["border"]
				layer.face_color = args["face"]
			else: self.viewer.add_points(points, size=1, border_color=args["color"], face_color=args["face"], border_width=args["border"], name=l_name)
			self.viewer.layers[l_name].editable = False

			# ROIs seulement pour le present
			if state != "Present": continue
			roi_size = self.pt.settings.localization["ROI Size"].value
			roi_shape = self.pt.settings.localization["ROI Shape"].value
			half_size = roi_size / 2
			if roi_shape == 0:  # Ellipses : [[y_center, x_center], [y_radius, x_radius]]
				rois = np.array([[[float(y), float(x)], [float(half_size), float(half_size)]] for y, x in points], dtype=np.float32)
				s_type = "ellipse"
			else:  # Rectangles : coins opposés
				rois = [[[y - half_size, x - half_size], [y + half_size, x + half_size]] for y, x in points]
				s_type = "rectangle"

			l_name = f"ROI {state}"
			# Si le calque existe, mais n'est pas du bon type, on le supprime
			if l_name in self.viewer.layers:
				layer = self.viewer.layers[l_name]
				layer.data = (rois, len(rois) * [s_type])  # Remplace toutes les formes
				layer.edge_color = args["color"]  # .		 Remets les différents arguments en cas de nombre de ROIs différents
				layer.edge_width = args["edge"]
				layer.face_color = "transparent"
			else:
				self.viewer.add_shapes(rois, shape_type=s_type, edge_color=args["color"], edge_width=args["edge"], face_color="transparent", name=l_name)
			self.viewer.layers[l_name].editable = False

		if "Raw" in self.viewer.layers: self.viewer.layers.selection.active = self.viewer.layers["Raw"]

	##################################################
	def _add_roi_filter_layer(self):
		"""Ajoute un calque à Napari pour afficher la zone d'intérêt si le filtre est activé."""
		if "Raw" not in self.viewer.layers: return
		# Suppression du calque "ROI Filter" s'il existe
		l_name = "ROI Filter"

		filter_loc = self.pt.settings.filters["Localization"]
		is_xf, is_yf = filter_loc["X"].active, filter_loc["Y"].active

		if not is_xf and not is_yf:  # .												  Aucun filtre -> rien à afficher
			self._remove_layer(l_name)
			return

		raw_data = self.viewer.layers["Raw"].data  # .									   Récupération du layer Raw
		x0, x1, y0, y1 = self.pt.get_roi_limits(raw_data.shape[-1], raw_data.shape[-2])  # Shape peut-être (Y, X) | (Z, Y, X) | (T, Z, Y, X)

		# Si range dégénéré (ligne/colonne), on peut soit l'accepter, soit ne rien afficher. Ici : si rectangle vide, on ne crée pas de layer.
		if x1 <= x0 or y1 <= y0:
			self._remove_layer(l_name)
			return

		# Napari attend un tableau (N, 2) pour un shape, la succession des points à tracer.
		rect = [[[y0, x0], [y0, x1], [y1, x1], [y1, x0]]]  # .					   Haut-gauche, haut-droite, bas-droite, bas-gauche
		if l_name in self.viewer.layers: self.viewer.layers[l_name].data = rect  # Remplace le rectangle
		else:  # .																   Création du Calque s'il n'existe pas
			layer = self.viewer.add_shapes(rect, shape_type="polygon", name=l_name, edge_color="red", edge_width=0.5, face_color="transparent")
			layer.editable, layer.visible = False, True  # .					   Rendre non éditable (Napari) et l'affiche

	##################################################
	def _get_actual_image(self, time: int = 0) -> Optional[np.ndarray]:
		"""
		Récupère l'image actuelle plus ou moins un temps indiqué en paramètres.

		:param time: Différence de temps entre l'image actuellement affichée et celle désirée.
		:return: L'image désirée (image actuellement affichée si time = 0).
		"""
		if "Raw" not in self.viewer.layers: return None
		layer = self.viewer.layers["Raw"]  # .				   Récupération du layer Raw
		plane_idx = self.viewer.dims.current_step[0] + time  # Récupération de l'index du plan actuellement affiché plus delta de temps
		if plane_idx < 0 or plane_idx >= self.viewer.layers["Raw"].data.shape[0]: return None
		plane = layer.data[plane_idx]  # .					   Récupération des données du plan affiché
		return np.asarray(plane, dtype=np.uint16)  # .		   Renvoie sous le format numpy

	##################################################
	def _preview(self):
		"""Action lors d'un clic sur le bouton de preview."""
		if not self.pt.settings.localization["Preview"].value: return

		past, pres, fut = self._get_actual_image(-1), self._get_actual_image(), self._get_actual_image(1)
		if pres is None: return

		s = self.pt.settings.localization.settings
		try: t, w, f, fp = (s["Threshold"], s["Watershed"], self.pt.settings.localization.get_fit(), self.pt.settings.localization.get_fit_params())
		except Exception: raise
		pres_loc = self.pt.palm.localization(pres, t, w, f, fp)
		filt_loc = self.pt.filtering.localization(pres_loc)
		remo_loc = pres_loc.loc[~pres_loc.index.isin(filt_loc.index)].copy()

		self._preview_locs = {
				"Present":  filt_loc[["Y", "X"]].to_numpy(),
				"Filtered": remo_loc[["Y", "X"]].to_numpy(),
				"Past":     np.empty(0) if past is None else self.pt.filtering.localization(
						self.pt.palm.localization(past, t, w, f, fp))[["Y", "X"]].to_numpy(),
				"Future":   np.empty(0) if fut is None else self.pt.filtering.localization(self.pt.palm.localization(fut, t, w, f, fp))[["Y", "X"]].to_numpy(),
				}

		# Affichage console (les notifications posent problème en thread externe)
		l_past, l_pres, l_fut = len(self._preview_locs["Past"]), len(self._preview_locs["Present"]), len(self._preview_locs["Future"])
		print(f"Preview of plane {self.viewer.dims.current_step[0]} : {l_past + l_pres + l_fut} detected points "
			  f"({l_pres} on the current frame, {l_past} on the previous frame, {l_fut} on the next frame).")

	##################################################
	def _auto_threshold(self):
		"""Action lors d'un clic sur le bouton auto du seuillage."""
		image = self._get_actual_image()
		if image is None: return
		threshold = self.pt.palm.auto_threshold(image, self.pt.settings.localization.get_fit_params())  # Calcul du seuil automatique
		print(f"Auto Threshold: {threshold:.2f}")
		# show_info(f"Auto Threshold: {threshold:.2f}") Durant les threads externes, dangereux de faire appel à l'interface
		self.pt.settings.localization["Threshold"].value = threshold  # .								  Changement du seuil dans les settings

	##################################################
	@staticmethod
	def _on_select_layer(event):
		"""Sélectionne tous les éléments d'un calque Points ou Shapes actif."""
		layer = event.value
		if layer is None: return
		if isinstance(layer, (Shapes, Points)) and layer.data is not None and len(layer.data) > 0:
			layer.selected_data = set(range(len(layer.data)))

	# ==================================================
	# endregion Layers Callback
	# ==================================================

	# ==================================================
	# region Extern Viewer
	# ==================================================
	##################################################
	def _open_hr_viewer(self):  # pragma: no cover — Aucun lancement de fenêtre sans controle en CI
		"""Ouvre une instance Napari avec le Viewer Haute Résolution, si elle n'existe pas déjà."""
		if self.viewer_hr is None:
			self.viewer_hr, self.viewer_hr_widget = create_viewerhr(self.pt)
			self._bind_viewer_lifecycle("viewer_hr")

	##################################################
	def _open_3d_viewer(self):  # pragma: no cover — Aucun lancement de fenêtre sans controle en CI
		"""Ouvre une instance Napari avec le Viewer 3D, si elle n'existe pas déjà."""
		if self.viewer_3d is None:
			self.viewer_3d, self.viewer_3d_widget = create_viewer3d()
			self._bind_viewer_lifecycle("viewer_3d")

	##################################################
	def _open_graph_viewer(self):  # pragma: no cover — Aucun lancement de fenêtre sans controle en CI
		"""Ouvre la visionneuse de graphiques, s'il n'existe pas déjà."""
		if self.viewer_graph is None:
			w = GraphViewerWidget(self.pt)
			w.resize(1280, 720)
			self.viewer_graph = w
			# Quand le widget est détruit, rémettre la réf à None.
			w.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
			w.destroyed.connect(lambda *_: setattr(self, "viewer_graph", None))

		# (re)montrer et mettre au premier plan
		self.viewer_graph.show()
		self.viewer_graph.raise_()
		self.viewer_graph.activateWindow()

	##################################################
	def _bind_viewer_lifecycle(self, viewer_attr: str) -> None:  # pragma: no cover — Aucun lancement de fenêtre sans controle en CI
		"""Connecte la destruction de la fenêtre Qt d'un viewer Napari à la remise à None."""
		viewer = getattr(self, viewer_attr, None)
		if viewer is None: return

		def _on_close(*_):
			w = getattr(self, f"{viewer_attr}_widget", None)
			if w is not None:
				w.close()
				setattr(self, f"{viewer_attr}_widget", None)
			setattr(self, viewer_attr, None)

		qt_window = viewer.window._qt_window  # .							 QMainWindow
		qt_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)  # Garantit que "close" détruit vraiment la fenêtre.
		qt_window.destroyed.connect(_on_close)  # .							 Quand la fenêtre est détruite, on invalide le pointeur Python.


##################################################
if __name__ == "__main__":
	import napari

	_viewer = napari.Viewer()  # .										   Crée le viewer Napari
	_viewer.title = "PALMTracer"  # .									   Modifier le titre de la fenêtre
	_w = PALMTracerWidget(_viewer)  # .									   Crée ton widget en lui passant le viewer
	_viewer.window.add_dock_widget(_w, name="PALMTracer", area="right")  # L'ajoute comme dock widget dans la fenêtre Napari
	napari.run()  # .													   Lance la boucle Qt gérée par Napari
