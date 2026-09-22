import ast
import inspect

from dataclasses import FrozenInstanceError, fields, replace

import pytest

from sp001.contracts.security_admission_candidate_media_type_observation_selection_indeterminate_comparison_result_binding import (
    SecurityAdmissionCandidateMediaTypeObservationSelectionIndeterminateComparisonResultBinding,
)
from sp001.contracts.security_admission_evaluation_record_indeterminate_media_type_comparison_result_binding import (
    SecurityAdmissionEvaluationRecordIndeterminateMediaTypeComparisonResultBinding,
)
from sp001.contracts.security_admission_evaluation_record_media_type_observation_selection_indeterminate_comparison_result_binding import (
    SecurityAdmissionEvaluationRecordMediaTypeObservationSelectionIndeterminateComparisonResultBinding,
)
from tests.test_security_admission_candidate_media_type_observation_selection_indeterminate_comparison_result_binding import (
    create_binding as create_governed_binding,
)
from tests.test_security_admission_evaluation_record_indeterminate_media_type_comparison_result_binding import (
    create_recorded_binding,
)


def create_binding(
) -> SecurityAdmissionEvaluationRecordMediaTypeObservationSelectionIndeterminateComparisonResultBinding:
    governed = create_governed_binding()
    recorded = create_recorded_binding(
        indeterminate_media_type_comparison_result_binding=(
            governed.indeterminate_media_type_comparison_result_binding
        ),
    )
    return (
        SecurityAdmissionEvaluationRecordMediaTypeObservationSelectionIndeterminateComparisonResultBinding(
            observation_selection_indeterminate_comparison_result_binding=governed,
            evaluation_record_indeterminate_media_type_comparison_result_binding=recorded,
        )
    )


def test_fields_are_exact() -> None:
    binding_fields = fields(
        SecurityAdmissionEvaluationRecordMediaTypeObservationSelectionIndeterminateComparisonResultBinding
    )
    assert tuple(field.name for field in binding_fields) == (
        "observation_selection_indeterminate_comparison_result_binding",
        "evaluation_record_indeterminate_media_type_comparison_result_binding",
    )
    assert (
        binding_fields[0].type
        is SecurityAdmissionCandidateMediaTypeObservationSelectionIndeterminateComparisonResultBinding
    )
    assert (
        binding_fields[1].type
        is SecurityAdmissionEvaluationRecordIndeterminateMediaTypeComparisonResultBinding
    )


def test_binding_is_immutable_and_slotted() -> None:
    binding = create_binding()
    assert not hasattr(binding, "__dict__")
    with pytest.raises(FrozenInstanceError):
        binding.evaluation_record_indeterminate_media_type_comparison_result_binding = (  # type: ignore[misc]
            create_recorded_binding()
        )


def test_exact_references_are_preserved() -> None:
    binding = create_binding()
    governed = binding.observation_selection_indeterminate_comparison_result_binding
    recorded = (
        binding.evaluation_record_indeterminate_media_type_comparison_result_binding
    )
    reconstructed = (
        SecurityAdmissionEvaluationRecordMediaTypeObservationSelectionIndeterminateComparisonResultBinding(
            observation_selection_indeterminate_comparison_result_binding=governed,
            evaluation_record_indeterminate_media_type_comparison_result_binding=recorded,
        )
    )
    assert (
        reconstructed.observation_selection_indeterminate_comparison_result_binding
        is governed
    )
    assert (
        reconstructed.evaluation_record_indeterminate_media_type_comparison_result_binding
        is recorded
    )


def test_governed_indeterminate_result_is_preserved_in_recorded_evaluation() -> None:
    binding = create_binding()
    governed_result = (
        binding.observation_selection_indeterminate_comparison_result_binding
        .indeterminate_media_type_comparison_result_binding
    )
    recorded_result = (
        binding.evaluation_record_indeterminate_media_type_comparison_result_binding
        .indeterminate_media_type_comparison_result_binding
    )
    assert recorded_result is governed_result


