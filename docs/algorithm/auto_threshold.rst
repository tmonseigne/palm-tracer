Seuillage automatique
=====================

.. function:: auto_threshold(image: np.ndarray, roi_size: int = 7, max_iterations: int = 4) -> float

	Calcule un seuil automatique basé sur la segmentation de l'image en utilisant une bibliothèque DLL externe.

	Cette fonction applique une segmentation itérative à l'image en exploitant la méthode **PALM (Point Accumulation for Localized Mean)**.
	L'objectif est d'affiner progressivement un seuil basé sur l'écart type des pixels non segmentés.

	:param image: Image en niveaux de gris sous forme de tableau NumPy 2D.
	:type image: np.array
	:param roi_size: Taille des régions d'intérêt (ROI) utilisées pour la segmentation. Défaut : 7.
	:type roi_size: int
	:param max_iterations: Nombre maximal d'itérations pour l'affinement du seuil. Défaut : 4.
	:type max_iterations: int

	:return: Seuil calculé après convergence (écart type des pixels non segmentés).
	:rtype: float


Algorithme
----------

L'algorithme fonctionne en plusieurs étapes :

1. **Initialisation :**

	- Création d'un masque vide (même taille que l'image, rempli de zéros).
	- Calcul de l'écart type initial de l'image (:math:`\sigma = \sqrt{\frac{1}{N} \sum_{i=1}^{N} (x_i - \bar{x})^2}`).
	- Définition de la demi-taille de la région d'intérêt (`roi_size`).

2. **Segmentation itérative :**

	- Lancement de la fonction PALM de la DLL pour détecter des points caractéristiques avec les paramètres suivants :
		- Le seuil est égal à l'écart-type calculé.
		- Le watershed est désactivé.
		- Le fit Gaussien est désactivé.
		- Sigma vaut 1.
		- Theta vaut :math:`\pi / 4`.
	- Mise à jour du masque en activant les pixels correspondant aux régions détectées (ROI autour de chaque points détectés).
	- Recalcule de l'écart type sur les pixels *hors* segmentation.
	- Répétition jusqu'à `max_iterations` ou convergence.

3. **Critère d'arrêt :**

	- Si tous les pixels sont segmentés avant la fin des itérations, la boucle s'arrête prématurément.
	  Cela n'est possible que si les points détectés et leur zone d'intérêt couvrent l'intégralité de l'image.


Exemple d'utilisation
---------------------

Voici un exemple d'utilisation de la fonction :

.. code-block:: python

	import ctypes
	import numpy as np
	from palm_tracer.Processing import Palm

	# Utilisation de PALM et Chargement de la DLL
	palm = Palm()

	# Image factice 100x100 avec des valeurs aléatoires
	image = np.random.randint(0, 255, (100, 100), dtype=np.uint8)

	# Calcul du seuil
	seuil = palm.auto_threshold(image)

	print(f"Seuil calculé : {seuil}")


Remarques
---------

- L'utilisation de la DLL est essentielle au bon fonctionnement de cette fonction.
- La performance dépend de la taille de l'image et du nombre d'itérations.
- L'approche PALM permet une segmentation robuste sur des images bruitées.
