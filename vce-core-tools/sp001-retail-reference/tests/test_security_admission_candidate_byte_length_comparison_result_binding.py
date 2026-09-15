from dataclasses import FrozenInstanceError, fields, replace

import ast
import inspect

import pytest

from sp001.contracts.security_admission_candidate_byte_length_comparison_result import (
    SecurityAdmissionByteLengthComparisonStatus,
    SecurityAdmissionCandidateByteLengthComparisonResult,
)
from sp001.contracts.security_admission_candidate_byte_length_comparison_result_binding import (
    SecurityAdmissionCandidateByteLengthComparisonResultBinding,
)
from sp001.contracts.security_admission_evaluation_basis import (
    SecurityAdmissionEvaluationBasis,
)
from tests.test_security_admission_candidate_byte_length_comparison_result import (
    create_result,
)
from tests.test_security_admission_candidate_indeterminate_byte_length_comparison_result import (
    create_result as create_indeterminate_result,
)
from tests.test_security_admission_evaluation_basis import (
    create_basis as create_evaluation_basis,
)


def candidate_from_result(
    result: SecurityAdmissionCandidateByteLengthComparisonResult,
):
    return (
        result
        .comparison_basis
        .declared_byte_length
        .metadata_identity
        .candidate_identity
    )


def evaluation_basis_for_result(
    result: SecurityAdmissionCandidateByteLengthComparisonResult,
) -> SecurityAdmissionEvaluationBasis:
    return SecurityAdmissionEvaluationBasis(
        candidate_identity=candidate_from_result(result),
        admission_policy_identity=(
            create_evaluation_basis().admission_policy_identity
        ),
    )


def create_binding(
) -> SecurityAdmissionCandidateByteLengthComparisonResultBinding:
    result = create_result()
    return SecurityAdmissionCandidateByteLengthComparisonResultBinding(
        evaluation_basis=evaluation_basis_for_result(result),
        byte_length_comparison_result=result,
    )


def test_binding_fields_are_exact() -> None:
    binding_fields = fields(
        SecurityAdmissionCandidateByteLengthComparisonResultBinding
    )

    assert tuple(field.name for field in binding_fields) == (
        "evaluation_basis",
        "byte_length_comparison_result",
    )
    assert binding_fields[0].type is SecurityAdmissionEvaluationBasis
    assert (
        binding_fields[1].type
        is SecurityAdmissionCandidateByteLengthComparisonResult
    )


def test_binding_is_immutable() -> None:
    binding = create_binding()

    with pytest.raises(FrozenInstanceError):
        binding.evaluation_basis = binding.evaluation_basis


def test_binding_uses_slots() -> None:
    binding = create_binding()

    assert hasattr(
        SecurityAdmissionCandidateByteLengthComparisonResultBinding,
        "__slots__",
    )
    assert not hasattr(binding, "__dict__")


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_evaluation_basis_requires_exact_type(invalid_value) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "evaluation_basis must be a "
            "SecurityAdmissionEvaluationBasis"
        ),
    ):
        SecurityAdmissionCandidateByteLengthComparisonResultBinding(
            evaluation_basis=invalid_value,
            byte_length_comparison_result=create_result(),
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_byte_length_result_requires_exact_type(invalid_value) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "byte_length_comparison_result must be a "
            "SecurityAdmissionCandidateByteLengthComparisonResult"
        ),
    ):
        SecurityAdmissionCandidateByteLengthComparisonResultBinding(
            evaluation_basis=create_evaluation_basis(),
            byte_length_comparison_result=invalid_value,
        )


def test_exact_evaluation_basis_reference_is_preserved() -> None:
    result = create_result()
    evaluation_basis = evaluation_basis_for_result(result)
    binding = SecurityAdmissionCandidateByteLengthComparisonResultBinding(
        evaluation_basis=evaluation_basis,
        byte_length_comparison_result=result,
    )

    assert binding.evaluation_basis is evaluation_basis


def test_exact_result_reference_is_preserved() -> None:
    result = create_result()
    binding = SecurityAdmissionCandidateByteLengthComparisonResultBinding(
        evaluation_basis=evaluation_basis_for_result(result),
        byte_length_comparison_result=result,
    )

    assert binding.byte_length_comparison_result is result


