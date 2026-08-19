from dataclasses import FrozenInstanceError

import pytest

from sp001.contracts.retail_context_dimension import (
    DimensionApplicability,
    DimensionEvidenceStatus,
    RetailContextDimension,
)
from sp001.contracts.retail_context_rule import (
    RetailContextRule,
)
from sp001.contracts.retail_context_rule_evaluation import (
    evaluate_context_rule,
)
from sp001.contracts.retail_context_rule_observation import (
    RetailContextRuleObservation,
    RuleObservationStatus,
)
from sp001.contracts.retail_context_rule_observation_binding import (
    bind_rule_observation,
)
from sp001.contracts.retail_context_rule_observation_comparison import (
    ObservationChangeStatus,
    compare_rule_observations,
)
from sp001.contracts.retail_context_snapshot import (
    RetailContextSnapshot,
)


def build_binding(
    *,
    observation_id: str,
    status: RuleObservationStatus,
    rule_id: str = "RULE-FIXTURE-001",
    snapshot_id: str = "RCP-SNAPSHOT-001",
    snapshot_version: int = 1,
    case_id: str = "CASE-001",
    evidence_id: str | None = None,
):
    dimension = RetailContextDimension(
        dimension_id="CTX-FIXTURE-001",
        dimension_type="FIXTURE_TYPE",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="BACKWALL",
    )

    snapshot = RetailContextSnapshot(
        snapshot_id=snapshot_id,
        snapshot_version=snapshot_version,
        case_id=case_id,
        dimensions=(dimension,),
    )

    rule = RetailContextRule(
        rule_id=rule_id,
        rule_type="VERIFY_FIXTURE_PRESENTATION",
        required_dimension_ids=(
            "CTX-FIXTURE-001",
        ),
    )

    evaluation = evaluate_context_rule(
        snapshot=snapshot,
        rule=rule,
    )

    evidence_ids = ()

    if status in {
        RuleObservationStatus.CONFORMANT,
        RuleObservationStatus.NON_CONFORMANT,
    }:
        evidence_ids = (
            evidence_id or "ART-001",
        )

    observation = RetailContextRuleObservation(
        observation_id=observation_id,
        rule_id=rule_id,
        snapshot_id=snapshot_id,
        snapshot_version=snapshot_version,
        case_id=case_id,
        status=status,
        evidence_ids=evidence_ids,
    )

    return bind_rule_observation(
        evaluation=evaluation,
        observation=observation,
    )


def test_non_conformant_to_conformant_is_improved() -> None:
    initial = build_binding(
        observation_id="OBSERVATION-INITIAL-001",
        status=RuleObservationStatus.NON_CONFORMANT,
        evidence_id="ART-003",
    )

    final = build_binding(
        observation_id="OBSERVATION-FINAL-001",
        status=RuleObservationStatus.CONFORMANT,
        evidence_id="ART-002",
    )

    result = compare_rule_observations(
        initial=initial,
        final=final,
    )

    assert result.change_status is ObservationChangeStatus.IMPROVED


def test_conformant_to_non_conformant_is_regressed() -> None:
    initial = build_binding(
        observation_id="OBSERVATION-INITIAL-001",
        status=RuleObservationStatus.CONFORMANT,
    )

    final = build_binding(
        observation_id="OBSERVATION-FINAL-001",
        status=RuleObservationStatus.NON_CONFORMANT,
    )

    result = compare_rule_observations(
        initial=initial,
        final=final,
    )

    assert result.change_status is ObservationChangeStatus.REGRESSED


@pytest.mark.parametrize(
    "status",
    (
        RuleObservationStatus.CONFORMANT,
        RuleObservationStatus.NON_CONFORMANT,
    ),
)
def test_identical_conclusive_outcomes_are_unchanged(
    status: RuleObservationStatus,
) -> None:
    initial = build_binding(
        observation_id="OBSERVATION-INITIAL-001",
        status=status,
    )

    final = build_binding(
        observation_id="OBSERVATION-FINAL-001",
        status=status,
    )

    result = compare_rule_observations(
        initial=initial,
        final=final,
    )

    assert result.change_status is ObservationChangeStatus.UNCHANGED


