from dataclasses import replace
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

from sp001.services.retail_context_assessment_report_artifact import (
    RetailContextAssessmentReportArtifact,
)
from sp001.services.retail_context_assessment_report_artifact_verification import (
    verify_retail_context_assessment_report_artifact,
)
from sp001.services.retail_context_assessment_report_digest import (
    RetailContextAssessmentReportDigest,
)


def load_artifact_verification_tests():
    path = (
        Path(__file__).resolve().parent
        / "test_retail_context_assessment_report_artifact_verification.py"
    )

    specification = importlib.util.spec_from_file_location(
        "rcp001_retail_artifact_verification_for_structural_integration",
        path,
    )

    if (
        specification is None
        or specification.loader is None
    ):
        raise RuntimeError(
            "retail artifact verification fixtures unavailable"
        )

    module = importlib.util.module_from_spec(
        specification,
    )

    specification.loader.exec_module(
        module,
    )

    return module


ARTIFACT = load_artifact_verification_tests()


def create_artifact():
    return ARTIFACT.create_artifact()


def artifact_with_payload(
    payload: str,
) -> RetailContextAssessmentReportArtifact:
    digest = RetailContextAssessmentReportDigest(
        algorithm="SHA-256",
        encoding="UTF-8",
        value=hashlib.sha256(
            payload.encode(
                "utf-8",
            )
        ).hexdigest(),
    )

    return RetailContextAssessmentReportArtifact(
        payload=payload,
        digest=digest,
        media_type="application/json",
    )


def modified_artifact(
    modifier,
) -> RetailContextAssessmentReportArtifact:
    original = create_artifact()

    document = json.loads(
        original.payload,
    )

    modifier(
        document,
    )

    payload = json.dumps(
        document,
        sort_keys=True,
        separators=(
            ",",
            ":",
        ),
        ensure_ascii=False,
        allow_nan=False,
    )

    return artifact_with_payload(
        payload,
    )


def test_valid_canonical_artifact_passes_integrity_and_structure() -> None:
    artifact = create_artifact()

    assert (
        verify_retail_context_assessment_report_artifact(
            artifact=artifact,
        )
        is True
    )


def test_empty_json_with_matching_digest_is_rejected() -> None:
    artifact = artifact_with_payload(
        "{}",
    )

    with pytest.raises(
        ValueError,
        match="missing required report fields",
    ):
        verify_retail_context_assessment_report_artifact(
            artifact=artifact,
        )


@pytest.mark.parametrize(
    "field",
    (
        "case_id",
        "snapshot_id",
        "snapshot_version",
        "rules",
        "total_rules",
    ),
)
def test_matching_digest_cannot_validate_missing_report_field(
    field: str,
) -> None:
    artifact = modified_artifact(
        lambda document: document.pop(
            field,
        )
    )

    with pytest.raises(
        ValueError,
        match="missing required report fields",
    ):
        verify_retail_context_assessment_report_artifact(
            artifact=artifact,
        )


def test_matching_digest_cannot_validate_unexpected_report_field() -> None:
    artifact = modified_artifact(
        lambda document: document.update(
            {
                "invented_authority": "VERIFIED",
            }
        )
    )

    with pytest.raises(
        ValueError,
        match="unexpected report fields",
    ):
        verify_retail_context_assessment_report_artifact(
            artifact=artifact,
        )


@pytest.mark.parametrize(
    "field",
    (
        "case_id",
        "snapshot_id",
    ),
)
def test_matching_digest_cannot_validate_empty_report_identity(
    field: str,
) -> None:
    artifact = modified_artifact(
        lambda document: document.update(
            {
                field: "   ",
            }
        )
    )

    with pytest.raises(
        ValueError,
        match=f"{field} must not be empty",
    ):
        verify_retail_context_assessment_report_artifact(
            artifact=artifact,
        )


@pytest.mark.parametrize(
    "version",
    (
        0,
        -1,
        True,
        "1",
    ),
)
def test_matching_digest_cannot_validate_invalid_snapshot_version(
    version,
) -> None:
    artifact = modified_artifact(
        lambda document: document.update(
            {
                "snapshot_version": version,
            }
        )
    )

    with pytest.raises(
        ValueError,
        match="snapshot_version must be a positive integer",
    ):
        verify_retail_context_assessment_report_artifact(
            artifact=artifact,
        )


