import ast
import inspect
from dataclasses import FrozenInstanceError, fields, replace
from datetime import timedelta

import pytest

from sp001.contracts.security_admission_candidate_indeterminate_byte_length_comparison_result_binding import (
    SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding,
)
from sp001.contracts.security_admission_evaluation_record import (
    SecurityAdmissionEvaluationRecord,
)
from sp001.contracts.security_admission_evaluation_record_indeterminate_byte_length_comparison_result_binding import (
    SecurityAdmissionEvaluationRecordIndeterminateByteLengthComparisonResultBinding,
)
from tests.test_security_admission_candidate_byte_length_comparison_result_binding import (
    create_binding as create_conclusive_byte_length_binding,
)
from tests.test_security_admission_candidate_indeterminate_byte_length_comparison_result_binding import (
    create_binding as create_indeterminate_byte_length_binding,
)
from tests.test_security_admission_evaluation_record import create_record


def create_recorded_binding(
    *,
    evaluation_record: SecurityAdmissionEvaluationRecord | None = None,
    indeterminate_byte_length_comparison_result_binding: (
        SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding
        | None
    ) = None,
) -> SecurityAdmissionEvaluationRecordIndeterminateByteLengthComparisonResultBinding:
    length_binding = (
        create_indeterminate_byte_length_binding()
        if indeterminate_byte_length_comparison_result_binding is None
        else indeterminate_byte_length_comparison_result_binding
    )
    record = create_record() if evaluation_record is None else evaluation_record
    identity = replace(
        record.evaluation_identity,
        evaluation_basis=length_binding.evaluation_basis,
    )
    record = replace(record, evaluation_identity=identity)
    return (
        SecurityAdmissionEvaluationRecordIndeterminateByteLengthComparisonResultBinding(
            evaluation_record=record,
            indeterminate_byte_length_comparison_result_binding=length_binding,
        )
    )


def test_recorded_binding_fields_are_exact() -> None:
    binding_fields = fields(
        SecurityAdmissionEvaluationRecordIndeterminateByteLengthComparisonResultBinding
    )
    assert tuple(field.name for field in binding_fields) == (
        "evaluation_record",
        "indeterminate_byte_length_comparison_result_binding",
    )
    assert binding_fields[0].type is SecurityAdmissionEvaluationRecord
    assert (
        binding_fields[1].type
        is SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding
    )


def test_recorded_binding_is_immutable() -> None:
    binding = create_recorded_binding()
    with pytest.raises(FrozenInstanceError):
        binding.evaluation_record = create_record()  # type: ignore[misc]


def test_recorded_binding_uses_slots() -> None:
    binding = create_recorded_binding()
    assert hasattr(
        SecurityAdmissionEvaluationRecordIndeterminateByteLengthComparisonResultBinding,
        "__slots__",
    )
    assert not hasattr(binding, "__dict__")


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_evaluation_record_requires_exact_type(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "evaluation_record must be a "
            "SecurityAdmissionEvaluationRecord"
        ),
    ):
        SecurityAdmissionEvaluationRecordIndeterminateByteLengthComparisonResultBinding(
            evaluation_record=invalid_value,  # type: ignore[arg-type]
            indeterminate_byte_length_comparison_result_binding=(
                create_indeterminate_byte_length_binding()
            ),
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_indeterminate_byte_length_binding_requires_exact_type(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "indeterminate_byte_length_comparison_result_binding must be a "
            "SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding"
        ),
    ):
        SecurityAdmissionEvaluationRecordIndeterminateByteLengthComparisonResultBinding(
            evaluation_record=create_record(),
            indeterminate_byte_length_comparison_result_binding=(
                invalid_value  # type: ignore[arg-type]
            ),
        )


def test_exact_evaluation_record_reference_is_preserved() -> None:
    binding = create_recorded_binding()
    record = binding.evaluation_record
    reconstructed = (
        SecurityAdmissionEvaluationRecordIndeterminateByteLengthComparisonResultBinding(
            evaluation_record=record,
            indeterminate_byte_length_comparison_result_binding=(
                binding.indeterminate_byte_length_comparison_result_binding
            ),
        )
    )
    assert reconstructed.evaluation_record is record


def test_exact_indeterminate_binding_reference_is_preserved() -> None:
    length_binding = create_indeterminate_byte_length_binding()
    binding = create_recorded_binding(
        indeterminate_byte_length_comparison_result_binding=length_binding,
    )
    assert (
        binding.indeterminate_byte_length_comparison_result_binding
        is length_binding
    )


def test_reconstructed_equal_binding_has_value_equality() -> None:
    binding = create_recorded_binding()
    reconstructed = (
        SecurityAdmissionEvaluationRecordIndeterminateByteLengthComparisonResultBinding(
            evaluation_record=replace(binding.evaluation_record),
            indeterminate_byte_length_comparison_result_binding=replace(
                binding.indeterminate_byte_length_comparison_result_binding
            ),
        )
    )
    assert reconstructed == binding
    assert reconstructed is not binding


