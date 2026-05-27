Pipeline des traitements
==============================

.. _pipeline_page:

.. role:: python(code)
   :language: python

.. role:: console(code)
   :language: console

Récupération des données, localisation, suivi, calculs sur les trajectoires, visualisation haute résolution, visualisation de graphiques et génération de galeries sont les étapes principales du pipeline de traitement de PALM.
Ces étapes sont lancées dans la méthode :py:meth:`~PALMTracer.process` selon les paramètres de l'interface.

Étape 1 : Récupération des piles
--------------------------------

Selon le batch défini dans les paramètres de l'interface. Les piles sont chargées en mémoire pour être traitées.

Il y a plusieurs possibilités :

- Une seule pile est chargée, dans ce cas-là, le mode importe peu.
- Plusieurs piles sont chargées, dans ce cas-là, le mode influe :
   - **Only one** : seule la pile sélectionnée est utilisée.
   - **Each File separately** : les piles sont utilisées les unes après les autres.
   - **All in One** : les piles sont concaténées en une seule.

Étape 2 : Sauvegarde des fichiers de paramètres et de métadonnées
-----------------------------------------------------------------

Dans le dossier de sortie - défini par le nom de la pile avec le suffixe :file:`_PALM_Tracer` (exemple: :file:`stack.tif` → :file:`stack_PALM_Tracer`) - sont sauvegardés :

- Un fichier de paramètres :file:`settings-<timestamp>.json` contenant les paramètres utilisés pour le traitement.
- Un fichier de métadonnées :file:`meta-<timestamp>.csv` contenant les métadonnées de la pile (dimensions, calibration, etc.).
- Un fichier de log :file:`log-<timestamp>.log` contenant les logs du traitement.


Étape 3 : Localisation
----------------------

La localisation est lancée selon les paramètres de l'interface. Si elle est désactivée, des localisations précalculées et non filtrées peuvent être chargées à condition qu'elle soit présente dans le dossier de sortie.

Si des filtres sont sélectionnés, ils sont appliqués aux localisations pour ne garder que les localisations répondant aux critères définis.
Si l'option :console:`save filtered` est sélectionné, la localisation filtrée est sauvegardée dans un fichier :file:`localizations_filtered-<timestamp>.csv`.

.. note:: Si la localisation est désactivée et qu'aucune localisation précalculée n'est présente dans le dossier de sortie, la localisation est considérée comme vide et les étapes suivantes sont lancées avec des localisations vides.
.. note:: Le chargement d'une localisation précalculée s'effectue toujours sur la version non filtrée la plus récente.

Étape 4 : Suivi des molécules (tracking)
-----------------------------------------

Le suivi est lancé selon les paramètres de l'interface. S'il est désactivé, un suivi précalculé et non filtré peut être chargé à condition qu'il soit présent dans le dossier de sortie.
Le suivi utilise en entrée la version filtrée des localisations précédentes (calculées ou chargées).
S'il n'y a pas de version filtrée ou si les filtres ont éliminé l'intégralité des localisations, la version non filtrée est utilisée.

Si des filtres sont sélectionnés, ils sont appliqués au suivi pour ne garder que les trajectoires répondant aux critères définis.
Si l'option :console:`save filtered` est sélectionné, le suivi filtré est sauvegardé dans un fichier :file:`tracking_filtered-<timestamp>.csv`.

Reconnexion des trajectoires
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Si l'option de reconnexion est activée, les trajectoires sont reconnectées pour tenter de reconstruire des trajectoires plus longues.
Les trajectoires reconnectées sont sauvegardées dans un fichier :file:`tracking-reconnected-<timestamp>.csv`. Il utilise en entrée la version non filtrée du suivi.

Si des filtres sont sélectionnés, ils sont appliqués au suivi pour ne garder que les trajectoires répondant aux critères définis.
Si l'option :console:`save filtered` est sélectionné, le suivi reconnecté et filtré est sauvegardé dans un fichier :file:`tracking_filtered_reconnected-<timestamp>.csv`.

.. note:: Si le suivi est désactivé et qu'aucun suivi précalculé n'est présent dans le dossier de sortie, le suivi est considéré comme vide et les étapes suivantes sont lancées avec un suivi vide.
.. note:: Le chargement d'un suivi précalculé s'effectue toujours sur la version non filtrée la plus récente et reconnectée si elle existe.


Étape 5 : Calculs sur les trajectoires
--------------------------------------

Des calculs peuvent être effectués sur les trajectoires pour en extraire des informations (MSD, diffusion instantanée, ajustement vers un modèle).
Ces calculs sont lancés selon les paramètres de l'interface.

Les calculs utilisent en entrée la version filtrée et reconnectée du suivi précédent (calculée ou chargée).
S'il n'y a pas de version filtrée ou reconnectée ou si les filtres ont éliminé l'intégralité des trajectoires, la version non filtrée est utilisée.

Si des filtres sont sélectionnés, ils sont appliqués au suivi pour ne garder que les trajectoires répondant aux critères définis.
Si l'option :console:`save filtered` est sélectionné, les calculs reconnectés et filtrés sont sauvegardés dans trois fichiers :
:file:`tracking_MSD_filtered-<timestamp>.csv`, :file:`tracking_InstantD_filtered-<timestamp>.csv`, :file:`tracking_Fit_filtered-<timestamp>.csv`.

.. note:: Si les calculs sont désactivés, les étapes suivantes seront capables de calculer les éléments nécessaires rapidement.

.. warning:: Les trajectoires éliminées sont également éliminées dans le tableau de suivi original et le fichier :file:`tracking_filtered-<timestamp>.csv` est réécrit.

Étape 6 : Visualisations
-------------------------

La partie visualisation comprend la génération d'une galerie de ROI de localisations ainsi que les visualisations de haute résolution et de graphiques.
Ce sont des générations automatiques avec de simples paramètres de base (exemple : nombre de ROI, taille des ROI, etc.) pour une première exploration rapide des données notamment lors de Batch important.
L'utilisation des visionneuses dédiées est recommandée pour une exploration plus approfondie et personnalisée des données.
