import ast
import inspect

from dataclasses import FrozenInstanceError, fields, replace

import pytest

from sp001.contracts.security_admission_candidate_indeterminate_byte_length_comparison_result_binding import (
    SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding,
)
from sp001.contracts.security_admission_candidate_byte_length_observation_selection_comparison_basis_binding import (
    SecurityAdmissionCandidateByteLengthObservationSelectionComparisonBasisBinding,
)
from sp001.contracts.security_admission_candidate_byte_length_observation_selection_indeterminate_comparison_result_binding import (
    SecurityAdmissionCandidateByteLengthObservationSelectionIndeterminateComparisonResultBinding,
)
from tests.test_security_admission_candidate_indeterminate_byte_length_comparison_result_binding import (
    create_binding as create_result_binding,
)
from tests.test_security_admission_candidate_byte_length_observation_selection_comparison_basis_binding import (
    create_binding as create_governed_basis_binding,
)


def create_binding(
) -> SecurityAdmissionCandidateByteLengthObservationSelectionIndeterminateComparisonResultBinding:
    governed = create_governed_basis_binding()
    initial_result_binding = create_result_binding()
    comparison_result = replace(
        initial_result_binding.indeterminate_byte_length_comparison_result,
        comparison_basis=governed.comparison_basis,
    )
    result_binding = replace(
        initial_result_binding,
        indeterminate_byte_length_comparison_result=comparison_result,
    )
    return (
        SecurityAdmissionCandidateByteLengthObservationSelectionIndeterminateComparisonResultBinding(
            observation_selection_comparison_basis_binding=governed,
            indeterminate_byte_length_comparison_result_binding=result_binding,
        )
    )


def test_fields_are_exact() -> None:
    binding_fields = fields(
        SecurityAdmissionCandidateByteLengthObservationSelectionIndeterminateComparisonResultBinding
    )
    assert tuple(field.name for field in binding_fields) == (
        "observation_selection_comparison_basis_binding",
        "indeterminate_byte_length_comparison_result_binding",
    )
    assert (
        binding_fields[0].type
        is SecurityAdmissionCandidateByteLengthObservationSelectionComparisonBasisBinding
    )
    assert (
        binding_fields[1].type
        is SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding
    )


def test_binding_is_immutable_and_slotted() -> None:
    binding = create_binding()
    assert not hasattr(binding, "__dict__")
    with pytest.raises(FrozenInstanceError):
        binding.indeterminate_byte_length_comparison_result_binding = (  # type: ignore[misc]
            create_result_binding()
        )


def test_exact_references_are_preserved() -> None:
    binding = create_binding()
    governed = (
        binding.observation_selection_comparison_basis_binding
    )
    result_binding = binding.indeterminate_byte_length_comparison_result_binding
    reconstructed = (
        SecurityAdmissionCandidateByteLengthObservationSelectionIndeterminateComparisonResultBinding(
            observation_selection_comparison_basis_binding=governed,
            indeterminate_byte_length_comparison_result_binding=result_binding,
        )
    )
    assert (
        reconstructed.observation_selection_comparison_basis_binding
        is governed
    )
    assert (
        reconstructed.indeterminate_byte_length_comparison_result_binding
        is result_binding
    )


def test_governed_basis_is_preserved_through_result() -> None:
    binding = create_binding()
    governed_basis = (
        binding.observation_selection_comparison_basis_binding
        .comparison_basis
    )
    result_basis = (
        binding.indeterminate_byte_length_comparison_result_binding
        .indeterminate_byte_length_comparison_result
        .comparison_basis
    )
    assert result_basis is governed_basis


def test_complete_selection_lineage_remains_reachable() -> None:
    binding = create_binding()
    governed = (
        binding.observation_selection_comparison_basis_binding
    )
    selection = governed.observation_selection_result
    assert selection.resolution_basis.observation_set.observations
    assert selection.resolution_basis.authority_order is not None
    assert governed.comparison_basis.measured_byte_length_observation == (
        selection.selected_observation
    )


def test_complete_indeterminate_result_remains_reachable() -> None:
    binding = create_binding()
    result = (
        binding.indeterminate_byte_length_comparison_result_binding
        .indeterminate_byte_length_comparison_result
    )
    assert result.result_id
    assert result.result_version > 0
    assert result.comparison_basis is (
        binding.observation_selection_comparison_basis_binding
        .comparison_basis
    )


def test_equal_reconstruction_has_value_equality() -> None:
    binding = create_binding()
    reconstructed = replace(
        binding,
        observation_selection_comparison_basis_binding=replace(
            binding.observation_selection_comparison_basis_binding
        ),
        indeterminate_byte_length_comparison_result_binding=replace(
            binding.indeterminate_byte_length_comparison_result_binding
        ),
    )
    assert reconstructed == binding
    assert reconstructed is not binding


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_governed_basis_binding_requires_nominal_type(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "observation_selection_comparison_basis_binding must be a "
            "SecurityAdmissionCandidateByteLengthObservationSelection"
            "ComparisonBasisBinding"
        ),
    ):
        replace(
            create_binding(),
            observation_selection_comparison_basis_binding=(
                invalid_value  # type: ignore[arg-type]
            ),
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_result_binding_requires_nominal_type(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "indeterminate_byte_length_comparison_result_binding must be a "
            "SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding"
        ),
    ):
        replace(
            create_binding(),
            indeterminate_byte_length_comparison_result_binding=(
                invalid_value  # type: ignore[arg-type]
            ),
        )


