Glossaire
=========

.. glossary::
   :sorted:

   Localisation
      Estimation de la position :math:`(x, y)` (et éventuellement :math:`z`) d'une molécule unique à partir de son image (PSF), généralement par ajustement d'un modèle ou d'une PSF expérimentale.

   Suivi
      Association des localisations d'une même molécule au fil des frames afin de former une trajectoire (track).

   Dérive
      Déplacement lent et global du champ d'observation au cours du temps (microscope, échantillon, stabilité mécanique/thermique), mesurable en :math:`(x, y)` et parfois en :math:`z`.

   Correction de dérive
      Estimation puis compensation de la dérive afin d'aligner les localisations (ou les images) dans un repère stable.

   ROI (Region Of Interest)
      Sous-région d'une image extraite autour d'une zone d'intérêt (ex. autour d'un maximum local) pour effectuer un traitement local (seuillage, fit, etc.).

   PSF (Point Spread Function)
      Réponse impulsionnelle optique du microscope. Elle décrit l'image formée par une source ponctuelle et conditionne la précision de localisation.

   SNR (Signal-to-Noise Ratio)
      Rapport signal sur bruit, indicateur de la qualité d'un signal mesuré. Un SNR faible dégrade la précision de localisation et augmente le risque de faux positifs.

   Seuil (Threshold)
      Valeur limite utilisée pour discriminer un signal (pixels/objets) du fond. Peut être fixe, automatique, ou dépendre d'un modèle de bruit.

   Watershed
      Méthode de segmentation basée sur la topographie d'une image (analogie "bassin versant"), souvent utilisée pour séparer des objets proches.

   Ajustement gaussien
      Ajustement d'une gaussienne (2D/3D) sur une PSF pour estimer les paramètres (position, amplitude, fond, largeur, etc.).

   Image haute résolution
      Image reconstruite à partir d'un ensemble de localisations (nuage de points) en appliquant un rendu (binning, gaussien, histogramme, etc.).

   Pipeline
      Enchaînement reproductible d'étapes de traitement (prétraitement, localisation, filtrage, suivi, rendu, export), avec des paramètres sauvegardés.
