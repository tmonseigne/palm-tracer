"""
Module contenant la classe :class:`GraphViewerWidget` pour la visualisation interactive
des graphiques liés aux données PALMTracer (pile TIFF, localisations, tracking).

Ce widget fournit :
- Une interface en deux parties :
  • Colonne gauche : informations fichier + présence localisation/tracking, choix du domaine
	(Stack / Localization / Tracking) via 3 boutons exclusifs, et sélection de la source.
  • Zone droite : rendu d'un graphe Plotly dans un QWebEngineView (zoom, pan, hover, export).
- Un couplage léger avec :class:`PALMTracer` pour accéder aux fichiers en cours et charger
  automatiquement pile/CSV (localisations/tracking).
- Des exports HTML/PNG/PDF (PNG via capture Qt en fallback, si Kaleido indisponible).

Notes
-----
- Le rendu interactif utilise QtWebEngine (PySide6-Addons / PyQt6-WebEngine / PyQtWebEngine selon binding).
  Si QtWebEngine n'est pas disponible, un fallback texte explicite est affiché.
- Le widget ne copie pas l'objet :class:`PALMTracer` ; il garde une **référence** passée au constructeur.
- Le calcul/formatage des figures est délégué à :class:`palm_tracer.Processing.Grapher`.

.. todo:: Warning si plus de 10 millions de points sur un affichage (avec option se souvenir du choix).
"""
from __future__ import annotations

from pathlib import Path
from typing import cast

import numpy as np
import pandas as pd
from qtpy.QtWidgets import QApplication, QFrame, QGridLayout, QGroupBox, QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from palm_tracer.PALMTracer import PALMTracer
from palm_tracer.Settings.Groups import Graph, GraphDisplay
from palm_tracer.Settings.Types import BaseSettingType, Combo, FileList
from palm_tracer.Tools import Ui
from palm_tracer.UI.BasePlotlyWidget import BasePlotlyWidget

