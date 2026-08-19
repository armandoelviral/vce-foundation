from dataclasses import FrozenInstanceError

import pytest

from sp001.contracts.retail_context_dimension import (
    DimensionApplicability,
    DimensionEvidenceStatus,
    RetailContextDimension,
)
from sp001.contracts.retail_context_dimension_evaluation import (
    DimensionEvaluationStatus,
)
from sp001.contracts.retail_context_rule import (
    RetailContextRule,
)
from sp001.contracts.retail_context_rule_evaluation import (
    RuleEvaluationStatus,
    evaluate_context_rule,
)
from sp001.contracts.retail_context_snapshot import (
    RetailContextSnapshot,
)


def build_dimension(
    *,
    dimension_id: str,
    applicability: DimensionApplicability,
    evidence_status: DimensionEvidenceStatus,
    value: str | None = None,
) -> RetailContextDimension:
    return RetailContextDimension(
        dimension_id=dimension_id,
        dimension_type="CUSTOMER_DEFINED_DIMENSION",
        applicability=applicability,
        evidence_status=evidence_status,
        value=value,
    )


def build_snapshot(
    *dimensions: RetailContextDimension,
) -> RetailContextSnapshot:
    return RetailContextSnapshot(
        snapshot_id="RCP-SNAPSHOT-001",
        snapshot_version=1,
        case_id="CASE-001",
        dimensions=dimensions,
    )


def build_rule(
    *dimension_ids: str,
) -> RetailContextRule:
    return RetailContextRule(
        rule_id="RULE-FIXTURE-001",
        rule_type="VERIFY_FIXTURE_PRESENTATION",
        required_dimension_ids=dimension_ids,
    )


def test_rule_with_supported_dimensions_is_evaluable() -> None:
    department = build_dimension(
        dimension_id="CTX-DEPARTMENT-001",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="CHILDRENSWEAR",
    )

    result = evaluate_context_rule(
        snapshot=build_snapshot(department),
        rule=build_rule("CTX-DEPARTMENT-001"),
    )

    assert result.status is RuleEvaluationStatus.EVALUABLE


def test_rule_preserves_rule_identity_and_type() -> None:
    department = build_dimension(
        dimension_id="CTX-DEPARTMENT-001",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="CHILDRENSWEAR",
    )

    result = evaluate_context_rule(
        snapshot=build_snapshot(department),
        rule=build_rule("CTX-DEPARTMENT-001"),
    )

    assert result.rule_id == "RULE-FIXTURE-001"

    assert (
        result.rule_type
        == "VERIFY_FIXTURE_PRESENTATION"
    )


def test_rule_preserves_snapshot_and_case_identity() -> None:
    department = build_dimension(
        dimension_id="CTX-DEPARTMENT-001",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="CHILDRENSWEAR",
    )

    result = evaluate_context_rule(
        snapshot=build_snapshot(department),
        rule=build_rule("CTX-DEPARTMENT-001"),
    )

    assert result.snapshot_id == "RCP-SNAPSHOT-001"
    assert result.snapshot_version == 1
    assert result.case_id == "CASE-001"


def test_rule_preserves_dimension_level_evaluation() -> None:
    department = build_dimension(
        dimension_id="CTX-DEPARTMENT-001",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="CHILDRENSWEAR",
    )

    result = evaluate_context_rule(
        snapshot=build_snapshot(department),
        rule=build_rule("CTX-DEPARTMENT-001"),
    )

    assert result.dimension_results == (
        (
            "CTX-DEPARTMENT-001",
            DimensionEvaluationStatus.EVALUABLE,
        ),
    )


def test_rule_reports_missing_required_dimension() -> None:
    result = evaluate_context_rule(
        snapshot=build_snapshot(),
        rule=build_rule("CTX-CAPACITY-001"),
    )

    assert (
        result.status
        is RuleEvaluationStatus.INSUFFICIENT_EVIDENCE
    )

    assert result.missing_dimension_ids == (
        "CTX-CAPACITY-001",
    )


def test_rule_reports_existing_dimension_without_evidence() -> None:
    capacity = build_dimension(
        dimension_id="CTX-CAPACITY-001",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.NOT_PROVIDED,
    )

    result = evaluate_context_rule(
        snapshot=build_snapshot(capacity),
        rule=build_rule("CTX-CAPACITY-001"),
    )

    assert (
        result.status
        is RuleEvaluationStatus.INSUFFICIENT_EVIDENCE
    )

    assert result.dimension_results == (
        (
            "CTX-CAPACITY-001",
            DimensionEvaluationStatus.INSUFFICIENT_EVIDENCE,
        ),
    )


