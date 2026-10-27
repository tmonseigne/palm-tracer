"""Teste les notifications locales, leur remplacement et leur transmission au thread Qt."""

from threading import Thread

import pytest

from palm_tracer.UI.BaseWidget import BaseWidget
from palm_tracer.UI.NotificationWidget import NotificationWidget
from tests.Utils import strip_ansi


# --------------------------------------------------
@pytest.fixture
def notification_panel(qtbot):
	"""Crée un panneau visible afin d'observer ses notifications sans autre interface métier."""
	panel = BaseWidget()
	qtbot.addWidget(panel)
	panel.resize(600, 300)
	panel.show()
	return panel


# ==================================================
# region Affichage
# ==================================================
@pytest.mark.parametrize("level", ["info", "success", "warning", "error"], ids=["information", "success", "warning", "error"])
def test_notification_prints_once_and_displays_level(notification_panel, capsys, level):
	"""Vérifie qu'un appel unique produit le texte console et la notification du niveau demandé."""
	getattr(notification_panel, f"notify_{level}")("Message <b>brut</b>", duration_ms=0)
	notification = notification_panel._notification
	assert notification.isVisible()
	assert notification.property("level") == level
	assert notification._message.text() == "Message <b>brut</b>"
	assert strip_ansi(capsys.readouterr().out).splitlines() == ["Message <b>brut</b>"]


# --------------------------------------------------
def test_notification_replaces_message_during_fade(notification_panel, qtbot):
	"""Vérifie que le nouveau message reste seul et visible après l'échéance du fondu précédent."""
	notification_panel.notify_info("Premier message")
	notification = notification_panel._notification
	notification._start_fade()
	notification._fade.setCurrentTime(notification.FADE_DURATION // 2)

	notification_panel.notify_error("Nouveau message", duration_ms=0)
	qtbot.wait(notification.FADE_DURATION + 50)
	notification = notification_panel._notification

	assert len(notification_panel.findChildren(NotificationWidget)) == 1
	assert notification._message.text() == "Nouveau message"
	assert notification._opacity.opacity() == 1.0
	assert notification.isVisible()


# --------------------------------------------------
def test_notification_fades_and_disappears(notification_panel, qtbot):
	"""Vérifie le cycle réel du temporisateur puis du fondu jusqu'au masquage."""
	notification_panel.notify_info("Message temporaire", duration_ms=10)
	notification = notification_panel._notification
	qtbot.waitUntil(lambda: not notification.isVisible(), timeout=2000)


# --------------------------------------------------
def test_notification_close_button_cancels_pending_fade(notification_panel):
	"""Vérifie que la fermeture manuelle stoppe le délai et permet de réutiliser la notification."""
	notification_panel.notify_warning("À fermer")
	notification = notification_panel._notification
	notification._close_button.click()
	assert not notification.isVisible()
	notification_panel.notify_info("Réouverture", duration_ms=0)
	assert notification_panel._notification.isVisible()


# --------------------------------------------------
@pytest.mark.parametrize("size", [(600, 300), (180, 120)], ids=["wide-panel", "narrow-panel"])
def test_notification_stays_inside_panel_after_resize(notification_panel, size):
	"""Vérifie que la notification reste dans le coin inférieur droit, même dans un panneau étroit."""
	notification_panel.notify_info("Un message assez long pour occuper plusieurs lignes dans un panneau étroit.", duration_ms=0)
	notification_panel.resize(*size)
	notification = notification_panel._notification
	assert notification_panel.rect().contains(notification.geometry())
	assert notification_panel.width() - notification.geometry().right() <= notification.MARGIN + 1
	assert notification_panel.height() - notification.geometry().bottom() <= notification.MARGIN + 1


# --------------------------------------------------
def test_notification_is_delivered_from_worker(notification_panel, qtbot):
	"""Vérifie qu'une demande d'un thread Python crée le composant uniquement dans le thread du panneau."""
	worker = Thread(target=notification_panel.notify_warning, args=("Message du worker",), kwargs={"duration_ms": 0})
	worker.start()
	worker.join(timeout=2)
	assert not worker.is_alive()
	qtbot.waitUntil(lambda: notification_panel._notification is not None, timeout=2000)
	notification = notification_panel._notification
	assert notification.thread() is notification_panel.thread()
	assert notification._message.text() == "Message du worker"
	assert notification.isVisible()


# --------------------------------------------------
def test_hidden_panel_only_prints_message(qtbot, capsys):
	"""Conserve le diagnostic console sans créer de notification pour un panneau masqué."""
	panel = BaseWidget()
	qtbot.addWidget(panel)
	panel.notify_error("Panneau masqué")
	assert panel._notification is None
	assert strip_ansi(capsys.readouterr().out).splitlines() == ["Panneau masqué"]


# --------------------------------------------------
def test_hiding_panel_cancels_notification(notification_panel):
	"""Vérifie qu'un panneau masqué puis réaffiché ne montre pas un ancien message."""
	notification_panel.notify_info("Ancien message")
	notification = notification_panel._notification
	notification_panel.hide()
	notification_panel.show()
	assert not notification.isVisible()


# --------------------------------------------------
@pytest.mark.parametrize("level, duration", [("unknown", 4000), ("info", -1)], ids=["unknown-level", "negative-duration"])
def test_notification_rejects_invalid_options(notification_panel, capsys, level, duration):
	"""Vérifie la validation avant toute écriture console ou création de notification."""
	with pytest.raises(ValueError): notification_panel.notify("Invalide", level, duration)
	assert capsys.readouterr().out == ""


# ==================================================
# endregion Affichage
# ==================================================
