"""
Fonctions utilitaires génériques pour la construction d'interfaces utilisateur Qt et l'affichage console coloré.

Ce module regroupe :
	- des helpers pour créer et configurer rapidement des layouts Qt cohérents (onglets, groupes, formulaires, séparateurs, spinbox, etc.) ;
	- des fonctions de synchronisation de widgets (callbacks) ;
	- des fonctions d'affichage console coloré (erreurs, warnings, succès) ;
	- quelques utilitaires généraux liés à l'IHM.

L'objectif est d'assurer :
	- une ergonomie homogène sur l'ensemble des interfaces ;
	- une réduction du boilerplate Qt ;
	- une meilleure lisibilité et maintenabilité du code UI.
"""

from pathlib import Path
from typing import Any

from colorama import Fore, Style
from qtpy.QtCore import Qt
from qtpy.QtGui import QFontMetrics
from qtpy.QtWidgets import (QButtonGroup, QDoubleSpinBox, QFormLayout, QFrame, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLayout, QPushButton, QScrollArea,
							QSpinBox, QVBoxLayout, QWidget)

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
def add_setting_row(form: QFormLayout, label: str, widget: QWidget, space: int = 0, margin: int = 0, *, tooltip: str = ""):
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
	:param tooltip: Tooltip à ajouter (si non vide).
	"""
	layout = QHBoxLayout()
	init_layout(layout, space, margin)
	layout.addWidget(widget)
	layout.addStretch(1)  # pousse tout à gauche, espace vide à droite
	label_widget = QLabel(label)
	label_widget.setToolTip(tooltip)
	form.addRow(label_widget, layout)


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
	layout.setSpacing(space)  # .		   Fait comme setHorizontalSpacing et setVerticalSpacing sur tous les types de calques sauf QFormLayout
	if isinstance(layout, QFormLayout):  # Cas particulier
		layout.setHorizontalSpacing(space)
		layout.setVerticalSpacing(space)


##################################################
def make_tab(parent: QWidget | None = None, space: int = COMMON_SPACE, margin: int = COMMON_SPACE) -> tuple[QWidget, QVBoxLayout]:
	"""
	Crée un onglet prêt à l'emploi (widget conteneur + layout vertical).

	L'onglet est représenté par un :class:`QWidget` et contient un :class:`QVBoxLayout` configuré avec des marges et un espacement uniformes.

	:param parent: Parent Qt du widget onglet (peut-être ``None`` si définie plus tard).
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

	:param parent: Parent Qt du group box (peut-être ``None`` si définie plus tard).
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
def make_exclusive_btn_group(labels: list[str], space: int = COMMON_SPACE) -> tuple[QHBoxLayout, QButtonGroup, dict[str, QPushButton]]:
	"""
	Crée un :class:`QGroupBox` avec un layout vertical configuré.

	:param labels: Titres affiché dans les boutons.
	:param space: Valeur (en pixels) utilisée pour l'espacement du layout. Par défaut : ``COMMON_SPACE``.

	:return: Un tuple ``(group, layout)`` où : ``group`` est le :class:`QGroupBox` créé et ``layout`` son calque.
	"""
	layout = QHBoxLayout()
	layout.setSpacing(space)
	group = QButtonGroup()
	group.setExclusive(True)
	buttons: dict[str, QPushButton] = {label: QPushButton(label) for label in labels}

	i = 0
	for _, button in buttons.items():
		button.setCheckable(True)
		button.setFocusPolicy(Qt.FocusPolicy.NoFocus)  # évite le focus rectangle
		layout.addWidget(button)
		group.addButton(button, i)  # Insertion dans le groupe exclusif
		i += 1

	buttons[labels[0]].setChecked(True)

	return layout, group, buttons