def test_rule_preserves_required_context_dispute() -> None:
    context = build_dimension(
        dimension_id="CTX-CONTEXT-001",
        applicability=DimensionApplicability.DISPUTED,
        evidence_status=DimensionEvidenceStatus.DISPUTED,
        value="DECLARED_CONTEXT_UNVERIFIED",
    )

    result = evaluate_context_rule(
        snapshot=build_snapshot(context),
        rule=build_rule("CTX-CONTEXT-001"),
    )

    assert result.status is RuleEvaluationStatus.DISPUTED


def test_unrelated_evidence_gap_does_not_block_rule() -> None:
    department = build_dimension(
        dimension_id="CTX-DEPARTMENT-001",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="CHILDRENSWEAR",
    )

    capacity = build_dimension(
        dimension_id="CTX-CAPACITY-001",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.NOT_PROVIDED,
    )

    result = evaluate_context_rule(
        snapshot=build_snapshot(department, capacity),
        rule=build_rule("CTX-DEPARTMENT-001"),
    )

    assert result.status is RuleEvaluationStatus.EVALUABLE


def test_unrelated_context_dispute_does_not_block_rule() -> None:
    department = build_dimension(
        dimension_id="CTX-DEPARTMENT-001",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="CHILDRENSWEAR",
    )

    context = build_dimension(
        dimension_id="CTX-CONTEXT-001",
        applicability=DimensionApplicability.DISPUTED,
        evidence_status=DimensionEvidenceStatus.DISPUTED,
        value="DECLARED_CONTEXT_UNVERIFIED",
    )

    result = evaluate_context_rule(
        snapshot=build_snapshot(department, context),
        rule=build_rule("CTX-DEPARTMENT-001"),
    )

    assert result.status is RuleEvaluationStatus.EVALUABLE


def test_rule_preserves_declared_dependency_order() -> None:
    department = build_dimension(
        dimension_id="CTX-DEPARTMENT-001",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="CHILDRENSWEAR",
    )

    fixture = build_dimension(
        dimension_id="CTX-FIXTURE-001",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="BACKWALL",
    )

    result = evaluate_context_rule(
        snapshot=build_snapshot(department, fixture),
        rule=build_rule(
            "CTX-FIXTURE-001",
            "CTX-DEPARTMENT-001",
        ),
    )

    assert tuple(
        dimension_id
        for dimension_id, _ in result.dimension_results
    ) == (
        "CTX-FIXTURE-001",
        "CTX-DEPARTMENT-001",
    )


def test_rule_evaluation_result_is_immutable() -> None:
    department = build_dimension(
        dimension_id="CTX-DEPARTMENT-001",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="CHILDRENSWEAR",
    )

    result = evaluate_context_rule(
        snapshot=build_snapshot(department),
        rule=build_rule("CTX-DEPARTMENT-001"),
    )

    with pytest.raises(FrozenInstanceError):
        result.rule_id = "RULE-FIXTURE-002"


def test_rule_evaluation_rejects_invalid_snapshot() -> None:
    with pytest.raises(
        TypeError,
        match="snapshot must be a RetailContextSnapshot",
    ):
        evaluate_context_rule(
            snapshot="RCP-SNAPSHOT-001",
            rule=build_rule("CTX-DEPARTMENT-001"),
        )


def test_rule_evaluation_rejects_invalid_rule() -> None:
    with pytest.raises(
        TypeError,
        match="rule must be a RetailContextRule",
    ):
        evaluate_context_rule(
            snapshot=build_snapshot(),
            rule="RULE-FIXTURE-001",
        )


def test_evaluable_status_does_not_claim_compliance() -> None:
    assert "COMPLIANT" not in {
        state.value
        for state in RuleEvaluationStatus
    }

    assert "NON_COMPLIANT" not in {
        state.value
        for state in RuleEvaluationStatus
    }


def test_rule_evaluation_vocabulary_is_exact() -> None:
    assert {
        state.value
        for state in RuleEvaluationStatus
    } == {
        "EVALUABLE",
        "INSUFFICIENT_EVIDENCE",
        "DISPUTED",
    }