def test_complete_selection_and_evaluation_lineage_remains_reachable() -> None:
    binding = create_binding()
    governed = binding.observation_selection_indeterminate_comparison_result_binding
    recorded = (
        binding.evaluation_record_indeterminate_media_type_comparison_result_binding
    )
    selection = (
        governed.observation_selection_comparison_basis_binding
        .observation_selection_result
    )
    assert selection.selected_observation is not None
    assert recorded.evaluation_record.evaluation_identity is not None
    assert (
        recorded.evaluation_record.evaluation_identity.evaluation_basis
        == governed.indeterminate_media_type_comparison_result_binding.evaluation_basis
    )


def test_equal_reconstruction_has_value_equality() -> None:
    binding = create_binding()
    reconstructed = replace(
        binding,
        observation_selection_indeterminate_comparison_result_binding=replace(
            binding.observation_selection_indeterminate_comparison_result_binding
        ),
        evaluation_record_indeterminate_media_type_comparison_result_binding=replace(
            binding.evaluation_record_indeterminate_media_type_comparison_result_binding
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
        .evaluation_record_indeterminate_media_type_comparison_result_binding
    )
    with pytest.raises(
        TypeError,
        match=(
            "observation_selection_indeterminate_comparison_result_binding must be a "
            "SecurityAdmissionCandidateMediaTypeObservationSelection"
            "IndeterminateComparisonResultBinding"
        ),
    ):
        SecurityAdmissionEvaluationRecordMediaTypeObservationSelectionIndeterminateComparisonResultBinding(
            observation_selection_indeterminate_comparison_result_binding=(
                invalid_value  # type: ignore[arg-type]
            ),
            evaluation_record_indeterminate_media_type_comparison_result_binding=recorded,
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_recorded_binding_requires_nominal_type(
    invalid_value: object,
) -> None:
    governed = (
        create_binding().observation_selection_indeterminate_comparison_result_binding
    )
    with pytest.raises(
        TypeError,
        match=(
            "evaluation_record_indeterminate_media_type_comparison_result_binding "
            "must be a "
            "SecurityAdmissionEvaluationRecordIndeterminateMediaType"
            "ComparisonResultBinding"
        ),
    ):
        SecurityAdmissionEvaluationRecordMediaTypeObservationSelectionIndeterminateComparisonResultBinding(
            observation_selection_indeterminate_comparison_result_binding=governed,
            evaluation_record_indeterminate_media_type_comparison_result_binding=(
                invalid_value  # type: ignore[arg-type]
            ),
        )


def test_different_indeterminate_candidate_result_binding_is_rejected() -> None:
    governed = create_governed_binding()
    candidate_result_binding = (
        governed.indeterminate_media_type_comparison_result_binding
    )
    changed_result = replace(
        candidate_result_binding.indeterminate_media_type_comparison_result,
        result_version=(
            candidate_result_binding
            .indeterminate_media_type_comparison_result
            .result_version
            + 1
        ),
    )
    changed_candidate_result_binding = replace(
        candidate_result_binding,
        indeterminate_media_type_comparison_result=changed_result,
    )
    recorded = create_recorded_binding(
        indeterminate_media_type_comparison_result_binding=(
            changed_candidate_result_binding
        ),
    )
    with pytest.raises(
        ValueError,
        match=(
            "recorded indeterminate media-type result must use the governed "
            "comparison result binding"
        ),
    ):
        SecurityAdmissionEvaluationRecordMediaTypeObservationSelectionIndeterminateComparisonResultBinding(
            observation_selection_indeterminate_comparison_result_binding=governed,
            evaluation_record_indeterminate_media_type_comparison_result_binding=recorded,
        )


def test_contract_defines_no_coverage_decision_or_rejection() -> None:
    assert tuple(
        field.name
        for field in fields(
            SecurityAdmissionEvaluationRecordMediaTypeObservationSelectionIndeterminateComparisonResultBinding
        )
    ) == (
        "observation_selection_indeterminate_comparison_result_binding",
        "evaluation_record_indeterminate_media_type_comparison_result_binding",
    )


def test_contract_defines_validation_only() -> None:
    module = inspect.getmodule(
        SecurityAdmissionEvaluationRecordMediaTypeObservationSelectionIndeterminateComparisonResultBinding
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
        SecurityAdmissionEvaluationRecordMediaTypeObservationSelectionIndeterminateComparisonResultBinding
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    roots = {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    assert roots == {"dataclasses", "sp001"}