##################################################
def make_form(parent: QWidget | None = None, space: int = COMMON_SPACE, margin: int = COMMON_SPACE) -> QFormLayout:
	"""
	Crée et configure un :class:`QFormLayout` pour des paramètres.

	Configuration appliquée :
		- labels alignés à droite et centrés verticalement ;
		- formulaire ancré en haut à gauche ;
		- espacements horizontaux/verticaux adaptés à une UI de réglages ;
		- politique de croissance des champs : les widgets de droite restent à leur *sizeHint* (évite qu'ils s'étirent jusqu'au bord droit).

	:param parent: Parent Qt du layout (peut-être ``None`` si définie plus tard).
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
	Construit une colonne d'informations structurée sous forme de :class:`QGridLayout`.

	La grille est composée de : un titre de section (ligne 0), un séparateur horizontal, plusieurs lignes ``label / value`` (et éventuellement ``unit``).

	La colonne ``value`` est extensible afin de conserver un alignement propre, tandis que les labels et unités gardent leur taille naturelle.

	:param elements:
		Dictionnaire décrivant les lignes à afficher.
		Chaque entrée doit contenir :

			- ``"label"`` : :class:`QLabel` (libellé) ;
			- ``"value"`` : :class:`QLabel` (valeur associée) ;
			- optionnellement ``"unit"`` : :class:`QLabel` (unité) si ``size == 3`` ;
			- optionnellement ``"tips"`` : ``str`` (tooltip appliqué au label).
	:param title: Titre de la colonne affichée en haut de la grille.
	:param size: Nombre de colonnes : ``2`` → ``label | value``, ``3`` → ``label | value | unit``.
	:param parent: Parent Qt du layout (optionnel).
	:param space: Espacement interne entre les éléments (en pixels).
	:param margin: Marges du layout (en pixels).
	:return: Le :class:`QGridLayout` configuré.
	"""
	layout = QGridLayout(parent)
	init_layout(layout, space, margin)

	# Titre de colonne
	title_lbl = QLabel(title)
	title_lbl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
	title_lbl.setStyleSheet("font-weight: 600;")
	layout.addWidget(title_lbl, 0, 0, 1, size)  # .					Titre
	layout.addWidget(make_horizontal_separator(), 1, 0, 1, size)  # Séparateur horizontal

	# Colonnes fixes : label | value | unit. On force la colonne "value" à s'étendre, pour garder l'alignement propre.
	layout.setColumnStretch(0, 0)  # .								Label
	layout.setColumnStretch(1, 1)  # .								Value (s'étire)
	if size == 3:    layout.setColumnStretch(2, 0)  # .				Unit

	row = 2
	for key, item in elements.items():
		lbl: QLabel = item["label"]
		val: QLabel = item["value"]
		lbl.setToolTip(item.get("tips", ""))  # .					Tooltips collé au label

		# Alignements : gauche | droite | gauche (si une unité)
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
def make_file_info_group(space: int = COMMON_SPACE, margin: int = COMMON_SPACE) -> tuple[QGroupBox, dict[str, QLabel]]:
	"""
	Construit un groupe d'information pour le listing des fichiers calculés.

	Le groupe est composée de : un titre, la liste des fichiers et leurs status.
	:return: Le :class:`QGroupBox` configuré ainsi que le lien vers les QLabel de status des fichiers.
	"""
	grp = QGroupBox("Informations")
	tips = {"File":         "Current stack.",
			"Localization": "Localizations on the current stack.",
			"Beads":        "Beads on the current stack.",
			"Tracking":     "Tracking on the current stack.",
			"MSD":          "Mean Square Displacement of tracks on the current stack.",
			"Instant D":    "Instant Diffusion of tracks on the current stack.",
			"Fit":          "Fit of tracks on the current stack."}

	# Statut des différentes tables (localisation / tracking / MSD / D / fit)
	status = {"File":         QLabel("No file"),
			  "Localization": QLabel("No"), "Beads": QLabel("No"), "Tracking": QLabel("No"),
			  "MSD":          QLabel("No"), "Instant D": QLabel("No"), "Fit": QLabel("No")}

	form = make_form(grp, space, margin)
	for key, value in status.items(): add_setting_row(form, f"{key}: ", value, tooltip=tips[key])
	return grp, status


