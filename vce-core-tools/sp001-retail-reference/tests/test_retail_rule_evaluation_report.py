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
    RetailRuleEvaluationRelationType,
)
from sp001.services.retail_rule_evaluation_report import (
    build_retail_rule_evaluation_report,
)


def records():
    actor = RetailProcessActor(
        "ACTOR-TEST", "CUSTOMER-TEST", ActorType.HUMAN, "ORG-TEST",
        RetailProcessRole("ROLE-TEST", "CUSTOMER-TEST", "VM reviewer"),
    )
    first = RetailRuleEvaluationRecord(
        "EVAL-1",
        RetailContextRuleObservation(
            "OBS-1", "RULE-1", "SNAPSHOT-1", 1, "CASE-1",
            RuleObservationStatus.NON_CONFORMANT, ("EVIDENCE-1",),
        ),
        RetailRuleCriterion("RULE-1", 1, "Synthetic initial criterion."),
        actor,
        datetime(2026, 1, 1, tzinfo=timezone.utc),
        "Synthetic original rationale.",
    )
    second = replace(
        first, evaluation_id="EVAL-2",
        observation=replace(
            first.observation, observation_id="OBS-2",
            snapshot_version=2,
            status=RuleObservationStatus.INSUFFICIENT_EVIDENCE,
            evidence_ids=(),
        ),
        criterion=RetailRuleCriterion(
            "RULE-1", 2, "Synthetic revised criterion."
        ),
        evaluated_at=first.evaluated_at + timedelta(seconds=1),
        rationale="Synthetic evidence limitation.",
    )
    relation = RetailRuleEvaluationRelation(
        "REL-1", first, second,
        RetailRuleEvaluationRelationType.JUDGMENT_REVIEW,
        "Explicit synthetic review relationship.",
    )
    return first, second, relation


def report(**overrides):
    first, second, relation = records()
    args = dict(
        case_id="CASE-1", evaluations=(first, second), relations=(relation,)
    )
    args.update(overrides)
    return build_retail_rule_evaluation_report(**args)


def test_preserves_complete_records_versions_and_foundations():
    first, second, relation = records()
    result = report(evaluations=(first, second), relations=(relation,))
    assert result.evaluations[0] is first
    assert result.evaluations[1] is second
    assert result.relations[0] is relation
    assert result.evaluations[0].rationale == "Synthetic original rationale."
    assert result.evaluations[1].rationale == "Synthetic evidence limitation."
    assert result.evaluations[0].criterion.criterion_version == 1
    assert result.evaluations[1].criterion.criterion_version == 2
    assert result.evaluations[0].evaluator is first.evaluator
    assert result.evaluations[0].evaluated_at == first.evaluated_at
    assert result.evaluations[0].observation.evidence_ids == ("EVIDENCE-1",)
    assert result.evaluations[1].observation.status is (
        RuleObservationStatus.INSUFFICIENT_EVIDENCE
    )


def test_single_evaluation_needs_no_inferred_relationship():
    first, _, _ = records()
    result = report(evaluations=(first,), relations=())
    assert result.relations == ()


def test_does_not_reorder_or_select_a_winner():
    first, second, relation = records()
    result = report(evaluations=(second, first), relations=(relation,))
    assert result.evaluations == (second, first)
    assert not hasattr(result, "winner")
    assert not hasattr(result, "change_status")


def test_rejects_cross_case_evaluation():
    first, _, _ = records()
    other = replace(
        first, observation=replace(first.observation, case_id="OTHER-CASE")
    )
    with pytest.raises(ValueError, match="case"):
        report(evaluations=(other,), relations=())


def test_rejects_duplicate_evaluation_identity():
    first, _, _ = records()
    with pytest.raises(ValueError, match="duplicate evaluation"):
        report(evaluations=(first, first), relations=())


def test_rejects_missing_relation_endpoint():
    first, _, relation = records()
    with pytest.raises(ValueError, match="absent"):
        report(evaluations=(first,), relations=(relation,))


def test_rejects_conflicting_relation_endpoint():
    first, second, relation = records()
    altered = replace(second, rationale="Contradictory content.")
    with pytest.raises(ValueError, match="content conflicts"):
        report(evaluations=(first, altered), relations=(relation,))


def test_rejects_conflicting_criterion_version_across_records():
    first, second, _ = records()
    altered = replace(
        second,
        criterion=replace(first.criterion, statement="Conflicting statement."),
    )
    with pytest.raises(ValueError, match="criterion version"):
        report(evaluations=(first, altered), relations=())


def test_rejects_conflicting_observation_identity_across_records():
    first, second, _ = records()
    altered = replace(
        second,
        observation=replace(
            second.observation,
            observation_id=first.observation.observation_id,
        ),
    )
    with pytest.raises(ValueError, match="observation identity"):
        report(evaluations=(first, altered), relations=())


def test_rejects_duplicate_relation_identity():
    first, second, relation = records()
    with pytest.raises(ValueError, match="duplicate relation"):
        report(
            evaluations=(first, second), relations=(relation, relation)
        )


@pytest.mark.parametrize("overrides,error", [
    ({"case_id": None}, TypeError),
    ({"case_id": " "}, ValueError),
    ({"evaluations": []}, TypeError),
    ({"evaluations": ()}, ValueError),
    ({"evaluations": (object(),)}, TypeError),
    ({"relations": []}, TypeError),
    ({"relations": (object(),)}, TypeError),
])
def test_rejects_invalid_report_inputs(overrides, error):
    with pytest.raises(error):
        report(**overrides)


def test_report_is_frozen():
    result = report()
    with pytest.raises(FrozenInstanceError):
        result.case_id = "REPLACEMENT"
