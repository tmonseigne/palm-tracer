"""Fichier permettant de transformer un rapport Pytest JSON en reStructuredText pour sphinx"""
from __future__ import annotations

import datetime
import json
import re
import sys
from pathlib import Path
from typing import Any

from ansi2html import Ansi2HTMLConverter

# Convertisseur ANSI vers HTML
conv = Ansi2HTMLConverter(inline=True)  # Utiliser des styles en ligne pour éviter les dépendances CSS


##################################################
def to_title_case(name: str) -> str:
	"""
	Convertit une chaîne de caractères en "Title Case" (majuscule à chaque mot).

	:param name: La chaîne de caractères à convertir.
	:return: La chaîne de caractères convertie en "Title Case".
	"""
	return name.replace("_", " ").title()


##################################################
def format_duration(duration: float) -> str:
	"""
	Formate une durée en une unité lisible avec la précision adéquate.

	:param duration: Durée en secondes (float).
	:return: Chaîne formatée avec la meilleure unité.
	"""
	if duration < 1: return f"{round(duration * 1000)}ms"  # .											   Moins d'une seconde : millisecondes
	if duration < 60: return f"{duration:.2f}s"  # .													   Moins d'une minute : secondes
	if duration < 3600: return f"{int(duration // 60)}min {round(duration % 60, 2):.0f}s"  # .			   Moins d'une heure : minutes et secondes
	return f"{int(duration // 3600)}h {int((duration % 3600) // 60)}min {round(duration % 60, 2):.0f}s"  # Une heure ou plus : heures, minutes et secondes


# ==================================================
# region Generation
# ==================================================
##################################################
def generate_rst_from_json(src: str | Path, dst: str | Path):
	"""
	Génère un fichier reStructuredText à partir d'un rapport Pytest en format JSON.

	:param src: Chemin du fichier JSON contenant les résultats de Pytest.
	:param dst: Chemin du fichier de sortie reStructuredText.
	"""
	src_path = Path(src)
	dst_path = Path(dst)

	try:
		data = json.loads(src_path.read_text(encoding="utf-8"))
	except FileNotFoundError:
		print("Json file not found.")
		return
	except json.JSONDecodeError as exc:
		print(f"Json decode error: {exc}")
		return

	title, monitoring = get_files_info(dst_path)

	dst_path.parent.mkdir(parents=True, exist_ok=True)
	with dst_path.open("w", encoding="utf-8", newline="\n") as f:
		f.write(f"{title}\n{'=' * len(title)}\n\n")
		f.write(get_metadata(data["metadata"]))
		f.write(get_summary(data))
		f.write(get_monitoring(monitoring))
		f.write(get_tests(data["tests"]))


##################################################
def get_files_info(src: str | Path, monitoring_ext: str = "html") -> list[str]:
	"""
	Extrait les informations du fichier source pour générer un titre et un nom de fichier pour le monitoring.

	:param src: Chemin du fichier source.
	:param monitoring_ext: Extension du fichier de monitoring (par défaut "html").
	:return: Liste contenant le titre et le nom du fichier de monitoring.
	"""
	file_basename = Path(src).stem
	title = to_title_case(file_basename)
	monitoring_file = file_basename.replace("test_report", "monitoring") + f".{monitoring_ext}"
	return [title, monitoring_file]


##################################################
def get_metadata(metadata: dict[str, Any]) -> str:
	"""
	Génère une section reStructuredText pour afficher les métadonnées du rapport.

	:param metadata: Dictionnaire contenant les métadonnées du rapport.
	:return: Chaîne reStructuredText formatée avec les métadonnées.
	"""
	res = ("Environnement\n"
		   "-------------\n\n"
		   ".. list-table::\n\n")

	for key, value in metadata.items():
		if key not in {"Packages", "Plugins"}:
			res += f"   * - {key}\n     - {value}\n"

	return res + "\n"


##################################################
def get_summary(data: dict) -> str:
	"""
	Génère une section reStructuredText pour afficher un résumé du rapport de test.

	:param data: Dictionnaire contenant les données du rapport, incluant la durée et les résultats des tests.
	:return: Chaîne reStructuredText formatée avec le résumé du rapport.
	"""
	res = ("Summary\n"
		   "-------\n\n")
	timestamp = datetime.datetime.fromtimestamp(data["created"])
	time = timestamp.strftime("%H:%M:%S")
	date = timestamp.strftime("%d/%m/%Y")
	duration = str(datetime.timedelta(seconds=data["duration"])).split(".")[0]
	summary = data["summary"]

	res += (f"{summary.get('collected', 0)} tests collected, "
			f"{summary.get('passed', 0)} passed ✅, {summary.get('failed', 0)} failed ❌, {summary.get('skipped', 0)} skipped ⏭️ "
			f"in {duration}s on {date} at {time}\n\n")
	return res