def test_equal_reconstructed_basis_is_permitted() -> None:
    binding = create_binding()
    result_binding = binding.indeterminate_byte_length_comparison_result_binding
    result = result_binding.indeterminate_byte_length_comparison_result
    reconstructed_basis = replace(result.comparison_basis)
    reconstructed_result = replace(
        result,
        comparison_basis=reconstructed_basis,
    )
    reconstructed_result_binding = replace(
        result_binding,
        indeterminate_byte_length_comparison_result=reconstructed_result,
    )
    preserved = replace(
        binding,
        indeterminate_byte_length_comparison_result_binding=(
            reconstructed_result_binding
        ),
    )
    assert preserved == binding


def test_different_comparison_scheme_is_rejected() -> None:
    binding = create_binding()
    result_binding = binding.indeterminate_byte_length_comparison_result_binding
    result = result_binding.indeterminate_byte_length_comparison_result
    different_basis = replace(
        result.comparison_basis,
        comparison_scheme_version=(
            result.comparison_basis.comparison_scheme_version + 1
        ),
    )
    different_result = replace(
        result,
        comparison_basis=different_basis,
    )
    different_result_binding = replace(
        result_binding,
        indeterminate_byte_length_comparison_result=different_result,
    )
    with pytest.raises(
        ValueError,
        match=(
            "indeterminate byte-length comparison result must use the governed "
            "comparison basis"
        ),
    ):
        replace(
            binding,
            indeterminate_byte_length_comparison_result_binding=(
                different_result_binding
            ),
        )


def test_different_selected_observation_basis_is_rejected() -> None:
    binding = create_binding()
    result_binding = binding.indeterminate_byte_length_comparison_result_binding
    result = result_binding.indeterminate_byte_length_comparison_result
    selected = result.comparison_basis.measured_byte_length_observation
    different_observation = replace(
        selected,
        observation_version=selected.observation_version + 1,
    )
    different_basis = replace(
        result.comparison_basis,
        measured_byte_length_observation=different_observation,
    )
    different_result = replace(
        result,
        comparison_basis=different_basis,
    )
    different_result_binding = replace(
        result_binding,
        indeterminate_byte_length_comparison_result=different_result,
    )
    with pytest.raises(
        ValueError,
        match="indeterminate byte-length comparison result must use the governed",
    ):
        replace(
            binding,
            indeterminate_byte_length_comparison_result_binding=(
                different_result_binding
            ),
        )

def test_evaluation_basis_remains_preserved() -> None:
    binding = create_binding()
    result_binding = binding.indeterminate_byte_length_comparison_result_binding
    assert result_binding.evaluation_basis is not None
    assert (
        result_binding.evaluation_basis.candidate_identity
        == binding.observation_selection_comparison_basis_binding
        .comparison_basis
        .declared_byte_length
        .metadata_identity
        .candidate_identity
    )


def test_each_binding_participates_in_value() -> None:
    binding = create_binding()
    changed_selection = replace(
        binding.observation_selection_comparison_basis_binding
        .observation_selection_result,
        result_version=(
            binding.observation_selection_comparison_basis_binding
            .observation_selection_result
            .result_version
            + 1
        ),
    )
    changed_governed = replace(
        binding.observation_selection_comparison_basis_binding,
        observation_selection_result=changed_selection,
    )
    assert replace(
        binding,
        observation_selection_comparison_basis_binding=changed_governed,
    ) != binding

    result_binding = binding.indeterminate_byte_length_comparison_result_binding
    changed_result = replace(
        result_binding.indeterminate_byte_length_comparison_result,
        result_version=(
            result_binding.indeterminate_byte_length_comparison_result.result_version + 1
        ),
    )
    changed_result_binding = replace(
        result_binding,
        indeterminate_byte_length_comparison_result=changed_result,
    )
    assert replace(
        binding,
        indeterminate_byte_length_comparison_result_binding=changed_result_binding,
    ) != binding


def test_decision_coverage_and_authority_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(
            SecurityAdmissionCandidateByteLengthObservationSelectionIndeterminateComparisonResultBinding
        )
    }
    assert names.isdisjoint({
        "coverage_status",
        "decision",
        "admitted",
        "rejected",
        "authorized",
        "authorization",
        "quarantine",
        "retention",
    })


def test_contract_defines_validation_only() -> None:
    module = inspect.getmodule(
        SecurityAdmissionCandidateByteLengthObservationSelectionIndeterminateComparisonResultBinding
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    functions = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    assert functions == {"__post_init__"}


def test_contract_imports_no_external_capability() -> None:
    module = inspect.getmodule(
        SecurityAdmissionCandidateByteLengthObservationSelectionIndeterminateComparisonResultBinding
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    roots = {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    assert roots == {"dataclasses", "sp001"}
