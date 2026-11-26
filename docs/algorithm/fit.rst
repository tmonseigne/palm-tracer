Ajustement de la localisation
=============================

.. _fit_page:

L':term:`ajustement gaussien <Ajustement gaussien>` affine la position latérale d'un émetteur en ajustant un modèle de :term:`PSF <PSF (Point Spread Function)>`
aux intensités brutes des pixels autour de la détection. La segmentation fournit la position initiale. Le centre du modèle ajusté donne les coordonnées subpixel.

Modèle de la tache
------------------

Le modèle comporte un fond constant :math:`b`, une amplitude :math:`A` et un centre :math:`(x_0,y_0)`. En posant
:math:`\Delta x=x-x_0` et :math:`\Delta y=y-y_0`, les coordonnées :math:`u,v` le long des axes du modèle sont

.. math::

   u=\Delta x\cos\theta-\Delta y\sin\theta,\qquad
   v=\Delta x\sin\theta+\Delta y\cos\theta.

L'intensité prédite au pixel :math:`(x,y)` vaut

.. math::

   \widehat I(x,y)=b+A\exp\left[-\frac12
      \left(\frac{u^2}{\sigma_x^2}+\frac{v^2}{\sigma_y^2}\right)\right].

Les largeurs :math:`\sigma_x` et :math:`\sigma_y` sont des écarts-types en pixels selon les deux axes du modèle.
Lorsque les largeurs sont égales, la tache est circulaire et l'angle est indéterminé.

Paramètres ajustés
------------------

Les quatre modes ajustent le fond, l'amplitude et le centre. Ils diffèrent par les paramètres de forme laissés libres.

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Mode
     - Forme de la PSF
   * - :guilabel:`X, Y`
     - Une largeur commune fixée par :guilabel:`σ`.
   * - :guilabel:`X, Y, Sigma`
     - Une largeur commune ajustée.
   * - :guilabel:`X, Y, SigmaX, SigmaY`
     - Deux largeurs ajustées avec l'angle fixé par :guilabel:`θ`.
   * - :guilabel:`X, Y, SigmaX, SigmaY, Theta`
     - Deux largeurs et un angle ajustés.

Le calcul de Z par :ref:`astigmatisme <astig_page>` utilise les deux modes à largeurs indépendantes.

Optimisation sur la fenêtre
---------------------------

#. Le cœur CPU extrait une fenêtre carrée autour de la détection. Pour un :guilabel:`ROI Radius` de :math:`r` pixels, son côté mesure :math:`2r + 1` pixels.
   Le minimum de la fenêtre initialise le fond, et l'écart entre son maximum et son minimum initialise l'amplitude.
#. Le solveur minimise la somme des carrés des résidus sur les pixels de la fenêtre. Pour les paramètres :math:`\boldsymbol p` du modèle, le coût vaut

   .. math::

      E(\boldsymbol p)=\sum_{i\in\mathrm{ROI}} \bigl[I_i-\widehat I_i(\boldsymbol p)\bigr]^2.

#. À chaque itération, Levenberg–Marquardt propose un pas à partir des dérivées du modèle. Le candidat est ramené dans les bornes des paramètres,
   notamment à un pixel du centre initial sur chaque axe. Le solveur accepte ou rejette le pas selon la réduction du coût et adapte l'amortissement.
   Il s'arrête lorsque le pas, le gradient ou le résidu devient suffisamment faible, ou lorsque le budget d'itérations est atteint.

Résultats et qualité
--------------------

Les colonnes ``X`` et ``Y`` donnent le centre en pixels. ``Sigma X`` et ``Sigma Y`` donnent les largeurs ajustées ou imposées, et ``Theta`` donne l'angle en radians.
La colonne ``Integrated Intensity`` contient l'intégrale du profil gaussien sans le fond, calculée par :math:`2\pi A\sigma_x\sigma_y`.

La colonne historique ``MSE XY`` contient le carré de la corrélation de Pearson entre les intensités observées et prédites sur la fenêtre.
Une valeur proche de 1 indique une forte concordance de forme. Un ajustement invalide, par exemple lorsque la fenêtre déborde de l'image,
est repérable par une valeur ``Integrated Intensity`` de −1.
