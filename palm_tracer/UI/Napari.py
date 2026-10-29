"""Retrouve le contexte PALM Tracer des outils ouverts depuis Napari."""

from __future__ import annotations

from typing import TYPE_CHECKING

import napari
from qtpy.QtWidgets import QLabel, QMenu, QWidgetAction

from palm_tracer.UI.BaseWidget import BaseWidget

if TYPE_CHECKING:
	from palm_tracer.PALMTracer import PALMTracer


# --------------------------------------------------
def install_plugin_menu_sections(viewer: napari.Viewer):
	"""
	Ajoute des titres discrets au sous-menu PALM Tracer lorsque le menu Plugins est ouvert.

	Les actions Napari et leur ordre sont conservés. Le branchement sur le menu parent permet de retrouver
	le sous-menu même après sa reconstruction par Napari, sans modifier son registre de commandes.
	Un modèle de viewer sans fenêtre, utilisé notamment par les tests des calques, ne nécessite aucun branchement.

	:param viewer: Visionneuse dont le menu Plugins doit être présenté par groupes.
	"""
	window = getattr(viewer, "window", None)
	if window is None: return
	plugins_menu = window.plugins_menu
	if plugins_menu.property("palm_tracer_sections_installed"): return
	plugins_menu.setProperty("palm_tracer_sections_installed", True)

	# --------------------------------------------------
	def prepare_sections():
		"""Retrouve uniquement le sous-menu de ce plugin parmi les menus générés par Napari."""
		for action in plugins_menu.actions():
			menu = action.menu()
			if menu is not None and menu.objectName() == "napari/plugins/palm-tracer":
				_add_plugin_menu_sections(menu)

	plugins_menu.aboutToShow.connect(prepare_sections)


# --------------------------------------------------
def _add_plugin_menu_sections(menu: QMenu):
	"""
	Insère les titres grisés avant les premières actions du widget principal, des viewers et des outils.

	:param menu: Sous-menu PALM Tracer contenant les actions créées par Napari.
	"""
	# Nettoie aussi les titres retirés par une reconstruction du menu, mais encore possédés par celui-ci.
	for child in menu.children():
		if isinstance(child, QWidgetAction) and child.objectName().startswith("palm-tracer.section."):
			menu.removeAction(child)
			child.deleteLater()

	sections = {"palm-tracer.make_qwidget": "Main widget", "palm-tracer.open_graphviewer": "Viewers", "palm-tracer.open_alignment": "Tools"}
	for action in menu.actions():
		title = sections.get(action.objectName())
		if title is None: continue
		label = QLabel(title, menu)
		label.setContentsMargins(12, 5, 12, 2)
		label.setEnabled(False)  # Utilise la couleur désactivée du thème Napari, sans couleur CSS imposée.
		header = QWidgetAction(menu)
		header.setObjectName(f"palm-tracer.section.{title}")
		header.setText(title)
		header.setDefaultWidget(label)
		header.setEnabled(False)
		menu.insertAction(action, header)


# --------------------------------------------------
def get_current_palmtracer(viewer: napari.Viewer | None = None) -> PALMTracer | None:
	"""
	Retrouve l'instance du widget principal dans la fenêtre Napari appelante.

	La recherche utilise uniquement les widgets dockés du viewer fourni ou actif, sans parcourir les parents Qt.
	L'absence de widget principal laisse la base du nouvel outil créer sa propre instance.
	Appeler cette fonction avant de créer une nouvelle fenêtre Napari, qui pourrait devenir le viewer actif.

	:param viewer: Visionneuse appelante, ou :obj:`None` pour utiliser la visionneuse active.
	:return: Instance du widget principal, ou :obj:`None` si aucun n'est présent dans cette fenêtre.
	"""
	if viewer is None: viewer = napari.current_viewer()
	if viewer is None: return None
	for widget in viewer.window.dock_widgets.values():
		# Le lancement comme script définit PALMTracerWidget dans __main__, distinct de la classe importée par le plugin.
		if isinstance(widget, BaseWidget) and widget.UI_NAME == "PALMTracer": return widget.pt
	return None
