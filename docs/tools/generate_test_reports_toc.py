"""Met à jour la table des matières des rapports de tests."""

from __future__ import annotations

from pathlib import Path


##################################################
def generate_toctree_rst(dst: str = "tests.rst"):
	"""Génère un fichier toctree Sphinx listant les rapports de tests CI."""

	docs_path = Path("docs")
	reports_path = docs_path / "reports"  # Répertoire contenant les fichiers .rst
	pattern = "test_report_ci_"  # .		Modèle pour les fichiers à inclure

	# Recherche des fichiers correspondants
	files = sorted(f for f in reports_path.glob(f"{pattern}*.rst"))

	# Génération du contenu du fichier .rst
	content = ("Tests\n"
			   "=====\n\n"
			   "Liste des rapports de tests générés :\n\n"
			   ".. toctree::\n"
			   "   :maxdepth: 1\n\n"
			   "   reports/test_report_main_computer\n")

	for f in files: content += f"   reports/{f.stem}\n"

	# Écriture dans le fichier de sortie
	output_file = docs_path / dst
	output_file.write_text(content, encoding="utf-8")
	print(f"{dst} generated successfully.")


##################################################
if __name__ == "__main__": generate_toctree_rst()
