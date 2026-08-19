from dataclasses import replace
import importlib.util
import json
from pathlib import Path

import pytest

from sp001.services.retail_context_assessment_report_serialization import (
    serialize_retail_context_assessment_report,
)


def load_report_tests():
    path = (
        Path(__file__).resolve().parent
        / "test_retail_context_assessment_report.py"
    )

    specification = importlib.util.spec_from_file_location(
        "rcp001_tcp_sears_assessment_report",
        path,
    )

    if (
        specification is None
        or specification.loader is None
    ):
        raise RuntimeError(
            "canonical retail assessment report unavailable"
        )

    module = importlib.util.module_from_spec(
        specification,
    )

    specification.loader.exec_module(
        module,
    )

    return module


REPORT = load_report_tests()


def create_report():
    return REPORT.create_report()


def create_payload() -> str:
    return serialize_retail_context_assessment_report(
        report=create_report(),
    )


def test_serializer_returns_text() -> None:
    payload = create_payload()

    assert isinstance(
        payload,
        str,
    )


def test_serializer_produces_valid_json_object() -> None:
    payload = create_payload()

    document = json.loads(
        payload,
    )

    assert isinstance(
        document,
        dict,
    )


def test_serializer_preserves_case_and_snapshot_identity() -> None:
    document = json.loads(
        create_payload(),
    )

    assert document["case_id"] == (
        "VCR-001-CASE-001"
    )

    assert document["snapshot_id"] == (
        "RCP-001-CASE-001-SNAPSHOT-001"
    )

    assert document["snapshot_version"] == 1


def test_serializer_preserves_provenance_counts() -> None:
    document = json.loads(
        create_payload(),
    )

    assert document["total_rules"] == 35

    assert (
        document["directly_observed_count"]
        == 23
    )

    assert document["derived_count"] == 7

    assert (
        document["evidence_assessed_count"]
        == 5
    )


def test_serializer_preserves_canonical_rule_order() -> None:
    document = json.loads(
        create_payload(),
    )

    assert len(
        document["rules"],
    ) == 35

    assert document["rules"][0]["rule_id"] == (
        "BRD-001"
    )

    assert document["rules"][-1]["rule_id"] == (
        "CAP-004"
    )


def test_serializer_represents_observation_states_as_strings() -> None:
    document = json.loads(
        create_payload(),
    )

    color_rule = next(
        rule
        for rule in document["rules"]
        if rule["rule_id"] == "CLR-001"
    )

    assert color_rule["initial_status"] == (
        "NON_CONFORMANT"
    )

    assert color_rule["final_status"] == (
        "CONFORMANT"
    )

    assert color_rule["change_status"] == (
        "IMPROVED"
    )


def test_serializer_represents_provenance_as_strings() -> None:
    document = json.loads(
        create_payload(),
    )

    provenance = {
        rule["rule_id"]: rule["provenance_type"]
        for rule in document["rules"]
    }

    assert provenance["CLR-001"] == (
        "DIRECTLY_OBSERVED"
    )

    assert provenance["GEO-005"] == (
        "DERIVED"
    )

    assert provenance["CAP-004"] == (
        "EVIDENCE_ASSESSED"
    )


def test_serializer_preserves_opaque_evidence_identities() -> None:
    document = json.loads(
        create_payload(),
    )

    assert document["evidence_ids"] == [
        "ART-002",
        "ART-003",
    ]


def test_serializer_preserves_empty_indeterminate_evidence() -> None:
    document = json.loads(
        create_payload(),
    )

    indeterminate = tuple(
        rule
        for rule in document["rules"]
        if (
            rule["change_status"]
            == "INDETERMINATE"
        )
    )

    assert len(
        indeterminate,
    ) == 5

    assert all(
        rule["initial_evidence_ids"] == []
        and rule["final_evidence_ids"] == []
        for rule in indeterminate
    )


def test_serializer_preserves_disputed_context_identity() -> None:
    document = json.loads(
        create_payload(),
    )

    assert document["disputed_dimension_ids"] == [
        "CTX-RETAILER-001",
    ]


def test_serializer_preserves_context_policy_identity() -> None:
    document = json.loads(
        create_payload(),
    )

    assert document["context_policy_ids"] == [
        "CP01-CONTEXTUAL-ADAPTATION",
    ]


def test_serializer_preserves_unestablished_claim_boundaries() -> None:
    document = json.loads(
        create_payload(),
    )

    assert document["customer_acceptance_status"] == (
        "NOT_ESTABLISHED"
    )

    assert document["commercial_impact_status"] == (
        "NOT_ESTABLISHED"
    )

    assert document["independent_intervention_status"] == (
        "NOT_ESTABLISHED"
    )


def test_serializer_is_deterministic_for_same_report() -> None:
    report = create_report()

    first = serialize_retail_context_assessment_report(
        report=report,
    )

    second = serialize_retail_context_assessment_report(
        report=report,
    )

    assert first == second


def test_serializer_orders_json_keys_deterministically() -> None:
    payload = create_payload()

    document = json.loads(
        payload,
    )

    reconstructed = json.dumps(
        document,
        sort_keys=True,
        separators=(
            ",",
            ":",
        ),
        ensure_ascii=False,
        allow_nan=False,
    )

    assert payload == reconstructed


def test_serializer_uses_compact_json_separators() -> None:
    payload = create_payload()

    assert "\\n" not in payload

    assert '": ' not in payload


def test_serializer_preserves_unicode_without_ascii_escaping() -> None:
    original = create_report()

    report = replace(
        original,
        case_id="CASO-NIÑEZ-001",
    )

    payload = serialize_retail_context_assessment_report(
        report=report,
    )

    assert "CASO-NIÑEZ-001" in payload

    assert json.loads(
        payload,
    )["case_id"] == (
        "CASO-NIÑEZ-001"
    )


def test_serializer_rejects_invalid_report() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "report must be a "
            "RetailContextAssessmentReport"
        ),
    ):
        serialize_retail_context_assessment_report(
            report="REPORT-001",
        )


def test_serializer_does_not_mutate_source_report() -> None:
    report = create_report()

    original_rules = report.rules
    original_evidence = report.evidence_ids

    serialize_retail_context_assessment_report(
        report=report,
    )

    assert report.rules is original_rules

    assert report.evidence_ids is original_evidence


def test_serializer_excludes_sensitive_locator_patterns() -> None:
    payload = create_payload()

    forbidden = (
        "/Users/",
        "file:",
        "http:",
        "https:",
        "PRIVATE KEY",
    )

    assert all(
        marker not in payload
        for marker in forbidden
    )


def test_serializer_preserves_complete_change_distribution() -> None:
    document = json.loads(
        create_payload(),
    )

    assert document["total_improved_count"] == 14

    assert (
        document["directly_observed_improved_count"]
        == 9
    )

    assert document["derived_improved_count"] == 5

    assert document["unchanged_count"] == 16

    assert document["regressed_count"] == 0

    assert document["indeterminate_count"] == 5
