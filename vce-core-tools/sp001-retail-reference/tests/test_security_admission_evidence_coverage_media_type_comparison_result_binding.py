import ast
import inspect
from dataclasses import FrozenInstanceError, fields, replace
from datetime import timedelta

import pytest

from sp001.contracts.security_admission_evaluation_record_media_type_comparison_result_binding import (
    SecurityAdmissionEvaluationRecordMediaTypeComparisonResultBinding,
)
from sp001.contracts.security_admission_evaluation_record_policy_evidence_requirements_binding import (
    SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding,
)
from sp001.contracts.security_admission_evidence_coverage_identity import (
    SecurityAdmissionEvidenceCoverageIdentity,
)
from sp001.contracts.security_admission_evidence_coverage_media_type_comparison_result_binding import (
    SecurityAdmissionEvidenceCoverageMediaTypeComparisonResultBinding,
)
from tests.test_security_admission_candidate_media_type_comparison_result_binding import (
    create_binding as create_candidate_media_binding,
)
from tests.test_security_admission_evidence_coverage_identity import (
    create_identity,
)


def create_binding(
) -> SecurityAdmissionEvidenceCoverageMediaTypeComparisonResultBinding:
    candidate_media = create_candidate_media_binding()
    initial_coverage = create_identity()
    initial_requirements_binding = (
        initial_coverage.evaluation_record_policy_evidence_requirements_binding
    )
    record = initial_requirements_binding.evaluation_record
    record = replace(
        record,
        evaluation_identity=replace(
            record.evaluation_identity,
            evaluation_basis=candidate_media.evaluation_basis,
        ),
    )
    requirements = replace(
        initial_requirements_binding.policy_evidence_requirements,
        admission_policy_identity=(
            candidate_media.evaluation_basis.admission_policy_identity
        ),
    )
    requirements_binding = (
        SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding(
            evaluation_record=record,
            policy_evidence_requirements=requirements,
        )
    )
    coverage = replace(
        initial_coverage,
        evaluation_record_policy_evidence_requirements_binding=(
            requirements_binding
        ),
    )
    recorded_media = (
        SecurityAdmissionEvaluationRecordMediaTypeComparisonResultBinding(
            evaluation_record=record,
            media_type_comparison_result_binding=candidate_media,
        )
    )
    return SecurityAdmissionEvidenceCoverageMediaTypeComparisonResultBinding(
        coverage_identity=coverage,
        evaluation_record_media_type_comparison_result_binding=recorded_media,
    )


def test_binding_fields_are_exact() -> None:
    binding_fields = fields(
        SecurityAdmissionEvidenceCoverageMediaTypeComparisonResultBinding
    )

    assert tuple(field.name for field in binding_fields) == (
        "coverage_identity",
        "evaluation_record_media_type_comparison_result_binding",
    )
    assert binding_fields[0].type is SecurityAdmissionEvidenceCoverageIdentity
    assert (
        binding_fields[1].type
        is SecurityAdmissionEvaluationRecordMediaTypeComparisonResultBinding
    )


def test_binding_is_immutable() -> None:
    binding = create_binding()

    with pytest.raises(FrozenInstanceError):
        binding.coverage_identity = create_identity()  # type: ignore[misc]


