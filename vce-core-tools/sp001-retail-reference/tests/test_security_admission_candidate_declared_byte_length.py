from dataclasses import FrozenInstanceError, fields, replace
import ast
import inspect

import pytest

from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
)
from sp001.contracts.security_admission_candidate_declared_byte_length import (
    SecurityAdmissionCandidateDeclaredByteLength,
)
from sp001.contracts.security_admission_candidate_identity import (
    SecurityAdmissionCandidateIdentity,
)
from sp001.contracts.security_admission_candidate_metadata_identity import (
    SecurityAdmissionCandidateMetadataIdentity,
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


def create_metadata_identity() -> (
    SecurityAdmissionCandidateMetadataIdentity
):
    return SecurityAdmissionCandidateMetadataIdentity(
        candidate_identity=create_candidate(),
        metadata_schema_id="admission-metadata",
        metadata_schema_version=1,
        metadata_digest=create_digest("1" * 64),
    )


def create_declaration() -> (
    SecurityAdmissionCandidateDeclaredByteLength
):
    return SecurityAdmissionCandidateDeclaredByteLength(
        metadata_identity=create_metadata_identity(),
        declared_byte_length=4096,
    )


def test_declared_byte_length_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(
            SecurityAdmissionCandidateDeclaredByteLength
        )
    ) == (
        "metadata_identity",
        "declared_byte_length",
    )


def test_declared_byte_length_is_immutable() -> None:
    declaration = create_declaration()

    with pytest.raises(FrozenInstanceError):
        declaration.declared_byte_length = 1  # type: ignore[misc]


def test_declared_byte_length_uses_slots() -> None:
    assert not hasattr(create_declaration(), "__dict__")


def test_metadata_identity_requires_exact_type() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "metadata_identity must be a "
            "SecurityAdmissionCandidateMetadataIdentity"
        ),
    ):
        replace(
            create_declaration(),
            metadata_identity=object(),  # type: ignore[arg-type]
        )


def test_exact_metadata_identity_reference_is_preserved() -> None:
    metadata_identity = create_metadata_identity()
    declaration = replace(
        create_declaration(),
        metadata_identity=metadata_identity,
    )

    assert declaration.metadata_identity is metadata_identity


def test_candidate_identity_remains_fully_recoverable() -> None:
    declaration = create_declaration()

    assert (
        declaration.metadata_identity.candidate_identity
        == create_candidate()
    )


@pytest.mark.parametrize(
    "value",
    [True, False, None, 1.0, "1", object()],
)
def test_declared_byte_length_requires_strict_integer(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="declared_byte_length must be an integer",
    ):
        replace(
            create_declaration(),
            declared_byte_length=value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("value", [-1, -(10**30)])
def test_declared_byte_length_must_not_be_negative(
    value: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="declared_byte_length must not be negative",
    ):
        replace(
            create_declaration(),
            declared_byte_length=value,
        )


def test_zero_is_an_explicit_declared_length() -> None:
    declaration = replace(
        create_declaration(),
        declared_byte_length=0,
    )

    assert declaration.declared_byte_length == 0


def test_arbitrary_size_integer_is_preserved_exactly() -> None:
    value = 10**1000
    declaration = replace(
        create_declaration(),
        declared_byte_length=value,
    )

    assert declaration.declared_byte_length == value


def test_reconstructed_equal_declaration_has_value_equality() -> None:
    original = create_declaration()
    reconstructed = SecurityAdmissionCandidateDeclaredByteLength(
        metadata_identity=create_metadata_identity(),
        declared_byte_length=4096,
    )

    assert reconstructed == original
    assert reconstructed is not original


def test_metadata_identity_participates_in_declaration() -> None:
    declaration = create_declaration()
    other_metadata = replace(
        create_metadata_identity(),
        metadata_schema_version=2,
    )

    assert replace(
        declaration,
        metadata_identity=other_metadata,
    ) != declaration


def test_literal_byte_length_participates_in_declaration() -> None:
    declaration = create_declaration()

    assert replace(
        declaration,
        declared_byte_length=4097,
    ) != declaration


def test_measured_policy_and_authority_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(
            SecurityAdmissionCandidateDeclaredByteLength
        )
    }

    assert names.isdisjoint(
        {
            "measured_byte_length",
            "maximum_byte_length",
            "allowed_byte_length",
            "content_bytes",
            "status",
            "decision",
            "reason",
            "authorized",
            "retention",
        }
    )


def test_media_type_declaration_is_not_coupled() -> None:
    names = {
        field.name
        for field in fields(
            SecurityAdmissionCandidateDeclaredByteLength
        )
    }

    assert names.isdisjoint(
        {
            "declared_media_type",
            "verified_media_type",
            "allowed_media_type",
        }
    )


def test_contract_performs_no_content_inspection_or_measurement() -> None:
    module = inspect.getmodule(
        SecurityAdmissionCandidateDeclaredByteLength
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))

    assert not any(
        isinstance(
            node,
            (
                ast.Try,
                ast.Match,
                ast.AsyncFunctionDef,
            ),
        )
        for node in ast.walk(tree)
    )


def test_contract_imports_no_content_or_external_capability() -> None:
    module = inspect.getmodule(
        SecurityAdmissionCandidateDeclaredByteLength
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
        SecurityAdmissionCandidateDeclaredByteLength
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    functions = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    assert functions == {"__post_init__"}
