"""
Génère les pages reStructuredText de l'API publique pour Sphinx.

La génération repose sur l'analyse statique de l'arborescence Python et ne nécessite aucun import des modules documentés.
"""

from __future__ import annotations

import ast
import shutil
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parent.parent.parent
DOCS_PATH = ROOT_PATH / "docs"
API_PATH = DOCS_PATH / "api"


# --------------------------------------------------
def _read_project_configuration() -> tuple[str, str]:
	"""
	Lit le nom du projet Sphinx et détermine le package Python associé sans importer sa configuration.

	Le nom du package correspond au nom du projet en minuscules, avec les espaces et tirets remplacés par des underscores.

	:return: Nom du package et titre du projet.
	:raises RuntimeError: Si le nom du projet n’est pas une chaîne littérale ou si le package associé est absent.
	"""
	tree = ast.parse((DOCS_PATH / "conf.py").read_text(encoding="utf-8"))
	for node in tree.body:
		if not isinstance(node, ast.Assign) or not any(isinstance(target, ast.Name) and target.id == "project" for target in node.targets): continue
		if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
			project_name = node.value.value
			module_name = project_name.lower().replace(" ", "_").replace("-", "_")
			if (ROOT_PATH / module_name / "__init__.py").is_file(): return module_name, project_name
			raise RuntimeError(f"Python package not found for Sphinx project: {project_name}")
	raise RuntimeError("Sphinx configuration must declare project as a string literal.")


MODULE_NAME, PROJECT_NAME = _read_project_configuration()
MODULE_PATH = ROOT_PATH / MODULE_NAME


# ==================================================
# region Classes
# ==================================================
@dataclass(frozen=True)
class ModulePublicApi:
	"""
	Décrit les symboles publics d'un module Python.

	:param classes: Noms des classes publiques, dans leur ordre de déclaration.
	:param functions: Noms des fonctions publiques, dans leur ordre de déclaration.
	:param constants: Noms des constantes publiques, dans leur ordre de déclaration.
	"""

	classes: tuple[str, ...]
	"""Noms des classes publiques, dans leur ordre de déclaration."""
	functions: tuple[str, ...]
	"""Noms des fonctions publiques, dans leur ordre de déclaration."""
	constants: tuple[str, ...]
	"""Noms des constantes publiques, dans leur ordre de déclaration."""


# --------------------------------------------------
@dataclass(frozen=True)
class ClassMember:
	"""
	Identifie un membre public d'une classe.

	:param name: Nom du membre.
	:param lineno: Numéro de sa ligne de déclaration.
	"""

	name: str
	"""Nom du membre."""
	lineno: int
	"""Numéro de la ligne de déclaration du membre."""


# --------------------------------------------------
@dataclass(frozen=True)
class ClassPublicApi:
	"""
	Décrit les membres publics d'une classe Python.

	:param attributes: Attributs publics, dans leur ordre de déclaration.
	:param methods: Méthodes publiques, dans leur ordre de déclaration.
	"""

	attributes: tuple[ClassMember, ...]
	"""Attributs publics, dans leur ordre de déclaration."""
	methods: tuple[ClassMember, ...]
	"""Méthodes publiques, dans leur ordre de déclaration."""


# --------------------------------------------------
@dataclass(frozen=True)
class PackageNode:
	"""
	Décrit un package Python et ses descendants directs.

	:param dotted_name: Nom qualifié du package.
	:param dir_path: Chemin du répertoire correspondant.
	:param subpackages: Sous-packages directs.
	:param modules: Modules publics directs.
	"""

	dotted_name: str
	"""Nom qualifié du package."""
	dir_path: Path
	"""Chemin du répertoire du package."""
	subpackages: tuple[PackageNode, ...]
	"""Sous-packages directs."""
	modules: tuple[str, ...]
	"""Modules publics directs."""  # Noms qualifiés (package inclus), sans __init__


# ==================================================
# endregion Classes
# ==================================================