# ==================================================
# region Constantes
# ==================================================
DATA_SRC: dict[str, list] = {
		"Localization": ["Integrated Intensity", "Sigma X", "Sigma Y", "Circularity", "Theta",
						 "X", "Y", "Z", "Surface", "MSE XY", "MSE Z", "Localizations Count"],
		"Tracking":     ["Length"],
		"No Dual":      ["Localizations Count", "Length", "MSD"],
		}

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
	"""Widget de visualisation interactive (Plotly + QtWebEngine) pour PALMTracer.

	Ce widget expose une UI compacte pour :
		- afficher des graphes à partir de la pile TIFF (Stack) ou des CSV (Localization/Tracking),
		- choisir la *famille* de données (Stack / Localization / Tracking) via 3 boutons exclusifs,
		- sélectionner la *source* dans une ComboBox (ex. Intensité, Localizations Count, etc.),
		- exporter la figure (HTML/PNG/PDF).

	Attributs :
		- _pt (:class:`PALMTracer <palm_tracer.PALMTracer>`) : Référence vers l'instance principale de PALMTracer (aucune copie).
		- _fig  (:class:`Optional[go.Figure]`) : Dernière figure Plotly produite (pour export/maj).
		- _html  (:class:`Optional[str]`)  : Dernier HTML généré pour la figure (export .html).
		- _grapher  (:class:`Grapher <palm_tracer.Processing.Grapher>`) : Utilitaire de création de figures (histogrammes, scatter, etc.).
		- _file  (:class:`str`) : Chemin du fichier image courant (TIF).

	Remarques :
		- Les boutons de domaine "Localization"/"Tracking" sont automatiquement désactivés si
		  aucune donnée correspondante n'est trouvée (cf. :meth:`_refresh_source_buttons`).
		- L'export PNG utilise un fallback par capture du widget Qt si Kaleido n'est pas utilisé.
	"""
	UI_NAME: str = "Graph Viewer"

	# ==================================================
	# region Initialisation
	# ==================================================
	##################################################
	def __init__(self, palmtracer: PALMTracer | None = None):
		"""
		Initialise le widget (UI, connexions, état initial) et lie PALMTracer.

		:param palmtracer: Instance principale :class:`PALMTracer <palm_tracer.PALMTracer>` sans copie (référence partagée).
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

		main_layout = QHBoxLayout(self)
		Ui.init_layout(main_layout)

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
		main_layout.addWidget(left)
		main_layout.addWidget(self._web, stretch=1)

		# --- Boutton pour charger une stack ---
		self._btn_add_stack = QPushButton("Add Stack")
		self._btn_add_stack.setToolTip(TIPS["Add Stack"])

		# --- Bloc Infos (lecture seule) ---
		grp_infos, self._status = Ui.make_file_info_group()

		# --- Bloc Source (donnée) + Type de graphe ---
		grp_source = QGroupBox("Source")
		form = Ui.make_form(grp_source)
		for key in self._graph_settings:
			if isinstance(self._graph_settings[key], BaseSettingType):
				self._graph_settings[key].get_ui(self.UI_NAME).attach_to_form(form)
				if isinstance(self._graph_settings[key], Combo):
					self._graph_settings[key].get_ui(self.UI_NAME).boxes[0].setMinimumWidth(200)

		# --- Bloc Affichage (2 colonnes) ---
		display_settings = cast(GraphDisplay, self._graph_settings["Display"])
		grp_display = QGroupBox("Display")
		grid = QGridLayout(grp_display)
		Ui.init_layout(grid)
		for i, key in enumerate(display_settings):
			row, col = i // 2, (i % 2) * 2
			ui = display_settings[key].get_ui(self.UI_NAME)
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
		scroll_layout.addWidget(grp_infos)
		scroll_layout.addWidget(grp_source)
		scroll_layout.addWidget(grp_display)
		scroll_layout.addWidget(grp_filters)
		scroll_layout.addStretch()  # Optionnel mais recommandé

		# --- Mise en page globbale ---
		vbox.addWidget(self._btn_add_stack)
		vbox.addWidget(scroll_area)
		vbox.addLayout(actions_row)

		# --- Affiche / masque les éléments en fonction des paramètres initiaux ---
		self._graph_settings.toggle_src(self._graph_settings["Source"].value)
		self._toggle_type(self._graph_settings["Type"].value)
		self._toggle_dual(self._graph_settings["Dual"].value)
		self._graph_settings["Display"]["Limits"].value = True

	##################################################
	def _connect_signals(self):
		"""Connecte les signaux UI aux callbacks."""
		# Connexion des bouttons Filters de cette UI
		self._pt.connect_filters_button(self.UI_NAME)

		self._btn_add_stack.clicked.connect(self._add_stack)

		# Sources
		self._graph_settings["Type"].connect(self._toggle_type)
		self._graph_settings["Dual"].connect(self._toggle_dual)

		# Settings Connexion
		self._graph_settings.connect(self._update_plot)
		self._filters.connect_button(self._actualize, self.UI_NAME, "reset")
		self._filters.connect_button(self._actualize, self.UI_NAME, "update")

		# Action Row a supprimer
		self._btn_actualize.clicked.connect(self._actualize)
		self._btn_export.clicked.connect(self._on_export)

	# ==================================================
	# endregion Initialisation
	# ==================================================

	# ==================================================
	# region UI Callback
	# ==================================================
	##################################################
	def _toggle_type(self, btn_id: int) -> None:
		"""
		Mets à jour la liste des sources selon le domaine choisi puis redessine.

		:param btn_id: Identifiant du bouton domaine sélectionné (0=Stack, 1=Localization, 2=Tracking).
		"""
		# Remplir la ComboBox 'Source' en fonction du domaine
		self._graph_settings.update_src(self._get_optionnal())

		if btn_id == 0:  # Localisation
			self._filters["Localization"].get_ui(self.UI_NAME).show()
			self._filters["Tracks"].get_ui(self.UI_NAME).hide()
		else:  # Tracking
			self._filters["Localization"].get_ui(self.UI_NAME).hide()
			self._filters["Tracks"].get_ui(self.UI_NAME).show()

	##################################################
	def _toggle_dual(self, value: bool) -> None:
		"""Affiche/Masque la seconde source."""
		self._graph_settings["Source B"].show() if value else self._graph_settings["Source B"].hide()
		self._graph_settings.update_src(self._get_optionnal())

	##################################################
	def _get_optionnal(self) -> list[str]:
		"""
		Génère la liste des variables d'intérêt pour les Trajectoires en fonction des fichiers disponibles.

		:return: La liste des sources disponibles pour les trajectoires.
		"""
		if self._graph_settings["Type"].value == 0: return []
		res: list[str] = []
		tc = self._pt.tracks_compute
		if not tc["MSD"].empty: res += ["MSD"]
		if not tc["InD"].empty: res += ["Instant D"]
		if not tc["Fit"].empty: res += tc["Fit"].columns[2:].tolist()
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
		self._actualize()  # Actualisation des statuts

	##################################################
	def _actualize(self):
		"""Actualise les status des fichiers/données depuis l'état PALMTracer et redessine le graph."""
		file = cast(FileList, self._pt.settings.batch["Files"]).current_text
		self._status["File"].setText(Path(file).name if file else "No File")
		# Mise à jour des Status
		status = self._pt.get_status()
		for key in status: self._status[key].setText(status[key])
		self._graph_settings["Display"]["Limits"].value = True
		self._update_plot()  # Puis redessiner le graphe.

	# ==================================================
	# endregion PALMTracer Link
	# ==================================================

	# ==================================================
	# region Drawing
	# ==================================================
	##################################################
	def _update_plot(self):
		"""Construit la figure Plotly courante en fonction du domaine et de la source."""
		s = self._graph_settings.settings
		src_id, dual = s["Type"], s["Dual"]
		src_a = cast(Combo, self._graph_settings["Source"]).current_text
		limit, sigma = s["Display Limits"], s["Display Sigma"]
		kde, gauss = s["Display KDE"], s["Display Gauss"]
		density, cumul = True, s["Display Cumul"]

		# Préparation des Données
		data, title = self._get_data()
		# print(f"{data.shape}, {data.size}, {title}") with data.size over 10M make a warning box

		# Selection du graphique à afficher
		if src_id == 0 and src_a == "Localizations Count":
			self._fig = self._grapher.scatter(data, title, xlabel="Plane", ylabel="Count", limit=limit, show_sigma=sigma)
		elif src_id == 1 and src_a == "Length":
			self._fig = self._grapher.scatter(data, title, xlabel="Track", ylabel="Length", limit=limit, show_sigma=sigma)
		elif dual:
			src_b = cast(Combo, self._graph_settings["Source B"]).current_text
			self._fig = self._grapher.cloud(data, title, xlabel=src_a, ylabel=src_b, limit=limit, show_sigma=sigma, kde=kde, gaussian=gauss)
		else:
			self._fig = self._grapher.histogram(data, title, limit=limit, show_sigma=sigma, kde=kde, gaussian=gauss, density=density, cumulative=cumul)

		self._update_web_widget()

	##################################################
	def _get_data(self) -> tuple[np.ndarray, str]:
		"""Récupère et prépare les données pour l'affichage."""
		s = self._graph_settings.settings
		src_id, dual, log_scale = s["Type"], s["Dual"], s["Display Log Scale"]
		src_a = cast(Combo, self._graph_settings["Source"]).current_text

		d, t = self._get_data_from_src(src_id, src_a, log_scale)
		if dual:
			src_b = cast(Combo, self._graph_settings["Source B"]).current_text
			t += f" / {src_b}"
			d_b, _ = self._get_data_from_src(src_id, src_b, log_scale)
			if d.ndim == 2: d = d[:, 1]
			if d_b.ndim == 2: d_b = d_b[:, 1]
			if d_b.size != d.size: return np.empty(0), t
			d = np.column_stack((d, d_b))

		return d, t

	##################################################
	def _get_data_from_src(self, src_id, src: str, log_scale: bool = False) -> tuple[np.ndarray, str]:
		"""Récupère et prépare les données pour l'affichage."""
		# Localizations
		if src_id == 0:
			title = f"Localizations {src}"
			df = self._pt.localizations
			if df.empty:  return np.empty(0), title
			if src == "Localizations Count":
				s = df["Plane"].astype(np.int64)
				planes = np.arange(int(s.min()), int(s.max()) + 1, dtype=int)  # Récupération des plans du min au max (si plans vides, ils seront compris)
				counts = (s.groupby(s).size().reindex(pd.Index(planes), fill_value=0).to_numpy(dtype=int))  # Comptage par groupe
				return np.column_stack((planes, counts)), src

			s = df.get(src)  # None si la colonne n'existe pas
			if s is None: return np.empty(0), title
			return self._log_data(s.to_numpy(dtype=float), log_scale), title

		# Tracks
		title = f"Tracks {src}"
		if src == "Length":  # Cas particulier, il est peut-être dans le tableau Fit, mais on va utiliser le tableau Tracks initial.
			df = self._pt.tracks
			if df.empty: return np.empty(0), title
			group = df.groupby("Track")["Plane"].agg(["min", "max"])  # Groupement par track + calcul min et max
			group["delta"] = group["max"] - group["min"]  # .							  Calcul du delta
			res = np.column_stack((group.index.to_numpy(), group["delta"].to_numpy()))  # Conversion vers numpy 2D : colonne Track + delta
			return res, title

		df = self._pt.tracks_compute
		if src == "MSD":
			df = df["MSD"]
			if df.empty: return np.empty(0), title
			step = self._graph_settings["MSD Step"].value  # .										Récupération du numéro du Step.
			col = f"Step {step}"  # .																Récupération du nom de la colonne.
			title += f" {col}"
			if not {"Track", col}.issubset(df.columns): return np.empty(0), title  # .				Vérification de présence des colonnes
			track, values = df["Track"].astype(int).to_numpy(), df[col].astype(float).to_numpy()  # Séparation track et valeur
			df = np.column_stack((track, self._log_data(values, log_scale)))  # .					Application du log sur les valeurs
			return df[np.isfinite(df).all(axis=1)], title  # .										Retour avec filtrage des Lignes NaN

		if src == "Instant D":
			df = df["InD"].drop(columns=["Track"], errors="ignore").to_numpy().ravel()  # .			Récupération des colonnes
			if df.size == 0: return np.empty(0), title
			df = self._log_data(df, log_scale)  # .													Application du log sur les valeurs
			return df[np.isfinite(df)], title  # .													Retour avec filtrage des Lignes NaN

		df = df["Fit"]
		if df.empty: return np.empty(0), title
		if not {"Track", src}.issubset(df.columns): return np.empty(0), title  # .					Vérification de présence des colonnes
		track, values = df["Track"].astype(int).to_numpy(), df[src].astype(float).to_numpy()  # .	Séparation track et valeur
		df = np.column_stack((track, self._log_data(values, log_scale)))  # .						Application du log sur les valeurs
		return df[np.isfinite(df).all(axis=1)], title  # .											Retour avec filtrage des Lignes NaN

	##################################################
	@staticmethod
	def _log_data(data: np.ndarray, log: bool) -> np.ndarray:
		"""
		Application du log avec suppression du warning pour les valeurs ≤ 0 et remplacement par Nan de ces valeurs.

		:param data: Données à transformer
		:param log: Application du log ou non
		:return: Données transformées
		"""
		with np.errstate(divide='ignore', invalid='ignore'): return np.where(data > 0, np.log10(data), np.nan) if log else data


##################################################
if __name__ == "__main__":
	import sys

	app = QApplication(sys.argv)
	w = GraphViewerWidget()
	w.resize(1280, 720)
	w.show()
	sys.exit(app.exec_())
