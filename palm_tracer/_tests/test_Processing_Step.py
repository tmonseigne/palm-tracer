"""Fichier des tests pour la création de galeries."""
from palm_tracer.Processing import Step
from palm_tracer.Settings.Groups import Localization


def test_object_creation():
	"""Test step objects creation."""

	def f(): return

	print(f"Step : {Step.Step('name', ['key'], f, f)}")
	print(f"Actions : {Step.StepAction.Compute},{Step.StepAction.Reuse},{Step.StepAction.Skip}")


def test_prepare_action(qtbot):
	"""Test step action preparation."""

	group1 = Localization()
	group2 = Localization()

	# Groupe inactif et précédent groupe vide
	action = Step.prepare_step_action(group1, None, True, True)
	assert action == Step.StepAction.Skip

	# Groupe actif et précédent groupe vide
	group1.active = True
	action = Step.prepare_step_action(group1, None, True, True)
	assert action == Step.StepAction.Compute

	# Groupe actif et précédent groupe vide
	action = Step.prepare_step_action(group1, group2, True, False)
	assert action == Step.StepAction.Compute

	# Groupe inactif et précédent groupe vide
	group1.active = False
	action = Step.prepare_step_action(group1, group2, True, False)
	assert action == Step.StepAction.Skip

	# Groupe inactif et précédent actif
	group2.active = True
	action = Step.prepare_step_action(group1, group2, False, False)
	assert action == Step.StepAction.Reuse

	# Groupe inactif et précédent inactif
	group1.active = False  # On doit le remettre à False, le precédent test l'a mis à True
	group2.active = False
	action = Step.prepare_step_action(group1, group2, False, False)
	assert action == Step.StepAction.Skip

	# Groupe actif et précédent inactif
	group1.active = True
	action = Step.prepare_step_action(group1, group2, False, False)
	assert action == Step.StepAction.Compute

	# Groupe actif et précédent actif et paramètres identiques
	group2.active = True
	action = Step.prepare_step_action(group1, group2, False, False)
	assert action == Step.StepAction.Reuse

	# Groupe actif et précédent actif et paramètres différents
	group1["Threshold"].value = 10
	action = Step.prepare_step_action(group1, group2, False, False)
	assert action == Step.StepAction.Compute
