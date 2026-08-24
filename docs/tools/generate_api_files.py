"""Génère les pages reStructuredText de l'API publique pour Sphinx.

La génération repose sur l'analyse statique de l'arborescence Python et ne nécessite aucun import des modules documentés.
"""

from __future__ import annotations

import ast
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT_PATH = Path(__file__).resolve().parent.parent.parent
DOCS_PATH = ROOT_PATH / "docs"
API_PATH = DOCS_PATH / "api"
MODULE_PATH = ROOT_PATH / "palm_tracer"


# ==================================================
# region Class
# ==================================================
##################################################
@dataclass(frozen=True)
class ModulePublicApi:
	"""Décrit les symboles publics d'un module Python.

	:param classes: Noms des classes publiques, dans leur ordre de déclaration.
	:param functions: Noms des fonctions publiques, dans leur ordre de déclaration.
	:param constants: Noms des constantes publiques, dans leur ordre de déclaration.
	"""

	classes: tuple[str, ...]
	functions: tuple[str, ...]
	constants: tuple[str, ...]


##################################################
@dataclass(frozen=True)
class ClassMember:
	"""Identifie un membre public d'une classe.

	:param name: Nom du membre.
	:param lineno: Numéro de sa ligne de déclaration.
	"""

	name: str
	lineno: int


##################################################
@dataclass(frozen=True)
class ClassPublicApi:
	"""Décrit les membres publics d'une classe Python.

	:param attributes: Attributs publics, dans leur ordre de déclaration.
	:param methods: Méthodes publiques, dans leur ordre de déclaration.
	"""

	attributes: tuple[ClassMember, ...]
	methods: tuple[ClassMember, ...]


##################################################
@dataclass(frozen=True)
class PackageNode:
	"""Décrit un package Python et ses descendants directs.

	:param dotted_name: Nom qualifié du package.
	:param dir_path: Chemin du répertoire correspondant.
	:param subpackages: Sous-packages directs.
	:param modules: Modules publics directs.
	"""

	dotted_name: str
	dir_path: Path
	subpackages: tuple["PackageNode", ...]
	modules: tuple[str, ...]  # noms en dotted (incluant le package), sans __init__


# ==================================================
# endregion Class
# ==================================================

# ==================================================
# region File Check
# ==================================================
##################################################
def _is_python_package(directory: Path) -> bool:
	"""Retourne True si directory contient un __init__.py."""
	return directory.is_dir() and (directory / "__init__.py").is_file()


##################################################
def _iter_public_py_modules(package_dir: Path) -> Iterable[Path]:
	"""Liste les fichiers .py publics d'un package (hors __init__.py)."""
	for py in sorted(package_dir.glob("*.py")):
		if py.name == "__init__.py": continue
		if py.name.startswith("_"): continue  # Fichiers privés
		yield py


##################################################
def _iter_public_subpackages(package_dir: Path) -> Iterable[Path]:
	"""Liste les sous-packages publics d'un package."""
	for child in sorted(package_dir.iterdir()):
		if child.name.startswith("_"): continue  # Package privés
		if _is_python_package(child): yield child


# ==================================================
# endregion File Check
# ==================================================


# ==================================================
# region Parsing
# ==================================================
##################################################
def _parse_public_api_from_file(py_file: Path) -> ModulePublicApi:
	"""Extrait les classes/fonctions/constantes publiques d'un fichier .py sans l'importer."""
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


##################################################
def _parse_class_public_api(py_file: Path, class_name: str) -> ClassPublicApi:
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


##################################################
def _is_property(func: ast.FunctionDef) -> bool:
	for dec in func.decorator_list:
		if isinstance(dec, ast.Name) and dec.id == "property": return True
		if isinstance(dec, ast.Attribute) and dec.attr == "setter": return True
	return False


##################################################
def _parse_regions_markers(py_file: Path) -> list[tuple[int, int | None, str]]:
	"""Retourne les régions sous la forme (start_line, end_line_or_none, name).

	- start_line / end_line sont 1-indexés.
	- Si '# endregion' absent, end_line vaut None (sera clos plus tard).
	- Pas de régions imbriquées (convention projet).
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


##################################################
def _clamp_regions_to_class(regions: list[tuple[int, int | None, str]], class_start: int, class_end: int) -> list[tuple[int, int, str]]:
	"""Applique la règle : région ouverte = jusqu'à la fin de la classe, et garde seulement celles qui intersectent la classe."""
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