# ==================================================
# region Vérification des fichiers
# ==================================================
def _is_python_package(directory: Path) -> bool:
	"""
	Indique si un dossier contient un fichier ``__init__.py``.

	:param directory: Chemin du dossier à examiner.
	:return: ``True`` si le dossier est un package Python.
	"""
	return directory.is_dir() and (directory / "__init__.py").is_file()


# --------------------------------------------------
def _iter_public_py_modules(package_dir: Path) -> Iterable[Path]:
	"""
	Énumère les modules publics directs d’un package, hors ``__init__.py``.

	:param package_dir: Chemin du dossier du package.
	:yield: Chemins des modules, triés par nom de fichier.
	"""
	for py in sorted(package_dir.glob("*.py")):
		if py.name == "__init__.py": continue
		if py.name.startswith("_"): continue  # Fichiers privés
		yield py


# --------------------------------------------------
def _iter_public_subpackages(package_dir: Path) -> Iterable[Path]:
	"""
	Énumère les sous-packages publics directs d’un package.

	:param package_dir: Chemin du dossier du package.
	:yield: Chemins des sous-packages, triés par nom de dossier.
	"""
	for child in sorted(package_dir.iterdir()):
		if child.name.startswith("_"): continue  # Packages privés
		if _is_python_package(child): yield child


# ==================================================
# endregion Vérification des fichiers
# ==================================================

# ==================================================
# region Analyse
# ==================================================
def _parse_public_api_from_file(py_file: Path) -> ModulePublicApi:
	"""
	Extrait les symboles publics d’un fichier Python sans l’importer.

	Les noms de constantes sont reconnus par leur écriture en majuscules.

	:param py_file: Fichier Python à analyser.
	:return: Classes, fonctions et constantes publiques dans leur ordre de déclaration.
	"""
	tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))

	classes: list[str] = []
	functions: list[str] = []
	constants: list[str] = []

	for node in tree.body:
		if isinstance(node, ast.ClassDef):
			if not node.name.startswith("_"): classes.append(node.name)
		elif isinstance(node, ast.FunctionDef):
			if not node.name.startswith("_"): functions.append(node.name)
		elif isinstance(node, (ast.Assign, ast.AnnAssign)):
			# Constantes simples au niveau module (heuristique)
			targets: list[str] = []
			if isinstance(node, ast.Assign):
				for t in node.targets:
					if isinstance(t, ast.Name): targets.append(t.id)
			else:  # AnnAssign
				if isinstance(node.target, ast.Name): targets.append(node.target.id)

			for name in targets:
				if name.isupper() and not name.startswith("_"): constants.append(name)

	return ModulePublicApi(tuple(classes), tuple(functions), tuple(constants))


# --------------------------------------------------
def _parse_class_public_api(py_file: Path, class_name: str) -> ClassPublicApi:
	"""
	Analyse les membres publics d'une classe Python.

	:param py_file: Fichier Python à analyser.
	:param class_name: Nom de la classe à analyser.
	:return: Attributs et méthodes publics de la classe.
	"""
	tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))

	for node in tree.body:
		if not (isinstance(node, ast.ClassDef) and node.name == class_name):
			continue

		attrs: list[ClassMember] = []
		meths: list[ClassMember] = []

		for item in node.body:
			if isinstance(item, ast.FunctionDef):
				if item.name.startswith("_"): continue
				if _is_property(item): attrs.append(ClassMember(item.name, item.lineno))
				else: meths.append(ClassMember(item.name, item.lineno))

			elif isinstance(item, (ast.Assign, ast.AnnAssign)):
				# Attributs de classe (heuristique)
				names: list[str] = []

				if isinstance(item, ast.Assign):
					for t in item.targets:
						if isinstance(t, ast.Name): names.append(t.id)
				else:
					if isinstance(item.target, ast.Name): names.append(item.target.id)

				for n in names:
					if n.startswith("_"): continue
					attrs.append(ClassMember(n, item.lineno))

		return ClassPublicApi(_unique_members_preserve_order(attrs), _unique_members_preserve_order(meths))

	return ClassPublicApi((), ())