def test_binding_uses_slots() -> None:
    binding = create_binding()

    assert hasattr(
        SecurityAdmissionEvidenceCoverageMediaTypeComparisonResultBinding,
        "__slots__",
    )
    assert not hasattr(binding, "__dict__")


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_coverage_identity_requires_nominal_type(
    invalid_value: object,
) -> None:
    recorded_media = (
        create_binding()
        .evaluation_record_media_type_comparison_result_binding
    )

    with pytest.raises(
        TypeError,
        match="coverage_identity must be a SecurityAdmissionEvidenceCoverageIdentity",
    ):
        SecurityAdmissionEvidenceCoverageMediaTypeComparisonResultBinding(
            coverage_identity=invalid_value,  # type: ignore[arg-type]
            evaluation_record_media_type_comparison_result_binding=(
                recorded_media
            ),
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_recorded_media_binding_requires_nominal_type(
    invalid_value: object,
) -> None:
    coverage = create_binding().coverage_identity

    with pytest.raises(
        TypeError,
        match=(
            "evaluation_record_media_type_comparison_result_binding must be a "
            "SecurityAdmissionEvaluationRecordMediaTypeComparisonResultBinding"
        ),
    ):
        SecurityAdmissionEvidenceCoverageMediaTypeComparisonResultBinding(
            coverage_identity=coverage,
            evaluation_record_media_type_comparison_result_binding=(
                invalid_value  # type: ignore[arg-type]
            ),
        )


def test_exact_coverage_identity_reference_is_preserved() -> None:
    binding = create_binding()
    coverage = binding.coverage_identity
    reconstructed = replace(binding, coverage_identity=coverage)

    assert reconstructed.coverage_identity is coverage


def test_exact_recorded_evidence_reference_is_preserved() -> None:
    binding = create_binding()
    recorded_media = (
        binding.evaluation_record_media_type_comparison_result_binding
    )
    reconstructed = replace(
        binding,
        evaluation_record_media_type_comparison_result_binding=recorded_media,
    )

    assert (
        reconstructed.evaluation_record_media_type_comparison_result_binding
        is recorded_media
    )


def test_reconstructed_equal_binding_has_value_equality() -> None:
    binding = create_binding()
    reconstructed = (
        SecurityAdmissionEvidenceCoverageMediaTypeComparisonResultBinding(
            coverage_identity=replace(binding.coverage_identity),
            evaluation_record_media_type_comparison_result_binding=replace(
                binding.evaluation_record_media_type_comparison_result_binding
            ),
        )
    )

    assert reconstructed == binding
    assert reconstructed is not binding


def test_equal_reconstructed_evaluation_record_permits_binding() -> None:
    binding = create_binding()
    recorded_media = (
        binding.evaluation_record_media_type_comparison_result_binding
    )
    reconstructed_recorded_media = replace(
        recorded_media,
        evaluation_record=replace(recorded_media.evaluation_record),
    )

    assert (
        SecurityAdmissionEvidenceCoverageMediaTypeComparisonResultBinding(
            coverage_identity=binding.coverage_identity,
            evaluation_record_media_type_comparison_result_binding=(
                reconstructed_recorded_media
            ),
        )
        == binding
    )


def test_different_evaluation_instant_is_rejected() -> None:
    binding = create_binding()
    recorded_media = (
        binding.evaluation_record_media_type_comparison_result_binding
    )
    different_record = replace(
        recorded_media.evaluation_record,
        evaluated_at=(
            recorded_media.evaluation_record.evaluated_at
            + timedelta(seconds=1)
        ),
    )

    with pytest.raises(
        ValueError,
        match="media-type result binding must use coverage evaluation record",
    ):
        SecurityAdmissionEvidenceCoverageMediaTypeComparisonResultBinding(
            coverage_identity=binding.coverage_identity,
            evaluation_record_media_type_comparison_result_binding=replace(
                recorded_media,
                evaluation_record=different_record,
            ),
        )


def test_different_evaluation_identity_is_rejected() -> None:
    binding = create_binding()
    recorded_media = (
        binding.evaluation_record_media_type_comparison_result_binding
    )
    record = recorded_media.evaluation_record
    different_record = replace(
        record,
        evaluation_identity=replace(
            record.evaluation_identity,
            evaluation_version=record.evaluation_identity.evaluation_version + 1,
        ),
    )

    with pytest.raises(
        ValueError,
        match="media-type result binding must use coverage evaluation record",
    ):
        SecurityAdmissionEvidenceCoverageMediaTypeComparisonResultBinding(
            coverage_identity=binding.coverage_identity,
            evaluation_record_media_type_comparison_result_binding=replace(
                recorded_media,
                evaluation_record=different_record,
            ),
        )


def test_coverage_identity_participates_in_binding_value() -> None:
    binding = create_binding()
    different_coverage = replace(
        binding.coverage_identity,
        coverage_version=binding.coverage_identity.coverage_version + 1,
    )

    assert replace(binding, coverage_identity=different_coverage) != binding


def test_recorded_evidence_participates_in_binding_value() -> None:
    binding = create_binding()
    recorded_media = (
        binding.evaluation_record_media_type_comparison_result_binding
    )
    changed_candidate_binding = replace(
        recorded_media.media_type_comparison_result_binding,
        media_type_comparison_result=replace(
            recorded_media
            .media_type_comparison_result_binding
            .media_type_comparison_result,
            result_version=(
                recorded_media
                .media_type_comparison_result_binding
                .media_type_comparison_result
                .result_version + 1
            ),
        ),
    )
    different_recorded_media = replace(
        recorded_media,
        media_type_comparison_result_binding=changed_candidate_binding,
    )

    assert replace(
        binding,
        evaluation_record_media_type_comparison_result_binding=(
            different_recorded_media
        ),
    ) != binding


def test_requirements_binding_cannot_occupy_recorded_evidence_slot() -> None:
    binding = create_binding()
    requirements_binding = (
        binding.coverage_identity
        .evaluation_record_policy_evidence_requirements_binding
    )

    with pytest.raises(TypeError):
        SecurityAdmissionEvidenceCoverageMediaTypeComparisonResultBinding(
            coverage_identity=binding.coverage_identity,
            evaluation_record_media_type_comparison_result_binding=(
                requirements_binding  # type: ignore[arg-type]
            ),
        )


def test_classification_decision_and_authority_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(
            SecurityAdmissionEvidenceCoverageMediaTypeComparisonResultBinding
        )
    }

    assert names.isdisjoint({
        "evaluation_record",
        "policy_evidence_requirements",
        "required_evidence_domains",
        "present_evidence_domains",
        "missing_evidence_domains",
        "coverage_status",
        "sufficient",
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
        SecurityAdmissionEvidenceCoverageMediaTypeComparisonResultBinding
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    functions = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    assert functions == {"__post_init__"}

    calls = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    assert calls <= {"dataclass", "isinstance", "TypeError", "ValueError"}


def test_contract_imports_no_external_capability() -> None:
    module = inspect.getmodule(
        SecurityAdmissionEvidenceCoverageMediaTypeComparisonResultBinding
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    roots = {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    assert roots == {"dataclasses", "sp001"}
