from dataclasses import replace
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

from sp001.services.retail_context_assessment_report_artifact import (
    RetailContextAssessmentReportArtifact,
    build_retail_context_assessment_report_artifact,
)
from sp001.services.retail_context_assessment_report_artifact_verification import (
    verify_retail_context_assessment_report_artifact,
)
from sp001.services.retail_context_assessment_report_digest import (
    RetailContextAssessmentReportDigest,
)


def load_artifact_tests():
    path = (
        Path(__file__).resolve().parent
        / "test_retail_context_assessment_report_artifact.py"
    )

    specification = importlib.util.spec_from_file_location(
        "rcp001_tcp_sears_exchange_artifact",
        path,
    )

    if (
        specification is None
        or specification.loader is None
    ):
        raise RuntimeError(
            "canonical retail exchange artifact unavailable"
        )

    module = importlib.util.module_from_spec(
        specification,
    )

    specification.loader.exec_module(
        module,
    )

    return module


ARTIFACT = load_artifact_tests()


def create_artifact():
    return ARTIFACT.create_artifact()


def test_verification_accepts_valid_exchange_artifact() -> None:
    artifact = create_artifact()

    assert (
        verify_retail_context_assessment_report_artifact(
            artifact=artifact,
        )
        is True
    )


def test_verification_requires_no_original_report_object() -> None:
    original = create_artifact()

    received = RetailContextAssessmentReportArtifact(
        payload=original.payload,
        digest=original.digest,
        media_type=original.media_type,
    )

    assert (
        verify_retail_context_assessment_report_artifact(
            artifact=received,
        )
        is True
    )


def test_verification_rejects_modified_payload() -> None:
    original = create_artifact()

    document = json.loads(
        original.payload,
    )

    document["case_id"] = (
        "VCR-001-CASE-002"
    )

    modified = replace(
        original,
        payload=json.dumps(
            document,
            sort_keys=True,
            separators=(
                ",",
                ":",
            ),
            ensure_ascii=False,
        ),
    )

    assert (
        verify_retail_context_assessment_report_artifact(
            artifact=modified,
        )
        is False
    )


def test_verification_rejects_modified_json_formatting() -> None:
    original = create_artifact()

    document = json.loads(
        original.payload,
    )

    formatted = json.dumps(
        document,
        sort_keys=True,
        indent=2,
        ensure_ascii=False,
    )

    modified = replace(
        original,
        payload=formatted,
    )

    assert (
        verify_retail_context_assessment_report_artifact(
            artifact=modified,
        )
        is False
    )


def test_verification_rejects_modified_digest_value() -> None:
    original = create_artifact()

    modified_digest = replace(
        original.digest,
        value="0" * 64,
    )

    modified = replace(
        original,
        digest=modified_digest,
    )

    assert (
        verify_retail_context_assessment_report_artifact(
            artifact=modified,
        )
        is False
    )


def test_verification_rejects_invalid_artifact_type() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "artifact must be a "
            "RetailContextAssessmentReportArtifact"
        ),
    ):
        verify_retail_context_assessment_report_artifact(
            artifact="ARTIFACT-001",
        )


def test_verification_rejects_unsupported_media_type() -> None:
    artifact = replace(
        create_artifact(),
        media_type="text/plain",
    )

    with pytest.raises(
        ValueError,
        match=(
            "artifact media_type must be application/json"
        ),
    ):
        verify_retail_context_assessment_report_artifact(
            artifact=artifact,
        )


@pytest.mark.parametrize(
    "invalid_payload",
    (
        None,
        b"{}",
        123,
    ),
)
def test_verification_rejects_non_text_payload(
    invalid_payload,
) -> None:
    artifact = replace(
        create_artifact(),
        payload=invalid_payload,
    )

    with pytest.raises(
        TypeError,
        match=(
            "artifact payload must be a string"
        ),
    ):
        verify_retail_context_assessment_report_artifact(
            artifact=artifact,
        )


@pytest.mark.parametrize(
    "invalid_payload",
    (
        "",
        "   ",
    ),
)
def test_verification_rejects_empty_payload(
    invalid_payload: str,
) -> None:
    artifact = replace(
        create_artifact(),
        payload=invalid_payload,
    )

    with pytest.raises(
        ValueError,
        match=(
            "artifact payload must not be empty"
        ),
    ):
        verify_retail_context_assessment_report_artifact(
            artifact=artifact,
        )