@pytest.mark.parametrize(
    ("initial_status", "final_status"),
    (
        (
            RuleObservationStatus.INSUFFICIENT_EVIDENCE,
            RuleObservationStatus.CONFORMANT,
        ),
        (
            RuleObservationStatus.CONFORMANT,
            RuleObservationStatus.INSUFFICIENT_EVIDENCE,
        ),
        (
            RuleObservationStatus.DISPUTED,
            RuleObservationStatus.CONFORMANT,
        ),
        (
            RuleObservationStatus.CONFORMANT,
            RuleObservationStatus.DISPUTED,
        ),
        (
            RuleObservationStatus.INSUFFICIENT_EVIDENCE,
            RuleObservationStatus.INSUFFICIENT_EVIDENCE,
        ),
        (
            RuleObservationStatus.DISPUTED,
            RuleObservationStatus.DISPUTED,
        ),
        (
            RuleObservationStatus.DISPUTED,
            RuleObservationStatus.INSUFFICIENT_EVIDENCE,
        ),
    ),
)
def test_inconclusive_observations_remain_indeterminate(
    initial_status: RuleObservationStatus,
    final_status: RuleObservationStatus,
) -> None:
    initial = build_binding(
        observation_id="OBSERVATION-INITIAL-001",
        status=initial_status,
    )

    final = build_binding(
        observation_id="OBSERVATION-FINAL-001",
        status=final_status,
    )

    result = compare_rule_observations(
        initial=initial,
        final=final,
    )

    assert (
        result.change_status
        is ObservationChangeStatus.INDETERMINATE
    )


def test_comparison_preserves_rule_and_case_identity() -> None:
    initial = build_binding(
        observation_id="OBSERVATION-INITIAL-001",
        status=RuleObservationStatus.NON_CONFORMANT,
    )

    final = build_binding(
        observation_id="OBSERVATION-FINAL-001",
        status=RuleObservationStatus.CONFORMANT,
    )

    result = compare_rule_observations(
        initial=initial,
        final=final,
    )

    assert result.rule_id == "RULE-FIXTURE-001"

    assert (
        result.rule_type
        == "VERIFY_FIXTURE_PRESENTATION"
    )

    assert result.case_id == "CASE-001"


def test_comparison_preserves_snapshot_identity() -> None:
    initial = build_binding(
        observation_id="OBSERVATION-INITIAL-001",
        status=RuleObservationStatus.NON_CONFORMANT,
    )

    final = build_binding(
        observation_id="OBSERVATION-FINAL-001",
        status=RuleObservationStatus.CONFORMANT,
    )

    result = compare_rule_observations(
        initial=initial,
        final=final,
    )

    assert result.snapshot_id == "RCP-SNAPSHOT-001"
    assert result.snapshot_version == 1


def test_comparison_preserves_observation_identity() -> None:
    initial = build_binding(
        observation_id="OBSERVATION-INITIAL-001",
        status=RuleObservationStatus.NON_CONFORMANT,
    )

    final = build_binding(
        observation_id="OBSERVATION-FINAL-001",
        status=RuleObservationStatus.CONFORMANT,
    )

    result = compare_rule_observations(
        initial=initial,
        final=final,
    )

    assert (
        result.initial_observation_id
        == "OBSERVATION-INITIAL-001"
    )

    assert (
        result.final_observation_id
        == "OBSERVATION-FINAL-001"
    )


def test_comparison_preserves_observation_statuses() -> None:
    initial = build_binding(
        observation_id="OBSERVATION-INITIAL-001",
        status=RuleObservationStatus.NON_CONFORMANT,
    )

    final = build_binding(
        observation_id="OBSERVATION-FINAL-001",
        status=RuleObservationStatus.CONFORMANT,
    )

    result = compare_rule_observations(
        initial=initial,
        final=final,
    )

    assert (
        result.initial_status
        is RuleObservationStatus.NON_CONFORMANT
    )

    assert (
        result.final_status
        is RuleObservationStatus.CONFORMANT
    )


