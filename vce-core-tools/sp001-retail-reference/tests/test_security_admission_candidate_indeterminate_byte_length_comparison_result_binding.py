from dataclasses import FrozenInstanceError, fields, replace

import ast
import inspect

import pytest

from sp001.contracts.security_admission_candidate_indeterminate_byte_length_comparison_result import (
    SecurityAdmissionByteLengthComparisonIndeterminacyReason,
    SecurityAdmissionCandidateIndeterminateByteLengthComparisonResult,
)
from sp001.contracts.security_admission_candidate_indeterminate_byte_length_comparison_result_binding import (
    SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding,
)
from sp001.contracts.security_admission_evaluation_basis import (
    SecurityAdmissionEvaluationBasis,
)
from tests.test_security_admission_candidate_byte_length_comparison_result import (
    create_result as create_conclusive_result,
)
from tests.test_security_admission_candidate_indeterminate_byte_length_comparison_result import (
    create_result,
)
from tests.test_security_admission_evaluation_basis import (
    create_basis as create_evaluation_basis,
)


def candidate_from_result(
    result: SecurityAdmissionCandidateIndeterminateByteLengthComparisonResult,
):
    return (
        result
        .comparison_basis
        .declared_byte_length
        .metadata_identity
        .candidate_identity
    )


def evaluation_basis_for_result(
    result: SecurityAdmissionCandidateIndeterminateByteLengthComparisonResult,
) -> SecurityAdmissionEvaluationBasis:
    return SecurityAdmissionEvaluationBasis(
        candidate_identity=candidate_from_result(result),
        admission_policy_identity=(
            create_evaluation_basis().admission_policy_identity
        ),
    )


def create_binding(
) -> SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding:
    result = create_result()
    return (
        SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding(
            evaluation_basis=evaluation_basis_for_result(result),
            indeterminate_byte_length_comparison_result=result,
        )
    )


def test_binding_fields_are_exact() -> None:
    binding_fields = fields(
        SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding
    )

    assert tuple(field.name for field in binding_fields) == (
        "evaluation_basis",
        "indeterminate_byte_length_comparison_result",
    )
    assert binding_fields[0].type is SecurityAdmissionEvaluationBasis
    assert (
        binding_fields[1].type
        is SecurityAdmissionCandidateIndeterminateByteLengthComparisonResult
    )


def test_binding_is_immutable() -> None:
    binding = create_binding()

    with pytest.raises(FrozenInstanceError):
        binding.evaluation_basis = binding.evaluation_basis


def test_binding_uses_slots() -> None:
    binding = create_binding()

    assert hasattr(
        SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding,
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
        SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding(
            evaluation_basis=invalid_value,
            indeterminate_byte_length_comparison_result=create_result(),
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_indeterminate_result_requires_exact_type(invalid_value) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "indeterminate_byte_length_comparison_result must be a "
            "SecurityAdmissionCandidateIndeterminateByteLengthComparisonResult"
        ),
    ):
        SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding(
            evaluation_basis=create_evaluation_basis(),
            indeterminate_byte_length_comparison_result=invalid_value,
        )


def test_exact_evaluation_basis_reference_is_preserved() -> None:
    result = create_result()
    evaluation_basis = evaluation_basis_for_result(result)
    binding = (
        SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding(
            evaluation_basis=evaluation_basis,
            indeterminate_byte_length_comparison_result=result,
        )
    )

    assert binding.evaluation_basis is evaluation_basis


def test_exact_indeterminate_result_reference_is_preserved() -> None:
    result = create_result()
    binding = (
        SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding(
            evaluation_basis=evaluation_basis_for_result(result),
            indeterminate_byte_length_comparison_result=result,
        )
    )

    assert binding.indeterminate_byte_length_comparison_result is result


def test_reconstructed_equal_binding_has_value_equality() -> None:
    binding = create_binding()
    reconstructed = (
        SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding(
            evaluation_basis=replace(binding.evaluation_basis),
            indeterminate_byte_length_comparison_result=replace(
                binding.indeterminate_byte_length_comparison_result
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

    binding = (
        SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding(
            evaluation_basis=evaluation_basis,
            indeterminate_byte_length_comparison_result=result,
        )
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
            "indeterminate byte-length comparison result "
            "candidate_identity does not match evaluation_basis"
        ),
    ):
        SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding(
            evaluation_basis=evaluation_basis,
            indeterminate_byte_length_comparison_result=result,
        )


@pytest.mark.parametrize(
    "reason",
    tuple(SecurityAdmissionByteLengthComparisonIndeterminacyReason),
)
def test_indeterminacy_reason_is_preserved_without_interpretation(
    reason: SecurityAdmissionByteLengthComparisonIndeterminacyReason,
) -> None:
    result = replace(create_result(), reason=reason)
    binding = (
        SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding(
            evaluation_basis=evaluation_basis_for_result(result),
            indeterminate_byte_length_comparison_result=result,
        )
    )

    assert (
        binding.indeterminate_byte_length_comparison_result.reason
        is reason
    )


def test_determined_at_is_preserved_without_replacement() -> None:
    result = create_result()
    binding = (
        SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding(
            evaluation_basis=evaluation_basis_for_result(result),
            indeterminate_byte_length_comparison_result=result,
        )
    )

    assert (
        binding.indeterminate_byte_length_comparison_result.determined_at
        is result.determined_at
    )


def test_conclusive_result_cannot_occupy_indeterminate_slot() -> None:
    with pytest.raises(TypeError):
        SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding(
            evaluation_basis=create_evaluation_basis(),
            indeterminate_byte_length_comparison_result=(
                create_conclusive_result()
            ),
        )


def test_policy_and_candidate_are_not_duplicated_as_fields() -> None:
    names = {
        field.name
        for field in fields(
            SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding
        )
    }

    assert "candidate_identity" not in names
    assert "admission_policy_identity" not in names


def test_rejection_classification_and_authority_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(
            SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding
        )
    }
    forbidden = {
        "binding_id",
        "binding_version",
        "status",
        "decision",
        "rejected",
        "evaluated_at",
        "actor",
        "authorized",
        "quarantine",
        "retention",
    }

    assert names.isdisjoint(forbidden)


def test_contract_performs_no_policy_or_comparison_execution() -> None:
    module = inspect.getmodule(
        SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding
    )
    assert module is not None
    source = inspect.getsource(module)

    assert ".evaluate(" not in source
    assert ".compare(" not in source
    assert ".execute(" not in source
    assert ".authorize(" not in source


def test_contract_imports_no_external_capability() -> None:
    module = inspect.getmodule(
        SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding
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
        "SecurityAdmissionCandidateIndeterminateByteLengthComparisonResult",
        "SecurityAdmissionEvaluationBasis",
    }


def test_contract_defines_validation_only() -> None:
    module = inspect.getmodule(
        SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    functions = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    assert functions == {"__post_init__"}
