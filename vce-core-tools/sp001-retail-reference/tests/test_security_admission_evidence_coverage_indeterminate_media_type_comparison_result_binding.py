import ast
import inspect
from dataclasses import FrozenInstanceError, fields, replace
from datetime import timedelta

import pytest

from sp001.contracts.security_admission_evaluation_record_indeterminate_media_type_comparison_result_binding import (
    SecurityAdmissionEvaluationRecordIndeterminateMediaTypeComparisonResultBinding,
)
from sp001.contracts.security_admission_evaluation_record_policy_evidence_requirements_binding import (
    SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding,
)
from sp001.contracts.security_admission_evidence_coverage_identity import (
    SecurityAdmissionEvidenceCoverageIdentity,
)
from sp001.contracts.security_admission_evidence_coverage_indeterminate_media_type_comparison_result_binding import (
    SecurityAdmissionEvidenceCoverageIndeterminateMediaTypeComparisonResultBinding,
)
from tests.test_security_admission_candidate_indeterminate_media_type_comparison_result_binding import (
    create_binding as create_candidate_media_binding,
)
from tests.test_security_admission_evidence_coverage_identity import (
    create_identity,
)


def create_binding(
) -> SecurityAdmissionEvidenceCoverageIndeterminateMediaTypeComparisonResultBinding:
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
        SecurityAdmissionEvaluationRecordIndeterminateMediaTypeComparisonResultBinding(
            evaluation_record=record,
            indeterminate_media_type_comparison_result_binding=candidate_media,
        )
    )
    return (
        SecurityAdmissionEvidenceCoverageIndeterminateMediaTypeComparisonResultBinding(
            coverage_identity=coverage,
            evaluation_record_indeterminate_media_type_comparison_result_binding=(
                recorded_media
            ),
        )
    )


def test_binding_fields_are_exact() -> None:
    binding_fields = fields(
        SecurityAdmissionEvidenceCoverageIndeterminateMediaTypeComparisonResultBinding
    )
    assert tuple(field.name for field in binding_fields) == (
        "coverage_identity",
        "evaluation_record_indeterminate_media_type_comparison_result_binding",
    )
    assert binding_fields[0].type is SecurityAdmissionEvidenceCoverageIdentity
    assert (
        binding_fields[1].type
        is SecurityAdmissionEvaluationRecordIndeterminateMediaTypeComparisonResultBinding
    )


def test_binding_is_immutable() -> None:
    binding = create_binding()
    with pytest.raises(FrozenInstanceError):
        binding.coverage_identity = create_identity()  # type: ignore[misc]


