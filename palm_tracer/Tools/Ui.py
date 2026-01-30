"""Fichier de fonctions génériques pour la gestion des interfaces Utilisateurs QT et l'affichage console"""
from pathlib import Path
from typing import Any

from colorama import Fore, Style
from qtpy.QtCore import Qt
from qtpy.QtGui import QFontMetrics
from qtpy.QtWidgets import QDoubleSpinBox, QFormLayout, QFrame, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLayout, QSpinBox, QVBoxLayout, QWidget

# ==================================================
# region Constants
# ==================================================
# Style pour une ligne d'information
STYLESHEET_INFO: str = "color: #666666; font-style: italic; padding: 2px;"

# Style général du layout (Pour le moment uniquement sur les QPushButton).
STYLESHEET_GENERAL: str = """
			QPushButton { border: 1px solid #c7c7c7; padding: 5px; background: #f7f7f7; }
			QPushButton + QPushButton { border-left: none; } /* fusion visuelle */
			QPushButton:first-child { border-top-left-radius: 5px; border-bottom-left-radius: 5px; }
			QPushButton:last-child { border-top-right-radius: 5px; border-bottom-right-radius: 5px; }
			QPushButton:pressed { background: #e9eff7; border-color: #6aa0e8; }
			QPushButton:checked	{ background: #e9eff7; border-color: #6aa0e8; }
			QPushButton:disabled { color: #999; background: #fafafa; }
			"""

# Configuration par défaut de l'interface Plotly opur les différents standalone.
CONFIG_PLOTLY: dict[str, Any] = {
		"responsive":             True,
		"displayModeBar":         True,
		"displaylogo":            False,
		"modeBarButtonsToRemove": ["zoom2d", "pan2d", "select2d", "lasso2d", "zoomIn2d", "zoomOut2d", "autoScale2d",
								   "resetScale2d", "hoverClosestCartesian", "hoverCompareCartesian"],
		"toImageButtonOptions":   dict(format="png", height=1200, width=1200, scale=2)}

# Espace par défaut de l'interface (padding, marge...).
COMMON_SPACE: int = 5


# ==================================================
# endregion Constants
# ==================================================

# ==================================================
# region UI Build
# ==================================================
##################################################
def add_setting_row(form: QFormLayout, label: str, widget: QWidget, space: int = 0, margin: int = 0):
	"""
	Ajoute une ligne de paramètre dans un :class:`QFormLayout`.

	Le champ (colonne de droite) est encapsulé dans un :class:`QHBoxLayout`	contenant le widget puis un ``stretch``.
	Cela évite que le widget s'étire horizontalement jusqu'au bord droit de l'onglet : il conserve sa taille naturelle (*sizeHint*) et l'espace	restant est
	laissé vide à droite.

	:param form: Formulaire cible à modifier (modification in-place via :meth:`addRow`).
	:param label: Texte du label (colonne de gauche).
	:param widget: Widget à placer dans la colonne de droite (spinbox, checkbox, combobox, ...).
	:param space: Valeur (en pixels) utilisée pour l'espacement du layout. Par défaut : ``0``.
	:param margin: Valeur (en pixels) utilisée pour les marges du layout. Par défaut : ``0``.
	"""
	layout = QHBoxLayout()
	init_layout(layout, space, margin)
	layout.addWidget(widget)
	layout.addStretch(1)  # pousse tout à gauche, espace vide à droite
	form.addRow(label, layout)


##################################################
def init_layout(layout: QLayout, space: int = COMMON_SPACE, margin: int = COMMON_SPACE):
	"""
	Configure un layout avec des marges et un espacement uniformes.

	Cette fonction applique des marges identiques sur les 4 côtés et un espacement identique entre widgets / sous-layouts.

	:param layout: Layout à configurer (ex: :class:`QVBoxLayout`, :class:`QGridLayout`, etc.).
	:param space: Valeur (en pixels) utilisée pour l'espacement du layout. Par défaut : ``COMMON_SPACE``.
	:param margin: Valeur (en pixels) utilisée pour les marges du layout. Par défaut : ``COMMON_SPACE``.
	"""
	layout.setContentsMargins(margin, margin, margin, margin)
	layout.setSpacing(space)			 # Fait comme setHorizontalSpacing et setVerticalSpacing sur tous les types de calques sauf QFormLayout
	if isinstance(layout, QFormLayout):  # Cas particulier
		layout.setHorizontalSpacing(space)
		layout.setVerticalSpacing(space)


##################################################
def make_tab(parent: QWidget | None = None, space: int = COMMON_SPACE, margin: int = COMMON_SPACE) -> tuple[QWidget, QVBoxLayout]:
	"""
	Crée un onglet prêt à l'emploi (widget conteneur + layout vertical).

	L'onglet est représenté par un :class:`QWidget` et contient un :class:`QVBoxLayout` configuré avec des marges et un espacement uniformes.

	:param parent: Parent Qt du widget onglet (peut être ``None`` si défini plus tard).
	:param space: Valeur (en pixels) utilisée pour l'espacement du layout. Par défaut : ``COMMON_SPACE``.
	:param margin: Valeur (en pixels) utilisée pour les marges du layout. Par défaut : ``COMMON_SPACE``.

	:return: Un tuple ``(tab, layout)`` où ``tab`` est le widget de l'onglet et ``layout`` son calque.
	"""
	tab = QWidget(parent)
	layout = QVBoxLayout(tab)
	init_layout(layout, space, margin)
	return tab, layout


