from dataclasses import FrozenInstanceError, fields, replace
from datetime import datetime, timezone
import ast
import inspect

import pytest

from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
)
from sp001.contracts.security_admission_candidate_declared_byte_length import (
    SecurityAdmissionCandidateDeclaredByteLength,
)
from sp001.contracts.security_admission_candidate_measured_byte_length_observation import (
    SecurityAdmissionCandidateMeasuredByteLengthObservation,
)
from sp001.contracts.security_admission_candidate_identity import (
    SecurityAdmissionCandidateIdentity,
)
from sp001.contracts.security_admission_candidate_byte_length_comparison_basis import (
    SecurityAdmissionCandidateByteLengthComparisonBasis,
)
from sp001.contracts.security_admission_candidate_metadata_identity import (
    SecurityAdmissionCandidateMetadataIdentity,
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


def create_declaration() -> SecurityAdmissionCandidateDeclaredByteLength:
    metadata = SecurityAdmissionCandidateMetadataIdentity(
        candidate_identity=create_candidate(),
        metadata_schema_id="admission-metadata",
        metadata_schema_version=1,
        metadata_digest=create_digest("1" * 64),
    )
    return SecurityAdmissionCandidateDeclaredByteLength(
        metadata_identity=metadata,
        declared_byte_length=17,
    )


def create_measurement() -> (
    SecurityAdmissionCandidateMeasuredByteLengthObservation
):
    procedure = SecurityAdmissionMetadataVerificationProcedureIdentity(
        verification_procedure_id="procedure-001",
        verifier_id="metadata-verifier",
        verifier_version="v1",
        configuration_digest=create_digest("2" * 64),
    )
    return SecurityAdmissionCandidateMeasuredByteLengthObservation(
        observation_id="observation-001",
        observation_version=1,
        candidate_identity=create_candidate(),
        verification_procedure_identity=procedure,
        measured_byte_length=23,
        observed_at=datetime(2026, 9, 11, tzinfo=timezone.utc),
    )


def create_basis() -> SecurityAdmissionCandidateByteLengthComparisonBasis:
    return SecurityAdmissionCandidateByteLengthComparisonBasis(
        declared_byte_length=create_declaration(),
        measured_byte_length_observation=create_measurement(),
        comparison_scheme_id="byte-length-comparison",
        comparison_scheme_version=1,
    )


def test_byte_length_comparison_basis_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(
            SecurityAdmissionCandidateByteLengthComparisonBasis
        )
    ) == (
        "declared_byte_length",
        "measured_byte_length_observation",
        "comparison_scheme_id",
        "comparison_scheme_version",
    )


def test_byte_length_comparison_basis_is_immutable() -> None:
    basis = create_basis()

    with pytest.raises(FrozenInstanceError):
        basis.comparison_scheme_version = 2  # type: ignore[misc]


def test_byte_length_comparison_basis_uses_slots() -> None:
    assert not hasattr(create_basis(), "__dict__")


def test_declared_byte_length_requires_exact_type() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "declared_byte_length must be a "
            "SecurityAdmissionCandidateDeclaredByteLength"
        ),
    ):
        replace(
            create_basis(),
            declared_byte_length=object(),  # type: ignore[arg-type]
        )


def test_exact_declaration_reference_is_preserved() -> None:
    declaration = create_declaration()
    basis = replace(
        create_basis(),
        declared_byte_length=declaration,
    )

    assert basis.declared_byte_length is declaration


def test_measured_observation_requires_exact_type() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "measured_byte_length_observation must be a "
            "SecurityAdmissionCandidateMeasuredByteLengthObservation"
        ),
    ):
        replace(
            create_basis(),
            measured_byte_length_observation=object(),  # type: ignore[arg-type]
        )


def test_exact_measurement_reference_is_preserved() -> None:
    measurement = create_measurement()
    basis = replace(
        create_basis(),
        measured_byte_length_observation=measurement,
    )

    assert basis.measured_byte_length_observation is measurement


