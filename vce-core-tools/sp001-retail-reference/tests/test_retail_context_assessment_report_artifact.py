from dataclasses import FrozenInstanceError, replace
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

from sp001.services.retail_context_assessment_report_artifact import (
    RetailContextAssessmentReportArtifact,
    build_retail_context_assessment_report_artifact,
)
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
        "rcp001_tcp_sears_artifact_report",
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


def create_artifact():
    return build_retail_context_assessment_report_artifact(
        report=create_report(),
    )


def test_artifact_returns_immutable_exchange_contract() -> None:
    artifact = create_artifact()

    assert isinstance(
        artifact,
        RetailContextAssessmentReportArtifact,
    )


def test_artifact_declares_json_media_type() -> None:
    artifact = create_artifact()

    assert artifact.media_type == (
        "application/json"
    )


def test_artifact_contains_serialized_json_payload() -> None:
    artifact = create_artifact()

    assert isinstance(
        artifact.payload,
        str,
    )

    document = json.loads(
        artifact.payload,
    )

    assert isinstance(
        document,
        dict,
    )


def test_artifact_reuses_existing_deterministic_serialization() -> None:
    report = create_report()

    artifact = build_retail_context_assessment_report_artifact(
        report=report,
    )

    expected = serialize_retail_context_assessment_report(
        report=report,
    )

    assert artifact.payload == expected


def test_artifact_contains_existing_digest_contract() -> None:
    artifact = create_artifact()

    assert isinstance(
        artifact.digest,
        RetailContextAssessmentReportDigest,
    )

    assert artifact.digest.algorithm == "SHA-256"

    assert artifact.digest.encoding == "UTF-8"


def test_artifact_reuses_existing_digest_identity() -> None:
    report = create_report()

    artifact = build_retail_context_assessment_report_artifact(
        report=report,
    )

    expected = digest_retail_context_assessment_report(
        report=report,
    )

    assert artifact.digest == expected


def test_artifact_digest_matches_payload_utf8_bytes() -> None:
    artifact = create_artifact()

    expected = hashlib.sha256(
        artifact.payload.encode(
            "utf-8",
        )
    ).hexdigest()

    assert artifact.digest.value == expected


def test_artifact_is_deterministic_for_same_report() -> None:
    report = create_report()

    first = build_retail_context_assessment_report_artifact(
        report=report,
    )

    second = build_retail_context_assessment_report_artifact(
        report=report,
    )

    assert first == second


def test_artifact_preserves_case_and_snapshot_identity() -> None:
    artifact = create_artifact()

    document = json.loads(
        artifact.payload,
    )

    assert document["case_id"] == (
        "VCR-001-CASE-001"
    )

    assert document["snapshot_id"] == (
        "RCP-001-CASE-001-SNAPSHOT-001"
    )

    assert document["snapshot_version"] == 1


def test_artifact_preserves_thirty_five_canonical_rules() -> None:
    artifact = create_artifact()

    document = json.loads(
        artifact.payload,
    )

    assert document["total_rules"] == 35

    assert len(
        document["rules"],
    ) == 35


def test_artifact_preserves_opaque_evidence_identities() -> None:
    artifact = create_artifact()

    document = json.loads(
        artifact.payload,
    )

    assert document["evidence_ids"] == [
        "ART-002",
        "ART-003",
    ]


def test_artifact_preserves_disputed_retailer_context() -> None:
    artifact = create_artifact()

    document = json.loads(
        artifact.payload,
    )

    assert document["disputed_dimension_ids"] == [
        "CTX-RETAILER-001",
    ]


def test_artifact_preserves_unestablished_claim_boundaries() -> None:
    artifact = create_artifact()

    document = json.loads(
        artifact.payload,
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


def test_artifact_preserves_unicode_payload_and_digest() -> None:
    report = replace(
        create_report(),
        case_id="CASO-NIÑEZ-001",
    )

    artifact = build_retail_context_assessment_report_artifact(
        report=report,
    )

    assert "CASO-NIÑEZ-001" in artifact.payload

    expected = hashlib.sha256(
        artifact.payload.encode(
            "utf-8",
        )
    ).hexdigest()

    assert artifact.digest.value == expected


def test_artifact_rejects_invalid_report() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "report must be a "
            "RetailContextAssessmentReport"
        ),
    ):
        build_retail_context_assessment_report_artifact(
            report="REPORT-001",
        )


def test_artifact_is_immutable() -> None:
    artifact = create_artifact()

    with pytest.raises(
        FrozenInstanceError,
    ):
        artifact.payload = "{}"


def test_artifact_does_not_claim_signature_or_authority() -> None:
    artifact = create_artifact()

    assert not hasattr(
        artifact,
        "signature",
    )

    assert not hasattr(
        artifact,
        "signer",
    )

    assert not hasattr(
        artifact,
        "authority",
    )


def test_artifact_does_not_mutate_source_report() -> None:
    report = create_report()

    original_rules = report.rules
    original_evidence_ids = report.evidence_ids

    build_retail_context_assessment_report_artifact(
        report=report,
    )

    assert report.rules is original_rules

    assert report.evidence_ids is original_evidence_ids
