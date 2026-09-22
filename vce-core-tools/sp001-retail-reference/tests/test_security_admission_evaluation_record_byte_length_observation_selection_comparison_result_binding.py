import ast
import inspect

from dataclasses import FrozenInstanceError, fields, replace

import pytest

from sp001.contracts.security_admission_candidate_byte_length_observation_selection_comparison_result_binding import (
    SecurityAdmissionCandidateByteLengthObservationSelectionComparisonResultBinding,
)
from sp001.contracts.security_admission_evaluation_record_byte_length_comparison_result_binding import (
    SecurityAdmissionEvaluationRecordByteLengthComparisonResultBinding,
)
from sp001.contracts.security_admission_evaluation_record_byte_length_observation_selection_comparison_result_binding import (
    SecurityAdmissionEvaluationRecordByteLengthObservationSelectionComparisonResultBinding,
)
from tests.test_security_admission_candidate_byte_length_observation_selection_comparison_result_binding import (
    create_binding as create_governed_binding,
)
from tests.test_security_admission_evaluation_record_byte_length_comparison_result_binding import (
    create_recorded_binding,
)


def create_binding(
) -> SecurityAdmissionEvaluationRecordByteLengthObservationSelectionComparisonResultBinding:
    governed = create_governed_binding()
    recorded = create_recorded_binding(
        byte_length_comparison_result_binding=(
            governed.byte_length_comparison_result_binding
        ),
    )
    return (
        SecurityAdmissionEvaluationRecordByteLengthObservationSelectionComparisonResultBinding(
            observation_selection_comparison_result_binding=governed,
            evaluation_record_byte_length_comparison_result_binding=recorded,
        )
    )


def test_fields_are_exact() -> None:
    binding_fields = fields(
        SecurityAdmissionEvaluationRecordByteLengthObservationSelectionComparisonResultBinding
    )
    assert tuple(field.name for field in binding_fields) == (
        "observation_selection_comparison_result_binding",
        "evaluation_record_byte_length_comparison_result_binding",
    )
    assert (
        binding_fields[0].type
        is SecurityAdmissionCandidateByteLengthObservationSelectionComparisonResultBinding
    )
    assert (
        binding_fields[1].type
        is SecurityAdmissionEvaluationRecordByteLengthComparisonResultBinding
    )


def test_binding_is_immutable_and_slotted() -> None:
    binding = create_binding()
    assert not hasattr(binding, "__dict__")
    with pytest.raises(FrozenInstanceError):
        binding.evaluation_record_byte_length_comparison_result_binding = (  # type: ignore[misc]
            create_recorded_binding()
        )


def test_exact_references_are_preserved() -> None:
    binding = create_binding()
    governed = binding.observation_selection_comparison_result_binding
    recorded = (
        binding.evaluation_record_byte_length_comparison_result_binding
    )
    reconstructed = (
        SecurityAdmissionEvaluationRecordByteLengthObservationSelectionComparisonResultBinding(
            observation_selection_comparison_result_binding=governed,
            evaluation_record_byte_length_comparison_result_binding=recorded,
        )
    )
    assert (
        reconstructed.observation_selection_comparison_result_binding
        is governed
    )
    assert (
        reconstructed.evaluation_record_byte_length_comparison_result_binding
        is recorded
    )


def test_governed_result_is_preserved_in_recorded_evaluation() -> None:
    binding = create_binding()
    governed_result = (
        binding.observation_selection_comparison_result_binding
        .byte_length_comparison_result_binding
    )
    recorded_result = (
        binding.evaluation_record_byte_length_comparison_result_binding
        .byte_length_comparison_result_binding
    )
    assert recorded_result is governed_result


