import ast
import inspect

from dataclasses import FrozenInstanceError, fields, replace

import pytest

from sp001.contracts.security_admission_evaluation_record_byte_length_observation_selection_comparison_result_binding import (
    SecurityAdmissionEvaluationRecordByteLengthObservationSelectionComparisonResultBinding,
)
from sp001.contracts.security_admission_evaluation_record_policy_evidence_requirements_binding import (
    SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding,
)
from sp001.contracts.security_admission_evidence_coverage_byte_length_comparison_result_binding import (
    SecurityAdmissionEvidenceCoverageByteLengthComparisonResultBinding,
)
from sp001.contracts.security_admission_evidence_coverage_byte_length_observation_selection_comparison_result_binding import (
    SecurityAdmissionEvidenceCoverageByteLengthObservationSelectionComparisonResultBinding,
)
from tests.test_security_admission_evaluation_record_byte_length_observation_selection_comparison_result_binding import (
    create_binding as create_governed_recorded_binding,
)
from tests.test_security_admission_evidence_coverage_byte_length_comparison_result_binding import (
    create_binding as create_initial_coverage_binding,
)


def create_binding(
) -> SecurityAdmissionEvidenceCoverageByteLengthObservationSelectionComparisonResultBinding:
    governed_recorded = create_governed_recorded_binding()
    recorded = (
        governed_recorded
        .evaluation_record_byte_length_comparison_result_binding
    )
    initial_coverage_binding = create_initial_coverage_binding()
    initial_coverage = initial_coverage_binding.coverage_identity
    initial_requirements_binding = (
        initial_coverage
        .evaluation_record_policy_evidence_requirements_binding
    )
    policy_identity = (
        recorded.evaluation_record
        .evaluation_identity
        .evaluation_basis
        .admission_policy_identity
    )
    requirements = replace(
        initial_requirements_binding.policy_evidence_requirements,
        admission_policy_identity=policy_identity,
    )
    requirements_binding = (
        SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding(
            evaluation_record=recorded.evaluation_record,
            policy_evidence_requirements=requirements,
        )
    )
    coverage_identity = replace(
        initial_coverage,
        evaluation_record_policy_evidence_requirements_binding=(
            requirements_binding
        ),
    )
    coverage_binding = (
        SecurityAdmissionEvidenceCoverageByteLengthComparisonResultBinding(
            coverage_identity=coverage_identity,
            evaluation_record_byte_length_comparison_result_binding=recorded,
        )
    )
    return (
        SecurityAdmissionEvidenceCoverageByteLengthObservationSelectionComparisonResultBinding(
            evaluation_record_byte_length_observation_selection_comparison_result_binding=(
                governed_recorded
            ),
            evidence_coverage_byte_length_comparison_result_binding=(
                coverage_binding
            ),
        )
    )


def test_fields_are_exact() -> None:
    binding_fields = fields(
        SecurityAdmissionEvidenceCoverageByteLengthObservationSelectionComparisonResultBinding
    )
    assert tuple(field.name for field in binding_fields) == (
        "evaluation_record_byte_length_observation_selection_comparison_result_binding",
        "evidence_coverage_byte_length_comparison_result_binding",
    )
    assert (
        binding_fields[0].type
        is SecurityAdmissionEvaluationRecordByteLengthObservationSelectionComparisonResultBinding
    )
    assert (
        binding_fields[1].type
        is SecurityAdmissionEvidenceCoverageByteLengthComparisonResultBinding
    )


def test_binding_is_immutable_and_slotted() -> None:
    binding = create_binding()
    assert not hasattr(binding, "__dict__")
    with pytest.raises(FrozenInstanceError):
        binding.evidence_coverage_byte_length_comparison_result_binding = (  # type: ignore[misc]
            create_initial_coverage_binding()
        )


def test_exact_references_are_preserved() -> None:
    binding = create_binding()
    governed = (
        binding
        .evaluation_record_byte_length_observation_selection_comparison_result_binding
    )
    coverage = (
        binding.evidence_coverage_byte_length_comparison_result_binding
    )
    reconstructed = (
        SecurityAdmissionEvidenceCoverageByteLengthObservationSelectionComparisonResultBinding(
            evaluation_record_byte_length_observation_selection_comparison_result_binding=(
                governed
            ),
            evidence_coverage_byte_length_comparison_result_binding=coverage,
        )
    )
    assert (
        reconstructed
        .evaluation_record_byte_length_observation_selection_comparison_result_binding
        is governed
    )
    assert (
        reconstructed
        .evidence_coverage_byte_length_comparison_result_binding
        is coverage
    )


def test_governed_recorded_result_is_preserved_in_coverage() -> None:
    binding = create_binding()
    governed_recorded = (
        binding
        .evaluation_record_byte_length_observation_selection_comparison_result_binding
        .evaluation_record_byte_length_comparison_result_binding
    )
    covered_recorded = (
        binding.evidence_coverage_byte_length_comparison_result_binding
        .evaluation_record_byte_length_comparison_result_binding
    )
    assert covered_recorded is governed_recorded