def test_verification_rejects_invalid_json_payload() -> None:
    artifact = replace(
        create_artifact(),
        payload="{invalid-json",
    )

    with pytest.raises(
        ValueError,
        match=(
            "artifact payload must contain valid JSON"
        ),
    ):
        verify_retail_context_assessment_report_artifact(
            artifact=artifact,
        )


@pytest.mark.parametrize(
    "payload",
    (
        "[]",
        "null",
        '"text"',
        "123",
        "true",
    ),
)
def test_verification_rejects_non_object_json_payload(
    payload: str,
) -> None:
    artifact = replace(
        create_artifact(),
        payload=payload,
    )

    with pytest.raises(
        ValueError,
        match=(
            "artifact payload must contain a JSON object"
        ),
    ):
        verify_retail_context_assessment_report_artifact(
            artifact=artifact,
        )


def test_verification_rejects_invalid_digest_type() -> None:
    artifact = replace(
        create_artifact(),
        digest="DIGEST-001",
    )

    with pytest.raises(
        TypeError,
        match=(
            "artifact digest must be a "
            "RetailContextAssessmentReportDigest"
        ),
    ):
        verify_retail_context_assessment_report_artifact(
            artifact=artifact,
        )


def test_verification_rejects_unsupported_digest_algorithm() -> None:
    original = create_artifact()

    digest = replace(
        original.digest,
        algorithm="SHA-512",
    )

    artifact = replace(
        original,
        digest=digest,
    )

    with pytest.raises(
        ValueError,
        match=(
            "digest algorithm must be SHA-256"
        ),
    ):
        verify_retail_context_assessment_report_artifact(
            artifact=artifact,
        )


def test_verification_rejects_unsupported_digest_encoding() -> None:
    original = create_artifact()

    digest = replace(
        original.digest,
        encoding="UTF-16",
    )

    artifact = replace(
        original,
        digest=digest,
    )

    with pytest.raises(
        ValueError,
        match=(
            "digest encoding must be UTF-8"
        ),
    ):
        verify_retail_context_assessment_report_artifact(
            artifact=artifact,
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
    original = create_artifact()

    digest = replace(
        original.digest,
        value=invalid_value,
    )

    artifact = replace(
        original,
        digest=digest,
    )

    with pytest.raises(
        ValueError,
        match=(
            "digest value must contain "
            "64 lowercase hexadecimal characters"
        ),
    ):
        verify_retail_context_assessment_report_artifact(
            artifact=artifact,
        )


def test_verification_hashes_exact_received_utf8_payload() -> None:
    original = create_artifact()

    document = json.loads(
        original.payload,
    )

    document["case_id"] = (
        "CASO-NIÑEZ-001"
    )

    payload = json.dumps(
        document,
        sort_keys=True,
        separators=(
            ",",
            ":",
        ),
        ensure_ascii=False,
    )

    digest = RetailContextAssessmentReportDigest(
        algorithm="SHA-256",
        encoding="UTF-8",
        value=hashlib.sha256(
            payload.encode(
                "utf-8",
            )
        ).hexdigest(),
    )

    received = RetailContextAssessmentReportArtifact(
        payload=payload,
        digest=digest,
        media_type="application/json",
    )

    assert (
        verify_retail_context_assessment_report_artifact(
            artifact=received,
        )
        is True
    )


def test_verification_does_not_require_report_reconstruction() -> None:
    original = create_artifact()

    payload = original.payload

    digest = RetailContextAssessmentReportDigest(
        algorithm=original.digest.algorithm,
        encoding=original.digest.encoding,
        value=original.digest.value,
    )

    received = RetailContextAssessmentReportArtifact(
        payload=payload,
        digest=digest,
        media_type="application/json",
    )

    assert (
        verify_retail_context_assessment_report_artifact(
            artifact=received,
        )
        is True
    )


def test_verification_returns_boolean_without_authenticity_claim() -> None:
    result = verify_retail_context_assessment_report_artifact(
        artifact=create_artifact(),
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


def test_verification_preserves_unsupported_commercial_claims() -> None:
    artifact = create_artifact()

    assert (
        verify_retail_context_assessment_report_artifact(
            artifact=artifact,
        )
        is True
    )

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


def test_verification_does_not_mutate_exchange_artifact() -> None:
    artifact = create_artifact()

    original_payload = artifact.payload
    original_digest = artifact.digest

    verify_retail_context_assessment_report_artifact(
        artifact=artifact,
    )

    assert artifact.payload is original_payload

    assert artifact.digest is original_digest
