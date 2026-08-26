"""Définit la représentation Qt des résultats de PALMTracer."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

from qtpy.QtWidgets import QFormLayout, QGroupBox, QLabel

from palm_tracer.Tools import Ui

_STATUS_TOOLTIPS = {
		"File":          "Current stack.",
		"Localizations": "Localizations on the current stack.",
		"Beads":         "Beads on the current stack.",
		"Tracks":        "Tracking on the current stack.",
		"MSD":           "Mean Square Displacement of tracks on the current stack.",
		"Instant D":     "Instant Diffusion of tracks on the current stack.",
		"MSD Fit":       "Fit of tracks on the current stack.",
		}


##################################################
@dataclass
class ResultsUI:
	"""
	Représente une vue Qt en lecture seule des résultats de PALMTracer.

	La vue ne conserve aucune donnée métier. Elle affiche les statuts transmis par :class:`palm_tracer.Results.Results`
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

	##################################################
	def __post_init__(self):
		"""Construit les composants Qt de la vue."""
		self.widget = QGroupBox(self.title)
		self.layout = Ui.make_form(self.widget, self.space, self.margin)

		for key, tooltip in _STATUS_TOOLTIPS.items():
			label = QLabel("No")
			Ui.add_setting_row(self.layout, f"{key}: ", label, tooltip=tooltip, )
			self._labels[key] = label

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
			if key in self._labels: self._labels[key].setText(value)
