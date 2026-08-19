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
    RuleEvaluationStatus,
    evaluate_context_rule,
)
from sp001.contracts.retail_context_rule_observation import (
    RetailContextRuleObservation,
    RuleObservationStatus,
)
from sp001.contracts.retail_context_rule_observation_binding import (
    bind_rule_observation,
)
from sp001.contracts.retail_context_snapshot import (
    RetailContextSnapshot,
)


def build_snapshot(
    *,
    dimension_status: DimensionEvidenceStatus,
    applicability: DimensionApplicability = (
        DimensionApplicability.REQUIRED
    ),
    snapshot_id: str = "RCP-SNAPSHOT-001",
    snapshot_version: int = 1,
    case_id: str = "CASE-001",
) -> RetailContextSnapshot:
    value = None

    if dimension_status in {
        DimensionEvidenceStatus.DOCUMENTED,
        DimensionEvidenceStatus.HUMAN_DECLARED,
        DimensionEvidenceStatus.MEASURED,
        DimensionEvidenceStatus.INDEPENDENTLY_VERIFIED,
        DimensionEvidenceStatus.DISPUTED,
    }:
        value = "BACKWALL"

    dimension = RetailContextDimension(
        dimension_id="CTX-FIXTURE-001",
        dimension_type="FIXTURE_TYPE",
        applicability=applicability,
        evidence_status=dimension_status,
        value=value,
    )

    return RetailContextSnapshot(
        snapshot_id=snapshot_id,
        snapshot_version=snapshot_version,
        case_id=case_id,
        dimensions=(dimension,),
    )


def build_evaluation(
    *,
    dimension_status: DimensionEvidenceStatus = (
        DimensionEvidenceStatus.DOCUMENTED
    ),
    applicability: DimensionApplicability = (
        DimensionApplicability.REQUIRED
    ),
):
    snapshot = build_snapshot(
        dimension_status=dimension_status,
        applicability=applicability,
    )

    rule = RetailContextRule(
        rule_id="RULE-FIXTURE-001",
        rule_type="VERIFY_FIXTURE_PRESENTATION",
        required_dimension_ids=("CTX-FIXTURE-001",),
    )

    return evaluate_context_rule(
        snapshot=snapshot,
        rule=rule,
    )


def build_observation(
    *,
    rule_id: str = "RULE-FIXTURE-001",
    snapshot_id: str = "RCP-SNAPSHOT-001",
    snapshot_version: int = 1,
    case_id: str = "CASE-001",
    status: RuleObservationStatus = (
        RuleObservationStatus.CONFORMANT
    ),
) -> RetailContextRuleObservation:
    evidence_ids = ()

    if status in {
        RuleObservationStatus.CONFORMANT,
        RuleObservationStatus.NON_CONFORMANT,
    }:
        evidence_ids = ("ART-002",)

    return RetailContextRuleObservation(
        observation_id="OBSERVATION-001",
        rule_id=rule_id,
        snapshot_id=snapshot_id,
        snapshot_version=snapshot_version,
        case_id=case_id,
        status=status,
        evidence_ids=evidence_ids,
    )


@pytest.mark.parametrize(
    "observation_status",
    (
        RuleObservationStatus.CONFORMANT,
        RuleObservationStatus.NON_CONFORMANT,
        RuleObservationStatus.INSUFFICIENT_EVIDENCE,
        RuleObservationStatus.DISPUTED,
    ),
)
def test_evaluable_rule_accepts_valid_observation_outcomes(
    observation_status: RuleObservationStatus,
) -> None:
    evaluation = build_evaluation()

    observation = build_observation(
        status=observation_status,
    )

    result = bind_rule_observation(
        evaluation=evaluation,
        observation=observation,
    )

    assert result.evaluation_status is RuleEvaluationStatus.EVALUABLE

    assert result.observation_status is observation_status


def test_binding_preserves_rule_and_observation_identity() -> None:
    result = bind_rule_observation(
        evaluation=build_evaluation(),
        observation=build_observation(),
    )

    assert result.rule_id == "RULE-FIXTURE-001"
    assert result.observation_id == "OBSERVATION-001"

    assert (
        result.rule_type
        == "VERIFY_FIXTURE_PRESENTATION"
    )


def test_binding_preserves_snapshot_and_case_identity() -> None:
    result = bind_rule_observation(
        evaluation=build_evaluation(),
        observation=build_observation(),
    )

    assert result.snapshot_id == "RCP-SNAPSHOT-001"
    assert result.snapshot_version == 1
    assert result.case_id == "CASE-001"


def test_binding_preserves_opaque_evidence_references() -> None:
    result = bind_rule_observation(
        evaluation=build_evaluation(),
        observation=build_observation(),
    )

    assert result.evidence_ids == ("ART-002",)


def test_binding_preserves_dimension_results() -> None:
    evaluation = build_evaluation()

    result = bind_rule_observation(
        evaluation=evaluation,
        observation=build_observation(),
    )

    assert (
        result.dimension_results
        == evaluation.dimension_results
    )


