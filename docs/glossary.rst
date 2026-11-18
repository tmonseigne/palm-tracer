Glossaire
=========

Les termes sont regroupés par thème et triés par ordre alphabétique dans chaque rubrique.

Acquisition et étalonnage
-------------------------

.. glossary::
   :sorted:

   ADU (Analog-to-Digital Unit)
      Unité des valeurs numériques enregistrées par la caméra. La conversion des intensités en photons utilise un facteur d'étalonnage exprimé en photons par ADU. Selon la caméra et le prétraitement, il faut aussi tenir compte du niveau de référence électronique.

   Calibration spatiale et temporelle
      Conversion des distances et des durées en unités physiques. La taille du pixel dans le plan de l'échantillon donne l'échelle latérale. Pour le suivi, le temps écoulé entre images fixe l'échelle temporelle, tandis que le temps d'exposition décrit la durée d'intégration du signal. Ces deux durées peuvent différer.

   Pile d'images
      Séquence ordonnée d'images à traiter ensemble. Dans une acquisition de suivi, le premier axe représente le temps. Dans une pile de calibration axiale, il représente une suite de positions en profondeur. La convention d'axes est décrite dans :doc:`algorithm/arrays_indices`.

   Plan (frame)
      Image individuelle d'une :term:`pile d'images <Pile d'images>`. Dans un suivi, la colonne ``Plane`` repère le plan d'acquisition. Dans une pile axiale, la conversion du numéro de plan en position Z demande de connaître le pas et le sens de déplacement.

   PALM (Photoactivated Localization Microscopy)
      Technique de :term:`SMLM (Single-Molecule Localization Microscopy)` dans laquelle l'activation contrôlée de fluorophores photoactivables permet d'observer des sous-ensembles clairsemés de molécules à chaque image. Les positions estimées sur une série d'images alimentent la reconstruction.

   SMLM (Single-Molecule Localization Microscopy)
      Famille de techniques de microscopie dans lesquelles les émetteurs fluorescents sont détectés individuellement, généralement sur une série d'images où seule une fraction d'entre eux est observable à la fois. L'accumulation des positions estimées permet de reconstruire des structures plus fines que celles discernables sur une image brute.

Détection et localisation
-------------------------