##################################################
def make_group(parent: QWidget | None = None, name: str = "", space: int = COMMON_SPACE, margin: int = COMMON_SPACE) -> tuple[QGroupBox, QVBoxLayout]:
	"""
	Crée un :class:`QGroupBox` avec un layout vertical configuré.

	:param parent: Parent Qt du group box (peut être ``None`` si défini plus tard).
	:param name: Titre affiché dans l'entête du group box.
	:param space: Valeur (en pixels) utilisée pour l'espacement du layout. Par défaut : ``COMMON_SPACE``.
	:param margin: Valeur (en pixels) utilisée pour les marges du layout. Par défaut : ``COMMON_SPACE``.

	:return: Un tuple ``(group, layout)`` où : ``group`` est le :class:`QGroupBox` créé et ``layout`` son calque.
	"""
	group = QGroupBox(name, parent)
	layout = QVBoxLayout(group)
	init_layout(layout, space, margin)
	return group, layout


##################################################
def make_form(parent: QWidget | None = None, space: int = COMMON_SPACE, margin: int = COMMON_SPACE) -> QFormLayout:
	"""
	Crée et configure un :class:`QFormLayout` pour des paramètres.

	Configuration appliquée :
	- labels alignés à droite et centrés verticalement ;
	- formulaire ancré en haut à gauche ;
	- espacements horizontaux/verticaux adaptés à une UI de réglages ;
	- politique de croissance des champs : les widgets de droite restent à leur *sizeHint* (évite qu'ils s'étirent jusqu'au bord droit).

	:param parent: Parent Qt du layout (peut être ``None`` si défini plus tard).
	:param space: Valeur (en pixels) utilisée pour l'espacement du layout. Par défaut : ``COMMON_SPACE``.
	:param margin: Valeur (en pixels) utilisée pour les marges du layout. Par défaut : ``COMMON_SPACE``.

	:return: Le :class:`QFormLayout` configuré.
	"""
	layout = QFormLayout(parent)
	init_layout(layout, space, margin)
	layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
	layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
	layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.FieldsStayAtSizeHint)
	return layout


##################################################
def make_info_grid(elements: dict[str, dict[str, QLabel | str]], title: str, size: int = 2, parent: QWidget | None = None,
				   space: int = COMMON_SPACE, margin: int = COMMON_SPACE) -> QGridLayout:
	"""
	Construit une colonne (titre + lignes) sous forme de QGridLayout.

	:param elements:
	:param title:
	:param size:
	:param parent:
	:param space:
	:param margin:
	:return:
	"""
	layout = QGridLayout(parent)
	init_layout(layout, space, margin)

	# Titre de colonne
	title_lbl = QLabel(title)
	title_lbl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
	title_lbl.setStyleSheet("font-weight: 600;")
	layout.addWidget(title_lbl, 0, 0, 1, size)  # Titre
	layout.addWidget(make_horizontal_separator(), 1, 0, 1, size)  # Séparateur horizontal

	# Colonnes fixes : label | value | unit. On force la colonne "value" à s’étendre, pour garder l’alignement propre.
	layout.setColumnStretch(0, 0)					# label
	layout.setColumnStretch(1, 1)					# value (s'étire)
	if size == 3:    layout.setColumnStretch(2, 0)  # unit

	row = 2
	for key, item in elements.items():
		lbl: QLabel = item["label"]
		val: QLabel = item["value"]
		tips: str = item.get("tips", "")

		if tips: lbl.setToolTip(tips)  # Tooltips collé au label

		# Alignements : gauche | droite | gauche
		val.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

		layout.addWidget(lbl, row, 0)
		layout.addWidget(val, row, 1)

		if size == 3:
			unit: QLabel = item["unit"]
			unit.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
			layout.addWidget(unit, row, 2)

		row += 1

	return layout


##################################################
def make_path_label(value: str = "", parent: QWidget | None = None) -> QLabel:
	"""

	:param value:
	:param parent:
	:return:
	"""
	lbl = QLabel(value, parent)
	lbl.setStyleSheet(STYLESHEET_INFO)
	return lbl


##################################################
def update_path_label(lbl: QLabel, path: Path):
	"""

	:param lbl:
	:param path:
	"""
	lbl.setText(path.name)
	lbl.setToolTip(str(path))


##################################################
def make_vertical_separator(color: str = "#B0B0B0") -> QFrame:
	"""
	Crée un séparateur vertical discret.

	:param color: Couleur du séparateur (format CSS, ex: ``"#B0B0B0"``).
	:return: Le :class:`QFrame` configuré.
	"""
	sep = QFrame()
	sep.setFrameShape(QFrame.Shape.VLine)
	sep.setFrameShadow(QFrame.Shadow.Sunken)
	sep.setStyleSheet(f"QFrame {{ color: {color}; min-width: 1px; }}")
	return sep


