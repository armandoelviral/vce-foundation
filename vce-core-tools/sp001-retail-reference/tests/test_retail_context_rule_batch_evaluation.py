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
from sp001.contracts.retail_context_rule_batch_evaluation import (
    evaluate_context_rule_batch,
)
from sp001.contracts.retail_context_rule_evaluation import (
    RuleEvaluationStatus,
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


def build_snapshot() -> RetailContextSnapshot:
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

    capacity = build_dimension(
        dimension_id="CTX-CAPACITY-001",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.NOT_PROVIDED,
    )

    retailer = build_dimension(
        dimension_id="CTX-RETAILER-001",
        applicability=DimensionApplicability.DISPUTED,
        evidence_status=DimensionEvidenceStatus.DISPUTED,
        value="SEARS_MEXICO_HUMAN_DECLARED",
    )

    return RetailContextSnapshot(
        snapshot_id="RCP-SNAPSHOT-001",
        snapshot_version=1,
        case_id="CASE-001",
        dimensions=(
            department,
            fixture,
            capacity,
            retailer,
        ),
    )


def build_rule(
    *,
    rule_id: str,
    required_dimension_ids: tuple[str, ...],
) -> RetailContextRule:
    return RetailContextRule(
        rule_id=rule_id,
        rule_type="CUSTOMER_DEFINED_RULE",
        required_dimension_ids=required_dimension_ids,
    )


def test_batch_evaluates_one_supported_rule() -> None:
    rule = build_rule(
        rule_id="RULE-CLR-005",
        required_dimension_ids=(
            "CTX-DEPARTMENT-001",
            "CTX-FIXTURE-001",
        ),
    )

    result = evaluate_context_rule_batch(
        snapshot=build_snapshot(),
        rules=(rule,),
    )

    assert len(result.rule_results) == 1

    assert (
        result.rule_results[0].status
        is RuleEvaluationStatus.EVALUABLE
    )


def test_batch_preserves_independent_rule_outcomes() -> None:
    evaluable_rule = build_rule(
        rule_id="RULE-CLR-005",
        required_dimension_ids=(
            "CTX-DEPARTMENT-001",
        ),
    )

    insufficient_rule = build_rule(
        rule_id="RULE-GEO-004",
        required_dimension_ids=(
            "CTX-CAPACITY-001",
        ),
    )

    disputed_rule = build_rule(
        rule_id="RULE-CAP-004",
        required_dimension_ids=(
            "CTX-RETAILER-001",
        ),
    )

    result = evaluate_context_rule_batch(
        snapshot=build_snapshot(),
        rules=(
            evaluable_rule,
            insufficient_rule,
            disputed_rule,
        ),
    )

    assert tuple(
        (
            item.rule_id,
            item.status,
        )
        for item in result.rule_results
    ) == (
        (
            "RULE-CLR-005",
            RuleEvaluationStatus.EVALUABLE,
        ),
        (
            "RULE-GEO-004",
            RuleEvaluationStatus.INSUFFICIENT_EVIDENCE,
        ),
        (
            "RULE-CAP-004",
            RuleEvaluationStatus.DISPUTED,
        ),
    )


def test_batch_preserves_snapshot_and_case_identity() -> None:
    rule = build_rule(
        rule_id="RULE-CLR-005",
        required_dimension_ids=(
            "CTX-DEPARTMENT-001",
        ),
    )

    result = evaluate_context_rule_batch(
        snapshot=build_snapshot(),
        rules=(rule,),
    )

    assert result.snapshot_id == "RCP-SNAPSHOT-001"
    assert result.snapshot_version == 1
    assert result.case_id == "CASE-001"


def test_batch_preserves_declared_rule_order() -> None:
    first = build_rule(
        rule_id="RULE-SECOND",
        required_dimension_ids=(
            "CTX-FIXTURE-001",
        ),
    )

    second = build_rule(
        rule_id="RULE-FIRST",
        required_dimension_ids=(
            "CTX-DEPARTMENT-001",
        ),
    )

    result = evaluate_context_rule_batch(
        snapshot=build_snapshot(),
        rules=(
            first,
            second,
        ),
    )

    assert tuple(
        item.rule_id
        for item in result.rule_results
    ) == (
        "RULE-SECOND",
        "RULE-FIRST",
    )


def test_batch_reports_evaluable_rule_count() -> None:
    first = build_rule(
        rule_id="RULE-CLR-001",
        required_dimension_ids=(
            "CTX-DEPARTMENT-001",
        ),
    )

    second = build_rule(
        rule_id="RULE-CLR-002",
        required_dimension_ids=(
            "CTX-FIXTURE-001",
        ),
    )

    result = evaluate_context_rule_batch(
        snapshot=build_snapshot(),
        rules=(
            first,
            second,
        ),
    )

    assert result.evaluable_count == 2
    assert result.insufficient_evidence_count == 0
    assert result.disputed_count == 0


def test_batch_reports_insufficient_evidence_count() -> None:
    rule = build_rule(
        rule_id="RULE-GEO-004",
        required_dimension_ids=(
            "CTX-CAPACITY-001",
        ),
    )

    result = evaluate_context_rule_batch(
        snapshot=build_snapshot(),
        rules=(rule,),
    )

    assert result.evaluable_count == 0
    assert result.insufficient_evidence_count == 1
    assert result.disputed_count == 0


def test_batch_reports_disputed_rule_count() -> None:
    rule = build_rule(
        rule_id="RULE-CAP-004",
        required_dimension_ids=(
            "CTX-RETAILER-001",
        ),
    )

    result = evaluate_context_rule_batch(
        snapshot=build_snapshot(),
        rules=(rule,),
    )

    assert result.evaluable_count == 0
    assert result.insufficient_evidence_count == 0
    assert result.disputed_count == 1


def test_batch_reports_total_rule_count() -> None:
    rules = (
        build_rule(
            rule_id="RULE-CLR-005",
            required_dimension_ids=(
                "CTX-DEPARTMENT-001",
            ),
        ),
        build_rule(
            rule_id="RULE-GEO-004",
            required_dimension_ids=(
                "CTX-CAPACITY-001",
            ),
        ),
        build_rule(
            rule_id="RULE-CAP-004",
            required_dimension_ids=(
                "CTX-RETAILER-001",
            ),
        ),
    )

    result = evaluate_context_rule_batch(
        snapshot=build_snapshot(),
        rules=rules,
    )

    assert result.total_rules == 3
    assert result.evaluable_count == 1
    assert result.insufficient_evidence_count == 1
    assert result.disputed_count == 1


def test_batch_rejects_invalid_snapshot() -> None:
    rule = build_rule(
        rule_id="RULE-CLR-005",
        required_dimension_ids=(
            "CTX-DEPARTMENT-001",
        ),
    )

    with pytest.raises(
        TypeError,
        match="snapshot must be a RetailContextSnapshot",
    ):
        evaluate_context_rule_batch(
            snapshot="RCP-SNAPSHOT-001",
            rules=(rule,),
        )


def test_batch_rejects_mutable_rule_collection() -> None:
    rule = build_rule(
        rule_id="RULE-CLR-005",
        required_dimension_ids=(
            "CTX-DEPARTMENT-001",
        ),
    )

    with pytest.raises(
        TypeError,
        match="rules must be an immutable tuple",
    ):
        evaluate_context_rule_batch(
            snapshot=build_snapshot(),
            rules=[rule],
        )


def test_batch_rejects_empty_rule_collection() -> None:
    with pytest.raises(
        ValueError,
        match="rules must not be empty",
    ):
        evaluate_context_rule_batch(
            snapshot=build_snapshot(),
            rules=(),
        )


def test_batch_rejects_invalid_rule_elements() -> None:
    with pytest.raises(
        TypeError,
        match="every rule must be a RetailContextRule",
    ):
        evaluate_context_rule_batch(
            snapshot=build_snapshot(),
            rules=("RULE-CLR-005",),
        )


def test_batch_rejects_duplicate_rule_identity() -> None:
    first = build_rule(
        rule_id="RULE-CLR-005",
        required_dimension_ids=(
            "CTX-DEPARTMENT-001",
        ),
    )

    duplicate = build_rule(
        rule_id="RULE-CLR-005",
        required_dimension_ids=(
            "CTX-FIXTURE-001",
        ),
    )

    with pytest.raises(
        ValueError,
        match="duplicate rule_id: RULE-CLR-005",
    ):
        evaluate_context_rule_batch(
            snapshot=build_snapshot(),
            rules=(
                first,
                duplicate,
            ),
        )


def test_batch_result_is_immutable() -> None:
    rule = build_rule(
        rule_id="RULE-CLR-005",
        required_dimension_ids=(
            "CTX-DEPARTMENT-001",
        ),
    )

    result = evaluate_context_rule_batch(
        snapshot=build_snapshot(),
        rules=(rule,),
    )

    with pytest.raises(FrozenInstanceError):
        result.case_id = "CASE-002"


def test_batch_rule_results_are_immutable() -> None:
    rule = build_rule(
        rule_id="RULE-CLR-005",
        required_dimension_ids=(
            "CTX-DEPARTMENT-001",
        ),
    )

    result = evaluate_context_rule_batch(
        snapshot=build_snapshot(),
        rules=(rule,),
    )

    with pytest.raises(TypeError):
        result.rule_results[0] = result.rule_results[0]


def test_batch_does_not_claim_rule_compliance() -> None:
    rule = build_rule(
        rule_id="RULE-CLR-005",
        required_dimension_ids=(
            "CTX-DEPARTMENT-001",
        ),
    )

    result = evaluate_context_rule_batch(
        snapshot=build_snapshot(),
        rules=(rule,),
    )

    assert not hasattr(
        result,
        "compliant_count",
    )

    assert not hasattr(
        result,
        "non_compliant_count",
    )


def test_batch_does_not_claim_commercial_outcomes() -> None:
    rule = build_rule(
        rule_id="RULE-CLR-005",
        required_dimension_ids=(
            "CTX-DEPARTMENT-001",
        ),
    )

    result = evaluate_context_rule_batch(
        snapshot=build_snapshot(),
        rules=(rule,),
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
        "independent_improvements",
    )
