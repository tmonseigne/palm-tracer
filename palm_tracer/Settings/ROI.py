"""Définit une zone d'intérêt utilisée pour filtrer les données dans Napari."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


##################################################
@dataclass
class ROI:
	"""Représente une zone d'intérêt issue d'un calque Napari.

	:param type: Type géométrique de la zone.
	:param data: Coordonnées décrivant sa géométrie.
	"""

	type: str
	"""Type de dessin (rectangle, polygone, ellipse)."""
	data: np.ndarray
	"""Liste des points sous forme de tableau NumPy."""