##################################################
def make_horizontal_separator(color: str = "#B0B0B0") -> QFrame:
	"""
	Crée un séparateur horizontal discret.

	:param color: Couleur du séparateur (format CSS, ex: ``"#B0B0B0"``).
	:return: Le :class:`QFrame` configuré.
	"""
	sep = QFrame()
	sep.setFrameShape(QFrame.Shape.HLine)
	sep.setFrameShadow(QFrame.Shadow.Sunken)
	sep.setStyleSheet(f"QFrame {{ color: {color}; min-height: 1px; }}")
	return sep


##################################################
def make_spin(parent: QWidget | None = None, minimum: int | float = 0, maximum: int | float = 1,
			  step: int | float = 1, value: int | float = 0, decimals: int = 0, buttons:bool = True) -> QDoubleSpinBox | QSpinBox:
	"""

	:param parent:
	:param minimum:
	:param maximum:
	:param step:
	:param value:
	:param decimals:
	:param buttons:
	:return:
	"""
	if decimals <= 0:
		spin = QSpinBox(parent, minimum=minimum, maximum=maximum, singleStep=step, value=value)
		spin.setStyleSheet("QSpinBox { padding: 0; }")								   # Suppression du padidng
		if not buttons: spin.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)		   # Supprime les flèches
	else:
		spin = QDoubleSpinBox(parent, decimals=decimals, minimum=minimum, maximum=maximum, singleStep=step, value=value)
		spin.setStyleSheet("QDoubleSpinBox { padding: 0; }")						   # Suppression du padidng
		if not buttons: spin.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)  # Supprime les flèches

	spin.setContentsMargins(0, 0, 0, 0)												   # Suppresison des marges
	spin.setAlignment(Qt.AlignmentFlag.AlignCenter)									   # Définir l'alignement au centre.
	set_spinbox_width(spin)															   # Définition de la largeur maximale
	return spin


##################################################
def set_spinbox_width(spinbox: QSpinBox | QDoubleSpinBox):
	"""
	Ajuste la largeur du widget :class:`QSpinBox` (ou :class:`QDoubleSpinBox`) au nombre de caractères affichables.

	:param spinbox:
	"""
	# ---- estimation du nombre de caractères ----
	min_val, max_val = spinbox.minimum(), spinbox.maximum()
	max_abs = max(abs(min_val), abs(max_val))
	has_sign = min_val < 0
	char_count = max(1, len(str(int(max_abs))))
	if has_sign: char_count += 1
	if isinstance(spinbox, QDoubleSpinBox): char_count += 1 + spinbox.decimals()  # "." + décimales

	# ---- conversion caractères → pixels ----
	metrics = QFontMetrics(spinbox.font())
	# petite marge de confort (boutons up/down, padding) "−" est en général le caractère le plus long en cas de police non uniforme.
	width_px = char_count * metrics.horizontalAdvance("−") + 50
	spinbox.setFixedWidth(width_px)


# ==================================================
# endregion UI Build
# ==================================================

# ==================================================
# region Callbacks
# ==================================================
##################################################
def sync_spin(target: QDoubleSpinBox | QSpinBox, value: float | int):
	"""
	Synchronise une spinbox avec la valeur envoyé (par signal).
	On bloque les signaux le temps de la mise à jour pour éviter les appels en série.

	s'utilise comme ceci :
		spin_1.valueChanged.connect(lambda v: Utils.sync_spin(spin_2, v))
		spin_2.valueChanged.connect(lambda v: Utils.sync_spin(spin_1, v))

	:param target: Spinbox à mettre à jour.
	:param value: Valeur à insérer.
	"""
	target.blockSignals(True)
	target.setValue(value)
	target.blockSignals(False)


# ==================================================
# endregion Callbacks
# ==================================================

# ==================================================
# region Prints
# ==================================================
##################################################
def print_error(msg: str):
	"""
	Affiche un message avec une couleur rouge

	:param msg: message à afficher
	"""
	print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)


##################################################
def print_warning(msg: str):
	"""
	Affiche un message avec une couleur jaune

	:param msg: message à afficher
	"""
	print(Fore.YELLOW + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)


##################################################
def print_success(msg: str):
	"""
	Affiche un message avec une couleur verte

	:param msg: message à afficher
	"""
	print(Fore.GREEN + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)


##################################################
def format_time(seconds):
	"""
	Fonction pour formater le temps en secondes en HH:MM:SS.

	:param seconds: Temps en secondes
	:return: chaine de caractère representant le temps au format HH:MM:SS.
	"""
	hours = int(seconds // 3600)
	minutes = int((seconds % 3600) // 60)
	seconds = int(seconds % 60)
	return f"{hours:02}:{minutes:02}:{seconds:02}"
# ==================================================
# endregion Prints
# ==================================================
