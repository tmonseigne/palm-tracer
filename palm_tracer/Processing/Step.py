"""Définit les étapes et les transitions du pipeline de traitement PALM."""

from __future__ import annotations

from dataclasses import dataclass
from enum import auto, Enum
from typing import Callable, TypeAlias

import pandas as pd

from palm_tracer.Settings.Groups import BaseSettingGroup

##################################################
FilterSingle: TypeAlias = Callable[[pd.DataFrame], pd.DataFrame]  # Fonction avec un dataframe et qui en retourne un.
FilterTracksCompute: TypeAlias = Callable[  # Fonction spécifique au tracks compute
	[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame], tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]]


##################################################
@dataclass(frozen=True)
class Step:
	"""
	Décrit une étape immuable du pipeline de traitement.

	:param group_name: Nom du groupe de paramètres contrôlant l'étape.
	:param keys: Clés des DataFrames lus ou produits par l'étape.
	:param process_func: Fonction exécutant le calcul.
	:param filter_func: Fonction appliquant le filtrage associé.
	:param allow_dirty: Autorise la réutilisation d'un résultat malgré l'invalidation du pipeline.
	:param apply_filter: Indique si le filtrage doit être appliqué.
	"""

	group_name: str
	"""Nom du groupe de paramètres lié."""
	keys: list[str]
	"""Liste des clés du/des DataFrame(s) dans le dictionnaire."""
	process_func: Callable[[], None]  # Fonction sans argument qui ne retourne rien
	"""Fonction de traitement de cette étape."""
	filter_func: Callable
	"""Fonction de filtre de cette étape."""
	allow_dirty: bool = False
	"""Autorise la réutilisation d'ancien traitement malgré un pipeline contenant un calcul (cas des billes)."""
	apply_filter: bool = True
	"""Choix de filtre à appliquer ou non (cas des visualisations)."""


##################################################
class StepAction(Enum):
	"""Énumère les décisions possibles lors de la préparation d'une étape du pipeline."""

	Compute = auto()
	"""Calcul réel."""
	Reuse = auto()
	"""Réutilisation d'un résultat existant."""
	Skip = auto()
	"""Ignoré (pas actif ou impossible)."""


##################################################
def prepare_step_action(group: BaseSettingGroup, previous_group: BaseSettingGroup | None, pipeline_dirty: bool, allow_dirty: bool = False) -> StepAction:
	"""
	Estime le type d'action à effectuer pour une étape du traitement.

	:param group: Groupe de paramètres actuel.
	:param previous_group: Groupe de paramètres du précédent process.
	:param pipeline_dirty: État du processus actuel (si un calcul a été fait, il n'est plus cohérent pour la suite).
	:param allow_dirty: Cas particulier ou une non-cohérence est permise.
		Exemple : l'extraction des billes a pu être fait avec des paramètres de localisations différents du traitement des données finales.
	:return: Type d'action à effectuer pour cette étape.
	"""
	# Calcul si aucun process précédent
	if previous_group is None: return StepAction.Compute if group.active else StepAction.Skip
	# Calcul si le Pipeline n'est plus cohérent
	if pipeline_dirty and not allow_dirty: return StepAction.Compute if group.active else StepAction.Skip
	# Si le group est inactif, mais que le précédent process l'était
	if not group.active:
		if previous_group.active:
			group.update_from_compact_dict(previous_group.to_compact_dict())  # On met à jour ses settings.
			return StepAction.Reuse
		else: return StepAction.Skip
	# Si l'étape du process précédent était inactive
	if not previous_group.active: return StepAction.Compute
	# Si l'étape du process précédent était active, la courante également, comparaison des valeurs pour éviter un recalcul
	if group.to_compact_dict() == previous_group.to_compact_dict(): return StepAction.Reuse
	# Valeurs différentes
	return StepAction.Compute
