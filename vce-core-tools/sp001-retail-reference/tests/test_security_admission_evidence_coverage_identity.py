import ast
import inspect
from dataclasses import FrozenInstanceError, fields, replace
from datetime import timedelta

import pytest

from sp001.contracts.security_admission_evaluation_record_policy_evidence_requirements_binding import (
    SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding,
)
from sp001.contracts.security_admission_evidence_coverage_identity import (
    SecurityAdmissionEvidenceCoverageIdentity,
)
from tests.test_security_admission_evaluation_record_policy_evidence_requirements_binding import (
    create_binding,
)


def create_identity() -> SecurityAdmissionEvidenceCoverageIdentity:
    return SecurityAdmissionEvidenceCoverageIdentity(
        coverage_id="coverage-001",
        coverage_version=1,
        evaluation_record_policy_evidence_requirements_binding=(
            create_binding()
        ),
    )


def test_coverage_identity_fields_are_exact() -> None:
    identity_fields = fields(SecurityAdmissionEvidenceCoverageIdentity)

    assert tuple(field.name for field in identity_fields) == (
        "coverage_id",
        "coverage_version",
        "evaluation_record_policy_evidence_requirements_binding",
    )
    assert identity_fields[0].type is str
    assert identity_fields[1].type is int
    assert (
        identity_fields[2].type
        is SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding
    )


def test_coverage_identity_is_immutable() -> None:
    identity = create_identity()

    with pytest.raises(FrozenInstanceError):
        identity.coverage_id = "coverage-002"  # type: ignore[misc]


def test_coverage_identity_uses_slots() -> None:
    identity = create_identity()

    assert hasattr(SecurityAdmissionEvidenceCoverageIdentity, "__slots__")
    assert not hasattr(identity, "__dict__")


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_coverage_id_requires_exact_type(invalid_value: object) -> None:
    binding = create_binding()

    with pytest.raises(TypeError, match="coverage_id must be a string"):
        SecurityAdmissionEvidenceCoverageIdentity(
            coverage_id=invalid_value,  # type: ignore[arg-type]
            coverage_version=1,
            evaluation_record_policy_evidence_requirements_binding=binding,
        )


@pytest.mark.parametrize("blank_value", ("", " ", "\t", "\n"))
def test_coverage_id_must_not_be_blank(blank_value: str) -> None:
    binding = create_binding()

    with pytest.raises(ValueError, match="coverage_id must not be blank"):
        SecurityAdmissionEvidenceCoverageIdentity(
            coverage_id=blank_value,
            coverage_version=1,
            evaluation_record_policy_evidence_requirements_binding=binding,
        )


@pytest.mark.parametrize(
    "invalid_value",
    (None, "1", 1.0, True, object()),
)
def test_coverage_version_requires_exact_type(
    invalid_value: object,
) -> None:
    binding = create_binding()

    with pytest.raises(
        TypeError,
        match="coverage_version must be an integer",
    ):
        SecurityAdmissionEvidenceCoverageIdentity(
            coverage_id="coverage-001",
            coverage_version=invalid_value,  # type: ignore[arg-type]
            evaluation_record_policy_evidence_requirements_binding=binding,
        )


@pytest.mark.parametrize("nonpositive_value", (0, -1, -100))
def test_coverage_version_must_be_positive(
    nonpositive_value: int,
) -> None:
    binding = create_binding()

    with pytest.raises(
        ValueError,
        match="coverage_version must be positive",
    ):
        SecurityAdmissionEvidenceCoverageIdentity(
            coverage_id="coverage-001",
            coverage_version=nonpositive_value,
            evaluation_record_policy_evidence_requirements_binding=binding,
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_record_requirements_binding_requires_exact_type(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "evaluation_record_policy_evidence_requirements_binding "
            "must be a "
            "SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding"
        ),
    ):
        SecurityAdmissionEvidenceCoverageIdentity(
            coverage_id="coverage-001",
            coverage_version=1,
            evaluation_record_policy_evidence_requirements_binding=(
                invalid_value  # type: ignore[arg-type]
            ),
        )


def test_exact_record_requirements_binding_reference_is_preserved() -> None:
    binding = create_binding()
    identity = SecurityAdmissionEvidenceCoverageIdentity(
        coverage_id="coverage-001",
        coverage_version=1,
        evaluation_record_policy_evidence_requirements_binding=binding,
    )

    assert (
        identity.evaluation_record_policy_evidence_requirements_binding
        is binding
    )


def test_reconstructed_equal_identity_has_value_equality() -> None:
    identity = create_identity()
    reconstructed = SecurityAdmissionEvidenceCoverageIdentity(
        coverage_id=identity.coverage_id,
        coverage_version=identity.coverage_version,
        evaluation_record_policy_evidence_requirements_binding=replace(
            identity.evaluation_record_policy_evidence_requirements_binding
        ),
    )

    assert reconstructed == identity
    assert reconstructed is not identity


def test_coverage_id_participates_in_identity_value() -> None:
    identity = create_identity()

    assert replace(identity, coverage_id="coverage-002") != identity


def test_coverage_version_participates_in_identity_value() -> None:
    identity = create_identity()

    assert replace(identity, coverage_version=2) != identity


def test_record_requirements_binding_participates_in_identity_value() -> None:
    identity = create_identity()
    binding = (
        identity.evaluation_record_policy_evidence_requirements_binding
    )
    different_record = replace(
        binding.evaluation_record,
        evaluated_at=(
            binding.evaluation_record.evaluated_at
            + timedelta(seconds=1)
        ),
    )
    different_binding = replace(
        binding,
        evaluation_record=different_record,
    )

    assert replace(
        identity,
        evaluation_record_policy_evidence_requirements_binding=(
            different_binding
        ),
    ) != identity


def test_evidence_and_domain_coverage_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(SecurityAdmissionEvidenceCoverageIdentity)
    }

    assert names.isdisjoint(
        {
            "evidence_binding",
            "evidence_bindings",
            "media_type_comparison_result_binding",
            "indeterminate_media_type_comparison_result_binding",
            "byte_length_comparison_result_binding",
            "indeterminate_byte_length_comparison_result_binding",
            "present_evidence_domains",
            "available_evidence_domains",
            "missing_evidence_domains",
            "coverage_status",
            "complete",
        }
    )


def test_occurrence_decision_and_authority_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(SecurityAdmissionEvidenceCoverageIdentity)
    }

    assert names.isdisjoint(
        {
            "covered_at",
            "evaluated_at",
            "actor",
            "procedure",
            "sufficient",
            "status",
            "decision",
            "reason",
            "admitted",
            "rejected",
            "authorized",
            "authorization",
            "quarantine",
            "retention",
            "effect",
        }
    )


def test_contract_performs_no_coverage_or_policy_execution() -> None:
    module = inspect.getmodule(SecurityAdmissionEvidenceCoverageIdentity)
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    function_names = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    assert function_names == {"__post_init__"}


def test_contract_imports_no_external_capability() -> None:
    module = inspect.getmodule(SecurityAdmissionEvidenceCoverageIdentity)
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
    source = inspect.getsource(SecurityAdmissionEvidenceCoverageIdentity)
    tree = ast.parse(source)
    calls = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }

    assert calls <= {
        "dataclass",
        "isinstance",
        "TypeError",
        "ValueError",
    }