@pytest.mark.parametrize(
    ("field", "invalid_value", "message"),
    (
        (
            "rule_id",
            "RULE-FIXTURE-002",
            "observation rule_id does not match evaluation",
        ),
        (
            "snapshot_id",
            "RCP-SNAPSHOT-002",
            "observation snapshot_id does not match evaluation",
        ),
        (
            "snapshot_version",
            2,
            "observation snapshot_version does not match evaluation",
        ),
        (
            "case_id",
            "CASE-002",
            "observation case_id does not match evaluation",
        ),
    ),
)
def test_binding_rejects_identity_mismatch(
    field: str,
    invalid_value: str | int,
    message: str,
) -> None:
    observation = build_observation(
        **{
            field: invalid_value,
        }
    )

    with pytest.raises(
        ValueError,
        match=message,
    ):
        bind_rule_observation(
            evaluation=build_evaluation(),
            observation=observation,
        )


def test_insufficient_context_accepts_insufficient_observation() -> None:
    evaluation = build_evaluation(
        dimension_status=(
            DimensionEvidenceStatus.NOT_PROVIDED
        ),
    )

    observation = build_observation(
        status=(
            RuleObservationStatus.INSUFFICIENT_EVIDENCE
        ),
    )

    result = bind_rule_observation(
        evaluation=evaluation,
        observation=observation,
    )

    assert (
        result.evaluation_status
        is RuleEvaluationStatus.INSUFFICIENT_EVIDENCE
    )

    assert (
        result.observation_status
        is RuleObservationStatus.INSUFFICIENT_EVIDENCE
    )


@pytest.mark.parametrize(
    "observation_status",
    (
        RuleObservationStatus.CONFORMANT,
        RuleObservationStatus.NON_CONFORMANT,
        RuleObservationStatus.DISPUTED,
    ),
)
def test_insufficient_context_rejects_incompatible_observation(
    observation_status: RuleObservationStatus,
) -> None:
    evaluation = build_evaluation(
        dimension_status=(
            DimensionEvidenceStatus.NOT_PROVIDED
        ),
    )

    observation = build_observation(
        status=observation_status,
    )

    with pytest.raises(
        ValueError,
        match=(
            "insufficient evaluation only permits "
            "INSUFFICIENT_EVIDENCE observation"
        ),
    ):
        bind_rule_observation(
            evaluation=evaluation,
            observation=observation,
        )


def test_disputed_context_accepts_disputed_observation() -> None:
    evaluation = build_evaluation(
        dimension_status=(
            DimensionEvidenceStatus.DISPUTED
        ),
        applicability=(
            DimensionApplicability.DISPUTED
        ),
    )

    observation = build_observation(
        status=(
            RuleObservationStatus.DISPUTED
        ),
    )

    result = bind_rule_observation(
        evaluation=evaluation,
        observation=observation,
    )

    assert (
        result.evaluation_status
        is RuleEvaluationStatus.DISPUTED
    )

    assert (
        result.observation_status
        is RuleObservationStatus.DISPUTED
    )


@pytest.mark.parametrize(
    "observation_status",
    (
        RuleObservationStatus.CONFORMANT,
        RuleObservationStatus.NON_CONFORMANT,
        RuleObservationStatus.INSUFFICIENT_EVIDENCE,
    ),
)
def test_disputed_context_rejects_incompatible_observation(
    observation_status: RuleObservationStatus,
) -> None:
    evaluation = build_evaluation(
        dimension_status=(
            DimensionEvidenceStatus.DISPUTED
        ),
        applicability=(
            DimensionApplicability.DISPUTED
        ),
    )

    observation = build_observation(
        status=observation_status,
    )

    with pytest.raises(
        ValueError,
        match=(
            "disputed evaluation only permits "
            "DISPUTED observation"
        ),
    ):
        bind_rule_observation(
            evaluation=evaluation,
            observation=observation,
        )


def test_binding_rejects_invalid_evaluation() -> None:
    with pytest.raises(
        TypeError,
        match="evaluation must be a RuleEvaluationResult",
    ):
        bind_rule_observation(
            evaluation="RULE-FIXTURE-001",
            observation=build_observation(),
        )


def test_binding_rejects_invalid_observation() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "observation must be a "
            "RetailContextRuleObservation"
        ),
    ):
        bind_rule_observation(
            evaluation=build_evaluation(),
            observation="OBSERVATION-001",
        )


def test_binding_result_is_immutable() -> None:
    result = bind_rule_observation(
        evaluation=build_evaluation(),
        observation=build_observation(),
    )

    with pytest.raises(FrozenInstanceError):
        result.case_id = "CASE-002"


def test_binding_does_not_claim_customer_acceptance() -> None:
    result = bind_rule_observation(
        evaluation=build_evaluation(),
        observation=build_observation(),
    )

    assert not hasattr(
        result,
        "customer_accepted",
    )

    assert not hasattr(
        result,
        "commercial_revenue",
    )
