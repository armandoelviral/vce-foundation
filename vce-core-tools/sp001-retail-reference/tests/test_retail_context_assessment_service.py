from dataclasses import FrozenInstanceError

import pytest

from sp001.contracts.retail_context_dependency_source import (
    DependencySourceType,
    RetailContextDependencySource,
)
from sp001.contracts.retail_context_dimension import (
    DimensionApplicability,
    DimensionEvidenceStatus,
    RetailContextDimension,
)
from sp001.contracts.retail_context_rule_observation import (
    RuleObservationStatus,
)
from sp001.contracts.retail_context_rule_observation_comparison import (
    ObservationChangeStatus,
    RuleObservationComparison,
)
from sp001.contracts.retail_context_rule_provenance import (
    RetailContextRuleProvenance,
    RuleProvenanceType,
)
from sp001.contracts.retail_context_snapshot import (
    RetailContextSnapshot,
)
from sp001.services.retail_context_assessment import (
    RetailContextAssessmentResult,
    execute_retail_context_assessment,
)


def snapshot(
    *,
    case_id: str = "CASE-001",
    snapshot_id: str = "SNAPSHOT-001",
    snapshot_version: int = 1,
) -> RetailContextSnapshot:
    fixture = RetailContextDimension(
        dimension_id="CTX-FIXTURE-001",
        dimension_type="FIXTURE_TYPE",
        applicability=(
            DimensionApplicability.REQUIRED
        ),
        evidence_status=(
            DimensionEvidenceStatus.DOCUMENTED
        ),
        value="TCP_PRESENTATION_FIXTURE",
    )

    return RetailContextSnapshot(
        snapshot_id=snapshot_id,
        snapshot_version=snapshot_version,
        case_id=case_id,
        dimensions=(
            fixture,
        ),
    )


def direct(
    rule_id: str,
) -> RetailContextRuleProvenance:
    return RetailContextRuleProvenance(
        rule_id=rule_id,
        provenance_type=(
            RuleProvenanceType.DIRECTLY_OBSERVED
        ),
    )


def derived(
    rule_id: str,
    *source_rule_ids: str,
) -> RetailContextRuleProvenance:
    return RetailContextRuleProvenance(
        rule_id=rule_id,
        provenance_type=(
            RuleProvenanceType.DERIVED
        ),
        source_rule_ids=source_rule_ids,
    )


def assessed(
    rule_id: str,
) -> RetailContextRuleProvenance:
    return RetailContextRuleProvenance(
        rule_id=rule_id,
        provenance_type=(
            RuleProvenanceType.EVIDENCE_ASSESSED
        ),
    )


def comparison(
    rule_id: str,
    *,
    case_id: str = "CASE-001",
    snapshot_id: str = "SNAPSHOT-001",
    snapshot_version: int = 1,
    change_status: ObservationChangeStatus = (
        ObservationChangeStatus.IMPROVED
    ),
) -> RuleObservationComparison:
    if (
        change_status
        is ObservationChangeStatus.IMPROVED
    ):
        initial_status = (
            RuleObservationStatus.NON_CONFORMANT
        )

        final_status = (
            RuleObservationStatus.CONFORMANT
        )

        initial_evidence_ids = (
            "ART-003",
        )

        final_evidence_ids = (
            "ART-002",
        )

    elif (
        change_status
        is ObservationChangeStatus.UNCHANGED
    ):
        initial_status = (
            RuleObservationStatus.CONFORMANT
        )

        final_status = (
            RuleObservationStatus.CONFORMANT
        )

        initial_evidence_ids = (
            "ART-003",
        )

        final_evidence_ids = (
            "ART-002",
        )

    else:
        initial_status = (
            RuleObservationStatus.INSUFFICIENT_EVIDENCE
        )

        final_status = (
            RuleObservationStatus.INSUFFICIENT_EVIDENCE
        )

        initial_evidence_ids = ()
        final_evidence_ids = ()

    return RuleObservationComparison(
        rule_id=rule_id,
        rule_type="CUSTOMER_DECLARED_RETAIL_CONSTRAINT",
        snapshot_id=snapshot_id,
        snapshot_version=snapshot_version,
        case_id=case_id,
        initial_observation_id=(
            f"{rule_id}-OBS"
        ),
        final_observation_id=(
            f"{rule_id}-OUT"
        ),
        initial_status=initial_status,
        final_status=final_status,
        initial_evidence_ids=(
            initial_evidence_ids
        ),
        final_evidence_ids=(
            final_evidence_ids
        ),
        change_status=change_status,
    )


