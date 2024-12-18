Cahier des charges PALM Tracer Python
=====================================

.. role:: python(code)
   :language: python

.. role:: console(code)
   :language: console

Description
-----------

Le but du projet est de transposer `PALM Tracer <https://www.iins.u-bordeaux.fr/projectSIBARITA70>`_ présent en tant que plugin de
`Metamorph <https://fr.moleculardevices.com/products/cellular-imaging-systems/high-content-analysis/metamorph-microscopy>`_.

Il a été développé en C++ et sera transposé vers un environnement Python.
La transposition sera “intelligente”, c’est-à-dire qu’elle ne se limitera pas à un simple copié collé du plugin existant.

Une étude devra être effectuée afin de définir les éléments nécessaires à cette nouvelle version ainsi que les modifications nécessaires aux anciennes fonctionnalités.

Le projet se fera sous la `licence publique générale GNU 3.0 <http://www.gnu.org/licenses/gpl-3.0.txt>`_ *(modifiable en fonction des limitations de brevets)*

Spécifications techniques
-------------------------

L’environnement de développement sera Python avec la bibliothèque `Napari <https://napari.org/stable/>`_ pour l’interface.
Durant la première phase, la majeure partie des fonctions sera intégrée par des DLL C++ déjà utilisés dans le plugin d’origine.
Une étude sera menée afin de vérifier les performances de cette méthode comparée à un process entièrement en python.
Le développement pourrait contenir 4 étapes principales :

1. Proposer l’ensemble des traitements hors ligne de PALM Tracer pour un usage interne.
   En parallèle, de nouveaux traitements hors ligne seront ajoutés.
2. Un déploiement externe pourra être envisagé à la fin ou au cours de la première étape, les spécifications Napari (en cas de déploiement officiel) et les limites de licences seront à prévoir.
3. Une seconde étape consistera à ajouter divers traitements en ligne (pseudo temps réel).
4. Une troisième étape consistera à intégrer un module d’acquisition afin de remplacer entièrement le programme Metamorph.

Le versionnage se fera sous Git avec **GitHub** et l’intégration continue avec **GitHub Action**.
Des fichiers exemple seront ajoutés au dépôt afin de pouvoir tester les différents traitements et permettre un exemple d’utilisation aux nouveaux utilisateurs.


Besoins et fonctionnalités
--------------------------

`État d'avancement des fonctionnalités <https://docs.google.com/spreadsheets/d/e/2PACX-1vSPxOeVrw6X-nY-u93qMAqFKf2eiyFgSI_tAKIc-BzaVCgvwG-fmkywWFDKAapWqiZsdv2gkcm3VLne/pubhtml?gid=0&single=true>`_

Management
^^^^^^^^^^

- Versionning *(la taille et la décomposition du projet nécessitent un versionnage propre)*
- Intégration continue *(l’intégration continue permettra de vérifier la bonne santé du projet)*
- Tests unitaires
- Tests d’intégration
- Génération de la documentation (code et manuel)
- Fichier de langue *(secondaire, mais proposition d’une interface multilingue)*
- Permettre de facilement ajouter une langue pour la communauté.
- Fichier de paramètres (settings) chargé automatiquement (ou créé si inexistant) (certaines options pourront ainsi être préremplies en fonction de l’utilisateur)
- Définir si le fichier est enregistré au fur et à mesure des changements ou à la fermeture

Base
^^^^^

- Lecture/écriture de fichiers datas :
- Streaming Metaseries Format (:console:`.smf`) (In/Out)
- MetaMorph Stack File (:console:`.stk`) (In/Out)
- MetaSeries Single/Multi-plane TIFF (:console:`.tif`) (In/Out)
- Portable Network Graphics (:console:`.png`) (Out)
- Lecture/écriture de fichiers pipeline : *(à moins d’un format spécifique largement répandu, JSON)*
- Prévoir un outil de conversion pipeline PALM Tracer metamorph -> PALM Tracer Python
- Lecture écriture de fichiers de pre-processing : *(CSV plus simple pour des analyses futures. l’entête actuel pourra être enregistré à part)*
- Prévoir un outil de conversion de fichiers de localisation PALM Tracer metamorph -> PALM Tracer Python *(il s’agit juste de supprimer l’entête et d’en faire un CSV)*
- Outil de Génération de données simulées (`Sample Maker <https://github.com/tmonseigne/Sample-Maker>`_) *(pour les tests de base, mais aussi pour des éléments plus complexes)*
- Optimisation des algorithmes *(attention aux MAJ des bibliothèques)*
- Vérifier la performance DLL C++ (date : ≈2010) et code Python.
- Vérifier l’interfaçage sur python pour multithreading et portage GPU.
- Mode Bash pour traitement par lot (pour lancer un pipeline sur un dossier avec ou sans sous-dossiers)
- Possibilité de lancer en ligne de commande ou plus simplement pour néophyte une option traitement par lots dans l’interface
- Génération de fichiers automatique (ou non par le biais d’une option) lors de l’exécution d’un pipeline
  (copie du pipeline, fichier texte avec la configuration matérielle, temps d’exécution, ressources utilisées, nombre de molécules trouvées…)