def test_binding_uses_slots() -> None:
    binding = create_binding()
    assert hasattr(type(binding), "__slots__")
    assert not hasattr(binding, "__dict__")


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_coverage_identity_requires_nominal_type(
    invalid_value: object,
) -> None:
    recorded_media = (
        create_binding()
        .evaluation_record_indeterminate_media_type_comparison_result_binding
    )
    with pytest.raises(
        TypeError,
        match="coverage_identity must be a SecurityAdmissionEvidenceCoverageIdentity",
    ):
        SecurityAdmissionEvidenceCoverageIndeterminateMediaTypeComparisonResultBinding(
            coverage_identity=invalid_value,  # type: ignore[arg-type]
            evaluation_record_indeterminate_media_type_comparison_result_binding=(
                recorded_media
            ),
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_indeterminate_binding_requires_nominal_type(
    invalid_value: object,
) -> None:
    coverage = create_binding().coverage_identity
    with pytest.raises(
        TypeError,
        match=(
            "evaluation_record_indeterminate_media_type_comparison_result_binding "
            "must be a "
            "SecurityAdmissionEvaluationRecordIndeterminateMediaTypeComparisonResultBinding"
        ),
    ):
        SecurityAdmissionEvidenceCoverageIndeterminateMediaTypeComparisonResultBinding(
            coverage_identity=coverage,
            evaluation_record_indeterminate_media_type_comparison_result_binding=(
                invalid_value  # type: ignore[arg-type]
            ),
        )


def test_exact_references_are_preserved() -> None:
    binding = create_binding()
    coverage = binding.coverage_identity
    recorded = (
        binding.evaluation_record_indeterminate_media_type_comparison_result_binding
    )
    reconstructed = (
        SecurityAdmissionEvidenceCoverageIndeterminateMediaTypeComparisonResultBinding(
            coverage_identity=coverage,
            evaluation_record_indeterminate_media_type_comparison_result_binding=(
                recorded
            ),
        )
    )
    assert reconstructed.coverage_identity is coverage
    assert (
        reconstructed.evaluation_record_indeterminate_media_type_comparison_result_binding
        is recorded
    )


def test_reconstructed_equal_binding_has_value_equality() -> None:
    binding = create_binding()
    reconstructed = replace(
        binding,
        coverage_identity=replace(binding.coverage_identity),
        evaluation_record_indeterminate_media_type_comparison_result_binding=(
            replace(
                binding
                .evaluation_record_indeterminate_media_type_comparison_result_binding
            )
        ),
    )
    assert reconstructed == binding
    assert reconstructed is not binding


def test_equal_reconstructed_record_permits_binding() -> None:
    binding = create_binding()
    recorded = (
        binding.evaluation_record_indeterminate_media_type_comparison_result_binding
    )
    assert replace(
        binding,
        evaluation_record_indeterminate_media_type_comparison_result_binding=(
            replace(recorded, evaluation_record=replace(recorded.evaluation_record))
        ),
    ) == binding


def test_different_evaluation_instant_is_rejected() -> None:
    binding = create_binding()
    recorded = (
        binding.evaluation_record_indeterminate_media_type_comparison_result_binding
    )
    different_record = replace(
        recorded.evaluation_record,
        evaluated_at=recorded.evaluation_record.evaluated_at + timedelta(seconds=1),
    )
    with pytest.raises(
        ValueError,
        match=(
            "indeterminate media-type result binding must use "
            "coverage evaluation record"
        ),
    ):
        replace(
            binding,
            evaluation_record_indeterminate_media_type_comparison_result_binding=(
                replace(recorded, evaluation_record=different_record)
            ),
        )


def test_different_evaluation_identity_is_rejected() -> None:
    binding = create_binding()
    recorded = (
        binding.evaluation_record_indeterminate_media_type_comparison_result_binding
    )
    identity = recorded.evaluation_record.evaluation_identity
    different_record = replace(
        recorded.evaluation_record,
        evaluation_identity=replace(
            identity,
            evaluation_version=identity.evaluation_version + 1,
        ),
    )
    with pytest.raises(ValueError, match="coverage evaluation record"):
        replace(
            binding,
            evaluation_record_indeterminate_media_type_comparison_result_binding=(
                replace(recorded, evaluation_record=different_record)
            ),
        )


def test_coverage_version_participates_in_binding_value() -> None:
    binding = create_binding()
    changed_coverage = replace(
        binding.coverage_identity,
        coverage_version=binding.coverage_identity.coverage_version + 1,
    )
    assert replace(binding, coverage_identity=changed_coverage) != binding


def test_indeterminate_result_participates_in_binding_value() -> None:
    binding = create_binding()
    recorded = (
        binding.evaluation_record_indeterminate_media_type_comparison_result_binding
    )
    candidate_binding = (
        recorded.indeterminate_media_type_comparison_result_binding
    )
    result = candidate_binding.indeterminate_media_type_comparison_result
    changed_candidate_binding = replace(
        candidate_binding,
        indeterminate_media_type_comparison_result=replace(
            result, result_version=result.result_version + 1
        ),
    )
    changed_recorded = replace(
        recorded,
        indeterminate_media_type_comparison_result_binding=changed_candidate_binding,
    )
    assert replace(
        binding,
        evaluation_record_indeterminate_media_type_comparison_result_binding=(
            changed_recorded
        ),
    ) != binding


def test_reason_and_determined_at_remain_in_complete_result() -> None:
    binding = create_binding()
    result = (
        binding
        .evaluation_record_indeterminate_media_type_comparison_result_binding
        .indeterminate_media_type_comparison_result_binding
        .indeterminate_media_type_comparison_result
    )
    assert result.reason is not None
    assert result.determined_at is not None
    assert "reason" not in {field.name for field in fields(type(binding))}
    assert "determined_at" not in {field.name for field in fields(type(binding))}


@pytest.mark.parametrize(
    "reason_name",
    ("UNSUPPORTED_COMPARISON_SCHEME", "NONCOMPARABLE_MEDIA_TYPE_EVIDENCE"),
)
def test_indeterminacy_reasons_remain_uninterpreted(reason_name: str) -> None:
    binding = create_binding()
    recorded = (
        binding.evaluation_record_indeterminate_media_type_comparison_result_binding
    )
    candidate_binding = (
        recorded.indeterminate_media_type_comparison_result_binding
    )
    result = candidate_binding.indeterminate_media_type_comparison_result
    reason = type(result.reason)[reason_name]
    changed_candidate_binding = replace(
        candidate_binding,
        indeterminate_media_type_comparison_result=replace(result, reason=reason),
    )
    preserved = replace(
        binding,
        evaluation_record_indeterminate_media_type_comparison_result_binding=(
            replace(
                recorded,
                indeterminate_media_type_comparison_result_binding=(
                    changed_candidate_binding
                ),
            )
        ),
    )
    preserved_result = (
        preserved
        .evaluation_record_indeterminate_media_type_comparison_result_binding
        .indeterminate_media_type_comparison_result_binding
        .indeterminate_media_type_comparison_result
    )
    assert preserved_result.reason is reason
    assert preserved_result.determined_at is result.determined_at


def test_requirements_binding_cannot_occupy_indeterminate_slot() -> None:
    binding = create_binding()
    with pytest.raises(TypeError):
        replace(
            binding,
            evaluation_record_indeterminate_media_type_comparison_result_binding=(
                binding.coverage_identity
                .evaluation_record_policy_evidence_requirements_binding
            ),
        )


def test_rejection_classification_and_authority_fields_are_absent() -> None:
    names = {field.name for field in fields(
        SecurityAdmissionEvidenceCoverageIndeterminateMediaTypeComparisonResultBinding
    )}
    assert names.isdisjoint({
        "present_evidence_domains",
        "missing_evidence_domains",
        "coverage_status",
        "sufficient",
        "decision",
        "rejected",
        "admitted",
        "authorized",
        "authorization",
        "quarantine",
        "retention",
    })


def test_contract_defines_validation_only() -> None:
    module = inspect.getmodule(
        SecurityAdmissionEvidenceCoverageIndeterminateMediaTypeComparisonResultBinding
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    functions = {
        node.name for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    assert functions == {"__post_init__"}
    calls = {
        node.func.id for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    assert calls <= {"dataclass", "isinstance", "TypeError", "ValueError"}


def test_contract_imports_no_external_capability() -> None:
    module = inspect.getmodule(
        SecurityAdmissionEvidenceCoverageIndeterminateMediaTypeComparisonResultBinding
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    roots = {
        node.module.split(".")[0] for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    assert roots == {"dataclasses", "sp001"}
