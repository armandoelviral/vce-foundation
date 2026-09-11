from dataclasses import FrozenInstanceError, fields, replace
import ast
import inspect

import pytest

from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
)
from sp001.contracts.security_admission_metadata_verification_procedure_identity import (
    SecurityAdmissionMetadataVerificationProcedureIdentity,
)


def create_digest(value: str) -> KnowledgeContentDigest:
    return KnowledgeContentDigest(
        algorithm="SHA-256",
        value=value,
    )


def create_identity() -> (
    SecurityAdmissionMetadataVerificationProcedureIdentity
):
    return SecurityAdmissionMetadataVerificationProcedureIdentity(
        verification_procedure_id="procedure-001",
        verifier_id="metadata-verifier",
        verifier_version="v1.2.3+build.7",
        configuration_digest=create_digest("0" * 64),
    )


def test_verification_procedure_identity_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(
            SecurityAdmissionMetadataVerificationProcedureIdentity
        )
    ) == (
        "verification_procedure_id",
        "verifier_id",
        "verifier_version",
        "configuration_digest",
    )


def test_verification_procedure_identity_is_immutable() -> None:
    identity = create_identity()

    with pytest.raises(FrozenInstanceError):
        identity.verifier_version = "v2"  # type: ignore[misc]


def test_verification_procedure_identity_uses_slots() -> None:
    assert not hasattr(create_identity(), "__dict__")


@pytest.mark.parametrize("value", [None, 1, True, object()])
def test_verification_procedure_id_requires_string(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="verification_procedure_id must be a string",
    ):
        replace(
            create_identity(),
            verification_procedure_id=value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("value", ["", " ", "\t", "\n"])
def test_verification_procedure_id_must_not_be_blank(
    value: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="verification_procedure_id must not be blank",
    ):
        replace(
            create_identity(),
            verification_procedure_id=value,
        )


@pytest.mark.parametrize("value", [None, 1, True, object()])
def test_verifier_id_requires_string(value: object) -> None:
    with pytest.raises(
        TypeError,
        match="verifier_id must be a string",
    ):
        replace(
            create_identity(),
            verifier_id=value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("value", ["", " ", "\t", "\n"])
def test_verifier_id_must_not_be_blank(value: str) -> None:
    with pytest.raises(
        ValueError,
        match="verifier_id must not be blank",
    ):
        replace(
            create_identity(),
            verifier_id=value,
        )


@pytest.mark.parametrize("value", [None, 1, True, object()])
def test_verifier_version_requires_string(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="verifier_version must be a string",
    ):
        replace(
            create_identity(),
            verifier_version=value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("value", ["", " ", "\t", "\n"])
def test_verifier_version_must_not_be_blank(
    value: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="verifier_version must not be blank",
    ):
        replace(
            create_identity(),
            verifier_version=value,
        )


def test_declared_identifiers_are_preserved_literally() -> None:
    identity = SecurityAdmissionMetadataVerificationProcedureIdentity(
        verification_procedure_id=" Procedure-001 ",
        verifier_id=" Verifier-Engine ",
        verifier_version=" V1.2.3+BUILD.7 ",
        configuration_digest=create_digest("0" * 64),
    )

    assert identity.verification_procedure_id == " Procedure-001 "
    assert identity.verifier_id == " Verifier-Engine "
    assert identity.verifier_version == " V1.2.3+BUILD.7 "


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
    identity = replace(
        create_identity(),
        configuration_digest=digest,
    )

    assert identity.configuration_digest is digest


def test_reconstructed_equal_identity_has_value_equality() -> None:
    original = create_identity()
    reconstructed = (
        SecurityAdmissionMetadataVerificationProcedureIdentity(
            verification_procedure_id="procedure-001",
            verifier_id="metadata-verifier",
            verifier_version="v1.2.3+build.7",
            configuration_digest=create_digest("0" * 64),
        )
    )

    assert reconstructed == original
    assert reconstructed is not original


def test_every_field_participates_in_procedure_identity() -> None:
    identity = create_identity()

    assert replace(
        identity,
        verification_procedure_id="procedure-002",
    ) != identity
    assert replace(
        identity,
        verifier_id="other-verifier",
    ) != identity
    assert replace(
        identity,
        verifier_version="v2",
    ) != identity
    assert replace(
        identity,
        configuration_digest=create_digest("1" * 64),
    ) != identity


def test_execution_result_and_authority_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(
            SecurityAdmissionMetadataVerificationProcedureIdentity
        )
    }

    assert names.isdisjoint(
        {
            "candidate_identity",
            "metadata_identity",
            "actor",
            "actor_identity",
            "authority_binding",
            "authorized",
            "observed_at",
            "verified_at",
            "measured_at",
            "media_type",
            "byte_length",
            "status",
            "decision",
            "reason",
            "retention",
        }
    )


def test_contract_performs_no_verification_or_execution() -> None:
    module = inspect.getmodule(
        SecurityAdmissionMetadataVerificationProcedureIdentity
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


def test_contract_imports_no_external_capability() -> None:
    module = inspect.getmodule(
        SecurityAdmissionMetadataVerificationProcedureIdentity
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
        SecurityAdmissionMetadataVerificationProcedureIdentity
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    functions = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    assert functions == {"__post_init__"}
