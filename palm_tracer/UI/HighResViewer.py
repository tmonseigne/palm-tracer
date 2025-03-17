""" Module contenant la classe :class:`HighResViewer` pour l'affichage du résultat de la visualization de l'application. """
from typing import cast, Optional

import numpy as np
from qtpy.QtCore import Qt, QTimer
from qtpy.QtGui import QImage, QPainter, QPixmap
from qtpy.QtWidgets import QGraphicsPixmapItem, QGraphicsScene, QGraphicsView, QMainWindow


##################################################
class HighResViewer(QMainWindow):
	"""Fenêtre pour afficher une image avec zoom/dézoom."""

	##################################################
	def __init__(self, image: np.ndarray):
		super().__init__()

		self.setWindowTitle("High resolution visualization")
		self.setGeometry(100, 100, 800, 600)

		self.min_size = [400, 400]								# Taille minimale de la fenêtre (en pixels)
		self.max_size = [3840, 2160]					# Taille maximale de la fenêtre (en pixels, pour un écran 4K)
		self.wheel_speed = 1.2							# Facteur de zoom
		self.last_size = (self.width(), self.height())  # Dernière taille connue de la fenêtre

		# Création de la vue et de la scène
		self.view = QGraphicsView(self)
		self.scene = QGraphicsScene()
		self.view.setScene(self.scene)
		self.setCentralWidget(self.view)

		# Ajout de l'image
		self.image_item: Optional[QGraphicsPixmapItem] = None
		self.load_image(image)

		# Activation du zoom avec la molette de la souris
		self.view.setRenderHint(QPainter.Antialiasing, True)
		self.view.setDragMode(QGraphicsView.ScrollHandDrag)
		self.view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

	##################################################
	def load_image(self, image: np.ndarray):
		"""Charge et met à jour l'image affichée dans la fenêtre."""
		# Gestion d'images en niveau de Gris ou en RGB
		if image.dtype == np.uint16: image = (image / 256).astype(np.uint8)  # Normalisation si uint16
		height, width = image.shape[:2]
		bytes_per_line = width * 3 if image.ndim == 3 else width
		qformat = QImage.Format_RGB888 if image.ndim == 3 else QImage.Format_Grayscale8
		qimage = QImage(image.data, width, height, bytes_per_line, qformat)
		pixmap = QPixmap.fromImage(qimage)

		if self.image_item: self.scene.removeItem(self.image_item)  # Supprime l'ancienne image
		self.image_item = QGraphicsPixmapItem(pixmap)				# Création du conteneur de l'image
		self.scene.addItem(self.image_item)							# Ajout de l'image
		self.view.update()											# Forcer l'actualisation de la vue
		QTimer.singleShot(0, lambda: self.view.fitInView(self.image_item, Qt.AspectRatioMode.KeepAspectRatio))  # Utiliser QTimer pour attendre que la scène soit prête
		self._adjust_window_size(pixmap.width(), pixmap.height()) 	# Ajuster la taille de la fenêtre en fonction de l'image

	##################################################
	def _check_ratio(self, width: int, height: int):
		pixmap = cast(QGraphicsPixmapItem, self.image_item).pixmap()  # Récupérer le pixmap de l'image
		img_width = pixmap.width()									  # Largeur de l'image
		img_height = pixmap.height()								  # Hauteur de l'image
		aspect_ratio_img = img_width / img_height					  # Ratio d'aspect de l'image
		aspect_ratio_window = width / height						  # Ratio d'aspect de la fenêtre

		if aspect_ratio_img != aspect_ratio_window:
			if aspect_ratio_img > aspect_ratio_window: width = int(height * aspect_ratio_img)  # Si le ratio d'aspect de l'image est plus large
			else: height = int(width / aspect_ratio_img)									   # Si le ratio d'aspect de l'image est plus haut

		return width, height

	##################################################
	def _adjust_window_size(self, width: int, height: int, keep_ratio:bool = False):
		"""Ajuste la taille de la fenêtre en fonction de la taille de l'image."""
		width = int(np.clip(width, self.min_size[0], self.max_size[0]))
		height = int(np.clip(height, self.min_size[1], self.max_size[1]))
		if keep_ratio: width, height = self._check_ratio(width, height)  # Redimensionnement selon le ratio

		self.last_size = (width, height)  # Mettre à jour la taille précédente
		self.resize(width, height)		  # Ajuster la taille de la fenêtre
		self.view.fitInView(self.image_item, Qt.AspectRatioMode.KeepAspectRatio)  # Ajuster la vue pour correspondre à la taille de l'image

	##################################################
	def wheelEvent(self, event):
		"""Gestion du zoom avec la molette."""
		factor = self.wheel_speed if event.angleDelta().y() > 0 else 1 / self.wheel_speed
		self._adjust_window_size(int(self.view.width() * factor), int(self.view.height() * factor), True)

	##################################################
	def resizeEvent(self, event, **kwargs):
		"""Gère l'événement de redimensionnement de la fenêtre. """
		# Récupérer la nouvelle taille de la fenêtre
		width, height = event.size().width(), event.size().height()

		# Vérifier si la taille a changé de manière significative
		if (abs(width - self.last_size[0]) > 5) or (abs(height - self.last_size[1]) > 5):
			self._adjust_window_size(width, height)  # Appeler _adjust_window_size avec les nouvelles dimensions