@pytest.mark.parametrize(
    "field",
    (
        "total_rules",
        "derived_count",
        "indeterminate_count",
    ),
)
def test_matching_digest_cannot_validate_negative_count(
    field: str,
) -> None:
    artifact = modified_artifact(
        lambda document: document.update(
            {
                field: -1,
            }
        )
    )

    with pytest.raises(
        ValueError,
        match=f"{field} must be a non-negative integer",
    ):
        verify_retail_context_assessment_report_artifact(
            artifact=artifact,
        )


def test_matching_digest_cannot_validate_boolean_count() -> None:
    artifact = modified_artifact(
        lambda document: document.update(
            {
                "total_rules": True,
            }
        )
    )

    with pytest.raises(
        ValueError,
        match="total_rules must be a non-negative integer",
    ):
        verify_retail_context_assessment_report_artifact(
            artifact=artifact,
        )


def test_matching_digest_cannot_validate_non_array_rules() -> None:
    artifact = modified_artifact(
        lambda document: document.update(
            {
                "rules": {},
            }
        )
    )

    with pytest.raises(
        ValueError,
        match="rules must be a JSON array",
    ):
        verify_retail_context_assessment_report_artifact(
            artifact=artifact,
        )


def test_matching_digest_cannot_validate_missing_rule_field() -> None:
    def remove_rule_field(document):
        document["rules"][0].pop(
            "rule_id",
        )

    artifact = modified_artifact(
        remove_rule_field,
    )

    with pytest.raises(
        ValueError,
        match="missing required rule fields",
    ):
        verify_retail_context_assessment_report_artifact(
            artifact=artifact,
        )


def test_matching_digest_cannot_validate_unexpected_rule_field() -> None:
    def add_rule_field(document):
        document["rules"][0][
            "invented_signature"
        ] = "VERIFIED"

    artifact = modified_artifact(
        add_rule_field,
    )

    with pytest.raises(
        ValueError,
        match="unexpected rule fields",
    ):
        verify_retail_context_assessment_report_artifact(
            artifact=artifact,
        )


@pytest.mark.parametrize(
    ("field", "message"),
    (
        (
            "initial_status",
            "initial_status must be a valid RuleObservationStatus",
        ),
        (
            "final_status",
            "final_status must be a valid RuleObservationStatus",
        ),
        (
            "change_status",
            "change_status must be a valid ObservationChangeStatus",
        ),
        (
            "provenance_type",
            "provenance_type must be a valid RuleProvenanceType",
        ),
    ),
)
def test_matching_digest_cannot_validate_unknown_rule_vocabulary(
    field: str,
    message: str,
) -> None:
    def replace_vocabulary(document):
        document["rules"][0][
            field
        ] = "INVENTED_VALUE"

    artifact = modified_artifact(
        replace_vocabulary,
    )

    with pytest.raises(
        ValueError,
        match=message,
    ):
        verify_retail_context_assessment_report_artifact(
            artifact=artifact,
        )


@pytest.mark.parametrize(
    "field",
    (
        "customer_acceptance_status",
        "commercial_impact_status",
        "independent_intervention_status",
    ),
)
def test_matching_digest_cannot_validate_unsupported_commercial_claim(
    field: str,
) -> None:
    artifact = modified_artifact(
        lambda document: document.update(
            {
                field: "VERIFIED",
            }
        )
    )

    with pytest.raises(
        ValueError,
        match=f"{field} must remain NOT_ESTABLISHED",
    ):
        verify_retail_context_assessment_report_artifact(
            artifact=artifact,
        )


def test_digest_mismatch_returns_false_before_structural_validation() -> None:
    original = create_artifact()

    modified = replace(
        original,
        payload="{}",
    )

    assert (
        verify_retail_context_assessment_report_artifact(
            artifact=modified,
        )
        is False
    )


def test_structural_verification_does_not_mutate_artifact() -> None:
    artifact = create_artifact()

    original_payload = artifact.payload
    original_digest = artifact.digest

    assert (
        verify_retail_context_assessment_report_artifact(
            artifact=artifact,
        )
        is True
    )

    assert artifact.payload == original_payload
    assert artifact.digest == original_digest


def test_structural_verification_does_not_claim_authenticity() -> None:
    artifact = create_artifact()

    result = verify_retail_context_assessment_report_artifact(
        artifact=artifact,
    )

    assert isinstance(
        result,
        bool,
    )

    assert result is True

    assert not hasattr(
        artifact,
        "signature",
    )

    assert not hasattr(
        artifact,
        "authority",
    )