def test_complete_selection_and_evaluation_lineage_remains_reachable() -> None:
    binding = create_binding()
    governed = binding.observation_selection_comparison_result_binding
    recorded = (
        binding.evaluation_record_byte_length_comparison_result_binding
    )
    selection = (
        governed.observation_selection_comparison_basis_binding
        .observation_selection_result
    )
    assert selection.selected_observation is not None
    assert recorded.evaluation_record.evaluation_identity is not None
    assert (
        recorded.evaluation_record.evaluation_identity.evaluation_basis
        == governed.byte_length_comparison_result_binding.evaluation_basis
    )


def test_equal_reconstruction_has_value_equality() -> None:
    binding = create_binding()
    reconstructed = replace(
        binding,
        observation_selection_comparison_result_binding=replace(
            binding.observation_selection_comparison_result_binding
        ),
        evaluation_record_byte_length_comparison_result_binding=replace(
            binding.evaluation_record_byte_length_comparison_result_binding
        ),
    )
    assert reconstructed == binding
    assert reconstructed is not binding


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_governed_binding_requires_nominal_type(
    invalid_value: object,
) -> None:
    recorded = (
        create_binding()
        .evaluation_record_byte_length_comparison_result_binding
    )
    with pytest.raises(
        TypeError,
        match=(
            "observation_selection_comparison_result_binding must be a "
            "SecurityAdmissionCandidateByteLengthObservationSelection"
            "ComparisonResultBinding"
        ),
    ):
        SecurityAdmissionEvaluationRecordByteLengthObservationSelectionComparisonResultBinding(
            observation_selection_comparison_result_binding=(
                invalid_value  # type: ignore[arg-type]
            ),
            evaluation_record_byte_length_comparison_result_binding=recorded,
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_recorded_binding_requires_nominal_type(
    invalid_value: object,
) -> None:
    governed = (
        create_binding().observation_selection_comparison_result_binding
    )
    with pytest.raises(
        TypeError,
        match=(
            "evaluation_record_byte_length_comparison_result_binding "
            "must be a "
            "SecurityAdmissionEvaluationRecordByteLength"
            "ComparisonResultBinding"
        ),
    ):
        SecurityAdmissionEvaluationRecordByteLengthObservationSelectionComparisonResultBinding(
            observation_selection_comparison_result_binding=governed,
            evaluation_record_byte_length_comparison_result_binding=(
                invalid_value  # type: ignore[arg-type]
            ),
        )


def test_different_candidate_result_binding_is_rejected() -> None:
    governed = create_governed_binding()
    candidate_result_binding = (
        governed.byte_length_comparison_result_binding
    )
    changed_result = replace(
        candidate_result_binding.byte_length_comparison_result,
        result_version=(
            candidate_result_binding
            .byte_length_comparison_result
            .result_version
            + 1
        ),
    )
    changed_candidate_result_binding = replace(
        candidate_result_binding,
        byte_length_comparison_result=changed_result,
    )
    recorded = create_recorded_binding(
        byte_length_comparison_result_binding=(
            changed_candidate_result_binding
        ),
    )
    with pytest.raises(
        ValueError,
        match=(
            "recorded byte-length result must use the governed "
            "comparison result binding"
        ),
    ):
        SecurityAdmissionEvaluationRecordByteLengthObservationSelectionComparisonResultBinding(
            observation_selection_comparison_result_binding=governed,
            evaluation_record_byte_length_comparison_result_binding=recorded,
        )


def test_contract_defines_no_coverage_decision_or_rejection() -> None:
    assert tuple(
        field.name
        for field in fields(
            SecurityAdmissionEvaluationRecordByteLengthObservationSelectionComparisonResultBinding
        )
    ) == (
        "observation_selection_comparison_result_binding",
        "evaluation_record_byte_length_comparison_result_binding",
    )


def test_contract_defines_validation_only() -> None:
    module = inspect.getmodule(
        SecurityAdmissionEvaluationRecordByteLengthObservationSelectionComparisonResultBinding
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
        SecurityAdmissionEvaluationRecordByteLengthObservationSelectionComparisonResultBinding
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    roots = {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    assert roots == {"dataclasses", "sp001"}
