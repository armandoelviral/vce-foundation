import ast
import inspect
from dataclasses import FrozenInstanceError, fields, replace

import pytest

from sp001.contracts.security_admission_candidate_media_type_comparison_result_binding import (
    SecurityAdmissionCandidateMediaTypeComparisonResultBinding,
)
from sp001.contracts.security_admission_evaluation_record import (
    SecurityAdmissionEvaluationRecord,
)
from sp001.contracts.security_admission_evaluation_record_media_type_comparison_result_binding import (
    SecurityAdmissionEvaluationRecordMediaTypeComparisonResultBinding,
)
from tests.test_security_admission_candidate_indeterminate_media_type_comparison_result_binding import (
    create_binding as create_indeterminate_media_type_binding,
)
from tests.test_security_admission_candidate_media_type_comparison_result_binding import (
    create_binding as create_media_type_binding,
)
from tests.test_security_admission_evaluation_record import create_record


def create_recorded_binding(
    *,
    evaluation_record: SecurityAdmissionEvaluationRecord | None = None,
    media_type_comparison_result_binding: (
        SecurityAdmissionCandidateMediaTypeComparisonResultBinding | None
    ) = None,
) -> SecurityAdmissionEvaluationRecordMediaTypeComparisonResultBinding:
    media_binding = (
        create_media_type_binding()
        if media_type_comparison_result_binding is None
        else media_type_comparison_result_binding
    )
    record = create_record() if evaluation_record is None else evaluation_record
    matching_identity = replace(
        record.evaluation_identity,
        evaluation_basis=media_binding.evaluation_basis,
    )
    matching_record = replace(
        record,
        evaluation_identity=matching_identity,
    )
    return SecurityAdmissionEvaluationRecordMediaTypeComparisonResultBinding(
        evaluation_record=matching_record,
        media_type_comparison_result_binding=media_binding,
    )


def test_recorded_binding_fields_are_exact() -> None:
    binding_fields = fields(
        SecurityAdmissionEvaluationRecordMediaTypeComparisonResultBinding
    )

    assert tuple(field.name for field in binding_fields) == (
        "evaluation_record",
        "media_type_comparison_result_binding",
    )
    assert binding_fields[0].type is SecurityAdmissionEvaluationRecord
    assert (
        binding_fields[1].type
        is SecurityAdmissionCandidateMediaTypeComparisonResultBinding
    )


def test_recorded_binding_is_immutable() -> None:
    binding = create_recorded_binding()

    with pytest.raises(FrozenInstanceError):
        binding.evaluation_record = create_record()  # type: ignore[misc]


