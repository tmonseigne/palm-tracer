# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/)
et ce projet adhère à [Semantic Versioning](https://semver.org/lang/fr/).

## [Unreleased]

<!-- run command : git log v1.2.0..HEAD --pretty=format:"- %s"-->

## [1.2.0] - 2025-12-15

### Ajouté

- Enregistrement des données filtrées optionnel lors du processing. ([#39](https://github.com/tmonseigne/palm-tracer/pull/39))
- Ajout de la visualisation haute résolution des trajectoires. ([#40](https://github.com/tmonseigne/palm-tracer/pull/40))
- Ajout de la couleur à la visualisation haute résolution des trajectoires. ([#44](https://github.com/tmonseigne/palm-tracer/pull/44))
- Ajout d'une visionneuse 3D. ([#46](https://github.com/tmonseigne/palm-tracer/pull/46) et [#52](https://github.com/tmonseigne/palm-tracer/pull/52))
- Ajout d'un outil d'alignement de piles (avec un fichier de coefficient précalculé) ([#47](https://github.com/tmonseigne/palm-tracer/issues/47)).
- Ajout d'une option de chargement des résultats précédents piour le fichier en cours ([#55](https://github.com/tmonseigne/palm-tracer/issues/55)).

### Modifié

- Certaines informations (thread fini, pile chargée...) utilisent les notifications internes à Napari. ([#45](https://github.com/tmonseigne/palm-tracer/pull/45))
- Lors de chargements de paramètres précédents, les différents process sont bloqué jusqu'à la fin du chargement. ([#43](https://github.com/tmonseigne/palm-tracer/issues/43))
- Amélioration d'une visionneuse de graphiques (ajout des filtres et lien avec l'interface principale). ([#54](https://github.com/tmonseigne/palm-tracer/pull/54))
- Amélioration d'une visionneuse haute résolution (ajout d'options de modifications dynamiques). ([#56](https://github.com/tmonseigne/palm-tracer/pull/56))
- Diverses mises à jour mineures

### Documentation

- Ajout d'un manuel utilisateur simple.
- Ajustements divers dans la documentation.

## [1.1.0] - 2025-10-23

### Ajouté

- Ajout de visualisation des points de la frame précédente et de la frame suivante lors de la preview et ajout d'une ROI circulaire au choix.
- Ajout de calculs de métriques pour les trajectoires. ([#37](https://github.com/tmonseigne/palm-tracer/pull/37))
- Ajout d'une option de reconnexion des trajectoires dû à des scintillements (blinking). ([#35](https://github.com/tmonseigne/palm-tracer/pull/35))
- Ajout d'une visionneuse de graphiques à partir des fichiers CSV précalculés. ([#29](https://github.com/tmonseigne/palm-tracer/pull/29))
- Ajout d'une visionneuse 3D à partir d'un fichier CSV contenant les colonnes X, Y, Z et Integrated Intensity. ([#28](https://github.com/tmonseigne/palm-tracer/pull/28))
- Ajout d'un d'un ajustement par Spline 3D. **Attention** : incorrect pour le moment. ([#26](https://github.com/tmonseigne/palm-tracer/pull/26))

### Modifié

- Mise à jour des unités de calcul (micromètre et secondes au lieu de nanomètres et millisecondes).
- Le calcul du seuil automatique est déporté dans la DLL C++.
- Modification des DLLs pour n'en avoir plus qu'une. ([#25](https://github.com/tmonseigne/palm-tracer/pull/25))
- Calcul effectué sur la pile complète au lieu de l'effectuer plan par plan. ([#23](https://github.com/tmonseigne/palm-tracer/pull/23))
- Diverses mises à jour mineures

### Documentation

- Ajustements divers dans la documentation utilisateur.

## [1.0.1] - 2025-05-20

### Ajouté

- Fichier de configuration par défaut (`settings.json`) pour faciliter le démarrage. ([#17](https://github.com/tmonseigne/palm-tracer/pull/17))
- Exécution du traitement dans un thread séparé pour éviter le blocage de l'interface. ([#14](https://github.com/tmonseigne/palm-tracer/pull/14))

### Modifié

- Interface : le bouton de prévisualisation a été remplacé par une case à cocher pour plus de clarté. ([#21](https://github.com/tmonseigne/palm-tracer/pull/21))
- Interface : amélioration de l’ergonomie pour le choix du mode de fit. ([#20](https://github.com/tmonseigne/palm-tracer/pull/20))

### Documentation

- Mise à jour du guide d’installation avec correction de bugs. ([#16](https://github.com/tmonseigne/palm-tracer/pull/16))
- Ajustements divers dans la documentation utilisateur.

### CI/CD

- Mise à jour de la configuration GitHub Actions pour intégrer MacOS et Unix et ajout des versions python de 3.10 à 3.13.

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
