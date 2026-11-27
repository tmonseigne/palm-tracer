Seuillage automatique
=====================

.. _auto_threshold_page:

Dans :guilabel:`Localization`, :guilabel:`Auto Threshold` estime un :term:`seuil <Seuil (Threshold)>` sur le plan affiché
et renseigne le champ :guilabel:`Threshold`. L'algorithme estime les fluctuations du fond à partir des intensités brutes
en écartant les voisinages des émetteurs détectés. Le seuil ainsi obtenu s'applique aux coefficients d'ondelettes.

Initialisation
--------------

Soit :math:`I(p)` l'intensité brute du pixel :math:`p`. Pour un ensemble non vide :math:`B` de pixels,
la moyenne :math:`\mu_B` et l'écart-type :math:`\sigma_B` sont

.. math::

   \mu_B = \frac{1}{|B|}\sum_{p \in B} I(p),
   \qquad
   \sigma_B = \sqrt{\frac{1}{|B|}\sum_{p \in B}\bigl(I(p)-\mu_B\bigr)^2}.

Au départ, :math:`B` contient tous les pixels du plan. L'écart-type :math:`\sigma_B` donne le premier seuil :math:`T_0`.

Détection et estimation du fond
-------------------------------

#. **Détecter avec le seuil courant.** La décomposition en ondelettes à trous lisse le plan à plusieurs échelles sans rééchantillonnage.
   Le deuxième plan de détail est la différence entre les deux premières approximations lissées. Le détecteur segmente les pixels
   dont le coefficient dans ce plan est strictement supérieur à :math:`T_k`. Le cœur CPU autorise la fusion des bassins du watershed
   et utilise les positions issues de la segmentation, sans ajustement de :term:`PSF <PSF (Point Spread Function)>`.
#. **Reconstruire le masque.** À chaque itération, le masque est remis à zéro. Pour chaque détection, on marque les pixels d'une
   fenêtre carrée centrée sur sa position et rognée aux bords de l'image. Le réglage :guilabel:`ROI Radius` donne le nombre de
   pixels de chaque côté du pixel central. Le masque est l'union de ces fenêtres.
#. **Réestimer le seuil.** On prend pour :math:`B` les pixels hors masque. On recalcule :math:`\sigma_B`
   à partir de leurs intensités brutes et on l'utilise comme seuil de l'itération suivante.

Par exemple, pour quatre intensités de 98, 100, 102 et 150 :term:`ADU <ADU (Analog-to-Digital Unit)>`, l'écart-type initial
vaut environ 21,70 ADU. Si le masque exclut la valeur 150, le recalcul sur les trois autres valeurs donne environ 1,63 ADU.

Critères d'arrêt
----------------

Le cœur CPU effectue au plus cinq itérations. Il s'arrête et conserve le seuil courant si le masque couvre tout le plan
ou si le nouveau seuil est pratiquement égal au précédent.
Si la limite d'itérations est atteinte, il renvoie le dernier seuil mis à jour.

Le résultat fournit un point de départ pour la détection. Vérifiez-le avec l'aperçu sur plusieurs plans représentatifs,
en particulier si le fond ou la densité d'émetteurs varie au cours de l'acquisition.

Exemple en Python
-----------------

:py:meth:`~palm_tracer.Processing.Palm.Palm.auto_threshold` reçoit une image 2D et un tableau de paramètres.
Le premier élément du tableau donne la taille de la fenêtre en pixels.

.. code-block:: python

   import numpy as np

   from palm_tracer.Processing import Palm
   from palm_tracer.Tools.FileIO import open_tif

   stack = open_tif("stack.tif")
   fit_params = np.array([7.0], dtype=np.float64)
   threshold = Palm().auto_threshold(stack[0], fit_params)
   print(threshold)
