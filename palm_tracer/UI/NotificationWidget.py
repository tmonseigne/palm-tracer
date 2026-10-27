"""Fournit une notification locale réutilisable avec fermeture manuelle et fondu automatique."""

from __future__ import annotations

from typing import Literal

from qtpy.QtCore import QEasingCurve, QPropertyAnimation, Qt, QTimer
from qtpy.QtWidgets import QFrame, QGraphicsOpacityEffect, QHBoxLayout, QLabel, QSizePolicy, QStyle, QToolButton, QWidget

from palm_tracer.Tools import Ui

#: Niveaux de présentation des notifications locales.
NotificationLevel = Literal["info", "success", "warning", "error"]


# --------------------------------------------------
class NotificationWidget(QFrame):
	"""
	Affiche un message superposé dans le coin inférieur droit de son parent, sans prendre le focus.

	Une seule instance est réutilisée : chaque nouveau message remplace le précédent et réinitialise son délai et son opacité.
	La notification ne fait partie d'aucun layout et ne change donc pas la disposition des commandes.
	Toutes ses méthodes doivent être appelées depuis le thread graphique.

	:param parent: Panneau ou fenêtre délimitant la notification.
	"""

	MAXIMUM_WIDTH: int = 380
	"""Largeur maximale de la notification, en pixels logiques."""
	MARGIN: int = 12
	"""Distance souhaitée aux bords du parent, en pixels logiques."""
	FADE_DURATION: int = 300
	"""Durée du fondu de fermeture, en millisecondes."""

	# ==================================================
	# region Initialisation
	# ==================================================
	def __init__(self, parent: QWidget):
		"""
		Construit le message, son icône, sa fermeture et les objets de temporisation.

		:param parent: Widget propriétaire de la notification.
		"""
		super().__init__(parent)
		self.setObjectName("pt_notification")
		self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
		self.setStyleSheet(Ui.STYLESHEET_NOTIFICATION)

		self._icon = QLabel(self)
		self._icon.setFixedSize(20, 20)
		self._icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

		self._message = QLabel(self)
		self._message.setWordWrap(True)
		self._message.setTextFormat(Qt.TextFormat.PlainText)
		self._message.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

		self._close_button = QToolButton(self)
		self._close_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarCloseButton))
		self._close_button.setToolTip("Dismiss notification")
		self._close_button.setAccessibleName("Dismiss notification")
		self._close_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
		self._close_button.clicked.connect(self.dismiss)

		layout = QHBoxLayout(self)
		layout.setContentsMargins(12, 10, 8, 10)
		layout.setSpacing(8)
		layout.addWidget(self._icon, 0, Qt.AlignmentFlag.AlignTop)
		layout.addWidget(self._message, 1)
		layout.addWidget(self._close_button, 0, Qt.AlignmentFlag.AlignTop)

		self._opacity = QGraphicsOpacityEffect(self)
		self._opacity.setOpacity(1.0)
		self.setGraphicsEffect(self._opacity)

		self._fade = QPropertyAnimation(self._opacity, b"opacity", self)
		self._fade.setDuration(self.FADE_DURATION)
		self._fade.setEasingCurve(QEasingCurve.Type.InOutQuad)
		self._fade.finished.connect(self.dismiss)
		self._timer = QTimer(self)
		self._timer.setSingleShot(True)
		self._timer.timeout.connect(self._start_fade)

		self.hide()

	# ==================================================
	# endregion Initialisation
	# ==================================================

	# ==================================================
	# region Affichage
	# ==================================================
	def show_message(self, message: str, level: NotificationLevel = "info", duration_ms: int = 3000):
		"""
		Remplace le message courant et programme son fondu après le délai demandé.

		:param message: Texte brut à afficher ; il n'est jamais interprété comme du HTML.
		:param level: Niveau déterminant l'icône et la couleur de la bordure.
		:param duration_ms: Délai avant fondu en millisecondes ; zéro conserve le message jusqu'à sa fermeture manuelle.
		:raises ValueError: Si le niveau est inconnu ou le délai négatif.
		"""
		icons = {"info":    QStyle.StandardPixmap.SP_MessageBoxInformation, "success": QStyle.StandardPixmap.SP_DialogApplyButton,
				 "warning": QStyle.StandardPixmap.SP_MessageBoxWarning, "error": QStyle.StandardPixmap.SP_MessageBoxCritical}
		if level not in icons or duration_ms < 0:
			raise ValueError("Niveau de notification inconnu ou délai négatif.")
		self._timer.stop()
		self._fade.stop()
		self._opacity.setOpacity(1.0)
		self._message.setText(message)
		self.setToolTip(message)  # Le texte complet reste accessible lorsque la place disponible impose un affichage tronqué.
		self.setProperty("level", level)
		self.style().unpolish(self)
		self.style().polish(self)
		self._icon.setPixmap(self.style().standardIcon(icons[level]).pixmap(20, 20))
		self.reposition()
		self.show()
		self.raise_()
		if duration_ms: self._timer.start(duration_ms)

	# --------------------------------------------------
	def reposition(self):
		"""Ajuste la taille au parent et replace la notification sans modifier les layouts environnants."""
		parent = self.parentWidget()
		if parent is None: return
		margin = min(self.MARGIN, max(0, min(parent.width(), parent.height()) // 8))
		width = min(self.MAXIMUM_WIDTH, max(1, parent.width() - 2 * margin))
		maximum_height = max(1, parent.height() - 2 * margin)
		self.setMaximumSize(width, maximum_height)
		layout = self.layout()
		height = layout.totalHeightForWidth(width) if layout.hasHeightForWidth() else self.sizeHint().height()
		self.resize(width, min(maximum_height, max(1, height)))
		self.move(max(0, parent.width() - self.width() - margin), max(0, parent.height() - self.height() - margin))

	# --------------------------------------------------
	def _start_fade(self):
		"""Démarre le fondu du message courant après expiration du délai."""
		self._fade.setStartValue(self._opacity.opacity())
		self._fade.setEndValue(0.0)
		self._fade.start()

	# --------------------------------------------------
	def dismiss(self):
		"""Ferme immédiatement la notification et annule toute temporisation ou animation en cours."""
		self._timer.stop()
		self._fade.stop()
		self.hide()
		self._opacity.setOpacity(1.0)
