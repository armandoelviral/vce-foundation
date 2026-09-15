from dataclasses import FrozenInstanceError, fields, replace

import ast
import inspect

import pytest

from sp001.contracts.knowledge_source_identity import KnowledgeContentDigest
from sp001.contracts.security_admission_candidate_identity import (
    SecurityAdmissionCandidateIdentity,
)
from sp001.contracts.security_admission_evaluation_basis import (
    SecurityAdmissionEvaluationBasis,
)
from sp001.contracts.security_admission_policy_identity import (
    SecurityAdmissionPolicyIdentity,
)


def create_digest(value: str) -> KnowledgeContentDigest:
    return KnowledgeContentDigest(algorithm="SHA-256", value=value)


def create_candidate(
    *,
    candidate_version: int = 1,
) -> SecurityAdmissionCandidateIdentity:
    return SecurityAdmissionCandidateIdentity(
        candidate_id="candidate-001",
        candidate_version=candidate_version,
        customer_id="customer-001",
        content_digest=create_digest("0" * 64),
    )


def create_policy(
    *,
    admission_policy_version: int = 1,
) -> SecurityAdmissionPolicyIdentity:
    return SecurityAdmissionPolicyIdentity(
        admission_policy_id="admission-policy-001",
        admission_policy_version=admission_policy_version,
        configuration_digest=create_digest("1" * 64),
    )


def create_basis() -> SecurityAdmissionEvaluationBasis:
    return SecurityAdmissionEvaluationBasis(
        candidate_identity=create_candidate(),
        admission_policy_identity=create_policy(),
    )


def test_evaluation_basis_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(SecurityAdmissionEvaluationBasis)
    ) == (
        "candidate_identity",
        "admission_policy_identity",
    )


def test_evaluation_basis_is_immutable() -> None:
    with pytest.raises(FrozenInstanceError):
        create_basis().candidate_identity = create_candidate(  # type: ignore[misc]
            candidate_version=2,
        )


def test_evaluation_basis_uses_slots() -> None:
    assert not hasattr(create_basis(), "__dict__")


@pytest.mark.parametrize("value", [None, 1, True, object()])
def test_candidate_identity_requires_exact_type(value: object) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "candidate_identity must be a "
            "SecurityAdmissionCandidateIdentity"
        ),
    ):
        replace(
            create_basis(),
            candidate_identity=value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("value", [None, 1, True, object()])
def test_admission_policy_identity_requires_exact_type(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "admission_policy_identity must be a "
            "SecurityAdmissionPolicyIdentity"
        ),
    ):
        replace(
            create_basis(),
            admission_policy_identity=value,  # type: ignore[arg-type]
        )


def test_exact_candidate_reference_is_preserved() -> None:
    candidate = create_candidate(candidate_version=2)
    basis = replace(create_basis(), candidate_identity=candidate)
    assert basis.candidate_identity is candidate


def test_exact_policy_reference_is_preserved() -> None:
    policy = create_policy(admission_policy_version=2)
    basis = replace(create_basis(), admission_policy_identity=policy)
    assert basis.admission_policy_identity is policy


def test_reconstructed_equal_basis_has_value_equality() -> None:
    original = create_basis()
    reconstructed = SecurityAdmissionEvaluationBasis(
        candidate_identity=create_candidate(),
        admission_policy_identity=create_policy(),
    )
    assert reconstructed == original
    assert reconstructed is not original


def test_candidate_and_policy_participate_in_basis_value() -> None:
    basis = create_basis()
    assert replace(
        basis,
        candidate_identity=create_candidate(candidate_version=2),
    ) != basis
    assert replace(
        basis,
        admission_policy_identity=create_policy(
            admission_policy_version=2,
        ),
    ) != basis


def test_basis_requires_no_evidence_object() -> None:
    basis = SecurityAdmissionEvaluationBasis(
        candidate_identity=create_candidate(),
        admission_policy_identity=create_policy(),
    )
    assert basis == create_basis()


def test_evidence_and_comparison_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(SecurityAdmissionEvaluationBasis)
    }
    assert names.isdisjoint(
        {
            "evidence",
            "evidence_items",
            "evidence_results",
            "media_type_result",
            "byte_length_result",
            "comparison_result",
            "comparison_results",
        }
    )


def test_event_classification_and_authority_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(SecurityAdmissionEvaluationBasis)
    }
    assert names.isdisjoint(
        {
            "evaluation_id",
            "evaluated_at",
            "effective_at",
            "actor",
            "actor_identity",
            "status",
            "decision",
            "reason",
            "admitted",
            "rejected",
            "malformed",
            "unsupported",
            "suspicious",
            "indeterminate",
            "quarantine",
            "retention",
            "authorized",
        }
    )


def test_contract_performs_no_policy_or_comparison_execution() -> None:
    module = inspect.getmodule(SecurityAdmissionEvaluationBasis)
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    assert not any(
        isinstance(
            node,
            (
                ast.Try,
                ast.Match,
                ast.AsyncFunctionDef,
                ast.For,
                ast.While,
            ),
        )
        for node in ast.walk(tree)
    )


def test_contract_imports_no_external_capability() -> None:
    module = inspect.getmodule(SecurityAdmissionEvaluationBasis)
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
    module = inspect.getmodule(SecurityAdmissionEvaluationBasis)
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    function_names = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    assert function_names == {"__post_init__"}
