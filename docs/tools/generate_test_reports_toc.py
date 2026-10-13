"""Met à jour la table des matières des rapports de tests."""

from __future__ import annotations

from pathlib import Path


# --------------------------------------------------
def generate_toctree_rst(dst: str = "tests.rst"):
	"""
	Génère la table des matières des rapports de tests.

	Inclut les rapports locaux ``test_report.rst`` et ``test_report_main_computer.rst`` lorsqu’ils existent,
	ainsi que les rapports ``test_report_ci_*.rst`` présents dans ``docs/reports``.

	:param dst: Chemin du fichier de sortie relatif au dossier ``docs``.
	"""

	docs_path = Path(__file__).resolve().parent.parent
	reports_path = docs_path / "reports"  # Répertoire contenant les fichiers .rst
	pattern = "test_report_ci_"  # .		Modèle pour les fichiers à inclure

	# Recherche des fichiers correspondants
	files = [reports_path / name for name in ("test_report.rst", "test_report_main_computer.rst") if (reports_path / name).is_file()]
	files.extend(sorted(reports_path.glob(f"{pattern}*.rst")))

	# Génération du contenu du fichier .rst
	content = ("Tests\n"
			   "=====\n\n"
			   "Liste des rapports de tests générés :\n\n"
			   ".. toctree::\n"
			   "   :maxdepth: 1\n\n")

	for f in files: content += f"   reports/{f.stem}\n"

	# Écriture dans le fichier de sortie
	output_file = docs_path / dst
	output_file.write_bytes(content.encode("utf-8"))
	print(f"{dst} generated successfully.")


# --------------------------------------------------
if __name__ == "__main__": generate_toctree_rst()