def test_recorded_binding_uses_slots() -> None:
    binding = create_recorded_binding()

    assert hasattr(
        SecurityAdmissionEvaluationRecordMediaTypeComparisonResultBinding,
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
        SecurityAdmissionEvaluationRecordMediaTypeComparisonResultBinding(
            evaluation_record=invalid_value,  # type: ignore[arg-type]
            media_type_comparison_result_binding=create_media_type_binding(),
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_media_type_result_binding_requires_exact_type(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "media_type_comparison_result_binding must be a "
            "SecurityAdmissionCandidateMediaTypeComparisonResultBinding"
        ),
    ):
        SecurityAdmissionEvaluationRecordMediaTypeComparisonResultBinding(
            evaluation_record=create_record(),
            media_type_comparison_result_binding=(
                invalid_value  # type: ignore[arg-type]
            ),
        )


def test_exact_evaluation_record_reference_is_preserved() -> None:
    binding = create_recorded_binding()
    record = binding.evaluation_record

    reconstructed = (
        SecurityAdmissionEvaluationRecordMediaTypeComparisonResultBinding(
            evaluation_record=record,
            media_type_comparison_result_binding=(
                binding.media_type_comparison_result_binding
            ),
        )
    )

    assert reconstructed.evaluation_record is record


def test_exact_media_type_binding_reference_is_preserved() -> None:
    media_binding = create_media_type_binding()
    binding = create_recorded_binding(
        media_type_comparison_result_binding=media_binding,
    )

    assert binding.media_type_comparison_result_binding is media_binding


def test_reconstructed_equal_binding_has_value_equality() -> None:
    binding = create_recorded_binding()
    reconstructed = (
        SecurityAdmissionEvaluationRecordMediaTypeComparisonResultBinding(
            evaluation_record=replace(binding.evaluation_record),
            media_type_comparison_result_binding=replace(
                binding.media_type_comparison_result_binding
            ),
        )
    )

    assert reconstructed == binding
    assert reconstructed is not binding


def test_equal_reconstructed_basis_permits_binding() -> None:
    media_binding = create_media_type_binding()
    record = create_record()
    reconstructed_basis = replace(media_binding.evaluation_basis)
    identity = replace(
        record.evaluation_identity,
        evaluation_basis=reconstructed_basis,
    )
    record = replace(record, evaluation_identity=identity)

    binding = (
        SecurityAdmissionEvaluationRecordMediaTypeComparisonResultBinding(
            evaluation_record=record,
            media_type_comparison_result_binding=media_binding,
        )
    )

    assert (
        binding.evaluation_record.evaluation_identity.evaluation_basis
        == binding.media_type_comparison_result_binding.evaluation_basis
    )
    assert (
        binding.evaluation_record.evaluation_identity.evaluation_basis
        is not binding.media_type_comparison_result_binding.evaluation_basis
    )


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
    different_identity = replace(
        binding.evaluation_record.evaluation_identity,
        evaluation_basis=different_basis,
    )
    different_record = replace(
        binding.evaluation_record,
        evaluation_identity=different_identity,
    )

    with pytest.raises(
        ValueError,
        match="media-type result binding must use evaluation record basis",
    ):
        SecurityAdmissionEvaluationRecordMediaTypeComparisonResultBinding(
            evaluation_record=different_record,
            media_type_comparison_result_binding=(
                binding.media_type_comparison_result_binding
            ),
        )


@pytest.mark.parametrize(
    "match_status",
    tuple(
        type(
            create_media_type_binding()
            .media_type_comparison_result
            .match_status
        )
    ),
)
def test_conclusive_status_is_preserved_without_interpretation(
    match_status: object,
) -> None:
    media_binding = create_media_type_binding()
    result = replace(
        media_binding.media_type_comparison_result,
        match_status=match_status,
    )
    media_binding = replace(
        media_binding,
        media_type_comparison_result=result,
    )
    binding = create_recorded_binding(
        media_type_comparison_result_binding=media_binding,
    )

    assert (
        binding
        .media_type_comparison_result_binding
        .media_type_comparison_result
        .match_status
        is match_status
    )


def test_indeterminate_binding_cannot_occupy_conclusive_slot() -> None:
    with pytest.raises(TypeError):
        SecurityAdmissionEvaluationRecordMediaTypeComparisonResultBinding(
            evaluation_record=create_record(),
            media_type_comparison_result_binding=(
                create_indeterminate_media_type_binding()  # type: ignore[arg-type]
            ),
        )


def test_candidate_policy_and_time_are_not_duplicated_as_fields() -> None:
    names = {
        field.name
        for field in fields(
            SecurityAdmissionEvaluationRecordMediaTypeComparisonResultBinding
        )
    }

    assert names.isdisjoint(
        {
            "candidate_identity",
            "admission_policy_identity",
            "evaluated_at",
            "compared_at",
        }
    )


def test_classification_cardinality_and_authority_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(
            SecurityAdmissionEvaluationRecordMediaTypeComparisonResultBinding
        )
    }

    assert names.isdisjoint(
        {
            "evidence",
            "evidence_items",
            "evidence_bindings",
            "status",
            "decision",
            "reason",
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
        SecurityAdmissionEvaluationRecordMediaTypeComparisonResultBinding
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
        SecurityAdmissionEvaluationRecordMediaTypeComparisonResultBinding
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
        SecurityAdmissionEvaluationRecordMediaTypeComparisonResultBinding
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    functions = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    assert functions == {"__post_init__"}
