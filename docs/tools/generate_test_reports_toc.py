""" Fichier permettant de mettre à jour le toctree du fichier de test """

import os


def generate_toctree_rst(dst: str = "tests.rst"):
	reports_path = "docs/reports"  # Répertoire contenant les fichiers `.rst`
	pattern = "test_report_ci_"    # Modèle pour les fichiers à inclure

	# Recherche des fichiers correspondants
	files = [f for f in os.listdir(reports_path) if f.startswith(pattern) and f.endswith(".rst")]

	# Génération du contenu du fichier .rst
	content = ("Tests\n"
			   "=====\n\n"
			   "Liste des rapports de tests générés :\n\n"
			   ".. toctree::\n"
			   "   :maxdepth: 1\n\n"
			   "   reports/test_report_main_computer\n")

	for file in sorted(files):  # Trie pour un ordre cohérent
		content += f"   reports/{os.path.splitext(file)[0]}\n"

	# Écriture dans le fichier de sortie
	with open(os.path.join("docs", dst), "w", encoding="utf-8") as f: f.write(content)
	print(f"{dst} generated successfully.")


if __name__ == "__main__":
	generate_toctree_rst()