def test_service_returns_retail_assessment_result() -> None:
    result = execute_retail_context_assessment(
        snapshot=snapshot(),
        comparisons=(
            comparison("CLR-001"),
        ),
        provenance_records=(
            direct("CLR-001"),
        ),
    )

    assert isinstance(
        result,
        RetailContextAssessmentResult,
    )


def test_service_preserves_snapshot_identity() -> None:
    context = snapshot()

    result = execute_retail_context_assessment(
        snapshot=context,
        comparisons=(
            comparison("CLR-001"),
        ),
        provenance_records=(
            direct("CLR-001"),
        ),
    )

    assert result.snapshot is context
    assert result.summary.case_id == context.case_id

    assert (
        result.summary.snapshot_id
        == context.snapshot_id
    )

    assert (
        result.summary.snapshot_version
        == context.snapshot_version
    )


def test_service_materializes_validated_provenance_graph() -> None:
    result = execute_retail_context_assessment(
        snapshot=snapshot(),
        comparisons=(
            comparison("CLR-001"),
        ),
        provenance_records=(
            direct("CLR-001"),
        ),
    )

    assert result.provenance_graph.total_rules == 1

    assert (
        result.provenance_graph.directly_observed_count
        == 1
    )


def test_service_materializes_improvement_summary() -> None:
    result = execute_retail_context_assessment(
        snapshot=snapshot(),
        comparisons=(
            comparison("CLR-001"),
        ),
        provenance_records=(
            direct("CLR-001"),
        ),
    )

    assert result.summary.total_comparisons == 1
    assert result.summary.total_improved_count == 1

    assert (
        result.summary.directly_observed_improved_count
        == 1
    )


def test_service_separates_direct_and_derived_improvements() -> None:
    result = execute_retail_context_assessment(
        snapshot=snapshot(),
        comparisons=(
            comparison("CLR-001"),
            comparison("GEO-001"),
        ),
        provenance_records=(
            direct("CLR-001"),
            derived(
                "GEO-001",
                "CLR-001",
            ),
        ),
    )

    assert result.summary.total_improved_count == 2

    assert (
        result.summary.directly_observed_improved_count
        == 1
    )

    assert result.summary.derived_improved_count == 1


def test_service_preserves_evidence_assessed_indeterminate_rules() -> None:
    result = execute_retail_context_assessment(
        snapshot=snapshot(),
        comparisons=(
            comparison(
                "GEO-004",
                change_status=(
                    ObservationChangeStatus.INDETERMINATE
                ),
            ),
        ),
        provenance_records=(
            assessed("GEO-004"),
        ),
    )

    assert (
        result.provenance_graph.evidence_assessed_count
        == 1
    )

    assert result.summary.indeterminate_count == 1

    assert result.summary.total_improved_count == 0


def test_service_accepts_declared_context_policy() -> None:
    source = RetailContextDependencySource(
        source_id="CP01-CONTEXTUAL-ADAPTATION",
        source_type=(
            DependencySourceType.CONTEXT_POLICY
        ),
    )

    provenance = RetailContextRuleProvenance(
        rule_id="GEO-005",
        provenance_type=(
            RuleProvenanceType.DERIVED
        ),
        dependency_sources=(
            source,
        ),
    )

    result = execute_retail_context_assessment(
        snapshot=snapshot(),
        comparisons=(
            comparison(
                "GEO-005",
                change_status=(
                    ObservationChangeStatus.UNCHANGED
                ),
            ),
        ),
        provenance_records=(
            provenance,
        ),
        context_policy_ids=(
            "CP01-CONTEXTUAL-ADAPTATION",
        ),
    )

    assert (
        result.provenance_graph.context_policy_ids
        == (
            "CP01-CONTEXTUAL-ADAPTATION",
        )
    )

    assert result.provenance_graph.total_rules == 1


