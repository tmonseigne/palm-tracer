"""Définit le groupe de paramètres du rendu haute résolution pour les animations de trajectoires."""

from __future__ import annotations

from dataclasses import dataclass

from palm_tracer.Settings.Groups.BaseSettingGroup import BaseSettingGroup
from palm_tracer.Settings.Types import CheckBox, Combo, SpinInt


##################################################
@dataclass
class HRTrackStack(BaseSettingGroup):
	"""
	Regroupe les paramètres des reconstructions haute résolution pour les animations de trajectoires.

	Configure la taille des têtes, la largeur et la durée des queues, leur effacement et le fond brut.
	"""

	label: str = "Track Stack"
	"""Libellé du groupe affiché dans l'interface."""
	setting_list = {"Head":       [SpinInt, ["Head Size", "Head circle diameter in rendered pixels.", 1, [1, 100], 1]],
					"Width":      [SpinInt, ["Tail Width", "Tail width in rendered pixels.", 1, [1, 100], 1]],
					"Length":     [SpinInt, ["Tail Length", "Tail lifetime in frames after each segment appears: -1 keeps all segments; "
															"0 shows heads only; N keeps segments through age N.",
											 -1, [-1, 100], 1]],
					"Fade":       [Combo, ["Fade",
										   "Remove tail segments abruptly or fade them linearly over their lifetime.",
										   0, ["Abrupt", "Fade"]]],
					"Map":        [Combo, ["Color Map", "Track color map when the raw background is enabled.", 0,
										   ["viridis", "magma", "plasma", "inferno", "cividis", "turbo", "hsv"]]],
					"Background": [CheckBox, ["Raw in Background", "Show the raw acquisition in the background.", True]],
					"Upscale":    [Combo, ["Background Upscale",
										   "Method used to enlarge the raw background.",
										   0, ["Nearest", "Lanczos"]]]
					}
	"""Définition des paramètres du groupe et de leur configuration."""
	mode: int = 2
	"""Mode d'affichage du groupe dans l'interface."""


##################################################
if __name__ == "__main__":
	import sys
	from qtpy.QtWidgets import QApplication, QVBoxLayout, QWidget

	app = QApplication(sys.argv)
	w = QWidget()
	lay = QVBoxLayout(w)  # Crée et affecte la mise en page au widget
	group = HRTrackStack()
	lay.addWidget(group.get_ui().widget)
	lay.addStretch(1)
	w.show()
	sys.exit(app.exec_())
