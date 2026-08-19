from dataclasses import FrozenInstanceError
import importlib.util
from pathlib import Path

import pytest

from sp001.contracts.retail_context_rule_observation_comparison import (
    ObservationChangeStatus,
)
from sp001.contracts.retail_context_rule_provenance import (
    RuleProvenanceType,
)
from sp001.services.retail_context_assessment_report import (
    RetailContextAssessmentReport,
    build_retail_context_assessment_report,
)


def load_canonical_service():
    path = (
        Path(__file__).resolve().parent
        / "test_rcp001_tcp_sears_assessment_service.py"
    )

    specification = importlib.util.spec_from_file_location(
        "rcp001_tcp_sears_assessment_service",
        path,
    )

    if (
        specification is None
        or specification.loader is None
    ):
        raise RuntimeError(
            "canonical TCP/Sears assessment service unavailable"
        )

    module = importlib.util.module_from_spec(
        specification,
    )

    specification.loader.exec_module(
        module,
    )

    return module


CANONICAL = load_canonical_service()


def create_report() -> RetailContextAssessmentReport:
    result = CANONICAL.execute_canonical_assessment()

    return build_retail_context_assessment_report(
        result=result,
    )


def test_report_returns_immutable_retail_assessment_contract() -> None:
    report = create_report()

    assert isinstance(
        report,
        RetailContextAssessmentReport,
    )


def test_report_preserves_case_identity() -> None:
    report = create_report()

    assert report.case_id == (
        "VCR-001-CASE-001"
    )


def test_report_preserves_snapshot_identity_and_version() -> None:
    report = create_report()

    assert report.snapshot_id == (
        "RCP-001-CASE-001-SNAPSHOT-001"
    )

    assert report.snapshot_version == 1


def test_report_contains_thirty_five_rule_records() -> None:
    report = create_report()

    assert report.total_rules == 35
    assert len(report.rules) == 35


def test_report_preserves_three_provenance_categories() -> None:
    report = create_report()

    assert report.directly_observed_count == 23
    assert report.derived_count == 7
    assert report.evidence_assessed_count == 5

    assert (
        report.directly_observed_count
        + report.derived_count
        + report.evidence_assessed_count
    ) == report.total_rules


def test_report_preserves_canonical_change_distribution() -> None:
    report = create_report()

    assert report.total_improved_count == 14
    assert report.unchanged_count == 16
    assert report.regressed_count == 0
    assert report.indeterminate_count == 5


def test_report_separates_direct_and_derived_improvements() -> None:
    report = create_report()

    assert report.directly_observed_improved_count == 9
    assert report.derived_improved_count == 5

    assert (
        report.directly_observed_improved_count
        + report.derived_improved_count
    ) == report.total_improved_count


def test_report_identifies_five_indeterminate_rules() -> None:
    report = create_report()

    indeterminate_rule_ids = {
        rule.rule_id
        for rule in report.rules
        if (
            rule.change_status
            is ObservationChangeStatus.INDETERMINATE
        )
    }

    assert indeterminate_rule_ids == {
        "GEO-004",
        "PHO-002",
        "CAP-001",
        "CAP-003",
        "CAP-004",
    }


def test_report_preserves_declared_contextual_policy() -> None:
    report = create_report()

    assert report.context_policy_ids == (
        "CP01-CONTEXTUAL-ADAPTATION",
    )


def test_report_preserves_only_opaque_evidence_identities() -> None:
    report = create_report()

    assert report.evidence_ids == (
        "ART-002",
        "ART-003",
    )


def test_report_does_not_invent_indeterminate_evidence() -> None:
    report = create_report()

    indeterminate = tuple(
        rule
        for rule in report.rules
        if (
            rule.change_status
            is ObservationChangeStatus.INDETERMINATE
        )
    )

    assert all(
        rule.initial_evidence_ids == ()
        and rule.final_evidence_ids == ()
        for rule in indeterminate
    )


def test_report_preserves_disputed_context_dimension() -> None:
    report = create_report()

    assert report.disputed_dimension_ids == (
        "CTX-RETAILER-001",
    )


def test_report_does_not_infer_customer_acceptance() -> None:
    report = create_report()

    assert report.customer_acceptance_status == (
        "NOT_ESTABLISHED"
    )


def test_report_does_not_infer_commercial_impact() -> None:
    report = create_report()

    assert report.commercial_impact_status == (
        "NOT_ESTABLISHED"
    )


def test_report_does_not_infer_independent_interventions() -> None:
    report = create_report()

    assert report.independent_intervention_status == (
        "NOT_ESTABLISHED"
    )


def test_report_rejects_invalid_assessment_result() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "result must be a "
            "RetailContextAssessmentResult"
        ),
    ):
        build_retail_context_assessment_report(
            result="RESULT-001",
        )


def test_report_is_immutable() -> None:
    report = create_report()

    with pytest.raises(
        FrozenInstanceError,
    ):
        report.case_id = "CASE-002"


def test_report_preserves_canonical_rule_order_and_provenance() -> None:
    report = create_report()

    assert report.rules[0].rule_id == "BRD-001"
    assert report.rules[-1].rule_id == "CAP-004"

    derived = next(
        rule
        for rule in report.rules
        if rule.rule_id == "GEO-005"
    )

    assert (
        derived.provenance_type
        is RuleProvenanceType.DERIVED
    )