def test_equal_reconstructed_basis_permits_binding() -> None:
    length_binding = create_indeterminate_byte_length_binding()
    record = create_record()
    reconstructed_basis = replace(length_binding.evaluation_basis)
    identity = replace(
        record.evaluation_identity,
        evaluation_basis=reconstructed_basis,
    )
    record = replace(record, evaluation_identity=identity)
    binding = (
        SecurityAdmissionEvaluationRecordIndeterminateByteLengthComparisonResultBinding(
            evaluation_record=record,
            indeterminate_byte_length_comparison_result_binding=length_binding,
        )
    )
    record_basis = binding.evaluation_record.evaluation_identity.evaluation_basis
    evidence_basis = (
        binding.indeterminate_byte_length_comparison_result_binding.evaluation_basis
    )
    assert record_basis == evidence_basis
    assert record_basis is not evidence_basis


def test_different_evaluation_basis_is_rejected() -> None:
    binding = create_recorded_binding()
    basis = binding.evaluation_record.evaluation_identity.evaluation_basis
    policy = basis.admission_policy_identity
    different_policy = replace(
        policy,
        admission_policy_version=policy.admission_policy_version + 1,
    )
    different_basis = replace(
        basis,
        admission_policy_identity=different_policy,
    )
    identity = replace(
        binding.evaluation_record.evaluation_identity,
        evaluation_basis=different_basis,
    )
    record = replace(binding.evaluation_record, evaluation_identity=identity)
    with pytest.raises(
        ValueError,
        match=(
            "indeterminate byte-length result binding must use "
            "evaluation record basis"
        ),
    ):
        SecurityAdmissionEvaluationRecordIndeterminateByteLengthComparisonResultBinding(
            evaluation_record=record,
            indeterminate_byte_length_comparison_result_binding=(
                binding.indeterminate_byte_length_comparison_result_binding
            ),
        )


@pytest.mark.parametrize(
    "reason",
    tuple(
        type(
            create_indeterminate_byte_length_binding()
            .indeterminate_byte_length_comparison_result
            .reason
        )
    ),
)
def test_indeterminacy_reason_is_preserved_without_interpretation(
    reason: object,
) -> None:
    length_binding = create_indeterminate_byte_length_binding()
    result = replace(
        length_binding.indeterminate_byte_length_comparison_result,
        reason=reason,
    )
    length_binding = replace(
        length_binding,
        indeterminate_byte_length_comparison_result=result,
    )
    binding = create_recorded_binding(
        indeterminate_byte_length_comparison_result_binding=length_binding,
    )
    assert (
        binding
        .indeterminate_byte_length_comparison_result_binding
        .indeterminate_byte_length_comparison_result
        .reason
        is reason
    )


def test_determined_at_is_preserved_without_replacement() -> None:
    length_binding = create_indeterminate_byte_length_binding()
    result = length_binding.indeterminate_byte_length_comparison_result
    determined_at = result.determined_at + timedelta(seconds=1)
    length_binding = replace(
        length_binding,
        indeterminate_byte_length_comparison_result=replace(
            result,
            determined_at=determined_at,
        ),
    )
    binding = create_recorded_binding(
        indeterminate_byte_length_comparison_result_binding=length_binding,
    )
    assert (
        binding
        .indeterminate_byte_length_comparison_result_binding
        .indeterminate_byte_length_comparison_result
        .determined_at
        is determined_at
    )


def test_conclusive_binding_cannot_occupy_indeterminate_slot() -> None:
    with pytest.raises(TypeError):
        SecurityAdmissionEvaluationRecordIndeterminateByteLengthComparisonResultBinding(
            evaluation_record=create_record(),
            indeterminate_byte_length_comparison_result_binding=(
                create_conclusive_byte_length_binding()  # type: ignore[arg-type]
            ),
        )


def test_candidate_policy_time_and_reason_are_not_duplicated() -> None:
    names = {
        field.name
        for field in fields(
            SecurityAdmissionEvaluationRecordIndeterminateByteLengthComparisonResultBinding
        )
    }
    assert names.isdisjoint(
        {
            "candidate_identity",
            "admission_policy_identity",
            "evaluated_at",
            "determined_at",
            "reason",
        }
    )


def test_rejection_cardinality_and_authority_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(
            SecurityAdmissionEvaluationRecordIndeterminateByteLengthComparisonResultBinding
        )
    }
    assert names.isdisjoint(
        {
            "evidence",
            "evidence_items",
            "evidence_bindings",
            "status",
            "decision",
            "admitted",
            "rejected",
            "authorized",
            "authorization",
            "quarantine",
            "retention",
        }
    )


def test_contract_performs_no_policy_or_comparison_execution() -> None:
    source = inspect.getsource(
        SecurityAdmissionEvaluationRecordIndeterminateByteLengthComparisonResultBinding
    )
    tree = ast.parse(source)
    forbidden_calls = {
        "compare",
        "evaluate",
        "execute",
        "authorize",
        "persist",
        "save",
    }
    called_names = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    assert called_names.isdisjoint(forbidden_calls)


def test_contract_imports_no_external_capability() -> None:
    module = inspect.getmodule(
        SecurityAdmissionEvaluationRecordIndeterminateByteLengthComparisonResultBinding
    )
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
    assert imported_roots == {"dataclasses", "sp001"}


def test_contract_defines_validation_only() -> None:
    module = inspect.getmodule(
        SecurityAdmissionEvaluationRecordIndeterminateByteLengthComparisonResultBinding
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    functions = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    assert functions == {"__post_init__"}
