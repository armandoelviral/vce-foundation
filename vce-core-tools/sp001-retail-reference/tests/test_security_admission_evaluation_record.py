import ast
import inspect
from dataclasses import FrozenInstanceError, fields, replace
from datetime import datetime, timedelta, timezone

import pytest

from sp001.contracts.security_admission_evaluation_identity import (
    SecurityAdmissionEvaluationIdentity,
)
from sp001.contracts.security_admission_evaluation_record import (
    SecurityAdmissionEvaluationRecord,
)
from tests.test_security_admission_evaluation_identity import create_identity


def create_record(
    *,
    evaluation_identity: SecurityAdmissionEvaluationIdentity | None = None,
    evaluated_at: datetime | None = None,
) -> SecurityAdmissionEvaluationRecord:
    return SecurityAdmissionEvaluationRecord(
        evaluation_identity=(
            create_identity()
            if evaluation_identity is None
            else evaluation_identity
        ),
        evaluated_at=(
            datetime(2026, 9, 16, 12, 30, tzinfo=timezone.utc)
            if evaluated_at is None
            else evaluated_at
        ),
    )


def test_evaluation_record_fields_are_exact() -> None:
    record_fields = fields(SecurityAdmissionEvaluationRecord)

    assert tuple(field.name for field in record_fields) == (
        "evaluation_identity",
        "evaluated_at",
    )
    assert record_fields[0].type is SecurityAdmissionEvaluationIdentity
    assert record_fields[1].type is datetime


def test_evaluation_record_is_immutable() -> None:
    record = create_record()

    with pytest.raises(FrozenInstanceError):
        record.evaluated_at = datetime.now(timezone.utc)  # type: ignore[misc]


def test_evaluation_record_uses_slots() -> None:
    record = create_record()

    assert hasattr(SecurityAdmissionEvaluationRecord, "__slots__")
    assert not hasattr(record, "__dict__")


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_evaluation_identity_requires_exact_type(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "evaluation_identity must be a "
            "SecurityAdmissionEvaluationIdentity"
        ),
    ):
        SecurityAdmissionEvaluationRecord(
            evaluation_identity=invalid_value,  # type: ignore[arg-type]
            evaluated_at=datetime.now(timezone.utc),
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_evaluated_at_requires_exact_type(invalid_value: object) -> None:
    with pytest.raises(TypeError, match="evaluated_at must be a datetime"):
        SecurityAdmissionEvaluationRecord(
            evaluation_identity=create_identity(),
            evaluated_at=invalid_value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "naive_value",
    (
        datetime(2026, 9, 16),
        datetime.fromisoformat("2026-09-16T12:30:00"),
    ),
)
def test_evaluated_at_must_be_timezone_aware(
    naive_value: datetime,
) -> None:
    with pytest.raises(
        ValueError,
        match="evaluated_at must be timezone-aware",
    ):
        SecurityAdmissionEvaluationRecord(
            evaluation_identity=create_identity(),
            evaluated_at=naive_value,
        )


@pytest.mark.parametrize(
    "evaluated_at",
    (
        datetime(2026, 9, 16, tzinfo=timezone.utc),
        datetime(
            2026,
            9,
            16,
            tzinfo=timezone(timedelta(hours=-5)),
        ),
    ),
)
def test_timezone_aware_instants_are_accepted(
    evaluated_at: datetime,
) -> None:
    record = create_record(evaluated_at=evaluated_at)

    assert record.evaluated_at is evaluated_at


def test_exact_evaluation_identity_reference_is_preserved() -> None:
    identity = create_identity()
    record = create_record(evaluation_identity=identity)

    assert record.evaluation_identity is identity


def test_exact_evaluated_at_reference_is_preserved() -> None:
    evaluated_at = datetime(2026, 9, 16, tzinfo=timezone.utc)
    record = create_record(evaluated_at=evaluated_at)

    assert record.evaluated_at is evaluated_at


def test_reconstructed_equal_record_has_value_equality() -> None:
    record = create_record()
    reconstructed = SecurityAdmissionEvaluationRecord(
        evaluation_identity=replace(record.evaluation_identity),
        evaluated_at=record.evaluated_at,
    )

    assert reconstructed == record
    assert reconstructed is not record


def test_evaluation_identity_participates_in_record_value() -> None:
    record = create_record()
    different_identity = replace(
        record.evaluation_identity,
        evaluation_version=record.evaluation_identity.evaluation_version + 1,
    )

    assert replace(record, evaluation_identity=different_identity) != record


def test_evaluated_at_participates_in_record_value() -> None:
    record = create_record()

    assert replace(
        record,
        evaluated_at=record.evaluated_at + timedelta(seconds=1),
    ) != record


def test_evidence_and_decision_fields_are_absent() -> None:
    names = {field.name for field in fields(SecurityAdmissionEvaluationRecord)}

    assert names.isdisjoint(
        {
            "evidence",
            "evidence_items",
            "evidence_bindings",
            "media_type_result_binding",
            "byte_length_result_binding",
            "status",
            "decision",
            "reason",
            "admitted",
            "rejected",
        }
    )


def test_actor_and_procedure_fields_are_absent() -> None:
    names = {field.name for field in fields(SecurityAdmissionEvaluationRecord)}

    assert names.isdisjoint(
        {
            "actor",
            "actor_identity",
            "evaluator",
            "evaluator_identity",
            "procedure",
            "procedure_identity",
        }
    )


def test_persistence_acceptance_and_authority_fields_are_absent() -> None:
    names = {field.name for field in fields(SecurityAdmissionEvaluationRecord)}

    assert names.isdisjoint(
        {
            "persisted",
            "accepted",
            "authorized",
            "authorization",
            "quarantine",
            "retention",
        }
    )


def test_contract_performs_no_evaluation_or_policy_execution() -> None:
    source = inspect.getsource(SecurityAdmissionEvaluationRecord)

    forbidden_calls = {
        "compare",
        "evaluate",
        "execute",
        "authorize",
        "persist",
        "save",
    }
    tree = ast.parse(source)
    called_names = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }

    assert called_names.isdisjoint(forbidden_calls)


def test_contract_imports_no_external_capability() -> None:
    module = inspect.getmodule(SecurityAdmissionEvaluationRecord)
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    imported_roots = {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    imported_roots.update(
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    )

    assert imported_roots == {"dataclasses", "datetime", "sp001"}


def test_contract_defines_validation_only() -> None:
    module = inspect.getmodule(SecurityAdmissionEvaluationRecord)
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    functions = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    assert functions == {"__post_init__"}