# --------------------------------------------------
def _is_property(func: ast.FunctionDef) -> bool:
	"""
	Indique si une fonction AST représente une propriété ou son setter.

	:param func: Nœud AST de la fonction.
	:return: ``True`` si la fonction représente une propriété ou son setter.
	"""
	for dec in func.decorator_list:
		if isinstance(dec, ast.Name) and dec.id == "property": return True
		if isinstance(dec, ast.Attribute) and dec.attr == "setter": return True
	return False


# --------------------------------------------------
def _parse_regions_markers(py_file: Path) -> list[tuple[int, int | None, str]]:
	"""
	Extrait les marqueurs de région d’un fichier Python.

	Les régions imbriquées ne sont pas prises en charge.
	Une région non fermée conserve une fin égale à ``None``, résolue ensuite lors du découpage par classe.

	:param py_file: Fichier Python à analyser.
	:return: Régions sous la forme ``(ligne_début, ligne_fin, nom)``, avec des lignes numérotées à partir de 1.
	"""
	lines = py_file.read_text(encoding="utf-8").splitlines()

	regions: list[tuple[int, int | None, str]] = []
	open_region: tuple[int, str] | None = None  # (start, name)

	for i, raw in enumerate(lines, start=1):
		line = raw.strip()

		if line.startswith("# region "):
			name = line[len("# region "):].strip()
			open_region = (i, name)
			continue

		if line.startswith("# endregion"):
			if open_region is None: continue
			start, name = open_region
			regions.append((start, i, name))
			open_region = None

	if open_region is not None:
		start, name = open_region
		regions.append((start, None, name))

	return regions


# --------------------------------------------------
def _clamp_regions_to_class(regions: list[tuple[int, int | None, str]], class_start: int, class_end: int) -> list[tuple[int, int, str]]:
	"""
	Restreint les régions aux lignes d’une classe.

	Une région non fermée se termine à la dernière ligne de la classe.

	:param regions: Régions sous la forme ``(ligne_début, ligne_fin, nom)``.
	:param class_start: Première ligne de la classe, numérotée à partir de 1.
	:param class_end: Dernière ligne de la classe, incluse.
	:return: Régions intersectant la classe, triées par ligne de début.
	"""
	out: list[tuple[int, int, str]] = []
	for start, end_or_none, name in regions:
		end = end_or_none if end_or_none is not None else class_end

		# Intersecte la classe ?
		if end < class_start or start > class_end: continue

		start2 = max(start, class_start)
		end2 = min(end, class_end)
		out.append((start2, end2, name))

	out.sort(key=lambda r: r[0])
	return out


# --------------------------------------------------
def _find_region_name(lineno: int, regions: list[tuple[int, int, str]]) -> str:
	"""
	Recherche la région contenant une ligne de déclaration.

	:param lineno: Numéro de la ligne de déclaration.
	:param regions: Régions fermées sous la forme ``(ligne_début, ligne_fin, nom)``.
	:return: Nom de la première région correspondante, ou chaîne vide.
	"""
	for start, end, name in regions:
		if start <= lineno <= end: return name
	return ""


# --------------------------------------------------
def _unique_members_preserve_order(items: list[ClassMember]) -> tuple[ClassMember, ...]:
	"""
	Déduplique les membres en conservant leur ordre de déclaration.

	:param items: Membres à dédupliquer.
	:return: Membres dédupliqués dans leur ordre de déclaration.
	"""
	seen: set[str] = set()
	out: list[ClassMember] = []
	for m in sorted(items, key=lambda x: x.lineno):  # Ordre bysource
		if m.name in seen: continue
		seen.add(m.name)
		out.append(m)
	return tuple(out)