##################################################
def make_path_label(value: str = "", parent: QWidget | None = None) -> QLabel:
	"""
	Crée un :class:`QLabel` stylisé pour afficher un chemin ou un nom de fichier.

	Le label utilise un style visuel discret (texte grisé et italique), adapté à l'affichage d'informations secondaires.

	:param value: Texte initial affiché (généralement un nom de fichier).
	:param parent: Parent Qt du label.
	:return: Le :class:`QLabel` configuré.
	"""
	lbl = QLabel(value, parent)
	lbl.setStyleSheet(STYLESHEET_INFO)
	return lbl


##################################################
def update_path_label(lbl: QLabel, path: str | Path):
	"""
	Mets à jour un label de chemin avec un nouvel objet :class:`pathlib.Path`.

	Le texte visible correspond uniquement au ``name`` du fichier/dossier, le chemin complet est placé dans le tooltip.

	:param lbl: Label à mettre à jour.
	:param path: Chemin à afficher.
	"""
	path = Path(path)
	lbl.setText(path.name)
	lbl.setToolTip(str(path))


##################################################
def make_vertical_scroll(widget: QWidget) -> QScrollArea:
	"""
	Crééer une zone scrollable verticalement
	:return: La :class:`QScrollArea` configuré.
	"""
	scroll = QScrollArea()
	scroll.setWidgetResizable(True)  # le contenu suit la largeur disponible.
	scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
	scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
	scroll.setFrameShape(QScrollArea.Shape.NoFrame)
	scroll.setWidget(widget)
	return scroll


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
			  step: int | float = 1, value: int | float = 0, decimals: int = 0, buttons: bool = True) -> QSpinBox | QDoubleSpinBox:
	"""
	Crée une :class:`QSpinBox` ou :class:`QDoubleSpinBox` configurée de manière compacte.

	Le type de spinbox est choisi automatiquement : :class:`QSpinBox` si ``decimals ≤ 0``, :class:`QDoubleSpinBox` sinon.

	Configuration appliquée :
		- suppression des marges et paddings inutiles ;
		- alignement centré du texte ;
		- largeur ajustée dynamiquement en fonction du range et du nombre de décimales ;
		- possibilité de masquer les boutons d'incrément.

	:param parent: Parent Qt du widget.
	:param minimum: Valeur minimale autorisée.
	:param maximum: Valeur maximale autorisée.
	:param step: Pas d'incrément.
	:param value: Valeur initiale.
	:param decimals: Nombre de décimales (si > 0 → spinbox flottante).
	:param buttons: Affiche ou non les boutons up/down.
	:return: La spinbox configurée (:class:`QSpinBox` ou :class:`QDoubleSpinBox`).
	"""
	if decimals <= 0:
		spin = QSpinBox(parent, minimum=minimum, maximum=maximum, singleStep=step, value=value)
		spin.setStyleSheet("QSpinBox { padding: 0; }")  # .								 Suppression du padidng
		if not buttons: spin.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)  # .	 Supprime les flèches
	else:
		spin = QDoubleSpinBox(parent, decimals=decimals, minimum=minimum, maximum=maximum, singleStep=step, value=value)
		spin.setStyleSheet("QDoubleSpinBox { padding: 0; }")  # .						 Suppression du padidng
		if not buttons: spin.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)  # Supprime les flèches

	spin.setContentsMargins(0, 0, 0, 0)  # .											 Suppresison des marges
	spin.setAlignment(Qt.AlignmentFlag.AlignCenter)  # .								 Définir l'alignement au centre.
	set_spin_width(spin)  # .															 Définition de la largeur maximale
	return spin