def test_complete_selection_evaluation_and_coverage_lineage_is_reachable() -> None:
    binding = create_binding()
    governed = (
        binding
        .evaluation_record_byte_length_observation_selection_comparison_result_binding
    )
    coverage = (
        binding.evidence_coverage_byte_length_comparison_result_binding
    )
    selection = (
        governed.observation_selection_comparison_result_binding
        .observation_selection_comparison_basis_binding
        .observation_selection_result
    )
    recorded = (
        governed.evaluation_record_byte_length_comparison_result_binding
    )
    coverage_record = (
        coverage.coverage_identity
        .evaluation_record_policy_evidence_requirements_binding
        .evaluation_record
    )
    assert selection.selected_observation is not None
    assert coverage_record is recorded.evaluation_record


def test_equal_reconstruction_has_value_equality() -> None:
    binding = create_binding()
    reconstructed = replace(
        binding,
        evaluation_record_byte_length_observation_selection_comparison_result_binding=replace(
            binding
            .evaluation_record_byte_length_observation_selection_comparison_result_binding
        ),
        evidence_coverage_byte_length_comparison_result_binding=replace(
            binding.evidence_coverage_byte_length_comparison_result_binding
        ),
    )
    assert reconstructed == binding
    assert reconstructed is not binding


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_governed_recorded_binding_requires_nominal_type(
    invalid_value: object,
) -> None:
    coverage = (
        create_binding()
        .evidence_coverage_byte_length_comparison_result_binding
    )
    with pytest.raises(
        TypeError,
        match=(
            "evaluation_record_byte_length_observation_selection_"
            "comparison_result_binding must be a "
            "SecurityAdmissionEvaluationRecordByteLength"
            "ObservationSelectionComparisonResultBinding"
        ),
    ):
        SecurityAdmissionEvidenceCoverageByteLengthObservationSelectionComparisonResultBinding(
            evaluation_record_byte_length_observation_selection_comparison_result_binding=(
                invalid_value  # type: ignore[arg-type]
            ),
            evidence_coverage_byte_length_comparison_result_binding=coverage,
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_coverage_binding_requires_nominal_type(
    invalid_value: object,
) -> None:
    governed = (
        create_binding()
        .evaluation_record_byte_length_observation_selection_comparison_result_binding
    )
    with pytest.raises(
        TypeError,
        match=(
            "evidence_coverage_byte_length_comparison_result_binding "
            "must be a "
            "SecurityAdmissionEvidenceCoverageByteLength"
            "ComparisonResultBinding"
        ),
    ):
        SecurityAdmissionEvidenceCoverageByteLengthObservationSelectionComparisonResultBinding(
            evaluation_record_byte_length_observation_selection_comparison_result_binding=(
                governed
            ),
            evidence_coverage_byte_length_comparison_result_binding=(
                invalid_value  # type: ignore[arg-type]
            ),
        )


def test_different_recorded_result_binding_is_rejected() -> None:
    binding = create_binding()
    coverage = (
        binding.evidence_coverage_byte_length_comparison_result_binding
    )
    recorded = (
        coverage.evaluation_record_byte_length_comparison_result_binding
    )
    candidate_binding = recorded.byte_length_comparison_result_binding
    changed_result = replace(
        candidate_binding.byte_length_comparison_result,
        result_version=(
            candidate_binding.byte_length_comparison_result.result_version + 1
        ),
    )
    changed_candidate_binding = replace(
        candidate_binding,
        byte_length_comparison_result=changed_result,
    )
    changed_recorded = replace(
        recorded,
        byte_length_comparison_result_binding=changed_candidate_binding,
    )
    changed_coverage = replace(
        coverage,
        evaluation_record_byte_length_comparison_result_binding=(
            changed_recorded
        ),
    )
    with pytest.raises(
        ValueError,
        match=(
            "byte-length evidence coverage must use the governed "
            "recorded comparison result binding"
        ),
    ):
        SecurityAdmissionEvidenceCoverageByteLengthObservationSelectionComparisonResultBinding(
            evaluation_record_byte_length_observation_selection_comparison_result_binding=(
                binding
                .evaluation_record_byte_length_observation_selection_comparison_result_binding
            ),
            evidence_coverage_byte_length_comparison_result_binding=(
                changed_coverage
            ),
        )


def test_contract_defines_no_completion_decision_or_rejection() -> None:
    assert tuple(
        field.name
        for field in fields(
            SecurityAdmissionEvidenceCoverageByteLengthObservationSelectionComparisonResultBinding
        )
    ) == (
        "evaluation_record_byte_length_observation_selection_comparison_result_binding",
        "evidence_coverage_byte_length_comparison_result_binding",
    )


def test_contract_defines_validation_only() -> None:
    module = inspect.getmodule(
        SecurityAdmissionEvidenceCoverageByteLengthObservationSelectionComparisonResultBinding
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
        SecurityAdmissionEvidenceCoverageByteLengthObservationSelectionComparisonResultBinding
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    roots = {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    assert roots == {"dataclasses", "sp001"}