##################################################
def get_monitoring(file: str) -> str:
	"""
	Génère une section reStructuredText pour afficher un graphique de monitoring à partir d'un fichier.

	:param file: Nom du fichier HTML contenant le graphique de monitoring.
	:return: Chaîne reStructuredText avec un iframe pour afficher le graphique.
	"""
	res = ("Monitoring\n"
		   "----------\n\n")

	# Le JSON pourrait être intégré avec chart, mais ne marche pas. Iframe est utilisé à la place.
	# res += f".. chart:: Reports/{file}\n\n    Resources Monitoring\n\n"
	res += (f".. raw:: html\n\n"
			f"   <div style=\"position: relative; width: 100%; height: 620px; max-width: 100%; margin: 0 0 1em 0; padding:0;\">\n"
			f"     <iframe src=\"{file}\"\n"
			f"             style=\"position: absolute; margin: 0; padding:0; width: 100%; height: 100%; border: none;\">\n"
			f"     </iframe>\n"
			f"   </div>\n\n")

	return res


##################################################
def get_tests(tests: list) -> str:
	"""
	Génère une section reStructuredText pour afficher les résultats des tests.

	:param tests: Liste des résultats de tests sous forme de dictionnaires.
	:return: Chaîne reStructuredText formatée avec les résultats des tests.
	"""
	res = ("Test Cases\n"
		   f"----------\n\n"
		   ".. raw:: html\n\n   <div class=\"test-page\">\n\n")

	# Grouper les tests par fichiers
	tests_by_file = {}  # type: dict[str, list]
	for test in tests:
		filename = test["nodeid"].split("::")[0]  # Extraire le nom du fichier
		if filename not in tests_by_file: tests_by_file[filename] = []
		tests_by_file[filename].append(test)

	for filename, file_tests in tests_by_file.items():
		title = to_title_case(filename.split("/")[-1][5:-3])  # Nom du fichier sans chemin, sans "test_" et sans ".py"
		underline = "^" * len(title)
		res += f"{title}\n{underline}\n\n"

		# Ajouter le tableau
		res += (".. list-table::\n"
				"   :header-rows: 1\n\n"
				"   * - Test Name\n"
				"     - Status\n"
				"     - Duration\n")

		for test in file_tests:
			test_name = to_title_case(test["nodeid"].split("::")[1][5:])  # Nom du test sans "test_"
			outcome = test["outcome"]
			durations = [test.get("setup", {}).get("duration", 0),
						 test.get("call", {}).get("duration", 0),
						 test.get("teardown", {}).get("duration", 0)]

			res += (f"   * - {test_name}\n"
					f"     - {get_outcome_icon(outcome)}\n"
					f"     - {format_duration(sum(durations))}\n")

		res += "\n"

		# Ajouter un lien vers le stdout
		for test in file_tests:
			if "call" not in test: continue  # .							Pas de log possible pour skipped, xfailed...
			test_name = to_title_case(test["nodeid"].split("::")[1][5:])  # Nom du test sans "test_"
			stdout = test["call"].get("stdout", "")
			stdout = conv.convert(stdout, full=False)  # .					Convertir ANSI en HTML
			stdout = stdout.replace("\n", "<br>")  # .						Remplacer les sauts de ligne par <br> pour un bon affichage en HTML
			stdout = re.sub(r"^(<br>)+", "", stdout)  # .					Supprime les "<br>" initiaux
			stdout = re.sub(r"(<br>)+$", "", stdout)  # .					Supprime les "<br>" finaux
			if stdout:  # .													Si le stdout existe, l'afficher dans un bloc repliable
				res += f".. raw:: html\n\n"
				res += f"   <details>\n"
				res += f"      <summary>Log Test : {test_name}</summary>\n"
				res += f"      <pre>{stdout}</pre>\n"
				res += f"   </details>\n\n"

	res += ".. raw:: html\n\n   </div>\n\n"
	return res


##################################################
def get_outcome_icon(outcome: str) -> str:
	"""
	Retourne une icône/emoji correspondant à un résultat de test.

	:param outcome: Résultat du test ("passed", "failed", "xpassed", "xfailed", "skipped").
	:return: Emoji correspondant au résultat.
	"""
	icons = {
			"passed":  "✅",  # .		Test réussi
			"failed":  "❌",  # .		Test échoué
			"xpassed": "⚠️",  # .		Test attendu comme échoué, mais a réussi
			"xfailed": "✔️",  # .		Test attendu comme échoué et a échoué
			"skipped": "⏭️",  # .		Test sauté
			}
	return icons.get(outcome, "❓")  # Par défaut, une icône d'interrogation pour les résultats inconnus


# ==================================================
# endregion Generation
# ==================================================
##################################################
def usage():
	"""Affiche l'usage du script en ligne de commande."""
	print("Usage:\n"
		  "  python pytest_json_to_rst.py <REPORT_FILE> <OUTPUT_FILE>\n"
		  "  Args:\n"
		  "    REPORT_FILE: Pytest json report.\n"
		  "    OUTPUT_FILE: Path to the output reStructuredText file.")


##################################################
if __name__ == "__main__":
	if len(sys.argv) < 3:
		usage()
		raise SystemExit(0)

	source, destination = Path(sys.argv[1]), Path(sys.argv[2])

	if not source.exists():
		print(f"ERROR: The report file '{source}' does not exist.")
		usage()
		raise SystemExit(1)

	print(f"Start generation: input ({source}), output ({destination})")
	generate_rst_from_json(source, destination)
	print("reStructuredText report was generated successfully.")