- Possibilité de Cut un fichier (prendre des frames N à N).
  *Il est possible que lors de l’acquisition il y ait eu un problème sur certains frames et donc les éliminer de l’analyse.*

Visualisation (dépendant des limitations de Napari)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Drag and Drop d’une image *(basique, mais pas si évident suivent les GUIS)*
- Affichage de l’image avec le pourcentage de zoom
- Affichage d’un histogramme shrinkable
- Proposition d’avoir une checkbox pour auto shrink les images (valeur par défaut 0.5% de l’histogramme « blanc » à l’air cohérent avec les images passées en exemple, mais paramètre modifiable)
- Affichage d’un choix de Look-Up Table Monochrome, Pseudo Color, Gold, Personnalisable (les autres sont-elles nécessaires ou surcharge ?)
- Option de Seuillage
- Option de changement d’échantillonnage.
- Play/pause des différents frames

Processing
^^^^^^^^^^

- Options d’acquisition (pixel size, exposition…)
- 2D/3D Localisation
	- Preview 2D Localisation
	- GPU portage (on/off) *pourquoi demander ? si possible GPU*
	- Auto seuil et spin pour rerégler
	- Taille des ROIs
	- Watershed (On/Off)
	- Gaussian fit (définir les options, qui fait quoi un chapitre dans la doc pourra être dédié)
	- Options pour la 3D ?
- Tracking
	- Distance max (unité à définir correctement on parle en pixel, µm ou autre ?)
	- Distance minimum (définir clairement que l’on parle de nombre de frames si une molécule est trouvée sur moins de frames que le minimum est-elle juste supprimé du tracking ? Dans ce cas, la longueur minimale serait plus au moment de la génération de l’image HR pour conserver un max d’infos au moment du pre-processing)
	- Drift Correction
- *Débruitage avec réseau de neurones (Méthode d’Abdel)*
- *ROI Map (Demande de Laetitia sur le test d’Abdel)*

Filtrage
^^^^^^^^^^

High Resolution Processing
^^^^^^^^^^^^^^^^^^^^^^^^^^

- Localisation
- Indiquer si des fichiers de localisations sont trouvés ou rendre l’onglet inactif tant que pas de dossiers
- Option de Drift si pré-process effectué
- Options de filtrage
- Niveau de zoom (limité à des puissances de 2 ? ça l’air d’être le cas, mais caché)
- Channel utilisé (intensité lumineuse ou autre)
- Tracking
- Indiquer si des fichiers de tracking sont trouvés ou rendre l’onglet inactif tant que pas de dossiers
- Option de Drift si pré-process effectué
- Option de filtrage
- Niveau de zoom
- Channel utilisé (trace, vitesse ou autre)

Sorties
^^^^^^^

Au cours des prétraitements et générations d’images HR. Un sous-dossier sera créé avec ce schéma :

.. code-block:: console

	Mon_fichier.tif
	Mon_fichier_PALM_Tracer
		|-Meta_Timestamp.txt
		|-Localisation_Timestamp.csv
		|-Tracking_Timestamp.csv
		|-Drift_Timestamp.csv
		|-Mon_fichier_Localisation_Timestamp.png
		|-Mon_fichier_Tracking_Timestamp.png
		|-Pipeline_Timestamp.json
		|-log_Timestamp.log

- **Meta** : Fichier contenant les entêtes des fichiers précédents
  (Width, Height, nb_Planes, Pixel_Size(um), Frame_Duration(s)) avec d’autres éléments comme la date, la configuration matérielle, les éléments d’acquisitions (pixel size, exposition…), la version de PALM Tracer.