##################################################
def _find_region_name(lineno: int, regions: list[tuple[int, int, str]]) -> str:
	"""Retourne le nom de région contenant lineno, sinon ''."""
	for start, end, name in regions:
		if start <= lineno <= end: return name
	return ""


##################################################
def _unique_members_preserve_order(items: list[ClassMember]) -> tuple[ClassMember, ...]:
	seen: set[str] = set()
	out: list[ClassMember] = []
	for m in sorted(items, key=lambda x: x.lineno):  # bysource
		if m.name in seen: continue
		seen.add(m.name)
		out.append(m)
	return tuple(out)


##################################################
def _unique_preserve_order(items: Iterable[str]) -> tuple[str, ...]:
	"""Supprime les doublons en conservant l'ordre d'apparition."""
	seen: set[str] = set()
	out: list[str] = []
	for x in items:
		if x in seen: continue
		seen.add(x)
		out.append(x)
	return tuple(out)


# ==================================================
# endregion Parsing
# ==================================================

# ==================================================
# region RST Generation
# ==================================================

##################################################
def _rst_title(title: str, sep: str = "=") -> str:
	"""Génère un titre RST avec underline '=','-','^'."""
	return f"{title}\n{sep * len(title)}\n\n"


##################################################
def _rst_package_page(node: PackageNode) -> str:
	"""Génère le contenu RST pour une page de package avec 2 toctree."""
	# Titre principal : tu peux décider d’un mapping spécifique pour la racine.
	if node.dotted_name == "palm_tracer": title = "PALM Tracer API Reference"
	else: title = node.dotted_name.split(".")[-1]
	out = _rst_title(title)

	# Optionnel : petit texte d’intro auto (tu peux faire un mapping manuel si tu veux)
	if node.dotted_name != "palm_tracer":
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


##################################################
def _rst_module_page(dotted_module: str, py_file: Path) -> str:
	"""Génère une page module avec une stratégie :
	- 1 classe publique, 0 fonction publique ⇒ autosummary vers la classe (template class.rst)
	- sinon ⇒ automodule (ou autosummary mixte si tu préfères)
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


##################################################
def _rst_class_page(dotted_module: str, class_name: str, py_file: Path) -> str:
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

	# Header: doc de classe seule
	out += f".. autoclass:: {fqcn}\n"
	out += "   :show-inheritance:\n"
	out += "   :no-members:\n\n"

	# Attributs : pas de ré-affichage de la classe et aucun tri par région
	if class_api.attributes:
		out += _rst_title("Attributs", "-")
		# pas forcément utile de retrier, mais au cas où pour conserver l'ordre du code...
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


##################################################
def _generate_node_files(node: PackageNode, api_path: Path = API_PATH) -> None:
	"""Génère récursivement les fichiers package + modules."""
	# Page package
	package_file = api_path / f"{node.dotted_name}.rst"
	package_file.write_text(_rst_package_page(node), encoding="utf-8")

	# Pages modules
	for py in _iter_public_py_modules(node.dir_path):
		mod = f"{node.dotted_name}.{py.stem}"
		(api_path / f"{mod}.rst").write_text(_rst_module_page(mod, py), encoding="utf-8")

	# Recurse
	for sub in node.subpackages: _generate_node_files(sub, api_path)


##################################################
def _build_tree(package_dir: Path, dotted_name: str) -> PackageNode:
	"""Construit récursivement l'arbre des packages/modules."""
	modules = tuple(f"{dotted_name}.{py.stem}" for py in _iter_public_py_modules(package_dir))
	subpackages = tuple(_build_tree(subpkg_dir, f"{dotted_name}.{subpkg_dir.name}") for subpkg_dir in _iter_public_subpackages(package_dir))
	return PackageNode(dotted_name=dotted_name, dir_path=package_dir, subpackages=subpackages, modules=modules)


##################################################
def generate_api_rst() -> None:
	"""Point d'entrée : génère tous les fichiers .rst de l'API."""
	if not _is_python_package(MODULE_PATH): raise RuntimeError(f"MODULE_PATH n'est pas un package Python : {MODULE_PATH}")

	shutil.rmtree(API_PATH, ignore_errors=True)  # Il y a une option de check de différence
	API_PATH.mkdir(parents=True, exist_ok=True)

	tree = _build_tree(MODULE_PATH, dotted_name="palm_tracer")
	_generate_node_files(tree, API_PATH)


# ==================================================
# endregion RST Generation
# ==================================================

##################################################
if __name__ == "__main__":
	generate_api_rst()
	print(f"RST API générés dans : {API_PATH}")