def test_reconstructed_candidate_identity_is_compatible() -> None:
    declaration = create_declaration()
    measurement = create_measurement()

    assert (
        declaration.metadata_identity.candidate_identity
        == measurement.candidate_identity
    )
    assert (
        declaration.metadata_identity.candidate_identity
        is not measurement.candidate_identity
    )

    basis = SecurityAdmissionCandidateByteLengthComparisonBasis(
        declared_byte_length=declaration,
        measured_byte_length_observation=measurement,
        comparison_scheme_id="byte-length-comparison",
        comparison_scheme_version=1,
    )

    assert basis.declared_byte_length is declaration
    assert basis.measured_byte_length_observation is measurement


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("candidate_id", "candidate-002"),
        ("candidate_version", 2),
        ("customer_id", "customer-002"),
        ("content_digest", create_digest("f" * 64)),
    ],
)
def test_incompatible_candidate_identity_is_rejected(
    field_name: str,
    value: object,
) -> None:
    basis = create_basis()
    incompatible_candidate = replace(
        basis.measured_byte_length_observation.candidate_identity,
        **{field_name: value},
    )
    incompatible_measurement = replace(
        basis.measured_byte_length_observation,
        candidate_identity=incompatible_candidate,
    )

    with pytest.raises(
        ValueError,
        match=(
            "declared and measured byte lengths must reference "
            "the same candidate_identity"
        ),
    ):
        replace(
            basis,
            measured_byte_length_observation=incompatible_measurement,
        )


@pytest.mark.parametrize("value", [None, 1, True, object()])
def test_comparison_scheme_id_requires_string(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="comparison_scheme_id must be a string",
    ):
        replace(
            create_basis(),
            comparison_scheme_id=value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("value", ["", " ", "\t", "\n"])
def test_comparison_scheme_id_must_not_be_blank(
    value: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="comparison_scheme_id must not be blank",
    ):
        replace(
            create_basis(),
            comparison_scheme_id=value,
        )


def test_comparison_scheme_id_is_preserved_literally() -> None:
    value = " Byte-Length-Comparison-Scheme "
    basis = replace(
        create_basis(),
        comparison_scheme_id=value,
    )

    assert basis.comparison_scheme_id == value


@pytest.mark.parametrize("value", [True, False, 1.0, "1", None])
def test_comparison_scheme_version_requires_strict_integer(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="comparison_scheme_version must be an integer",
    ):
        replace(
            create_basis(),
            comparison_scheme_version=value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("value", [0, -1, -(10**30)])
def test_comparison_scheme_version_must_be_positive(
    value: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="comparison_scheme_version must be positive",
    ):
        replace(
            create_basis(),
            comparison_scheme_version=value,
        )


def test_reconstructed_equal_basis_has_value_equality() -> None:
    original = create_basis()
    reconstructed = SecurityAdmissionCandidateByteLengthComparisonBasis(
        declared_byte_length=create_declaration(),
        measured_byte_length_observation=create_measurement(),
        comparison_scheme_id="byte-length-comparison",
        comparison_scheme_version=1,
    )

    assert reconstructed == original
    assert reconstructed is not original


def test_every_field_participates_in_basis_identity() -> None:
    basis = create_basis()

    assert replace(
        basis,
        declared_byte_length=replace(
            basis.declared_byte_length,
            declared_byte_length=29,
        ),
    ) != basis
    assert replace(
        basis,
        measured_byte_length_observation=replace(
            basis.measured_byte_length_observation,
            measured_byte_length=29,
        ),
    ) != basis
    assert replace(
        basis,
        comparison_scheme_id="other-scheme",
    ) != basis
    assert replace(
        basis,
        comparison_scheme_version=2,
    ) != basis


def test_unequal_byte_lengths_remain_admissible_inputs() -> None:
    basis = create_basis()

    assert (
        basis.declared_byte_length.declared_byte_length
        != basis.measured_byte_length_observation.measured_byte_length
    )


def test_result_and_admission_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(
            SecurityAdmissionCandidateByteLengthComparisonBasis
        )
    }

    assert names.isdisjoint(
        {
            "match_status",
            "mismatch_reason",
            "matches",
            "normalized_declared_byte_length",
            "normalized_measured_byte_length",
            "maximum_byte_length",
            "oversize",
            "compared_at",
            "status",
            "decision",
            "reason",
            "authorized",
            "rejected",
            "malformed",
            "unsupported",
            "suspicious",
            "quarantine",
            "retention",
        }
    )


def test_contract_performs_no_byte_length_comparison() -> None:
    module = inspect.getmodule(
        SecurityAdmissionCandidateByteLengthComparisonBasis
    )
    assert module is not None
    source = inspect.getsource(module)
    tree = ast.parse(source)
    accessed_attributes = {
        node.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute)
    }

    assert "measured_byte_length" not in accessed_attributes
    assert "casefold(" not in source
    assert "lower(" not in source
    assert "upper(" not in source


def test_contract_imports_no_comparison_or_external_capability() -> None:
    module = inspect.getmodule(
        SecurityAdmissionCandidateByteLengthComparisonBasis
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
            "re",
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
        SecurityAdmissionCandidateByteLengthComparisonBasis
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    functions = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    assert functions == {"__post_init__"}
