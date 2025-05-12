# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/)
et ce projet adhère à [Semantic Versioning](https://semver.org/lang/fr/).

## [Unreleased]

## [1.0.0] - 2025-05-12
### Ajouté
- Première version stable de PALMTracer.
- Interface graphique interactive basée sur [napari](https://napari.org/).
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
