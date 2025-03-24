try:
	from ._version import version as __version__
except ImportError:
	__version__ = "unknown"

from . import Processing, Settings, Tools, UI
from .PALMTracer import PALMTracer
from .UI import PALMTracerWidget

__all__ = ("PALMTracer", "PALMTracerWidget",
		   "UI", "Processing", "Settings", "Tools")
