"""Module contenant la classe mère :class:`StandAloneWidget`, permettant de centraliser des fonctions communes aux widgets Stand Alone."""

from pathlib import Path
from typing import Any, Optional

import plotly.graph_objects as go
import plotly.io as pio
from qtpy.QtCore import Qt
from qtpy.QtGui import QCloseEvent
from qtpy.QtWidgets import QDoubleSpinBox, QFileDialog, QFormLayout, QFrame, QGroupBox, QHBoxLayout, QLayout, QSpinBox, QTextBrowser, QVBoxLayout, QWidget

# Tentative d'import QtWebEngine (via qtpy)
try:
	from qtpy.QtWebEngineWidgets import QWebEngineView  # type: ignore

	_HAS_WEBENGINE = True
except Exception:
	QWebEngineView = None  # type: ignore
	_HAS_WEBENGINE = False


##################################################
class StandAloneWidget(QWidget):
	"""Classe mère avec les fonctions interne aux widgets Stand Alone (Hors Napari)."""

	# ==================================================
	# region Constants
	# ==================================================
	STYLESHEET_INFO: str = "color: #666666; font-style: italic; padding: 2px;"

	STYLESHEET_GENERAL: str = """
				QPushButton { border: 1px solid #c7c7c7; padding: 5px; background: #f7f7f7; }
				QPushButton + QPushButton { border-left: none; } /* fusion visuelle */
				QPushButton:first-child { border-top-left-radius: 5px; border-bottom-left-radius: 5px; }
				QPushButton:last-child { border-top-right-radius: 5px; border-bottom-right-radius: 5px; }
				QPushButton:pressed { background: #e9eff7; border-color: #6aa0e8; }
				QPushButton:checked	{ background: #e9eff7; border-color: #6aa0e8; }
				QPushButton:disabled { color: #999; background: #fafafa; }
				"""

	CONFIG_PLOTLY: dict[str, Any] = {
			"responsive":             True,
			"displayModeBar":         True,
			"displaylogo":            False,
			"modeBarButtonsToRemove": ["zoom2d", "pan2d", "select2d", "lasso2d", "zoomIn2d", "zoomOut2d", "autoScale2d",
									   "resetScale2d", "hoverClosestCartesian", "hoverCompareCartesian"],
			"toImageButtonOptions":   dict(format="png", height=1200, width=1200, scale=2)}

	COMMON_SPACE: int = 10

	# ==================================================
	# endregion Constants
	# ==================================================

	##################################################
	def __init__(self, parent: Optional[QWidget] = None):
		"""
		Construit le widget et initialise l'interface.

		:param parent: Widget parent Qt, ou :obj:`None` si widget racine.
		"""
		super().__init__(parent)

		# On applique un style général aux QPushButton
		self.setStyleSheet(self.STYLESHEET_GENERAL)

	# ==================================================
	# region UI Build
	# ==================================================
	##################################################
	@staticmethod
	def _add_setting_row(form: QFormLayout, label: str, widget: QWidget):
		"""
		Ajoute une ligne de paramètre dans un :class:`QFormLayout`.

		Le champ (colonne de droite) est encapsulé dans un :class:`QHBoxLayout`	contenant le widget puis un ``stretch``.
		Cela évite que le widget s'étire horizontalement jusqu'au bord droit de l'onglet : il conserve sa taille naturelle (*sizeHint*) et l'espace	restant est
		laissé vide à droite.

		:param form: Formulaire cible à modifier (modification in-place via :meth:`addRow`).
		:param label: Texte du label (colonne de gauche).
		:param widget: Widget à placer dans la colonne de droite (spinbox, checkbox, combobox, ...).
		"""
		layout = QHBoxLayout()
		layout.setContentsMargins(0, 0, 0, 0)
		layout.addWidget(widget)
		layout.addStretch(1)  # pousse tout à gauche, espace vide à droite
		form.addRow(label, layout)

	##################################################
	@staticmethod
	def _init_layout(layout: QLayout, space: int = COMMON_SPACE):
		"""
		Configure un layout avec des marges et un espacement uniformes.

		Cette fonction applique des marges identiques sur les 4 côtés et un espacement identique entre widgets / sous-layouts.

		:param layout: Layout à configurer (ex: :class:`QVBoxLayout`, :class:`QGridLayout`, etc.).
		:param space: Valeur (en pixels) utilisée pour les marges et l'espacement du layout. Par défaut : ``COMMON_SPACE``.
		"""
		layout.setContentsMargins(space, space, space, space)
		layout.setSpacing(space)

	##################################################
	def _make_tab(self, parent: QWidget | None, space: int = COMMON_SPACE) -> tuple[QWidget, QVBoxLayout]:
		"""
		Crée un onglet prêt à l'emploi (widget conteneur + layout vertical).

		L'onglet est représenté par un :class:`QWidget` et contient un :class:`QVBoxLayout` configuré avec des marges et un espacement uniformes.

		:param parent: Parent Qt du widget onglet (peut être ``None`` si défini plus tard).
		:param space: Valeur (en pixels) utilisée pour les marges et l'espacement du layout. Par défaut : ``COMMON_SPACE``.

		:return: Un tuple ``(tab, layout)`` où ``tab`` est le widget de l'onglet et ``layout`` son calque.
		"""
		tab = QWidget(parent)
		layout = QVBoxLayout(tab)
		self._init_layout(layout, space)
		return tab, layout

	##################################################
	def _make_group(self, parent: QWidget | None, name: str, space: int = COMMON_SPACE) -> tuple[QGroupBox, QVBoxLayout]:
		"""
		Crée un :class:`QGroupBox` avec un layout vertical configuré.

		:param parent: Parent Qt du group box (peut être ``None`` si défini plus tard).
		:param name: Titre affiché dans l'entête du group box.
		:param space: Valeur (en pixels) utilisée pour les marges et l'espacement du layout. Par défaut : ``COMMON_SPACE``.

		:return: Un tuple ``(group, layout)`` où : ``group`` est le :class:`QGroupBox` créé et ``layout`` son calque.
		"""
		group = QGroupBox(name, parent)
		layout = QVBoxLayout(group)
		self._init_layout(layout, space)
		return group, layout

	##################################################
	@staticmethod
	def _make_form(parent: QWidget | None, space: int = COMMON_SPACE) -> QFormLayout:
		"""
		Crée et configure un :class:`QFormLayout` pour des paramètres.

		Configuration appliquée :
		- labels alignés à droite et centrés verticalement ;
		- formulaire ancré en haut à gauche ;
		- espacements horizontaux/verticaux adaptés à une UI de réglages ;
		- politique de croissance des champs : les widgets de droite restent à leur *sizeHint* (évite qu'ils s'étirent jusqu'au bord droit).

		:param parent: Parent Qt du layout (peut être ``None`` si défini plus tard).
		:param space: Valeur (en pixels) utilisée pour les marges et l'espacement du layout. Par défaut : ``COMMON_SPACE``.

		:return: Le :class:`QFormLayout` configuré.
		"""
		form = QFormLayout(parent)
		form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
		form.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
		form.setHorizontalSpacing(space)
		form.setVerticalSpacing(space)
		form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.FieldsStayAtSizeHint)
		return form

	##################################################
	@staticmethod
	def _make_vertical_separator() -> QFrame:
		"""
		Crée un séparateur vertical discret.

		:return: Le :class:`QFrame` configuré.
		"""
		sep = QFrame()
		sep.setFrameShape(QFrame.Shape.VLine)
		sep.setFrameShadow(QFrame.Shadow.Sunken)
		sep.setStyleSheet("""QFrame {color: #B0B0B0;}""")
		return sep

	##################################################
	@staticmethod
	def _make_horizontal_separator() -> QFrame:
		"""
		Crée un séparateur horizontal discret.

		:return: Le :class:`QFrame` configuré.
		"""
		sep = QFrame()
		sep.setFrameShape(QFrame.Shape.HLine)
		sep.setFrameShadow(QFrame.Shadow.Sunken)
		sep.setStyleSheet("QFrame { color: #B0B0B0; }")
		return sep

	# ==================================================
	# endregion UI Build
	# ==================================================

	# ==================================================
	# region Web Widget (for Plotly)
	# ==================================================
	##################################################
	def _make_web_widget(self):
		"""Créé un Widget pour integrer plotly
		:return: QWebEngineView ou QTextBrowser si indisponible
		"""
		# Zone droite : QWebEngineView avec Plotly
		if _HAS_WEBENGINE: res = QWebEngineView(self)
		else:  # pragma: no cover - Fallback affichant un message d'erreur explicite
			res = QTextBrowser(self)
			res.setText("<b>QtWebEngine unavailable</b><br>Install PyQtWebEngine for Plotly display.")
		return res

	##################################################
	def _update_web_widget(self, web: QWebEngineView | QTextBrowser, fig: go.Figure, config: dict[str, Any] | None = None):
		"""
		Créé un Widget pour integrer plotly
		:return: :class:`QWebEngineView` ou :class:`QTextBrowser` si indisponible
		"""
		if config is None: config = self.CONFIG_PLOTLY
		html = pio.to_html(fig, include_plotlyjs="cdn", full_html=False, config=config)
		self._fig = fig
		self._html = html
		if _HAS_WEBENGINE and isinstance(web, QWebEngineView): web.setHtml(html)
		else:  # pragma: no cover - Fallback affichant un message d'erreur explicite
			web.setText("<b>QtWebEngine unavailable</b><br>Install PyQtWebEngine for Plotly display.")

	##################################################
	def _connect_web_widget(self, web: QWebEngineView | QTextBrowser | None):
		"""Connecte les signaux des boutons aux callbacks."""
		if _HAS_WEBENGINE and isinstance(web, QWebEngineView):  # pragma: no cover Vérification en cas d'UI defectueuse
			profile = web.page().profile()
			profile.downloadRequested.connect(self._on_download_requested)

	# ==================================================
	# endregion Web Widget (for Plotly)
	# ==================================================

	# ==================================================
	# region Callbacks
	# ==================================================
	##################################################
	def _on_download_requested(self, download):
		"""
		Intercepte le téléchargement Plotly (Save image) pour demander
		explicitement où enregistrer le fichier.
		"""
		path, _ = QFileDialog.getSaveFileName(self, "Enregistrer l'image", str(self._download_initial_path()), "Images (*.png)")

		if not path:
			download.cancel()
			return

		path = Path(path)
		# Qt6: on règle le dossier + le nom de fichier séparément.
		download.setDownloadDirectory(str(path.parent))
		download.setDownloadFileName(path.name)
		download.accept()

	##################################################
	def _download_initial_path(self) -> Path:
		""" Renvoie un chemin initial pour le téléchargement par plotly. à Définir dans les classes filles."""
		return Path.cwd() / "image"

	##################################################
	@staticmethod
	def _sync_spin(target: QDoubleSpinBox | QSpinBox, value: float | int):
		"""
		Synchronise une spinbox avec la valeur envoyé (par signal).
		On bloque les signaux le temps de la mise à jour pour éviter les appels en série.

		:param target: Spinbox à mettre à jour.
		:param value: Valeur à insérer.
		"""
		target.blockSignals(True)
		target.setValue(value)
		target.blockSignals(False)

	# ==================================================
	# endregion Callbacks
	# ==================================================

	##################################################
	def closeEvent(self, event: QCloseEvent) -> None:
		"""Assure une destruction propre de QtWebEngine (évite warnings et crash à la sortie)."""
		try:
			if _HAS_WEBENGINE and hasattr(self, "_web") and isinstance(self._web, QWebEngineView):
				page = self._web.page()
				if page is not None:
					# Arrête chargements / timers internes WebEngine.
					page.triggerAction(page.WebAction.Stop)

					self._web.setHtml("")  # Optionnel: libère le contenu HTML pour réduire l'activité pendant le teardown.

					# Déconnecte proprement le signal de download (évite callbacks tardifs).
					try: page.profile().downloadRequested.disconnect(self._on_download_requested)
					except Exception: pass

					# Destruction différée (Qt-safe).
					page.deleteLater()

				self._web.deleteLater()
		# On ne doit jamais crasher sur un closeEvent durant des tests.
		except Exception: pass
		super().closeEvent(event)
