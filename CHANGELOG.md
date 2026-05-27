# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/) et ce projet adhère à [Semantic Versioning](https://semver.org/lang/fr/).

## [Unreleased]

<!-- run command : git log v1.4.0..HEAD --pretty=format:"- %s"-->

## [1.4.0] - 2026-05-27

### Ajouté

- Ajout d'un outil de Migration depuis l'ancienne version Metamorph de PALM Tracer ([#70](https://github.com/tmonseigne/palm-tracer/issues/70)).
- Compatibilité de la plateforme sur Mac et Unix ([#71](https://github.com/tmonseigne/palm-tracer/issues/71)).
- Ajout d'une sécurité permettant le calcul sur des fichiers dépassants la mémoire disponible ([#78](https://github.com/tmonseigne/palm-tracer/issues/78)).
- Ajout de bouttons dans la partie filtre permettant de réinitialiser, mettre à jour et sauvegarder les fichiers filtrés ([#86](https://github.com/tmonseigne/palm-tracer/issues/86)).
- Ajout d'une étape d'extraction de billes ([#90](https://github.com/tmonseigne/palm-tracer/issues/90) [#99](https://github.com/tmonseigne/palm-tracer/issues/99)).
- **Graphiques** :
  - Ajout de sources pour la génération de graphiques ([#93](https://github.com/tmonseigne/palm-tracer/issues/93)).
  - Ajout d'une option de visualisation de deux données en forme de nuage de points ([#61](https://github.com/tmonseigne/palm-tracer/issues/61)).
- Ajout de graphiques supplémentaires pour l'astigmatisme 3D ([#106](https://github.com/tmonseigne/palm-tracer/issues/106)).
- Ajout des éléments filtré à la prévisualisation (en rouge) ([#109](https://github.com/tmonseigne/palm-tracer/issues/109)).
- **Reconstruction** :
  - Ajout d'une option de reconstruction gaussienne ([#63](https://github.com/tmonseigne/palm-tracer/issues/63), [#65](https://github.com/tmonseigne/palm-tracer/issues/65)).
  - Ajout des options de filtrage à l'interface ([#64](https://github.com/tmonseigne/palm-tracer/issues/64)).
  - Ajout d'une option de correction de dérive lors de la reconstruction ([#91](https://github.com/tmonseigne/palm-tracer/issues/91), [#103](https://github.com/tmonseigne/palm-tracer/issues/103), [#105](https://github.com/tmonseigne/palm-tracer/issues/105)).
  - Possibilité d'enregistrer la visualisation actuelle (avec les paramètres de contraste, colormap, gamma) ([#112](https://github.com/tmonseigne/palm-tracer/issues/112)).
  - Possibilité de supprimer les billes identifiées ([#113](https://github.com/tmonseigne/palm-tracer/issues/113)).
  - Possibilité de recadrer automatiquement le résultat lors de l'enregistrement ([#115](https://github.com/tmonseigne/palm-tracer/issues/115)).
- Ajout de la possibiliter d'estimer directement la position axiale Z si le modèle d'astigmatisme est déjà calculé ([#114](https://github.com/tmonseigne/palm-tracer/issues/114)).

### Modifié

- **Correction de bugs Napari**
  - Lancement de signaux durant la mise à jour d'un paramètre et non uniquement à la fin de l'édition ([#81](https://github.com/tmonseigne/palm-tracer/issues/81)).
  - Les paramètres de calques n'était pas pris en compte ([#82](https://github.com/tmonseigne/palm-tracer/issues/82)).
- Correction d'un bug Plotly, les graphiques générés par Plotly ne fonctionnait pas snas connexion internet ([#88](https://github.com/tmonseigne/palm-tracer/issues/88)).
- Lors d'une impossibilité d'ajustement, les résultat sont explicitements identifiable par de nombreuses valeurs à -1 ([#96](https://github.com/tmonseigne/palm-tracer/issues/96)).
- **Astigmatism 3D** :
  - Changement des paramètres de configuration ([#97](https://github.com/tmonseigne/palm-tracer/issues/97), [#119](https://github.com/tmonseigne/palm-tracer/issues/119)).
  - Correction de divers points pour les calculs ([#102](https://github.com/tmonseigne/palm-tracer/issues/102)).
- Le fichier de paramètre sauvegardé est réduit pour ne prendre en compte que les éléments modifiables ([#101](https://github.com/tmonseigne/palm-tracer/issues/101)).
- Les angles sont maintenant toujours exprimés en degrés au lieu des radians ([#107](https://github.com/tmonseigne/palm-tracer/issues/107)).
- Ajout d'un système d'étape de processus permettant de passer certains calculs et réduire le nombre de fichiers en sortie ([#125](https://github.com/tmonseigne/palm-tracer/issues/125)).
- Amélioration de l'ergnomie de la fenêtre de reconstruction ([#126](https://github.com/tmonseigne/palm-tracer/issues/126)).
- Changement de l'architecture des paramètres en permettant la création de nouvelles interfaces liées et synchronisées ([#132](https://github.com/tmonseigne/palm-tracer/issues/132)).
- Diverses mises à jour mineures.

### Documentation

- Internationalisation de la documentation ([#76](https://github.com/tmonseigne/palm-tracer/issues/76)).
- Ajustements divers dans la documentation.

## [1.3.0] - 2026-02-04

### Ajouté

- Ajout d'un outil permettant de calculer un modèle d'astigmatisme 3D et d'estimer une position axiale en fonction de ce modèle ([#62](https://github.com/tmonseigne/palm-tracer/pull/62)).
- Ajout d'un outil permettant de migrer des résultats faits sous Metamorph vers le nouveau format Python ([#72](https://github.com/tmonseigne/palm-tracer/pull/72)).
- Ajout d'un filtre sur X et Y avec affichage de la zone d'intérêt en direct sur Napari ([#73](https://github.com/tmonseigne/palm-tracer/pull/73)).

### Modifié

- Durcissement des validations des tests.
- Changement de l'architecture lors de la construction des interfaces (intégré à l'ajout [#73](https://github.com/tmonseigne/palm-tracer/pull/73)).
  - Factorisation de certaines constructions (onglets, grilles, formulaires...).
  - Préparation d'un champ tooltip pour chaque paramètre (actuellement vide).
- Diverses mises à jour mineures.

### Documentation

- Ajout de manuels utilisateurs simples pour les différents outils standalone de la suite.
- Ajustements divers dans la documentation.

## [1.2.0] - 2025-12-15

### Ajouté

- Enregistrement des données filtrées optionnel lors du traitement ([#39](https://github.com/tmonseigne/palm-tracer/pull/39)).
- Ajout de la visualisation haute résolution des trajectoires ([#40](https://github.com/tmonseigne/palm-tracer/pull/40)).
- Ajout de la couleur à la visualisation haute résolution des trajectoires ([#44](https://github.com/tmonseigne/palm-tracer/pull/44)).
- Ajout d'une visionneuse 3D ([#46](https://github.com/tmonseigne/palm-tracer/pull/46), [#52](https://github.com/tmonseigne/palm-tracer/pull/52)).
- Ajout d'un outil d'alignement de piles (avec un fichier de coefficient précalculé) ([#47](https://github.com/tmonseigne/palm-tracer/issues/47)).
- Ajout d'une option de chargement des résultats précédents pour le fichier en cours ([#55](https://github.com/tmonseigne/palm-tracer/issues/55)).

### Modifié

- Lors de chargements de paramètres précédents, les différents traitements sont bloqués jusqu'à la fin du chargement ([#43](https://github.com/tmonseigne/palm-tracer/issues/43)).
- Certaines informations (thread fini, pile chargée...) utilisent les notifications internes à Napari ([#45](https://github.com/tmonseigne/palm-tracer/pull/45)).
- Amélioration d'une visionneuse de graphiques (ajout des filtres et lien avec l'interface principale) ([#54](https://github.com/tmonseigne/palm-tracer/pull/54)).
- Amélioration d'une visionneuse haute résolution (ajout d'options de modifications dynamiques) ([#56](https://github.com/tmonseigne/palm-tracer/pull/56)).
- Diverses mises à jour mineures.

### Documentation

- Ajout d'un manuel utilisateur simple.
- Ajustements divers dans la documentation.

## [1.1.0] - 2025-10-23

### Ajouté

- Ajout de visualisation des points du plan précédent et du plan suivant lors de la prévisualisation et ajout d'une zone d'intérêt circulaire ou carré au choix.
- Ajout de calculs de métriques pour les trajectoires ([#37](https://github.com/tmonseigne/palm-tracer/pull/37)).
- Ajout d'une option de reconnexion des trajectoires dû à des scintillements (blinking) ([#35](https://github.com/tmonseigne/palm-tracer/pull/35)).
- Ajout d'une visionneuse de graphiques à partir des fichiers CSV précalculés ([#29](https://github.com/tmonseigne/palm-tracer/pull/29)).
- Ajout d'une visionneuse 3D à partir d'un fichier CSV contenant les colonnes X, Y, Z et Integrated Intensity ([#28](https://github.com/tmonseigne/palm-tracer/pull/28)).
- Ajout d'un ajustement par spline 3D. **Attention** : incorrect pour le moment ([#26](https://github.com/tmonseigne/palm-tracer/pull/26)).

### Modifié

- Mise à jour des unités de calcul (micromètre et secondes au lieu de nanomètres et millisecondes).
- Le calcul du seuil automatique est déporté dans la DLL C++.
- Calcul effectué sur la pile complète au lieu de l'effectuer plan par plan ([#23](https://github.com/tmonseigne/palm-tracer/pull/23)).
- Modification des DLLs pour n'en avoir plus qu'une ([#25](https://github.com/tmonseigne/palm-tracer/pull/25)).
- Diverses mises à jour mineures.

### Documentation

- Ajustements divers dans la documentation utilisateur.

## [1.0.1] - 2025-05-20

### Ajouté

- Fichier de configuration par défaut (`settings.json`) pour faciliter le démarrage ([#17](https://github.com/tmonseigne/palm-tracer/pull/17)).
- Exécution du traitement dans un thread séparé pour éviter le blocage de l'interface ([#14](https://github.com/tmonseigne/palm-tracer/pull/14)).

### Modifié

- Interface : le bouton de prévisualisation a été remplacé par une case à cocher pour plus de clarté ([#21](https://github.com/tmonseigne/palm-tracer/pull/21)).
- Interface : amélioration de l'ergonomie pour le choix du mode de fit ([#20](https://github.com/tmonseigne/palm-tracer/pull/20)).

### Documentation

- Mise à jour du guide d'installation avec correction de bugs ([#16](https://github.com/tmonseigne/palm-tracer/pull/16)).
- Ajustements divers dans la documentation utilisateur.

### CI/CD

- Mise à jour de la configuration GitHub Actions pour intégrer macOS et Unix et ajout des versions python de 3.10 à 3.13.

## [1.0.0] - 2025-05-12

### Ajouté

- Première version stable de PALMTracer.
- Interface graphique interactive basée sur [Napari](https://napari.org/).
- Module d'importation des données SMLM (formats compatibles : .csv).
- Algorithmes d'analyse de trajectoires (suivi, regroupement, statistiques).
- Intégration continue avec GitHub Actions.
- Tests unitaires avec `pytest` et couverture de code via `codecov`.
- Documentation générée avec Sphinx, disponible dans le dossier `docs/`.

### Modifié

- Structure du projet conforme aux standards Python (`pyproject.toml`, `tox.ini`, `pytest.ini`).
- Ajout de la configuration `pre-commit` pour assurer la qualité du code.

### Supprimé

- N/A
