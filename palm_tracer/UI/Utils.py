"""Fichier de fonctions génériques et constantes pour les widgets"""
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QFormLayout, QFrame, QGroupBox, QHBoxLayout, QLayout, QVBoxLayout, QWidget

# ==================================================
# region Constants
# ==================================================
STYLESHEET_GENERAL: str = """
			QPushButton { border: 1px solid #c7c7c7; padding: 5px; background: #f7f7f7; }
			QPushButton + QPushButton { border-left: none; } /* fusion visuelle */
			QPushButton:first-child { border-top-left-radius: 5px; border-bottom-left-radius: 5px; }
			QPushButton:last-child { border-top-right-radius: 5px; border-bottom-right-radius: 5px; }
			QPushButton:pressed { background: #e9eff7; border-color: #6aa0e8; }
			QPushButton:checked	{ background: #e9eff7; border-color: #6aa0e8; }
			QPushButton:disabled { color: #999; background: #fafafa; }
			"""

STYLESHEET_INFO: str = "color: #666666; font-style: italic; padding: 2px;"

COMMON_SPACE: int = 10


# ==================================================
# endregion Constants
# ==================================================

# ==================================================
# region Functions
# ==================================================
##################################################
def add_setting_row(form: QFormLayout, label: str, widget: QWidget):
	"""
	Ajoute une ligne de paramètre dans un :class:`QFormLayout`.

	Le champ (colonne de droite) est encapsulé dans un :class:`QHBoxLayout`	contenant le widget puis un ``stretch``.
	Cela évite que le widget s'étire horizontalement jusqu'au bord droit de l'onglet : il conserve sa taille naturelle (*sizeHint*) et l'espace	restant est
	laissé vide à droite.

	:param form: Formulaire cible à modifier (modification in-place via :meth:`addRow`).
	:param label: Texte du label (colonne de gauche).
	:param widget: Widget à placer dans la colonne de droite (spinbox, checkbox, combobox, ...).
	"""
	layout = QHBoxLayout()
	layout.setContentsMargins(0, 0, 0, 0)
	layout.addWidget(widget)
	layout.addStretch(1)  # pousse tout à gauche, espace vide à droite
	form.addRow(label, layout)


##################################################
def init_layout(layout: QLayout, space: int = COMMON_SPACE):
	"""
	Configure un layout principal avec des marges et un espacement uniformes.

	Cette fonction applique des marges identiques sur les 4 côtés et un espacement identique entre widgets / sous-layouts.

	:param layout: Layout à configurer (ex: :class:`QVBoxLayout`, :class:`QGridLayout`, etc.).
	:param space: Valeur (en pixels) utilisée pour les marges et l'espacement du layout. Par défaut : ``COMMON_SPACE``.
	"""
	layout.setContentsMargins(space, space, space, space)
	layout.setSpacing(space)


##################################################
def make_tab(parent: QWidget | None, space: int = COMMON_SPACE) -> tuple[QWidget, QVBoxLayout]:
	"""
	Crée un onglet prêt à l'emploi (widget conteneur + layout vertical).

	L'onglet est représenté par un :class:`QWidget` et contient un :class:`QVBoxLayout` configuré avec des marges et un espacement uniformes.

	:param parent: Parent Qt du widget onglet (peut être ``None`` si défini plus tard).
	:param space: Valeur (en pixels) utilisée pour les marges et l'espacement du layout. Par défaut : ``COMMON_SPACE``.

	:return: Un tuple ``(tab, layout)`` où ``tab`` est le widget de l'onglet et ``layout`` son calque.
	"""
	tab = QWidget(parent)
	layout = QVBoxLayout(tab)
	init_layout(layout, space)
	return tab, layout


##################################################
def make_group(parent: QWidget | None, name: str, space: int = COMMON_SPACE) -> tuple[QGroupBox, QVBoxLayout]:
	"""
	Crée un :class:`QGroupBox` avec un layout vertical configuré.

	:param parent: Parent Qt du group box (peut être ``None`` si défini plus tard).
	:param name: Titre affiché dans l'entête du group box.
	:param space: Valeur (en pixels) utilisée pour les marges et l'espacement du layout. Par défaut : ``COMMON_SPACE``.

	:return: Un tuple ``(group, layout)`` où : ``group`` est le :class:`QGroupBox` créé et ``layout`` son calque.
	"""
	group = QGroupBox(name, parent)
	layout = QVBoxLayout(group)
	init_layout(layout, space)
	return group, layout


##################################################
def make_form(parent: QWidget | None, space: int = COMMON_SPACE) -> QFormLayout:
	"""
	Crée et configure un :class:`QFormLayout` pour des paramètres.

	Configuration appliquée :
	- labels alignés à droite et centrés verticalement ;
	- formulaire ancré en haut à gauche ;
	- espacements horizontaux/verticaux adaptés à une UI de réglages ;
	- politique de croissance des champs : les widgets de droite restent à leur *sizeHint* (évite qu'ils s'étirent jusqu'au bord droit).

	:param parent: Parent Qt du layout (peut être ``None`` si défini plus tard).
	:param space: Valeur (en pixels) utilisée pour les marges et l'espacement du layout. Par défaut : ``COMMON_SPACE``.

	:return: Le :class:`QFormLayout` configuré.
	"""
	form = QFormLayout(parent)
	form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
	form.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
	form.setHorizontalSpacing(space)
	form.setVerticalSpacing(space)
	form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.FieldsStayAtSizeHint)
	return form


##################################################
def make_vertical_separator() -> QFrame:
	"""Crée un séparateur vertical discret."""
	sep = QFrame()
	sep.setFrameShape(QFrame.Shape.VLine)
	sep.setFrameShadow(QFrame.Shadow.Sunken)
	sep.setStyleSheet("""QFrame {color: #B0B0B0;}""")
	return sep


##################################################
def make_horizontal_separator() -> QFrame:
	"""Crée un séparateur horizontal discret."""
	sep = QFrame()
	sep.setFrameShape(QFrame.Shape.HLine)
	sep.setFrameShadow(QFrame.Shadow.Sunken)
	sep.setStyleSheet("QFrame { color: #B0B0B0; }")
	return sep

# ==================================================
# endregion Functions
# ==================================================
