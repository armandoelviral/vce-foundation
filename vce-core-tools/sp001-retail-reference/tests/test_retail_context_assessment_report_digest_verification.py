from dataclasses import replace
import importlib.util
from pathlib import Path

import pytest

from sp001.services.retail_context_assessment_report_digest import (
    RetailContextAssessmentReportDigest,
    digest_retail_context_assessment_report,
)
from sp001.services.retail_context_assessment_report_digest_verification import (
    verify_retail_context_assessment_report_digest,
)


def load_report_tests():
    path = (
        Path(__file__).resolve().parent
        / "test_retail_context_assessment_report.py"
    )

    specification = importlib.util.spec_from_file_location(
        "rcp001_tcp_sears_digest_verification_report",
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


def create_digest(
    report,
) -> RetailContextAssessmentReportDigest:
    return digest_retail_context_assessment_report(
        report=report,
    )


def test_verification_accepts_matching_report_digest() -> None:
    report = create_report()

    digest = create_digest(
        report,
    )

    assert (
        verify_retail_context_assessment_report_digest(
            report=report,
            digest=digest,
        )
        is True
    )


def test_verification_rejects_modified_case_identity() -> None:
    original = create_report()

    digest = create_digest(
        original,
    )

    modified = replace(
        original,
        case_id="VCR-001-CASE-002",
    )

    assert (
        verify_retail_context_assessment_report_digest(
            report=modified,
            digest=digest,
        )
        is False
    )


def test_verification_rejects_modified_snapshot_version() -> None:
    original = create_report()

    digest = create_digest(
        original,
    )

    modified = replace(
        original,
        snapshot_version=2,
    )

    assert (
        verify_retail_context_assessment_report_digest(
            report=modified,
            digest=digest,
        )
        is False
    )


def test_verification_rejects_modified_evidence_identity() -> None:
    original = create_report()

    digest = create_digest(
        original,
    )

    modified = replace(
        original,
        evidence_ids=(
            "ART-002",
            "ART-004",
        ),
    )

    assert (
        verify_retail_context_assessment_report_digest(
            report=modified,
            digest=digest,
        )
        is False
    )


def test_verification_rejects_modified_rule_order() -> None:
    original = create_report()

    digest = create_digest(
        original,
    )

    modified = replace(
        original,
        rules=tuple(
            reversed(
                original.rules,
            )
        ),
    )

    assert (
        verify_retail_context_assessment_report_digest(
            report=modified,
            digest=digest,
        )
        is False
    )


def test_verification_rejects_modified_context_policy() -> None:
    original = create_report()

    digest = create_digest(
        original,
    )

    modified = replace(
        original,
        context_policy_ids=(
            "CP02-ALTERNATIVE-ADAPTATION",
        ),
    )

    assert (
        verify_retail_context_assessment_report_digest(
            report=modified,
            digest=digest,
        )
        is False
    )


def test_verification_rejects_modified_claim_boundary() -> None:
    original = create_report()

    digest = create_digest(
        original,
    )

    modified = replace(
        original,
        customer_acceptance_status=(
            "DOCUMENTALLY_VERIFIED"
        ),
    )

    assert (
        verify_retail_context_assessment_report_digest(
            report=modified,
            digest=digest,
        )
        is False
    )


def test_verification_rejects_nonmatching_valid_digest() -> None:
    report = create_report()

    digest = RetailContextAssessmentReportDigest(
        algorithm="SHA-256",
        encoding="UTF-8",
        value="0" * 64,
    )

    assert (
        verify_retail_context_assessment_report_digest(
            report=report,
            digest=digest,
        )
        is False
    )


def test_verification_rejects_invalid_report_type() -> None:
    report = create_report()

    digest = create_digest(
        report,
    )

    with pytest.raises(
        TypeError,
        match=(
            "report must be a "
            "RetailContextAssessmentReport"
        ),
    ):
        verify_retail_context_assessment_report_digest(
            report="REPORT-001",
            digest=digest,
        )


def test_verification_rejects_invalid_digest_type() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "digest must be a "
            "RetailContextAssessmentReportDigest"
        ),
    ):
        verify_retail_context_assessment_report_digest(
            report=create_report(),
            digest="DIGEST-001",
        )


def test_verification_rejects_unsupported_digest_algorithm() -> None:
    digest = RetailContextAssessmentReportDigest(
        algorithm="SHA-512",
        encoding="UTF-8",
        value="0" * 64,
    )

    with pytest.raises(
        ValueError,
        match=(
            "digest algorithm must be SHA-256"
        ),
    ):
        verify_retail_context_assessment_report_digest(
            report=create_report(),
            digest=digest,
        )


def test_verification_rejects_unsupported_digest_encoding() -> None:
    digest = RetailContextAssessmentReportDigest(
        algorithm="SHA-256",
        encoding="UTF-16",
        value="0" * 64,
    )

    with pytest.raises(
        ValueError,
        match=(
            "digest encoding must be UTF-8"
        ),
    ):
        verify_retail_context_assessment_report_digest(
            report=create_report(),
            digest=digest,
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        "",
        "0" * 63,
        "0" * 65,
        "g" * 64,
        "A" * 64,
        None,
    ),
)
def test_verification_rejects_invalid_digest_format(
    invalid_value,
) -> None:
    digest = RetailContextAssessmentReportDigest(
        algorithm="SHA-256",
        encoding="UTF-8",
        value=invalid_value,
    )

    with pytest.raises(
        ValueError,
        match=(
            "digest value must contain "
            "64 lowercase hexadecimal characters"
        ),
    ):
        verify_retail_context_assessment_report_digest(
            report=create_report(),
            digest=digest,
        )


def test_verification_accepts_equivalent_independently_created_report() -> None:
    original = create_report()

    equivalent = create_report()

    digest = create_digest(
        original,
    )

    assert (
        verify_retail_context_assessment_report_digest(
            report=equivalent,
            digest=digest,
        )
        is True
    )


def test_verification_preserves_unicode_utf8_identity() -> None:
    report = replace(
        create_report(),
        case_id="CASO-NIÑEZ-001",
    )

    digest = create_digest(
        report,
    )

    assert (
        verify_retail_context_assessment_report_digest(
            report=report,
            digest=digest,
        )
        is True
    )


def test_verification_returns_boolean_without_authority_claim() -> None:
    report = create_report()

    digest = create_digest(
        report,
    )

    result = verify_retail_context_assessment_report_digest(
        report=report,
        digest=digest,
    )

    assert isinstance(
        result,
        bool,
    )

    assert not hasattr(
        result,
        "signature",
    )

    assert not hasattr(
        result,
        "authority",
    )


def test_verification_does_not_mutate_report_or_digest() -> None:
    report = create_report()

    digest = create_digest(
        report,
    )

    original_rules = report.rules
    original_digest_value = digest.value

    verify_retail_context_assessment_report_digest(
        report=report,
        digest=digest,
    )

    assert report.rules is original_rules

    assert digest.value == original_digest_value


def test_verification_preserves_unestablished_commercial_claims() -> None:
    report = create_report()

    digest = create_digest(
        report,
    )

    assert (
        verify_retail_context_assessment_report_digest(
            report=report,
            digest=digest,
        )
        is True
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
