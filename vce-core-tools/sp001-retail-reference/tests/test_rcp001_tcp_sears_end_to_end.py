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
from sp001.contracts.retail_context_snapshot_evaluation import (
    SnapshotEvaluationStatus,
    evaluate_context_snapshot,
)
from sp001.models.objective import Objective


def create_tcp_sears_case():
    objective = Objective(
        objective_id="VCR-001-OBJECTIVE-001",
        title="Verify customer-declared retail fixture presentation",
        description=(
            "Evaluate evidence-backed visual merchandising "
            "without inferring customer acceptance or revenue."
        ),
    )

    return objective.create_case(
        case_id="VCR-001-CASE-001",
        scope="SEARS-MEXICO-HUMAN-DECLARED",
    )


def create_tcp_sears_snapshot(case_id: str):
    department = RetailContextDimension(
        dimension_id="CTX-DEPARTMENT-001",
        dimension_type="DEPARTMENT",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.HUMAN_DECLARED,
        value="CHILDRENSWEAR",
    )

    fixture = RetailContextDimension(
        dimension_id="CTX-FIXTURE-001",
        dimension_type="FIXTURE_TYPE",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="TCP_PRESENTATION_FIXTURE",
    )

    retailer = RetailContextDimension(
        dimension_id="CTX-RETAILER-001",
        dimension_type="RETAILER_CONTEXT",
        applicability=DimensionApplicability.DISPUTED,
        evidence_status=DimensionEvidenceStatus.DISPUTED,
        value="SEARS_MEXICO_HUMAN_DECLARED",
    )

    capacity = RetailContextDimension(
        dimension_id="CTX-CAPACITY-001",
        dimension_type="PRESENTATION_CAPACITY",
        applicability=DimensionApplicability.OPTIONAL,
        evidence_status=DimensionEvidenceStatus.NOT_PROVIDED,
    )

    return RetailContextSnapshot(
        snapshot_id="RCP-001-CASE-001-SNAPSHOT-001",
        snapshot_version=1,
        case_id=case_id,
        dimensions=(
            department,
            fixture,
            retailer,
            capacity,
        ),
    )


def create_presentation_rule():
    return RetailContextRule(
        rule_id="VCR-001-CASE-001-CLR-005",
        rule_type="VERIFY_DECLARED_COLOR_SEQUENCE",
        required_dimension_ids=(
            "CTX-DEPARTMENT-001",
            "CTX-FIXTURE-001",
        ),
    )


def create_observation(
    *,
    observation_id: str,
    status: RuleObservationStatus,
    evidence_id: str,
    rule_id: str,
    snapshot: RetailContextSnapshot,
):
    return RetailContextRuleObservation(
        observation_id=observation_id,
        rule_id=rule_id,
        snapshot_id=snapshot.snapshot_id,
        snapshot_version=snapshot.snapshot_version,
        case_id=snapshot.case_id,
        status=status,
        evidence_ids=(evidence_id,),
    )


def test_tcp_sears_fixture_rule_improves_between_obs_and_out() -> None:
    case = create_tcp_sears_case()

    snapshot = create_tcp_sears_snapshot(
        case.case_id,
    )

    rule = create_presentation_rule()

    evaluation = evaluate_context_rule(
        snapshot=snapshot,
        rule=rule,
    )

    assert evaluation.status is RuleEvaluationStatus.EVALUABLE

    initial_observation = create_observation(
        observation_id="VCR-001-CASE-001-OBS-001",
        status=RuleObservationStatus.NON_CONFORMANT,
        evidence_id="ART-003",
        rule_id=rule.rule_id,
        snapshot=snapshot,
    )

    final_observation = create_observation(
        observation_id="VCR-001-CASE-001-OUT-001",
        status=RuleObservationStatus.CONFORMANT,
        evidence_id="ART-002",
        rule_id=rule.rule_id,
        snapshot=snapshot,
    )

    initial = bind_rule_observation(
        evaluation=evaluation,
        observation=initial_observation,
    )

    final = bind_rule_observation(
        evaluation=evaluation,
        observation=final_observation,
    )

    comparison = compare_rule_observations(
        initial=initial,
        final=final,
    )

    assert comparison.case_id == "VCR-001-CASE-001"

    assert (
        comparison.rule_id
        == "VCR-001-CASE-001-CLR-005"
    )

    assert (
        comparison.initial_status
        is RuleObservationStatus.NON_CONFORMANT
    )

    assert (
        comparison.final_status
        is RuleObservationStatus.CONFORMANT
    )

    assert (
        comparison.change_status
        is ObservationChangeStatus.IMPROVED
    )

    assert comparison.initial_evidence_ids == (
        "ART-003",
    )

    assert comparison.final_evidence_ids == (
        "ART-002",
    )


