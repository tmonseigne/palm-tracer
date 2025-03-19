import ctypes
from pathlib import Path
from typing import Optional

from palm_tracer.Tools import print_warning

DLL_PATH = Path(__file__).parent.parent.parent / "DLL"


##################################################
def load_dll(name: str) -> Optional[ctypes.CDLL]:
	"""Récupère la DLL si elle existe."""
	dll_filename = DLL_PATH / f"{name}_PALM.dll"
	try:
		return ctypes.cdll.LoadLibrary(str(dll_filename.resolve()))
	except OSError as e:
		print_warning(f"Impossible de charger la DLL '{dll_filename}':\n\t{e}")
		return None
