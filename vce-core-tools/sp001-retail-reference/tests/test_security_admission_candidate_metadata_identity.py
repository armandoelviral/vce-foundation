from dataclasses import FrozenInstanceError, fields, replace
import ast
import inspect

import pytest

from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
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


def test_metadata_identity_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(
            SecurityAdmissionCandidateMetadataIdentity
        )
    ) == (
        "candidate_identity",
        "metadata_schema_id",
        "metadata_schema_version",
        "metadata_digest",
    )


def test_metadata_identity_is_immutable() -> None:
    identity = create_metadata_identity()

    with pytest.raises(FrozenInstanceError):
        identity.metadata_schema_version = 2  # type: ignore[misc]


def test_metadata_identity_uses_slots() -> None:
    assert not hasattr(create_metadata_identity(), "__dict__")


def test_candidate_identity_requires_exact_type() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "candidate_identity must be a "
            "SecurityAdmissionCandidateIdentity"
        ),
    ):
        replace(
            create_metadata_identity(),
            candidate_identity=object(),  # type: ignore[arg-type]
        )


def test_exact_candidate_reference_is_preserved() -> None:
    candidate = create_candidate()
    identity = replace(
        create_metadata_identity(),
        candidate_identity=candidate,
    )

    assert identity.candidate_identity is candidate


@pytest.mark.parametrize("value", [None, 1, True, object()])
def test_metadata_schema_id_requires_string(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="metadata_schema_id must be a string",
    ):
        replace(
            create_metadata_identity(),
            metadata_schema_id=value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("value", ["", " ", "\t", "\n"])
def test_metadata_schema_id_must_not_be_blank(
    value: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="metadata_schema_id must not be blank",
    ):
        replace(
            create_metadata_identity(),
            metadata_schema_id=value,
        )


def test_metadata_schema_id_is_preserved_literally() -> None:
    value = " Metadata-Schema "
    identity = replace(
        create_metadata_identity(),
        metadata_schema_id=value,
    )

    assert identity.metadata_schema_id == value


@pytest.mark.parametrize("value", [True, False, 1.0, "1", None])
def test_metadata_schema_version_requires_strict_integer(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="metadata_schema_version must be an integer",
    ):
        replace(
            create_metadata_identity(),
            metadata_schema_version=value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("value", [0, -1, -(10**30)])
def test_metadata_schema_version_must_be_positive(
    value: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="metadata_schema_version must be positive",
    ):
        replace(
            create_metadata_identity(),
            metadata_schema_version=value,
        )


def test_metadata_digest_requires_exact_type() -> None:
    with pytest.raises(
        TypeError,
        match="metadata_digest must be a KnowledgeContentDigest",
    ):
        replace(
            create_metadata_identity(),
            metadata_digest=object(),  # type: ignore[arg-type]
        )


def test_exact_metadata_digest_reference_is_preserved() -> None:
    digest = create_digest("a" * 64)
    identity = replace(
        create_metadata_identity(),
        metadata_digest=digest,
    )

    assert identity.metadata_digest is digest


def test_reconstructed_equal_identity_has_value_equality() -> None:
    original = create_metadata_identity()
    reconstructed = SecurityAdmissionCandidateMetadataIdentity(
        candidate_identity=create_candidate(),
        metadata_schema_id="admission-metadata",
        metadata_schema_version=1,
        metadata_digest=create_digest("1" * 64),
    )

    assert reconstructed == original
    assert reconstructed is not original


def test_candidate_schema_version_and_digest_participate() -> None:
    identity = create_metadata_identity()
    other_candidate = replace(
        create_candidate(),
        candidate_version=2,
    )

    assert replace(
        identity,
        candidate_identity=other_candidate,
    ) != identity
    assert replace(
        identity,
        metadata_schema_id="other-schema",
    ) != identity
    assert replace(
        identity,
        metadata_schema_version=2,
    ) != identity
    assert replace(
        identity,
        metadata_digest=create_digest("2" * 64),
    ) != identity


def test_declared_and_verified_metadata_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(
            SecurityAdmissionCandidateMetadataIdentity
        )
    }

    assert names.isdisjoint(
        {
            "metadata_bytes",
            "media_type",
            "declared_byte_length",
            "measured_byte_length",
            "original_name",
            "source_uri",
            "verified",
            "status",
            "decision",
            "retention",
            "authorized",
        }
    )


def test_contract_performs_no_serialization_or_parsing() -> None:
    module = inspect.getmodule(
        SecurityAdmissionCandidateMetadataIdentity
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))

    assert not any(
        isinstance(node, (ast.Try, ast.BinOp))
        for node in ast.walk(tree)
    )


def test_contract_imports_no_external_capability() -> None:
    module = inspect.getmodule(
        SecurityAdmissionCandidateMetadataIdentity
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
            "json",
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
        SecurityAdmissionCandidateMetadataIdentity
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    functions = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    assert functions == {"__post_init__"}
