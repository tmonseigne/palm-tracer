"""Met à jour la table des matières des rapports de tests."""

from __future__ import annotations

from pathlib import Path


# --------------------------------------------------
def generate_toctree_rst(dst: str = "tests.rst"):
	"""
	Génère la table des matières des rapports de tests.

	Inclut les rapports ``test_report*.rst`` présents dans ``docs/reports``, notamment le rapport local et les rapports CI.

	:param dst: Chemin du fichier de sortie relatif au dossier ``docs``.
	"""

	docs_path = Path(__file__).resolve().parent.parent
	reports_path = docs_path / "reports"  # Répertoire contenant les fichiers .rst

	# Recherche des fichiers correspondants
	files = sorted(reports_path.glob("test_report*.rst"))

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
