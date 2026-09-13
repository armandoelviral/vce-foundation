from dataclasses import FrozenInstanceError, fields, replace
import ast
import inspect

import pytest

from sp001.contracts.knowledge_source_identity import KnowledgeContentDigest
from sp001.contracts.security_admission_policy_identity import (
    SecurityAdmissionPolicyIdentity,
)


def create_digest(value: str) -> KnowledgeContentDigest:
    return KnowledgeContentDigest(algorithm="SHA-256", value=value)


def create_identity() -> SecurityAdmissionPolicyIdentity:
    return SecurityAdmissionPolicyIdentity(
        admission_policy_id="admission-policy-001",
        admission_policy_version=1,
        configuration_digest=create_digest("0" * 64),
    )


def test_admission_policy_identity_fields_are_exact() -> None:
    assert tuple(
        field.name for field in fields(SecurityAdmissionPolicyIdentity)
    ) == (
        "admission_policy_id",
        "admission_policy_version",
        "configuration_digest",
    )


def test_admission_policy_identity_is_immutable() -> None:
    with pytest.raises(FrozenInstanceError):
        create_identity().admission_policy_version = 2  # type: ignore[misc]


def test_admission_policy_identity_uses_slots() -> None:
    assert not hasattr(create_identity(), "__dict__")


@pytest.mark.parametrize("value", [None, 1, True, object()])
def test_admission_policy_id_requires_string(value: object) -> None:
    with pytest.raises(
        TypeError,
        match="admission_policy_id must be a string",
    ):
        replace(
            create_identity(),
            admission_policy_id=value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("value", ["", " ", "\t", "\n"])
def test_admission_policy_id_must_not_be_blank(value: str) -> None:
    with pytest.raises(
        ValueError,
        match="admission_policy_id must not be blank",
    ):
        replace(create_identity(), admission_policy_id=value)


def test_admission_policy_id_is_preserved_literally() -> None:
    identity = replace(
        create_identity(),
        admission_policy_id=" Admission-Policy-001 ",
    )
    assert identity.admission_policy_id == " Admission-Policy-001 "


@pytest.mark.parametrize("value", [True, False, 1.0, "1", None])
def test_admission_policy_version_requires_strict_integer(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="admission_policy_version must be an integer",
    ):
        replace(
            create_identity(),
            admission_policy_version=value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("value", [0, -1, -(10**30)])
def test_admission_policy_version_must_be_positive(value: int) -> None:
    with pytest.raises(
        ValueError,
        match="admission_policy_version must be positive",
    ):
        replace(create_identity(), admission_policy_version=value)


def test_arbitrary_size_positive_policy_version_is_exact() -> None:
    version = 10**100
    identity = replace(
        create_identity(),
        admission_policy_version=version,
    )
    assert identity.admission_policy_version == version


def test_configuration_digest_requires_exact_type() -> None:
    with pytest.raises(
        TypeError,
        match="configuration_digest must be a KnowledgeContentDigest",
    ):
        replace(
            create_identity(),
            configuration_digest=object(),  # type: ignore[arg-type]
        )


def test_exact_configuration_digest_reference_is_preserved() -> None:
    digest = create_digest("a" * 64)
    identity = replace(create_identity(), configuration_digest=digest)
    assert identity.configuration_digest is digest


def test_reconstructed_equal_identity_has_value_equality() -> None:
    original = create_identity()
    reconstructed = SecurityAdmissionPolicyIdentity(
        admission_policy_id="admission-policy-001",
        admission_policy_version=1,
        configuration_digest=create_digest("0" * 64),
    )
    assert reconstructed == original
    assert reconstructed is not original


def test_every_field_participates_in_policy_identity() -> None:
    identity = create_identity()
    assert replace(
        identity,
        admission_policy_id="admission-policy-002",
    ) != identity
    assert replace(identity, admission_policy_version=2) != identity
    assert replace(
        identity,
        configuration_digest=create_digest("1" * 64),
    ) != identity


def test_evaluation_and_authority_fields_are_absent() -> None:
    names = {
        field.name for field in fields(SecurityAdmissionPolicyIdentity)
    }
    assert names.isdisjoint(
        {
            "candidate_identity",
            "actor_identity",
            "effective_at",
            "valid_from",
            "valid_until",
            "evaluated_at",
            "status",
            "decision",
            "reason",
            "authorized",
            "rejected",
            "malformed",
            "unsupported",
            "suspicious",
            "indeterminate",
            "quarantine",
            "retention",
        }
    )


def test_contract_performs_no_policy_evaluation() -> None:
    module = inspect.getmodule(SecurityAdmissionPolicyIdentity)
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    assert not any(
        isinstance(node, (ast.Try, ast.Match, ast.AsyncFunctionDef))
        for node in ast.walk(tree)
    )


def test_contract_imports_no_external_capability() -> None:
    module = inspect.getmodule(SecurityAdmissionPolicyIdentity)
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
        if isinstance(node, ast.ImportFrom) and node.module is not None
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
    module = inspect.getmodule(SecurityAdmissionPolicyIdentity)
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    functions = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    assert functions == {"__post_init__"}
