"""
Quelques fonctions de dessin utiles

Ce module contient des fonctions pour la génération de graphiques interactifs avec Plotly,
notamment pour gérer des palettes de couleurs et ajouter des éléments visuels représentant
des données de tests.

**Structure** :

1. **`get_color_map_by_name`**

   - Génère un dictionnaire associant des noms à des couleurs à partir d'une palette spécifiée.
   - Prend en charge la répétition cyclique des couleurs si la palette est insuffisante.

2. **`draw_test_section`**

   - Ajoute des éléments visuels à un graphique Plotly pour représenter les périodes associées à des tests.
   - Comprend des zones colorées semi-transparentes et des lignes verticales pour marquer les événements.

"""

import plotly.express as px  # Pour accéder aux couleurs qualitatives
import plotly.graph_objects as go


##################################################
def get_color_map_by_name(names: list[str], palette: list[str] = px.colors.qualitative.Plotly) -> dict[str, str]:
	"""
	Génère un dictionnaire associant chaque nom de fichier à une couleur unique.

	Cette fonction prend une liste de noms de fichiers et associe une couleur de la palette spécifiée à chaque nom de fichier.
	Si le nombre de fichiers dépasse le nombre de couleurs disponibles dans la palette, elle réutilise les couleurs de manière cyclique.

	:param names: Liste des noms des fichiers pour lesquels une couleur doit être attribuée.
	:param palette: Liste des couleurs à utiliser pour les fichiers. Si non spécifié, la palette `Plotly` est utilisée par défaut.
	:return: Un dictionnaire où les clés sont les noms de fichiers et les valeurs sont les couleurs attribuées.
	"""
	unique_names = set(names)  # Récupérer les noms uniques
	color_map = {}  # Dictionnaire pour associer chaque fichier à une couleur
	# Associer une couleur unique à chaque fichier
	color_index = 0
	for name in unique_names:
		color_map[name] = palette[color_index % len(palette)]
		color_index += 1  # Passer à la couleur suivante

	return color_map


##################################################
def draw_test_section(fig: go.Figure, y_range: list, tests: list[dict], color_map: dict, last_time: float, row: int):
	"""
	Ajoute des barres verticales et des zones colorées pour chaque test dans un graphique Plotly.

	Cette fonction ajoute des zones colorées en fonction des timestamps des tests et leur fichier associé,
	ainsi que des lignes verticales pour marquer chaque test. Elle est utilisée pour représenter graphiquement
	les périodes d'exécution de chaque test dans le temps.

	:param fig: L'objet figure de Plotly dans lequel les éléments (barres et lignes) seront ajoutés.

	:param y_range: La plage des valeurs sur l'axe Y pour la section du graphique où les zones colorées seront tracées.
			La plage est définie par deux valeurs [y_min, y_max].

	:param tests: Une liste de dictionnaires représentant les tests effectués. Chaque dictionnaire doit contenir les clés :
			- "Timestamp" (float) : Le timestamp du test.
			- "File" (str) : Le nom du fichier associé au test.
			- "Test" (str) : Le nom du test effectué.

	:param color_map: Un dictionnaire associant chaque fichier de test à une couleur. Le fichier est utilisé comme clé et la couleur
			(en format HTML) comme valeur.

	:param last_time: Le dernier timestamp enregistré, utilisé pour déterminer la fin de la zone colorée pour le dernier test.

	:param row: L'index de la ligne dans la figure Plotly (utile lorsque plusieurs sous-graphiques sont utilisés) pour ajouter
			les éléments (barres verticales et zones colorées) dans la section correspondante.

	:return: Cette fonction modifie l'objet `fig` en ajoutant des traces et des formes, mais ne retourne rien.
	"""

	# Ajouter les barres verticales pour chaque test et des zones colorées en fonction du fichier
	for i, test in enumerate(tests):
		# Récupérer les informations du test et la couleur associée au fichier
		t, f, n = test["Timestamp"], test["File"], test["Test"]
		text = f"{f} - {n}"
		color = color_map[f]

		# Déterminer la plage pour la zone colorée
		# Si ce n'est pas le dernier test, la fin de la zone est le timestamp du test suivant sinon le dernier timestamp
		if i < len(tests) - 1: next_timestamp = tests[i + 1]["Timestamp"]
		else: next_timestamp = last_time

		# Ajouter une zone colorée
		fig.add_shape(type="rect", x0=t, x1=next_timestamp, y0=y_range[0], y1=y_range[1],
					  fillcolor=color, opacity=0.2, line=dict(width=0), row=row, col=1)
		# Ajouter une ligne verticale pointillée
		fig.add_trace(go.Scatter(x=[t, t], y=y_range, mode="lines", line=dict(color=color, width=0.5, dash="dash"),
								 name=text, hoverinfo="text", text=text), row=row, col=1)
