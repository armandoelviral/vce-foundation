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


def create_digest(value: str = "0" * 64) -> KnowledgeContentDigest:
    return KnowledgeContentDigest(
        algorithm="SHA-256",
        value=value,
    )


def create_identity() -> SecurityAdmissionCandidateIdentity:
    return SecurityAdmissionCandidateIdentity(
        candidate_id="candidate-001",
        candidate_version=1,
        customer_id="customer-001",
        content_digest=create_digest(),
    )


def test_candidate_identity_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(SecurityAdmissionCandidateIdentity)
    ) == (
        "candidate_id",
        "candidate_version",
        "customer_id",
        "content_digest",
    )


def test_candidate_identity_is_immutable() -> None:
    identity = create_identity()

    with pytest.raises(FrozenInstanceError):
        identity.candidate_id = "other"  # type: ignore[misc]


def test_candidate_identity_uses_slots() -> None:
    assert not hasattr(create_identity(), "__dict__")


@pytest.mark.parametrize("value", [None, 1, True, object()])
def test_candidate_id_requires_string(value: object) -> None:
    with pytest.raises(
        TypeError,
        match="candidate_id must be a string",
    ):
        replace(
            create_identity(),
            candidate_id=value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("value", ["", " ", "\t", "\n"])
def test_candidate_id_must_not_be_blank(value: str) -> None:
    with pytest.raises(
        ValueError,
        match="candidate_id must not be blank",
    ):
        replace(create_identity(), candidate_id=value)


def test_candidate_id_is_preserved_without_normalization() -> None:
    value = " Candidate-ID "
    identity = replace(create_identity(), candidate_id=value)

    assert identity.candidate_id == value


@pytest.mark.parametrize("value", [True, False, 1.0, "1", None])
def test_candidate_version_requires_strict_integer(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="candidate_version must be an integer",
    ):
        replace(
            create_identity(),
            candidate_version=value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("value", [0, -1, -(10**30)])
def test_candidate_version_must_be_positive(value: int) -> None:
    with pytest.raises(
        ValueError,
        match="candidate_version must be positive",
    ):
        replace(create_identity(), candidate_version=value)


@pytest.mark.parametrize("value", [None, 1, True, object()])
def test_customer_id_requires_string(value: object) -> None:
    with pytest.raises(
        TypeError,
        match="customer_id must be a string",
    ):
        replace(
            create_identity(),
            customer_id=value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("value", ["", " ", "\t", "\n"])
def test_customer_id_must_not_be_blank(value: str) -> None:
    with pytest.raises(
        ValueError,
        match="customer_id must not be blank",
    ):
        replace(create_identity(), customer_id=value)


def test_customer_id_is_preserved_without_normalization() -> None:
    value = " Customer-ID "
    identity = replace(create_identity(), customer_id=value)

    assert identity.customer_id == value


def test_content_digest_requires_exact_type() -> None:
    with pytest.raises(
        TypeError,
        match="content_digest must be a KnowledgeContentDigest",
    ):
        replace(
            create_identity(),
            content_digest=object(),  # type: ignore[arg-type]
        )


def test_exact_content_digest_reference_is_preserved() -> None:
    digest = create_digest("a" * 64)
    identity = replace(create_identity(), content_digest=digest)

    assert identity.content_digest is digest


def test_reconstructed_equal_identity_has_value_equality() -> None:
    original = create_identity()
    reconstructed = SecurityAdmissionCandidateIdentity(
        candidate_id="candidate-001",
        candidate_version=1,
        customer_id="customer-001",
        content_digest=create_digest(),
    )

    assert reconstructed == original
    assert reconstructed is not original


def test_customer_version_and_digest_participate_in_identity() -> None:
    identity = create_identity()

    assert replace(identity, customer_id="customer-002") != identity
    assert replace(identity, candidate_version=2) != identity
    assert replace(
        identity,
        content_digest=create_digest("b" * 64),
    ) != identity


def test_authority_and_payload_fields_are_absent() -> None:
    field_names = {
        field.name
        for field in fields(SecurityAdmissionCandidateIdentity)
    }

    assert field_names.isdisjoint(
        {
            "content_bytes",
            "raw_payload",
            "source_uri",
            "media_type",
            "status",
            "decision",
            "reason",
            "policy",
            "retention",
            "authorized",
        }
    )


def test_contract_imports_no_external_capability() -> None:
    module = inspect.getmodule(SecurityAdmissionCandidateIdentity)
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    imported_roots = {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imported_roots.update(
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        and node.module is not None
    )

    assert imported_roots.isdisjoint(
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
    module = inspect.getmodule(SecurityAdmissionCandidateIdentity)
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    function_names = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    assert function_names == {"__post_init__"}
