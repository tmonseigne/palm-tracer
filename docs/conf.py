"""Configuration file for the Sphinx documentation builder."""

# -- Gestion des fichiers à ajouter ------------------------------------------

import shutil
import sys
from pathlib import Path

# Ajout du chemin vers le dossier palm_tracer
root = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(root), str(root / "palm_tracer")]

# -- Project information -----------------------------------------------------

project = "PALM Tracer"
copyright = "2025, Thibaut Monseigne"
author = "Thibaut Monseigne"
language = "fr"

# -- General configuration ---------------------------------------------------

extensions = [
		"sphinx.ext.autodoc",
		"sphinx.ext.autosummary",
		"sphinx.ext.autosectionlabel",
		"sphinx.ext.intersphinx",
		"sphinx.ext.mathjax",
		"sphinx.ext.napoleon",
		"sphinx.ext.todo",
		"sphinx.ext.viewcode",
		"sphinx.ext.graphviz",
		"sphinxcontrib.jquery",
		"sphinx_qt_documentation",
		]

autodoc_typehints = "both"

intersphinx_mapping = {
		"python":       ("https://docs.python.org/3", None),
		"numpy":        ("https://numpy.org/doc/stable", None),
		"pandas":       ("https://pandas.pydata.org/pandas-docs/stable", None),
		"scipy":        ("https://docs.scipy.org/doc/scipy/", None),
		"scikit-image": ("https://scikit-image.org/docs/stable/", None),
		"matplotlib":   ("https://matplotlib.org/stable/", None),
		"seaborn":      ("https://seaborn.pydata.org/", None),
		"pillow":       ("https://pillow.readthedocs.io/en/stable/", None),
		"psutil":       ("https://psutil.readthedocs.io/en/latest/", None),
		"pytest":       ("https://docs.pytest.org/en/latest/", None),
		"pytest-cov":   ("https://pytest-cov.readthedocs.io/en/latest/", None),
		"pytest-qt":    ("https://pytest-qt.readthedocs.io/en/latest/", None),
		"napari":       ("https://napari.org/stable/", None),
		"magicgui":     ("https://pyapp-kit.github.io/magicgui/", None),
		"sphinx":       ("https://www.sphinx-doc.org/en/master/", None),
		"plotly":       ("https://plotly.com/python-api-reference/", None),
		}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["css/custom.css"]
html_favicon = "_static/favicon.ico"

# Autoriser l'inclusion de contenu HTML brut
html_context = {"allow_html_in_rst": True}

# -- Automatisation ----------------------------------------------------------

autosummary_generate = False  # .			Evite des arborescences trop profondes et des liens internes vers de nouvelles pages
autodoc_member_order = "bysource"  # .		Evite le tri alphabétique
add_module_names = False  # .				Evite le nom des module(s) parent au début des objets
toc_object_entries_show_parents = "hide"  # Evite le nom des module(s) parent au début des objets dans l'arborescence
todo_include_todos = True
python_use_unqualified_type_names = True  # Evite le nom des module(s) parent au début des objets

suppress_warnings = ["autosectionlabel.*"]

# -- Multilingue ----------------------------------------------------------
locale_dirs = ["locale/"]
gettext_compact = False

# Création des fichiers de reférences de texte pour la traduction
# sphinx-build -b gettext docs/ docs/_build/gettext
# Création des fichiers de traductions
# sphinx-intl update -p docs/_build/gettext -d docs/locale -l fr -l en
# Build de la documentation avec les traductions
# sphinx-build -b html -D language=fr docs docs/_build/html
# sphinx-build -b html -D language=en docs docs/_build/html/en

def copy_dir(src: str | Path, dst: str | Path) -> None:
	"""Copie récursivement un dossier source vers un dossier destination."""
	src, dst = Path(src), Path(dst)
	if not src.exists(): return  # .				 Copie les fichiers si le dossier source existe
	dst.mkdir(parents=True, exist_ok=True)  # .		 Crée le dossier de destination s'il n'existe pas
	shutil.copytree(src, dst, dirs_exist_ok=True)  # Copie récursivement les fichiers du dossier source vers le dossier de destination.


copy_dir("reports", "_build/html/reports")
copy_dir("reports", "_build/html/en/reports")

default_language_code = "fr"

languages = [("Français", "fr"), ("English", "en")]


def setup(app):
	"""Ajoute des variables de contexte HTML (Jinja) en fonction de la langue réellement utilisée."""

	def _inject_context(app_, pagename, templatename, context, doctree):
		cur = app_.config.language or default_language_code
		context["default_language_code"] = default_language_code
		context["current_language_code"] = cur
		context["languages"] = languages

	app.connect("html-page-context", _inject_context)
