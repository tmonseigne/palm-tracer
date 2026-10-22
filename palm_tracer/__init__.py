"""Expose l'API publique principale de PALM Tracer."""

from importlib.metadata import PackageNotFoundError, version

try:
	__version__ = version("palm-tracer")
except PackageNotFoundError:
	__version__ = "unknown"

from .PALMTracer import PALMTracer
from .Results import Results

__all__ = ("PALMTracer", "Results", "Processing", "Settings", "Tools", "UI")
