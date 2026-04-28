"""Classes utiles à la gestion du Pipeline PALM Tracer."""
from dataclasses import dataclass
from enum import auto, Enum
from typing import Callable, TypeAlias

import pandas as pd

from palm_tracer.Settings.Groups import BaseSettingGroup

##################################################
FuncNone: TypeAlias = Callable[[], None]  # Fonction sans argument qui ne retourne rien
FuncSingle: TypeAlias = Callable[[pd.DataFrame], pd.DataFrame]  # Fonction avec un dataframe et qui en retourne un.
FuncTracksCompute: TypeAlias = Callable[  # Fonction spécifique au tracks compute
	[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame], tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame],]


##################################################
@dataclass(frozen=True)
class Step:
	"""Classe immuable permettant de définir une étape du traitement."""
	group_name: str
	keys: list[str]
	process_func: FuncNone  # Fonction sans argument qui ne retourne rien
	filter_func: FuncNone | FuncSingle | FuncTracksCompute
	allow_dirty: bool = False
	apply_filter: bool = True


##################################################
class StepAction(Enum):
	"""Actions possibles pour une étape du pipeline."""
	Compute = auto()  # Calcul réel
	Reuse = auto()  # .	Réutilisation d'un résultat existant
	Skip = auto()  # .	Ignoré (pas actif ou impossible)


##################################################
def prepare_step_action(group: BaseSettingGroup, previous_group: BaseSettingGroup | None, pipeline_dirty: bool, allow_dirty: bool = False) -> StepAction:
	"""
	Estime le type d'action à effectuer pour une étape du traitement
	:param group: Group de setting actuel
	:param previous_group: Group de setting du précédent process
	:param pipeline_dirty: Etat du processus actuel (si un calcul a été fait, il n'est plus cohérent pour la suite)
	:param allow_dirty: Cas particulier ou une non-cohérence est permise
	(exemple l'extraction des billes a pu être fait avec des paramètres de localisations différents du traitement des données finales)
	:return: Type d'action à effectuer pour cette étape
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
