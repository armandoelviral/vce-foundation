from dataclasses import FrozenInstanceError, fields, replace
from datetime import datetime, timedelta, timezone
import ast
import inspect

import pytest

from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
)
from sp001.contracts.security_admission_candidate_detected_media_type_observation import (
    SecurityAdmissionCandidateDetectedMediaTypeObservation,
)
from sp001.contracts.security_admission_candidate_identity import (
    SecurityAdmissionCandidateIdentity,
)
from sp001.contracts.security_admission_metadata_verification_procedure_identity import (
    SecurityAdmissionMetadataVerificationProcedureIdentity,
)


def create_digest(value: str) -> KnowledgeContentDigest:
    return KnowledgeContentDigest(
        algorithm="SHA-256",
        value=value,
    )


def create_candidate() -> SecurityAdmissionCandidateIdentity:
    return SecurityAdmissionCandidateIdentity(
        candidate_id="candidate-001",
        candidate_version=1,
        customer_id="customer-001",
        content_digest=create_digest("0" * 64),
    )


def create_procedure() -> (
    SecurityAdmissionMetadataVerificationProcedureIdentity
):
    return SecurityAdmissionMetadataVerificationProcedureIdentity(
        verification_procedure_id="procedure-001",
        verifier_id="metadata-verifier",
        verifier_version="v1.2.3",
        configuration_digest=create_digest("1" * 64),
    )


def create_observation() -> (
    SecurityAdmissionCandidateDetectedMediaTypeObservation
):
    return SecurityAdmissionCandidateDetectedMediaTypeObservation(
        observation_id="observation-001",
        observation_version=1,
        candidate_identity=create_candidate(),
        verification_procedure_identity=create_procedure(),
        detected_media_type="image/jpeg",
        observed_at=datetime(2026, 9, 11, tzinfo=timezone.utc),
    )


def test_detected_media_type_observation_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(
            SecurityAdmissionCandidateDetectedMediaTypeObservation
        )
    ) == (
        "observation_id",
        "observation_version",
        "candidate_identity",
        "verification_procedure_identity",
        "detected_media_type",
        "observed_at",
    )


def test_detected_media_type_observation_is_immutable() -> None:
    observation = create_observation()

    with pytest.raises(FrozenInstanceError):
        observation.detected_media_type = "image/png"  # type: ignore[misc]


def test_detected_media_type_observation_uses_slots() -> None:
    assert not hasattr(create_observation(), "__dict__")


@pytest.mark.parametrize("value", [None, 1, True, object()])
def test_observation_id_requires_string(value: object) -> None:
    with pytest.raises(
        TypeError,
        match="observation_id must be a string",
    ):
        replace(
            create_observation(),
            observation_id=value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("value", ["", " ", "\t", "\n"])
def test_observation_id_must_not_be_blank(value: str) -> None:
    with pytest.raises(
        ValueError,
        match="observation_id must not be blank",
    ):
        replace(
            create_observation(),
            observation_id=value,
        )


@pytest.mark.parametrize("value", [True, False, 1.0, "1", None])
def test_observation_version_requires_strict_integer(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="observation_version must be an integer",
    ):
        replace(
            create_observation(),
            observation_version=value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("value", [0, -1, -(10**30)])
def test_observation_version_must_be_positive(value: int) -> None:
    with pytest.raises(
        ValueError,
        match="observation_version must be positive",
    ):
        replace(
            create_observation(),
            observation_version=value,
        )


def test_candidate_identity_requires_exact_type() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "candidate_identity must be a "
            "SecurityAdmissionCandidateIdentity"
        ),
    ):
        replace(
            create_observation(),
            candidate_identity=object(),  # type: ignore[arg-type]
        )


def test_exact_candidate_identity_reference_is_preserved() -> None:
    candidate = create_candidate()
    observation = replace(
        create_observation(),
        candidate_identity=candidate,
    )

    assert observation.candidate_identity is candidate


def test_verification_procedure_identity_requires_exact_type() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "verification_procedure_identity must be a "
            "SecurityAdmissionMetadataVerificationProcedureIdentity"
        ),
    ):
        replace(
            create_observation(),
            verification_procedure_identity=object(),  # type: ignore[arg-type]
        )


def test_exact_verification_procedure_reference_is_preserved() -> None:
    procedure = create_procedure()
    observation = replace(
        create_observation(),
        verification_procedure_identity=procedure,
    )

    assert observation.verification_procedure_identity is procedure


