"""Définit la représentation Qt des résultats de PALMTracer."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path

from qtpy.QtWidgets import QFormLayout, QGroupBox, QLabel, QPushButton, QStyle, QToolButton

from palm_tracer.Tools import Ui

_STATUS_TOOLTIPS = {
		"File":               "Current stack.",
		"Localizations":      "Localizations on the current stack.",
		"Beads":              "Beads on the current stack.",
		"Tracks":             "Tracking on the current stack.",
		"Tracks Reconnected": "Tracking after blinking reconnection on the current stack.",
		"MSD":                "Mean Square Displacement of tracks on the current stack.",
		"Instant D":          "Instant Diffusion of tracks on the current stack.",
		"MSD Fit":            "Fit of tracks on the current stack.",
		}


##################################################
@dataclass
class ResultsUI:
	"""
	Représente une vue Qt des résultats de PALMTracer avec des boutons de suppression.

	La vue ne conserve aucune donnée métier. Elle affiche les statuts transmis par :class:`~palm_tracer.Results.Results`
	et peut ainsi être synchronisée avec les autres représentations du même modèle.

	:param title: Titre du groupe d'informations.
	:param space: Espacement interne entre les éléments, en pixels.
	:param margin: Marges internes du groupe, en pixels.
	"""

	title: str = "Information"
	"""Titre du groupe d'informations."""
	space: int = Ui.COMMON_SPACE
	"""Espacement entre les lignes, en pixels."""
	margin: int = Ui.COMMON_SPACE
	"""Marges internes du groupe, en pixels."""
	widget: QGroupBox = field(init=False)
	"""Widget contenant les informations sur les résultats."""
	layout: QFormLayout = field(init=False)
	"""Calque contenant les différentes lignes d'informations."""
	_labels: dict[str, QLabel] = field(init=False, default_factory=dict)
	"""Libellés affichant les statuts des résultats."""
	_clear_buttons: dict[str, QToolButton] = field(init=False, default_factory=dict)
	"""Corbeilles par catégorie, connectées au modèle par :class:`~palm_tracer.Results.Results`."""
	_open_folder_button: QPushButton = field(init=False)
	"""Bouton d'ouverture du dossier de résultats, connecté au modèle."""

	##################################################
	def __post_init__(self):
		"""Construit les composants Qt de la vue."""
		self.widget = QGroupBox(self.title)
		self.layout = Ui.make_form(self.widget, self.space, self.margin)
		self.layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

		for key, tooltip in _STATUS_TOOLTIPS.items():
			label = QLabel("No")
			Ui.add_setting_row(self.layout, f"{key}: ", label, tooltip=tooltip, )
			self._labels[key] = label
			if key == "File": continue

			button = QToolButton(self.widget)
			button.setIcon(self.widget.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton))
			button.setToolTip(f"Clear {key.lower()} results.")
			button.setAccessibleName(f"Clear {key.lower()} results")
			self._clear_buttons[key] = button
			# Place la corbeille après l'espace extensible, à l'extrémité droite de la ligne.
			row = self.layout.itemAt(self.layout.rowCount() - 1, QFormLayout.ItemRole.FieldRole).layout()
			row.addWidget(button)

		self._open_folder_button = QPushButton("Open results folder", self.widget)
		self._open_folder_button.setEnabled(False)
		self.layout.addRow(self._open_folder_button)

	# ==================================================
	# region Mise à jour
	# ==================================================
	##################################################
	def update_status(self, status: Mapping[str, str]):
		"""
		Actualise les statuts affichés.

		Les clés inconnues sont ignorées afin de permettre au modèle de fournir
		des informations qui ne sont pas représentées par cette vue.

		:param status: Statuts à afficher, indexés par type de résultat.
		"""
		for key, value in status.items():
			if key not in self._labels: continue
			self._labels[key].setText(Path(value).name if key == "File" else value)
			if key == "File": self._labels[key].setToolTip(value if value != "No File" else "")

	##################################################
	def update_results_folder(self, path: Path | None):
		"""
		Actualise la disponibilité du bouton et son infobulle.

		:param path: Dossier des résultats, ou :obj:`None` si aucun dossier n'est associé.
		"""
		self._open_folder_button.setEnabled(path is not None and path.is_dir())
		self._open_folder_button.setToolTip(str(path) if path is not None else "")


##################################################
if __name__ == "__main__":
	import sys

	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # Crée et affecte la mise en page au widget
	ui = ResultsUI()
	lay.addWidget(ui.widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
