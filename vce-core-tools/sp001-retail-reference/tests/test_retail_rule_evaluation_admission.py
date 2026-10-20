from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timezone
from typing import get_type_hints

import pytest

from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.retail_context_rule_observation import (
    RetailContextRuleObservation,
)
from sp001.contracts.retail_evaluator_binding import (
    RetailEvaluatorBinding, RetailEvaluatorBindingSnapshot,
)
from sp001.contracts.retail_process_actor import ActorType, RetailProcessActor
from sp001.contracts.retail_process_role import RetailProcessRole
from sp001.contracts.retail_rule_criterion import RetailRuleCriterion
from sp001.contracts.retail_rule_evaluation_record import (
    RetailRuleEvaluationRecord,
)
from sp001.contracts.retail_rule_evaluation_admission import (
    RetailRuleEvaluationAdmission,
)


def arguments():
    actor = RetailProcessActor(
        "ACTOR", "CUSTOMER", ActorType.HUMAN, "ORG",
        RetailProcessRole("ROLE", "CUSTOMER", "VM reviewer"),
    )
    principal = AuthenticatedPrincipal("ISSUER", "SUBJECT")
    status_type = get_type_hints(RetailContextRuleObservation)["status"]
    observation = RetailContextRuleObservation(
        observation_id="OBS", rule_id="RULE", snapshot_id="SNAPSHOT",
        snapshot_version=1, case_id="CASE",
        status=status_type.INSUFFICIENT_EVIDENCE, evidence_ids=(),
    )
    evaluation = RetailRuleEvaluationRecord(
        evaluation_id="EVALUATION", observation=observation,
        criterion=RetailRuleCriterion("RULE", 1, "Declared criterion"),
        evaluator=actor,
        evaluated_at=datetime(2020, 1, 1, tzinfo=timezone.utc),
        rationale="Available evidence does not support a conclusion.",
    )
    binding = RetailEvaluatorBinding(
        "BINDING", 2, principal, actor, "CASE", 100, 200,
    )
    return dict(
        evaluation=evaluation, principal=principal,
        binding_snapshot=RetailEvaluatorBindingSnapshot(binding, False),
        validated_at=150,
    )


def test_preserves_complete_evaluation_and_binding_references():
    args = arguments()
    admission = RetailRuleEvaluationAdmission(**args)
    assert admission.evaluation is args["evaluation"]
    assert admission.principal is args["principal"]
    assert admission.binding_snapshot is args["binding_snapshot"]
    assert admission.binding_snapshot.binding.revision == 2
    assert admission.evaluation.evaluated_at.year == 2020
    assert admission.validated_at == 150
    assert admission == RetailRuleEvaluationAdmission(**args)
    assert not hasattr(admission, "__dict__")
    with pytest.raises(FrozenInstanceError):
        admission.validated_at = 151


@pytest.mark.parametrize("instant,accepted", [
    (99, False), (100, True), (199, True), (200, False),
])
def test_validation_instant_uses_half_open_binding_interval(instant, accepted):
    args = arguments()
    args["validated_at"] = instant
    if accepted:
        RetailRuleEvaluationAdmission(**args)
    else:
        with pytest.raises(ValueError, match="outside binding validity"):
            RetailRuleEvaluationAdmission(**args)


@pytest.mark.parametrize("field,value,error", [
    ("evaluation", None, TypeError),
    ("principal", "SUBJECT", TypeError),
    ("binding_snapshot", None, TypeError),
    ("validated_at", True, TypeError),
    ("validated_at", 150.0, TypeError),
    ("validated_at", -1, ValueError),
])
def test_rejects_invalid_values(field, value, error):
    args = arguments()
    args[field] = value
    with pytest.raises(error):
        RetailRuleEvaluationAdmission(**args)


@pytest.mark.parametrize("mismatch", [
    "issuer", "subject", "actor_role", "case", "revoked",
])
def test_rejects_incoherent_attribution(mismatch):
    args = arguments()
    snapshot = args["binding_snapshot"]
    binding = snapshot.binding
    if mismatch == "issuer":
        args["principal"] = AuthenticatedPrincipal("OTHER", "SUBJECT")
    elif mismatch == "subject":
        args["principal"] = AuthenticatedPrincipal("ISSUER", "OTHER")
    elif mismatch == "actor_role":
        changed_actor = replace(
            binding.actor,
            role=replace(binding.actor.role, role_id="OTHER-ROLE"),
        )
        binding = replace(binding, actor=changed_actor)
    elif mismatch == "case":
        binding = replace(binding, case_id="OTHER-CASE")
    else:
        snapshot = replace(snapshot, revoked=True)
    args["binding_snapshot"] = replace(snapshot, binding=binding)
    with pytest.raises(ValueError):
        RetailRuleEvaluationAdmission(**args)


def test_later_revocation_does_not_rewrite_historical_record():
    args = arguments()
    admission = RetailRuleEvaluationAdmission(**args)
    historical = admission.binding_snapshot
    later = replace(
        historical,
        binding=replace(historical.binding, revision=3),
        revoked=True,
    )
    assert later.revoked is True
    assert admission.binding_snapshot is historical
    assert admission.binding_snapshot.revoked is False
    assert admission.binding_snapshot.binding.revision == 2
