from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timedelta, timezone

import pytest

from sp001.contracts.retail_context_rule_observation import (
    RetailContextRuleObservation, RuleObservationStatus,
)
from sp001.contracts.retail_process_actor import ActorType, RetailProcessActor
from sp001.contracts.retail_process_role import RetailProcessRole
from sp001.contracts.retail_rule_criterion import RetailRuleCriterion
from sp001.contracts.retail_rule_evaluation_record import (
    RetailRuleEvaluationRecord,
)
from sp001.contracts.retail_rule_evaluation_relation import (
    RetailRuleEvaluationRelation,
    RetailRuleEvaluationRelationType as RelationType,
)


def make_records():
    actor = RetailProcessActor(
        actor_id="ACTOR-TEST",
        customer_id="CUSTOMER-TEST",
        actor_type=ActorType.HUMAN,
        organization_id="ORG-TEST",
        role=RetailProcessRole("ROLE-TEST", "CUSTOMER-TEST", "VM reviewer"),
    )
    first = RetailRuleEvaluationRecord(
        evaluation_id="EVAL-1",
        observation=RetailContextRuleObservation(
            observation_id="OBS-1", rule_id="RULE-1",
            snapshot_id="SNAPSHOT-1", snapshot_version=1,
            case_id="CASE-1",
            status=RuleObservationStatus.NON_CONFORMANT,
            evidence_ids=("EVIDENCE-1",),
        ),
        criterion=RetailRuleCriterion("RULE-1", 1, "Synthetic criterion."),
        evaluator=actor,
        evaluated_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        rationale="Synthetic initial assessment.",
    )
    second = replace(
        first,
        evaluation_id="EVAL-2",
        evaluated_at=first.evaluated_at + timedelta(seconds=1),
        rationale="Synthetic subsequent assessment.",
    )
    return first, second


def make_relation(kind=RelationType.JUDGMENT_REVIEW):
    first, second = make_records()
    return RetailRuleEvaluationRelation(
        relation_id="REL-1", previous=first, current=second,
        relation_type=kind,
        rationale="Explicit synthetic relationship.",
        intervention_evidence_ids=(
            ("INTERVENTION-EVIDENCE-1",)
            if kind is RelationType.AFTER_DECLARED_INTERVENTION else ()
        ),
    )


@pytest.mark.parametrize("kind", list(RelationType))
def test_preserves_exact_records_and_declared_relation(kind):
    relation = make_relation(kind)
    rebuilt = replace(relation)
    assert rebuilt.previous is relation.previous
    assert rebuilt.current is relation.current
    assert rebuilt.relation_type is kind
    assert relation.previous.evaluation_id == "EVAL-1"


def test_distinct_criterion_versions_are_preserved_without_classification():
    relation = make_relation()
    changed = replace(
        relation.current,
        criterion=RetailRuleCriterion("RULE-1", 2, "Changed requirement."),
    )
    result = replace(relation, current=changed)
    assert result.previous.criterion.criterion_version == 1
    assert result.current.criterion.criterion_version == 2
    assert not hasattr(result, "change_status")


def test_rejects_conflicting_content_for_same_criterion_version():
    relation = make_relation()
    changed = replace(
        relation.current,
        criterion=replace(relation.current.criterion, statement="Altered."),
    )
    with pytest.raises(ValueError, match="criterion version"):
        replace(relation, current=changed)


def test_rejects_conflicting_content_for_same_observation_identity():
    relation = make_relation()
    changed = replace(
        relation.current,
        observation=replace(
            relation.current.observation,
            status=RuleObservationStatus.CONFORMANT,
        ),
    )
    with pytest.raises(ValueError, match="observation identity"):
        replace(relation, current=changed)


def test_accepts_distinct_observation_without_inferring_intervention():
    relation = make_relation()
    changed = replace(
        relation.current,
        observation=replace(
            relation.current.observation,
            observation_id="OBS-2",
            status=RuleObservationStatus.CONFORMANT,
        ),
    )
    result = replace(relation, current=changed)
    assert result.relation_type is RelationType.JUDGMENT_REVIEW
    assert result.intervention_evidence_ids == ()
    assert result.previous.observation.status is RuleObservationStatus.NON_CONFORMANT


def test_rejects_same_evaluation_identity():
    relation = make_relation()
    with pytest.raises(ValueError, match="identities"):
        replace(relation, current=relation.previous)


def test_rejects_different_case():
    relation = make_relation()
    changed = replace(
        relation.current,
        observation=replace(
            relation.current.observation,
            observation_id="OTHER-OBS", case_id="OTHER-CASE",
        ),
    )
    with pytest.raises(ValueError, match="same case"):
        replace(relation, current=changed)


def test_rejects_different_rule():
    relation = make_relation()
    changed = replace(
        relation.current,
        criterion=replace(relation.current.criterion, rule_id="OTHER-RULE"),
        observation=replace(
            relation.current.observation,
            observation_id="OTHER-OBS", rule_id="OTHER-RULE",
        ),
    )
    with pytest.raises(ValueError, match="same rule"):
        replace(relation, current=changed)


def test_rejects_reversed_evaluation_time():
    relation = make_relation()
    changed = replace(
        relation.current,
        evaluated_at=relation.previous.evaluated_at - timedelta(seconds=1),
    )
    with pytest.raises(ValueError, match="precede"):
        replace(relation, current=changed)


def test_equal_times_do_not_imply_causality():
    relation = make_relation()
    result = replace(
        relation,
        current=replace(
            relation.current, evaluated_at=relation.previous.evaluated_at
        ),
    )
    assert result.relation_type is RelationType.JUDGMENT_REVIEW


def test_declared_intervention_requires_references():
    relation = make_relation(RelationType.AFTER_DECLARED_INTERVENTION)
    with pytest.raises(ValueError, match="requires evidence"):
        replace(relation, intervention_evidence_ids=())


def test_review_cannot_carry_intervention_references():
    with pytest.raises(ValueError, match="must not declare"):
        replace(make_relation(), intervention_evidence_ids=("EV-1",))


@pytest.mark.parametrize("value", [
    ["EV-1"], ("",), ("EV-1", "EV-1"), (42,),
])
def test_rejects_invalid_intervention_references(value):
    relation = make_relation(RelationType.AFTER_DECLARED_INTERVENTION)
    with pytest.raises((TypeError, ValueError)):
        replace(relation, intervention_evidence_ids=value)


@pytest.mark.parametrize("field", ["relation_id", "rationale"])
@pytest.mark.parametrize("value", ["", "  ", None])
def test_rejects_invalid_required_text(field, value):
    with pytest.raises((TypeError, ValueError)):
        replace(make_relation(), **{field: value})


@pytest.mark.parametrize("field", ["previous", "current", "relation_type"])
def test_rejects_invalid_nominal_values(field):
    with pytest.raises(TypeError):
        replace(make_relation(), **{field: None})


def test_relation_is_frozen():
    relation = make_relation()
    with pytest.raises(FrozenInstanceError):
        relation.rationale = "Replacement"