def test_tcp_sears_retailer_context_remains_human_declared() -> None:
    case = create_tcp_sears_case()

    snapshot = create_tcp_sears_snapshot(
        case.case_id,
    )

    retailer = next(
        dimension
        for dimension in snapshot.dimensions
        if dimension.dimension_id == "CTX-RETAILER-001"
    )

    assert (
        retailer.value
        == "SEARS_MEXICO_HUMAN_DECLARED"
    )

    assert (
        retailer.applicability
        is DimensionApplicability.DISPUTED
    )

    assert (
        retailer.evidence_status
        is DimensionEvidenceStatus.DISPUTED
    )

    assert (
        retailer.evidence_status
        is not DimensionEvidenceStatus.INDEPENDENTLY_VERIFIED
    )


def test_tcp_sears_snapshot_preserves_context_discrepancy() -> None:
    case = create_tcp_sears_case()

    snapshot = create_tcp_sears_snapshot(
        case.case_id,
    )

    result = evaluate_context_snapshot(
        snapshot,
    )

    assert result.status is SnapshotEvaluationStatus.DISPUTED

    assert (
        "CTX-RETAILER-001",
        DimensionEvaluationStatus.DISPUTED,
    ) in result.dimension_results


def test_unrelated_retailer_dispute_does_not_block_color_rule() -> None:
    case = create_tcp_sears_case()

    snapshot = create_tcp_sears_snapshot(
        case.case_id,
    )

    evaluation = evaluate_context_rule(
        snapshot=snapshot,
        rule=create_presentation_rule(),
    )

    assert evaluation.status is RuleEvaluationStatus.EVALUABLE

    assert tuple(
        dimension_id
        for dimension_id, _ in evaluation.dimension_results
    ) == (
        "CTX-DEPARTMENT-001",
        "CTX-FIXTURE-001",
    )


def test_retailer_dependent_rule_preserves_context_dispute() -> None:
    case = create_tcp_sears_case()

    snapshot = create_tcp_sears_snapshot(
        case.case_id,
    )

    rule = RetailContextRule(
        rule_id="VCR-001-CASE-001-CAP-004",
        rule_type="VERIFY_RETAILER_CONTEXT",
        required_dimension_ids=(
            "CTX-RETAILER-001",
        ),
    )

    evaluation = evaluate_context_rule(
        snapshot=snapshot,
        rule=rule,
    )

    assert evaluation.status is RuleEvaluationStatus.DISPUTED

    assert evaluation.dimension_results == (
        (
            "CTX-RETAILER-001",
            DimensionEvaluationStatus.DISPUTED,
        ),
    )


def test_unavailable_optional_capacity_does_not_block_color_rule() -> None:
    case = create_tcp_sears_case()

    snapshot = create_tcp_sears_snapshot(
        case.case_id,
    )

    evaluation = evaluate_context_rule(
        snapshot=snapshot,
        rule=create_presentation_rule(),
    )

    assert evaluation.status is RuleEvaluationStatus.EVALUABLE

    assert "CTX-CAPACITY-001" not in {
        dimension_id
        for dimension_id, _ in evaluation.dimension_results
    }