@pytest.mark.parametrize("value", [None, 1, True, object()])
def test_detected_media_type_requires_string(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="detected_media_type must be a string",
    ):
        replace(
            create_observation(),
            detected_media_type=value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("value", ["", " ", "\t", "\n"])
def test_detected_media_type_must_not_be_blank(value: str) -> None:
    with pytest.raises(
        ValueError,
        match="detected_media_type must not be blank",
    ):
        replace(
            create_observation(),
            detected_media_type=value,
        )


@pytest.mark.parametrize(
    "value",
    [
        " IMAGE/JPEG ",
        "text/plain; charset=UTF-8",
        "application/x-future-format",
        "detector-specific unclassified value",
    ],
)
def test_detected_media_type_is_preserved_literally(
    value: str,
) -> None:
    observation = replace(
        create_observation(),
        detected_media_type=value,
    )

    assert observation.detected_media_type == value


@pytest.mark.parametrize("value", [None, "2026-09-11", 1, object()])
def test_observed_at_requires_datetime(value: object) -> None:
    with pytest.raises(
        TypeError,
        match="observed_at must be a datetime",
    ):
        replace(
            create_observation(),
            observed_at=value,  # type: ignore[arg-type]
        )


def test_observed_at_must_be_timezone_aware() -> None:
    with pytest.raises(
        ValueError,
        match="observed_at must be timezone-aware",
    ):
        replace(
            create_observation(),
            observed_at=datetime(2026, 9, 11),
        )


def test_exact_observed_at_reference_is_preserved() -> None:
    observed_at = datetime(
        2026,
        9,
        11,
        4,
        30,
        tzinfo=timezone(timedelta(hours=-6)),
    )
    observation = replace(
        create_observation(),
        observed_at=observed_at,
    )

    assert observation.observed_at is observed_at


def test_reconstructed_equal_observation_has_value_equality() -> None:
    original = create_observation()
    reconstructed = (
        SecurityAdmissionCandidateDetectedMediaTypeObservation(
            observation_id="observation-001",
            observation_version=1,
            candidate_identity=create_candidate(),
            verification_procedure_identity=create_procedure(),
            detected_media_type="image/jpeg",
            observed_at=datetime(
                2026,
                9,
                11,
                tzinfo=timezone.utc,
            ),
        )
    )

    assert reconstructed == original
    assert reconstructed is not original


def test_every_field_participates_in_observation() -> None:
    observation = create_observation()

    assert replace(
        observation,
        observation_id="observation-002",
    ) != observation
    assert replace(
        observation,
        observation_version=2,
    ) != observation
    assert replace(
        observation,
        candidate_identity=replace(
            create_candidate(),
            candidate_version=2,
        ),
    ) != observation
    assert replace(
        observation,
        verification_procedure_identity=replace(
            create_procedure(),
            verifier_version="v2",
        ),
    ) != observation
    assert replace(
        observation,
        detected_media_type="image/png",
    ) != observation
    assert replace(
        observation,
        observed_at=datetime(2026, 9, 12, tzinfo=timezone.utc),
    ) != observation


def test_declaration_comparison_and_decision_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(
            SecurityAdmissionCandidateDetectedMediaTypeObservation
        )
    }

    assert names.isdisjoint(
        {
            "metadata_identity",
            "declared_media_type",
            "media_type_matches",
            "valid_media_type",
            "allowed_media_type",
            "status",
            "decision",
            "reason",
            "authorized",
            "quarantine",
            "retention",
            "actor_identity",
            "authority_binding",
        }
    )


def test_contract_imports_no_detection_or_external_capability() -> None:
    module = inspect.getmodule(
        SecurityAdmissionCandidateDetectedMediaTypeObservation
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    roots = {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    roots.update(
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        and node.module is not None
    )

    assert roots.isdisjoint(
        {
            "mimetypes",
            "magic",
            "os",
            "pathlib",
            "subprocess",
            "sqlite3",
            "requests",
            "httpx",
            "urllib",
            "openai",
            "notion_client",
        }
    )


def test_contract_defines_validation_only() -> None:
    module = inspect.getmodule(
        SecurityAdmissionCandidateDetectedMediaTypeObservation
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    functions = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    assert functions == {"__post_init__"}