- **Localisation**, Tracking, Drift tableaux de coordonnées
- **Fichiers Images** : Format différent possible si c'est plus conventionnel, l'enregistrement se fait automatiquement à la fin de chaque processing.
- **Pipeline** : Fichier mis à jour continuellement en fonction des process effectués, il contient 4 parties (Général, Processing, Localisation, Tracking, Filtering)
  avec les dernières options utilisées pour cela et la date du dernier lancement. Il permettra de garder une trace et d’être chargé comme pipeline de Batch.
- **Log** : Log (temps, ressources, n molécules...)

Protocole de test
-----------------

**Données simulées** : Le protocole pour générer un jeu de données sera similaire à la thèse d’adel (Kechkar, 2013) :

- Image simulée contrôlée
- Image motif bande / carré / soleil 3D
- À définir, mais une image contenant un ensemble de problèmes connu serait envisageable également
- Une gamme de variants selon la densité de particules et le SNR
- À définir, mais densités possible 0.1, 0.25, 0.5, 0.75, 1 molécules/μm²
- À définir, mais SNR possible 2, 4, 6, 8, 10
- Donc 25 (5x5) combinaisons de la même image simulée

**Rapport** : Un rapport sera généré lors de l’exécution d’un pipeline de test et directement intégré à la doc en ligne générée automatiquement.
On recueillera les informations suivantes :

- Configuration matérielle
- Fichier en entrée
- Définition des variants (densité, SNR, méthodes)
- Précision (accuracy) de la localisation
- Matrice de confusion simplifiée : Nombre de molécules, faux positifs et faux négatifs
- Temps d’exécution total et détaillé
- Mémoire max utilisé
- Nombre de cœur max utilisé

**Process différents** : En cas de process différents pour un résultat similaire, un schéma comparatif des 2 méthodes sera généré. Un outil pourrait être dédié à la génération de graphiques et rapport avec plusieurs rapports en entrée.

Documentation
-------------

La documentation sera répartie en plusieurs parties générées dynamiquement ou statiquement selon les cas.
Les différentes parties seront :

1. Présentation (readme ou autre)
2. Guide d'utilisation qui devra être rédigé depuis le début du process (installation et Utilisation).
   C’est-à-dire que l’installation de python devra également être indiquée pour pallier les différences de niveau en informatique de l’utilisateur.
3. Licence
4. Documentation du code (API)
5. Quelques pages sur différents processus complexes expliqués
6. Résultats des tests de l’intégration continue. Une partie pourra être statique avec les tests sur différentes machines et leurs configurations respectives l’autre sera dépendante du CI et donc les spécifications du CI devront être reportées.


Glossaire
---------

- **Environnement de développement** : L’environnement de développement, dans ce cas, correspond aux langages, bibliothèques et systèmes d’exploitation utilisés.
- **Langage de programmation** : Un langage de programmation est le moyen d’écrire du code source avant qu’il ne soit analysé par la machine.
- **Bibliothèque** : En développement informatique, une bibliothèque est un ensemble de fonctions (code) déjà développé pouvant être réutilisé.
- **DLL (bibliothèque de liens dynamiques)** : Ensemble de fonctions (code) enregistré en langage machine préchargé au lancement du programme. Le code source n’est pas forcément disponible.
- **Calcul hors ligne** : Calcul prenant un certain temps à être effectué (ce n’est donc pas instantané).
- **Calcul en ligne** : Calcul étant effectué en pseudo temps réel presque instantanément et sans temps d’attente pour l’utilisateur.
- **Versionning** : Le versionning permet de conserver en mémoire toutes les modifications apportées aux fichiers afin de garder une trace et permettre de passer facilement d’une version à l’autre
- **Intégration continue (CI)** : L’Intégration continue (Continuous Integration) est un une routine automatique qui se lance pour vérifier que le code marche toujours. Cela peut être juste : compiler un programme, le lancer ou voir si le programme est bien propre, le compiler, le lancer avec des tests, analyser le code, la gestion de la mémoire… Cela peut être lancé à chaque mise à jour ou tous les jours, semaines… ou à la demande.
- **ROI (Region Of Interest)** : Zone d’intérêt sélection permettant de récupérer un ensemble de pixels autour d’un point donné.