# --------------------------------------------------
def _unique_preserve_order(items: Iterable[str]) -> tuple[str, ...]:
	"""
	Déduplique des chaînes en conservant leur ordre d’apparition.

	:param items: Chaînes à dédupliquer.
	:return: Chaînes distinctes dans leur ordre d’apparition.
	"""
	seen: set[str] = set()
	out: list[str] = []
	for x in items:
		if x in seen: continue
		seen.add(x)
		out.append(x)
	return tuple(out)


# ==================================================
# endregion Analyse
# ==================================================

# ==================================================
# region Génération RST
# ==================================================

# --------------------------------------------------
def _rst_title(title: str, sep: str = "=") -> str:
	"""
	Génère un titre reStructuredText souligné.

	:param title: Texte du titre.
	:param sep: Caractère de soulignement du titre.
	:return: Titre suivi de son soulignement et d’une ligne vide.
	"""
	return f"{title}\n{sep * len(title)}\n\n"


# --------------------------------------------------
def _rst_package_page(node: PackageNode) -> str:
	"""
	Génère la page reStructuredText d’un package.

	:param node: Package et descendants directs à documenter.
	:return: Page contenant les tables des matières des modules et sous-packages disponibles.
	"""
	# Titre spécifique du package racine.
	title = f"{PROJECT_NAME} API Reference" if node.dotted_name == MODULE_NAME else node.dotted_name.split(".")[-1]
	out = _rst_title(title)

	# Introduction du sous-package.
	if node.dotted_name != MODULE_NAME:
		short_name = node.dotted_name.split(".")[-1]
		out += f"{short_name}\n\n"

	# 1) Modules (maxdepth 1) : pages module
	if node.modules:
		out += ".. toctree::\n"
		out += "   :maxdepth: 1\n\n"
		for mod in node.modules: out += f"   {mod}\n"
		out += "\n"

	# 2) Sous-packages (maxdepth 2) : pages package
	if node.subpackages:
		out += ".. toctree::\n"
		out += "   :maxdepth: 2\n\n"
		for sub in node.subpackages: out += f"   {sub.dotted_name}\n"
		out += "\n"

	return out


# --------------------------------------------------
def _rst_module_page(dotted_module: str, py_file: Path) -> str:
	"""
	Génère la page reStructuredText d’un module.

	Un module contenant une seule classe publique et aucune fonction publique utilise la page détaillée de cette classe.
	Les autres modules utilisent la directive ``automodule``.

	:param dotted_module: Nom qualifié du module.
	:param py_file: Fichier Python à analyser.
	:return: Contenu reStructuredText de la page du module.
	"""
	title = dotted_module.split(".")[-1]
	out = _rst_title(title, "=")

	api = _parse_public_api_from_file(py_file)

	only_one_class = (len(api.classes) == 1 and len(api.functions) == 0)

	if only_one_class: return _rst_class_page(dotted_module, api.classes[0], py_file)

	# Cas général : module complet
	out += f".. automodule:: {dotted_module}\n"
	out += "   :members:\n"
	out += "   :show-inheritance:\n"
	out += "\n"
	return out


