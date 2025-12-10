"""

"""

import napari
from qtpy.QtWidgets import QWidget


class ViewerHRWidget(QWidget):
	"""
	Widget d'affichage HR pour un viewer napari.

	Ce widget permet :
		- de charger un fichier CSV contenant des localisations ou des trajectoires
		- de modifier la taille des points

	**Remarque** : peut être lancé directement avec la commande ``napari -w palm-tracer "Viewer HR"``

	:param viewer: Instance du viewer napari où sera ajouté le calque HR.
	:type viewer: :class:`napari.Viewer`
	"""

	##################################################
	def __init__(self, viewer: napari.Viewer):
		"""
		Initialise le widget et configure l'interface graphique (boutons, champs numériques, checkbox).

		La création du calque napari se fait plus tard dans :meth:`update_layer` lorsqu'un fichier CSV est chargé.

		:param viewer: Viewer napari cible.
		:type viewer: :class:`napari.Viewer`
		"""
		super().__init__()
		self.viewer = viewer

##################################################
def create_viewerhr() -> napari.Viewer:  # pragma: no cover
	"""
	Crée une nouvelle fenêtre napari HR, sans menu,
	et y ajoute le ViewerHRWidget docké à droite.

	Cette fonction NE lance PAS napari.run() : elle est faite
	pour être appelée depuis un plugin, donc dans une appli Qt déjà active.
	"""
	viewer = napari.Viewer(ndisplay=3)									   # Crée le viewer HR napari
	viewer.title = "HR Viewer"											   # Modifier le titre de la fenêtre
	viewer.window.main_menu.setVisible(False)							   # Cacher la barre de menu
	widget = ViewerHRWidget(viewer)										   # Crée le widget en lui passant le viewer
	viewer.window.add_dock_widget(widget, name="Viewer HR", area="right")  # L'ajoute comme dock widget dans la fenêtre napari
	return viewer


##################################################
def open_viewerhr(_viewer: "napari.viewer.Viewer" = None, ) -> QWidget:  # pragma: no cover
	"""
	Callable utilisé par napari pour le menu Plugins > PALM Tracer > Viewer HR.

	- Ignore le viewer courant.
	- Crée une nouvelle fenêtre napari HR dédiée.
	- Retourne un QWidget stub (caché) juste pour satisfaire
	  l'API "widget plugin" de napari.
	"""
	# Crée la nouvelle fenêtre HR
	create_viewerhr()

	# Stub minimal pour napari (sera docké, mais caché)
	stub = QWidget()
	stub.hide()
	return stub


##################################################
if __name__ == "__main__":  # pragma: no cover
	import napari

	_v = create_viewerhr()
	napari.run()  # Lance la boucle Qt gérée par napari
