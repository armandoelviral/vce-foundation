from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timezone

import pytest

from sp001.contracts.retail_context_rule_observation import (
    RetailContextRuleObservation,
    RuleObservationStatus,
)
from sp001.contracts.retail_process_actor import ActorType, RetailProcessActor
from sp001.contracts.retail_process_role import RetailProcessRole
from sp001.contracts.retail_rule_criterion import RetailRuleCriterion
from sp001.contracts.retail_rule_evaluation_record import (
    RetailRuleEvaluationRecord,
)


def make_record(status=RuleObservationStatus.CONFORMANT):
    role = RetailProcessRole("ROLE-TEST", "CUSTOMER-TEST", "VM reviewer")
    actor = RetailProcessActor(
        actor_id="ACTOR-TEST",
        customer_id="CUSTOMER-TEST",
        actor_type=ActorType.HUMAN,
        organization_id="ORG-TEST",
        role=role,
    )
    observation = RetailContextRuleObservation(
        observation_id="OBS-TEST",
        rule_id="RULE-TEST",
        snapshot_id="SNAPSHOT-TEST",
        snapshot_version=1,
        case_id="CASE-TEST",
        status=status,
        evidence_ids=(
            ("EVIDENCE-TEST",)
            if status in (
                RuleObservationStatus.CONFORMANT,
                RuleObservationStatus.NON_CONFORMANT,
            )
            else ()
        ),
    )
    return RetailRuleEvaluationRecord(
        evaluation_id="EVALUATION-TEST",
        observation=observation,
        criterion=RetailRuleCriterion(
            "RULE-TEST", 1,
            "Synthetic criterion: front-view slot S1 must contain blue.",
        ),
        evaluator=actor,
        evaluated_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        rationale="Synthetic reviewer statement for this test.",
    )


def test_preserves_complete_declared_evaluation():
    record = make_record()
    rebuilt = RetailRuleEvaluationRecord(
        record.evaluation_id,
        record.observation,
        record.criterion,
        record.evaluator,
        record.evaluated_at,
        record.rationale,
    )
    assert rebuilt == record
    assert rebuilt.observation is record.observation
    assert rebuilt.criterion is record.criterion
    assert rebuilt.evaluator is record.evaluator
    assert rebuilt.observation.evidence_ids == ("EVIDENCE-TEST",)


@pytest.mark.parametrize("status", list(RuleObservationStatus))
def test_preserves_each_observation_outcome(status):
    record = make_record(status)
    assert record.observation.status is status
    if status in (
        RuleObservationStatus.INSUFFICIENT_EVIDENCE,
        RuleObservationStatus.DISPUTED,
    ):
        assert record.observation.evidence_ids == ()
        assert record.rationale


def test_rejects_different_rule():
    record = make_record()
    criterion = replace(record.criterion, rule_id="OTHER-RULE")
    with pytest.raises(ValueError, match="rule_id"):
        replace(record, criterion=criterion)


def test_preserves_selected_criterion_version():
    record = make_record()
    revised = replace(
        record,
        evaluation_id="EVALUATION-SECOND",
        criterion=replace(
            record.criterion,
            criterion_version=2,
            statement="Revised synthetic criterion.",
        ),
    )
    assert record.criterion.criterion_version == 1
    assert revised.criterion.criterion_version == 2
    assert record.criterion.statement != revised.criterion.statement


@pytest.mark.parametrize("field", ["evaluation_id", "rationale"])
@pytest.mark.parametrize("value", ["", "   "])
def test_rejects_empty_required_text(field, value):
    with pytest.raises(ValueError):
        replace(make_record(), **{field: value})


@pytest.mark.parametrize("field", ["evaluation_id", "rationale"])
@pytest.mark.parametrize("value", [None, 42])
def test_rejects_invalid_text_types(field, value):
    with pytest.raises(TypeError):
        replace(make_record(), **{field: value})


@pytest.mark.parametrize("field", ["observation", "criterion", "evaluator"])
@pytest.mark.parametrize("value", [None, "opaque-id", object()])
def test_rejects_invalid_nominal_values(field, value):
    with pytest.raises(TypeError):
        replace(make_record(), **{field: value})


def test_rejects_naive_evaluation_time():
    with pytest.raises(ValueError, match="timezone-aware"):
        replace(make_record(), evaluated_at=datetime(2026, 1, 1))


@pytest.mark.parametrize("value", [None, "2026-01-01", 123])
def test_rejects_invalid_time_types(value):
    with pytest.raises(TypeError):
        replace(make_record(), evaluated_at=value)


def test_record_is_frozen():
    record = make_record()
    with pytest.raises(FrozenInstanceError):
        record.rationale = "Replacement"


def test_reassessment_does_not_modify_original():
    original = make_record()
    reassessment = replace(
        original,
        evaluation_id="EVALUATION-SECOND",
        observation=replace(
            original.observation,
            observation_id="OBS-SECOND",
            status=RuleObservationStatus.NON_CONFORMANT,
            evidence_ids=("EVIDENCE-SECOND",),
        ),
        rationale="A distinct synthetic observation was evaluated.",
    )
    assert reassessment.evaluation_id != original.evaluation_id
    assert original.observation.status is RuleObservationStatus.CONFORMANT
    assert original.observation.evidence_ids == ("EVIDENCE-TEST",)
    assert reassessment.observation.status is RuleObservationStatus.NON_CONFORMANT
