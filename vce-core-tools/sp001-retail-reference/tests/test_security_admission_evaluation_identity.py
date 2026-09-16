from dataclasses import FrozenInstanceError, fields, replace

import ast
import inspect

import pytest

from sp001.contracts.security_admission_evaluation_basis import (
    SecurityAdmissionEvaluationBasis,
)
from sp001.contracts.security_admission_evaluation_identity import (
    SecurityAdmissionEvaluationIdentity,
)
from tests.test_security_admission_evaluation_basis import (
    create_basis,
)


def create_identity() -> SecurityAdmissionEvaluationIdentity:
    return SecurityAdmissionEvaluationIdentity(
        evaluation_id="evaluation-001",
        evaluation_version=1,
        evaluation_basis=create_basis(),
    )


def test_evaluation_identity_fields_are_exact() -> None:
    identity_fields = fields(SecurityAdmissionEvaluationIdentity)

    assert tuple(field.name for field in identity_fields) == (
        "evaluation_id",
        "evaluation_version",
        "evaluation_basis",
    )
    assert identity_fields[0].type is str
    assert identity_fields[1].type is int
    assert identity_fields[2].type is SecurityAdmissionEvaluationBasis


def test_evaluation_identity_is_immutable() -> None:
    identity = create_identity()

    with pytest.raises(FrozenInstanceError):
        identity.evaluation_id = "evaluation-002"


def test_evaluation_identity_uses_slots() -> None:
    identity = create_identity()

    assert hasattr(SecurityAdmissionEvaluationIdentity, "__slots__")
    assert not hasattr(identity, "__dict__")


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_evaluation_id_requires_exact_type(invalid_value) -> None:
    with pytest.raises(
        TypeError,
        match="evaluation_id must be a string",
    ):
        SecurityAdmissionEvaluationIdentity(
            evaluation_id=invalid_value,
            evaluation_version=1,
            evaluation_basis=create_basis(),
        )


@pytest.mark.parametrize("invalid_value", ("", " ", "\t", "\n"))
def test_evaluation_id_must_not_be_blank(invalid_value: str) -> None:
    with pytest.raises(
        ValueError,
        match="evaluation_id must not be blank",
    ):
        SecurityAdmissionEvaluationIdentity(
            evaluation_id=invalid_value,
            evaluation_version=1,
            evaluation_basis=create_basis(),
        )


@pytest.mark.parametrize(
    "invalid_value",
    (None, "1", 1.0, True, object()),
)
def test_evaluation_version_requires_exact_type(invalid_value) -> None:
    with pytest.raises(
        TypeError,
        match="evaluation_version must be an integer",
    ):
        SecurityAdmissionEvaluationIdentity(
            evaluation_id="evaluation-001",
            evaluation_version=invalid_value,
            evaluation_basis=create_basis(),
        )


@pytest.mark.parametrize("invalid_value", (0, -1, -100))
def test_evaluation_version_must_be_positive(
    invalid_value: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="evaluation_version must be positive",
    ):
        SecurityAdmissionEvaluationIdentity(
            evaluation_id="evaluation-001",
            evaluation_version=invalid_value,
            evaluation_basis=create_basis(),
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_evaluation_basis_requires_exact_type(invalid_value) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "evaluation_basis must be a "
            "SecurityAdmissionEvaluationBasis"
        ),
    ):
        SecurityAdmissionEvaluationIdentity(
            evaluation_id="evaluation-001",
            evaluation_version=1,
            evaluation_basis=invalid_value,
        )


def test_exact_evaluation_basis_reference_is_preserved() -> None:
    basis = create_basis()
    identity = SecurityAdmissionEvaluationIdentity(
        evaluation_id="evaluation-001",
        evaluation_version=1,
        evaluation_basis=basis,
    )

    assert identity.evaluation_basis is basis


def test_reconstructed_equal_identity_has_value_equality() -> None:
    identity = create_identity()
    reconstructed = SecurityAdmissionEvaluationIdentity(
        evaluation_id=identity.evaluation_id,
        evaluation_version=identity.evaluation_version,
        evaluation_basis=replace(identity.evaluation_basis),
    )

    assert reconstructed == identity
    assert reconstructed is not identity


def test_evaluation_id_participates_in_identity_value() -> None:
    identity = create_identity()

    assert replace(identity, evaluation_id="evaluation-002") != identity


def test_evaluation_version_participates_in_identity_value() -> None:
    identity = create_identity()

    assert replace(identity, evaluation_version=2) != identity


def test_evaluation_basis_participates_in_identity_value() -> None:
    identity = create_identity()
    different_candidate = replace(
        identity.evaluation_basis.candidate_identity,
        candidate_id="candidate-002",
    )
    different_basis = replace(
        identity.evaluation_basis,
        candidate_identity=different_candidate,
    )

    assert replace(identity, evaluation_basis=different_basis) != identity


def test_occurrence_and_evidence_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(SecurityAdmissionEvaluationIdentity)
    }
    forbidden = {
        "evaluated_at",
        "occurred_at",
        "bindings",
        "evidence",
        "evidence_bindings",
    }

    assert names.isdisjoint(forbidden)


def test_decision_and_authority_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(SecurityAdmissionEvaluationIdentity)
    }
    forbidden = {
        "status",
        "decision",
        "reason",
        "actor",
        "procedure_identity",
        "authorized",
        "quarantine",
        "retention",
    }

    assert names.isdisjoint(forbidden)


def test_contract_performs_no_evaluation_or_policy_execution() -> None:
    module = inspect.getmodule(SecurityAdmissionEvaluationIdentity)
    assert module is not None
    source = inspect.getsource(module)

    assert ".evaluate(" not in source
    assert ".compare(" not in source
    assert ".execute(" not in source
    assert ".authorize(" not in source


def test_contract_imports_no_external_capability() -> None:
    module = inspect.getmodule(SecurityAdmissionEvaluationIdentity)
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    imported_names = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        for alias in node.names
    }

    assert imported_names == {
        "dataclass",
        "SecurityAdmissionEvaluationBasis",
    }


def test_contract_defines_validation_only() -> None:
    module = inspect.getmodule(SecurityAdmissionEvaluationIdentity)
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    functions = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    assert functions == {"__post_init__"}
