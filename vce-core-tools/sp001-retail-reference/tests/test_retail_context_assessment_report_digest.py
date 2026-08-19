from dataclasses import FrozenInstanceError, replace
import hashlib
import importlib.util
from pathlib import Path
import re

import pytest

from sp001.services.retail_context_assessment_report_digest import (
    RetailContextAssessmentReportDigest,
    digest_retail_context_assessment_report,
)
from sp001.services.retail_context_assessment_report_serialization import (
    serialize_retail_context_assessment_report,
)


def load_report_tests():
    path = (
        Path(__file__).resolve().parent
        / "test_retail_context_assessment_report.py"
    )

    specification = importlib.util.spec_from_file_location(
        "rcp001_tcp_sears_digest_report",
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


def create_digest():
    return digest_retail_context_assessment_report(
        report=create_report(),
    )


def test_digest_returns_immutable_content_identity() -> None:
    digest = create_digest()

    assert isinstance(
        digest,
        RetailContextAssessmentReportDigest,
    )


def test_digest_declares_sha256_algorithm() -> None:
    digest = create_digest()

    assert digest.algorithm == "SHA-256"


def test_digest_declares_utf8_encoding() -> None:
    digest = create_digest()

    assert digest.encoding == "UTF-8"


def test_digest_contains_exactly_sixty_four_hexadecimal_characters() -> None:
    digest = create_digest()

    assert re.fullmatch(
        r"[0-9a-f]{64}",
        digest.value,
    )


def test_digest_matches_independent_sha256_calculation() -> None:
    report = create_report()

    payload = serialize_retail_context_assessment_report(
        report=report,
    )

    expected = hashlib.sha256(
        payload.encode(
            "utf-8",
        )
    ).hexdigest()

    digest = digest_retail_context_assessment_report(
        report=report,
    )

    assert digest.value == expected


def test_digest_is_deterministic_for_same_report() -> None:
    report = create_report()

    first = digest_retail_context_assessment_report(
        report=report,
    )

    second = digest_retail_context_assessment_report(
        report=report,
    )

    assert first == second


def test_digest_is_deterministic_across_equivalent_reports() -> None:
    first = digest_retail_context_assessment_report(
        report=create_report(),
    )

    second = digest_retail_context_assessment_report(
        report=create_report(),
    )

    assert first.value == second.value


def test_digest_changes_when_case_identity_changes() -> None:
    report = create_report()

    modified = replace(
        report,
        case_id="VCR-001-CASE-002",
    )

    original_digest = digest_retail_context_assessment_report(
        report=report,
    )

    modified_digest = digest_retail_context_assessment_report(
        report=modified,
    )

    assert original_digest.value != modified_digest.value


def test_digest_changes_when_snapshot_version_changes() -> None:
    report = create_report()

    modified = replace(
        report,
        snapshot_version=2,
    )

    original_digest = digest_retail_context_assessment_report(
        report=report,
    )

    modified_digest = digest_retail_context_assessment_report(
        report=modified,
    )

    assert original_digest.value != modified_digest.value


def test_digest_changes_when_evidence_identity_changes() -> None:
    report = create_report()

    modified = replace(
        report,
        evidence_ids=(
            "ART-002",
            "ART-004",
        ),
    )

    original_digest = digest_retail_context_assessment_report(
        report=report,
    )

    modified_digest = digest_retail_context_assessment_report(
        report=modified,
    )

    assert original_digest.value != modified_digest.value


def test_digest_changes_when_context_policy_changes() -> None:
    report = create_report()

    modified = replace(
        report,
        context_policy_ids=(
            "CP02-ALTERNATIVE-ADAPTATION",
        ),
    )

    original_digest = digest_retail_context_assessment_report(
        report=report,
    )

    modified_digest = digest_retail_context_assessment_report(
        report=modified,
    )

    assert original_digest.value != modified_digest.value


def test_digest_changes_when_rule_order_changes() -> None:
    report = create_report()

    modified = replace(
        report,
        rules=tuple(
            reversed(
                report.rules,
            )
        ),
    )

    original_digest = digest_retail_context_assessment_report(
        report=report,
    )

    modified_digest = digest_retail_context_assessment_report(
        report=modified,
    )

    assert original_digest.value != modified_digest.value


def test_digest_changes_when_claim_boundary_changes() -> None:
    report = create_report()

    modified = replace(
        report,
        customer_acceptance_status=(
            "DOCUMENTALLY_VERIFIED"
        ),
    )

    original_digest = digest_retail_context_assessment_report(
        report=report,
    )

    modified_digest = digest_retail_context_assessment_report(
        report=modified,
    )

    assert original_digest.value != modified_digest.value


def test_digest_preserves_unicode_utf8_semantics() -> None:
    report = replace(
        create_report(),
        case_id="CASO-NIÑEZ-001",
    )

    payload = serialize_retail_context_assessment_report(
        report=report,
    )

    expected = hashlib.sha256(
        payload.encode(
            "utf-8",
        )
    ).hexdigest()

    digest = digest_retail_context_assessment_report(
        report=report,
    )

    assert digest.value == expected


def test_digest_rejects_invalid_report() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "report must be a "
            "RetailContextAssessmentReport"
        ),
    ):
        digest_retail_context_assessment_report(
            report="REPORT-001",
        )


def test_digest_result_is_immutable() -> None:
    digest = create_digest()

    with pytest.raises(
        FrozenInstanceError,
    ):
        digest.value = "0" * 64


def test_digest_does_not_claim_signature_or_authority() -> None:
    digest = create_digest()

    assert not hasattr(
        digest,
        "signature",
    )

    assert not hasattr(
        digest,
        "signer",
    )

    assert not hasattr(
        digest,
        "authority",
    )


def test_digest_does_not_claim_customer_acceptance_or_revenue() -> None:
    digest = create_digest()

    assert not hasattr(
        digest,
        "customer_acceptance",
    )

    assert not hasattr(
        digest,
        "commercial_impact",
    )

    assert not hasattr(
        digest,
        "revenue",
    )


def test_digest_does_not_mutate_source_report() -> None:
    report = create_report()

    original_rules = report.rules
    original_evidence = report.evidence_ids

    digest_retail_context_assessment_report(
        report=report,
    )

    assert report.rules is original_rules

    assert report.evidence_ids is original_evidence


def test_digest_preserves_unestablished_claims_in_source_report() -> None:
    report = create_report()

    digest_retail_context_assessment_report(
        report=report,
    )

    assert report.customer_acceptance_status == (
        "NOT_ESTABLISHED"
    )

    assert report.commercial_impact_status == (
        "NOT_ESTABLISHED"
    )

    assert report.independent_intervention_status == (
        "NOT_ESTABLISHED"
    )
