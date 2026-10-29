"""Centralise les dialogues Qt et la mémorisation de leurs derniers dossiers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal

from qtpy.QtWidgets import QFileDialog, QWidget

from palm_tracer.Tools import FileIO, Ui


# --------------------------------------------------
def _read_state() -> dict[str, Any]:
	"""Relit les préférences pour partager les dossiers entre fenêtres et les retrouver après redémarrage."""
	try:
		state = json.loads(FileIO.USER_UI_STATE_FILE.read_text(encoding="utf-8"))
		return state if isinstance(state, dict) else {}
	except  (FileNotFoundError, OSError, ValueError): return {}


# --------------------------------------------------
def _dialog_directory(kind: Literal["open", "save"], filename: str = "") -> str:
	"""
	Retrouve le dossier mémorisé, avec repli sur le dossier utilisateur.

	:param kind: Historique des ouvertures ou des exports.
	:param filename: Nom de fichier éventuellement proposé pour un export, sans réutiliser son ancien dossier.
	:return: Dossier initial, complété par le nom proposé s'il est fourni.
	"""
	stored = _read_state().get(kind)
	folder = Path(stored) if isinstance(stored, str) and stored else Path.home()
	if not folder.is_dir(): folder = Path.home()
	return str(folder / Path(filename).name) if filename and not Path(filename).is_dir() else str(folder)


# --------------------------------------------------
def _remember_dialog_directory(kind: Literal["open", "save"], folder: Path):
	"""
	Mémorise le dossier sélectionné sans faire échouer le dialogue si l'enregistrement est impossible.

	:param kind: Historique des ouvertures ou des exports.
	:param folder: Dossier choisi ou dossier contenant le fichier choisi.
	"""
	if not folder.is_dir(): return
	state = _read_state()
	directory = str(folder.resolve())
	if state.get(kind) == directory: return
	state[kind] = directory
	try:
		FileIO.USER_UI_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
		FileIO.USER_UI_STATE_FILE.write_text(json.dumps(state, indent=4, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
	except OSError as error: Ui.print_warning(f"Unable to save file dialog preferences: {error}")


# --------------------------------------------------
def open_file(parent: QWidget | None, caption: str, file_filter: str = "") -> tuple[str, str]:
	"""
	Sélectionne un fichier dans le dernier dossier ouvert et mémorise le dossier après validation.

	:param parent: Widget parent éventuel du dialogue.
	:param caption: Titre du dialogue.
	:param file_filter: Filtre des fichiers affichés, au format Qt.
	:return: Chemin du fichier et filtre sélectionné, ou chaînes vides en cas d'annulation.
	"""
	filename, selected_filter = QFileDialog.getOpenFileName(parent, caption, _dialog_directory("open"), file_filter)
	if filename: _remember_dialog_directory("open", Path(filename).parent)
	return filename, selected_filter


# --------------------------------------------------
def open_files(parent: QWidget | None, caption: str, file_filter: str = "") -> tuple[list[str], str]:
	"""
	Sélectionne plusieurs fichiers en partageant l'historique des autres dialogues d'ouverture.

	:param parent: Widget parent éventuel du dialogue.
	:param caption: Titre du dialogue.
	:param file_filter: Filtre des fichiers affichés, au format Qt.
	:return: Chemins des fichiers et filtre sélectionné, ou liste vide en cas d'annulation.
	"""
	filenames, selected_filter = QFileDialog.getOpenFileNames(parent, caption, _dialog_directory("open"), file_filter)
	if filenames: _remember_dialog_directory("open", Path(filenames[-1]).parent)
	return filenames, selected_filter


# --------------------------------------------------
def open_directory(parent: QWidget | None, caption: str) -> str:
	"""
	Sélectionne un dossier en partageant l'historique des dialogues d'ouverture de fichiers.

	:param parent: Widget parent éventuel du dialogue.
	:param caption: Titre du dialogue.
	:return: Dossier choisi, ou chaîne vide en cas d'annulation.
	"""
	folder = QFileDialog.getExistingDirectory(parent, caption, _dialog_directory("open"))
	if folder: _remember_dialog_directory("open", Path(folder))
	return folder


# --------------------------------------------------
def save_file(parent: QWidget | None, caption: str, filename: str = "", file_filter: str = "") -> tuple[str, str]:
	"""
	Sélectionne un chemin d'export dans un historique distinct de celui des ouvertures.

	:param parent: Widget parent éventuel du dialogue.
	:param caption: Titre du dialogue.
	:param filename: Nom de fichier proposé ; un éventuel dossier est remplacé par le dernier dossier d'export.
	:param file_filter: Filtre des formats proposés, au format Qt.
	:return: Chemin de sortie et filtre sélectionné, ou chaînes vides en cas d'annulation.
	"""
	path, selected_filter = QFileDialog.getSaveFileName(parent, caption, _dialog_directory("save", filename), file_filter)
	if path: _remember_dialog_directory("save", Path(path).parent)
	return path, selected_filter
