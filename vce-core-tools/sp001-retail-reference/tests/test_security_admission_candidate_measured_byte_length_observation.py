from dataclasses import FrozenInstanceError, fields, replace
from datetime import datetime, timedelta, timezone
import ast
import inspect

import pytest

from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
)
from sp001.contracts.security_admission_candidate_identity import (
    SecurityAdmissionCandidateIdentity,
)
from sp001.contracts.security_admission_candidate_measured_byte_length_observation import (
    SecurityAdmissionCandidateMeasuredByteLengthObservation,
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
    SecurityAdmissionCandidateMeasuredByteLengthObservation
):
    return SecurityAdmissionCandidateMeasuredByteLengthObservation(
        observation_id="observation-001",
        observation_version=1,
        candidate_identity=create_candidate(),
        verification_procedure_identity=create_procedure(),
        measured_byte_length=4096,
        observed_at=datetime(2026, 9, 11, tzinfo=timezone.utc),
    )


def test_measured_byte_length_observation_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(
            SecurityAdmissionCandidateMeasuredByteLengthObservation
        )
    ) == (
        "observation_id",
        "observation_version",
        "candidate_identity",
        "verification_procedure_identity",
        "measured_byte_length",
        "observed_at",
    )


def test_measured_byte_length_observation_is_immutable() -> None:
    observation = create_observation()

    with pytest.raises(FrozenInstanceError):
        observation.measured_byte_length = 1  # type: ignore[misc]


def test_measured_byte_length_observation_uses_slots() -> None:
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


@pytest.mark.parametrize(
    "value",
    [True, False, None, 1.0, "1", object()],
)
def test_measured_byte_length_requires_strict_integer(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="measured_byte_length must be an integer",
    ):
        replace(
            create_observation(),
            measured_byte_length=value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("value", [-1, -(10**30)])
def test_measured_byte_length_must_not_be_negative(
    value: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="measured_byte_length must not be negative",
    ):
        replace(
            create_observation(),
            measured_byte_length=value,
        )


def test_zero_is_an_explicit_measured_byte_length() -> None:
    observation = replace(
        create_observation(),
        measured_byte_length=0,
    )

    assert observation.measured_byte_length == 0


def test_arbitrary_size_measurement_is_preserved_exactly() -> None:
    value = 10**1000
    observation = replace(
        create_observation(),
        measured_byte_length=value,
    )

    assert observation.measured_byte_length == value


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
        SecurityAdmissionCandidateMeasuredByteLengthObservation(
            observation_id="observation-001",
            observation_version=1,
            candidate_identity=create_candidate(),
            verification_procedure_identity=create_procedure(),
            measured_byte_length=4096,
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
        measured_byte_length=4097,
    ) != observation
    assert replace(
        observation,
        observed_at=datetime(2026, 9, 12, tzinfo=timezone.utc),
    ) != observation


def test_declaration_comparison_and_policy_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(
            SecurityAdmissionCandidateMeasuredByteLengthObservation
        )
    }

    assert names.isdisjoint(
        {
            "metadata_identity",
            "declared_byte_length",
            "length_matches",
            "maximum_byte_length",
            "allowed_byte_length",
            "oversize",
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


def test_contract_imports_no_measurement_or_external_capability() -> None:
    module = inspect.getmodule(
        SecurityAdmissionCandidateMeasuredByteLengthObservation
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
        SecurityAdmissionCandidateMeasuredByteLengthObservation
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    functions = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    assert functions == {"__post_init__"}