def test_capacity_dependent_rule_reports_insufficient_evidence() -> None:
    case = create_tcp_sears_case()

    snapshot = create_tcp_sears_snapshot(
        case.case_id,
    )

    rule = RetailContextRule(
        rule_id="VCR-001-CASE-001-GEO-004",
        rule_type="VERIFY_DECLARED_PRESENTATION_CAPACITY",
        required_dimension_ids=(
            "CTX-CAPACITY-001",
        ),
    )

    evaluation = evaluate_context_rule(
        snapshot=snapshot,
        rule=rule,
    )

    assert (
        evaluation.status
        is RuleEvaluationStatus.INSUFFICIENT_EVIDENCE
    )

    assert evaluation.dimension_results == (
        (
            "CTX-CAPACITY-001",
            DimensionEvaluationStatus.OPTIONAL_UNAVAILABLE,
        ),
    )


def test_tcp_sears_case_preserves_original_objective_identity() -> None:
    case = create_tcp_sears_case()

    assert case.case_id == "VCR-001-CASE-001"

    assert (
        case.objective_id
        == "VCR-001-OBJECTIVE-001"
    )

    assert (
        case.scope
        == "SEARS-MEXICO-HUMAN-DECLARED"
    )


def test_tcp_sears_observations_use_opaque_external_evidence_ids() -> None:
    case = create_tcp_sears_case()

    snapshot = create_tcp_sears_snapshot(
        case.case_id,
    )

    rule = create_presentation_rule()

    initial = create_observation(
        observation_id="VCR-001-CASE-001-OBS-001",
        status=RuleObservationStatus.NON_CONFORMANT,
        evidence_id="ART-003",
        rule_id=rule.rule_id,
        snapshot=snapshot,
    )

    final = create_observation(
        observation_id="VCR-001-CASE-001-OUT-001",
        status=RuleObservationStatus.CONFORMANT,
        evidence_id="ART-002",
        rule_id=rule.rule_id,
        snapshot=snapshot,
    )

    assert initial.evidence_ids == ("ART-003",)
    assert final.evidence_ids == ("ART-002",)

    for evidence_id in (
        *initial.evidence_ids,
        *final.evidence_ids,
    ):
        assert evidence_id.startswith("ART-")
        assert "/" not in evidence_id
        assert "http" not in evidence_id.lower()


def test_tcp_sears_improvement_does_not_imply_customer_acceptance() -> None:
    case = create_tcp_sears_case()

    snapshot = create_tcp_sears_snapshot(
        case.case_id,
    )

    rule = create_presentation_rule()

    evaluation = evaluate_context_rule(
        snapshot=snapshot,
        rule=rule,
    )

    initial = bind_rule_observation(
        evaluation=evaluation,
        observation=create_observation(
            observation_id="VCR-001-CASE-001-OBS-001",
            status=RuleObservationStatus.NON_CONFORMANT,
            evidence_id="ART-003",
            rule_id=rule.rule_id,
            snapshot=snapshot,
        ),
    )

    final = bind_rule_observation(
        evaluation=evaluation,
        observation=create_observation(
            observation_id="VCR-001-CASE-001-OUT-001",
            status=RuleObservationStatus.CONFORMANT,
            evidence_id="ART-002",
            rule_id=rule.rule_id,
            snapshot=snapshot,
        ),
    )

    comparison = compare_rule_observations(
        initial=initial,
        final=final,
    )

    assert (
        comparison.change_status
        is ObservationChangeStatus.IMPROVED
    )

    assert not hasattr(
        comparison,
        "customer_accepted",
    )

    assert not hasattr(
        comparison,
        "commercial_revenue",
    )

    assert not hasattr(
        comparison,
        "independent_interventions",
    )
