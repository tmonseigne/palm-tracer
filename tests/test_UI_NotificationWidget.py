"""Teste le composant de notification, son remplacement, son positionnement et son fondu."""

import pytest
from qtpy.QtWidgets import QWidget

from palm_tracer.UI.NotificationWidget import NotificationWidget


# --------------------------------------------------
@pytest.fixture
def notification_widget(qtbot):
	"""Crée une notification sur un simple parent Qt, sans dépendre de BaseWidget."""
	parent = QWidget()
	qtbot.addWidget(parent)
	parent.resize(600, 300)
	parent.show()
	yield NotificationWidget(parent)


# ==================================================
# region Affichage
# ==================================================
@pytest.mark.parametrize("level, duration", [("unknown", 4000), ("info", -1)], ids=["unknown-level", "negative-duration"])
def test_show_message_rejects_invalid_options(qtbot, level, duration):
	"""Vérifie directement le rejet d'un niveau inconnu ou d'un délai négatif par la notification."""
	parent = QWidget()
	qtbot.addWidget(parent)
	notification = NotificationWidget(parent)
	with pytest.raises(ValueError): notification.show_message("Invalide", level, duration)


# --------------------------------------------------
def test_notification_replaces_message_during_fade(notification_widget, qtbot):
	"""Vérifie que le nouveau message reste visible après l'échéance du fondu précédent."""
	notification = notification_widget
	notification.show_message("Premier message")
	notification._start_fade()
	notification._fade.setCurrentTime(notification.FADE_DURATION // 2)

	notification.show_message("Nouveau message", "error", duration_ms=0)
	qtbot.wait(notification.FADE_DURATION + 50)

	assert notification._message.text() == "Nouveau message"
	assert notification._opacity.opacity() == 1.0
	assert notification.isVisible()


# --------------------------------------------------
def test_notification_fades_and_disappears(notification_widget, qtbot):
	"""Vérifie le cycle réel du temporisateur puis du fondu jusqu'au masquage."""
	notification_widget.show_message("Message temporaire", duration_ms=10)
	qtbot.waitUntil(lambda: not notification_widget.isVisible(), timeout=5000)


# --------------------------------------------------
def test_notification_close_button_cancels_pending_fade(notification_widget):
	"""Vérifie que la fermeture manuelle permet de réutiliser la notification."""
	notification_widget.show_message("À fermer", "warning")
	notification_widget._close_button.click()
	assert not notification_widget.isVisible()
	notification_widget.show_message("Réouverture", duration_ms=0)
	assert notification_widget.isVisible()


# --------------------------------------------------
@pytest.mark.parametrize("size", [(600, 300), (180, 120)], ids=["wide-panel", "narrow-panel"])
def test_notification_stays_inside_panel_after_resize(notification_widget, size):
	"""Vérifie que la notification reste dans le coin inférieur droit, même dans un panneau étroit."""
	notification_widget.show_message("Un message assez long pour occuper plusieurs lignes dans un panneau étroit.", duration_ms=0)
	parent = notification_widget.parentWidget()
	parent.resize(*size)
	notification_widget.reposition()
	notification = notification_widget
	assert parent.rect().contains(notification.geometry())
	assert parent.width() - notification.geometry().right() <= notification.MARGIN + 1
	assert parent.height() - notification.geometry().bottom() <= notification.MARGIN + 1

# ==================================================
# endregion Affichage
# ==================================================