def test_service_rejects_invalid_snapshot() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "snapshot must be a "
            "RetailContextSnapshot"
        ),
    ):
        execute_retail_context_assessment(
            snapshot="SNAPSHOT-001",
            comparisons=(
                comparison("CLR-001"),
            ),
            provenance_records=(
                direct("CLR-001"),
            ),
        )


def test_service_rejects_mismatched_case_identity() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "assessment case_id does not match snapshot"
        ),
    ):
        execute_retail_context_assessment(
            snapshot=snapshot(
                case_id="CASE-001",
            ),
            comparisons=(
                comparison(
                    "CLR-001",
                    case_id="CASE-002",
                ),
            ),
            provenance_records=(
                direct("CLR-001"),
            ),
        )


def test_service_rejects_mismatched_snapshot_identity() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "assessment snapshot_id does not match snapshot"
        ),
    ):
        execute_retail_context_assessment(
            snapshot=snapshot(
                snapshot_id="SNAPSHOT-001",
            ),
            comparisons=(
                comparison(
                    "CLR-001",
                    snapshot_id="SNAPSHOT-002",
                ),
            ),
            provenance_records=(
                direct("CLR-001"),
            ),
        )


def test_service_rejects_mismatched_snapshot_version() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "assessment snapshot_version does not match snapshot"
        ),
    ):
        execute_retail_context_assessment(
            snapshot=snapshot(
                snapshot_version=1,
            ),
            comparisons=(
                comparison(
                    "CLR-001",
                    snapshot_version=2,
                ),
            ),
            provenance_records=(
                direct("CLR-001"),
            ),
        )


def test_service_rejects_provenance_without_comparison() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "missing comparison for rule_id: GEO-001"
        ),
    ):
        execute_retail_context_assessment(
            snapshot=snapshot(),
            comparisons=(
                comparison("CLR-001"),
            ),
            provenance_records=(
                direct("CLR-001"),
                derived(
                    "GEO-001",
                    "CLR-001",
                ),
            ),
        )


def test_service_rejects_comparison_without_provenance() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "missing provenance for rule_id: GEO-001"
        ),
    ):
        execute_retail_context_assessment(
            snapshot=snapshot(),
            comparisons=(
                comparison("CLR-001"),
                comparison("GEO-001"),
            ),
            provenance_records=(
                direct("CLR-001"),
            ),
        )


def test_service_rejects_undeclared_context_policy() -> None:
    source = RetailContextDependencySource(
        source_id="CP01-CONTEXTUAL-ADAPTATION",
        source_type=(
            DependencySourceType.CONTEXT_POLICY
        ),
    )

    provenance = RetailContextRuleProvenance(
        rule_id="GEO-005",
        provenance_type=(
            RuleProvenanceType.DERIVED
        ),
        dependency_sources=(
            source,
        ),
    )

    with pytest.raises(
        ValueError,
        match=(
            "missing context policy source_id: "
            "CP01-CONTEXTUAL-ADAPTATION"
        ),
    ):
        execute_retail_context_assessment(
            snapshot=snapshot(),
            comparisons=(
                comparison(
                    "GEO-005",
                    change_status=(
                        ObservationChangeStatus.UNCHANGED
                    ),
                ),
            ),
            provenance_records=(
                provenance,
            ),
        )


def test_service_preserves_external_evidence_identities() -> None:
    result = execute_retail_context_assessment(
        snapshot=snapshot(),
        comparisons=(
            comparison("CLR-001"),
        ),
        provenance_records=(
            direct("CLR-001"),
        ),
    )

    observed = result.summary.comparisons[0]

    assert observed.initial_evidence_ids == (
        "ART-003",
    )

    assert observed.final_evidence_ids == (
        "ART-002",
    )


def test_service_result_is_immutable() -> None:
    result = execute_retail_context_assessment(
        snapshot=snapshot(),
        comparisons=(
            comparison("CLR-001"),
        ),
        provenance_records=(
            direct("CLR-001"),
        ),
    )

    with pytest.raises(
        FrozenInstanceError,
    ):
        result.snapshot = snapshot()