.. glossary::
   :sorted:

   Ajustement gaussien
      Ajustement d'un modèle gaussien à l'image locale d'un émetteur. En 2D, le modèle peut fournir le centre, l'amplitude, le fond, ainsi que les largeurs et l'orientation de la tache. En 3D par astigmatisme, la position axiale est déduite des largeurs de la tache projetée à l'aide d'une calibration.

   Astigmatisme 3D
      Méthode de localisation axiale qui exploite la variation des largeurs de la :term:`PSF (Point Spread Function)` selon deux directions du plan image. Une calibration sur des positions Z connues permet d'estimer Z à partir des largeurs mesurées. Le sens de l'axe et la plage effectivement calibrée déterminent l'interprétation du résultat. Voir :ref:`outil de calibration de l'astigmatisme <tool_astig_page>`.

   Détection
      Repérage des candidats émetteurs dans chaque image. Une détection fournit une position initiale autour de laquelle une fenêtre peut être extraite pour affiner la position. Le choix du seuil influe sur le compromis entre faux positifs et émetteurs manqués.

   Fond et bruit
      Le fond est la contribution moyenne au signal mesuré autour de l'émetteur, due par exemple à la fluorescence hors foyer. Le bruit désigne les fluctuations de la mesure, notamment celles du comptage des photons et de la lecture de la caméra. Ces deux contributions influencent la détection et la précision de localisation.

   Localisation
      Position estimée d'un émetteur dans le plan :math:`(x, y)` et, si la méthode le permet, en profondeur :math:`z`. Le terme désigne aussi le calcul de cette position. Un ajustement dans une :term:`ROI (Region Of Interest)` peut fournir des coordonnées à une fraction de pixel.

   Précision de localisation
      Dispersion attendue des positions estimées pour un émetteur immobile sous des conditions comparables, généralement exprimée comme un écart-type par axe en nanomètres. Elle dépend notamment du nombre de photons, du fond et de l'échantillonnage. Le biais systématique et la résolution de l'image reconstruite sont des grandeurs distinctes.

   PSF (Point Spread Function)
      Fonction d'étalement du point. Elle décrit l'image produite par une source ponctuelle à travers le système optique. Sa forme, qui peut varier avec la mise au point, sert de base au modèle utilisé pour estimer la position de l'émetteur.

   ROI (Region Of Interest)
      Région d'intérêt sélectionnée dans l'image. Pour l'ajustement, PALM-Tracer extrait une fenêtre carrée autour de chaque détection, dont la taille est réglée par :guilabel:`ROI Size`. Dans l'aperçu, la forme du marqueur est un réglage d'affichage.

   Seuil (Threshold)
      Valeur utilisée par le détecteur pour retenir les candidats dont la réponse est suffisamment forte. Le seuil peut être réglé manuellement ou estimé à partir des pixels situés hors des régions détectées, selon le :ref:`seuillage automatique <auto_threshold_page>`.

   Sigma (largeur gaussienne)
      Écart-type :math:`\sigma` d'un profil gaussien, dans l'unité de ses coordonnées. Pour un axe donné, la largeur à mi-hauteur vaut :math:`2\sqrt{2\ln 2}\,\sigma \simeq 2{,}355\,\sigma`. Les colonnes ``Sigma X`` et ``Sigma Y`` décrivent les largeurs ajustées de la tache. Leur valeur décrit la forme du signal, tandis que la précision de localisation décrit l'incertitude sur le centre.

   SNR (Signal-to-Noise Ratio)
      Rapport signal sur bruit. Il compare une mesure du signal à une mesure du bruit. La définition exacte des deux termes du rapport doit être connue pour comparer des valeurs. Un rapport faible rend l'identification des candidats et l'estimation de leur position plus difficiles.

   Watershed
      Segmentation par ligne de partage des eaux qui découpe une image en régions à partir de son relief d'intensité. Dans PALM-Tracer, cette option aide à séparer des détections proches dont les signaux se recouvrent partiellement.

Suivi, mouvement et dérive
--------------------------

.. glossary::
   :sorted:

   Bille fiduciaire
      Particule fluorescente utilisée comme référence spatiale, supposée immobile par rapport à l'échantillon. Son déplacement apparent au fil de l'acquisition peut servir à estimer la :term:`dérive <Dérive>`. Suivre plusieurs billes réduit l'influence d'une mesure individuelle bruitée.

   Coefficient de diffusion
      Grandeur :math:`D` qui quantifie la vitesse d'étalement d'une population de particules par diffusion, généralement exprimée en :math:`\mu\mathrm{m}^2/\mathrm{s}`. Pour une diffusion brownienne libre isotrope dans :math:`d` dimensions, le modèle idéal donne :math:`\mathrm{MSD}(\tau) = 2dD\tau`. Le bruit de localisation et le flou pendant l'exposition peuvent modifier la courbe mesurée.

   Correction de dérive
      Estimation puis compensation du déplacement commun au champ d'observation. Pour le rendu haute résolution, PALM-Tracer estime la dérive latérale à partir de billes suivies et soustrait aux coordonnées XY le déplacement cumulé à chaque plan.

   Dérive
      Déplacement global apparent du champ d'observation au cours de l'acquisition, par exemple sous l'effet d'une instabilité mécanique ou thermique. Elle ajoute un déplacement commun aux particules et peut élargir des structures dans une reconstruction cumulée.

   Diffusion instantanée
      Estimation locale de la mobilité fondée sur des déplacements observés dans une fenêtre de la trajectoire. Le paramètre :guilabel:`Fit Length` règle la longueur de cette fenêtre dans l'analyse. Des fenêtres courtes rendent l'estimation plus sensible aux fluctuations des déplacements individuels.

   MSD (Mean Squared Displacement)
      Déplacement quadratique moyen pour un retard temporel :math:`\tau`. Il s'obtient en moyennant :math:`\lVert\mathbf r(t+\tau)-\mathbf r(t)\rVert^2` sur les paires de positions séparées par ce retard. Il s'exprime en unités de longueur au carré. Pour une trajectoire de durée finie, les grands retards disposent généralement de moins de paires.

   Reconnexion des trajectoires
      Association de deux segments séparés par des plans sans localisation, par exemple pendant un :term:`scintillement <Scintillement>`. Les réglages limitent la durée de la coupure et le déplacement admissible selon le modèle de mouvement choisi. Une reconnexion peut relier deux particules différentes lorsque plusieurs associations sont plausibles.

   Scintillement
      Alternance de périodes fluorescentes et d'états sombres d'un fluorophore. En suivi, un épisode sombre peut interrompre une trajectoire puis laisser réapparaître la même particule. Dans une reconstruction SMLM, plusieurs détections peuvent ainsi provenir d'un même fluorophore.

   SPT (Single-Particle Tracking)
      Suivi de particules individuelles pour caractériser leur dynamique. Le SPT associe des positions issues d'une acquisition temporelle, puis analyse les trajectoires obtenues, par exemple à l'aide du :term:`MSD (Mean Squared Displacement)`. Voir :doc:`user/examples/01_SPT`.

   Suivi
      Association de localisations successives en trajectoires. Le réglage :guilabel:`Max Distance` limite les associations entre plans consécutifs. Une distance trop faible fragmente le suivi des particules mobiles, et une distance trop grande augmente le risque d'associations erronées en champ dense.

   Trajectoire
      Suite ordonnée de positions associées à une même particule par le :term:`suivi <Suivi>`. Les numéros de plan permettent de retrouver les intervalles entre observations, notamment après reconnexion. Un segment affiché entre deux positions représente leur liaison et ne fournit aucune position mesurée dans les plans manquants.

Reconstruction, visualisation et résultats
------------------------------------------

.. glossary::
   :sorted:

   Alignement de canaux
      Transformation géométrique qui place les coordonnées de deux canaux dans un référentiel commun. Elle peut être estimée à partir de repères visibles dans les deux canaux et compenser leur décalage spatial, par exemple dû à l'optique. Voir :ref:`outil d'alignement <tool_alignment_page>`.

   Filtrage des résultats
      Sélection de localisations ou de trajectoires à partir de critères appliqués aux mesures calculées, par exemple le nombre de positions d'une trajectoire. Le filtrage change la population analysée et peut influer sur les distributions et les images produites en aval.

   Galerie de détections
      Mosaïque de régions d'intérêt extraites de la pile aux positions détectées. Elle permet d'inspecter côte à côte la forme des taches, le fond et les détections atypiques.

   Image haute résolution
      Image reconstruite à partir des coordonnées des localisations ou des trajectoires sur une grille généralement plus fine que celle de l'acquisition. La résolution effective dépend de la précision, de la densité des localisations et du rendu. Voir :ref:`viewer_hr_page`.

   Pipeline
      Enchaînement des traitements appliqués aux données, depuis le chargement de la pile jusqu'aux analyses, visualisations et exports. PALM-Tracer enregistre les paramètres et les métadonnées qui permettent de retracer le traitement. Voir :ref:`pipeline des traitements <pipeline_page>`.

   Rendu gaussien
      Représentation des localisations par des noyaux gaussiens centrés sur leurs coordonnées estimées. La largeur de ces noyaux détermine le lissage du rendu. L'ajustement gaussien estime des paramètres à partir de l'image brute, tandis que le rendu gaussien utilise des paramètres pour dessiner le résultat.

   Suréchantillonnage (Upscale Ratio)
      Augmentation du nombre de pixels de sortie par pixel d'acquisition dans le plan XY. Avec un facteur :math:`r` et une taille de pixel d'acquisition :math:`p`, le pas de la grille de rendu vaut :math:`p/r`. Une grille plus fine permet de représenter des positions sous-pixelliques et conserve la précision des positions estimées en entrée.

   Voxel
      Élément d'une grille volumique. Dans un rendu 3D, le pas entre deux coupes Z peut différer de la taille latérale du pixel de rendu, ce qui produit des voxels anisotropes.
