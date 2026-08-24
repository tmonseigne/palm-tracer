"""Définit une zone d'intérêt utilisée pour filtrer les données dans Napari."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


##################################################
@dataclass
class ROI:
	"""Classe de définition d'une zone d'intérêt (ROI) pour Napari."""
	type: str
	"""Type de dessin (rectangle, polygone, ellipse)."""
	data: np.ndarray
	"""Liste des points sous forme de tableau NumPy."""
