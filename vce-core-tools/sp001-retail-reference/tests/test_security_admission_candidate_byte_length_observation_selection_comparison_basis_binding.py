import ast
import inspect

from dataclasses import FrozenInstanceError, fields, replace
from datetime import timedelta

import pytest

from sp001.contracts.security_admission_candidate_byte_length_comparison_basis import (
    SecurityAdmissionCandidateByteLengthComparisonBasis,
)
from sp001.contracts.security_admission_candidate_byte_length_observation_selection_comparison_basis_binding import (
    SecurityAdmissionCandidateByteLengthObservationSelectionComparisonBasisBinding,
)
from sp001.contracts.security_admission_candidate_byte_length_observation_selection_result import (
    SecurityAdmissionCandidateByteLengthObservationSelectionResult,
)
from tests.test_security_admission_candidate_byte_length_comparison_basis import (
    create_basis as create_comparison_basis,
)
from tests.test_security_admission_candidate_byte_length_observation_selection_result import (
    create_result as create_selection_result,
)


def create_binding(
) -> SecurityAdmissionCandidateByteLengthObservationSelectionComparisonBasisBinding:
    selection = create_selection_result()
    comparison_basis = replace(
        create_comparison_basis(),
        measured_byte_length_observation=selection.selected_observation,
    )
    return (
        SecurityAdmissionCandidateByteLengthObservationSelectionComparisonBasisBinding(
            observation_selection_result=selection,
            comparison_basis=comparison_basis,
        )
    )


def test_fields_are_exact() -> None:
    binding_fields = fields(
        SecurityAdmissionCandidateByteLengthObservationSelectionComparisonBasisBinding
    )
    assert tuple(field.name for field in binding_fields) == (
        "observation_selection_result",
        "comparison_basis",
    )
    assert (
        binding_fields[0].type
        is SecurityAdmissionCandidateByteLengthObservationSelectionResult
    )
    assert (
        binding_fields[1].type
        is SecurityAdmissionCandidateByteLengthComparisonBasis
    )


def test_binding_is_immutable_and_slotted() -> None:
    binding = create_binding()
    assert not hasattr(binding, "__dict__")
    with pytest.raises(FrozenInstanceError):
        binding.comparison_basis = (  # type: ignore[misc]
            create_comparison_basis()
        )


def test_exact_references_are_preserved() -> None:
    binding = create_binding()
    selection = binding.observation_selection_result
    comparison_basis = binding.comparison_basis
    reconstructed = (
        SecurityAdmissionCandidateByteLengthObservationSelectionComparisonBasisBinding(
            observation_selection_result=selection,
            comparison_basis=comparison_basis,
        )
    )
    assert reconstructed.observation_selection_result is selection
    assert reconstructed.comparison_basis is comparison_basis
    assert (
        reconstructed.comparison_basis.measured_byte_length_observation
        is selection.selected_observation
    )


def test_equal_reconstruction_has_value_equality() -> None:
    binding = create_binding()
    reconstructed = replace(
        binding,
        observation_selection_result=replace(
            binding.observation_selection_result
        ),
        comparison_basis=replace(binding.comparison_basis),
    )
    assert reconstructed == binding
    assert reconstructed is not binding


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_selection_result_requires_nominal_type(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "observation_selection_result must be a "
            "SecurityAdmissionCandidateByteLengthObservationSelectionResult"
        ),
    ):
        replace(
            create_binding(),
            observation_selection_result=invalid_value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_comparison_basis_requires_nominal_type(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "comparison_basis must be a "
            "SecurityAdmissionCandidateByteLengthComparisonBasis"
        ),
    ):
        replace(
            create_binding(),
            comparison_basis=invalid_value,  # type: ignore[arg-type]
        )


def test_equal_reconstructed_selected_observation_is_permitted() -> None:
    binding = create_binding()
    reconstructed_selected = replace(
        binding.observation_selection_result.selected_observation
    )
    comparison_basis = replace(
        binding.comparison_basis,
        measured_byte_length_observation=reconstructed_selected,
    )
    preserved = replace(
        binding,
        comparison_basis=comparison_basis,
    )
    assert preserved == binding
    assert (
        preserved.comparison_basis.measured_byte_length_observation
        is reconstructed_selected
    )


def test_different_observation_identity_is_rejected() -> None:
    binding = create_binding()
    different_observation = replace(
        binding.observation_selection_result.selected_observation,
        observation_id="observation-999",
    )
    comparison_basis = replace(
        binding.comparison_basis,
        measured_byte_length_observation=different_observation,
    )
    with pytest.raises(
        ValueError,
        match=(
            "comparison basis must use the selected "
            "byte-length observation"
        ),
    ):
        replace(binding, comparison_basis=comparison_basis)


def test_different_observation_version_is_rejected() -> None:
    binding = create_binding()
    selected = binding.observation_selection_result.selected_observation
    different_observation = replace(
        selected,
        observation_version=selected.observation_version + 1,
    )
    comparison_basis = replace(
        binding.comparison_basis,
        measured_byte_length_observation=different_observation,
    )
    with pytest.raises(ValueError, match="selected byte-length observation"):
        replace(binding, comparison_basis=comparison_basis)


def test_different_observation_time_is_rejected() -> None:
    binding = create_binding()
    selected = binding.observation_selection_result.selected_observation
    different_observation = replace(
        selected,
        observed_at=selected.observed_at + timedelta(microseconds=1),
    )
    comparison_basis = replace(
        binding.comparison_basis,
        measured_byte_length_observation=different_observation,
    )
    with pytest.raises(ValueError, match="selected byte-length observation"):
        replace(binding, comparison_basis=comparison_basis)


def test_different_detected_value_is_rejected() -> None:
    binding = create_binding()
    selected = binding.observation_selection_result.selected_observation
    different_observation = replace(
        selected,
        measured_byte_length=(
            selected.measured_byte_length + 1
        ),
    )
    comparison_basis = replace(
        binding.comparison_basis,
        measured_byte_length_observation=different_observation,
    )
    with pytest.raises(ValueError, match="selected byte-length observation"):
        replace(binding, comparison_basis=comparison_basis)


def test_comparison_scheme_participates_in_binding_value() -> None:
    binding = create_binding()
    changed_basis = replace(
        binding.comparison_basis,
        comparison_scheme_version=(
            binding.comparison_basis.comparison_scheme_version + 1
        ),
    )
    assert replace(binding, comparison_basis=changed_basis) != binding


def test_selection_result_participates_in_binding_value() -> None:
    binding = create_binding()
    changed_selection = replace(
        binding.observation_selection_result,
        result_version=(
            binding.observation_selection_result.result_version + 1
        ),
    )
    assert replace(
        binding,
        observation_selection_result=changed_selection,
    ) != binding


def test_result_decision_and_coverage_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(
            SecurityAdmissionCandidateByteLengthObservationSelectionComparisonBasisBinding
        )
    }
    assert names.isdisjoint({
        "comparison_result",
        "coverage_status",
        "decision",
        "admitted",
        "rejected",
        "authorized",
        "authorization",
    })


def test_contract_defines_validation_only() -> None:
    module = inspect.getmodule(
        SecurityAdmissionCandidateByteLengthObservationSelectionComparisonBasisBinding
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
        SecurityAdmissionCandidateByteLengthObservationSelectionComparisonBasisBinding
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    roots = {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    assert roots == {"dataclasses", "sp001"}
