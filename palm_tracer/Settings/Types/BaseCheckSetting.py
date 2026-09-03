"""Définit la classe de base commune aux paramètres activables."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, cast

from qtpy.QtCore import QSignalBlocker
from qtpy.QtWidgets import QCheckBox

from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType


##################################################
@dataclass
class BaseCheckSetting(BaseSettingType):
	"""
	Définit le comportement commun d'un paramètre activable par une case à cocher.

	La première boîte de chaque interface associée doit être une
	:class:`~qtpy.QtWidgets.QCheckBox` représentant l'état d'activation.
	"""

	_active: bool = field(init=False, default=False)
	"""Indicateur d'activation du paramètre."""

	##################################################
	def reset(self):
		"""Réinitialise la valeur et désactive le paramètre."""
		super().reset()
		self.active = False

	# ==================================================
	# region Accesseurs
	# ==================================================
	##################################################
	@property
	def active(self) -> bool:
		"""Indique si le paramètre est actif."""
		return self._active

	##################################################
	@active.setter
	def active(self, value: bool):
		"""Modifie l'état actif et synchronise les interfaces associées."""
		if self._active == value: return
		self._active = value
		for ui in self._uis.values():
			checkbox = cast(QCheckBox, ui.boxes[0])
			with QSignalBlocker(checkbox): checkbox.setChecked(value)
		self.emit(value)

	# ==================================================
	# endregion Accesseurs
	# ==================================================

	# ==================================================
	# region Sérialisation
	# ==================================================
	##################################################
	def to_compact_dict(self) -> dict[str, Any]:
		"""Renvoie la valeur et l'état actif du paramètre."""
		return {**super().to_compact_dict(), "active": self.active}

	##################################################
	def update_from_compact_dict(self, data: dict[str, Any]):
		"""Met à jour la valeur et l'état actif depuis un dictionnaire minimal."""
		super().update_from_compact_dict(data)
		self.active = data["active"]

	# ==================================================
	# endregion Sérialisation
	# ==================================================

	# ==================================================
	# region Fonctions de rappel
	# ==================================================
	##################################################
	def set_active(self, state: bool):
		"""Met à jour l'état actif lorsque la case à cocher est modifiée."""
		self.active = state
