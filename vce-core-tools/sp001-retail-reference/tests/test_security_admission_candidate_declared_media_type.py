from dataclasses import FrozenInstanceError, fields, replace
import ast
import inspect

import pytest

from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
)
from sp001.contracts.security_admission_candidate_declared_media_type import (
    SecurityAdmissionCandidateDeclaredMediaType,
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
    SecurityAdmissionCandidateDeclaredMediaType
):
    return SecurityAdmissionCandidateDeclaredMediaType(
        metadata_identity=create_metadata_identity(),
        declared_media_type="image/jpeg",
    )


def test_declared_media_type_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(
            SecurityAdmissionCandidateDeclaredMediaType
        )
    ) == (
        "metadata_identity",
        "declared_media_type",
    )


def test_declared_media_type_is_immutable() -> None:
    declaration = create_declaration()

    with pytest.raises(FrozenInstanceError):
        declaration.declared_media_type = "image/png"  # type: ignore[misc]


def test_declared_media_type_uses_slots() -> None:
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


@pytest.mark.parametrize("value", [None, 1, True, object()])
def test_declared_media_type_requires_string(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="declared_media_type must be a string",
    ):
        replace(
            create_declaration(),
            declared_media_type=value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("value", ["", " ", "\t", "\n"])
def test_declared_media_type_must_not_be_blank(
    value: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="declared_media_type must not be blank",
    ):
        replace(
            create_declaration(),
            declared_media_type=value,
        )


@pytest.mark.parametrize(
    "value",
    [
        " IMAGE/JPEG ",
        "text/plain; charset=UTF-8",
        "application/x-future-format",
        "not/a verified media type",
    ],
)
def test_declared_media_type_is_preserved_literally(
    value: str,
) -> None:
    declaration = replace(
        create_declaration(),
        declared_media_type=value,
    )

    assert declaration.declared_media_type == value


def test_unknown_future_media_type_remains_representable() -> None:
    value = "application/vnd.future.vendor+binary; version=9000"

    assert replace(
        create_declaration(),
        declared_media_type=value,
    ).declared_media_type == value


def test_declaration_makes_no_syntactic_validity_claim() -> None:
    value = "untrusted declaration without MIME syntax"

    assert replace(
        create_declaration(),
        declared_media_type=value,
    ).declared_media_type == value


def test_reconstructed_equal_declaration_has_value_equality() -> None:
    original = create_declaration()
    reconstructed = SecurityAdmissionCandidateDeclaredMediaType(
        metadata_identity=create_metadata_identity(),
        declared_media_type="image/jpeg",
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


def test_literal_media_type_participates_in_declaration() -> None:
    declaration = create_declaration()

    assert replace(
        declaration,
        declared_media_type="IMAGE/JPEG",
    ) != declaration
    assert replace(
        declaration,
        declared_media_type=" image/jpeg ",
    ) != declaration


def test_verified_admission_and_authority_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(
            SecurityAdmissionCandidateDeclaredMediaType
        )
    }

    assert names.isdisjoint(
        {
            "verified_media_type",
            "allowed_media_type",
            "measured_byte_length",
            "status",
            "decision",
            "reason",
            "authorized",
            "retention",
        }
    )


def test_contract_performs_no_parsing_matching_or_mapping() -> None:
    module = inspect.getmodule(
        SecurityAdmissionCandidateDeclaredMediaType
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))

    assert not any(
        isinstance(node, (ast.Try, ast.Match, ast.BinOp))
        for node in ast.walk(tree)
    )


def test_contract_imports_no_media_or_external_capability() -> None:
    module = inspect.getmodule(
        SecurityAdmissionCandidateDeclaredMediaType
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
        SecurityAdmissionCandidateDeclaredMediaType
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    functions = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    assert functions == {"__post_init__"}
