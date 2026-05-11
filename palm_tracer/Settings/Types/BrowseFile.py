"""
Fichier contenant la classe :class:`BrowseFile` dérivée de :class:`.BaseSettingType`, qui permet la gestion d'un paramètre type recherche de fichier.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, cast

from qtpy.QtCore import QSignalBlocker
from qtpy.QtWidgets import QFileDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton, QStyle,QApplication

from palm_tracer.Settings.Types.BaseSettingType import BaseSettingType
from palm_tracer.Settings.Types.BaseUI import BaseUI


##################################################
@dataclass
class BrowseFile(BaseSettingType):
	"""
	Classe pour un paramètre spécifique de type recherche de fichier.

	:param label: Nom du paramètre à afficher
	:param tooltip: Description détaillée en overlay.
	:param default: Valeur par défaut du paramètre.
	"""

	default: str = ""
	"""Valeur par défaut du paramètre (:class:`str`)."""
	_value: str = field(init=False, default="")
	"""Valeur actuelle du paramètre (:class:`str`)."""

	# ==================================================
	# region Getter/Setter
	# ==================================================
	##################################################
	def get_ui(self, name: str = "default") -> BaseUI:
		if name in self._uis: return self._uis[name]

		box: QLineEdit = QLineEdit()
		browse_button: QPushButton = QPushButton()
		browse_button.setIcon(QApplication.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon))
		browse_button.clicked.connect(self.browse_file)  # Connexion du bouton à la méthode de sélection

		ui = BaseUI(layout=QHBoxLayout(), label=QLabel(self.label), boxes=[box, browse_button])
		ui.set_tooltip(self.tooltip)  # .					Ajout du Tooltip

		box.textChanged.connect(self.set_value_from_ui)  # .Connecte le changement de valeur pour que les autres UI se mettent à jour

		# Disposer le QLineEdit et le bouton dans un calque horizontal
		ui.layout.addWidget(box)  # .						Ajout du champ de texte.
		ui.layout.addWidget(browse_button)  # .				Ajout du boutton.

		self._uis[name] = ui  # .							Ajoute l'ui au dictionnaire
		return ui

	##################################################
	@property
	def value(self) -> str:
		"""Valeur actuelle du paramètre (:class:`str`)."""
		return self._value

	##################################################
	@value.setter
	def value(self, value: str):
		"""Valeur actuelle du paramètre (:class:`str`)."""
		if self._value == value: return
		self._value = value
		for ui in self._uis.values():
			b = cast(QLineEdit, ui.boxes[0])
			with QSignalBlocker(b): b.setText(value)

		self.emit(value)

	# ==================================================
	# endregion Getter/Setter
	# ==================================================

	# ==================================================
	# region Callbacks
	# ==================================================
	##################################################
	def browse_file(self):
		"""Ouvre un dialogue de sélection de fichiers et mets à jour la boîte avec le chemin sélectionné."""
		current = Path(self.value)
		# Si le chemin par défaut n'est pas valide, on utilise le chemin principal du projet
		if not current.exists() or current == Path.cwd(): current = Path.cwd()
		path, _ = QFileDialog.getOpenFileName(None, "Sélectionner un fichier", str(current))
		if not path: return
		if Path(path).is_file(): self.value = path  # Mets à jour le chemin dans la boîte de texte


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QWidget, QFormLayout

	app = QApplication(sys.argv)
	w = QWidget()
	form = QFormLayout(w)  # crée et assigne le layout au widget
	setting = BrowseFile("Test", "tooltip")
	setting.get_ui("default").attach_to_form(form)
	setting.get_ui("second").attach_to_form(form)
	w.show()
	sys.exit(app.exec_())