##################################################
def set_spin_width(spin: QSpinBox | QDoubleSpinBox):
	"""
	Ajuste la largeur fixe d'une spinbox en fonction du contenu affichable.

	La largeur est estimée à partir du nombre maximal de caractères nécessaires (valeur max, signe, décimales) et de la métrique de police du widget.
	Cela permet d'éviter les widgets trop larges et de garantir que toutes les valeurs restent visibles sans troncature.

	:param spin: Spinbox à ajuster.
	"""
	# ---- estimation du nombre de caractères ----
	min_val, max_val = spin.minimum(), spin.maximum()
	max_abs = max(abs(min_val), abs(max_val))
	has_sign = min_val < 0
	char_count = max(1, len(str(int(max_abs))))
	if has_sign: char_count += 1
	if isinstance(spin, QDoubleSpinBox): char_count += 1 + spin.decimals()  # "." + décimales

	# ---- conversion caractères → pixels ----
	metrics = QFontMetrics(spin.font())
	# petite marge de confort (boutons up/down, padding) "−" est en général le caractère le plus long en cas de police non uniforme.
	width_px = char_count * metrics.horizontalAdvance("−") + 50
	spin.setFixedWidth(width_px)


# ==================================================
# endregion UI Build
# ==================================================

# ==================================================
# region Callbacks
# ==================================================
##################################################
def sync_button_group(target: QButtonGroup, value: int):
	"""
	Synchronise un groupe de boutons exclusif avec un autre via son id.

	On bloque les signaux le temps de la mise à jour pour éviter les appels en série.

	Exemple d'utilisation ::

	    group_1.idClicked.connect(lambda v: sync_button_group(group_2, v))
	    group_2.idClicked.connect(lambda v: sync_button_group(group_1, v))

	:param target: QButtonGroup à mettre à jour.
	:param value: Identifiant du boutton à sélectionner.
	"""
	target.blockSignals(True)
	button = target.button(value)
	if button is not None: button.setChecked(True)
	target.blockSignals(False)


##################################################
def sync_spin(target: QDoubleSpinBox | QSpinBox, value: float | int):
	"""
	Synchronise une spinbox avec la valeur envoyée (par signal).

	On bloque les signaux le temps de la mise à jour pour éviter les appels en série.

	Exemple d'utilisation ::

	    spin_1.valueChanged.connect(lambda v: sync_spin(spin_2, v))
	    spin_2.valueChanged.connect(lambda v: sync_spin(spin_1, v))

	:param target: Spinbox à mettre à jour.
	:param value: Valeur à insérer.
	"""
	target.blockSignals(True)
	target.setValue(value)
	target.blockSignals(False)


##################################################
def update_spin_limits(spin: QDoubleSpinBox | QSpinBox, minimum: float | int | None = None, maximum: float | int | None = None, ):
	"""
	Mets à jour dynamiquement les bornes d'une spinbox.

	Les bornes non spécifiées conservent leur valeur actuelle.

	.. note:: Qt ajuste automatiquement la valeur courante si elle sort du nouvel intervalle.

	:param spin: Spinbox cible.
	:param minimum: Nouvelle borne minimale (optionnelle).
	:param maximum: Nouvelle borne maximale (optionnelle).
	"""
	spin.setRange(spin.minimum() if minimum is None else minimum, spin.maximum() if maximum is None else maximum)


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

	:param msg: Message à afficher
	"""
	print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)


##################################################
def print_warning(msg: str):
	"""
	Affiche un message avec une couleur jaune

	:param msg: Message à afficher
	"""
	print(Fore.YELLOW + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)


##################################################
def print_success(msg: str):
	"""
	Affiche un message avec une couleur verte

	:param msg: Message à afficher
	"""
	print(Fore.GREEN + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)


##################################################
def format_time(seconds):
	"""
	Fonction pour formater le temps en secondes en HH:MM:SS.

	:param seconds: Temps en secondes
	:return: Chaine de caractère représentant le temps au format HH:MM:SS.
	"""
	hours = int(seconds // 3600)
	minutes = int((seconds % 3600) // 60)
	seconds = int(seconds % 60)
	return f"{hours:02}:{minutes:02}:{seconds:02}"
# ==================================================
# endregion Prints
# ==================================================