# --------------------------------------------------
def _rst_class_page(dotted_module: str, class_name: str, py_file: Path) -> str:
	"""
	Génère la page reStructuredText d'une classe.

	:param dotted_module: Nom qualifié du module.
	:param class_name: Nom de la classe à analyser.
	:param py_file: Fichier Python à analyser.
	:return: Contenu reStructuredText de la page.
	"""
	out = _rst_title(class_name, "=")
	fqcn = f"{dotted_module}.{class_name}"
	class_api = _parse_class_public_api(py_file, class_name)
	# Régions (pas imbriquées). Si région non fermée ⇒ jusqu'à fin de la classe.
	markers = _parse_regions_markers(py_file)

	# Trouver start/end de la classe (end_lineno dispo en Python 3.8+)
	tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
	class_start, class_end = 1, len(py_file.read_text(encoding="utf-8").splitlines())
	for n in tree.body:
		if isinstance(n, ast.ClassDef) and n.name == class_name:
			class_start = n.lineno
			class_end = n.end_lineno or class_end
			break

	regions = _clamp_regions_to_class(markers, class_start, class_end)

	# En-tête : documentation de la classe uniquement
	out += f".. autoclass:: {fqcn}\n"
	out += "   :show-inheritance:\n"
	out += "   :no-members:\n\n"

	# Attributs : pas de ré-affichage de la classe et aucun tri par région
	if class_api.attributes:
		out += _rst_title("Attributs", "-")
		# Pas forcément utile de retrier, mais au cas où pour conserver l'ordre du code...
		for a in sorted(class_api.attributes, key=lambda x: x.lineno): out += f".. autoattribute:: {fqcn}.{a.name}\n"
		out += "\n"

	# Méthodes : pas de ré-affichage de la classe
	if class_api.methods:
		out += _rst_title("Méthodes", "-")

		by_region: dict[str, list[ClassMember]] = {}
		region_order: list[str] = []

		for m in class_api.methods:
			r = _find_region_name(m.lineno, regions) or "Divers"
			if r not in region_order: region_order.append(r)
			by_region.setdefault(r, []).append(m)

		for r in region_order:
			out += _rst_title(r, "^")
			for m in by_region[r]: out += f".. automethod:: {fqcn}.{m.name}\n"
			out += "\n"

	return out


# --------------------------------------------------
def _generate_node_files(node: PackageNode, api_path: Path = API_PATH):
	"""
	Écrit récursivement les pages reStructuredText d’un package.

	:param node: Package et descendants directs à documenter.
	:param api_path: Chemin du dossier de sortie des pages API.
	"""
	# Page package
	package_file = api_path / f"{node.dotted_name}.rst"
	package_file.write_bytes(_rst_package_page(node).encode("utf-8"))

	# Pages modules
	for py in _iter_public_py_modules(node.dir_path):
		mod = f"{node.dotted_name}.{py.stem}"
		(api_path / f"{mod}.rst").write_bytes(_rst_module_page(mod, py).encode("utf-8"))

	# Récursion
	for sub in node.subpackages: _generate_node_files(sub, api_path)


# --------------------------------------------------
def _build_tree(package_dir: Path, dotted_name: str) -> PackageNode:
	"""
	Construit récursivement l’arborescence publique d’un package.

	:param package_dir: Chemin du dossier du package.
	:param dotted_name: Nom qualifié du package.
	:return: Package avec ses modules et sous-packages publics.
	"""
	modules = tuple(f"{dotted_name}.{py.stem}" for py in _iter_public_py_modules(package_dir))
	subpackages = tuple(_build_tree(subpkg_dir, f"{dotted_name}.{subpkg_dir.name}") for subpkg_dir in _iter_public_subpackages(package_dir))
	return PackageNode(dotted_name=dotted_name, dir_path=package_dir, subpackages=subpackages, modules=modules)


# --------------------------------------------------
def generate_api_rst():
	"""
	Régénère les pages reStructuredText de l’API publique.

	Le dossier ``docs/api`` est supprimé puis recréé ; ses pages sont entièrement générées.

	:raises RuntimeError: Si le dossier source n’est pas un package Python.
	"""
	if not _is_python_package(MODULE_PATH):
		raise RuntimeError(f"MODULE_PATH n'est pas un package Python : {MODULE_PATH}")

	shutil.rmtree(API_PATH, ignore_errors=True)  # Supprime les anciennes pages avant régénération.
	API_PATH.mkdir(parents=True, exist_ok=True)

	tree = _build_tree(MODULE_PATH, dotted_name=MODULE_NAME)
	_generate_node_files(tree, API_PATH)


# ==================================================
# endregion Génération RST
# ==================================================

# --------------------------------------------------
if __name__ == "__main__":
	generate_api_rst()
	print(f"RST API générés dans : {API_PATH}")