def test_reconstructed_equal_binding_has_value_equality() -> None:
    binding = create_binding()
    reconstructed = (
        SecurityAdmissionCandidateByteLengthComparisonResultBinding(
            evaluation_basis=replace(binding.evaluation_basis),
            byte_length_comparison_result=replace(
                binding.byte_length_comparison_result
            ),
        )
    )

    assert reconstructed == binding
    assert reconstructed is not binding


def test_equal_reconstructed_candidate_permits_binding() -> None:
    result = create_result()
    candidate = replace(candidate_from_result(result))
    evaluation_basis = SecurityAdmissionEvaluationBasis(
        candidate_identity=candidate,
        admission_policy_identity=(
            create_evaluation_basis().admission_policy_identity
        ),
    )

    binding = SecurityAdmissionCandidateByteLengthComparisonResultBinding(
        evaluation_basis=evaluation_basis,
        byte_length_comparison_result=result,
    )

    assert binding.evaluation_basis.candidate_identity == candidate


def test_different_candidate_is_rejected() -> None:
    result = create_result()
    different_candidate = replace(
        candidate_from_result(result),
        candidate_id="candidate-002",
    )
    evaluation_basis = SecurityAdmissionEvaluationBasis(
        candidate_identity=different_candidate,
        admission_policy_identity=(
            create_evaluation_basis().admission_policy_identity
        ),
    )

    with pytest.raises(
        ValueError,
        match=(
            "byte-length comparison result candidate_identity "
            "does not match evaluation_basis"
        ),
    ):
        SecurityAdmissionCandidateByteLengthComparisonResultBinding(
            evaluation_basis=evaluation_basis,
            byte_length_comparison_result=result,
        )


@pytest.mark.parametrize(
    "status",
    tuple(SecurityAdmissionByteLengthComparisonStatus),
)
def test_conclusive_status_is_preserved_without_interpretation(
    status: SecurityAdmissionByteLengthComparisonStatus,
) -> None:
    result = replace(create_result(), match_status=status)
    binding = SecurityAdmissionCandidateByteLengthComparisonResultBinding(
        evaluation_basis=evaluation_basis_for_result(result),
        byte_length_comparison_result=result,
    )

    assert binding.byte_length_comparison_result.match_status is status


def test_indeterminate_result_cannot_occupy_conclusive_slot() -> None:
    with pytest.raises(TypeError):
        SecurityAdmissionCandidateByteLengthComparisonResultBinding(
            evaluation_basis=create_evaluation_basis(),
            byte_length_comparison_result=create_indeterminate_result(),
        )


def test_policy_and_candidate_are_not_duplicated_as_fields() -> None:
    names = {
        field.name
        for field in fields(
            SecurityAdmissionCandidateByteLengthComparisonResultBinding
        )
    }

    assert "candidate_identity" not in names
    assert "admission_policy_identity" not in names


def test_classification_event_and_authority_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(
            SecurityAdmissionCandidateByteLengthComparisonResultBinding
        )
    }
    forbidden = {
        "binding_id",
        "binding_version",
        "status",
        "decision",
        "reason",
        "evaluated_at",
        "actor",
        "authorized",
        "quarantine",
        "retention",
    }

    assert names.isdisjoint(forbidden)


def test_contract_performs_no_policy_or_comparison_execution() -> None:
    module = inspect.getmodule(
        SecurityAdmissionCandidateByteLengthComparisonResultBinding
    )
    assert module is not None
    source = inspect.getsource(module)

    assert ".evaluate(" not in source
    assert ".compare(" not in source
    assert ".execute(" not in source
    assert ".authorize(" not in source


def test_contract_imports_no_external_capability() -> None:
    module = inspect.getmodule(
        SecurityAdmissionCandidateByteLengthComparisonResultBinding
    )
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
        "SecurityAdmissionCandidateByteLengthComparisonResult",
        "SecurityAdmissionEvaluationBasis",
    }


def test_contract_defines_validation_only() -> None:
    module = inspect.getmodule(
        SecurityAdmissionCandidateByteLengthComparisonResultBinding
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    functions = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    assert functions == {"__post_init__"}