def test_comparison_preserves_independent_evidence_references() -> None:
    initial = build_binding(
        observation_id="OBSERVATION-INITIAL-001",
        status=RuleObservationStatus.NON_CONFORMANT,
        evidence_id="ART-003",
    )

    final = build_binding(
        observation_id="OBSERVATION-FINAL-001",
        status=RuleObservationStatus.CONFORMANT,
        evidence_id="ART-002",
    )

    result = compare_rule_observations(
        initial=initial,
        final=final,
    )

    assert result.initial_evidence_ids == (
        "ART-003",
    )

    assert result.final_evidence_ids == (
        "ART-002",
    )


@pytest.mark.parametrize(
    ("field", "invalid_value", "message"),
    (
        (
            "rule_id",
            "RULE-FIXTURE-002",
            "observation rule_id does not match",
        ),
        (
            "snapshot_id",
            "RCP-SNAPSHOT-002",
            "observation snapshot_id does not match",
        ),
        (
            "snapshot_version",
            2,
            "observation snapshot_version does not match",
        ),
        (
            "case_id",
            "CASE-002",
            "observation case_id does not match",
        ),
    ),
)
def test_comparison_rejects_identity_mismatch(
    field: str,
    invalid_value: str | int,
    message: str,
) -> None:
    initial = build_binding(
        observation_id="OBSERVATION-INITIAL-001",
        status=RuleObservationStatus.NON_CONFORMANT,
    )

    final = build_binding(
        observation_id="OBSERVATION-FINAL-001",
        status=RuleObservationStatus.CONFORMANT,
        **{
            field: invalid_value,
        },
    )

    with pytest.raises(
        ValueError,
        match=message,
    ):
        compare_rule_observations(
            initial=initial,
            final=final,
        )


def test_comparison_rejects_same_observation_identity() -> None:
    initial = build_binding(
        observation_id="OBSERVATION-001",
        status=RuleObservationStatus.NON_CONFORMANT,
    )

    final = build_binding(
        observation_id="OBSERVATION-001",
        status=RuleObservationStatus.CONFORMANT,
    )

    with pytest.raises(
        ValueError,
        match="initial and final observations must be distinct",
    ):
        compare_rule_observations(
            initial=initial,
            final=final,
        )


def test_comparison_rejects_invalid_initial_binding() -> None:
    final = build_binding(
        observation_id="OBSERVATION-FINAL-001",
        status=RuleObservationStatus.CONFORMANT,
    )

    with pytest.raises(
        TypeError,
        match="initial must be a RuleObservationBinding",
    ):
        compare_rule_observations(
            initial="OBSERVATION-INITIAL-001",
            final=final,
        )


def test_comparison_rejects_invalid_final_binding() -> None:
    initial = build_binding(
        observation_id="OBSERVATION-INITIAL-001",
        status=RuleObservationStatus.NON_CONFORMANT,
    )

    with pytest.raises(
        TypeError,
        match="final must be a RuleObservationBinding",
    ):
        compare_rule_observations(
            initial=initial,
            final="OBSERVATION-FINAL-001",
        )


def test_comparison_result_is_immutable() -> None:
    initial = build_binding(
        observation_id="OBSERVATION-INITIAL-001",
        status=RuleObservationStatus.NON_CONFORMANT,
    )

    final = build_binding(
        observation_id="OBSERVATION-FINAL-001",
        status=RuleObservationStatus.CONFORMANT,
    )

    result = compare_rule_observations(
        initial=initial,
        final=final,
    )

    with pytest.raises(FrozenInstanceError):
        result.case_id = "CASE-002"


def test_comparison_does_not_claim_commercial_outcomes() -> None:
    initial = build_binding(
        observation_id="OBSERVATION-INITIAL-001",
        status=RuleObservationStatus.NON_CONFORMANT,
    )

    final = build_binding(
        observation_id="OBSERVATION-FINAL-001",
        status=RuleObservationStatus.CONFORMANT,
    )

    result = compare_rule_observations(
        initial=initial,
        final=final,
    )

    assert not hasattr(
        result,
        "customer_accepted",
    )

    assert not hasattr(
        result,
        "commercial_revenue",
    )

    assert not hasattr(
        result,
        "independent_interventions",
    )


def test_change_vocabulary_is_exact() -> None:
    assert {
        status.value
        for status in ObservationChangeStatus
    } == {
        "IMPROVED",
        "UNCHANGED",
        "REGRESSED",
        "INDETERMINATE",
    }
