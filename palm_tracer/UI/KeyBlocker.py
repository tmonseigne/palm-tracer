"""Petite classe permettant d'empêcher Napari de récupérer l'utilisation du clavier."""
from __future__ import annotations

from qtpy.QtCore import QEvent, QObject
from qtpy.QtGui import QKeyEvent
from qtpy.QtWidgets import QAbstractSpinBox, QLineEdit


class KeyBlocker(QObject):
	"""Empêche Napari de capturer certaines touches lorsqu'un widget d'édition a le focus."""

	def eventFilter(self, obj, event):
		"""
		Permet de filtrer la gestion du clavier si l'on est sur un objet QT éditable
		:param obj: Objet QT en cours
		:param event: Evenement clavier
		:return:
		"""
		# laisser le widget traiter la touche
		return event.type() == QEvent.Type.KeyPress and isinstance(event, QKeyEvent) and isinstance(obj.focusWidget(), (QAbstractSpinBox, QLineEdit))
