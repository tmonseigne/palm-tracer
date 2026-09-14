"""Teste les étapes et les transitions du pipeline de traitement."""

import pytest

from palm_tracer.Processing import Step
from palm_tracer.Settings.Groups import Localization


##################################################
def test_object_creation():
	"""Vérifie step objects creation."""

	def f():
		"""Retourne la valeur utilisée par le scénario de test."""
		return

	print(f"Step : {Step.Step('name', ['key'], f, f)}")
	print(f"Actions : {Step.StepAction.Compute},{Step.StepAction.Reuse},{Step.StepAction.Skip}")


##################################################
@pytest.mark.parametrize("active, previous_active, pipeline_dirty, allow_dirty, different, expected", [
		pytest.param(False, None, True, True, False, Step.StepAction.Skip, id="inactive-without-previous"),
		pytest.param(True, None, True, True, False, Step.StepAction.Compute, id="active-without-previous"),
		pytest.param(True, False, True, False, False, Step.StepAction.Compute, id="dirty-pipeline"),
		pytest.param(False, False, True, False, False, Step.StepAction.Skip, id="inactive-with-dirty-pipeline"),
		pytest.param(False, True, False, False, False, Step.StepAction.Reuse, id="reactivation-through-reuse"),
		pytest.param(False, False, False, False, False, Step.StepAction.Skip, id="both-groups-inactive"),
		pytest.param(True, False, False, False, False, Step.StepAction.Compute, id="activation-without-previous-result"),
		pytest.param(True, True, False, False, False, Step.StepAction.Reuse, id="identical-parameters"),
		pytest.param(True, True, False, False, True, Step.StepAction.Compute, id="different-parameters")])
def test_prepare_action(qtbot, active, previous_active, pipeline_dirty, allow_dirty, different, expected):
	"""Vérifie chaque décision indépendamment de l'état laissé par le scénario précédent."""
	group = Localization()
	group.active = active
	previous = None
	if previous_active is not None:
		previous = Localization()
		previous.active = previous_active
	if different: group["Threshold"].value = 10
	assert Step.prepare_step_action(group, previous, pipeline_dirty, allow_dirty) == expected
	if expected == Step.StepAction.Reuse: assert group.active
